#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Setup, Logger


# ================================================================================

def check_storage(serv=""):
  setup = Setup.Setup()

  if not serv in ["daq","ana","access"]:
    return

  cmd = ""
  outputfile = ""
  if serv=="daq":
    cmd = "ssh {0} df -h | grep \"/home\"".format(setup.SERV_DAQ)
    outputfile = setup.STORAGE_FILE_DAQ
  elif serv=="ana":
    cmd = "df -h | grep \"/home\""
    outputfile = setup.STORAGE_FILE_ANA
  elif serv=="access":
    cmd = "ssh {0} df -h | grep \"/home\"".format(setup.SERV_ACCESS)
    outputfile = setup.STORAGE_FILE_ACCESS
 
  res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
  result = res.communicate()[0].strip().split()
  size  = 0.
  used  = 0.
  avail = 0.
  for i in range(1,4):
    tmp = result[i]
    if   tmp[-1:]=="K": tmp = float(tmp[0:-1])*1e-9
    elif tmp[-1:]=="M": tmp = float(tmp[0:-1])*1e-6
    elif tmp[-1:]=="G": tmp = float(tmp[0:-1])*1e-3
    elif tmp[-1:]=="T": tmp = float(tmp[0:-1])*1
    else              : tmp = float(tmp[0:-1])*1e-12
    if   i==1: size  = tmp
    elif i==2: used  = tmp
    elif i==3: avail = tmp
  percent = float(result[4][0:-1])
  with open(outputfile,"w") as f:
    f.write("Size[T] Used[T] Avail[T] Use%\n")
    f.write("%f %f %f %f"%(size,used,avail,percent))


# ================================================================================

def run_now():
  check_storage("daq")
  check_storage("ana")
  check_storage("access")

# ================================================================================

def run_loop():
  setup = Setup.Setup()
  while True:
    run_now()
    time.sleep(setup.STORAGE_CHECK_TIME)

# ================================================================================

def main():
  mode = "default"
  if len(sys.argv)>0:
    mode = sys.argv[1]
  
  if mode=="default":
    run_loop()
  elif mode=="now":
    run_now()

# ================================================================================

if __name__ == '__main__':
  main()
