#!/bin/sh

source $(cd $(dirname $0) && pwd)/ccc_setup.sh


RESULT=`$RBCPexe $READ $ADDR 16`
echo $RESULT
STATE=`echo $RESULT | cut -c 14-15`
STATEnum=`printf '%d\n' "0x"$STATE`
#echo $STATEnum
if [ $STATEnum -eq 0 ]; then
  printf "STATE:%d External spill mode\n" "${STATEnum}" 
elif [ $STATEnum -eq 1 ]; then
  printf "STATE:%d Internal spill mode\n" "${STATEnum}" 
elif [ $STATEnum -eq 2 ]; then
  printf "STATE:%d Single trigger mode\n" "${STATEnum}" 
elif [ $STATEnum -eq 3 ]; then
  printf "STATE:%d Continuous mode\n" "${STATEnum}" 
elif [ $STATEnum -eq 4 ]; then
  printf "STATE:%d Beam only mode\n" "${STATEnum}" 
elif [ $STATEnum -eq 5 ]; then
  printf "STATE:%d Pre-beam trigger mode\n" "${STATEnum}" 
elif [ $STATEnum -eq 6 ]; then
  printf "STATE:%d Spill OFF mode\n" "${STATEnum}" 
else
  echo "ERROR: Unknown state"
fi
