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
    parser.add_option("-p", "--path", action="store", type="string", default=None, dest="path", help="Path to obfuscate, if not specified, use current directory")
    parser.add_option("-o", "--output", action="store", type="string", default='output.json', dest="output", help="Filename to document file obfuscation in JSON format, default: output.json")
    (opts, args) = parser.parse_args()
    verbose=opts.verbose
    do_nothing=opts.do_nothing
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
        
    # create dictionary for files and their obfuscated version
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
            tmpfile = os.path.join(root, file)
            actiondict[tmpfile] = os.path.join(path,str(uuid.uuid4())+'.root')

    if verbose:
        print ""
        print "following files will be obfuscated:"
        for file in actiondict.keys():
            print actiondict[file],'obfuscates',file
    
    # store actiondict in json file
    json_output = open(outputfilename,'w')
    json.dump(actiondict,json_output)
    json_output.close()
    if verbose:
        print ''
        print 'File obfuscation successfully documented in:',outputfilename

    # move files
    if verbose:
        print ""
    for file in actiondict.keys():
        # check if destination directory exists, otherwise create it
        dest_dir = os.path.dirname(actiondict[file])
        if  not os.path.exists(dest_dir):
            if verbose:
                print "destination directory",dest_dir,'does not exist, creating!'
            if do_nothing:
                print "DO NOTHING: creating directory",dest_dir
            else:
                os.mkdir(dest_dir)
        # rename file
        if verbose:
            print "renaming",file,'to',actiondict[file]
        if do_nothing:
            print "DO NOTHING: renaming",file,'to',actiondict[file]
        else:
            os.rename(file,actiondict[file])
            
    # remove input directory tree
    tmp_dirs = []
    for file in actiondict.keys():
        tmp_dir = os.path.dirname(file)
        tmp_dir = tmp_dir.replace(path+'/','')
        if tmp_dir not in tmp_dirs: tmp_dirs.append(tmp_dir)
    # reverse sort by length
    tmp_dirs.sort(key=len,reverse=True)
    if verbose:
        print ""
        print "Input directories to be cleaned up:",tmp_dirs
    # remove directories
    for dir in tmp_dirs:
        dir_to_be_removed = os.path.join(path,dir)
        if verbose:
            print "directory to be removed:",dir_to_be_removed
        if do_nothing:
            print "DO NOTHING: remove directory:",dir_to_be_removed
        else:
            os.rmdir(dir_to_be_removed)
    
if __name__ == "__main__":
    main()
    sys.exit(0);
