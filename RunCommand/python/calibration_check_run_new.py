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
range_pe=[2,3]

def calibration_check_run_new_init():
  declare_param("run_name","name of run","calib")
  declare_param("acq_time","duration of acquisition (s)","600")
  declare_param("rewrite","rewrite: append or remove","remove")
  
def calibration_check_run_new_run(run_name,acq_time,rewrite):
  print OKGREEN + " =================================================" +ENDC
  print OKGREEN + "        ===================================" +ENDC
  print OKGREEN + "               calibration check run " +ENDC
  print OKGREEN + "        ===================================" +ENDC
  print OKGREEN + " =================================================" +ENDC

  runname_dir = "%s/%s"%(RAW_DIR,run_name)
  if not os.path.isdir(runname_dir):
    os.mkdir(runname_dir)

  runstopfile = "/opt/calicoes/config/run_stop.txt" 
  with open(runstopfile,"w") as f:
    f.write("0")
  script_end = False

  for pe in range_pe:
    if script_end:
      print "calibration_run_new.py is stopped in the middle of run."
      sys.stdout.flush()
      return

    CALIB_CARD="/home/data/calibration/%s/calibration_card.xml"%(run_name)
    cmd="%s/bin/wgOptimize -m 1 -f %s -p %d"%(ANA_DIR,CALIB_CARD,int(pe))
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
    
    run_name0="%s_check_pe%d"%(run_name,int(pe))
    print OKBLUE +"RUN %s start ... "%(run_name0) + ENDC
   
    #run time
    if int(pe)==2:
      run_time=120
    else:
      run_time=600

    run=new_run(run_name0,rewrite)
    ##acq=timed_acq(run_name0,run,float(run_time))
    ##wait_acq_finished(acq)
    acq=new_acq(run_name0,run,"remove")
    start_acq(acq)
    for i in range(int(run_time)):
      with open(runstopfile,"r") as f:
        if f.readline().strip()=="1":
          script_end = True
          break
      time.sleep(1)
    stop_acq()
    time.sleep(5)
    if os.path.isdir("%s/%s"%(runname_dir,run_name0)):
      if os.path.isdir("%s/%s_bak"%(runname_dir,run_name0)):
        cmd = "rm -rf %s/%s_bak"%(runname_dir,run_name0)
        print cmd;
        subprocess.call(cmd,shell=True)
      cmd = "mv %s/%s %s/%s_bak"%(runname_dir,run_name0,runname_dir,run_name0)
      subprocess.call(cmd,shell=True)
              
    cmd = "mv %s/%s_* %s"%(RAW_DIR,run_name,runname_dir)
    subprocess.call(cmd,shell=True)
    print OKGREEN +"RUN %s finish... "%(run_name0) + ENDC

  print OKGREEN +"RUN %s_check finish! "%(run_name) + ENDC
  cmd="ssh wagasci-ana %s/spill_off.sh"%(CCC_DIR) #end all run
  subprocess.call( cmd , shell=True)
  

#end def

def calibration_check_run_new_get_progress():
    return progress_acq

execfile("/opt/calicoes/pycaldaq_rcs.py")
