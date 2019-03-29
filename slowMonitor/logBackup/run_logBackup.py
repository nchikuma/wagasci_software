#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime, glob
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Setup, Logger

# ================================================================================

def run_loop(doNow=False):
  setup = Setup.Setup()
  while True:
    d = datetime.datetime.today()
    current_hour = d.strftime("%H")
    YYYYMMDD     = d.strftime("%Y%m%d") 
    if current_hour==setup.LOG_BACKUP_HOUR or doNow:
      dir_backup = "{0}/{1}".format(setup.SM_LOG_DIR,YYYYMMDD)
      if not os.path.isdir(dir_backup):
        os.mkdir(dir_backup)
      logfiles = glob.glob("{0}/*.log".format(setup.SM_LOG_DIR))
      if doNow:
        print logfiles
      for logfile in logfiles:
        cmd = "cp -f {0} {1}".format(logfile,dir_backup)
        subprocess.call(cmd,shell=True)
        linemax = 0
        if logfile==setup.SLOWMONITOR_LOG: linemax = setup.LINE_MAX_SLOWMONITOR
        elif logfile==setup.DECODE_LOG   : linemax = setup.LINE_MAX_DECODE
        elif logfile==setup.RECON_LOG    : linemax = setup.LINE_MAX_RECON
        elif logfile==setup.ALARM_LOG    : linemax = setup.LINE_MAX_ALARM
        elif logfile==setup.TEMP_LOG     : linemax = setup.LINE_MAX_TEMP
        elif logfile==setup.LAMBDA_LOG   : linemax = setup.LINE_MAX_LAMBDA
        while True:
          linenum = 0
          with open(logfile) as f:
            linenum = len(f.readlines())
          if linenum > linemax:
            cmd = "sed -i \"1,1000d\" {0}".format(logfile)
            subprocess.call(cmd,shell=True)
          else:
            break
      logfiles = glob.glob("{0}/*.txt".format(setup.SM_LOG_DIR))
      for logfile in logfiles:
        cmd = "cp -f {0} {1}".format(logfile,dir_backup)
        subprocess.call(cmd,shell=True)
      logfiles = glob.glob("{0}/*.csv".format(setup.SM_LOG_DIR))
      for logfile in logfiles:
        cmd = "cp -f {0} {1}".format(logfile,dir_backup)
        subprocess.call(cmd,shell=True)
      logfiles = glob.glob("{0}/*.png".format(setup.SM_LOG_DIR))
      for logfile in logfiles:
        cmd = "cp -f {0} {1}".format(logfile,dir_backup)
        subprocess.call(cmd,shell=True)
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("Log files have been copied as backup. {0}".format(dir_backup))
      if doNow:
        return
    else:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("Nothing was done. Logs are copied as backup every {0} o'clock."
            .format(setup.LOG_BACKUP_HOUR))
    time.sleep(setup.LOG_BACKUP_TIME)



# ================================================================================

def main():
  doNow = False
  if len(sys.argv)>1:
    if sys.argv[1]=="now":
      doNow = True
  run_loop(doNow)

# ================================================================================

if __name__ == '__main__':
  main()
