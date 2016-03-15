#!/usr/bin/env python

import os,sys,shutil
from optparse import OptionParser

def main():
    # initialization
    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    parser.add_option("-n", "--do_nothing", action="store_true", default=False, dest="do_nothing", help="Dry run, do nothing")
    parser.add_option("-p", "--path", action="store", type="string", default=None, dest="path", help="Path to obfuscate, if not specified, use current directory")
    (opts, args) = parser.parse_args()
    verbose=opts.verbose
    do_nothing=opts.do_nothing
    path=opts.path

    # use current directory if path was not specified
    if path == None:
        path = os.getcwd()
    # clean last / from path
    if path.endswith('/'): path = path[:-1]
    if verbose:
        print ""
        print "Current directory:",path
        
    # create dictionary for base names and their associated files
    actiondict = {}

    # get recursive list of files
    for (root, dirs, files) in os.walk(path):
        for file in files:
            # exclude dot-files
            if file.startswith('.'): continue
            # exclude dot-directories, need to clean root of path
            if root.replace(path,'')[1:].startswith('.'): continue
            if verbose:
                print 'VERBOSE: os.walk resulted in: root:',root,'dirs:',dirs,'file:',file
            base = os.path.splitext(file)[0]
            if base not in actiondict.keys(): actiondict[base] = []
            actiondict[base].append(os.path.join(root,file))
    if verbose:
        for tmp_base in actiondict.keys():
            print 'VERBOSE: base:',tmp_base,'files:',actiondict[tmp_base]


    # create temporary directory for files already existing (dupicates)
    tmp_dir = os.path.join(path,"duplicates")
    if os.path.exists(tmp_dir):
        print "tmp_dir exists, clean up!"
        sys.exit(1)
    else:
            os.mkdir(tmp_dir)
    for tmp_base in actiondict.keys():
        # make directories in path
        dest_dir = os.path.join(path,tmp_base)
        if  not os.path.exists(dest_dir):
            if verbose:
                print "VERBOSE: destination directory",dest_dir,'does not exist, creating!'
            if do_nothing:
                print "DO NOTHING: creating directory",dest_dir
            else:
                os.mkdir(dest_dir)
        # mv files
        for file in actiondict[tmp_base]:
            # check if file already exists in dest_dir
            if os.path.exists(os.path.join(dest_dir,os.path.basename(file))):
                print "Duplicate, moving to tmp dir:",file
                shutil.move(file,tmp_dir)
            elif do_nothing:
                print "DO NOTHING: move file",file,"to directory",dest_dir
            else:
                shutil.move(file,dest_dir)
    
if __name__ == "__main__":
    main()
    sys.exit(0);
