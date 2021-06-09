#!/usr/bin/python
import datetime,time
l = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
curr_year = int(time.strftime("%Y").strip())

now = datetime.datetime.now()
now_minus_30 = now - datetime.timedelta(minutes = 15)

f = open('/var/log/messages','r')
for line in f:
    month = l.index(line.split()[0].lower())+1
    date = int(line.split()[1])
    time = line.split()[2]
    hr = int(time.split(':')[0])
    minu = int(time.split(':')[1])
    sec = int(time.split(':')[2])
    timestamp = datetime.datetime(curr_year,month,date,hr,minu,sec)
    if timestamp > now_minus_30:
        print line.strip()

