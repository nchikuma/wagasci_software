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
CCC_DIR="%s/../cccCtrl/script"%(ANA_DIR)
XMLCONFIG="/opt/calicoes/config/wagasci_config_%dasu.xml"%(NCHIP)

FAIL = '\033[41m'
WARNING = '\033[31m'
OKGREEN = '\033[42m'
OKBLUE = '\033[36m'
ENDC = '\033[0m'
def test_run_init():
  declare_param("run_name","name of run","test")
  declare_param("acq_time","duration of acquisition (s)","180")
  declare_param("mode","rewrite mode: append or remove","append")
  
def test_run_run(run_name,acq_time,mode):
  cmd="%s/shell/reconfigure.sh %s"%(RUN_DIR,XMLCONFIG)
  subprocess.call( cmd , shell=True)
  time.sleep(0.1)

  #run
  run_name0="%s"%(run_name)
  raw_output="%s/%s/%s_dif_1_1_1.raw"%(RAW_DIR,run_name0,run_name0) 
  config_output="%s/%s/%s.xml"%(RAW_DIR,run_name0,run_name0) 
  tree_output="%s/%s_dif_1_1_1_tree.root"%(ROOT_DIR,run_name0) 
  hist_output="%s/%s_dif_1_1_1_hist.root"%(ROOT_DIR,run_name0) 
  xml_output="%s/%s_dif_1_1_1"%(XML_DIR,run_name0) 

  cmd="%s/spill_internal.sh"%(CCC_DIR)
  subprocess.call( cmd , shell=True)
  time.sleep(0.1)

  print OKBLUE +"RUN %s start ... "%(run_name0) + ENDC

  run=new_run(run_name0,mode)
  acq=new_acq(run_name0,run,mode)
  start_acq(acq)
  time.sleep(float(acq_time));
  stop_acq()
  time.sleep(1)
 
  cmd="%s/bin/Decoder -rf %s"%(ANA_DIR,raw_output)
  subprocess.call( cmd , shell=True)
  cmd="%s/bin/wgMakeHist -rf %s"%(ANA_DIR,tree_output)
  subprocess.call( cmd , shell=True)
  cmd="%s/bin/wgAnaHist -f %s -i %s -m 1 -p %d -r"%(ANA_DIR,hist_output,config_output,NCHIP)
  subprocess.call( cmd , shell=True)
  cmd="%s/bin/wgAnaHistSummary -rf %s"%(ANA_DIR,xml_output)
  subprocess.call( cmd , shell=True)
           
  print OKGREEN +"RUN %s finish! "%(run_name0) + ENDC 
  cmd="%s/spill_off.sh"%(CCC_DIR) #end all run
  subprocess.call( cmd , shell=True)
#end def

def test_run_get_progress():
    return progress_acq

execfile("/opt/calicoes/pycaldaq_rcs.py")
