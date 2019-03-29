#!/bin/sh
# -*- coding: utf-8 -*-
# 

runname="test"
runid=`ssh wagasci-daq cat /opt/calicoes/config/runid.txt`
runid=`expr ${runid} + 1`
content="1s/^/${runid} ${runname}\n/"
echo $content
sed -i "${content}" /home/data/runid/calib_id.txt
