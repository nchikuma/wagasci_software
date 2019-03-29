#!/bin/sh

option=$1
echo ${option:?"Need an argument. {p,a}"}

source $(cd $(dirname $0) && pwd)/ccc_setup.sh


ADDRspill=256
echo "Information of the internal spill"
while :
do 

  case $option in
    "p")
      echo ""
      if [ "$2" = "" ]; then
        echo "-- Put an integer (>=8)."
        echo -n " >> Period [us] : "  
        read READDATA
      else
        READDATA=$2
      fi
      expr ${READDATA} + 1 > /dev/null 2>&1
      PERIODtemp=$?
      if [ $PERIODtemp -lt 2 ] && [ $READDATA -gt 7 ] ; then
        ADDRall=`echo "scale=0; ${ADDRspill}+0" | bc `
        READcount=`echo "scale=0; ${READDATA}/4" | bc `
        WRITEoption=$WRITELong
        break
      fi
      ;;
    "a")
      if [ "$2" = "" ]; then
        echo "-- Put an integer (>=4 and less than the peirod)."
        echo -n " >> Active time [us] : "  
        read READDATA
      else
        READDATA=$2
      fi
      expr ${READDATA} + 1 > /dev/null 2>&1
      ACTIVEtemp=$?
      if [ $ACTIVEtemp -lt 2 ] && [ $READDATA -gt 3 ] ; then
        ADDRall=`echo "scale=0; ${ADDRspill}+2" | bc `
        READcount=`echo "scale=0; ${READDATA}/4" | bc `
        WRITEoption=$WRITELong
        break
      fi
      ;;
    *)
      echo "Nothing has been done. Put an argument {p (period), a (active time)}."
      exit
      ;;
  esac

done


echo $ADDRall
echo $READcount

$RBCPexe $WRITEoption $ADDR $ADDRall $DATA $READcount
$RBCPexe $WRITEoption $ADDR $ADDRall $DATA $READcount
$RBCPexe $WRITEoption $ADDR $ADDRall $DATA $READcount
