#!/usr/bin/env python

import sys,os

input_list = open('requests.list')
# input_list = open('test3.list')

data = '/*/Fall13*/GEN-SIM'
data_regexp = data.replace('*','[\w\-]*',99)


results = {}

for line in input_list.readlines():
    array = line.split()
    workflowname = array[0]
    status = array[1]
    basename = '_'.join(workflowname.split('_')[1:-3])
    if basename.lower().count('test') > 0: continue
    if basename.lower().count('-fall13-') == 0: continue
    if basename not in results.keys(): results[basename] = []
    results[basename].append([workflowname,status])
    
counter = 0
selected_key = ''
for key in results.keys():
    if len(results[key]) > counter:
        counter = len(results[key])
        selected_key = key
        
print selected_key
for entry in sorted(map(lambda x: [x[1],x[0]],results[selected_key])):
    print entry[0],entry[1]
