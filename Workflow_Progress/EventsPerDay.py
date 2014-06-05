#!/usr/bin/env python
"""

 DBS 3 script to calculate accumulated events per day for a interval.

 python EventsPerDay.py -d '/*/*Fall13-POST*/GEN-SIM'

"""

import  sys,datetime,json,re,urllib2,httplib,time
import pytz
from optparse import OptionParser
from dbs.apis.dbsClient import DbsApi
from dbs.exceptions.dbsClientException import dbsClientException

def main():
    usage="%prog <options>"

    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--url", dest="url", help="DBS Instance url. default is https://cmsweb.cern.ch/dbs/prod/global/DBSReader", metavar="<url>")
    parser.add_option("-c", "--couchurl", dest="couchurl", help="Couch Instance url. default is cmssrv101.fnal.gov:7714", metavar="<couchurl>")
    parser.add_option("-l", "--length", dest="length", help="Number of days for calculate the accumated events. It is Optional, default is 30 days.", metavar="<length>")
    parser.add_option("-d", "--dataset", dest="dataset", help="The dataset name for cacluate the events. Allows to use wildcards, don't forget to escape on the commandline.", metavar="<dataset>")
   
    parser.set_defaults(url="https://cmsweb.cern.ch/dbs/prod/global/DBSReader")
    parser.set_defaults(couchurl="cmssrv101.fnal.gov:7714")
    parser.set_defaults(length=30)
   
    (opts, args) = parser.parse_args()
    if not (opts.dataset or opts.datatier):
        parser.print_help()
        parser.error('either --dataset or --datatier is required')	
        
    url = opts.url
    couchurl = opts.couchurl
    data = opts.dataset
    data_regexp = data.replace('*','[\w\-]*',99)
    numdays = int(opts.length)
    # seconds per day	
    sdays = 86400
    # determine start time of current day
    current_date = datetime.datetime.utcnow().date()
    # subtract one day from today
    now = int(datetime.datetime(current_date.year, current_date.month, current_date.day,0,0,0,0, tzinfo=pytz.timezone('UTC')).strftime("%s"))
    then = now - sdays*(numdays)
    
    # generate basename for input and output files
    # use selected dataset, replace wildcards to make it readable
    file_base_name = data
    if file_base_name.startswith('/') == True: file_base_name = file_base_name[1:]
    file_base_name = file_base_name.replace('/','_',99)
    file_base_name = file_base_name.replace('*',"STAR",99)

    # don't count requests with the following status
    rejected_status = ['rejected-archived', 'aborted-archived', 'aborted', 'failed']

    print "Started executing script with selected dataset string:",data,'at',datetime.datetime.utcnow()

    # load output dictionary from json file, if not existing, create dictionary, key is the starting time of the day
    try:
        dictfile = open(file_base_name + ".json")
        result = json.load(dictfile)
        print "Loaded query result dictionary from " + file_base_name + ".json"
        # reset days that will be queries in this script
        for i in range(numdays):
            result[str(now-i*sdays)] = { 'VALID':0, 'PRODUCTION':0, 'REQUESTED':0, 'VALID_CUMULATIVE':0, 'PRODUCTION_CUMULATIVE':0, 'REQUESTED_CUMULATIVE':0}
        dictfile.close()
    except:
        # create dictionary, 
        result = {}
        for i in range(numdays):
            result[str(now-i*sdays)] = { 'VALID':0, 'PRODUCTION':0, 'REQUESTED':0, 'VALID_CUMULATIVE':0, 'PRODUCTION_CUMULATIVE':0, 'REQUESTED_CUMULATIVE':0}
        print "Created new query result dictionary"

    api=DbsApi(url=url)
    outputDataSetsValid = api.listDatasets(dataset=data,detail=1, dataset_access_type="VALID")
    outputDataSetsProd = api.listDatasets(dataset=data,detail=1, dataset_access_type="PRODUCTION")

    for dataset in outputDataSetsValid:
        inp=dataset['dataset']
        ct = dataset['creation_date']
        if ct > (then-30*sdays):
            blocks = api.listBlocks(dataset=inp, detail=True)
            for block in blocks:
                reply= api.listBlockSummaries(block_name=block['block_name'])
                neventsb= reply[0]['num_event']
                reply=api.listFiles(block_name=block['block_name'],detail=True)
                ct=reply[0]['last_modification_date']
                # strip off hours and seconds from day, renormalized to 00:00
                starttime_day_ct = int(datetime.datetime(datetime.datetime.fromtimestamp(ct, tz=pytz.timezone('UTC')).year, datetime.datetime.fromtimestamp(ct, tz=pytz.timezone('UTC')).month, datetime.datetime.fromtimestamp(ct, tz=pytz.timezone('UTC')).day,0,0,0,0, tzinfo=pytz.timezone('UTC')).strftime("%s"))
                if starttime_day_ct > then:
                    result[str(starttime_day_ct)]['VALID'] += neventsb
                        
    for dataset in outputDataSetsProd:
        inp=dataset['dataset']
        ct = dataset['creation_date']
        if ct > (then-30*sdays):
            blocks = api.listBlocks(dataset=inp, detail=True)
            for block in blocks:
                reply= api.listBlockSummaries(block_name=block['block_name'])
                neventsb= reply[0]['num_event']
                reply=api.listFiles(block_name=block['block_name'],detail=True)
                ct=reply[0]['last_modification_date']
                # strip off hours and seconds from day, renormalized to 00:00
                starttime_day_ct = int(datetime.datetime(datetime.datetime.fromtimestamp(ct, tz=pytz.timezone('UTC')).year, datetime.datetime.fromtimestamp(ct, tz=pytz.timezone('UTC')).month, datetime.datetime.fromtimestamp(ct, tz=pytz.timezone('UTC')).day,0,0,0,0, tzinfo=pytz.timezone('UTC')).strftime("%s"))
                if starttime_day_ct > then:
                    result[str(starttime_day_ct)]['PRODUCTION'] += neventsb
                        
    # load requests from json
    # load requests from couch db
    header = {'Content-type': 'application/json', 'Accept': 'application/json'}
    conn = httplib.HTTPConnection(couchurl)
    conn.request("GET", '/latency_analytics/_design/latency/_view/maria', headers= header)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    myString = data.decode('utf-8')
    workflows = json.loads(myString)['rows']
    
    for entry in workflows:
        workflowname = entry['id']
        info = entry['value']
        workflow_dict = {
                          'Campaign' : info[0],
                          'Tier' : info[1],
                          'Task type' : info[2],
                          'Status' : info[3],
                          'Priority' : info[4],
                          'Requested events' : info[5],
                          '% Complete' : info[6],
                          'Completed events' : 0,
                          'Request date' : time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(info[7])),
                          'Processing dataset name' : '',
                          'Input Dataset' : info[8],
                          'Output Datasets' : info[9],
                          'Filter efficiency' : info[10],
                          'Run white list' : info[11],
                          }
        if workflow_dict['Status'] in rejected_status: continue
        # match at least one output dataset with match string
        if re.compile('[\w\-]*ACDC[\w\-]*').match(workflowname) is not None: continue
        match = False
        try:
            for output_dataset in workflow_dict['Output Datasets']:
                if re.compile(data_regexp).match(output_dataset) is not None:
                    match = True
                    break
        except:
            for output_dataset in workflow_dict['Output Datasets']:
                if re.compile(data_regexp).match(output_dataset[0]) is not None:
                    match = True
                    break

        if match == True:
            # extract unix time of start of day of request date
            request_date = datetime.datetime.strptime(workflow_dict['Request date'],"%Y-%m-%d %H:%M:%S")
            request_date = request_date.replace(tzinfo=pytz.timezone('UTC'))
            request_day = int(datetime.datetime(request_date.year, request_date.month, request_date.day,0,0,0,0, tzinfo=pytz.timezone('UTC')).strftime("%s"))
            request_events = int(workflow_dict['Requested events'])
            if request_events == 0 and workflow_dict['Input Dataset'] != '':
                blocks = api.listBlocks(dataset=workflow_dict['Input Dataset'], detail=False)
                for block in blocks:
                    reply= api.listBlockSummaries(block_name=block['block_name'])
                    request_events += reply[0]['num_event']
            if request_day > then:
                if workflow_dict['Filter efficiency'] == None :
                        result[str(request_day)]['REQUESTED'] += int(request_events)
                else:
                    result[str(request_day)]['REQUESTED'] += int(request_events) * float(workflow_dict['Filter efficiency'])
                
    # calculate cumulative values
    first = True
    for day in sorted(result.keys()):
        if first == True:
            result[day]['VALID_CUMULATIVE'] = result[day]['VALID']
            result[day]['PRODUCTION_CUMULATIVE'] = result[day]['PRODUCTION']
            result[day]['REQUESTED_CUMULATIVE'] = result[day]['REQUESTED']
            first = False
        else :
            result[day]['VALID_CUMULATIVE'] = result[str(int(day)-86400)]['VALID_CUMULATIVE'] + result[day]['VALID']
            result[day]['PRODUCTION_CUMULATIVE'] = result[str(int(day)-86400)]['PRODUCTION_CUMULATIVE'] + result[day]['PRODUCTION']
            result[day]['REQUESTED_CUMULATIVE'] = result[str(int(day)-86400)]['REQUESTED_CUMULATIVE'] + result[day]['REQUESTED']

    # write output to files
    csv_output = open(file_base_name + '.csv','w')
    json_output = open(file_base_name + '.json','w')


    for day in sorted(result.keys()):
        csv_line = "%s,%i,%i,%i,%i,%i,%i,%i,%i" % (datetime.datetime.fromtimestamp(int(day), tz=pytz.timezone('UTC')).strftime("%d %b %Y"),result[day]['VALID'],result[day]['PRODUCTION'],result[day]['PRODUCTION']+result[day]['VALID'],result[day]['REQUESTED'],result[day]['VALID_CUMULATIVE'],result[day]['PRODUCTION_CUMULATIVE'],result[day]['PRODUCTION_CUMULATIVE']+result[day]['VALID_CUMULATIVE'],result[day]['REQUESTED_CUMULATIVE'])
        csv_output.write(csv_line + '\n')
    csv_output.close()
    
    json.dump(result,json_output)
    json_output.close

    print "Finished executing script writing json and csv with base name",file_base_name,'at',datetime.datetime.utcnow()

    sys.exit(0);
    

if __name__ == "__main__":
    main()
    sys.exit(0);
