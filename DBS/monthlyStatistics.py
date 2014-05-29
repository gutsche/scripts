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
parser.add_option("-s", "--startdate", action="store", type="string", default=None, dest="startdate", help="Start date, format \"YYYY-MM-DD\"")
parser.add_option("-e", "--enddate", action="store", type="string", default=None, dest="enddate", help="End date, format \"YYYY-MM-DD\"")
parser.add_option("-u", "--url", action="store", type="string", default="https://cmsweb.cern.ch/dbs/prod/global/DBSReader", dest="url", help="DBS3 URL, default: https://cmsweb.cern.ch/dbs/prod/global/DBSReader")
parser.add_option("-p", "--persist", action="store", type="string", default=None, dest="persist", help="Specify filename to persist dbs query results")
parser.add_option("-r", "--read", action="store", type="string", default=None, dest="read", help="Specify filename to read in persisted dbs query results")
(opts, args) = parser.parse_args()

if (opts.startdate == None and opts.enddate == None and opts.read == None):
    parser.error("Either define number of months to gather statistics for or define start and end date.")

verbose = opts.verbose
persist = opts.persist
read = opts.read
if opts.startdate != None: startdate = datetime.datetime.strptime(opts.startdate,"%Y-%m-%d")
if opts.enddate != None: enddate = datetime.datetime.strptime(opts.enddate,"%Y-%m-%d")
url = opts.url
results = {}
dbs_query_results = {}
datatiers = {}
datatiers['data'] = ['RAW','RECO','AOD','RAW-RECO','USER']
datatiers['mc'] = ['GEN','GEN-SIM','GEN-RAW','GEN-SIM-RECO','AODSIM']
separations = ['PromptReco','PromptSkim']
exclusion_strings = {}
exclusion_strings['mc'] = ['test','backfill','jobrobot','sam','bunnies','penguins']
exclusion_strings['data'] = ['test','backfill','StoreResults','monitor','Error/','Scouting','MiniDaq','/Alca','L1Accept','L1EG','L1Jet','L1Mu','PhysicsDST','VdM','/Hcal','express','Interfill']

api3 = DbsApi(url)

if read == None:
	for category in datatiers.keys():
		if category not in dbs_query_results.keys(): dbs_query_results[category] = {}
		for datatier in datatiers[category]:
			if datatier not in dbs_query_results[category].keys(): dbs_query_results[category][datatier] = {}
			blocks = api3.listBlocks(data_tier_name=datatier,min_cdate=startdate.strftime("%s"),max_cdate=enddate.strftime("%s"))
			for block in blocks:
				exclude = False
				for exclusion_string in exclusion_strings[category]:
					if exclusion_string.lower() in block['block_name'].lower():
						if verbose == True: print 'blockname was rejected:',block['block_name']
						exclude = True
						continue
				if exclude == True: continue
				if verbose == True: print 'Querying for the summary for block:',block['block_name'],'!'
				properties = api3.listBlockSummaries(block_name=block['block_name'])
				dbs_query_results[category][datatier][block['block_name']] = properties
	
	if persist != None:
		outputfile = open(persist,'w')
		json.dump(dbs_query_results,outputfile)
		outputfile.close()
else:
	dbs_query_results = json.load(open(read))

for category in datatiers.keys():
	if category not in results.keys(): results[category] = {}
	for datatier in datatiers[category]:
		if datatier not in results[category].keys(): results[category][datatier] = {}
		for blockname in dbs_query_results[category][datatier]:
			triggered_separation = False
			for separation in separations:
				if separation.lower() in blockname.lower():
					if separation not in results[category][datatier].keys(): results[category][datatier][separation] = {'events': 0, 'size': 0.0}
					for property in dbs_query_results[category][datatier][blockname]:
						try:
							results[category][datatier][separation]['size'] += float(property['file_size'])/1000000000000.
							results[category][datatier][separation]['events'] += property['num_event']
						except:
							print "Problem with query result for block:",blockname,"result:",property
					triggered_separation = True
					continue
			if triggered_separation == False:
				if 'All' not in results[category][datatier].keys(): results[category][datatier]['All'] = {'events': 0, 'size': 0.0}
				for property in dbs_query_results[category][datatier][blockname]:
					try:
						results[category][datatier]['All']['size'] += float(property['file_size'])/1000000000000.
						results[category][datatier]['All']['events'] += property['num_event']
					except:
						print "Problem with query result for block:",blockname,"result:",property

# printout

for category in datatiers.keys():
	print ''
	print 'Category:',category
	print ''
	header = ''
	line = ''
	for datatier in datatiers[category]:
		temp_separations = ['All']
		if category == 'data':
			if datatier != 'RAW' :
				temp_separations = list(separations)
				temp_separations.append('All')
			if datatier == 'RAW-RECO' :
				temp_separations = ['PromptSkim','All']
			if datatier == 'USER' :
				temp_separations = ['PromptSkim','All']
		for temp_separation in temp_separations:
			try:
				size = results[category][datatier][temp_separation]['size']
			except:
				size = 0.
			try:
				events = results[category][datatier][temp_separation]['events']
			except:
				events = 0.
			header += '%s/%s(size)\t%s/%s(events)\t' % (datatier,temp_separation,datatier,temp_separation)
			line += '%f\t%i\t' % (size,events)
	print header
	print line
