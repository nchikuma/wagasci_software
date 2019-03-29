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

def calibration_check_run_init():
  declare_param("run_name","name of run","calib")
  declare_param("acq_time","duration of acquisition (s)","600")
  declare_param("rewrite","rewrite: append or remove","remove")
  declare_param("mode","0 or 1","0")
  
def calibration_check_run_run(run_name,acq_time,rewrite,mode):
  print OKGREEN + " =================================================" +ENDC
  print OKGREEN + "        ===================================" +ENDC
  print OKGREEN + "               calibration check run " +ENDC
  print OKGREEN + "        ===================================" +ENDC
  print OKGREEN + " =================================================" +ENDC

  cmd="mkdir /home/data/prototech/%s"%(run_name)
  subprocess.call( cmd , shell = True )
  cmd="mkdir /home/data/rootfile/%s"%(run_name)
  subprocess.call( cmd , shell = True )
  cmd="mkdir /home/data/xmlfile/%s"%(run_name)
  subprocess.call( cmd , shell = True )
  cmd="mkdir /home/data/image/%s"%(run_name)
  subprocess.call( cmd , shell = True )

  cmd="mkdir /home/data/prototech/%s/check"%(run_name)
  subprocess.call( cmd , shell = True )
  cmd="mkdir /home/data/rootfile/%s/check"%(run_name)
  subprocess.call( cmd , shell = True )
  cmd="mkdir /home/data/xmlfile/%s/check"%(run_name)
  subprocess.call( cmd , shell = True )
  cmd="mkdir /home/data/image/%s/check"%(run_name)
  subprocess.call( cmd , shell = True )

  for pe in range_pe:
    CALIB_CARD="/home/data/calibration/%s/calibration_card.xml"%(run_name)
    cmd="%s/bin/wgOptimize -m 1 -f %s -p %d"%(ANA_DIR,CALIB_CARD,int(pe))
    subprocess.call( cmd , shell=True)
    
    cmd="%s/shell/reconfigure.sh %s"%(RUN_DIR,XMLCONFIG)
    ret=subprocess.call( cmd , shell=True)
    if ret !=0 :
      sys.exit(FAIL+'Error! While reconfigure!'+ENDC)
      time.sleep(0.1)
    
    #run 
    cmd="ssh wagasci-ana %s/spill_internal.sh"%(CCC_DIR)
    subprocess.call( cmd , shell=True)
    time.sleep(0.1)
    
    run_name0="%s_check_pe%d"%(run_name,int(pe))
    print OKBLUE +"RUN %s start ... "%(run_name0) + ENDC
    
    run=new_run(run_name0,rewrite)
    acq=timed_acq(run_name0,run,float(acq_time))
    wait_acq_finished(acq)
    time.sleep(5)
    
    threads=[]
    threads_state=[0,0]
    
    while(True):
      for i in [0,1]:
        if threads_state[i]==0 :
          threads_state[i] = threads_state[i] + 1
          raw_output="%s/%s/%s_dif_1_1_%d.raw"%(RAW_DIR,run_name0,run_name0,i+1) 
          t=threading.Thread(target=Decode, args=(raw_output,))
          threads.append(t)
          t.start()
        
        elif not threads[i].is_alive():      
          if threads_state[i]==1:
            threads_state[i] = threads_state[i] + 1
            tree_output="%s/%s_dif_1_1_%d_tree.root"%(ROOT_DIR,run_name0,i+1) 
            t=threading.Thread(target=MakeHist, args=(tree_output,))
            threads[i]=t
            t.start()
    
          elif threads_state[i]==2:
            threads_state[i] = threads_state[i] + 1
            hist_output="%s/%s_dif_1_1_%d_hist.root"%(ROOT_DIR,run_name0,i+1)
            config_output="%s/%s/%s.xml"%(RAW_DIR,run_name0,run_name0) 
            t=threading.Thread(target=AnaHist, args=(hist_output,config_output,i+1,mode,))
            threads[i]=t
            t.start()
    
          elif threads_state[i]==3:
            threads_state[i] = threads_state[i] + 1
            xml_output="%s/%s_dif_1_1_%d"%(XML_DIR,run_name0,i+1) 
            t=threading.Thread(target=AnaHistSummary, args=(xml_output,mode,))
            threads[i]=t
            t.start()
    
          elif threads_state[i]==4:
            threads_state[i] = threads_state[i] + 1
            print " ** threads %d Finish! ** "%(i+1)
          
          elif threads_state[i]==5:
            print "..."  
          else:
            print " ** Error!! threads %d ** "%(i+1)
           
        else:
          print " wait until threads %d is released ..."%(i+1)
    
      if(threads_state[0]==5 and threads_state[1]==5):
        print "Finish!!"
        break
    
      time.sleep(5)
           
    cmd="mv /home/data/prototech/%s /home/data/prototech/%s/check"%(run_name0,run_name)
    subprocess.call( cmd , shell = True )  
    for ndif in range_dif:  
      cmd="mv /home/data/rootfile/%s_dif_1_1_%d_tree.root /home/data/rootfile/%s/check"%(run_name0,ndif,run_name)
      subprocess.call( cmd , shell = True )
      cmd="mv /home/data/rootfile/%s_dif_1_1_%d_hist.root /home/data/rootfile/%s/check"%(run_name0,ndif,run_name)
      subprocess.call( cmd , shell = True )
      cmd="mv /home/data/xmlfile/%s_dif_1_1_%d /home/data/xmlfile/%s/check"%(run_name0,ndif,run_name)
      subprocess.call( cmd , shell = True )
      cmd="mv /home/data/image/%s_dif_1_1_%d /home/data/image/%s/check"%(run_name0,ndif,run_name)
      subprocess.call( cmd , shell = True )
    
  print OKGREEN +"RUN %s_check finish! "%(run_name0) + ENDC
  cmd="ssh wagasci-ana %s/spill_off.sh"%(CCC_DIR) #end all run
  subprocess.call( cmd , shell=True)

  CALIB_CARD="/home/data/calibration/%s/calibration_card.xml"%(run_name)
  cmd="%s/bin/wgOptimize -m 1 -f %s -p %d"%(ANA_DIR,CALIB_CARD,3)
  subprocess.call( cmd , shell=True)
  cmd="%s/shell/reconfigure.sh %s"%(RUN_DIR,XMLCONFIG)
  ret=subprocess.call( cmd , shell=True)
#end def

def calibration_check_run_get_progress():
    return progress_acq

def Decode(rawfile):
  cmd="%s/bin/Decoder -rf %s"%(ANA_DIR,rawfile)
  subprocess.call(cmd,shell=True)
  return
  
def MakeHist(treefile):
  cmd="%s/bin/wgMakeHist -rf %s"%(ANA_DIR,treefile)
  subprocess.call(cmd,shell=True)
  return

def AnaHist(histfile,configfile,ndif,mode):
  ana_mode=10
  if int(mode)==0:
    ana_mode=10
  elif int(mode)==1:
    ana_mode=11
  cmd="%s/bin/wgAnaHist -f %s -i %s -d %d -m %d -r"%(ANA_DIR,histfile,configfile,ndif,ana_mode)
  subprocess.call(cmd,shell=True)
  return

def AnaHistSummary(xmlfile,mode):
  cmd="%s/bin/wgAnaHistSummary -rf %s -m %d"%(ANA_DIR,xmlfile,int(mode))
  subprocess.call( cmd , shell=True)
  return

execfile("/opt/calicoes/pycaldaq_rcs.py")
