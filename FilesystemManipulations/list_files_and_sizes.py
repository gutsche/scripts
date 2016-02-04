#!/usr/bin/env python

import os,sys, uuid
from optparse import OptionParser
import json

def main():
    # initialization
    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    parser.add_option("-p", "--paths", action="store", type="string", default=None, dest="paths", help="Paths to list files recursively separated by comma, if not specified, use current directory")
    parser.add_option("-o", "--output", action="store", type="string", default='output.json', dest="output", help="Filename to document file obfuscation in JSON format, default: output.json")
    (opts, args) = parser.parse_args()
    verbose=opts.verbose
    outputfilename = opts.output
    
    # current directory
    currentDir = os.getcwd()

    # use current directory if path was not specified, clean paths of trailing /
    tmppaths=opts.paths
    paths = []
    if tmppaths == None:
        tmppath = currentDir
        if tmppath.endswith('/'): tmppath = tmppath[:-1]
        paths.append(tmppath)
    else:
        for tmppath in tmppaths.split(','):
            if not os.path.isabs(tmppath): tmppath = os.path.join(currentDir,tmppath)
            if tmppath.endswith('/'): tmppath = tmppath[:-1]
            paths.append(tmppath)
    if verbose:
        print ""
        print "Working on following directories:",','.join(paths)
        
    # create dictionary for files and their obfuscated version
    actiondict = {}

    # get recursive list of files
    for path in paths:
        for (root, dirs, files) in os.walk(path):
            for file in files:
                # exclude dot-files
                if file.startswith('.'): continue
                # exclude dot-directories, need to clean root of path
                if root.replace(path,'')[1:].startswith('.'): continue
                # exclude output filename
                if file == outputfilename: continue
                tmpfile = os.path.join(root, file)
                tmpsize = os.path.getsize(tmpfile)
                if tmpsize not in actiondict.keys():
                    actiondict[tmpsize] = tmpfile
                    if verbose:
                        print 'added file',tmpfile,'with size',tmpsize
                else:
                    print 'error: found same size:',tmpsize,' for two different files'
                    print 'file 1:',actiondict[tmpsize]
                    print 'file 2:',tmpfile

    # store actiondict in json file
    json_output = open(outputfilename,'w')
    json.dump(actiondict,json_output)
    json_output.close()
    if verbose:
        print ''
        print 'File list successfully documented in:',outputfilename

    
if __name__ == "__main__":
    main()
    sys.exit(0);
