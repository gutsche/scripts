#!/usr/bin/env python3

import sys,os,argparse
import pytz
import datetime
from statistics import mean
import psycopg2
import requests

#global variables
verbose =  0
central_timezone = pytz.timezone('US/Central')
utc_timezone = pytz.timezone('UTC')
day_delta = datetime.timedelta(days=1)

def calculate_comed_cost(utc_start,utc_end,kwh):
    """

    query comed and caluclate cost for kwh

    """

    if kwh == 0.:
        if verbose >= 1:
            print("Input kwh is 0.0, returning zero cost")
        return 0.0

    if verbose >= 3:
        print('Retrieving hourly pricing information from comed for {0} to {1}'.format(utc_start.strftime('%Y%m%d%H%M'),utc_end.strftime('%Y%m%d%H%M')))
    url = 'https://hourlypricing.comed.com/api?type=5minutefeed&datestart={0}&dateend={1}'.format(utc_start.strftime('%Y%m%d%H%M'),utc_end.strftime('%Y%m%d%H%M'))
    comed_info = requests.get(url=url).json()
    pricing = {}
    for entry in comed_info:
        sec = int(int(entry['millisUTC'])/1000)
        time = utc_timezone.localize(datetime.datetime.fromtimestamp(sec))
        pricing[time] = float(entry['price'])
    if verbose >= 3:
        print('Retrieved prices for {0} 5-min intervals from comed'.format(len(pricing.keys())))

    # average prices
    if len(pricing.keys()) == 0:
        if verbose >= 1:
            print("ComEd didn't return any pricing for interval from {0} CST to {1} CST, returning average of 2 cent per kWh".format(utc_start.astimezone(central_timezone),utc_end.astimezone(central_timezone)))
        average_kwh_price = 0.02
    else:
        average_kwh_price = mean(pricing.values())/100.
    if verbose >= 3:
        print("average_kwh_price: {0:.4f}".format(average_kwh_price))

    # input parameter for cost calculation
    Average_Consumption_Per_Month = 600 #[kWh]
    Capcity_Obligation = 1.41 #[kWh]
    Electricity_Supply_Charge =  11.79 #[$$]
    Transmission_Service_Charge =  0.00786 #[$$/kWh]
    Capacity_Charge =  5.90209 #[$$/kWh]
    Purchased_Electricity_Adjustment =  -2.83000 #[$$]
    Misc_Procurement_Component_Chg =  0.00091 #[$$/kWh]
    Customer_charge =  11.30000 #[$$]
    Standard_Metering_Charge = 4.52000 #[$$]
    Distribution_Facilities_Charge =  0.03541 #[$$/kWh]
    IL_Electricity_Distribiution_Charge =  0.00120 #[$$/kWh]
    Environmental_Cost_Recovery_Adj =  0.00039 #[$$/kWh]
    Renewable_Portfolio_Standard =  0.00189 #[$$/kWh]
    Zero_Emission_Standard =  0.00190 #[$$/kWh]
    Energy_Efficiency_Programs =  0.00132 #[$$/kWh]
    Energy_Efficiency_Adjustment = 0 #[$$/kWh]
    Peak_Time_Savings = 0 #[$$]
    Franchise_Cost =  0.99000 #[$$]
    State_Tax =  1.87000 #[$$]
    Municipal_Tax = 3.55000 #[$$]

    # calculate cost for consumed
    cost = average_kwh_price * kwh
    cost += Electricity_Supply_Charge / Average_Consumption_Per_Month
    cost += Transmission_Service_Charge * kwh
    cost += Capacity_Charge * Capcity_Obligation / Average_Consumption_Per_Month
    cost += Purchased_Electricity_Adjustment / Average_Consumption_Per_Month
    cost += Misc_Procurement_Component_Chg * kwh

    cost += Customer_charge / Average_Consumption_Per_Month
    cost += Standard_Metering_Charge / Average_Consumption_Per_Month
    cost += Distribution_Facilities_Charge * kwh
    cost += IL_Electricity_Distribiution_Charge * kwh

    cost += Environmental_Cost_Recovery_Adj * kwh
    cost += Renewable_Portfolio_Standard * kwh
    cost += Zero_Emission_Standard * kwh
    cost += Energy_Efficiency_Programs * kwh
    cost += Energy_Efficiency_Adjustment * kwh
    cost += Peak_Time_Savings / Average_Consumption_Per_Month
    cost += Franchise_Cost / Average_Consumption_Per_Month
    cost += State_Tax / Average_Consumption_Per_Month
    cost += Municipal_Tax / Average_Consumption_Per_Month

    if verbose >= 3:
        print("Cost for {0:.2f} kWh from {1} CST to {2} CST: {3:.2f}".format(kwh,utc_start.astimezone(central_timezone),utc_end.astimezone(central_timezone),cost))

    return cost


def main(args):
    """

    update teslamate postgres to calculate cost of charges using ComEd hourly prices

    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", "-v", action="count", help="Increase the verbosity level by increasing -v, -vv, -vvv", default=0)
    parser.add_argument("--password", action="store", type=str, required=True, help="Password for teslamate database")

    args = parser.parse_args()
    global verbose
    verbose = args.verbose
    password = args.password

    # sql for updating database
    sql = """UPDATE charging_processes SET cost = %s WHERE id = %s"""


    # connect to postgres database
    connection = psycopg2.connect("dbname='teslamate' user='teslamate' host='localhost' password='{0}' port='5632'".format(password))
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM charging_processes ORDER BY id DESC")
    rows = cursor.fetchall()

    #  query the last X entries
    num_query_entries = 3

    for row in rows[:num_query_entries]:
        id = row[0]
        starttime = utc_timezone.localize(row[1])
        endtime = utc_timezone.localize(row[2])
        kwh = row[16]
        cost = row[17]
        if cost == None:
            cost = 0.0
        comed_cost = calculate_comed_cost(starttime,endtime,kwh)
        print("kWh: {0:.2f} cost: {1:.2f} comed: {2:.2f}".format(kwh,cost,comed_cost))

        # update database
        sql = "UPDATE charging_processes SET cost = {0} WHERE id = {1}".format(str(comed_cost),str(id))
        try:
            cursor.execute(sql)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    try:
        connection.commit()
        cursor.close()
        connection.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

if __name__ == '__main__':
    main(sys.argv)
