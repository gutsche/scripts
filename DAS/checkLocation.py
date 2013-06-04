#!/usr/bin/env python

import sys,getopt,urllib,json
from das_client import get_data

def blockquery(dasHost,query):
    output = {}
    das_data = get_data(dasHost,query,0,0,0)
    if isinstance(das_data, basestring):
        result = json.loads(das_data)
    else:
        result = das_data
    if result['status'] == 'fail' :
        print 'DAS query failed with reason:',result['reason']
    else :
        for entry in result['data'] :
            # determine phedex resul index
            phedex_result_index = entry['das']['system'].index('phedex')
            phedex_block = entry['block'][phedex_result_index]
            name = phedex_block['dataset']
            if name not in output.keys(): output[name] = {'custodial':{},'non-custodial':{}}
            for replica in phedex_block['replica'] :
                nfiles = replica['nfiles']
                size = replica['size']
                site = replica['site']
                if replica['custodial'] == 'y' : 
                    if site not in output[name]['custodial'].keys(): output[name]['custodial'][site] = {'size':0,'nfiles':0}
                    output[name]['custodial'][site]['size'] += size
                    output[name]['custodial'][site]['nfiles'] += nfiles
                else :
                    if site not in output[name]['custodial'].keys(): output[name]['non-custodial'][site] = {'size':0,'nfiles':0}
                    output[name]['non-custodial'][site]['size'] += size
                    output[name]['non-custodial'][site]['nfiles'] += nfiles
    return output
    
def main():

    datasetpath = None
    allSites = True
    mode = 'none'
    dasHost = 'https://cmsweb.cern.ch'

    try:
        opts, args = getopt.getopt(sys.argv[1:], "", ["dataset=","onlyT1","mode=","help"])
    except getopt.GetoptError:
        print 'Please specify dataset with --dataset'
        print 'Specify --onlyT1 to show only T1 sites'
        print 'Specify --mode files/size/none to show information per site'
        sys.exit(2)

    # check command line parameter
    for opt, arg in opts :
        if opt == "--dataset" :
            datasetpath = arg
        if opt == "--onlyT1" :
            allSites = False
        if opt == "--mode" :
            mode = arg
        if opt == "--help" :
            print 'Please specify dataset with --dataset'
            print 'Specify --onlyT1 to show only T1 sites'
            print 'Specify --mode files/size/none to show information per site'
            sys.exit(2)
                    
    if datasetpath == None:
        print 'Please specify dataset with --dataset'
        print 'Specify --onlyT1 to show only T1 sites'
        print 'Specify --mode files/size/none to show information per site'
        sys.exit(2)

    query="block dataset=%s | grep block" % (datasetpath)
    output = blockquery(dasHost,query)

    for dataset in output.keys():
        
        if allSites == True:
            custodial_sites = output[dataset]['custodial'].keys()
            non_custodial_sites = output[dataset]['non-custodial'].keys()
        else:
            custodial_sites = []
            non_custodial_sites = []
            for site in output[dataset]['custodial'].keys():
                if site[:2] == 'T1': custodial_sites.append(site)
            for site in output[dataset]['non-custodial'].keys():
                if site[:2] == 'T1': non_custodial_sites.append(site)

        custodial_sites.sort()
        non_custodial_sites.sort()

        sites = ''
        custsites = ''
        for site in non_custodial_sites :
            sites += site
            if mode == "files" :
                sites += '(' + str(output[dataset]['non-custodial'][site]['nfiles']) + ')'
            elif mode == "size" :
                sites += '(' + str(output[dataset]['non-custodial'][site]['size']) + ')'
            sites += ','
        if sites[-1:] == ',' :
            sites = sites[:-1]
        for custsite in custodial_sites :
            custsites += custsite
            if mode == "files" :
                custsites += '(' + str(output[dataset]['custodial'][custsite]['nfiles']) + ')'
            elif mode == "size" :
                custsites += '(' + str(output[dataset]['custodial'][custsite]['size']) + ')'
            custsites += ','
        if custsites[-1:] == ',' :
            custsites = custsites[:-1]
    
        print 'dataset:',datasetpath,'custodial:',custsites,'non-custodial:',sites



if __name__ == '__main__':
    main()