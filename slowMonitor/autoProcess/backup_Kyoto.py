#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math, glob
import threading

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup


def run_now(mode="default"):
  setup = Setup.Setup()
  cmd = ""
  if mode=="default":
    cmd = "rsync -avz {0} {1}:{2} >> /dev/null".format(
      setup.BACKUPDATA_DIR,setup.SERV_KYOTO_BACKUP,setup.BACKUP_KYOTO_DIR)
  elif mode=="now":
    cmd = "rsync -avz {0} {1}:{2}".format(
      setup.BACKUPDATA_DIR,setup.SERV_KYOTO_BACKUP,setup.BACKUP_KYOTO_DIR)
  else:
    return
 
  if mode=="default":
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    msg = "Raw data backup is done:"
    for var in result:
      msg += var.replace("\n",";")
    if mode=="default":
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info(msg)
  elif mode=="now":
    subprocess.call(cmd,shell=True)
    print "Start RSYNC raw data..."
  else:
    return
  
  if mode=="default":
    cmd = "rsync -avz {0} {1}:{2} >> /dev/null".format(
      setup.RECON_DATA_DIR,setup.SERV_KYOTO_BACKUP,setup.BACKUP_KYOTO_DIR)
  elif mode=="now":
    cmd = "rsync -avz {0} {1}:{2}".format(
      setup.RECON_DATA_DIR,setup.SERV_KYOTO_BACKUP,setup.BACKUP_KYOTO_DIR)
  else:
    return
  
  if mode=="default":
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    msg = "Recon data backup is done:"
    for var in result:
      msg += var.replace("\n",";")
    if mode=="default":
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info(msg)
  elif mode=="now":
    print "Start RSYNC recon data..."
    subprocess.call(cmd,shell=True)
  else:
    return
  

  if mode=="default":
    cmd = "rsync -avz {0} {1}:{2} >> /dev/null".format(
      setup.CALIB_DIR,setup.SERV_KYOTO_BACKUP,setup.BACKUP_KYOTO_DIR)
  elif mode=="now":
    cmd = "rsync -avz {0} {1}:{2}".format(
      setup.CALIB_DIR,setup.SERV_KYOTO_BACKUP,setup.BACKUP_KYOTO_DIR)
  else:
    return

  if mode=="default":
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    msg = "Calibration data backup is done:"
    for var in result:
      msg += var.replace("\n",";")
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info(msg)
  elif mode=="now":
    print "Start RSYNC calibration data..."
    subprocess.call(cmd,shell=True)
  else:
    return

  if mode=="default":
    cmd = "rsync -avz {0} {1}:{2} >> /dev/null".format(
      setup.ID_DIR,setup.SERV_KYOTO_BACKUP,setup.BACKUP_KYOTO_DIR)
  elif mode=="now":
    cmd = "rsync -avz {0} {1}:{2}".format(
      setup.ID_DIR,setup.SERV_KYOTO_BACKUP,setup.BACKUP_KYOTO_DIR)
  else:
    return

  if mode=="default":
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    msg = "Runid data backup is done:"
    for var in result:
      msg += var.replace("\n",";")
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info(msg)
  elif mode=="now":
    print "Start RSYNC runid data..."
    subprocess.call(cmd,shell=True)
  else:
    return

  if mode=="default":
    cmd = "rsync -avz {0} {1}:{2} >> /dev/null".format(
      setup.SM_LOG_DIR,setup.SERV_KYOTO_BACKUP,setup.BACKUP_KYOTO_DIR)
  elif mode=="now":
    cmd = "rsync -avz {0} {1}:{2}".format(
      setup.SM_LOG_DIR,setup.SERV_KYOTO_BACKUP,setup.BACKUP_KYOTO_DIR)
  else:
    return

  if mode=="default":
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    msg = "Monitor log data backup is done:"
    for var in result:
      msg += var.replace("\n",";")
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info(msg)
  elif mode=="now":
    print "Start RSYNC monitor log data..."
    subprocess.call(cmd,shell=True)
  else:
    return

def run_loop():
  setup = Setup.Setup()
  while True:
    run_now()    
    time.sleep(setup.BACKUP_KYOTO_TIME)


if __name__ == '__main__' :

  mode = "default"
  if len(sys.argv)>1:
    mode = sys.argv[1]

  if mode=="default":
    run_loop()
  elif mode=="now":
    print "run now"
    run_now(mode)
    
