#!/usr/bin/env python

import os,sys, uuid
from optparse import OptionParser
import json

def main():
    # initialization
    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    parser.add_option("-n", "--do_nothing", action="store_true", default=False, dest="do_nothing", help="Dry run, do nothing")
    parser.add_option("-i", "--input", action="store", type="string", default=None, dest="input", help="Input filename that contains the details of the obfuscation in JSON format that should be restored")
    (opts, args) = parser.parse_args()
    verbose=opts.verbose
    do_nothing=opts.do_nothing
    inputfilename=opts.input

    if inputfilename == None:
        print ""
        parser.print_help()
        parser.error('Pleae specify input')

    # read in input json
    actiondict = json.load(open(inputfilename))
    
    if verbose:
        print ""
        print "obfuscation of following files will be restored:"
        for file in actiondict.keys():
            print actiondict[file],'restorted to',file
        
    # move files
    if verbose:
        print ""
    for file in actiondict.keys():
        # check if destination directory exists, otherwise create it
        dest_dir = os.path.dirname(file)
        if  not os.path.exists(dest_dir):
            if verbose:
                print "destination directory",dest_dir,'does not exist, creating!'
            if do_nothing:
                print "DO NOTHING: creating directory",dest_dir
            else:
                os.makedirs(dest_dir)
        # rename file
        if verbose:
            print "renaming",actiondict[file],'to',file
        if do_nothing:
            print "DO NOTHING: renaming",actiondict[file],'to',file
        else:
            try:
                os.rename(actiondict[file],file)
            except:
                print "file:",actiondict[file],"could not be found"

if __name__ == "__main__":
    main()
    sys.exit(0);
