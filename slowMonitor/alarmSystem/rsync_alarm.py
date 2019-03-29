#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Setup, Logger

# ================================================================================

def rsync_loop():
  setup = Setup.Setup()
  if not os.path.isfile(setup.ALARM_LOG):
    with open(setup.ALARM_LOG,"w") as f: f.write("\n")
  previous_timestamp = int(os.stat(setup.ALARM_LOG).st_mtime)
  while True:
    current_timestamp = int(os.stat(setup.ALARM_LOG).st_mtime)
    if not current_timestamp==previous_timestamp:
      cmd = "rsync -avz {0} {1}:{2} >> /dev/null"\
            .format(setup.ALARM_LOG,setup.SERV_ACCESS,setup.ALARM_LOG)
      subprocess.call(cmd,shell=True)
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("Rsync has been done.")
    previous_timestamp = current_timestamp
    time.sleep(setup.ALARM_TIME_RSYNC)

# ================================================================================

def main():
  rsync_loop()

# ================================================================================

if __name__ == '__main__':
  main()
