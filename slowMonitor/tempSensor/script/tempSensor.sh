#!/usr/bin/sh

PROGRAM=usbrh
LOG="/usr/local/src/wagasci_software/slowMonitor/log/temperature.log"
TIME_UPDATE=10

if [ `which "$PROGRAM"` ]; then
  if [ "$2" == "loop" ]; then
    while :
    do
      VAR1=`echo -n "["`
      VAR2=`date "+%Y/%m/%d %H:%M:%S|unixtime=%s" | tr -d "\n"`
      VAR3=`echo -n "]"`                   
      VAR4=`$PROGRAM -f1 -1 | tr -d "\n"`
      VAR5=`echo -n "|"`                  
      VAR6=`$PROGRAM -f2 -1 | cat`
      echo "${VAR1}${VAR2}${VAR3}${VAR4}${VAR5}${VAR6}"
      sleep $TIME_UPDATE
    done
  else
    VAR1=`echo -n "["`
    VAR2=`date "+%Y/%m/%d %H:%M:%S|unixtime=%s" | tr -d "\n"`
    VAR3=`echo -n "]"`                   
    VAR4=`$PROGRAM -f1 -1 | tr -d "\n"`
    VAR5=`echo -n "|"`                  
    VAR6=`$PROGRAM -f2 -1 | cat`
    echo "${VAR1}${VAR2}${VAR3}${VAR4}${VAR5}${VAR6}"
  fi
else
  echo "There is no exectable program of $PROGRAM"
fi
