#!/usr/bin/env python

import sys,getopt
import urllib
import xml.etree.ElementTree as ET

def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
            
def clean(tag):
    return tag.split('}')[1].strip().lower()

def EmptyFilterDict(property_categories):
    tmp_dictionary = {}
    for category in property_categories:
        tmp_dictionary[category] = ''
    return tmp_dictionary
    
def freeze(o):
  if isinstance(o,dict):
    return frozenset({ k:freeze(v) for k,v in o.items()}.items())

  if isinstance(o,list):
    return tuple([freeze(v) for v in o])

  return o


def make_hash(o):
    """
    makes a hash out of anything that contains only list,dict and hashable types including string and numeric types
    """
    return hash(freeze(o))

input_csv = open('mailFilters.csv')

lines = input_csv.readlines()

property_categories = []
for entry in lines[0].strip().split(','):
    property_categories.append(entry.strip())
    
rules = []

for line in lines[1:]:
    filters = {}
    entries = line.strip().split(',')
    for counter in range(len(entries)):
        filters[property_categories[counter]] = entries[counter]
    rules.append(filters)
    
declaration = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>'
root = ET.Element("feed")
root.set('xmlns','http://www.w3.org/2005/Atom')
root.set('xmlns:apps','http://schemas.google.com/apps/2006')

title = ET.SubElement(root,'title')
title.text = 'Mail Filters'

author = ET.SubElement(root,'author')
name = ET.SubElement(author,'name')
name.text = 'Oliver Gutsche'
email = ET.SubElement(author,'email')
email.text = 'oguatworld@gmail.com'

for rule in rules:
    
    if 'label' in rule.keys():
        labels = rule['label'].strip().split(';')
        for label in labels:
            entry = ET.SubElement(root,'entry')
            category = ET.SubElement(entry,'category')
            category.set('term','filter')
            title = ET.SubElement(entry,'title')
            title.text = 'Mail Filter'
            content = ET.SubElement(entry,'content')
            for filter in rule.keys():
                if filter == 'label': continue
                if rule[filter] == '': continue
                prop = ET.SubElement(entry,'apps:property')
                prop.set('name',filter)
                prop.set('value',rule[filter])
            lab = ET.SubElement(entry,'apps:property')
            lab.set('name','label')
            lab.set('value',label)
            
    else:
        entry = ET.SubElement(root,'entry')
        category = ET.SubElement(entry,'category')
        category.set('term','filter')
        title = ET.SubElement(entry,'title')
        title.text = 'Mail Filter'
        content = ET.SubElement(entry,'content')
        for filter in rule.keys():
            if rule[filter] == '': continue
            prop = ET.SubElement(entry,'apps:property')
            prop.set('name',filter)
            prop.set('value',rule[filter])
            

output = open('oli.xml','w')
output.write(declaration + '\n')
indent(root)
output.write(ET.tostring(root))
output.close()