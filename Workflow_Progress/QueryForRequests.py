#!/usr/bin/env python
"""

 DBS 3 script to calculate accumulated events per day for a interval.

 python QueryForRequests.py -d '/*/*Fall13-POST*/GEN-SIM'

"""

import  sys,datetime,json,re,urllib2,httplib,time
from optparse import OptionParser
from dbs.apis.dbsClient import DbsApi
from dbs.exceptions.dbsClientException import dbsClientException

def main():
    usage="%prog <options>"

    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--url", dest="url", help="DBS Instance url. default is https://cmsweb.cern.ch/dbs/prod/global/DBSReader", metavar="<url>")
    parser.add_option("-d", "--dataset", dest="dataset", help="The dataset name for cacluate the events. Allows to use wildcards, don't forget to escape on the commandline.", metavar="<dataset>")
   
    parser.set_defaults(url='cmssrv101.fnal.gov:7714')
    parser.set_defaults(length=30)
   
    (opts, args) = parser.parse_args()
    if not (opts.dataset or opts.datatier):
        parser.print_help()
        parser.error('either --dataset or --datatier is required')	

    data = opts.dataset
    data_regexp = data.replace('*','[\w\-]*',99)
    url = opts.url

    result = {}

    # load requests from json
    header = {'Content-type': 'application/json', 'Accept': 'application/json'}
    conn = httplib.HTTPConnection(url)
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
                          }
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
            request_day = int(datetime.datetime(request_date.year, request_date.month, request_date.day).strftime("%s"))
            if str(request_day) not in result.keys(): result[str(request_day)] = {'requests' : [], 'requested_events' : 0}
            result[str(request_day)]['requests'].append(workflowname)
            result[str(request_day)]['requested_events'] += workflow_dict['Requested events']
                
    for day in sorted(result.keys()):
        print "%s: number of requests: %4i, requested events: %10i" % (datetime.datetime.fromtimestamp(int(day)).strftime("%d %b %Y"),len(result[day]['requests']),result[day]['requested_events'])
        # print "%s: number of requests: %4i, requested events: %10i, requests: %s" % (datetime.datetime.fromtimestamp(int(day)).strftime("%d %b %Y"),len(result[day]['requests']),result[day]['requested_events'],','.join(result[day]['requests']))


    sys.exit(0);
    

if __name__ == "__main__":
    main()
    sys.exit(0);
