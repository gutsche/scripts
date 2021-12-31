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

def logprint(text):
    print("{0}: {1}".format(time(),text))

def start_nas(command,sleep_seconds,verbose):
    if verbose >= 1: logprint("Start NAS")
    result = subprocess.run(shlex.split(ipmi_start_command))
    # sleep for 5 min
    sleep(sleep_seconds)
    if verbose >= 1: logprint("NAS started")

def main():
    # start of execution
    logprint("Starting execution of homelab-storage script")

    # initialization
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count", help="increase output verbosity", default=0)
    parser.add_argument("-d", "--dir", action="store", help="NAS main directory (default: %(default)s)", default='/cifs/Homelab-Scratch')
    parser.add_argument("-t", "--temp", action="store", help="temporary directory name holding lock files (default: %(default)s)", default='temp')
    parser.add_argument("-c", "--config", action="store", help="Config file (default: %(default)s)", default='$HOME/.homelab-storage')
    parser.add_argument("-s", "--sleep", action="store", help="Time in seconds to sleep after server is started (default: %(default)d)", default=300, type=int)
    parser.add_argument("--ipmi_address", action="store", help="IMPI interface address (default: %(default)s)", default='192.168.196.35')
    parser.add_argument("--ipmi_command", action="store", help="Full path to IPMI command (default: %(default)s)", default='/usr/bin/ipmitool')
    requiredNamed = parser.add_argument_group('required named arguments:')
    requiredNamed.add_argument("-m", "--mode", action="store", help="start or stop homelab-storage NAS", choices=["start","stop"], required=True)
    requiredNamed.add_argument("-i", "--identifier", action="store", help="identifies who called the start/stop script", required=True)
    args = parser.parse_args()
    verbose = args.verbose
    mode = args.mode
    identifier = args.identifier
    sleep_seconds = args.sleep
    ipmi_command = args.ipmi_command
    ipmi_address = args.ipmi_address
    tempdir = os.path.join(args.dir,args.temp)
    lockfile = os.path.join(tempdir,'{0}.lock'.format(identifier))
    
    # read .homelab-storage configuration file
    conf_filename = os.path.join(os.path.expanduser("~"),'.homelab-storage')
    # if configuration file does not exist, exit
    if not os.path.exists(conf_filename):
        print("Configuration file does not exist: {0}".format(conf_filename))
        sys.exit(1)
    # check for configuration file attribute to be 600
    conf_mode = int(str(oct(os.stat(conf_filename).st_mode))[5:])
    if conf_mode != 600:
        print('Configuration file can only be readable and writeable by the owner, noone else (600). Please change the configuration file attributes of {0}'.format(conf_filename))
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(conf_filename)
    if "HOMELAB-STORAGE-IPMI" not in config:
        print("'HOMELAB-STORAGE-IPMI' section missing in config file {0}".format(conf_filename))
        sys.exit(1)
    if 'password' not in config['HOMELAB-STORAGE-IPMI'] or 'username' not in config['HOMELAB-STORAGE-IPMI']:
        print("'username' and 'password' for IPMI access to HOMELAB-STORAGE server need to be defined in config file {0}".format(conf_filename))
        sys.exit(1)

    ipmi_username = config['HOMELAB-STORAGE-IPMI']['username']
    ipmi_password = config['HOMELAB-STORAGE-IPMI']['password']
    if verbose >= 2: logprint("IPMI username is {0}".format(ipmi_username))

    # check if impi tool exists
    if not os.path.exists(ipmi_command):
        print("The ipmi tool was not found at {0}, please specify the correct location of the tool.".format(ipmi_command))
        sys.exit(1)

    ipmi_start_command = "{0} -H {1} -U {2} -P {3} power on".format(ipmi_command,ipmi_address,ipmi_username,ipmi_password)
    ipmi_stop_command = "{0} -H {1} -U {2} -P {3} power soft".format(ipmi_command,ipmi_address,ipmi_username,ipmi_password)

    # ipmi_start_command = "echo \"Start World\""
    # ipmi_stop_command = "echo \"Stop World\""

    if mode == "start":
        if verbose >= 1: logprint("Mode: start")
        # temp directory tempdir exists?
        if not os.path.exists(tempdir):
            if verbose >= 1: logprint("Directory tempdir does not exist, NAS is not running, starting NAS")
            if verbose >= 1: logprint("Start NAS")
            result = subprocess.run(shlex.split(ipmi_start_command))
            # sleep for 5 min
            sleep(sleep_seconds)
            if verbose >= 1: logprint("NAS started")
        if not os.path.exists(tempdir):
            if verbose >= 2: logprint("NAS is running and directory tempdir does not exist, create directory tempdir")
            os.mkdir(tempdir)
        if not os.path.isdir(tempdir):
            if verbose >= 2: logprint("NAS is running, tempdir exists but is not a directory, remove file tempdir and create directory tempdir")
            os.remove(tempdir)
            os.mkdir(tempdir)
        # check if there are other lock files in the tempdir
        numlockfiles = len([f for f in os.listdir(tempdir) if f.endswith('.lock') and os.path.isfile(os.path.join(tempdir, f))])
        if verbose >= 2: logprint("Number of lockfiles found: {0}".format(numlockfiles))
        # if lockfiles already exist, just create the one of this process, then exit, otherwise start NAS
        if numlockfiles > 0:
            if os.path.exists(lockfile):
                if verbose >= 2: logprint("File lockfile does exist, process already requested start of NAS")
            else:
                if verbose >= 2: logprint("Other lockfiles already exist, just creating the lockfile of this process: {0}".format(lockfile))
                open(lockfile,'a').close()
        else:
            if os.path.exists(lockfile):
                if verbose >= 2: logprint("File lockfile does exist, process already requested start of NAS")
            else:
                if verbose >= 2: logprint("Create the lockfile of this process: {0}".format(lockfile))
                open(lockfile,'a').close()

    else:
        if verbose >= 1: logprint("Mode: stop")
        # if lockfile does not exist, don't do anything, this action has not accessed the NAS
        if not os.path.exists(lockfile):
            logprint("This action never accessed the NAS, don't do anything")
            sys.exit(0)
        # check if there are other lock files in the tempdir
        numlockfiles = len([f for f in os.listdir(tempdir) if f.endswith('.lock') and os.path.isfile(os.path.join(tempdir, f))])
        if verbose >= 2: logprint("Number of lockfiles found: {0}".format(numlockfiles))
        # if there are more than 2 lock files, remove the lock file of this process
        if numlockfiles > 1:
            os.remove(lockfile)
            if verbose >= 2: logprint("Only removed lockfile: {0}".format(lockfile))
        else:
            if verbose >= 1: logprint("Stopping NAS")
            result = subprocess.run(shlex.split(ipmi_stop_command))
            if verbose >= 1: logprint("NAS stopped")
            os.remove(lockfile)
            if verbose >= 2: logprint("Removed lockfile: {0}".format(lockfile))
    
    # end of execution
    logprint("Ending execution of homelab-storage script")

if __name__ == "__main__":
    main()
    sys.exit(0);
