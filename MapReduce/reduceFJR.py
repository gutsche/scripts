#!/usr/bin/env python

import sys,json

input_dict = {}
# read input
for line in sys.stdin:
    (key,val) = line.strip().split()
    if key not in input_dict.keys(): input_dict[key] = []
    if val != 'NONE': input_dict[key].append(float(val))
    
# calculate average
for tmp_key in input_dict.keys():
    if len(input_dict[tmp_key]) == 0:
        print "%s\t%s" % (tmp_key,'NONE')
    else:
        average = sum(input_dict[tmp_key])/len(input_dict[tmp_key])
        print "%s\t%f" % (tmp_key,average)