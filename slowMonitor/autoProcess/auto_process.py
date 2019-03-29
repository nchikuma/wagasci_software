#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math, glob
import threading

sys.path.append("{0}/".format(os.path.abspath(os.path.dirname(__file__))))
import AnaAll

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

def process_loop():
  setup = Setup.Setup()
  if not os.path.exists(setup.AUTO_RUNID_LIST):
    print "No auto procces runid list file: {0}".format(setup.AUTO_RUNID_LIST)
    return
    
  while True:
    # Read auto process runid list 
    runid_raw_list = []
    with open(setup.AUTO_RUNID_LIST,"r") as f:
      line = f.readline()
      while line:
        line = line.strip().split()
        if len(line)==4:
          runid_raw_list.append(line)
        line = f.readline()
    
    # Start analysis threads
    threads = []
    for i in range(setup.MAX_PROCESS_THREAD): 
      threads.append(threading.Thread())
    
    i_run=0
    for runid_raw in runid_raw_list:
      i_run=i_run+1 
      runid     = runid_raw[0]
      acqid     = runid_raw[1]
      state     = runid_raw[2]
      calibname = runid_raw[3]
      if int(state)>=1 and int(state)<11: #copy:1,decode:3,MakeHist:5,recon:7,dqcheck:9,delete:11
        while True:
          throw_job = False
          for i in range(setup.MAX_PROCESS_THREAD):
            if not threads[i].isAlive():
              with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
                msg = "Analysis thread start. Run={%s %s}, Calib data = %s"%(runid,acqid,calibname)
                logger.logger.info(msg)
              threads[i] = threading.Thread(target=AnaAll.analysis_all,args=(int(runid),int(acqid),"auto",))
              threads[i].start()
              throw_job = True
              break
          if throw_job: break
          else: time.sleep(10)
    time.sleep(600)
      
if __name__ == '__main__':
  process_loop()
