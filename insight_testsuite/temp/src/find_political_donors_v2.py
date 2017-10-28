import sys
from utils.recorder import Recorder
from collections import defaultdict
import time
import datetime

def main():
    file_dir = sys.argv[1] #input dir
    zip_dir = sys.argv[2] #output dir
    date_dir = sys.argv[3] #ourput dir

    #open file handles
    fh = open(file_dir, mode = 'rt')
    zip_file = open(zip_dir, mode = 'wt')
    date_file = open(date_dir, mode = 'wt')

    #indices for CMTE_ID, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID
    indices = [0, 10, 13, 14, 15]

    #two level dictionary, 1st level uses CMTE_ID as key, a corresponding
    #dictionary as value, 2nd level uses ZIP_CODE/TRANSACTION_DT as key,
    #and a self-defined Recorder class as value.
    #Recorder is responsible for recording the streamed in TRANSACTION_AMT and
    #calculate the running median, total transactions and total amount.
    #Create two dictionaries for zip and dates respectively.
    zip_dic = defaultdict(lambda : defaultdict(Recorder))
    date_dic = defaultdict(lambda : defaultdict(Recorder))

    #variables to track the invalid(skipped) lines, invalid zips and invalid dates.
    invalid, inv_zip, inv_date = 0, 0, 0

    begin = time.time() #record the running time

    #iterating/streaming the input file
    for line in fh:
        fields = line.split('|')
        if len(fields) != 21: #make sure each line contains the right information
            invalid += 1
            continue
        items = list(map(lambda x: fields[x], indices)) #map out the interested fields
        CMTE_ID, ZIP_CODE, TRANSACTION_DT, TRANSACTION_AMT, OTHER_ID = items

        #skip this line if OTHER_ID is not '', or CMTE_ID is '', or
        #TRANSACTION_AMT is ''.
        if OTHER_ID or not CMTE_ID or not TRANSACTION_AMT:
            invalid += 1
            continue

        ZIP_CODE = ZIP_CODE[:5]
        #only record ZIP_CODE that has length >= 5 and is numeric.
        if len(ZIP_CODE) == 5 and ZIP_CODE.isnumeric():
            cur_recorder = zip_dic[CMTE_ID][ZIP_CODE]
            #record streamed in TRANSACTION_AMT
            cur_recorder.record(float(TRANSACTION_AMT))
            write_file(CMTE_ID, ZIP_CODE, cur_recorder, zip_file)
        else:
            inv_zip += 1

        #only record TRANSACTION_DT that conforms to built in datetime.date class
        try:
            assert len(TRANSACTION_DT) == 8
            new_date = datetime.date(int(TRANSACTION_DT[4:]),
                                     int(TRANSACTION_DT[:2]),
                                     int(TRANSACTION_DT[2:4]))
            cur_recorder = date_dic[CMTE_ID][TRANSACTION_DT]
            cur_recorder.record(float(TRANSACTION_AMT))
        #only catches errors in assert and datetime.date statements
        except (AssertionError, ValueError):
            inv_date += 1
    zip_file.close()
    end = time.time()
    print('invalid: %d, inv_zip: %d, inv_date: %d' % (invalid, inv_zip, inv_date))
    print('medianvals_by_zip.txt generated in %f s' % (end - begin))

    begin = time.time()
    #begin to write medianvals_by_date.txt
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

def write_file(ID, field, recorder, file):
    """calculate median, total transactions and amount in the recorder so far,
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
    new_line = '|'.join([ID, field, str(median),str(total_tran), str(total_amt)])
    file.write(new_line + '\n')

if __name__ == '__main__':
    main()
