#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

PIR_PIN = 26

def read_motion(name):
	print 'OLI',GPIO.input(PIR_PIN)
	return GPIO.input(PIR_PIN)

def metric_init(lparams):
    """Initialize metric descriptors"""

    # create descriptors
    descriptors = []

    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIR_PIN, GPIO.IN)

    descriptors.append({
        'name': "Motion",
        'call_back': read_motion,
        'time_max': 10,
        'value_type': 'uint',
        'units': 'Motion',
        'slope': 'both',
        'format': '%d',
        'description': "Motion from HC-SR501 sensor",
        'groups': 'Pi Sensors'
    })

    return descriptors

def metric_cleanup():
    """Cleanup"""
    GPIO.cleanup()
    pass

# the following code is for debugging and testing
if __name__ == '__main__':
    descriptors = metric_init({})
    for d in descriptors:
        print (('%s = %s') % (d['name'], d['format'])) % (d['call_back'](d['name']))
