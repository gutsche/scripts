#!/usr/bin/env python

import os,sys,json,urllib2

def printWorkflowsPerSite(sitenamepattern, excludesitepattern, sites, sortByWorkflow):
    local = {}
    for site in sites.keys():
        if excludesitepattern != "" and site.count(excludesitepattern) > 0: continue
        if site.count(sitenamepattern) > 0:
            for name in sites[site].keys():
                if name not in local.keys(): local[name] = 0
                local[name] += sites[site][name]
                
    print 'Sites:',sitenamepattern
    print '-----------------------------------------------'
    sum = 0
    if sortByWorkflow == True:
        for name in sorted(local):
            print "%7i %s" % (local[name],name)
            sum+=local[name]
    else:
        for name in sorted(local,key=local.get,reverse=True):
            print "%7i %s" % (local[name],name)
            sum+=local[name]
    print '-----------------------------------------------'
    print "%7i %s" % (sum,'Total')
    print ''
    return sum
        
# workflows = json.load(open('CondorJobs_Workflows.json'))
workflows = json.load(urllib2.urlopen('https://cmst1.web.cern.ch/CMST1/WFMon/CondorJobs_Workflows.json'))

sites = {}

for workflow in workflows.keys():
    name = workflow
    running = workflows[workflow]['runningJobs']
    pending = workflows[workflow]['pendingJobs']
    for site in running.keys():
        if site not in sites.keys(): sites[site] = {}
        if name not in sites[site].keys(): sites[site][name] = 0
        sites[site][name] += running[site]

absolutetotal = 0
printWorkflowsPerSite('T1','', sites, False)
absolutetotal += printWorkflowsPerSite('T1_DE_KIT','', sites, False)
absolutetotal += printWorkflowsPerSite('T1_ES_PIC','', sites, False)
absolutetotal += printWorkflowsPerSite('T1_FR_CCIN2P3','', sites, False)
absolutetotal += printWorkflowsPerSite('T1_IT_CNAF','', sites, False)
absolutetotal += printWorkflowsPerSite('T1_RU_JINR','', sites, False)
absolutetotal += printWorkflowsPerSite('T1_TW_ASGC','', sites, False)
absolutetotal += printWorkflowsPerSite('T1_UK_RAL','', sites, False)
absolutetotal += printWorkflowsPerSite('T1_US_FNAL','', sites, False)
absolutetotal += printWorkflowsPerSite('T2_CH_CERN','', sites, False)
absolutetotal += printWorkflowsPerSite('T2','T2_CH_CERN', sites, False)
absolutetotal += printWorkflowsPerSite('T3','', sites, False)

print'Absolute Total'
print '-----------------------------------------------'
print "%7i %s" % (absolutetotal,'Absolute Total')
print ''