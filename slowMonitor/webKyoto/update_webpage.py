#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math
import threading

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

# ================================================================================

def update_webpage():
  setup = Setup.Setup()
  #cmd = "scp -r {0}/* {1}:{2}"\
  cmd = "rsync -avz {0}/* {1}:{2} &>> /dev/null"\
           .format(setup.KYOTO_WEB_LOCAL,setup.SERV_KYOTO,setup.KYOTO_WEB_DIR)
  print cmd
  subprocess.call(cmd,shell=True)
  with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
    logger.logger.info("The web page on kyoto hep-serv has been updated.: {0}".format(cmd))

  loglist = "{0}/*.png {1}/*.log {2}/*.png {2}/*.js {3}/*png".format(
      setup.SM_LOG_DIR,setup.SM_LOG_DIR,setup.DQ_HISTORY_DIR,setup.SPILL_LOG_DIR)
  print loglist
  cmd = "rsync -avz {0} {1}:{2} &>> /dev/null".format(loglist,setup.SERV_KYOTO,setup.KYOTO_WEB_LOG)
  subprocess.call(cmd,shell=True)
  with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
    logger.logger.info("Logs are copied to Kyoto HEP server. {0}".format(cmd))


# ================================================================================

def main():
  update_webpage()

# ================================================================================

if __name__ == '__main__':
  main()
