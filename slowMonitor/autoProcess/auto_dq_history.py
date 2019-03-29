#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math, glob
import threading

sys.path.append("{0}/".format(os.path.abspath(os.path.dirname(__file__))))
import AnaAll

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup


def process_loop_tmp():
  setup = Setup.Setup()
  while True:
    d = datetime.datetime.today()
    current_hour = d.strftime("%H")
    if current_hour=="03":
      cmd = "%s &>> %s"%(setup.PROCESS_DQHISTORY, setup.ANAHIST_LOG)
      subprocess.call(cmd,shell=True)
    time.sleep(1000)

def process_loop():
  setup = Setup.Setup()
  if not os.path.exists(setup.AUTO_RUNID_LIST):
    print "No auto procces runid list file: {0}".format(setup.AUTO_RUNID_LIST)
    return
    
  while True:

    # Read auto process runid list 
    runid_list = []
    acqid_list = []
    last_runid = -1
    last_acqidgroup = -1
    with open(setup.AUTO_RUNID_LIST,"r") as f:
      runid     = ""
      acqid     = ""
      state     = ""
      calibname = ""
      line = f.readline()
      while line:
        line = line.strip().split()
        if len(line)==4:
          runid     = line[0]
          acqid     = line[1]
          state     = line[2]
          calibname = line[3]
          if int(state)==11 or int(state)==12:
            if last_acqidgroup==-1 or (runid==last_runid and int(acqid)/9==last_acqidgroup):
              acqid_list.append(acqid)
            else:
              runid_list.append([last_runid,acqid_list,calibname])
              acqid_list = []
              acqid_list.append(acqid)
            last_acqidgroup = int(acqid)/9
            last_runid = runid
        line = f.readline()
      runid_list.append([last_runid,acqid_list,calibname])
    
    # Start merge files every 3 hours (9 files)
    threads = []
    for i in range(setup.MAX_PROCESS_THREAD): 
      threads.append(threading.Thread())
    
    i_run=0
    for runids in runid_list:
      runid     = runids[0]
      acqidlist = runids[1]
      calibname = runids[2]
      while True:
        throw_job = False
        for i in range(setup.MAX_PROCESS_THREAD):
          if not threads[i].isAlive():
            with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
              msg = "Analysis thread start. Run={%s %s}, Calib data = %s"%(runid,acqidlist,calibname)
              logger.logger.info(msg)
            threads[i] = threading.Thread(target=AnaAll.dq_all,args=(runid,acqidlist,"auto",))
            print "runid=",runid, " acqidlist=",acqidlist
            threads[i].start()
            throw_job = True
            break
        if throw_job: break
        else: time.sleep(10)
      #end while True
    #end for runids

    time.sleep(1200)

  #endi While True


if __name__ == '__main__':
  #process_loop()
  process_loop_tmp()
