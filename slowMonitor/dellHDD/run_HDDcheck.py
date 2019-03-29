#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Setup, Logger

# ================================================================================

def run_loop():
  setup = Setup.Setup()
  while True:
    cmd = "{0} | grep -v \"Power Status\" | grep \"Status\"".format(setup.HDD_CHECK)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result = res.communicate()[0].strip().replace(" ","").split("\n")
    for i in range(len(result)):
      if result[i]=="Status:Ok":
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.info("Physical Disk #{0} is OK.".format(i))
      else:
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.error("Physical Disk #{0} is NG. Check the HDD status.".format(i))
        setup.set_alarm("HDD Stauts")
    time.sleep(setup.HDD_TIME_LOOP)


# ================================================================================

def main():
  run_loop()

# ================================================================================

if __name__ == '__main__':
  main()
