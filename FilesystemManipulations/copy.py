#!/usr/bin/env python
# -*- coding: utf-8 -*-

verbose=False

import sys,os,shutil,getopt

def copy(sourcedir,destdir,relfilepath):
    dir = destdir + '/' + os.path.dirname(relfilepath)
    source = sourcedir + '/' + relfilepath
    destination = destdir + '/' + relfilepath

    try:
        os.makedirs(dir)
        print 'created dir "' + dir + '"'
    except:
        if verbose:
            print 'dir "' + dir + '" already exists.'
    try:
        shutil.copy(source,destination)
        print 'copied "' + source + '" to "' + destination + '"'
        sys.stdout.flush()
    except:
        if verbose:
            print 'file "' + destination + '" already exists.'


source = None
destination = None
filelistname = None

try:
    opts, args = getopt.getopt(sys.argv[1:], "", ["source=","destination=","filelist="])
except getopt.GetoptError:
    print 'Please specify source directory, destination directory and filelist containing relateive paths to source and destination'
    sys.exit(2)

# check command line parameter
for opt, arg in opts :
    if opt == "--source" :
        source = arg
    if opt == "--destination" :
        destination = arg
    if opt == "--filelist" :
        filelistname = arg
        

if source == None or destination == None or filelistname == None:
    print 'Please specify source directory, destination directory and filelist containing relateive paths to source and destination'
    sys.exit(2)

filelisthandle = open(filelistname)
for file in filelisthandle.readlines():
    copy(source,destination,file[2:].strip())