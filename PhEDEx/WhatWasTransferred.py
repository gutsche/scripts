#!/usr/bin/env python

import sys,getopt,urllib2,json
import datetime, time, pytz
from optparse import OptionParser

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
        
# seconds per day	
sdays = 86400

def local_time_offset(t=None):
    """Return offset of local zone from GMT, either at present or at time t."""
    # python2.3 localtime() can't take None
    if t is None:
        t = time.time()

    if time.localtime(t).tm_isdst and time.daylight:
        return -time.altzone
    else:
        return -time.timezone

def utcTimestampFromDate(year,month,day):
    local = datetime.datetime(year,month,day)
    return int(local.strftime('%s')) + local_time_offset()

def utcTimeStringFromUtcTimestamp(timestamp):
    return datetime.datetime.fromtimestamp(int(timestamp), tz=pytz.timezone('UTC')).strftime("%d %b %Y")

def query(destination,start,end):

    output = {}

    url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/blocklatencylog?to_node=' + destination + '&subscribe_since=' + str(start) + '&subscribe_before=' + str(end)
    jstr = urllib2.urlopen(url).read()
    jstr = jstr.replace("\n", " ")
    result = json.loads(jstr)
    
    for block in result['phedex']['block']:
        dataset = block['dataset']
        if dataset not in output.keys(): output[dataset] = 0
        output[dataset] += block['bytes']
            
    url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/blocklatency?to_node=' + destination + '&subscribe_since=' + str(start) + '&subscribe_before=' + str(end)
    jstr = urllib2.urlopen(url).read()
    jstr = jstr.replace("\n", " ")
    result = json.loads(jstr)

    for block in result['phedex']['block']:
        dataset = block['dataset']
        if dataset not in output.keys(): output[dataset] = 0
        output[dataset] += block['bytes']

    return output
    
def main():

    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    parser.add_option("-d", "--destination", action="store", type="string", default=None, dest="destination", help="Destination PhEDEx node name")
    parser.add_option("-s", "--start", action="store", type="string", default=None, dest="start", help="Start date of query window, format 2014-12-31")
    parser.add_option("-e", "--end", action="store", type="string", default=None, dest="end", help="End date of query window, format 2014-12-31")
    (opts, args) = parser.parse_args()
    
    if ( opts.destination == None ) :
        print ""
        print "Please specify destination PhEDEx node name!"
        print ""
        parser.print_help()
        sys.exit(2)

    if ( opts.start == None ) :
        print ""
        print "Please specify start of query window!"
        print ""
        parser.print_help()
        sys.exit(2)

    if ( opts.end == None ) :
        print ""
        print "Please specify end of query window!"
        print ""
        parser.print_help()
        sys.exit(2)

    verbose = opts.verbose
    destination = opts.destination
    startdate_array = opts.start.split('-')
    enddate_array = opts.end.split('-')
    start = int(utcTimestampFromDate(int(startdate_array[0]),int(startdate_array[1]),int(startdate_array[2])))
    end = int(utcTimestampFromDate(int(enddate_array[0]),int(enddate_array[1]),int(enddate_array[2])))
    
    datasets = query(destination,start,end)
    
    print ''
    print 'Following datasets have been transferred to the destination',destination,'during the time window from',utcTimeStringFromUtcTimestamp(start),'to',utcTimeStringFromUtcTimestamp(end)
    print ''
    for dataset in sorted(datasets.keys(), key=datasets.get, reverse=True):
        print dataset,formatSize(datasets[dataset])
    print ''

if __name__ == '__main__':
    main()
