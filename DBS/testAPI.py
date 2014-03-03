#!/usr/bin/env python

import os,sys, re
import datetime
from dateutil.relativedelta import relativedelta
from optparse import OptionParser
import urllib,json
from dbs.apis.dbsClient import DbsApi

usage  = "Usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
parser.add_option("-u", "--url", action="store", type="string", default="https://cmsweb.cern.ch/dbs/prod/global/DBSReader", dest="url", help="DBS3 URL, default: https://cmsweb.cern.ch/dbs/prod/global/DBSReader")
(opts, args) = parser.parse_args()

verbose = opts.verbose
url = opts.url

api3 = DbsApi(url)

# result = api3.listBlocks(data_tier_name=datatier,min_cdate=startdate.strftime("%s"),max_cdate=enddate.strftime("%s"))
# result = api3.listAcquisitionEras()
# result = api3.listDataTiers()
# result = api3.listDataTypes()
# result = api3.
results = api3.listPrimaryDatasets()
# print result

types = {}

for result in results:
	if result['primary_ds_type'] not in types.keys(): types[result['primary_ds_type']] = []
	types[result['primary_ds_type']].append(result['primary_ds_name'])
	
for type in types.keys():
	outputfile = open(type+'.out','w')
	for name in types[type]:
		outputfile.write(name+'\n')
	outputfile.close()