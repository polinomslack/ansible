#!/usr/bin/env python

import ipaddress
import sys
import codecs

with open(sys.argv[1],'r') as f:
    for line in f:
        if '/' in line:
            for addr in ipaddress.IPv4Network(line.decode('utf8').rstrip()):
                print(addr)
        else:
            print(line.rstrip())
