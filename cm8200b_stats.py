#!/usr/bin/python3

import sys
from urllib.request import urlopen
from urllib.error import URLError
from argparse import ArgumentParser
from bs4 import BeautifulSoup
from influxdb import InfluxDBClient
from datetime import datetime

# Change settings below to your influxdb - database needs to be created or existing db
# creates 5 tables - downlink, uplink, fw_ver, uptime, event_log

influxip = "127.0.0.1"
influxport = "8086"
influxdb = "cm8200b_stats"
influxid = "admin"
influxpass = ""

# cm8200b URLs - leave these as is unless a firmware upgrade changes them

linestats = "http://192.168.0.1/cmconnectionstatus.html"
generalstats = "http://192.168.0.1/cmswinfo.html"
logstats = "http://192.168.0.1/cmeventlog.html"

table_results = []

def main():

    current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    client = InfluxDBClient(influxip, influxport, influxid, influxpass, influxdb)	
    # Make soup
    try:
        resp = urlopen(linestats)
    except URLError as e:
        print ('An error occured fetching %s \n %s' % (linestats, e.reason))   
        return 1
    soup = BeautifulSoup(resp.read(),"lxml")


# COLLECT DOWNSTREAMSTREAM DATA

    # Get table
    try:
        table = soup.find_all('table')[1] # Grab the first table
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
    for row in rows:

        table_data = row.find_all('td')
        if table_data:
            n_rows+=1
            if n_rows > 0:
               # Simple math to turn frequency into MHz
               dfreq = float(table_data[3].text.split(' ', 1)[0])
               dfreq = int(dfreq / 1000000)

               json_body = [
                   {
                       "measurement": "downstream_statistics",
		       "time": current_time,
                       "fields": {
                           "modulation": table_data[2].text,
                           "frequency": dfreq,
                           "power": float(table_data[4].text.split(' ', 1)[0]),
                           "snr": float(table_data[5].text.split(' ', 1)[0]),
                           "corrected": int(table_data[6].text),
                           "uncorrectables": int(table_data[7].text),
                           "status": table_data[1].text
                        },
                       "tags": {
                           "channel_id": table_data[0].text
                       }
}
               ]
               print(json_body)
               client.write_points(json_body)


# COLLECT UPSTREAM DATA

    # Get table
    try:
        table = soup.find_all('table')[2] # Grab the first table
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

    for row in rows:
        table_data = row.find_all('td')
        if table_data:
            n_rows+=1
            if n_rows > 0:
               # Simple math to turn frequency into MHz
               upfreq = float(table_data[4].text.split(' ', 1)[0])
               upfreq = upfreq / 1000000

               # Simple math to turn frequency into MHz
               chanwide = float(table_data[5].text.split(' ', 1)[0])
               chanwide = chanwide / 1000000

               json_body = [
                   {
                       "measurement": "upstream_statistics",
		       "time": current_time,
                       "fields": {
                           "channel_type": table_data[3].text,
			   "frequency": upfreq,
                           "power": float(table_data[6].text.split(' ', 1)[0]),
                           "width": float(chanwide),
                           "status": table_data[2].text
                        },
                       "tags": {
                           "channel_id": table_data[1].text
                       }
                    }
               ]
               print(json_body)
               client.write_points(json_body)

    try:
        resp = urlopen(generalstats)
    except URLError as e:
        print ('An error occured fetching %s \n %s' % (generalstats, e.reason))   
        return 1
    soup = BeautifulSoup(resp.read(),"lxml")


# COLLECT FIRMWARE DATA

    # Get table
    try:
        table = soup.find_all('table')[0] # Grab the first table
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

    for row in rows:
        table_data = row.find_all('td')
        if table_data:
            n_rows+=1
            if n_rows == 3:

                json_body = [
                    {
                        "measurement": "fw_ver",
                        "tags": {
                            "host": "cm8200b"
                        },
                        "fields": {
                            "firmware": table_data[1].text,
                         }
                     }
                ]
                print(json_body)
                client.write_points(json_body)


# COLLECT UPTIME DATA

    # Get table
    try:
        table = soup.find_all('table')[1] # Grab the first table
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

    for row in rows:
        table_data = row.find_all('td')
        if table_data:
            n_rows+=1
            if n_rows == 1:
                # drop all the minutes and other nonsense
                linetemp = table_data[1].text.split(' ', 1)[1]
                line = table_data[1].text.split(' ', 1)[0] + ' ' + linetemp.split(':', 1)[0]

                json_body = [
                    {
                        "measurement": "uptime",
                        "tags": {
                            "host": "cm8200b",
			    "up_time": table_data[0].text,
                        },
                        "fields": {
                           "uptime_d_h": line,
                           "uptime_full": table_data[1].text,
                         }
                     }
                ]
                print(json_body)
                client.write_points(json_body)

    # Make soup
    try:
        resp = urlopen(logstats)
    except URLError as e:
        print ('An error occured fetching %s \n %s' % (logstats, e.reason))   
        return 1
    soup = BeautifulSoup(resp.read(),"lxml")


# COLLECT EVENT_LOG DATA

    # Remove previous log information as its not required. This will also more or less simulate a reboot thus losing previous log files
    # It also aids in the selection of the logs ensuring none are skipped due to same time stamps etc..
    client.drop_measurement("event_log")

    # Get table
    try:
        table = soup.find_all('table')[0] # Grab the first table
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

    for row in rows:

        table_data = row.find_all('td')
        if table_data:
            n_rows+=1
            if n_rows > 0:

               json_body = [
                   {
                       "measurement": "event_log",
                       "fields": {
                           "time_d_t": table_data[0].text,
			   "id": table_data[1].text,
                           "level": table_data[2].text,
                           "desc": table_data[3].text
                       },
                       "tags": {
                           "tag_timestamp": table_data[0].text
                       }
}
               ]
               print(json_body)
               client.write_points(json_body)


if __name__ == '__main__':
    status = main()
    sys.exit(status)
