#!/usr/bin/env python
"""

 DBS 3 script to calculate accumulated events per day for a interval.

 python EventsPerDay.py -d '/*/*Fall13-POST*/GEN-SIM'

"""

import sys,json,re,urllib2,httplib
import pytz,datetime,time
from optparse import OptionParser
from dbs.apis.dbsClient import DbsApi
from dbs.exceptions.dbsClientException import dbsClientException

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
    
def PositiveIntegerWithCommas(number):
    if number > 0:
        return ''.join(reversed([x + (',' if i and not i % 3 else '') for i, x in enumerate(reversed(str(number)))]))

    return str(number)


def queryDBSForEventsPerDay(dbsapi,dataset,start,end,status,result,verbose):
    # query for all datasets with status using the dataset that can include wildcards
    # use last modification date of block to count events
    # restrict to datasets that have been created 30 days before the start of the query
    if verbose == True:
        temp_results = {}
    datasets = dbsapi.listDatasets(dataset=dataset,detail=1, dataset_access_type=status)    
    for dataset in datasets:
        inp=dataset['dataset']
        ct = dataset['creation_date']
        if ct > (start-30*sdays):
            blocks = dbsapi.listBlocks(dataset=inp, detail=True)
            for block in blocks:
                reply= dbsapi.listBlockSummaries(block_name=block['block_name'])
                neventsb= reply[0]['num_event']
                reply=dbsapi.listFiles(block_name=block['block_name'],detail=True)
                ct=reply[0]['last_modification_date']
                # use the day of ct at 00:00:00 UTC as identifier
                ct -= ct%sdays
                if ct >= start and ct <= end:
                    result[str(ct)][status] += neventsb
                    if verbose == True:
                        if str(ct) not in temp_results.keys(): temp_results[str(ct)] = {}
                        if inp not in temp_results[str(ct)].keys(): temp_results[str(ct)][inp] = 0
                        temp_results[str(ct)][inp] += neventsb
                        
    if verbose == True:
        print ''
        print 'Status:',status
        print ''
        for day in temp_results.keys():
            for dataset in sorted(temp_results[day], key=temp_results[day].get, reverse=True):
                print utcTimeStringFromUtcTimestamp(day),dataset,PositiveIntegerWithCommas(temp_results[day][dataset])
                
    

def main():
    usage="%prog <options>"

    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--url", dest="url", help="DBS Instance url. default is https://cmsweb.cern.ch/dbs/prod/global/DBSReader", metavar="<url>")
    parser.add_option("-c", "--couchurl", dest="couchurl", help="Couch Instance url. default is cmssrv101.fnal.gov:7714", metavar="<couchurl>")
    parser.add_option("-l", "--length", dest="length", help="Number of days for calculate the accumated events. It is Optional, default is 30 days.", metavar="<length>")
    parser.add_option("-s", "--startdate", dest="startdate", help="Startdate in the form of 2014-06-11, overrides -l", metavar="<startdate>")
    parser.add_option("-d", "--dataset", dest="dataset", help="The dataset name for cacluate the events. Allows to use wildcards, don't forget to escape on the commandline.", metavar="<dataset>")
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose output")
   
    parser.set_defaults(url="https://cmsweb.cern.ch/dbs/prod/global/DBSReader")
    parser.set_defaults(couchurl="cmssrv101.fnal.gov:7714")
    parser.set_defaults(length=30)
    parser.set_defaults(startdate=None)
   
    (opts, args) = parser.parse_args()
    if not (opts.dataset):
        parser.print_help()
        parser.error('either --dataset or --datatier is required')	
        
    url = opts.url
    dbsapi=DbsApi(url=url)
    couchurl = opts.couchurl
    verbose = opts.verbose
    data = opts.dataset
    data_regexp = data.replace('*','[\w\-]*',99)

    # all days are identified by their unix timestamp of 00:00:00 UTC of that day
    # last day to query is yesterday
    current_date = datetime.datetime.utcnow().date()
    end = utcTimestampFromDate(current_date.year,current_date.month,current_date.day-1)
    # calculate start day
    numdays = int(opts.length)
    start = end - sdays*(numdays)
    if opts.startdate != None:
        startdate=str(opts.startdate).split('-')
        start = utcTimestampFromDate(int(startdate[0]), int(startdate[1]), int(startdate[2]))
        numdays = (end - start)/sdays
        
    print 'Querying for events created per day for datasets:',data,'for the time range from',utcTimeStringFromUtcTimestamp(start),'to',utcTimeStringFromUtcTimestamp(end)

    # generate basename for input and output files
    # use selected dataset, replace wildcards to make it readable
    file_base_name = data
    if file_base_name.startswith('/') == True: file_base_name = file_base_name[1:]
    file_base_name = file_base_name.replace('/','_',99)
    file_base_name = file_base_name.replace('*',"STAR",99)
    
    # create dictionary, 
    result = {}
    for i in range(numdays+1):
        result[str(end-i*sdays)] = { 'VALID':0, 'PRODUCTION':0, 'REQUESTED':0, 'INVALID':0, 'DEPRECATED':0}

                
    # query
    queryDBSForEventsPerDay(dbsapi,data,start,end,'VALID',result,verbose)
    queryDBSForEventsPerDay(dbsapi,data,start,end,'PRODUCTION',result,verbose)
    queryDBSForEventsPerDay(dbsapi,data,start,end,'INVALID',result,verbose)
    queryDBSForEventsPerDay(dbsapi,data,start,end,'DEPRECATED',result,verbose)
                    
    # write output to files
    csv_output = open(file_base_name + '.csv','w')
    json_output = open(file_base_name + '.json','w')
    
    for day in sorted(result.keys()):
        csv_line = "%s,%i,%i,%i,%i,%i\n" % (utcTimeStringFromUtcTimestamp(int(day)),result[day]['VALID'],result[day]['PRODUCTION'],result[day]['REQUESTED'],result[day]['INVALID'],result[day]['DEPRECATED'])
        csv_output.write(csv_line)
    csv_output.close()
    
    json.dump(result,json_output)
    json_output.close
    
    print "Finished executing script writing json and csv with base name",file_base_name,'at',datetime.datetime.utcnow()

    sys.exit(0);
    

if __name__ == "__main__":
    main()
    sys.exit(0);
