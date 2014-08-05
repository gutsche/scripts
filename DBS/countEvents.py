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
    if len(datasets) > 0:
        for dataset in datasets:
            blocks = dbs3api.listBlocks(dataset=dataset['dataset'], detail=False)
            blockList = []
            for block in blocks:
                blockList.append(block["block_name"])
            blockSum = []
            if blockList: 
                blockSum = dbs3api.listBlockSummaries(block_name=blockList, detail=1)
            for b in blockSum:
                events += b['num_evernt']
        return events
    else:
        return None


def main():
    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-d", "--dataset", dest="dataset", help="The dataset name for cacluate the events. Allows to use wildcards, don't forget to escape on the commandline.", metavar="<dataset>")
    parser.add_option("-i", "--invalid", action="store_true", default=False, dest="invalid", help="Query for INVALID datasets")
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    parser.add_option("-u", "--url", action="store", type="string", default="https://cmsweb.cern.ch/dbs/prod/global/DBSReader", dest="url", help="DBS3 URL, default: https://cmsweb.cern.ch/dbs/prod/global/DBSReader")
    (opts, args) = parser.parse_args()

    verbose = opts.verbose
    invalid = opts.invalid
    url = opts.url
    dbs3api = DbsApi(url)

    pattern = opts.dataset

    if not opts.dataset:
        parser.print_help()
        parser.error('--dataset is required')

    print "Query for pattern:",pattern
    total = 0
    status = "PRODUCTION"
    production_events = QueryDBSForEvents(dbs3api,pattern,status)
    if production_events == None:
        if verbose == True:
            print 'No datasets in status PRODUCTION found for pattern:',pattern
    else:
        total += production_events

    if invalid == True:
        status = "INVALID"
        invalid_events = QueryDBSForEvents(dbs3api,pattern,status)
        if invalid_events == None:
            if verbose == True:
                print 'No datasets in status INVALID found for pattern:',pattern
        else:
            total += invalid_events

    status = "VALID"
    valid_events = QueryDBSForEvents(dbs3api,pattern,status)
    if valid_events == None:
        if verbose == True:
            print 'No datasets in status VALID found for pattern:',pattern
    else:
        total += valid_events

    print "status: %10s events: %13s" % ('PRODUCTION',PositiveIntegerWithCommas(production_events))
    print "status: %10s events: %13s" % ('VALID',PositiveIntegerWithCommas(valid_events))
    if invalid == True:
        print "status: %10s events: %13s" % ('INVALID',PositiveIntegerWithCommas(invalid_events))
    print "total:  %10s events: %13s" % ("",PositiveIntegerWithCommas(total))
    
if __name__ == "__main__":
    main()
    sys.exit(0);
