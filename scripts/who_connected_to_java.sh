#!/bin/bash
ports=$(netstat -tlnp | grep java | awk '{  split($4,a,":"); print a[2] }' | tr '\n' ' ')
for port in $ports
do
  echo "Port $port:"
  for sourceip in $(netstat -tan  | grep 'tcp ' | grep ":$port" | awk -F: '{ print $2 }' | grep -v '0.0.0.0' | awk '{ print $2}' | sort | uniq)
  do
      echo "$sourceip" $(host -t ptr $sourceip | awk '{print $NF}')
  done
done

