#!/usr/bin/sh

source ./setRs232dev.sh

arg=($@)

cmd=$(for tmp in ${arg[@]}; do printf ":$tmp; "; done)

enquiry="05"
eot="04"
starttxt="02"
endtxt="03"

header="\x$enquiry\x$starttxt"
trailer="\x$endtxt\x$eot"

for cmd_i in ${cmd[@]}; do
  echo -n $cmd_i
  cmd_ascii=`./str2ascii.sh ${cmd_i}`
  cmd_tx="$header$cmd_ascii$spacer$trailer"
  echo $cmd_tx
  echo -e "$cmd_tx" >> $DEVICE
done

