#!/bin/bash
PATH=$PATH:/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
if [[ $# -ne 4 ]];then
  echo "usage: restore.sh [vmid] [ip] [netmask] [gateway]" >&2; exit 1
else
  vmid=$1
  ip=$2
  nm=$3
  gw=$4
fi

re='^[0-9]+$'
if ! [[ $vmid =~ $re ]] ; then
   echo "error: Not a number" >&2; exit 1
else
  newvmid=$((vmid + 200))
fi

function check_return {
  rc=$1
  lastrun=$2
  if [[ rc -ne 0 ]]; then
    echo "error: got error during executing \"$lastrun\"" >&2
    umount /mnt/build > /dev/null 2>&1
    umount /mnt/u137034 > /dev/null 2>&1
    exit 1
  else
    return 0
  fi
}

function changeip {
  ip=$1
  nm=$2
  gw=$3
  modprobe nbd
  qemu-nbd --connect=/dev/nbd0 /data/images/${newvmid}/vm-${newvmid}-disk-1.qcow2
  check_return $? $*
  pvscan --cache /dev/nbd0p5
  vgscan > /dev/null 2>&1
  lvscan > /dev/null 2>&1
  lvchange -a y /dev/debian8-changeme-vg/root
  check_return $? $*
  mount /dev/mapper/debian8--changeme--vg-root /mnt/build/
  check_return $? $*
  sed -i "s/address.*/address ${ip}/;s/netmask.*/netmask ${nm}/;s/gateway.*/gateway ${gw}/;" /mnt/build/etc/network/interfaces
  check_return $? $*
  sed -i "/^.*broadcast.*$/d;/^.*network.*$/d" /mnt/build/etc/network/interfaces
  check_return $? $*
  sed -i "s/^.*bitbucket\.prod\.win\.windeln-it\.de.*$/${ip} bitbucket.prod.win.windeln-it.de bitbucket/" /etc/hosts
  check_return $? $*
  umount /mnt/build/
  check_return $? $*
  lvchange -a n /dev/debian8-changeme-vg/root
  check_return $? $*
  qemu-nbd -d /dev/nbd0p5
  check_return $? $*
}

mountpoint -q /mnt/u137034
if [ $? -ne 0 ];then
  mount /mnt/u137034
else
  echo "error: /mnt/u137034 is already mounted" >&2; exit 1
fi
latest=$(find /mnt/u137034/proxmox-backups/dump/ -name "*${vmid}*" -ctime -1)
if ! [ -z $latest ]; then
 qm stop $newvmid
 sleep 5
 qmrestore ${latest} $newvmid -force && echo "restore succeeded"
 check_return $? $*
 echo -e "newip: $ip\nnewnm: $nm\nnewgw: $gw\nnewvmid: $newvmid\n"
fi
changeip $ip $nm $gw && qm start $newvmid
sleep 10
umount /mnt/u137034
