#!/usr/bin/env bash
/bin/ping -q -W 3 -c 1 10.0.3.252 || \
{ /sbin/ifdown tun0; /bin/sleep 2; /sbin/ifup tun0; }

