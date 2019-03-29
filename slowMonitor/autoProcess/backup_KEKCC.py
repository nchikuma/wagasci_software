#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime, glob
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Setup, Logger

# ================================================================================

def run_now():
  cmd = "rsync -avz /home/data/daqdata KEKCCnchikuma:/hsm/nu/wagasci/ &>> /dev/null"
  subprocess.call(cmd,shell=True)
  cmd = "rsync -avz /home/data/recon KEKCCnchikuma:/hsm/nu/wagasci/ &>> /dev/null"
  subprocess.call(cmd,shell=True)
  cmd = "rsync -avz /home/data/calibration KEKCCnchikuma:/hsm/nu/wagasci/ &>> /dev/null"
  subprocess.call(cmd,shell=True)
  cmd = "rsync -avz /home/data/runid KEKCCnchikuma:/hsm/nu/wagasci/ &>> /dev/null"
  subprocess.call(cmd,shell=True)
  cmd = "rsync -avz /home/data/monitor_log KEKCCnchikuma:/hsm/nu/wagasci/ &>> /dev/null"
  subprocess.call(cmd,shell=True)


def run_loop():
  setup = Setup.Setup()
  while True:
    run_now()
    msg = "Raw data are copied to the KEKCC tape region"
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(msg)
    time.sleep(10800) #3 hours

# ================================================================================

def main():
  mode = "default"
  if len(sys.argv)>1:
    mode = sys.argv[1]
  if mode=="default":
    run_loop()
  elif mode=="now":
    run_now()
  else:
    return

# ================================================================================

if __name__ == '__main__':
  main()
