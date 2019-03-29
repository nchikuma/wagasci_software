#!/bin/sh
# -*- coding: utf-8 -*-
# 

. /opt/pyrame/ports.sh

txtfile=$1
declare -i ch=$2
declare -i value=`expr $3*512+$3*8+0`

echo ${txtfile:?"txtfile=NULL. Need a first argument of the configure txt file."}
echo ${ch:?"txtfile=NULL. Need a second argument of channel.(0-35,36:all)"}
echo ${value:?"txtfile=NULL. Need a third argument of value(0-255)."}

python $WAGASCI_SEMIOFFDIR/RunCommand/python/change_txt.py -f ${txtfile} -c edit -s 367 -b ${ch} -v ${value} -r
