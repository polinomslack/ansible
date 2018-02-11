#!/usr/bin/env python

import route53,sys

def fill_dns(ipaddr, hostname):
    if ndict.has_key(ipaddr) and hostname not in ndict[ipaddr]:
            ndict[ipaddr].append(hostname)
    else:
        ndict[ipaddr] = [hostname, ]
    return

conn = route53.connect(
    aws_access_key_id='key',
    aws_secret_access_key='access_key',
)

ndict = {}

for zone in conn.list_hosted_zones():
    for record_set in zone.record_sets:
        if record_set.rrset_type == 'A':
            for i in record_set.records:
                fill_dns(i, record_set.name)

print(ndict)

