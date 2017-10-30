#!/usr/bin/env python

from xml.etree import ElementTree as et

input_file_name = 'export_mini.xml'
verbose = False
tags = ['Record','Correlation','Workout','ActivitySummary']
common_tags = []
counter = int(0)

input_tree = et.parse(input_file_name)
input_root = input_tree.getroot()

## create output xml files
years = ['2014','2015','2016','2017']
categories = years
categories.append('None')
outputs = {}
for year in categories:
    outputs[year] = {}
    outputs[year]['file_name'] = 'output' + str(year) + '.xml'
    outputs[year]['root'] = et.Element(input_root.tag,input_root.attrib)
    outputs[year]['tree'] = et.ElementTree(outputs[year]['root'])
    outputs[year]['counter'] = {}
    for tag in tags:
        outputs[year]['counter'][tag] = int(0)
    outputs[year]['common_counter'] = int(0)

## iterate over input tree
print('Iterating over input xml\n')

for input_child in input_root:
    counter += 1
    if counter < 10: print('Child counter: %8i' % counter)
    elif counter < 100 and counter%10 == 0: print('Child counter: %8i' % counter)
    elif counter < 1000 and counter%100 == 0: print('Child counter: %8i' % counter)
    elif counter < 10000 and counter%1000 == 0: print('Child counter: %8i' % counter)
    elif counter%10000 == 0: print('Child counter: %8i' % counter)

    if verbose: print('Input child tag: %s' % input_child.tag)
    if input_child.tag in tags:
        if verbose: print('Checking year for input tag: %s' % input_child.tag)
        if 'creationDate' in input_child.attrib:
            year = input_child.attrib.get('creationDate')[0:4]
        elif 'dateComponents' in input_child.attrib:
            year = input_child.attrib.get('dateComponents')[0:4]
        else:
            print('ERROR: couldn\'t handle year extraction for input child tag: %s' % input_child.tag)
            break
        if verbose: print('Identified year for child input tag: %s as %s' % (input_child.tag,year))
        if year in years:
            outputs[year]['root'].append(input_child)
            outputs[year]['counter'][input_child.tag] += 1
        else:
            outputs['None']['root'].append(input_child)
            outputs['None']['counter'][input_child.tag] += 1
    else:
        if verbose: print('Copying input child tag: %s to all output xmls' % input_child.tag)
        if input_child.tag not in common_tags: common_tags.append(input_child.tag)
        for year in categories:
            outputs[year]['root'].append(input_child)
            outputs[year]['common_counter'] += 1

## write all output xmls
print('\nWrite all output xmls.')
for year in categories:
    print('Write %s' % outputs[year]['file_name'])
    outputs[year]['tree'].write(outputs[year]['file_name'], xml_declaration=True, encoding="utf-8")

print('\nStatistics')
print ('Input child counter: %i' % counter)
for category in categories:
    for tag in tags:
        print('Output child: year: %5s tag: %20s counter: %8i' % (category,tag,outputs[category]['counter'][tag]))
    print('Output child: year: %5s tag:               common counter: %8i' % (category,outputs[category]['common_counter']))

print('\nCross checks')
reference = None
referenceCheck = True
for category in categories:
    if reference == None: reference = outputs[category]['common_counter']
    if outputs[category]['common_counter'] != reference:
        referenceCheck = False
if referenceCheck:
    print('Common counter the same in all categories')
else:
    print ('Common counter NOT the same in all categories')
output_counter = reference
for category in categories:
    for tag in tags:
        output_counter += outputs[category]['counter'][tag]
if counter != output_counter:
    print('Input counter: %i and output counter: %i INCONSISTENT' % (counter,output_counter))
else:
    print('Input counter: %i and output counter: %i consistent' % (counter,output_counter))
