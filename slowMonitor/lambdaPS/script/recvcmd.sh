#!/usr/bin/sh


source ./setRs232dev.sh

while :
do
  cat $DEVICE
  sleep 1
done
