#!/bin/sh
# -*- coding: utf-8 -*-
# 
# Copyright 2012-2015 Frédéric Magniette, Miguel Rubio-Roy
# This file is part of Calicoes.

. /opt/pyrame/ports.sh

ini_pe=2
fin_pe=2
step_pe=1

overwrite=append
step=0

pe=${ini_pe}
while [ ${pe} -le ${fin_pe} ]
  do
  echo "start run,  pe:${pe}"
  sleep 1
  run_time=`expr \( 30 + \( ${pe} - 1 \) \* 90 \) \* 60`
  echo $run_time
  $WAGASCI_RUNCOMMANDDIR/python/pedestal_check_run.py $1 ${run_time} ${overwrite} ${pe}
  if [ $? -eq 1 ]; then
    exit 1
  fi
  sleep 1
  pe=`expr ${pe} + ${step_pe}`
done #pe 

calibdir="${WAGASCI_XMLDATADIR}/${1}"
$WAGASCI_MAINDIR/bin/wgAnaPedestalSummary -f ${calibdir}
