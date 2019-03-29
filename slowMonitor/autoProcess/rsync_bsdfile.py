#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime, glob
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Setup, Logger, RunSetting

# ================================================================================

def run_now(version="p06",t2krun=-1):
  setup = Setup.Setup()
  dataname = ""
  if version=="p06":
    dataname = "qsd"
  elif version=="v01":
    dataname = "bsd"
  else:
    print "Unknown version. Should be p06/v01"
    return
  cmd="rsync -avz %s:/export/scraid2/data/beam_summary/%s/%s/t2krun%d %s/%s >> /dev/null"%(
      setup.SERV_KYOTO_BACKUP,
      dataname,version,t2krun,
      setup.BSD_DIR,version)
  subprocess.call(cmd,shell=True)
  msg = "BSDs are copied. {0} {1} {2}".format(dataname,version,t2krun)
  with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(msg)

def run_loop(bsd_ver="p06",t2krun=-1):
  setup = Setup.Setup()
  run = RunSetting.RunSetting()
  while True:
    run_now(bsd_ver,t2krun)
    if not os.path.exists(setup.BSD_FILENUM):
      with open(setup.BSD_FILENUM,"w") as f:
        for mrrun in range(run.MRRUN1,run.MRRUN2+1):
          f.write("%03d 0"%(mrrun))
    mrrun_list = []
    filenum_list = []
    with open(setup.BSD_FILENUM,"r") as f:
      line = f.readline().strip().split()
      if len(line)==2:
        mrrun_list  .append(int(line[0]))
        filenum_list.append(int(line[1]))
    for mrrun in range(run.MRRUN1,run.MRRUN2+1):
      sourcefile = "%s/%s/t2krun%d/bsd_run%03d*_*%s.root"%(
        setup.BSD_DIR,run.BSD_VER,run.T2KRUN,mrrun,run.BSD_VER)
      targetfile = "%s/%s/t2krun%d/merge_bsd_run%03d_%s.root"%(
        setup.BSD_DIR,run.BSD_VER,run.T2KRUN,mrrun,run.BSD_VER)
      filelist = glob.glob(sourcefile)
      if mrrun in mrrun_list:
        last_filenum = filenum_list[mrrun_list.index(mrrun)]
        filenum = len(filelist)
        if filenum>last_filenum:
          cmd = "hadd -f %s %s"%(targetfile,sourcefile)
          subprocess.call(cmd,shell=True)
          filenum_list[mrrun_list.index(mrrun)] = len(filelist)
      else:
        mrrun_list.append(mrrun)
        filenum_list.append(0)
    with open(setup.BSD_FILENUM,"w") as f:
      for i in range(len(mrrun_list)):
        f.write("%03d %d\n"%(mrrun_list[i],filenum_list[i]))
    time.sleep(setup.BSD_RSYNC_TIME)

# ================================================================================

def main():
  t2krun  = RunSetting.RunSetting().T2KRUN
  bsd_ver = RunSetting.RunSetting().BSD_VER 
  if len(sys.argv)==3:
    bsd_ver = sys.argv[1]
    t2krun  = int(sys.argv[2])
    run_now(bsd_ver,t2krun)
  elif len(sys.argv)==1:
    run_now(bsd_ver,t2krun)
  else:
    print "Usage: {0} / {0} <p06/v01> <t2krun#>".format(sys.argv[0])
    return

# ================================================================================

if __name__ == '__main__':
  main()
