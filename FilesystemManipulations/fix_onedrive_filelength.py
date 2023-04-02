#! /usr/bin/env python3

import os,sys
import uuid
import stat
from time import sleep
from argparse import ArgumentParser
import json
from datetime import datetime
import subprocess, shlex
import configparser
import subprocess, shlex

def time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def logprint(text,level,setting):
    if level <= setting:
        print("{0}: {1}".format(time(),text))

def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts

def main():
    # start of execution
    logprint("Fix length of files recursively to fit in OneDrive",0,0)

    # initialization
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", help="increase output verbosity", default=0)
    parser.add_argument("-l", "--length", action="store", help="Maximum path length allowed (default: %(default)s)", default=300)
    parser.add_argument("-r", "--reduction", action="store", help="Maximum filename/path length without extension (default: %(default)s)", default=12)
    parser.add_argument("-t", "--test", action="store_true", help="If set, test without executing mv commands")
    requiredNamed = parser.add_argument_group('required named arguments:')
    requiredNamed.add_argument("-d", "--directory", action="store", help="Start Directory", required=True)
    args = parser.parse_args()
    verbose_setting = int(args.verbose)
    length_goal = int(args.length)
    reduction_limit = int(args.reduction)
    directory = os.path.abspath(args.directory)
    test = args.test
    logprint("Fixing OneDrive files path lengths to be less than {0} characters in directory {1}".format(length_goal,directory),1,verbose_setting)

    too_long_files = {}
    # walk through directory tree
    for (root, dirs, files) in os.walk(directory):
        for file in files:
            original_filename = os.path.join(root,file)
            original_filename_array = splitall(original_filename)
            original_filename_length = len(original_filename)
            target_filename = original_filename
            target_filename_array = original_filename_array[:]
            target_filename_length = len(target_filename)
            if original_filename_length > length_goal:
                logprint("Original file: {0} with length {1} is longer than goal {2}".format(original_filename,original_filename_length,length_goal),2,verbose_setting)
                # new_length = len(os.path.join('', *target_filename_array))
                counter = 0
                while (target_filename_length > length_goal):
                    # split off extension and reduce to number of characters defined in parameters
                    index = -1 - counter
                    oldtmpname = target_filename_array[index]
                    newtmpname = os.path.splitext(oldtmpname)[0][:reduction_limit] + os.path.splitext(oldtmpname)[1]
                    target_filename_array[index] = newtmpname
                    target_filename = os.path.join('', *target_filename_array)
                    target_filename_length = len(target_filename)
                    logprint("Counter {0} reduced {1} to {2} to new length {3} and new filename {4}".format(counter,oldtmpname,newtmpname,target_filename_length,target_filename),2,verbose_setting)
                    counter = counter + 1
                logprint("Original file: {0} with length {1} is longer than goal {2} and was reduced to new file: {3} with length {4}".format(original_filename,original_filename_length,length_goal,target_filename,target_filename_length),1,verbose_setting)
                tmp = {}
                tmp['original_filename'] = original_filename
                tmp['original_filename_array'] = original_filename_array
                tmp['target_filename'] = target_filename
                tmp['target_filename_array'] = target_filename_array
                if counter not in too_long_files.keys(): too_long_files[counter] = []
                too_long_files[counter].append(tmp)
                
    # shorted files on disk
    commands = []
    for counter in too_long_files.keys():
        for entry in too_long_files[counter]:
            # print(entry['original_filename_array'])
            # print(entry['target_filename_array'])
            basepath = os.path.join('', *entry['original_filename_array'][:-counter])
            source_mv_path = basepath
            dest_mv_path = basepath
            for index in range(counter):
                target_index = len(entry['original_filename_array']) - counter + index
                source_mv_path = source_mv_path + "/" + entry['original_filename_array'][target_index]
                dest_mv_path = dest_mv_path + "/" + entry['target_filename_array'][target_index]    
                if entry['original_filename_array'][target_index] != entry['target_filename_array'][target_index]:
                    cmd = "mv '" + source_mv_path + "' '" + dest_mv_path + "'"
                    if cmd not in commands: commands.append(cmd)   
                source_mv_path = dest_mv_path

    sorted_commands = sorted(commands, key=lambda t: t.count('/'))
    for command in sorted_commands:
        print("Executing command: {0}".format(command))
        if not test:
            os.system(command)

    # end of execution
    logprint("Ending to fix length of files recursively to fit in OneDrive",0,0)

if __name__ == "__main__":
    main()
    sys.exit(0);
