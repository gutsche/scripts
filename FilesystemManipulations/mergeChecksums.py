#!/usr/bin/env python
import os,sys
from optparse import OptionParser
import json


def main():
    # initialization
    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    parser.add_option("-i", "--input", action="append", type="string", default=None, dest="paths", help="Input file, use multiple times to add more than two files")
    parser.add_option("-o", "--output", action="store", type="string", default='output.json', dest="output", help="Filename to document checksums in JSON format, default: output.json")
    (opts, args) = parser.parse_args()
    verbose=opts.verbose
    # do_nothing=opts.do_nothing
    paths=opts.paths
    outputfilename = opts.output

    # verbose output
    if verbose:
        print ''
        print 'Number of files to merge:',len(paths)
        total = 0
        for path in paths:
            tmp = len(json.load(open(path)).keys())
            total += tmp
            print 'Number of entries in file',path,':',tmp
        print 'Total number of entries to merge',total

    actiondict = {}
    
    for path in paths:
        tmpdict = json.load(open(path))
        for file in tmpdict.keys():
            if file not in actiondict.keys():
                actiondict[file] = tmpdict[file]
            else:
                print "conflict, file:",file,"is listed twice in input files, last occurance in",path


    # store actiondict in json file
    json_output = open(outputfilename,'w')
    json.dump(actiondict,json_output)
    json_output.close()
    if verbose:
        print ''
        print 'Checksums successfully documented in:',outputfilename
        print 'Output contains',len(actiondict.keys()),'entries.'

if __name__ == "__main__":
    main()
    sys.exit(0);
