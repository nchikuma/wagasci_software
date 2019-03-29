#!/bin/sh
# -*- coding: utf-8 -*-
# 
# Copyright 2012-2015 Frédéric Magniette, Miguel Rubio-Roy
# This file is part of Calicoes.

. /opt/pyrame/ports.sh

ini_inputDAC=1
fin_inputDAC=20
step_inputDAC=20

ini_threshold=144
fin_threshold=170
step_threshold=2

inputDAC=${ini_inputDAC}
while [ ${inputDAC} -le ${fin_inputDAC} ]
do
  threshold=${ini_threshold}
  while [ ${threshold} -le ${fin_threshold} ]
    do
    data=$1_inputDAC${inputDAC}_trigger${threshold}
    dir=$2
    echo "start run, inputDAC:${inputDAC}, threshold:${threshold}"
    $WAGASCI_RUNCOMMANDDIR/python/ana.py $data $dir
    sleep 1
    threshold=`expr ${threshold} + ${step_threshold}`
  done #inputDAC 
  inputDAC=`expr ${inputDAC} + ${step_inputDAC}`
done #threshold
