#!/bin/sh
# -*- coding: utf-8 -*-
# 
# Copyright 2012-2015 Frédéric Magniette, Miguel Rubio-Roy
# This file is part of Calicoes.

. /opt/pyrame/ports.sh

ini_pe=1
fin_pe=2
step_pe=1

overwrite=remove
step=0
mode=0

DATESTR=`date +%Y%m%d`
run_name="calib_${DATESTR}"
i_run_name=2
if [ -e /home/data/prototech/${run_name} ];then
  while :
  do
    pre_run_name=${run_name}_${i_run_name}
    if [ ! -e /home/data/prototech/${pre_run_name} ];then
      run_name=${pre_run_name}
      break
    fi
    i_run_name=`expr ${i_run_name} + 1`
  done
fi
run_time=120

if test $# -eq 1 ; then
  run_name="${1}"
elif test $# -eq 2; then
  run_name="${1}"
  run_time=${2}
elif test $# -eq 3; then
  run_name="${1}"
  run_time=${2}
  overwrite=${3}
  echo "overwrite mode : ${overwrite}"
elif test $# -eq 4; then
  run_name="${1}"
  run_time=${2}
  overwrite=${3}
  mode=${4}
  echo "overwrite mode : ${overwrite}"
fi

if test ${mode} -eq 1 ; then
  run_time=1200
fi

echo "restart pyrame... "
  systemctl restart pyrame
sleep 1

$WAGASCI_RUNCOMMANDDIR/python/calibration_run.py ${run_name} ${run_time} ${overwrite} ${mode}
if [ $? -eq 1 ]; then
 exit 1
fi
sleep 1

calibdir="${WAGASCI_XMLDATADIR}/${run_name}"
$WAGASCI_MAINDIR/bin/wgPreCalib -f ${calibdir} -m ${mode}
sleep 3

$WAGASCI_RUNCOMMANDDIR/python/calibration_check_run.py ${run_name} ${run_time} ${overwrite} ${pe}
if [ $? -eq 1 ]; then
  exit 1
fi
sleep 1

calibdir="${WAGASCI_XMLDATADIR}/${run_name}/check"
$WAGASCI_MAINDIR/bin/wgCalib -f ${calibdir} -m ${mode}
