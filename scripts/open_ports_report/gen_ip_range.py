#!/usr/bin/env pyhton
import json
import urllib2
import base64
import sys
import traceback
import datetime


def make_query(url):
    request = urllib2.Request(url)
    base64string = base64.b64encode('%s:%s' % (username, password))
    request.add_header("Authorization", "Basic %s" % base64string)

    try:
        result = urllib2.urlopen(request)
    except:
        print("Something went wrong during HTTP request. Check stacktrace below: ")
        print '-' * 60
        traceback.print_exc(file=sys.stdout)
        print '-' * 60
        sys.exit(1)
    return result

if len(sys.argv) != 3:
    print("Usage: "+sys.argv[0]+" username password")
    print("Provide username and password to access Hetzner API")
    exit(1)
else:
    username=sys.argv[1]
    password=sys.argv[2]


data_subnets = json.load(make_query('https://robot-ws.your-server.de/subnet/'))

net_union = []

for item in data_subnets:
    for subitem in item.itervalues():
        if subitem['failover'] == False:
            net_union.append(subitem['server_ip'])
            if subitem['mask'] != 64:
                net_union.append(subitem['ip']+'/'+str(subitem['mask']))

data_servers = json.load(make_query('https://robot-ws.your-server.de/server/'))


for item in data_servers:
    for subitem in item.itervalues():
        if subitem['server_ip'] not in net_union:
            net_union.append(subitem['server_ip'])

date = datetime.datetime.today().strftime("%d-%m-%y_%X")
filename = "hetzner_networks"+date
file = open(filename,'w')
for item in net_union:
    file.write(item+'\n')
file.close()






