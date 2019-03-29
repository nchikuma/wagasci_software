#!/bin/sh
# -*- coding: utf-8 -*-

#systemctl restart pyrame
#sleep 3

date
source /root/setting_wagasci.sh
if test $# -eq 0; then
  $WAGASCI_RUNCOMMANDDIR/python/reconfigure.py
  if [ $? -eq 0 ]; then
    exit 0
  else
    exit 1
  fi
else
  $WAGASCI_RUNCOMMANDDIR/python/reconfigure.py -f $1
  if [ $? -eq 0 ]; then
    exit 0
  else
    exit 1
  fi
fi

. /opt/pyrame/ports.sh
