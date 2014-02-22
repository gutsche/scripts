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
        

def blockquery(datasets,showOnlyT1,skipT0):

    output = {}

    for dataset in datasets:

        url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/blockreplicas?dataset=' + dataset
        jstr = urllib2.urlopen(url).read()
        jstr = jstr.replace("\n", " ")
        result = json.loads(jstr)

        if dataset not in output.keys(): output[dataset] = {'total':{'size':0,'nfiles':0},'custodial':{},'non-custodial':{}}

        try:
            for block in result['phedex']['block']:
                name = block['name']
                output[dataset]['total']['size'] += block['bytes']
                output[dataset]['total']['nfiles'] = block['files']
                if block['is_open'] == 'y':
                    print 'block:',name,'is open'
                for replica in block['replica']:
                    nfiles = replica['files']
                    size = replica['bytes']
                    site = replica['node']
                    if skipT0 == True and site[0:2] == 'T0': continue
                    if showOnlyT1 == True and not site[0:2] == 'T1': continue
                    if replica['complete'] == 'n':
                        print 'block:',name,'is not complete at site:',site
                    if replica['custodial'] == 'y' : 
                        if site not in output[dataset]['custodial'].keys(): output[dataset]['custodial'][site] = {'size':0,'nfiles':0}
                        output[dataset]['custodial'][site]['size'] += size
                        output[dataset]['custodial'][site]['nfiles'] += nfiles
                    else :
                        if site not in output[dataset]['custodial'].keys(): output[dataset]['non-custodial'][site] = {'size':0,'nfiles':0}
                        output[dataset]['non-custodial'][site]['size'] += size
                        output[dataset]['non-custodial'][site]['nfiles'] += nfiles
        except:
            print 'problems with dataset:',dataset

    return output
    
def main():

    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    parser.add_option("-m", "--mode", action="store", type="string", default='size', dest="mode", help="Specify --mode files/size/none to show information per site, default size")
    parser.add_option("-d", "--datasets", action="store", type="string", default=None, dest="datasets", help="Comma separated list of dataset names")
    parser.add_option("-t", "--transferRequests", action="store", type="string", default=None, dest="transferRequests", help="Comma separated list of transfer request ids")
    parser.add_option("-r", "--deletionRequests", action="store", type="string", default=None, dest="deletionRequests", help="Comma separated list of deletion request ids")
    parser.add_option("-1", "--showOnlyT1", action="store_true", default=False, dest="showOnlyT1", help="Only show T1 locations")
    parser.add_option("-0", "--skipT0", action="store_true", default=False, dest="skipT0", help="Skip T0 locations")
    (opts, args) = parser.parse_args()
    
    if ( opts.datasets == None and opts.transferRequests == None and opts.deletionRequests == None) :
        print ""
        print "Please specify comma separated list of dataset names or transfer request ids or deletion request ids!"
        print ""
        parser.print_help()
        sys.exit(2)

    verbose = opts.verbose
    mode = opts.mode
    datasets = []
    if opts.datasets != None: datasets = opts.datasets.split(',')
    if opts.transferRequests != None:
        requests = opts.transferRequests.split(',')
        for request in requests:
            url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/transferrequests?request=' + request
            jstr = urllib2.urlopen(url).read()
            jstr = jstr.replace("\n", " ")
            result = json.loads(jstr)

            for item in result['phedex']['request']:
                for dataset in item['data']['dbs']['dataset']:
                    datasets.append(dataset['name'])        
    if opts.deletionRequests != None:
        requests = opts.deletionRequests.split(',')
        for request in requests:
            url='https://cmsweb.cern.ch/phedex/datasvc/json/prod/deleterequests?request=' + request
            jstr = urllib2.urlopen(url).read()
            jstr = jstr.replace("\n", " ")
            result = json.loads(jstr)

            for item in result['phedex']['request']:
                for dataset in item['data']['dbs']['dataset']:
                    datasets.append(dataset['name'])        
        
    showOnlyT1 = opts.showOnlyT1
    skipT0 = opts.skipT0
                    
    output = blockquery(datasets,showOnlyT1,skipT0)

    for dataset in output.keys():
        
        custodial_sites = output[dataset]['custodial'].keys()
        non_custodial_sites = output[dataset]['non-custodial'].keys()

        custodial_sites.sort()
        non_custodial_sites.sort()

        sites = ''
        custsites = ''
        for site in non_custodial_sites :
            sites += site
            if mode == "files" :
                sites += '(' + str(output[dataset]['non-custodial'][site]['nfiles']) + ')'
            elif mode == "size" :
                sites += '(' + formatSize(output[dataset]['non-custodial'][site]['size']) + ')'
            sites += ','
        if sites[-1:] == ',' :
            sites = sites[:-1]
        for custsite in custodial_sites :
            custsites += custsite
            if mode == "files" :
                custsites += '(' + str(output[dataset]['custodial'][custsite]['nfiles']) + ')'
            elif mode == "size" :
                custsites += '(' + formatSize(output[dataset]['custodial'][custsite]['size']) + ')'
            custsites += ','
        if custsites[-1:] == ',' :
            custsites = custsites[:-1]
    
        if mode == 'size':
            print "dataset: %s total: (%s) custodial: %s non-custodial: %s" % (dataset,formatSize(output[dataset]['total']['size']),custsites,sites)
        elif mode == "files":
            print "dataset: %s total: (%s) custodial: %s non-custodial: %s" % (dataset,str(output[dataset]['total']['nfiles']),custsites,sites)
        else:
            print "dataset: %s custodial: %s non-custodial: %s" % (dataset,custsites,sites)



if __name__ == '__main__':
    main()