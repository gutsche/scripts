#!/usr/bin/env python
# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import dht11
import time

def read_temperature(name):
    result = instance.read()
    while result.is_valid() == False:
        time.sleep(3)
        result = instance.read()
    if result.is_valid():
	return result.temperature
    
    return 999

def read_humidity(name):
    result = instance.read()
    while result.is_valid() == False:
        time.sleep(3)
        result = instance.read()
    if result.is_valid():
        return result.humidity

    return 999
    
def metric_init(lparams):
    """Initialize metric descriptors"""

    # create descriptors
    descriptors = []

    # initialize GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()

    # read data using pin 22
    global instance 
    instance = dht11.DHT11(pin=22)

    descriptors.append({
        'name': "Humidity",
        'call_back': read_humidity,
        'time_max': 60,
        'value_type': 'uint',
        'units': '%%',
        'slope': 'both',
        'format': '%d',
        'description': "Humidity from DHT11 Sensor",
        'groups': 'Pi Sensors'
    })

    descriptors.append({
        'name': "Temperature",
        'call_back': read_temperature,
        'time_max': 60,
        'value_type': 'uint',
        'units': 'Degree Celsius',
        'slope': 'both',
        'format': '%d',
        'description': "Temperature from DHT11 Sensor",
        'groups': 'Pi Sensors'
    })

    return descriptors

def metric_cleanup():
    """Cleanup"""
    pass

# the following code is for debugging and testing
if __name__ == '__main__':
    descriptors = metric_init({})
    for d in descriptors:
        print (('%s = %s') % (d['name'], d['format'])) % (d['call_back'](d['name']))
