# coding=utf-8
import csv
from datetime import datetime
import os
import time  # for time delay with sleep() function.

from coin_utils import get_details

def main():
    print 'hello world!'
    # filename e.g. 20170703-btc-details.csv
    # 현시각, 가격, 매도가, 매수가, 지난 24시간 기준 최고가 최저가, 거래 볼륨
    
    status, details = get_details()
    if status != 200:
        print 'status: %s, text: %s \nFailure from the start. Exit.' % (status, details)
        exit()
    while True:
        local_time = datetime.fromtimestamp(float(details[u'timestamp']) / 1000.0)
        date_str = local_time.strftime('%Y%m%d')
        filename = date_str + '-btc-details.csv'
        writing_mode = 'w'
        if os.path.isfile(filename):
            print 'There is the file ' + filename + ' So appending...'
            writing_mode = 'a'
        else:
            print 'Writing new file ' + filename

        with open(filename, writing_mode) as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=details.keys())
            if writing_mode == 'w':
                print 'Writing header.'
                writer.writeheader()
            writer.writerow(details)
            while True:
                time.sleep(2)
                status, new_details = get_details()
                if status != 200:
                    print 'code: %s, text: %s \nFailed to fetch the data. Skipping...' % (status, details)
                    continue
                if details[u'timestamp'] == new_details[u'timestamp']:
                    continue
                local_time = datetime.fromtimestamp(float(new_details[u'timestamp']) / 1000.0)
                new_date_str = local_time.strftime('%Y%m%d')
                if date_str == new_date_str:
                    print 'New data found. Writing down...%s' % new_details[u'timestamp']
                    writer.writerow(new_details)
                    details = new_details
                else:
                    print 'Date changed. Preparing for new file...'
                    details = new_details
                    break

if __name__ == '__main__':
    main()
