#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math
import threading


RAWDATADIR    = "/home/data/prototech/wagasci"
BACKUPSERV    = "wagasci-ana"
BACKUPDATADIR = "/home/data/daqdata/"
#RUNNBFILE     = "/opt/calicoes/config/runid.txt"
RUNNAME       = "run"
UPDATE_PERIOD = 600 #sec

while True:

  # get the current run nb
  with open(RUNNBFILE,"r") as f:
    runnb = int(f.read())
  print("The current RunNb is {0}".format(runnb))
  
  # look for current acq nb
  acqnb=0
  while True:
    isRawFile1 = os.path.isfile("%s/%s_%05d/%s_%05d_%03d_dif_1_1_1.raw"\
                              %(RAWDATADIR,RUNNAME,runnb,RUNNAME,runnb,acqnb))
    isRawFile2 = os.path.isfile("%s/%s_%05d/%s_%05d_%03d_dif_1_1_2.raw"\
                              %(RAWDATADIR,RUNNAME,runnb,RUNNAME,runnb,acqnb))
    if not (isRawFile1 or isRawFile2): break
    else: acqnb+=1

  # there is no .raw file
  if acqnb==0:
    d = datetime.datetime.today()
    timestr = d.strftime("%Y-%m-%d %H:%M:%S")
    print(timestr)
    print "There is no .raw file. It will be checked in 10min."
    pass

  else:
    acqnb -= 1
    print "current AcqNb = {0}".format(acqnb)
    rawfile1 = "%s/%s_%05d/%s_%05d_%03d_dif_1_1_1.raw"\
                                %(RAWDATADIR,runnb,runnb,acqnb)
    rawfile2 = "%s/%s_%05d/%s_%05d_%03d_dif_1_1_2.raw"\
                                %(RAWDATADIR,runnb,runnb,acqnb)
    isRawFile1 = os.path.isfile(rawfile1)
    isRawFile2 = os.path.isfile(rawfile2)
    if isRawFile1: size_last1 = os.path.getsize(rawfile1)
    if isRawFile2: size_last2 = os.path.getsize(rawfile2)
    
    # check if the raw file is being updated
    while True:
      time.sleep(10) #sec
      isUpdated = False
      if isRawFile1: 
        size_cur1 = os.path.getsize(rawfile1)
        if not size_cur1==size_last1: 
          isUpdated=True
          size_last1 = size_cur1
      if isRawFile2: 
        size_cur2 = os.path.getsize(rawfile2)
        if not size_cur2==size_last2: 
          isUpdated=True
          size_last2 = size_cur2
      if not isUpdated:
        cmd = "rsync -avuz {0} {1}:{2}".format(RAWDATADIR,BACKUPSERV,BACKUPDATADIR)
        d = datetime.datetime.today()
        timestr = d.strftime("%Y-%m-%d %H:%M:%S")
        print(timestr)
        print(cmd)
        subprocess.call(cmd,shell=True)
        print "DONE...."
        break
  time.sleep(UPDATE_PERIOD)
