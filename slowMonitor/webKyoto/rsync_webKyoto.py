#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math, glob
import threading

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

# ================================================================================
def make_js():
  setup = Setup.Setup()
  with open(setup.COPY_RUNID_FILE,"r") as f:
    runid = int(f.read())
  with open(setup.COPY_ACQID_FILE,"r") as f:
    acqid = int(f.read())
  with open("{0}/runid.js".format(setup.ID_DIR),"w") as f:
    f.write("document.write(\"Current RunID:{0}, AcqID:{1}\");".format(runid,acqid))

def rsync_cmd():
  setup = Setup.Setup()
  make_js()
  loglist = "{0}/*.png {1}/*.log {2}/*.png {2}/dq_history_time.js {3}/*.js {4}/*.png".format(
      setup.SM_LOG_DIR,
      setup.SM_LOG_DIR,
      setup.DQ_HISTORY_DIR,
      setup.ID_DIR,
      setup.SPILL_LOG_DIR)
  cmd = "ls {0}".format(loglist)
  res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
  result = res.communicate()[0].strip().split()
  ziplist = ""
  cmd = "cd {0}>> /dev/null; tar zcvf {1} ./*png ./*eps>> /dev/null; cd - >> /dev/null".format(setup.SM_LOG_DIR,setup.KYOTO_LOG_ZIP)
  subprocess.call(cmd,shell=True)
  cmd = "cd {0}>> /dev/null; tar zcvf {1} ./*png>> /dev/null; cd ->> /dev/null".format(setup.DQ_HISTORY_DIR,setup.KYOTO_DQ_ZIP)
  subprocess.call(cmd,shell=True)
  cmd = "rsync -avuz {0} {1}/{2} {3}/{4} {5}:{6} &>> /dev/null"\
      .format(loglist,                             #0
          setup.SM_LOG_DIR,setup.KYOTO_LOG_ZIP,    #1 2 
          setup.DQ_HISTORY_DIR,setup.KYOTO_DQ_ZIP, #3 4
          setup.SERV_KYOTO,setup.KYOTO_WEB_LOG)    #5 6
  subprocess.call(cmd,shell=True)
  with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
    logger.logger.info("Logs are copied to Kyoto HEP server. {0}".format(cmd))

def rsync_loop():
  setup = Setup.Setup()
  while True:
    rsync_cmd()
    time.sleep(setup.KYOTO_TIME_RSYNC)

# ================================================================================

def main():
  if len(sys.argv)>1:
    if sys.argv[1]=="now":
      rsync_cmd()
      return
  else:
    rsync_loop()

# ================================================================================

if __name__ == '__main__':
  main()
