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


def queryDBSForEventsPerDay(dbsapi,dataset,start,end,status,result,verbose,csa):
    # query for all datasets with status using the dataset that can include wildcards
    # use last modification date of block to count events
    # restrict to datasets that have been created 30 days before the start of the query
    if verbose == True:
        temp_results = {}
    datasets = []
    if csa == False:
        datasets = dbsapi.listDatasets(dataset=dataset, min_cdate=start-30*sdays, max_cdate=end+30*sdays,dataset_access_type=status)    
    elif csa == True:
        tmp = dbsapi.listDatasets(dataset=dataset, detail=True, min_cdate=start-30*sdays, max_cdate=end+30*sdays,dataset_access_type=status)
        operators = ['mmascher', 'spiga', 'riahi', 'mmdali', 'jbalcas', 'sciaba', 'atanasi', 'dciangot', 'vmancine']
        for ds in tmp:
            if not ds['creation_date']:
                continue #some weird datasets we would like to skip
            #filter out datasets we are not interested in
            if ds['physics_group_name']=='CRAB3' and ds['create_by'] not in operators and ds['dataset_access_type'] == 'VALID':
                #take only things that looks like miniAOD productions
                parents = dbsapi.listDatasetParents(dataset=ds['dataset'])
                if parents and parents[0]['parent_dataset'].find('Spring14')!=-1:
                    datasets.append(ds)
    if len(datasets) > 0:
        for dataset in datasets:
            blocks = dbsapi.listBlocks(dataset=dataset['dataset'], detail=True, min_cdate=start-sdays, max_cdate=end+sdays)
            blockList = {}
            for block in blocks:
                blockList[block["block_name"]] = block["last_modification_date"]
            blockSummaries = []
            if blockList: 
                blockSummaries = dbsapi.listBlockSummaries(block_name=blockList.keys(), detail=True)
            for block in blockSummaries:
                day = blockList[block['block_name']]
                # normalize day to 00:00:00 UTC as identifier
                day -= day%sdays
                if day >= start and day <= end:
                    result[str(day)][status] += block['num_evernt']
                    if verbose == True:
                        if str(day) not in temp_results.keys(): temp_results[str(day)] = {}
                        if dataset['dataset'] not in temp_results[str(day)].keys(): temp_results[str(day)][dataset['dataset']] = 0
                        temp_results[str(day)][dataset['dataset']] += block['num_evernt']
                        
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
    parser.add_option("-m", "--csa_miniaod", action="store_true", dest="csa", default=False, help="CSA14 mode to query for MINIAOD samples using CSA14 AODSIM as parent")
   
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
    csa = opts.csa
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
        
    print 'Querying for events created per day for datasets:',data,'for the time range from',utcTimeStringFromUtcTimestamp(start),'to',utcTimeStringFromUtcTimestamp(end),'starting at',datetime.datetime.utcnow()

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
    queryDBSForEventsPerDay(dbsapi,data,start,end,'VALID',result,verbose,csa)
    queryDBSForEventsPerDay(dbsapi,data,start,end,'PRODUCTION',result,verbose,csa)
    queryDBSForEventsPerDay(dbsapi,data,start,end,'INVALID',result,verbose,csa)
    queryDBSForEventsPerDay(dbsapi,data,start,end,'DEPRECATED',result,verbose,csa)
                    
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
