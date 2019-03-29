#!/bin/sh
# -*- coding: utf-8 -*-
# 

. /opt/pyrame/ports.sh

txtfile=$1
declare -i value=$2

echo ${txtfile:?"txtfile=NULL. Need a first argument of the configure txt file."}
echo ${value:?"txtfile=NULL. Need a third argument of value(0-1023)."}

python $WAGASCI_SEMIOFFDIR/RunCommand/python/change_txt.py -f ${txtfile} -c edit -s 931 -v ${value} -r
