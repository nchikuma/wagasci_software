#!/bin/sh
# -*- coding: utf-8 -*-
# 
# Copyright 2012-2015 Frédéric Magniette, Miguel Rubio-Roy
# This file is part of Calicoes.

#QUESTION="Do you want to start calibration run? It will take about two hours." 
#while true; do
#  read -p "${QUESTION} [yes/no] : " yn
#  if [ "$yn" = "no" ]; then
#    echo "EXIT"
#    exit
#  elif [ "$yn" = "yes" ]; then
#    echo "START"
#    break;
#  fi
#done

. /opt/pyrame/ports.sh

ini_pe=1
fin_pe=2
step_pe=1

overwrite=remove
step=0
mode=0

DATESTR=`date +%Y%m%d`
run_name="calib_${DATESTR}"
checkrun_name=${run_name}_check_pe${pe}
i_run_name=2

RAWDATA_DIR_DAQ=/home/data/prototech
CALIBRATION_DIR=/home/data/calibration
ANA_DIR=/usr/local/src/wagasci_software/Analysis

if  ssh wagasci-daq test -e /home/data/prototech/${run_name}; then
  while :
  do
    pre_run_name=${run_name}_${i_run_name}
    if ! ssh wagasci-daq test -e /home/data/prototech/${pre_run_name};then
      run_name=${pre_run_name}
      checkrun_name=${run_name}_check_pe${pe}
      break
    fi
    i_run_name=`expr ${i_run_name} + 1`
  done
fi

run_time=120

### for DEBUG ###
#run_name="calib_20171014"
#checkrun_name=${run_name}_check_pe${pe}
#################

anamode=10
if test ${mode} -eq 1 ; then
  run_time=1200
  anamode=11
fi
echo "run_name : ${run_name}"
echo "run_time : ${run_time}"

echo "restart pyrame... "
ssh wagasci-daq systemctl restart pyrame
sleep 1

CALIB_DIR=${CALIBRATION_DIR}/${run_name}
CALIBDATA_DIR=${CALIBRATION_DIR}/${run_name}/data
CALIBXML_DIR=${CALIBRATION_DIR}/${run_name}/xml
CALIBIMG_DIR=${CALIBRATION_DIR}/${run_name}/image
CHECK_DIR=${CALIBRATION_DIR}/${run_name}/check
CHECKDATA_DIR=${CALIBRATION_DIR}/${run_name}/check/data
CHECKXML_DIR=${CALIBRATION_DIR}/${run_name}/check/xml
CHECKIMG_DIR=${CALIBRATION_DIR}/${run_name}/check/image
if ! test -e ${CALIB_DIR}; then
  mkdir ${CALIB_DIR}
fi
if ! test -e ${CALIBDATA_DIR}; then
  mkdir ${CALIBDATA_DIR}
fi
if ! test -e ${CALIBIMG_DIR}; then
  mkdir ${CALIBIMG_DIR}
fi
if ! test -e ${CALIBXML_DIR}; then
  mkdir ${CALIBXML_DIR}
fi
if ! test -e ${CHECK_DIR}; then
  mkdir ${CHECK_DIR}
fi 
if ! test -e ${CHECKDATA_DIR}; then
  mkdir ${CHECKDATA_DIR}
fi 
if ! test -e ${CHECKXML_DIR}; then
  mkdir ${CHECKXML_DIR}
fi 
if ! test -e ${CHECKIMG_DIR}; then
  mkdir ${CHECKIMG_DIR}
fi 

LOG=${CALIB_DIR}/calib_analysis.log
echo "" > ${LOG} #DEBUG


echo "====== Data taking is started. ======"
date
echo "Wait for 5 times of ${run_time} sec run"
ssh wagasci-daq $WAGASCI_RUNCOMMANDDIR/python/calibration_run_new.py ${run_name} ${run_time} ${overwrite} ${mode} &>> ${LOG}
if [ $? -eq 1 ]; then
 exit 1
fi
sleep 1

if test `ssh wagasci-daq cat /opt/calicoes/config/run_stop.txt` -eq 1; then 
  echo "Data taking is stopped in the middle" 
  exit 1
fi

echo "====== Acquired data are being copied. ======"
date
scp -r wagasci-daq:${RAWDATA_DIR_DAQ}/${run_name}/* ${CALIBDATA_DIR}/


echo "====== Analyses are started ======"
date

pe=2
for dif in `seq 1 2`; do
  for inputDac in `seq 81 20 161`; do
    echo "-----------------------------------------"
    echo "dif=${dif} inputDac=${inputDac} pe=${pe}"
    date

    run_name0=${run_name}_inputDAC${inputDac}_pe${pe}
    calibdir0=${CALIBDATA_DIR}/${run_name0}

    rawdata=${calibdir0}/${run_name0}_dif_1_1_${dif}.raw
    treedata=${calibdir0}/${run_name0}_dif_1_1_${dif}_tree.root
    histdata=${calibdir0}/${run_name0}_dif_1_1_${dif}_hist.root
    configxml=${calibdir0}/${run_name0}.xml
    chipxml=${CALIBXML_DIR}/${run_name0}_dif_1_1_${dif}

    echo "..Decoding.."
    echo "${ANA_DIR}/bin/Decoder -rf ${rawdata} -o ${calibdir0}"  >> ${LOG}
    ${ANA_DIR}/bin/Decoder -rf ${rawdata} -o ${calibdir0} &>> ${LOG}
    echo "..Making histograms.."
    echo "${ANA_DIR}/bin/wgMakeHist -rf ${treedata} -o ${calibdir0}" >> ${LOG}
    ${ANA_DIR}/bin/wgMakeHist -rf ${treedata} -o ${calibdir0} &>> ${LOG}
    echo "..Analyzing histograms.."
    echo "${ANA_DIR}/bin/wgAnaHist -rf ${histdata} -i ${configxml} -d ${dif} -m ${anamode} -o ${CALIBXML_DIR} -c ${CALIBIMG_DIR}" >> ${LOG}
    ${ANA_DIR}/bin/wgAnaHist -rf ${histdata} -i ${configxml} -d ${dif} -m ${anamode} -o ${CALIBXML_DIR} -c ${CALIBIMG_DIR} &>> ${LOG}
    echo "..Summarizing the analyses.."
    echo "${ANA_DIR}/bin/wgAnaHistSummary -rf ${chipxml} -m ${anamode} -i ${CALIBDATA_DIR}">> ${LOG}
    ${ANA_DIR}/bin/wgAnaHistSummary -rf ${chipxml} -m ${anamode} -i ${CALIBDATA_DIR} &>> ${LOG}
  done
done


echo "====== Analyses are completed. ======"
echo "====== Set the result as a current config ======"
date

${ANA_DIR}/bin/wgPreCalib -f ${CALIBXML_DIR} -m ${mode} -o ${CALIB_DIR} -i ${CALIBIMG_DIR} &>> ${LOG}
sleep 3
if ! ssh wagasci-daq test -d ${CALIB_DIR}; then
  ssh wagasci-daq mkdir ${CALIB_DIR}
fi
scp ${CALIB_DIR}/calibration_card.xml wagasci-daq:${CALIB_DIR}/

echo "====== Data taking for checking calibration result is started. ==="
date
echo "Wait for 10 min... "
ssh wagasci-daq $WAGASCI_RUNCOMMANDDIR/python/calibration_check_run_new.py ${run_name} ${run_time} ${overwrite} &>> ${LOG}
if [ $? -eq 1 ]; then
  exit 1
fi
sleep 1

if test `ssh wagasci-daq cat /opt/calicoes/config/run_stop.txt` -eq 1; then 
  echo "Data taking is stopped in the middle" 
  exit 1
fi

echo "====== Acquired data are being copied. ======"
date
scp -r wagasci-daq:${RAWDATA_DIR_DAQ}/${run_name}/${checkrun_name}* ${CHECKDATA_DIR}

echo "====== Analyses are started ======"
date

for pe in `seq 2 3`;do
  for dif in `seq 1 2`; do
    echo "-----------------------------------------"
    echo "dif=${dif} pe=${pe}"
    date

    run_name0=${run_name}_check_pe${pe}
    calibdir0=${CHECKDATA_DIR}/${run_name0}

    rawdata=${calibdir0}/${run_name0}_dif_1_1_${dif}.raw
    treedata=${calibdir0}/${run_name0}_dif_1_1_${dif}_tree.root
    histdata=${calibdir0}/${run_name0}_dif_1_1_${dif}_hist.root
    configxml=${calibdir0}/${run_name0}.xml
    chipxml=${CHECKXML_DIR}/${run_name0}_dif_1_1_${dif}

    echo "..Decoding.."
    echo "${ANA_DIR}/bin/Decoder -rf ${rawdata} -o ${calibdir0}"  >> ${LOG}
    ${ANA_DIR}/bin/Decoder -rf ${rawdata} -o ${calibdir0} &>> ${LOG}
    echo "..Making histograms.."
    echo "${ANA_DIR}/bin/wgMakeHist -rf ${treedata} -o ${calibdir0}" >> ${LOG}
    ${ANA_DIR}/bin/wgMakeHist -rf ${treedata} -o ${calibdir0} &>> ${LOG}
    echo "..Analyzing histograms.."
    echo "${ANA_DIR}/bin/wgAnaHist -rf ${histdata} -i ${configxml} -d ${dif} -m ${anamode} -o ${CHECKXML_DIR} -c ${CHECKIMG_DIR}" >> ${LOG}
    ${ANA_DIR}/bin/wgAnaHist -rf ${histdata} -i ${configxml} -d ${dif} -m ${anamode} -o ${CHECKXML_DIR} -c ${CHECKIMG_DIR} &>> ${LOG}
    echo "..Summarizing the analyses.."
    echo "${ANA_DIR}/bin/wgAnaHistSummary -rf ${chipxml} -m ${mode} -i ${CHECKDATA_DIR}">> ${LOG}
    ${ANA_DIR}/bin/wgAnaHistSummary -rf ${chipxml} -m ${anamode} -i ${CHECKDATA_DIR} &>> ${LOG}
  done
  echo "$WAGASCI_MAINDIR/bin/wgCalib -f ${CHECKXML_DIR} -m ${mode} -i ${CALIBIMG_DIR} -o ${CALIB_DIR}" >> ${LOG}
  $WAGASCI_MAINDIR/bin/wgCalib -f ${CHECKXML_DIR} -m ${mode} -i ${CALIBIMG_DIR} -o ${CALIB_DIR} -p ${pe}&>> ${LOG}
done



date
echo "====== DONE. ======"

runid=`ssh wagasci-daq cat /opt/calicoes/config/runid.txt`
runid=`expr ${runid} + 1`
content="1s/^/${runid} ${run_name}\n/"
sed -i "${content}" /home/data/runid/calib_id.txt
