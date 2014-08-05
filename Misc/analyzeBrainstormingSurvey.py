#!/usr/bin/env python

import os,sys

input = open('input.tsv')
survey = {}
days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Sessions']
times = ['1PM - 3PM','2PM - 4PM','3PM - 5PM','4PM - 6PM']

lines = input.readlines()
for line_number in range(1,len(lines)):
    line = lines[line_number].split('\t')
    name = line[1].strip()
    # print 'name:',name
    if name not in survey.keys(): survey[name] = {}
    for field_number in range(2,len(line)):
        # print 'day:',days[field_number-2],'times:',line[field_number].strip()
        if days[field_number-2] not in survey[name].keys(): survey[name][days[field_number-2]] = []
        if line[field_number].strip() == "": continue
        items = line[field_number].strip().split(',')
        for item in items:
            survey[name][days[field_number-2]].append(item.strip())

matrix = {}

for name in survey.keys():
    sessions = survey[name]['Sessions']
    for session in sessions:
        if session not in matrix.keys(): matrix[session] = {}
        for day in survey[name].keys():
            if day == 'Sessions': continue
            if day not in matrix[session].keys(): matrix[session][day] = {}
            for time in survey[name][day]:
                if time not in matrix[session][day].keys(): matrix[session][day][time] = []
                matrix[session][day][time].append(name)
                
for session in matrix.keys():
    print 'session:',session
    print ''
    for day in days[:-1]:
        for time in times:
            tmp_array = []
            if day in matrix[session].keys() and time in matrix[session][day].keys():
                tmp_array = matrix[session][day][time]
            print "%10s: %12s Number of participants: %2i Participants %s" % (day,time,len(tmp_array),','.join(tmp_array))
    print ''