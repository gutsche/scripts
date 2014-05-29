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

# properties = api3.listBlockSummaries(block_name="/BuToKstarMuMu_EtaPtFilter_8TeV-pythia6-evtgen/Summer12-START53_V7C_ext1-v1/GEN-SIM#a40ebaec-af7a-11e3-bdae-0024e83ef644")
# print properties
# startdate = datetime.datetime.strptime("2013-05-01","%Y-%m-%d")
# enddate = datetime.datetime.strptime("2013-05-10","%Y-%m-%d")
# result = api3.listBlocks(data_tier_name="GEN-SIM",min_cdate=startdate.strftime("%s"),max_cdate=enddate.strftime("%s"),dataset_access_type="*")
# result = api3.listAcquisitionEras()
# result = api3.listDataTiers()
# result = api3.listDataTypes()
# result = api3.
#results = api3.listPrimaryDatasets()
summ=0
# result = api3.listDatasets(dataset="/*/Fall13-*/GEN-SIM", dataset_access_type='VALID')
# result = api3.listDatasets(dataset="/*/Spring14dr-*S14_POSTLS170*/AODSIM", dataset_access_type='VALID')
result = api3.listDatasets(dataset="/*/Spring14dr-*PU20bx25_POSTLS170*/AODSIM", dataset_access_type='VALID')
for dataset in result:
    result2 = api3.listFileSummaries(dataset=dataset['dataset'])
    for entry in result2:
        summ+=entry['num_event']
        
print summ
summ=0
# result = api3.listDatasets(dataset="/*/Fall13-*/GEN-SIM", dataset_access_type='PRODUCTION')
# result = api3.listDatasets(dataset="/*/Spring14dr-*S14_POSTLS170*/AODSIM", dataset_access_type='PRODUCTION')
result = api3.listDatasets(dataset="/*/Spring14dr-*PU20bx25_POSTLS170*/AODSIM", dataset_access_type='PRODUCTION')
for dataset in result:
    result2 = api3.listFileSummaries(dataset=dataset['dataset'])
    for entry in result2:
        summ+=entry['num_event']
        
print summ


        

#types = {}

#for result in results:
#	if result['primary_ds_type'] not in types.keys(): types[result['primary_ds_type']] = []
#	types[result['primary_ds_type']].append(result['primary_ds_name'])
	
#for type in types.keys():
#	outputfile = open(type+'.out','w')
#	for name in types[type]:
#		outputfile.write(name+'\n')
#	outputfile.close()
