#!/usr/bin/env python

import os,sys, re
import datetime
from dateutil.relativedelta import relativedelta
from optparse import OptionParser
import urllib,json
from dbs.apis.dbsClient import DbsApi

def formatSize(size):
    output = ''
    if size < 1E3:
        output += "%i B" % size
    elif size < 1E6:
        output += "%.3f kB" % (float(size)/1E3)
    elif size < 1E9:
        output += "%.3f MB" % (float(size)/1E6)
    elif size < 1E12:
        output += "%.3f GB" % (float(size)/1E9)
    elif size < 1E15:
        output += "%.3f TB" % (float(size)/1E12)
    elif size < 1E18:
        output += "%.3f PB" % (float(size)/1E15)

    return output
    
def PositiveIntegerWithCommas(number):
    if number > 0:
        return ''.join(reversed([x + (',' if i and not i % 3 else '') for i, x in enumerate(reversed(str(number)))]))

    return str(number)

def QueryDBSForEvents(dbs3api,pattern,status):
    events = 0
    size = 0
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
                size += b['file_size']
        return (events,size)
    else:
        return (None,None)


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
    total_events = 0
    total_size = 0

    status = "PRODUCTION"
    (production_events,production_size) = QueryDBSForEvents(dbs3api,pattern,status)
    if production_events == None:
        if verbose == True:
            print 'No datasets in status PRODUCTION found for pattern:',pattern
        production_events = 0
    else:
        total_events += production_events
    if production_size == None:
        if verbose == True:
            print 'No datasets in status PRODUCTION found for pattern:',pattern
        production_size = 0
    else:
        total_size += production_size

    if invalid == True:
        status = "INVALID"
        (invalid_events,invalid_size) = QueryDBSForEvents(dbs3api,pattern,status)
        if invalid_events == None:
            if verbose == True:
                print 'No datasets in status INVALID found for pattern:',pattern
            invalid_events = 0
        else:
            total_events += invalid_events
        if invalid_size == None:
            if verbose == True:
                print 'No datasets in status INVALID found for pattern:',pattern
            invalid_size = 0
        else:
            total_size += invalid_size

    status = "VALID"
    (valid_events,valid_size) = QueryDBSForEvents(dbs3api,pattern,status)
    if valid_events == None:
        if verbose == True:
            print 'No datasets in status VALID found for pattern:',pattern
        valid_events = 0
    else:
        total_events += valid_events
    if valid_size == None:
        if verbose == True:
            print 'No datasets in status VALID found for pattern:',pattern
        valid_size = 0
    else:
        total_size += valid_size

    print "status: %10s events: %13s size: %13s" % ('PRODUCTION',PositiveIntegerWithCommas(production_events),formatSize(production_size))
    print "status: %10s events: %13s size: %13s" % ('VALID',PositiveIntegerWithCommas(valid_events),formatSize(valid_size))
    if invalid == True:
        print "status: %10s events: %13s size: %13s" % ('INVALID',PositiveIntegerWithCommas(invalid_events),formatSize(invalid_size))
    print "total:  %10s events: %13s size: %13s" % ("",PositiveIntegerWithCommas(total_events),formatSize(total_size))
    
if __name__ == "__main__":
    main()
    sys.exit(0);
