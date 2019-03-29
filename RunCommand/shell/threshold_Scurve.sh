#!/bin/sh
# -*- coding: utf-8 -*-
# 
# Copyright 2012-2015 Frédéric Magniette, Miguel Rubio-Roy
# This file is part of Calicoes.

. /opt/pyrame/ports.sh

ini_inputDAC=161
fin_inputDAC=200
step_inputDAC=40


ini_threshold=110
ini_threshold2=110
fin_threshold=122
step_threshold=2

overwrite=append
step=0

run_name="scurve" 
run_time=60 

if test $# -lt 1 ; then
  echo "too few argument!!"
  echo "need runname & time "
  exit 1
elif test $# -eq 1; then
  run_name=$1
elif test $# -eq 2; then
  run_name=$1
  run_time=$2
elif test $# -ge 3; then
  run_name=$1
  run_time=$2
  overwrite=$3
  echo "overwrite mode : ${overwrite}"
fi

inputDAC=${ini_inputDAC}
while [ ${inputDAC} -le ${fin_inputDAC} ]
do
  if [ ${inputDAC} -eq ${ini_inputDAC} ];then
    threshold=${ini_threshold2}
  else
    threshold=${ini_threshold}
  fi
  while [ ${threshold} -le ${fin_threshold} ]
    do
    echo "start run, inputDAC:${inputDAC}, threshold:${threshold}"

    step=`expr ${step} + 1`
    if [ ${step} -gt 8 ]; then
      echo "run 8 times. restart pyrame... "
      systemctl restart pyrame
      sleep 3
      step=0
    fi

    sleep 3
    $WAGASCI_RUNCOMMANDDIR/python/threshold_Scurve_run.py ${run_name} ${run_time} ${overwrite} ${inputDAC} ${threshold}
    if [ $? -eq 1 ]; then
      exit 1
    fi
    sleep 1
    threshold=`expr ${threshold} + ${step_threshold}`
  done #inputDAC 
  inputDAC=`expr ${inputDAC} + ${step_inputDAC}`
done #threshold
