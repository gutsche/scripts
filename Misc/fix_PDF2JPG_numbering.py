#!/usr/bin/env python

import os,sys,re

# current directory
currentDir = os.getcwd()

pattern = '.* (\d+)$'
digits = re.compile(pattern)

for (root, dirs, files) in os.walk(currentDir):
   for file in files:
      # exclude dot-files
      if file.startswith('.'): continue
      (root,ext) = os.path.splitext(file)
      if digits.match(root) == None:
         new = root + " 01" + ext
         print 'renaming',file,'into',new
         os.rename(file,new)
