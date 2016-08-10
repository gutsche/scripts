#!/usr/bin/env python
BLOCKSIZE=32*1024*1024
import os,sys
from optparse import OptionParser
import json
from zlib import adler32

def calc_adler32(f):
    val = 1
    fp=open(f)
    while True:
        data = fp.read(BLOCKSIZE)
        if not data:
            break
        val = adler32(data, val)
    if val < 0:
            val += 2**32
    return hex(val)[2:10].zfill(8).lower()

def main():
    # initialization
    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    # parser.add_option("-n", "--do_nothing", action="store_true", default=False, dest="do_nothing", help="Dry run, do nothing")
    parser.add_option("-p", "--path", action="store", type="string", default=None, dest="path", help="Path to checksum all files recursively, if not specified, use current directory")
    parser.add_option("-o", "--output", action="store", type="string", default='output.json', dest="output", help="Filename to document checksums in JSON format, default: output.json")
    (opts, args) = parser.parse_args()
    verbose=opts.verbose
    # do_nothing=opts.do_nothing
    path=opts.path
    outputfilename = opts.output

    # use current directory if path was not specified
    if path == None:
        path = os.getcwd()
    # clean last / from path
    if path.endswith('/'): path = path[:-1]
    if verbose:
        print ""
        print "Current directory:",path
        
    # create dictionary for files and their checksums
    actiondict = {}

    # get recursive list of files
    for (root, dirs, files) in os.walk(path):
        for file in files:
            # exclude dot-files
            if file.startswith('.'): continue
            # exclude dot-directories, need to clean root of path
            if root.replace(path,'')[1:].startswith('.'): continue
            # exclude output filename
            if file == outputfilename: continue
            if verbose:
                print 'os.walk resulted in:',root,dirs,file
            actiondict[file] = {"root":root,"chksum":None}

    if verbose:
        print ""
        print "following files will be checksum'ed:"
        for file in actiondict.keys():
            print file,'in root directory',actiondict[file]["root"]
    
    #checksum files
    counter = 0
    total = len(actiondict.keys())
    for file in actiondict.keys():
        if verbose:
            counter += 1
            print 'Chksumming:',counter,'of',total,':',file
            sys.stdout.flush()
        chksum = calc_adler32(os.path.join(actiondict[file]["root"],file))
        actiondict[file]["chksum"] = chksum

    if verbose:
        print ""
        print "following files have been checksum'ed:"
        for file in actiondict.keys():
            print file,'in root directory',actiondict[file]["root"],'has checksum:',actiondict[file]["chksum"]

    # store actiondict in json file
    json_output = open(outputfilename,'w')
    json.dump(actiondict,json_output)
    json_output.close()
    if verbose:
        print ''
        print 'Checksums successfully documented in:',outputfilename

if __name__ == "__main__":
    main()
    sys.exit(0);
