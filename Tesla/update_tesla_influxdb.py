#!/usr/bin/env python3

import sys,os
from influxdb import InfluxDBClient
from datetime import datetime,timedelta

display_name = "Oli's Tesla"
vin = "5YJ3E1EB9KF533435"

debug = 2

start = datetime.utcnow() - timedelta(days=30)
startepoch = int(start.strftime('%s'))*1000000000
startstring = start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
print("Querying InfluxDb for the last 30 days, starting at {0} in UTC, which corresponds to the following string: {1}".format(startepoch,startstring))

client = InfluxDBClient(host='localhost', port=8086, username='FILLME', password='FILLME')
client.switch_database('tesla')

results = client.query('select charge_energy_added,charging_state,charger_actual_current,charger_voltage,charger_phases from charge_state where time >= {}'.format(startepoch))

# charging interval
charging_interval = False
start_charging = None
counter = 0
charge_energy_added = 0.0
charger_actual_current = 0
charger_voltage = 0
charging_events = []

points = results.get_points()
for point in points:

    # parse input information
    try:
        point_time = datetime.strptime(point['time'],'%Y-%m-%dT%H:%M:%S.%fZ')
    except:
        point_time = datetime.strptime(point['time'],'%Y-%m-%dT%H:%M:%SZ')
    if point['charge_energy_added'] != None:
        point_charge_energy_added = float(point['charge_energy_added'])
    else:
        point_charge_energy_added = 0.0
    if point['charging_state'] != None:
        point_charging_state = str(point['charging_state'])
    else:
        point_charging_state = ''
    if point['charger_actual_current'] != None:
        point_charger_actual_current = int(point['charger_actual_current'])
    else:
        point_charger_actual_current = 0
    if point['charger_voltage'] != None:
        point_charger_voltage = int(point['charger_voltage'])
    else:
        point_point_charger_voltage = 0
    if point['charger_phases'] != None:
        point_charger_phases = int(point['charger_phases'])
    else:
        point_point_charger_phases = 0

    # debug printout
    if debug >= 3:
        print('time: {0:23s}, charge_energy_added: {1:5.2f}, charging_state: {2:15s}, charger_actual_current: {3:4d}, charger_voltage: {4:4d}, charger_phases: {5:4d},'.format(point_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),point_charge_energy_added,point_charging_state,point_charger_actual_current,point_charger_voltage,point_point_charger_phases))

    # start charging interval
    if point_charging_state == 'Charging':
        # shouldn't be in active charging charging_interval
        if charging_interval == False:
            # start charging interval
            charging_interval = True
            start_charging = point_time
            charge_energy_added = point_charge_energy_added
            # don't count first entry for voltage and current
            counter = 0
            charger_actual_current = 0
            charger_voltage = 0

    # inside charging interval
    if charging_interval == True:
        if point_charge_energy_added > 0.: charge_energy_added = point_charge_energy_added
        if point_charging_state == 'Complete' or point_charger_voltage == 0 and point_charger_actual_current == 0:
            charging_interval = False
            length = point_time - start_charging
            consumed = charger_voltage/counter*charger_actual_current/counter/1000./3600.*length.total_seconds()
            print('Charging interval: {0:16s} seconds, charged {1:5.2f} kWh, average voltage: {2:6.2f}, average current: {3:6.2f}, consumed: {4:6.2f}'.format(str(length),charge_energy_added,charger_voltage/counter,charger_actual_current/counter,consumed))
            charging_events.append({"start":start_charging, "end": point_time, "length": length.total_seconds(), "charged": charge_energy_added, "consumed": consumed})
        else :
            # last measurement for charge interval ('Complete') does not have voltage and current
            counter += 1
            charger_actual_current += point_charger_actual_current
            charger_voltage += point_charger_voltage

# prepare object to write into InfluxDb
input = []
for entry in charging_events:
    tmp = {}
    tmp['measurement'] = "charging_events"
    tmp['tags'] = {"display_name": display_name, "vin": str(vin)}
    tmp['time'] = entry['end'].strftime('%Y-%m-%dT%H:%M:%SZ')
    tmp['fields'] = {"start": entry['start'].strftime('%Y-%m-%dT%H:%M:%SZ'), "end": entry['end'].strftime('%Y-%m-%dT%H:%M:%SZ'),"duration": entry['length'], "charged": entry['charged'], "consumed": entry['consumed']}
    input.append(tmp)

try:
    client.write_points(input)
except Exception as e:
    print(e)
