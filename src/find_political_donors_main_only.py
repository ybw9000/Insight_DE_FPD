#Uses python3

import sys
from collections import defaultdict
from utils.streamer import *
import time
import datetime
import heapq

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

if __name__ == '__main__':
    main()
