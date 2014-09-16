#!/usr/bin/env python

import os,sys,json,urllib2, httplib, time, re
from optparse import OptionParser

def printWorkflowsPerSite(sitenamepattern, excludesitepattern, sites, workflow_info, sortByWorkflow, quick):
    local = {}
    for site in sites.keys():
        if excludesitepattern != "" and site.count(excludesitepattern) > 0: continue
        if site.count(sitenamepattern) > 0:
            for name in sites[site].keys():
                if name not in local.keys(): local[name] = {'running':0}
                local[name]['running'] += sites[site][name]['running']
                
                
    if excludesitepattern != "":
        print 'Sites:',sitenamepattern,'excluding:',excludesitepattern
    else:
        print 'Sites:',sitenamepattern
    print '-----------------------------------------------'
    sum = 0
    if sortByWorkflow == True:
        for name in sorted(local):
            if quick == False:
                priority = None
                completion = None
                if name in workflow_info.keys():
                    priority = workflow_info[name]['Priority']
                    completion = workflow_info[name]['% Complete']            
                    status = workflow_info[name]['Status']
                    type = workflow_info[name]['Task type']
                print "%7i %7s %5s%% %s(%s,%s)" % (local[name]['running'],str(priority),str(completion),name,type,status)
            else:
                print "%7i %s" % (local[name]['running'],name)
            sum+=local[name]['running']
    else:
        for name in sorted(local,key=local.get,reverse=True):
            if quick == False:
                priority = None
                completion = None
                status = None
                if name in workflow_info.keys():
                    priority = workflow_info[name]['Priority']
                    completion = workflow_info[name]['% Complete']
                    status = workflow_info[name]['Status']
                    type = workflow_info[name]['Task type']
                    print "%7i %7s %5s%% %s(%s,%s)" % (local[name]['running'],str(priority),str(completion),name,type,status)
            else:
                print "%7i %s" % (local[name]['running'],name)
            sum+=local[name]['running']
    print '-----------------------------------------------'
    print "%7i %s" % (sum,'Total')
    print ''
    return sum
        
def main():
    usage="%prog <options>"

    parser = OptionParser(usage=usage)
    parser.add_option("-u", "--url", dest="url", help="URL to condor query json, default: https://cmst1.web.cern.ch/CMST1/WFMon/CondorJobs_Workflows.json", metavar="<url>")
    parser.add_option("-c", "--couchurl", dest="couchurl", help="Couch Instance url. default is cmssrv101.fnal.gov:7714", metavar="<couchurl>")
    parser.add_option("-q", "--quiet", action="store_true", dest="quick", default=False, help="Don't load workflow details from couch db.")

    parser.set_defaults(url="https://cmst1.web.cern.ch/CMST1/WFMon/CondorJobs_Workflows.json")
    parser.set_defaults(couchurl="cmssrv101.fnal.gov:7714")

    (opts, args) = parser.parse_args()

    url = opts.url
    couchurl = opts.couchurl
    quick = opts.quick

    # load workflow details from chouch db

    # don't count requests with the following status
    rejected_status = ['rejected-archived', 'aborted-archived', 'aborted', 'failed']

    workflow_info = {}
    if quick == False:
        # load requests from json
        # load requests from couch db
        header = {'Content-type': 'application/json', 'Accept': 'application/json'}
        conn = httplib.HTTPConnection(couchurl)
        conn.request("GET", '/latency_analytics/_design/latency/_view/maria', headers= header)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        myString = data.decode('utf-8')
        workflows_from_couch = json.loads(myString)['rows']

        for entry in workflows_from_couch:
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
            # reject some status
            # if workflow_dict['Status'] in rejected_status: continue
            # exclude ACDC
            # if re.compile('[\w\-]*ACDC[\w\-]*').match(workflowname) is not None: continue
            workflow_info[workflowname] = workflow_dict

    # load info from condor

    workflows = json.load(urllib2.urlopen(url))

    sites = {}

    for workflow in workflows.keys():
        name = workflow
        running = workflows[workflow]['runningJobs']
        # pending = workflows[workflow]['pendingJobs']
        for site in running.keys():
            if site not in sites.keys(): sites[site] = {}
            if name not in sites[site].keys(): sites[site][name] = {'running' : 0}
            sites[site][name]['running'] += running[site]
            
    absolutetotal = 0
    printWorkflowsPerSite('T1','', sites, workflow_info, False, quick)
    absolutetotal += printWorkflowsPerSite('T1_DE_KIT','', sites, workflow_info, False, quick)
    absolutetotal += printWorkflowsPerSite('T1_ES_PIC','', sites, workflow_info, False, quick)
    absolutetotal += printWorkflowsPerSite('T1_FR_CCIN2P3','', sites, workflow_info, False, quick)
    absolutetotal += printWorkflowsPerSite('T1_IT_CNAF','', sites, workflow_info, False, quick)
    absolutetotal += printWorkflowsPerSite('T1_RU_JINR','', sites, workflow_info, False, quick)
    absolutetotal += printWorkflowsPerSite('T1_TW_ASGC','', sites, workflow_info, False, quick)
    absolutetotal += printWorkflowsPerSite('T1_UK_RAL','', sites, workflow_info, False, quick)
    absolutetotal += printWorkflowsPerSite('T1_US_FNAL','', sites, workflow_info, False, quick)
    absolutetotal += printWorkflowsPerSite('T2_CH_CERN','', sites, workflow_info, False, quick)
    absolutetotal += printWorkflowsPerSite('T2','T2_CH_CERN', sites, workflow_info, False, quick)
    absolutetotal += printWorkflowsPerSite('T3','', sites, workflow_info, False, quick)

    print'Absolute Total'
    print '-----------------------------------------------'
    print "%7i %s" % (absolutetotal,'Absolute Total')
    print ''

if __name__ == "__main__":
    main()
    sys.exit(0);
