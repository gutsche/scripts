#!/usr/bin/env python

import os,sys, re
import datetime
from dateutil.relativedelta import relativedelta
from optparse import OptionParser
import urllib2,json

usage  = "Usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
parser.add_option("-m", "--month", action="store", type="int", default=6, dest="months", help="Gather popularity statistics for the last N months, default is 6")
parser.add_option("-n", "--datasetname", action="store", type="string", default=None, dest="datasetname", help="Gather popularity statistics for specific dataset")
parser.add_option("-f", "--file", action="store", type="string", default=None, dest="file", help="Gather popularity statistics for all dataset in file (one dataset per line)")
parser.add_option("-d", "--deletionRequest", action="store", type="int", default=None, dest="dr", help="Gather popularity statistics for all dataset of deletion request DR")
(opts, args) = parser.parse_args()

if (opts.file == None and opts.datasetname == None and opts.dr == None):
    parser.error("One of the following options need to be used: -n DATASETNAME or -f FILE or -d DR")

debug = opts.verbose
months = opts.months
datasetname = opts.datasetname
filename = opts.file
dr = opts.dr

endtime = datetime.datetime.now()
starttime = endtime + relativedelta(months = -1*months)

# get popularity information
url="https://cms-popularity.cern.ch/popdb/popularity/DSStatInTimeWindow/?tstart=" + starttime.strftime("%Y-%m-%d") + "&tstop=" + endtime.strftime("%Y-%m-%d")
popularity = json.load(open('output_1'))

if datasetname != None :
    for dataset in popularity['DATA']:
        if dataset['COLLNAME'] == datasetname :
            print 'Dataset %s was accessed %i times in the last %i months.' % (datasetname,dataset['NACC'],months)
            
if filename != None :
    for line in open(filename).readlines():
        name = line.strip()
        for dataset in popularity['DATA']:
            if dataset['COLLNAME'] == name :
                print 'Dataset %s was accessed %i times in the last %i months.' % (name,dataset['NACC'],months)
                
if dr != None :
    datasets = []
    url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/deleterequests?request=' + str(dr)
    jstr = urllib2.urlopen(url).read()
    jstr = jstr.replace("\n", " ")
    result = json.loads(jstr)

    for item in result['phedex']['request']:
        for dataset in item['data']['dbs']['dataset']:
            if dataset['name'] not in datasets: datasets.append(dataset['name'])
        for block in item['data']['dbs']['block']:            
            dataset = block['name'].split('#')[0]
            if dataset['name'] not in datasets: datasets.append(dataset['name'])
    for name in datasets:
        for dataset in popularity['DATA']:
            if dataset['COLLNAME'] == name :
                print 'Dataset %s was accessed %i times in the last %i months.' % (name,dataset['NACC'],months)