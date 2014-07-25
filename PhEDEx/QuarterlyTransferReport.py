#!/usr/bin/env python

import os,sys, re
import datetime
from dateutil.relativedelta import relativedelta
from optparse import OptionParser
import urllib,json

def queryStatistics(startdate, enddate, destination, source, binwidth):
	url="https://cmsweb.cern.ch/phedex/datasvc/json/prod/transferhistory?starttime="+str(startdate)+"&endtime="+str(enddate)+"&binwidth="+str(binwidth)+"&from="+str(source)+"&to="+str(destination)
	if debug == True : print url

	result = json.load(urllib.urlopen(url))
	statistics = {}

	for link in result['phedex']['link']:
		for bin in link['transfer']:
			if bin['timebin'] not in statistics.keys(): statistics[bin['timebin']] = {}
			if 'width' not in statistics[bin['timebin']].keys(): statistics[bin['timebin']]['width'] = float(bin['binwidth'])
			if statistics[bin['timebin']]['width'] != float(bin['binwidth']):
				print 'ERROR: bin width changed'
				sys.exit(1)
			if 'bytes' not in statistics[bin['timebin']].keys(): statistics[bin['timebin']]['bytes'] = 0		
			statistics[bin['timebin']]['bytes'] += bin['done_bytes']

	total_volume = 0.
	total_binwidth = 0.
	peak_volume = 0.
	peak_rate = 0.
	for bin in statistics.keys():
		if debug == True : print "bin: %i, volume %8.2f TB" % (bin,float(statistics[bin]['bytes'])/1000000000000.)
		total_volume += statistics[bin]['bytes']
		total_binwidth += statistics[bin]['width']
		if statistics[bin]['bytes'] > peak_volume: peak_volume = statistics[bin]['bytes']
		rate = float(statistics[bin]['bytes'])/float(statistics[bin]['width'])
		if rate > peak_rate: peak_rate = rate

	average_rate = float(total_volume)/float(total_binwidth)
	average_volume = float(total_volume)/float(len(statistics.keys()))

	return [float(total_volume),float(average_rate),float(average_volume),float(peak_rate),float(peak_volume)]
	
def formatOutput(result,mode=""):
	if mode == "table":
		return "%f\t%f\t%f\t%f\t%f" % (result[0]/1000000000000., result[1]/1000000000., result[2]/1000000000000., result[3]/1000000000., result[4]/1000000000000.)
	elif mode == "screen":
		return "total volume: %8.2f TB, average weekly rate: %8.2f GB/s, average weekly volume %8.2f TB, peak weekly rate %8.2f GB/s, peak weekly volume %8.2f TB" % (result[0]/1000000000000., result[1]/1000000000., result[2]/1000000000000., result[3]/1000000000., result[4]/1000000000000.)
	return "No mode selected"
		

usage  = "Usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
parser.add_option("-m", "--month", action="store", type="int", default=-1, dest="months", help="Gather statistics for the last N months")
parser.add_option("-s", "--startdate", action="store", type="string", default=None, dest="startdate", help="Start date, format \"YYYY-MM-DD\"")
parser.add_option("-e", "--enddate", action="store", type="string", default=None, dest="enddate", help="End date, format \"YYYY-MM-DD\"")
parser.add_option("-t", "--destination", action="store", type="string", default="", dest="destination", help="Calculate Transfer Statisics for 60s from given site name")
parser.add_option("-f", "--source", action="store", type="string", default="", dest="source", help="Calculate Transfer Statisics for imports to given site name")
parser.add_option("-r", "--report", action="store_true", default=False, dest="report", help="Report preset")
parser.add_option("-b", "--binwidth", action="store", type="int", default=604800, dest="binwidth", help="Bin width for statistics query in second (default 1 week = 604800s)")
(opts, args) = parser.parse_args()

if (opts.report == False and ( opts.source == "" and opts.destination == "" ) ):
    parser.error("Either choose predefined report or define site name for either import or export statistics.")
if (opts.months < 0 and ( opts.startdate == None and opts.enddate == None ) ):
    parser.error("Either define number of months to gather statistics for or define start and end date.")

debug = opts.verbose
months = opts.months
startdate = opts.startdate
enddate = opts.enddate
destination = opts.destination
source = opts.source
report = opts.report
binwidth = opts.binwidth

if (months > 0):
	enddate = datetime.datetime.now().strftime("%Y-%m-%d")
	startdate = (endtime + relativedelta(months = -1*months)).strftime("%Y-%m-%d")
	

if ( report == True ):
	total = queryStatistics(startdate, enddate, "", "", binwidth)
	ust1_destination = queryStatistics(startdate, enddate, "T1_US_FNAL_*", "", binwidth)
	ust1_source = queryStatistics(startdate, enddate, "", "T1_US_FNAL_*", binwidth)
	ust2_destination = queryStatistics(startdate, enddate, "T2_US_*", "", binwidth)
	ust2_source = queryStatistics(startdate, enddate, "", "T2_US_*", binwidth)
	print "Statistics report (\"All CMS cites\", \"USCMS T1 Import\", \"USCMS T1 Export\", \"USCMS T2s Import\", \"USCMS T2s Export\")"
	print ""
	print formatOutput(total,"screen")
	print formatOutput(ust1_destination,"screen")
	print formatOutput(ust1_source,"screen")
	print formatOutput(ust2_destination,"screen")
	print formatOutput(ust2_source,"screen")
	print ""
	print "Table output"
	print ""
	print formatOutput(total,"table")
	print formatOutput(ust1_destination,"table")
	print formatOutput(ust1_source,"table")
	print formatOutput(ust2_destination,"table")
	print formatOutput(ust2_source,"table")

else:
	result = queryStatistics(startdate, enddate, destination, source, binwidth)
	print "Statistics for:"
	if destination != "": print "destination:",destination
	if source != "": print "source:",source
	print ""
	print formatOutput(result,"screen")
	print ""
	print "Table output"
	print ""
	print formatOutput(result,"table")
	
