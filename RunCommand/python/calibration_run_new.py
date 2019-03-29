#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# 
# Copyright 2012-2016 Frédéric Magniette, Miguel Rubio-Roy
# This file is part of Calicoes.
import os
import subprocess
import time

NCHIP=20
ANA_DIR=os.environ['WAGASCI_MAINDIR']
RUN_DIR=os.environ['WAGASCI_RUNCOMMANDDIR']
RAW_DIR=os.environ['WAGASCI_RAWDATADIR']
ROOT_DIR=os.environ['WAGASCI_DECODEDIR']
XML_DIR=os.environ['WAGASCI_XMLDATADIR']
CCC_DIR="%s/../slowMonitor/cccCtrl/script"%(ANA_DIR)
XMLCONFIG="/opt/calicoes/config/wagasci_config_40asu.xml"
THRESHOLD_CARD="/home/data/calibration/threshold_card.xml"

FAIL = '\033[41m'
WARNING = '\033[31m'
OKGREEN = '\033[42m'
OKBLUE = '\033[36m'
ENDC = '\033[0m'

range_dif=[1,2]
range_pe=[2]
range_inputDAC=[81,101,121,141,161]

def MakeLogo():
  print OKGREEN + " ......ooooooo0000000000OOOOOOOOOOOOOOOO0000000000ooooooo...... " +ENDC
  print OKGREEN + "                    start calibration run....       "  +ENDC 
  print OKGREEN + " ......ooooooo0000000000OOOOOOOOOOOOOOOO0000000000ooooooo...... " +ENDC
  sys.stdout.flush()

def calibration_run_new_init():
  declare_param("run_name","name of run","calib")
  declare_param("acq_time","duration of acquisition (s)","1200")
  declare_param("rewrite","rewrite : append or remove","append")
  declare_param("mode","0 or 1","0")
  
def calibration_run_new_run(run_name,acq_time,rewrite,mode):

  MakeLogo()
  runname_dir = "%s/%s"%(RAW_DIR,run_name)
  if not os.path.isdir(runname_dir):
    os.mkdir(runname_dir)

  runstopfile = "/opt/calicoes/config/run_stop.txt" 
  with open(runstopfile,"w") as f:
    f.write("0")

  for inputDAC in range_inputDAC:
    for pe in range_pe:
      print OKBLUE + " =================================================" +ENDC
      print "        " + OKBLUE + "        ===================================" +ENDC
      print "   run_name :%s, acq_time : %s, rewrite : %s"%(run_name, acq_time, rewrite)
      print "         inputDAC : %s,  pe : %s"%(inputDAC,pe)
      print "        " + OKBLUE + "        ===================================" +ENDC
      print OKBLUE + " =================================================" +ENDC
      sys.stdout.flush()

      #configure
      for dif in range_dif:
        for ichip in range(NCHIP): 
          TXTCONFIG="/opt/calicoes/config/spiroc2d/wagasci_config_dif%d_chip%d.txt"%(dif,ichip+1)
          cmd="%s/bin/wgChangeConfig -f %s -r -c -m 2 -b 36 -v %d"%(ANA_DIR,TXTCONFIG,int(inputDAC))
          subprocess.call( cmd , shell=True)

      cmd="%s/bin/wgOptimize -f %s -i %d -p %d"%(ANA_DIR,THRESHOLD_CARD,int(inputDAC),int(pe))
      subprocess.call( cmd , shell=True)

      cmd="%s/shell/reconfigure.sh %s"%(RUN_DIR,XMLCONFIG)
      ret=subprocess.call( cmd , shell=True)
      if ret !=0 :
        sys.exit(FAIL+'Error! While reconfigure!'+ENDC)
        time.sleep(0.1)
      
      #run 
      cmd="ssh wagasci-ana %s/spill_setinfo.sh p 260000"%(CCC_DIR)
      subprocess.call( cmd , shell=True)
      cmd="ssh wagasci-ana %s/spill_setinfo.sh a 5000"%(CCC_DIR)
      subprocess.call( cmd , shell=True)
      cmd="ssh wagasci-ana %s/spill_internal.sh"%(CCC_DIR)
      subprocess.call( cmd , shell=True)
      time.sleep(1)

      run_name0="%s_inputDAC%d_pe%d"%(run_name,int(inputDAC),int(pe))
      print OKBLUE +"RUN %s start ... "%(run_name0) + ENDC
      sys.stdout.flush()

      run=new_run(run_name0,rewrite)
      #acq=timed_acq(run_name0,run,float(acq_time))
      #wait_acq_finished(acq)
      acq=new_acq(run_name0,run,"append")
      start_acq(acq)
      for i in range(int(acq_time)):
        with open(runstopfile,"r") as f:
          if f.readline().strip()=="1":
            stop_acq()
            return
        time.sleep(1)
      stop_acq()

      time.sleep(5)

    #end dif loop
  #end inputDAC loop

  cmd = "mv %s/%s_* %s"%(RAW_DIR,run_name,runname_dir)
  subprocess.call(cmd,shell=True)

  print OKGREEN +"RUN %s finish! "%(run_name0) + ENDC 
  sys.stdout.flush()
  cmd="ssh wagasci-ana %s/spill_off.sh"%(CCC_DIR) #end all run
  subprocess.call( cmd , shell=True)
#end def

def calibration_run_new_get_progress():
    return progress_acq

execfile("/opt/calicoes/pycaldaq_rcs.py")
