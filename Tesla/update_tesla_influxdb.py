#!/usr/bin/env python3

import sys,os
from influxdb import InfluxDBClient
from datetime import datetime,timedelta
import requests
from statistics import mean

display_name = "Oli's Tesla"
vin = "<VIN>"

debug = 2

days_to_parse = 5
start = datetime.utcnow() - timedelta(days=days_to_parse)
end = datetime.utcnow()
startepoch = int(start.strftime('%s'))*1000000000
startstring = start.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
endstring = end.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
print("{0}: Querying InfluxDb for the last {1} days, starting at {2} in UTC, which corresponds to the following string: {3}".format(endstring,days_to_parse,startepoch,startstring))

# get comed hourly pricing
if debug >= 3:
    print('Retrieving hourly pricing information from comed for {0} to {1}'.format(start.strftime('%Y%m%d%H%M'),end.strftime('%Y%m%d%H%M')))
url = 'https://hourlypricing.comed.com/api?type=5minutefeed&datestart={0}&dateend={1}'.format(start.strftime('%Y%m%d%H%M'),end.strftime('%Y%m%d%H%M'))
comed_info = requests.get(url=url).json()
pricing = {}
for entry in comed_info:
    sec = int(int(entry['millisUTC'])/1000)
    time = datetime.fromtimestamp(sec)
    pricing[time] = float(entry['price'])
if debug >= 3:
    print('Retrieved prices for {0} 5-min intervals from comed'.format(len(pricing.keys())))

# input parameter for cost calculation
Average_Consumption_Per_Month = 600 #[kWh]
Capcity_Obligation = 2.625 #[kWh]
Electricity_Supply_Charge =  11.79 #[$$]
Transmission_Service_Charge =  0.01256 #[$$/kWh]
Capacity_Charge =  5.90092 #[$$/kWh]
Purchased_Electricity_Adjustment =  -1.14000 #[$$]
Misc_Procurement_Component_Chg =  0.00096 #[$$/kWh]
Customer_charge =  11.30000 #[$$]
Standard_Metering_Charge = 5.15000 #[$$]
Distribution_Facilities_Charge =  0.03537 #[$$/kWh]
IL_Electricity_Distribiution_Charge =  0.00122 #[$$/kWh]
Environmental_Cost_Recovery_Adj =  0.00039 #[$$/kWh]
Renewable_Portfolio_Standard =  0.00189 #[$$/kWh]
Zero_Emission_Standard =  0.00190 #[$$/kWh]
Energy_Efficiency_Programs =  0.00132 #[$$/kWh]
Energy_Efficiency_Adjustment = 0 #[$$/kWh]
Peak_Time_Savings = 0 #[$$]
Franchise_Cost =  0.98000 #[$$]
State_Tax =  1.81000 #[$$]
Municipal_Tax = 3.45000 #[$$]

# connect influxdb
client = InfluxDBClient(host='localhost', port=8086, username='tesla',
        password='<passwd>')
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
    if debug >= 4:
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

            if debug >= 3:
                print('Charging interval calculation start: start: {0}, end: {1}, length: {2:16s} seconds'.format(start_charging.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),point_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), str(length)))

            ## calculate average price for interval
            prices = []
            for time in pricing.keys():
                if start_charging <= time and time <= point_time:
                    prices.append(pricing[time])
                    if debug >= 3:
                        print("start_charging: {0}, time: {1}, point_time: {2}".format(start_charging.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),point_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')))
            if len(prices) == 0:
                print('No pricing information found for time interval start_charging: {0}, point_time: {1}, setting to $0.02/kWh'.format(start_charging.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),point_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')))
                average_kwh_price = 0.02
            else:
                if debug >= 3:
                    print("prices: {0}, average: {1}".format(prices,mean(prices)))
                average_kwh_price = mean(prices) / 100.

            # calculate cost for charge_energy_added
            charged_costs = average_kwh_price * charge_energy_added
            charged_costs += Electricity_Supply_Charge / Average_Consumption_Per_Month
            charged_costs += Transmission_Service_Charge * charge_energy_added
            charged_costs += Capacity_Charge * Capcity_Obligation / Average_Consumption_Per_Month
            charged_costs += Purchased_Electricity_Adjustment / Average_Consumption_Per_Month
            charged_costs += Misc_Procurement_Component_Chg * charge_energy_added

            charged_costs += Customer_charge / Average_Consumption_Per_Month
            charged_costs += Standard_Metering_Charge / Average_Consumption_Per_Month
            charged_costs += Distribution_Facilities_Charge * charge_energy_added
            charged_costs += IL_Electricity_Distribiution_Charge * charge_energy_added

            charged_costs += Environmental_Cost_Recovery_Adj * charge_energy_added
            charged_costs += Renewable_Portfolio_Standard * charge_energy_added
            charged_costs += Zero_Emission_Standard * charge_energy_added
            charged_costs += Energy_Efficiency_Programs * charge_energy_added
            charged_costs += Energy_Efficiency_Adjustment * charge_energy_added
            charged_costs += Peak_Time_Savings / Average_Consumption_Per_Month
            charged_costs += Franchise_Cost / Average_Consumption_Per_Month
            charged_costs += State_Tax / Average_Consumption_Per_Month
            charged_costs += Municipal_Tax / Average_Consumption_Per_Month

            # calculate cost for consumed
            consumed_costs = average_kwh_price * consumed
            consumed_costs += Electricity_Supply_Charge / Average_Consumption_Per_Month
            consumed_costs += Transmission_Service_Charge * consumed
            consumed_costs += Capacity_Charge * Capcity_Obligation / Average_Consumption_Per_Month
            consumed_costs += Purchased_Electricity_Adjustment / Average_Consumption_Per_Month
            consumed_costs += Misc_Procurement_Component_Chg * consumed

            consumed_costs += Customer_charge / Average_Consumption_Per_Month
            consumed_costs += Standard_Metering_Charge / Average_Consumption_Per_Month
            consumed_costs += Distribution_Facilities_Charge * consumed
            consumed_costs += IL_Electricity_Distribiution_Charge * consumed

            consumed_costs += Environmental_Cost_Recovery_Adj * consumed
            consumed_costs += Renewable_Portfolio_Standard * consumed
            consumed_costs += Zero_Emission_Standard * consumed
            consumed_costs += Energy_Efficiency_Programs * consumed
            consumed_costs += Energy_Efficiency_Adjustment * consumed
            consumed_costs += Peak_Time_Savings / Average_Consumption_Per_Month
            consumed_costs += Franchise_Cost / Average_Consumption_Per_Month
            consumed_costs += State_Tax / Average_Consumption_Per_Month
            consumed_costs += Municipal_Tax / Average_Consumption_Per_Month

            if debug >= 3:
                print("charged_costs: ${0:.2f}, consumed_costs: ${1:.2f}".format(charged_costs,consumed_costs))

            print('Charging interval final result: start: {0}, end: {1}, length: {2:16s} seconds, charged {3:5.2f} kWh, average voltage: {4:6.2f}, average current: {5:6.2f}, consumed: {6:6.2f}, charged_costs: ${7:.2f}, consumed_costs: ${8:.2f}'.format(start_charging.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),point_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ'), str(length),charge_energy_added,charger_voltage/counter,charger_actual_current/counter,consumed,charged_costs,consumed_costs))

            charging_events.append({"start":start_charging, "end": point_time, "length": length.total_seconds(), "charged": charge_energy_added, "consumed": consumed, "charged_costs": charged_costs, "consumed_costs": consumed_costs})
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
    tmp['fields'] = {"start": entry['start'].strftime('%Y-%m-%dT%H:%M:%SZ'), "end": entry['end'].strftime('%Y-%m-%dT%H:%M:%SZ'),"duration": entry['length'], "charged": entry['charged'], "consumed": entry['consumed'], "charged_costs": entry['charged_costs'], "consumed_costs": entry['consumed_costs']}
    input.append(tmp)

try:
    client.write_points(input)
except Exception as e:
    print(e)
