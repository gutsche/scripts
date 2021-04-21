#! /usr/bin/env python3

import os,sys,uuid
from optparse import OptionParser
import json
from datetime import datetime
import subprocess, shlex

selectingWalk = lambda targetDirectory, includedExtentions: (
    (root, dirs, [F for F in files if os.path.splitext(F)[1] in includedExtentions]) 
    for (root, dirs, files) in os.walk(targetDirectory)
)

def time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def logprint(text):
    print("{0}: {1}".format(time(),text))

def main():
    # start of execution
    logprint("Starting execution of Plex Library Post Processing Script")

    # initialization
    usage  = "Usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
    parser.add_option("-t", "--tvpath", action="store", type="string", default="/home/gutsche/PlexMedia", dest="tvpath", help="Path to TV shows")
    parser.add_option("-m", "--mpath", action="store", type="string", default="/Media/HD Movies", dest="mpath", help="Path to Movies")
    parser.add_option("-l", "--lockfile", action="store", type="string", default="/tmp/plexPostProcessing.lock", dest="lockfile", help="Don't execute script if this file exists.")
    (opts, args) = parser.parse_args()
    verbose=opts.verbose
    tvpath = opts.tvpath
    mpath = opts.mpath
    lockfile = opts.lockfile
    
    # lockfile handling
    if os.path.isfile(lockfile):
        logprint("Other instance of script is currently running, terminate this instance.")
        sys.exit(0)
    else:
        logprint("First instance of script, creating lock file")
        open(lockfile,'w').close()

    # threshold to delete files: 1MB
    filesize_threshold = 1000000
    input_files = []
    input_files_to_be_deleted = []
    update_plex_library = False

    # scan TV shows and Movies directory for *.ts files
    for line in selectingWalk(tvpath, [".ts"]):
        #exclude dot directories
        if '.' not in line[0]:
            for file in line[2]:
                filename = os.path.join(line[0],file)
                # check file size
                filesize = os.stat(filename).st_size
                if filesize < filesize_threshold:
                    input_files_to_be_deleted.append(filename)
                else:
                    input_files.append(filename)

    print("{0}: Files to be processed".format(time()))        
    for file in input_files:
        print(file)

    # process files
    for file in input_files:
        inputfile = file
        outputfile = file.replace(".ts",".mkv")
        logprint("Converting {0} to {1}".format(inputfile,outputfile))
        command = "/usr/local/bin/transcode-video --target small --no-log --handbrake-option encoder=x265 --encoder nvenc_h265 -o \"{0}\" \"{1}\"".format(outputfile,inputfile)
        result = subprocess.run(shlex.split(command))
        ## execution succeeded, delete input file if output file exists, set update plex library
        if result.returncode == 0:
            update_plex_library = True
            if os.path.isfile(outputfile):
                if os.path.isfile(inputfile):
                    os.remove(inputfile)

    print("{0}: Files to be deleted".format(time()))        
    for file in input_files_to_be_deleted:
        if os.path.isfile(file):
            print("{0}: Recording produced a file smaller than 1 MB, deleting file: {1}".format(time(),file))
            os.remove(file)

    # update plex libraries
    if update_plex_library == True:
        logprint("Updating plex libraries.")
        subprocess.run(shlex.split("/usr/bin/curl
            http://192.168.96.40:32400/library/sections/7/refresh?X-Plex-Token=<fillme>"))
        subprocess.run(shlex.split("/usr/bin/curl
            http://192.168.96.40:32400/library/sections/6/refresh?X-Plex-Token=<fillme>"))

    # remove lockfile
    logprint("Removing lock file.")
    if os.path.isfile(lockfile):
        os.remove(lockfile)

    # end of execution
    print("{0}: Ending execution of Plex Library Post Processing Script".format(time()))

if __name__ == "__main__":
    main()
    sys.exit(0);
