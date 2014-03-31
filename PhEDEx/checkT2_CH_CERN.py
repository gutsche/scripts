#!/usr/bin/env python

import sys,getopt,urllib2,json
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
        

def groupquery(node):

    output = {}

    url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/groupusage?node=' + node
    jstr = urllib2.urlopen(url).read()
    jstr = jstr.replace("\n", " ")
    result = json.loads(jstr)

    for node in result['phedex']['node']:
        nodename = node['name']
        if nodename not in output.keys(): output[nodename] = {}
        for group in node['group']:
            groupname = group['name'].lower()
            if groupname not in output[nodename].keys(): output[nodename][groupname] = 0.
            output[nodename][groupname] += group['dest_bytes']
            
    return output
    
def main():

    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    parser.add_option("-t", "--twiki", action="store_true", default=False, dest="twiki", help="TWiki table output")
    (opts, args) = parser.parse_args()
    
    verbose = opts.verbose
    twiki = opts.twiki
    
    # hardcoded quotas for T2_CH_CERN
    # IB Relval and AnalysisOps goes into DataOps
    # everything not identified here is added to Commissioning/caf-comm
    quota = {}
    quota['caf-comm'] = {'description' : 'Commissioning+Physics','quota' : 1325E12}
    quota['caf-alca'] = {'description' : 'AlcaReco','quota' : 225E12}
    quota['upgrade'] = {'description' : 'Upgrade','quota' : 225E12}
    quota['relval'] = {'description' : 'RelVal','quota' : 300E12}
    quota['caf-lumi'] = {'description' : 'Lumi','quota' : 225E12}
    quota['local'] = {'description' : 'local','quota' : 40E12}
    quota['express'] = {'description' : 'Express','quota' : 100E12}
    quota['dataops'] = {'description' : 'DataOps','quota' : 850E12}

    output = groupquery('T2_CH_CERN')
    
    for site in output.keys():
        print ''
        print 'Site:',site
        print ''
        if twiki == True:
            print '| *Group* | *Usage* |'
        for group in output[site].keys():
            if twiki == True:
                print '| %s |  %s |' % (group,formatSize(output[site][group]))
            else:
                print 'Group: %15s used: %15s' % (group,formatSize(output[site][group]))

    for site in output.keys():
        for group in output[site].keys():
            if group in quota.keys() and 'caf-comm' != group: 
                quota[group]['used'] = output[site][group]
            else :
                if 'used' not in quota['caf-comm'].keys(): quota['caf-comm']['used'] = 0
                if 'used' not in quota['dataops'].keys(): quota['dataops']['used'] = 0
                if group == 'ib relval' or group == 'analysisops' or group == "facops":
                    quota['dataops']['used'] += output[site][group]
                    if verbose == True: print 'group',group,'usage added to dataops'
                else:
                    quota['caf-comm']['used'] += output[site][group]
                    if verbose == True: print 'group',group,'usage added to caf-comm',formatSize(quota['caf-comm']['used'])
                
    print ''
    if twiki == True:
        print '| *Group* | *Description* | *Quota* | *Usage* | *Percentage* |'
    for group in quota.keys():
        if twiki == True:
            print '| %s | %s |  %s |  %s |  %6.2f |' % (group,quota[group]['description'],formatSize(quota[group]['quota']),formatSize(quota[group]['used']),float(quota[group]['used'])/float(quota[group]['quota'])*100.0)
        else :
            print 'group: %15s description: %25s quota: %10s used: %10s percentage: %6.2f' % (group,quota[group]['description'],formatSize(quota[group]['quota']),formatSize(quota[group]['used']),float(quota[group]['used'])/float(quota[group]['quota'])*100.0)

    print ''
    print 'Comments:'
    print ''
    print 'groups IB RelVal, AnalysisOps and FacOps are added to group DataOps'
    print 'Commissioning and Physics are treated together and their quotas are added'
    print 'All groups not with dedicated quota are added to Commissioning'
    print ''
if __name__ == '__main__':
    main()
