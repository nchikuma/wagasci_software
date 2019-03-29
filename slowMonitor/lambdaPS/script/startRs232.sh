#!/usr/bin/sh

source ./setRs232dev.sh

cmd="stty -F $DEVICE $BAUD_RATE ixon"
echo $cmd
$cmd
if [ $? -ne 0 ]; then
  echo "Error!!! Failed to initialize $DEVICE"
fi
