#!/bin/sh

proces="/usr/local/src/wagasci_software/slowMonitor/systemManager/gui_systemManager.py"
res=`ps ux | grep ${proces} | grep -v grep | wc -l`
if [ $res -eq 0 ];then
  echo "WAGASCI Monitor Manager starts."
  ${proces} &
else
  echo "WAGASCI Monitor Manager has alaready been running."
fi
