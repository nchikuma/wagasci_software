#!/usr/bin/sh

#LOG="/usr/local/src/wagasci_software/log/dellstatus_log.txt"
LOG="/usr/local/src/wagasci_software/log/slowmonitor.log"
ALARM_LOG="/usr/local/src/wagasci_software/log/alarm_log.txt"
UPDATETIMING=01 #hour by 24

while :
do
  DATE=`date`
  if [ `date +%H` -eq ${UPDATETIMING} ]; then
    UNIXTIME=`date +%s`
    ./CheckPdisk.sh | grep -v "Power Status" | grep "Status" | while read line 
    do
      if [ "${line}"=="Status : Ok" ]; then
        echo "[${DATE}][run_HDDcheck.sh][INFO] All HDDs status is OK." >> $LOG
      else
        sed -i "1s/^/${UNIXTIME}\/HDD Status\\n/" ${ALARM_LOG}
        echo "[${DATE}][run_HDDcheck.sh][ERROR] HDD Status is not good. Check the Dell Status log file." >> $LOG
      fi
    done
  else
    echo "[${DATE}][run_HDDcheck.sh][INFO] Nothing has been done." >> $LOG
  fi

  sleep 1000

done
