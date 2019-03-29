#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math, glob
import threading

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup


setup = Setup.Setup()

if not os.path.exists(setup.COPY_DONE_ID_FILE):
  with open(setup.COPY_DONE_ID_FILE,"w") as f:
    f.write(u"0 0")
if not os.path.exists(setup.AUTO_RUNID_LIST):
  runid_raw = []
  rawfilepath1 = "%s/%s*/*_dif_1_1_1.raw"%(setup.BACKUPDATA_DIR,setup.RUNNAME)
  rawfiles1 = glob.glob(rawfilepath1)
  for rawfile1 in rawfiles1:
    rawfilename1 = os.path.basename(rawfile1)
    rawfilename1 = rawfilename1.replace("%s_"%(setup.RUNNAME),"")
    runid = int(rawfilename1[0:5])
    acqid = int(rawfilename1[6:9])
    suffix = rawfilename1.replace("%05d_%03d"%(runid,acqid),"").replace("_dif_1_1_1.raw","")
    rawfilename2 = "%s/%s_%05d%s/%s_%05d_%03d%s_dif_1_1_2.raw"%(
        setup.BACKUPDATA_DIR,
        setup.RUNNAME,runid,suffix,
        setup.RUNNAME,runid,acqid,suffix)
    if os.path.exists(rawfilename2):
      runid_raw.append([runid,acqid])
  runid_raw.sort()

  calibfile = []
  with open(setup.CALIB_ID_FILE,"r") as f:
    line = f.readline().strip().split()
    while line:
      if len(line)==2:
        calibfile.append(line)
      line = f.readline().strip().split()

  with open(setup.AUTO_RUNID_LIST,"w") as f:
    for tmp in runid_raw: 
      calibname = ""
      for i in range(len(calibfile)):
        if tmp[0]>=int(calibfile[i][0]):
          calibname = calibfile[i][1]
          break
      f.write(u"%05d %03d 1 %s\n"%(tmp[0],tmp[1],calibname))

current_runnb = 0
current_acqnb = -1
backup_runnb  = 0
backup_acqnb  = -1
done_runnb    = 0
done_acqnb    = -1

while True:


  # get the current run nb
  cmd = "rsync -avuz {0}:{1} {2} &>> /dev/null"\
    .format(setup.RAWDATA_SERV,setup.RUNID_FILE,setup.COPY_RUNID_FILE)
  subprocess.call(cmd,shell=True)
  with open(setup.COPY_RUNID_FILE,"r") as f:
    current_runnb = int(f.read())
  msg = "The current RunNb is {0}".format(current_runnb)
  with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(msg)
  
  # get the current acq nb
  cmd = "rsync -avuz {0}:{1} {2} &>> /dev/null"\
    .format(setup.RAWDATA_SERV,setup.ACQID_FILE,setup.COPY_ACQID_FILE)
  subprocess.call(cmd,shell=True)
  with open(setup.COPY_ACQID_FILE,"r") as f:
    current_acqnb = int(f.read())
  msg = "The current AcqNb is {0}".format(current_acqnb)
  with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(msg)

 
  # get the run/acq nb completed to rsync
  with open(setup.COPY_DONE_ID_FILE,"r") as f:
    ids = f.readline().split(" ")
    done_runnb = int(ids[0])
    done_acqnb = int(ids[1])
  backup_runnb = done_runnb
  backup_acqnb = done_acqnb+1

  if (backup_runnb==current_runnb and backup_acqnb>=current_acqnb) or\
     (backup_runnb>current_runnb):
    msg = "There is no new acqusition. It will be checked in %d sec."%(setup.COPY_UPDATE_PERIOD)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(msg)
    time.sleep(setup.COPY_UPDATE_PERIOD)

  else:
    #get run dir & suffix
    cmd = "ssh %s basename %s/run_%05d*"%(setup.RAWDATA_SERV,setup.RAWDATA_DIR,backup_runnb)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    run_name = res.communicate()[0].strip()
    suffix = run_name.replace("run_%05d"%(backup_runnb),"")
    cmd = "if ssh {0} test -d {1}/{2} ; then echo 'yes'; else echo 'no'; fi"\
              .format(setup.RAWDATA_SERV,setup.RAWDATA_DIR,run_name)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    isdir = res.communicate()[0].strip()
    if isdir=='no':
      msg = "No such a run directory in %s: %s/%s"%(setup.RAWDATA_SERV,setup.RAWDATA_DIR,run_name)
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(msg)
      with open(setup.COPY_DONE_ID_FILE,"w") as f:
        f.write(u"%05d %03d"%(backup_runnb+1,-1))
      continue
    else:
      #get raw data path
      acq_path = "%s/run_%05d%s/run_%05d_%03d%s"\
                                  %(setup.RAWDATA_DIR,backup_runnb,suffix,
                                      backup_runnb,backup_acqnb,suffix)
      rawfile1 = "%s_dif_1_1_1.raw"%(acq_path)
      rawfile2 = "%s_dif_1_1_2.raw"%(acq_path)

      #make run dir in backup serv, if not exist
      backup_path = "%s/%s"%(setup.BACKUPDATA_DIR,run_name)
      if not os.path.isdir(backup_path):
        os.mkdir(backup_path)

      #get raw file size and copy it if not updated any more
      is_updated = True
      last_filesize1 = -1
      last_filesize2 = -1
      while True:
        if not is_updated:
          cmd = "rsync -avz %s:%s/* %s &>> /dev/null"%(
              setup.RAWDATA_SERV,setup.RAWDATA_DIR,setup.BACKUPDATA_DIR)
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
 
          subprocess.call(cmd,shell=True)
          msg = "Raw data rsync is done: {0}".format(acq_path)
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.info(msg)
          with open(setup.COPY_DONE_ID_FILE,"w") as f:
            f.write(u"%05d %03d"%(backup_runnb,backup_acqnb))
          calibfile = []
          with open(setup.CALIB_ID_FILE,"r") as f:
            line = f.readline().strip().split()
            while line:
              if len(line)==2:
                calibfile.append(line)
              line = f.readline().strip().split()
          with open(setup.AUTO_RUNID_LIST,"a") as f:
            calibname = ""
            for i in range(len(calibfile)):
              if backup_runnb>=int(calibfile[i][0]):
                calibname = calibfile[i][1]
                break
            f.write(u"%05d %03d 1 %s\n"%(backup_runnb,backup_acqnb,calibname))

          break
        else:
          #get file size
          cmd = "ssh %s wc -c %s | awk '{print $1}'"%(setup.RAWDATA_SERV,rawfile1)
          res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
          filesize1 = res.communicate()[0].strip()
          cmd = "ssh %s wc -c %s | awk '{print $1}'"%(setup.RAWDATA_SERV,rawfile2)
          res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
          filesize2 = res.communicate()[0].strip()
          if filesize1.isdigit() and filesize2.isdigit(): 
            if int(filesize1)==last_filesize1 and int(filesize2)==last_filesize2:
              is_updated = False
            last_filesize1 = int(filesize1)
            last_filesize2 = int(filesize2)
          else: #Not exists or broken
            if current_runnb>backup_runnb:
              with open(setup.COPY_DONE_ID_FILE,"w") as f:
                f.write(u"%05d %03d"%(backup_runnb+1,-1))
            else:
              with open(setup.COPY_DONE_ID_FILE,"w") as f:
                f.write(u"%05d %03d"%(backup_runnb,backup_acqnb))
            break
          time.sleep(10) #sec

      #end of while True

    #end of "if isdir"

  # end of "if run/acqnb check"


#end of while True
