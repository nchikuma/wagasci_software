#!/bin/sh

RESULT=`ping 192.168.10.17 -c 3 -w 3 | grep "packet loss" | cut -d , -f 3-3`
echo $RESULT
