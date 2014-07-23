#!/usr/bin/env python

import os,sys, re
import datetime
from dateutil.relativedelta import relativedelta
from optparse import OptionParser
import urllib,json
from dbs.apis.dbsClient import DbsApi

def PositiveIntegerWithCommas(number):
    if number > 0:
        return ''.join(reversed([x + (',' if i and not i % 3 else '') for i, x in enumerate(reversed(str(number)))]))

    return str(number)

def QueryDBSForEvents(dbs3api,pattern,status):
    events = 0
    datasets = dbs3api.listDatasets(dataset=pattern, dataset_access_type=status)
    for dataset in datasets:
        blocks = dbs3api.listBlocks(dataset=dataset['dataset'], detail=False)
        for block in blocks:
            blockSummaries = dbs3api.listBlockSummaries(block_name=block['block_name'])
            events += blockSummaries[0]['num_event']
            
    return events


def main():
    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    parser.add_option("-u", "--url", action="store", type="string", default="https://cmsweb.cern.ch/dbs/prod/global/DBSReader", dest="url", help="DBS3 URL, default: https://cmsweb.cern.ch/dbs/prod/global/DBSReader")
    (opts, args) = parser.parse_args()

    verbose = opts.verbose
    url = opts.url
    dbs3api = DbsApi(url)

    pattern = "/*/Fall13-*/GEN-SIM"
    # pattern = "/*/Spring14dr*/AODSIM"
    print "Query for pattern:",pattern
    total = 0
    status = "PRODUCTION"
    events = QueryDBSForEvents(dbs3api,pattern,status)
    total += events
    print "status: %10s events: %13s" % (status,PositiveIntegerWithCommas(events))
    status = "INVALID"
    events = QueryDBSForEvents(dbs3api,pattern,status)
    total += events
    print "status: %10s events: %13s" % (status,PositiveIntegerWithCommas(events))
    status = "VALID"
    events = QueryDBSForEvents(dbs3api,pattern,status)
    total += events
    print "status: %10s events: %13s" % (status,PositiveIntegerWithCommas(events))
    print "total:  %10s events: %13s" % ("",PositiveIntegerWithCommas(total))
    
if __name__ == "__main__":
    main()
    sys.exit(0);
