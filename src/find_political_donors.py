#Uses python3

import sys
from utils.recorder import Recorder
from collections import defaultdict
import time
import datetime

def main():
    file_dir = sys.argv[1] #input dir
    zip_dir = sys.argv[2] #output dir1
    date_dir = sys.argv[3] #ourput dir2

    fh = open(file_dir, mode = 'rt')
    zip_file = open(zip_dir, mode = 'wt')
    date_file = open(date_dir, mode = 'wt')

    streamer = Streamer()
    zip_dic, date_dic = streamer.stream(fh, zip_file, date_file)
    streamer.process_date(date_dic, date_file)

class Streamer(object):
    def __init__(self):
        #indices for CMTE_ID, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID
        self.indices = [0, 10, 13, 14, 15]

        #variables to track the invalid(skipped) lines,
        #invalid zips and invalid dates.
        self.invalid, self.inv_zip, self.inv_date = 0, 0, 0

        ###########################################################################
        #  Create two dictionaries for zip and dates respectively.                #
        #                                                                         #
        #  Two level dictionary, 1st level uses CMTE_ID as key, a corresponding   #
        #  dictionary as value, 2nd level uses ZIP_CODE/TRANSACTION_DT as key,    #
        #  and a self-defined Recorder class as value.                            #
        #                                                                         #
        #  Recorder is responsible for recording the streamed in TRANSACTION_AMT  #
        #  and calculate the running median, total transactions and total amount. #
        ###########################################################################
        self.zip_dic = defaultdict(lambda : defaultdict(Recorder))
        self.date_dic = defaultdict(lambda : defaultdict(Recorder))

    def stream(self, fh, zip_file, date_file):
        """
        Stream the input file and record/calculate median, total transcations,
        and total amounts. Meanwhile also write into the zip_file.
        input: file handles
        output:
            zip_dic: dictionary
                2 level dictionary contains records for (CMTE_ID, ZIP_CODE)
            date_dic: dictionary
                2 level dictionary contains records for (CMTE_ID, TRANSACTION_DT)
        """
        #record time needed for streamig
        begin = time.time()

        #streaming the input file
        for line in fh:
            fields = line.split('|')

            #make sure each line conforms to the description.
            assert len(fields) == 21, print("Not 21 fields:", line, sep = '\n')

            #map out the interested fields.
            items = list(map(lambda x: fields[x], self.indices))
            CMTE_ID, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID = items


            if check_invalid(OTHER_ID, CMTE_ID, TRANSACTION_AMT):
                self.invalid += 1
                continue


            ZIP_CODE = ZIP_CODE[:5]
            if check_zip(ZIP_CODE):
                cur_recorder = self.zip_dic[CMTE_ID][ZIP_CODE]
                cur_recorder.record(float(TRANSACTION_AMT))
                #write streamed out line to medianvals_by_zip.txt
                write_file(CMTE_ID, ZIP_CODE, cur_recorder, zip_file)
            else:
                self.inv_zip += 1


            if check_date(TRANSACTION_DT):
                cur_recorder = self.date_dic[CMTE_ID][TRANSACTION_DT]
                cur_recorder.record(float(TRANSACTION_AMT))
            else:
                self.inv_date += 1

        zip_file.close()
        end = time.time()
        print('invalid: %d, inv_zip: %d, inv_date: %d' % (self.invalid, self.inv_zip, self.inv_date))
        print('medianvals_by_zip.txt generated in %f s' % (end - begin))

        return self.zip_dic, self.date_dic

    def process_date(self, date_dic, date_file):
        """
        sort date_dic alphabetically and chronologically and write into the file.
        input:
            date_dic: dictionary
            date_file: file handle
        output:
            void
        """
        begin = time.time()
        IDs = sorted(date_dic.keys()) #sort alphabetically
        for ID in IDs:
            #sort chronologically
            dates = sorted(date_dic[ID].keys(), key=lambda x: x[4:] + x[:4])
            for date in dates:
                cur_recorder = date_dic[ID][date]
                write_file(ID, date, cur_recorder, date_file)
        date_file.close()
        end = time.time()
        print('medianvals_by_date.txt generated in %f s' % (end - begin))

def check_invalid(OTHER_ID, CMTE_ID, TRANSACTION_AMT):
    """
    check if OTHER_ID is not '', or CMTE_ID is '', or
    TRANSACTION_AMT is ''.
    input: str
    output: boolean
    """
    return True if OTHER_ID or not CMTE_ID or not TRANSACTION_AMT else False

def check_zip(ZIP_CODE):
    """
    check whether ZIP_CODE is valid or not.
    input: str
    output: boolean
    """
    return True if len(ZIP_CODE) == 5 and ZIP_CODE.isnumeric() else False

def check_date(TRANSACTION_DT):
    """
    check whether TRANSACTION_DT is a valid date or not by datetime.date class.
    input: str
    output: boolean
    """
    try:
        assert len(TRANSACTION_DT) == 8
        new_date = datetime.date(int(TRANSACTION_DT[4:]),
                                 int(TRANSACTION_DT[:2]),
                                 int(TRANSACTION_DT[2:4]))
        return True
    except (AssertionError, ValueError):
        return False

def write_file(ID, field, recorder, file):
    """
    calculate median, total transactions and amount in the recorder so far,
    and write into file.
    input:
        ID: str
            CMTE_ID
        field: str
            ZIP_CODE or TRANSACTION_DT
        recorder: Recorder
        file: file handle
    output:
        void
    """
    median, total_tran, total_amt = recorder.indicate()
    new_line = '|'.join([ID, field, str(median), str(total_tran),
                        str(total_amt)])
    file.write(new_line + '\n')

if __name__ == '__main__':
    main()
