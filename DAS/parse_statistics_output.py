#!/usr/bin/env python

import sys,os

handle = open('tmp')

months = 5
lines = handle.readlines()
headers = []
lists = []

for lineindex in range(int(len(lines)/(months+3))):
  header = None
  tmplist = []
  header = lines[lineindex*(months+3)+1].strip()
  for index in range(months):
    entry = lines[lineindex*(months+3)+index+3].strip()
    if entry == '': entry = str(0)
    tmplist.append(entry)
  headers.append(header)
  lists.append(tmplist)


print ';'.join(headers)
for index in range(months):
  string = ''
  for entry in lists:
    string += entry[index] + ';'
  print string
  