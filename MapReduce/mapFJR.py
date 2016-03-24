#!/usr/bin/env python

import sys,json

for line in sys.stdin:

    try:
        fjr = json.loads(line.strip())
    except:
        print ''
        print 'new line'
        print ''
        print line

    workload = fjr['workload']
    steps = fjr['steps']
    for step in steps:
        if 'performance' not in fjr[step].keys():
            print "%s_%s\t%s" % (workload,"NONE","NONE")
            continue
        if 'memory' not in fjr[step]['performance'].keys():
            print "%s_%s\t%s" % (workload,step,"NONE")
            continue
        if  'PeakValueRss' not in fjr[step]['performance']['memory'].keys():
            print "%s_%s\t%s" % (workload,step,"NONE")
            continue
        print "%s_%s\t%s" % (workload,step,fjr[step]['performance']['memory']['PeakValueRss'])
