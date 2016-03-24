#!/usr/bin/env python

import sys,getopt
import urllib
import xml.etree.ElementTree as ET

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
    

tree = ET.parse('mailFilters.xml')
root = tree.getroot()

# exclude following attribute names
exclude_attrib = ['label','sizeOperator','sizeUnit']

# collect property categories
property_categories = []
entry_counter = 0
for entry in root:
    entry_counter += 1
    if clean(entry.tag) == "entry":
        for item in entry:
            if clean(item.tag) == "property":
                if item.attrib['name'] not in exclude_attrib :
                    if item.attrib['name'] not in property_categories: property_categories.append(item.attrib['name'])
                
# parse output list
rules = {}

for entry in root:
    if clean(entry.tag) == "entry":
        empty_filters = EmptyFilterDict(property_categories)
        label = ''
        for item in entry:
            if clean(item.tag) == "property":
                if item.attrib['name'] == 'label':
                    label = item.attrib['value']
                elif item.attrib['name'] not in exclude_attrib:
                    empty_filters[item.attrib['name']] = item.attrib['value']
        # hash empty
        localhash = make_hash(empty_filters)
        # find if entry already exists in filters, add label
        if localhash in rules.keys():
            rules[localhash]['label'].append(label)
        else :
            rules[localhash] = {'filters':empty_filters,'label':[label]}

# prepare csv output
csv = ''

for category in property_categories:
    csv += category + ','
csv += 'label\n'

for rule in rules:
    for category in property_categories:
        csv += rules[rule]['filters'][category] + ','
    csv += ';'.join(sorted(rules[rule]['label'],reverse=False)) + '\n'
    
print csv