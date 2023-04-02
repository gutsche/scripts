#!/usr/bin/env python3

import os,sys
from urllib.request import urlopen
import json
import sqlite3
from argparse import ArgumentParser
from datetime import datetime
import configparser

def time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def logprint(text):
    print("{0}: {1}".format(time(),text))

def main():
    # start of execution
    logprint("Starting execution of comed_hourly script")

    # initialization
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", help="increase output verbosity", default=0)
    parser.add_argument("-o", "--output", action="store", help="Full path of sqlite database output file (default: %(default)s)", default='/home/gutsche/comed.db')
    args = parser.parse_args()
    verbose = args.verbose

    url = "https://hourlypricing.comed.com/api?type=5minutefeed&format=json"
    sqlite_filename = args.output

    connection = sqlite3.connect(sqlite_filename)
    cursor = connection.cursor()

    # setup squlite3 db if the hourly table does not exist
    try:
        # create table
        cursor.execute("CREATE TABLE hourly (millisUTC INTEGER, price REAL)")
    except:
        if verbose >= 1: logprint("Table hourly already exists, continuing")
    try:
        # create unique index for millisUTC
        cursor.execute("CREATE UNIQUE INDEX idx_hourly_millisUTC ON hourly (millisUTC)")
    except:
        if verbose >= 1: logprint("Unique index for column millisUTC in table hourly already exists, continuing")

    data_json = json.load(urlopen(url))
    for entry in data_json:
        time = int(entry["millisUTC"])
        price=entry["price"]
        cursor.execute("REPLACE INTO hourly VALUES ({millisUTC},{price})".format(millisUTC=str(time),price=price))

    connection.commit()
    connection.close()

    # end of execution
    logprint("Ending execution of comed_hourly script")


if __name__ == "__main__":
    main()
    sys.exit(0);
