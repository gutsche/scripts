#!/usr/bin/env python
"""

 DBS 3 script to calculate accumulated events per day for a interval.

 python QueryForRequests.py -d '/*/*Fall13-POST*/GEN-SIM'

"""

import  sys,datetime,json,re,urllib2,httplib,time
import pytz
from optparse import OptionParser
from dbs.apis.dbsClient import DbsApi
from dbs.exceptions.dbsClientException import dbsClientException

def QueryForRquestedEventsPerDay(dbsurl,couchurl,outputdict,data_regexp):
    #
    # query couch DB and extract list of requests per day

    # these status values are for rejected workflows
    rejected_status = ['rejected','rejected-archived']

    basenames_to_print = []

    # load requests from json
    header = {'Content-type': 'application/json', 'Accept': 'application/json'}
    conn = httplib.HTTPConnection(couchurl)
    conn.request("GET", '/latency_analytics/_design/latency/_view/maria', headers= header)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    myString = data.decode('utf-8')
    workflows = json.loads(myString)['rows']
    
    # first extract workflows per workflow basename to identify actual requests in case of clones or other 
    basenames = {}
    for entry in workflows:
        # extract information
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

        # filter for data_regexp
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

        if match == False: continue

        # extract workflow basename, split by '_', remove first field that is the username who injected the workflow, and the last 3 fields that are date, time and fractions of a second (?)
        workflowname_array = workflowname.split('_')
        basename_array = workflowname_array[1:-3]

        # continue if basename_array length == 0
        if len(basename_array) == 0: continue

        # filter out ACDC and tests
        if workflowname.lower().count('acdc') > 0: continue
        if workflowname.lower().count('test') > 0: continue

        # Jen's username is jen_a, from split above a_ could remain, remove
        if basename_array[0].lower() == 'a':
            basename_array = basename_array[1:]

        # if extension, remove EXT from beginning of basename
        if basename_array[0].lower() == 'ext':
            basename_array = basename_array[1:]

        basename = '_'.join(basename_array)
        requestdatetime = int(workflowname_array[-1]) + int(workflowname_array[-2]) * 1E4 + int(workflowname_array[-3]) * 1E10
        if basename not in basenames.keys(): basenames[basename] = {}
        basenames[basename][requestdatetime] = [workflowname,workflow_dict]
    
    # select the original workflow removing clones, etc
    selected = {}
    rejected = {}
    for basename in basenames.keys():
        if basename in basenames_to_print:
            print 'selected basename:',basename
            for date in sorted(basenames[basename].keys()):
                print basenames[basename][date]

        if basename in selected.keys() or basename in rejected.keys(): continue

        # look at all the workflow names of a basename ordered by injection time

        # if the first workflow name of a basename ordered by injection time is not a rejected status, select it
        if basenames[basename][sorted(basenames[basename].keys())[0]][1]['Status'] not in rejected_status:
            selected[basename] = basenames[basename][sorted(basenames[basename].keys())[0]]
        else :
            # if the last workflow is not in rejected status (indication that the workflow never started to run), choose the first workflow as reference
            if basenames[basename][sorted(basenames[basename].keys())[-1]][1]['Status'] not in rejected_status:
                selected[basename] = basenames[basename][sorted(basenames[basename].keys())[0]]
            else :
                # if there is only one workflow for the basename and if the status is rejected
                if len(basenames[basename]) ==  1 and basenames[basename][basenames[basename].keys()[0]][1]['Status'] in rejected_status:
                    rejected[basename] = basenames[basename][basenames[basename].keys()[0]]
                else :
                    # go through workflowname per basename ordered by status, select the first status that is not a rejected status
                    firstvalidentry = None
                    for entry in sorted(basenames[basename].keys()):
                        if basenames[basename][entry][1]['Status'] not in rejected_status:
                            firstvalidentry = entry
                            break
                    if firstvalidentry != None:
                        selected[basename] = basenames[basename][firstvalidentry]
                    else:
                        # check if there are only workflownames per basename that are in a rejected status
                        nonrejectedstatus = False
                        for entry in basenames[basename].keys():
                            if basenames[basename][entry][1]['Status'] not in rejected_status:
                                nonrejectedstatus = True
                                break
                        if nonrejectedstatus == False :
                            # select last one
                            rejected[basename] = basenames[basename][sorted(basenames[basename].keys())[-1]]
                            
        if basename in selected.keys() or basename in rejected.keys(): continue
        print 'could not decide which workflow is the original workflow for basename:',basename
        for date in sorted(basenames[basename].keys()):
            print basenames[basename][date]
        sys.exit(1)
    
    # loop over selected workflows and fill requested events per day
    # only fill day if defined as key of outputdict
    api=DbsApi(url=dbsurl)
    for basename in selected.keys():
        print 'selected basename:',basename
        for date in sorted(basenames[basename].keys()):
            print basenames[basename][date]
        workflowname = selected[basename][0]
        workflow_dict = selected[basename][1]

        # extract unix time of start of day of request date
        request_date = datetime.datetime.strptime(workflow_dict['Request date'],"%Y-%m-%d %H:%M:%S")
        request_date = request_date.replace(tzinfo=pytz.timezone('UTC'))
        request_day = int(datetime.datetime(request_date.year, request_date.month, request_date.day,0,0,0,0, tzinfo=pytz.timezone('UTC')).strftime("%s"))
        if str(request_day) not in outputdict.keys(): continue
        if 'REQUESTED' not in outputdict[str(request_day)].keys(): outputdict[str(request_day)]['REQUESTED'] = 0
        if 'WORKFLOWS' not in outputdict[str(request_day)].keys(): outputdict[str(request_day)]['WORKFLOWS'] = []
        outputdict[str(request_day)]['WORKFLOWS'].append(workflowname)
        request_events = int(workflow_dict['Requested events'])
        if request_events == 0 and workflow_dict['Input Dataset'] != '':
            blocks = api.listBlocks(dataset=workflow_dict['Input Dataset'], detail=False)
            for block in blocks:
                reply= api.listBlockSummaries(block_name=block['block_name'])
                request_events += reply[0]['num_event']
        if workflow_dict['Filter efficiency'] == None :
            outputdict[str(request_day)]['REQUESTED'] += int(request_events)
        else:
            outputdict[str(request_day)]['REQUESTED'] += int(request_events) * float(workflow_dict['Filter efficiency'])

def main():
    usage="%prog <options>"

    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--url", dest="url", help="DBS Instance url. default is https://cmsweb.cern.ch/dbs/prod/global/DBSReader", metavar="<url>")
    parser.add_option("-c", "--couchurl", dest="couchurl", help="Couch Instance url. default is cmssrv101.fnal.gov:7714", metavar="<couchurl>")
    parser.add_option("-d", "--dataset", dest="dataset", help="The dataset name for cacluate the events. Allows to use wildcards, don't forget to escape on the commandline.", metavar="<dataset>")
    parser.add_option("-s", "--startdate", dest="startdate", help="Startdate in the form of 2014-06-11, overrides -l", metavar="<startdate>")    
    parser.add_option("-l", "--length", dest="length", help="Number of days for calculate the accumated events. It is Optional, default is 30 days.", metavar="<length>")
   
    parser.set_defaults(url="https://cmsweb.cern.ch/dbs/prod/global/DBSReader")
    parser.set_defaults(couchurl="cmssrv101.fnal.gov:7714")
    parser.set_defaults(length=0)
   
    (opts, args) = parser.parse_args()
    if not (opts.dataset or opts.datatier):
        parser.print_help()
        parser.error('either --dataset or --datatier is required')	

    data = opts.dataset
    data_regexp = data.replace('*','[\w\-]*',99)
    dbsurl = opts.url
    couchurl = opts.couchurl

    # seconds per day	
    sdays = 86400

    # determine start time of current day
    current_date = datetime.datetime.utcnow().date()
    now = int(datetime.datetime(current_date.year, current_date.month, current_date.day,0,0,0,0, tzinfo=pytz.timezone('UTC')).strftime("%s"))

    # determine numdays
    numdays = int(opts.length)
    if opts.startdate != None:
        startdate=str(opts.startdate).split('-')
        start = int(datetime.datetime(int(startdate[0]), int(startdate[1]), int(startdate[2]),0,0,0,0, tzinfo=pytz.timezone('UTC')).strftime("%s"))
        numdays = (now - start)/sdays
    then = now - sdays*(numdays)

    result = {}
    for i in range(numdays+1):
        result[str(now-i*sdays)] = {'REQUESTED' : 0, 'WORKFLOWS': []}
        
    QueryForRquestedEventsPerDay(dbsurl,couchurl,result,data_regexp)

    for day in sorted(result.keys()):
        print "%s: requested events: %10i, workflows: %s" % (datetime.datetime.fromtimestamp(int(day)).strftime("%d %b %Y"),result[day]['REQUESTED'],','.join(result[day]['WORKFLOWS']))

    sys.exit(0);
    

if __name__ == "__main__":
    main()
    sys.exit(0);
