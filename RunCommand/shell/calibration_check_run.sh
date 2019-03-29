#!/bin/sh
# -*- coding: utf-8 -*-
# 
# Copyright 2012-2015 Frédéric Magniette, Miguel Rubio-Roy
# This file is part of Calicoes.

. /opt/pyrame/ports.sh

overwrite=remove
step=0
mode=0

run_time=120
overwrite=remove

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

$WAGASCI_RUNCOMMANDDIR/python/calibration_check_run.py $1 ${run_time} ${overwrite} ${mode}
if [ $? -eq 1 ]; then
  exit 1
fi

calibdir="${WAGASCI_XMLDATADIR}/${1}/check"
$WAGASCI_MAINDIR/bin/wgCalib -f ${calibdir} -m ${mode}
