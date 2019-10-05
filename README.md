# Arris CM8200 to InfluxDB

This is a python script to webscrape the Arris CM8200 web interface and place data into Influxdb for graphing in Grafana.
![alt text](overview.png)

## Installation

```bash
sudo apt install python3 python3-pip python3-lxml
```
Use the pip package manager pip3 to install necessary requirements.

```bash
pip install -r requirements.txt
```

Setup influx with a database
```bash
$ influx
> CREATE DATABASE cm8200b_stats
```
Ensure that the database was created
```bash
> show databases
name: databases
name
----
cm8200b_stats <------
```

Adjust cm8200_stats.py to suite your requirements
```python
# Change settings below to your influxdb - database needs to be created or existing db
# creates 4 tables - downlink, uplink, fw_ver, uptime

influxip = "127.0.0.1"
influxport = "8086"
influxdb = "cm8200b_stats"
influxid = "admin"
influxpass = ""

# cm8200b URLs - leave these as is unless a firmware upgrade changes them

linestats = "http://192.168.0.1/cmconnectionstatus.html"
generalstats = "http://192.168.0.1/cmswinfo.html"
```

## Usage
### Running the webscraper

Standalone (once off)
```bash
/usr/bin/python3 /opt/arris_stats/cm8200b_stats.py
```

As cron
```bash
sudo crontab -e
```
Place the below into crontab. Ctrl + X to exit.
```bash
# m h  dom mon dow   command

*/5 * * * * /usr/bin/python3 /opt/arris_stats/cm8200b_stats.py
```

