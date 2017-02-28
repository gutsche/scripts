#!/usr/bin/env python

import os,sys, re
import json, datetime
from optparse import OptionParser

usage  = "Usage: %prog [options]"
parser = OptionParser(usage=usage)
parser.add_option("-v", "--verbose", action="store_true", default=False, dest="verbose", help="verbose output")
parser.add_option("-i", "--input", action="store", default=None, dest="input", help="input JSON file name")
(opts, args) = parser.parse_args()

verbose = opts.verbose

if opts.input == None:
    parser.error("Please specify input JSON file name with -i")
    
input = json.load(open(opts.input))

for note in input:
    #parse first line of file to extract title
    first_line = note['content'].split('\n')[0]
    if first_line[0] != '#':
        print 'Problem with input file',file,'No title in first line',first_line
        continue
    title = first_line[2:]
    title = title.replace('/','-')
    title = title.replace('&amp;','&')
    title = title.replace(';','')
    title = re.sub(r'\d{6}', '', title).strip()
    if verbose:
        print 'VERBOSE: title:',title
        
    # determine create date string
    org_createdate = datetime.datetime.strptime(note['createdate'],'%b %d %Y %H:%M:%S')
    createdate = org_createdate.strftime("%y%m%d")
    
    # store content in file
    file = open(createdate+' '+title+'.txt','w')
    file.write(note['content'].encode("utf-8"))
    file.close()
    
    
    
