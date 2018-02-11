#!/usr/bin/env python

import sys,route53,re

def fill_dns_dict(ipaddr, hostname):
    if ndict.has_key(ipaddr) and hostname not in ndict[ipaddr]:
            ndict[ipaddr].append(hostname)
    else:
        ndict[ipaddr] = [hostname, ]
    return

def retreive_aws_data():
    global ndict
    ndict = {}
    conn = route53.connect(
        aws_access_key_id='key',
        aws_secret_access_key='access_key',
    )
    for zone in conn.list_hosted_zones():
        for record_set in zone.record_sets:
            if record_set.rrset_type == 'A':
                for i in record_set.records:
                    fill_dns_dict(i, record_set.name)
    return ndict

source=sys.argv[1]
report=sys.argv[2]

ndict = retreive_aws_data()

sfile = open(source,'r')
rfile = open(report,'w')

regex_line = re.compile("Host:.*Ports:.*")
#regex_host = re.compile("(?<=Host:\s).*(?=\sPorts:)")
regex_host = re.compile("(?<=Host:\s)(?:\d{,3}\.?){4}")
regex_ports = re.compile("(?<=Ports:\s)(?:\d{1,5}[\/a-z-]*(?:,\s)?)*")

date=sfile.readline()
date=date.split(" as:")[0]
sfile.seek(0)
head="""<html><head><title>NMAP SCAN RESULTS</title></head><body><h1 align="center">{date}</h1><br>
<style type="text/css">
table.nmap {{background-color:transparent;border-collapse:collapse;width:100%;}}
table.nmap th, table.example2 td {{text-align:center;border:1px solid black;padding:5px;}}
table.nmap th {{background-color:AntiqueWhite;}}
table.nmap td:first-child {{width:20%;}}
</style>
<table class="nmap"><tr><th>IP address</th><th>DNS names</th><th>Exposed ports</th></tr>
""".format(date=date)
tail="</table></body></html>"

rfile.write(head)

for line in sfile:
    if regex_line.match(line):
        host = regex_host.findall(line)[0]
        if ndict.has_key(host):
            domains = "<br>".join(ndict[host])
        else:
            domains = "<font color="red">Names were not found in DNS delegated to AWS Route53</font>"
        ports = regex_ports.findall(line)
        ports = re.findall("\d{1,5}(?=\/)",ports[0])
        row="<tr><th>"+host+"</th><th>"+domains+"</th><th>"+", ".join(ports)+"</th></tr>"
        rfile.write(row)

rfile.write(tail)
sfile.close()
rfile.close()
