#!/usr/bin/sh

if [ "$1" = "status_check" ]; then
  if [ "$2" = "0" ]; then
    result="STATE:0 DEBUG mode"
    #result="STATE:4 Continuous mode"
    #result="STATE:5 ERROR mode"
    echo -n $result
  elif [ "$2" = "1" ]; then
    result="SPILL period: debug [ms]"
    echo -n $result
    result="SPILL active: debug [us]"
    echo -n $result
  fi
elif [ "$1" = "set_trigmode" ]; then
  result="DEBUG: cmd $1 $2 is sent"
  echo -n $result
elif [ "$1" = "set_bunchinfo" ]; then
  result="DEBUG: cmd $1 $2 $3 is sent"
  echo -n $result
elif [ "$1" = "set_spilinfo" ]; then
  result="DEBUG: cmd $1 $2 $3 is sent"
  echo -n $result
fi
sleep 3
echo -n " ... DEBUG: done ..."
