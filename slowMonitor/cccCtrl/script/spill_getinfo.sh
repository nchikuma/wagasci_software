#!/bin/sh

source $(cd $(dirname $0) && pwd)/ccc_setup.sh

RESULT1=`$RBCPexe $READLong $ADDR 4096`
echo $RESULT1
PERIOD1=`echo $RESULT1 | cut -c 14-15`
PERIOD2=`echo $RESULT1 | cut -c 30-31`
PERIOD=`printf '%d\n' "0x"$PERIOD1$PERIOD2`
PERIODtime=`echo "scale=0; ${PERIOD}*0.004" | bc `
printf 'SPILL period: %.0f [ms]\t(%d)\n' "$PERIODtime" "$PERIOD"

RESULT2=`$RBCPexe $READLong $ADDR 4098`
echo $RESULT2
ACTIVE1=`echo $RESULT2 | cut -c 14-15`
ACTIVE2=`echo $RESULT2 | cut -c 30-31`
ACTIVE=`printf '%d\n' "0x"$ACTIVE1$ACTIVE2`
ACTIVEtime=`echo "scale=0; ${ACTIVE}*4" | bc `
printf 'SPILL active: %.0f [us]\t(%d)\n' "$ACTIVEtime" "$ACTIVE"
