#!/usr/bin/python3

import sys
from urllib.request import urlopen
from urllib.error import URLError
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
from datetime import datetime

# Change settings below to your influxdb - database needs to be created or existing db
# creates 4 tables - downlink, uplink, fw_ver, uptime

#influxip = "127.0.0.1"
#influxport = 8086
#influxdb = "cm8200b_stats"
#influxid = "admin"
#influxpass = ""

# cm8200b URLs - leave these as is unless a firmware upgrade changes them

linestats = "http://192.168.0.1/cmconnectionstatus.html"
generalstats = "http://192.168.0.1/cmswinfo.html"
logstats = "http://192.168.0.1/cmeventlog.html"

table_results = []

def main():

    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    # Make soup
    try:
        resp = urlopen(logstats)
    except URLError as e:
        print ('An error occured fetching %s \n %s' % (logstats, e.reason))   
        return 1
    soup = BeautifulSoup(resp.read(),"lxml")


# COLLECT DOWNSTREAMSTREAM DATA

    # Get table
    try:
        table = soup.find_all('table')[1] # Grab the first table
#        table = soup.find('table')
    except AttributeError as e:
        print ('No tables found, exiting')
        return 1

    # Get rows
    try:
        rows = table.find_all('tr')
    except AttributeError as e:
        print ('No table rows found, exiting')
        return 1

    # Get data
    n_rows=0
    #client = InfluxDBClient(influxip, influxport, influxid, influxpass, influxdb)

    for row in rows:

        table_data = row.find_all('td')
        if table_data:
            n_rows+=1
            if n_rows > 0:

               json_body = [
                   {
                       "measurement": "event_log",
		                   "time": current_time,
                       "fields": {
                           "modulation": table_data[1].text,
                           "frequency": table_data[2].text,
                           "power": table_data[3].text
                        },
                       "tags": {
                           "event_time": table_data[0].text
                       }
}
               ]
               print(json_body)
               #client.write_points(json_body)

if __name__ == '__main__':
    status = main()
    sys.exit(status)
