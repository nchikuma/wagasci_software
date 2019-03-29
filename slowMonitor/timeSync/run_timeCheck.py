#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime, glob
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Setup, Logger

# ================================================================================

def run_loop():
  setup = Setup.Setup()
  while True:
    d = datetime.datetime.today()
    current_hour = d.strftime("%H")
    YYYYMMDD     = d.strftime("%Y%m%d") 
    if current_hour==setup.SERV_TIME_CHECK_HOUR:
      cmd = "ssh {0} date +%s".format(setup.SERV_ACCESS)
      res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
      result_acc = res.communicate()[0].strip()
      cmd = "ssh {0} date +%s".format(setup.SERV_DAQ)
      res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
      result_daq = res.communicate()[0].strip()
      cmd = "date +%s"
      res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
      result_ana = res.communicate()[0].strip()

      if (not result_acc.isdigit()) or\
        (not result_daq.isdigit()) or\
        (not result_ana.isdigit()):
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.warning("Server time check failed.")
      else:
        time_diff_acc = abs(int(result_acc)-int(result_ana))
        isOk = True
        if (time_diff_acc>setup.MAX_TIME_DIFF):
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.warning("Time in {0} differs from time in {1} by {2}"
              .format(setup.SERV_ACCESS,setup.SERV_ANA,time_diff_acc))
          isOk = False
        time_diff_daq = abs(int(result_daq)-int(result_ana))
        if (time_diff_daq>setup.MAX_TIME_DIFF):
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.warning("Time in {0} differs from time in {1} by {2}"
              .format(setup.SERV_DAQ,setup.SERV_ANA,time_diff_daq))
          isOk = False
        if isOk:
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.info("Server times are well synchronized within {0} sec."
              .format(setup.MAX_TIME_DIFF))
    else:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        msg = "Nothing was done. Server time synchronization is checked every {0} o'clock."\
                  .format(setup.SERV_TIME_CHECK_HOUR)
        logger.logger.info(msg)
    time.sleep(setup.SERV_TIME_CHECK_TIME)



# ================================================================================

def main():
  run_loop()

# ================================================================================

if __name__ == '__main__':
  main()
