#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math, glob
import threading

sys.path.append("{0}/".format(os.path.abspath(os.path.dirname(__file__))))
import rsync_bsdfile

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup, RunSetting

# =================================================================================
def merge_files(sourcefile="",targetfile="",mode=""):
  setup = Setup.Setup()    
  if mode=="local":
    cmd = "hadd -f %s %s"%(targetfile,sourcefile)
  else:
    cmd = "hadd -f %s %s &>> %s"%(targetfile,sourcefile,setup.BSD_ANA_LOG)
  subprocess.call(cmd,shell=True)
  msg = "BSD files have been merged: SRC=%s, TARGET=%s"%(sourcefile,targetfile)
  with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(msg)

# =================================================================================
def bsd_spillcheck(t2krun=-1,mrrun=-1,bsd_ver="",mode=""):
  setup = Setup.Setup()
  if mode=="local":
    cmd = "{0} -t {1} -m {2} -v {3}".format(
        setup.BSD_SPILLCHECK,t2krun,mrrun,bsd_ver)
  else:
    cmd = "{0} -t {1} -m {2} -v {3} &>> {4}".format(
        setup.BSD_SPILLCHECK,t2krun,mrrun,bsd_ver,setup.BSD_ANA_LOG)
  subprocess.call(cmd,shell=True)
  msg = "BSD Spill list has been created: T2KRUN=%d, MRRUN=%d, BSD_VER=%s"%(
      t2krun,mrrun,bsd_ver)
  with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(msg)

# =================================================================================
def get_bsd_spill_time(srcfile):
  spill    = []
  mode     = []
  unixtime = []
  pot      = []
  num_line = 0
  with open(srcfile,"r") as f:
    line = f.readline()
    while line:
      line = line.strip().split()
      if len(line)==4:
        spill   .append(int(line[0]))
        mode    .append(int(line[1]))
        unixtime.append(int(line[2]))
        pot     .append(float(line[3]))
        num_line += 1
      line = f.readline()
  return [spill,mode,unixtime,pot,num_line]


# =================================================================================

def get_wagasci_spill_time(srcfile):
  spill     = []
  sunixtime = 0 
  funixtime = 0 
  num_line = 0
  with open(srcfile,"r") as f:
    line = f.readline()
    while line:
      line = line.strip().split()
      if len(line)==3:
        if (sunixtime==0 or sunixtime==int(line[1])) and \
           (funixtime==0 or funixtime==int(line[2])):
          spill    .append(int(line[0]))
          sunixtime = int(line[1])
          funixtime = int(line[2])
          num_line += 1
      line = f.readline()
  return [spill,sunixtime,funixtime,num_line]


# =================================================================================

def wagasci_spillcheck(t2krun,mrrun,runid1=-1,runid2=-1,mode=""):
  setup = Setup.Setup()

  # get BSD spill files
  bsdspillfile = "%s/spill_bsd_t2krun%d_mrrun%03d.txt"%(
      setup.SPILL_LOG_DIR,t2krun,mrrun)
  if not os.path.exists(bsdspillfile):
    msg = "No such a file : %s"%(bsdspillfile)
    if mode=="local":
      print msg
    else:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.warning(msg)
    return

  msg = "Checking WAGASCI spill."
  with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(msg)

  bsd_spilltime = get_bsd_spill_time(bsdspillfile)
  num_bsdspilltime = bsd_spilltime[4]
  bsd_spill        = bsd_spilltime[0]
  bsd_mode         = bsd_spilltime[1]
  bsd_unixtime     = bsd_spilltime[2]
  bsd_pot          = bsd_spilltime[3]
  bsd_starttime    = bsd_unixtime[0]
  bsd_stoptime     = bsd_unixtime[num_bsdspilltime-1]

  # get wagasci spill files
  bsdevt = 0
  targetfile = "%s/spill_wg_t2krun%d_mrrun%03d.txt"%(setup.SPILL_LOG_DIR,int(t2krun),int(mrrun))
  with open(targetfile,"w") as f:
    f.write("")
  for runid in range(runid1,runid2):
    sourcefile = "%s/spill_wg_run%05d_acq*.txt"%(setup.SPILL_LOG_DIR,runid)
    filelist = sorted(glob.glob(sourcefile))
    i=0
    numfile = len(filelist)
    for ifile in filelist:
      i+=1
      if mode=="local":
        print "Reading ", ifile, "%dth file, out of %d"%(i,numfile)
      wg_spilltime = get_wagasci_spill_time(ifile)
      num_wgspilltime = wg_spilltime[3]
      wg_starttime    = wg_spilltime[1]
      wg_stoptime     = wg_spilltime[2]
      if wg_starttime>bsd_stoptime or wg_stoptime<bsd_starttime:
        pass
      else:
        for wgevt in range(num_wgspilltime):
          wg_spill = wg_spilltime[0][wgevt]
          last_bsdevt = bsdevt
          while True:
            if bsdevt>=num_bsdspilltime:
              bsdevt=0
              break
            elif bsd_unixtime[bsdevt]>wg_stoptime:
              break
            elif bsd_unixtime[bsdevt]<wg_starttime:
              bsdevt+=1
            else:
              if wg_spill+1==bsd_spill[bsdevt]%0x8000:
                cmd = "echo \"%d %d %d %6.5e\" >> %s"%(
                  bsd_spill[bsdevt],bsd_mode[bsdevt],
                  bsd_unixtime[bsdevt],bsd_pot[bsdevt],
                  targetfile)
                subprocess.call(cmd,shell=True)
                last_bsdevt=bsdevt
                bsdevt+=1
                break
              elif wg_spill+1<bsd_spill[bsdevt]%0x8000:
                last_bsdevt=bsdevt
                break
              else: 
                bsdevt+=1
   
  # Check SPILL gap
  bsdspillfile = "%s/spill_bsd_t2krun%d_mrrun%03d.txt" %(setup.SPILL_LOG_DIR,int(t2krun),int(mrrun))
  wgspillfile  = "%s/spill_wg_t2krun%d_mrrun%03d.txt"  %(setup.SPILL_LOG_DIR,int(t2krun),int(mrrun))
  diffspillfile= "%s/spill_diff_t2krun%d_mrrun%03d.txt"%(setup.SPILL_LOG_DIR,int(t2krun),int(mrrun))
  cmd = "diff {0} {1} | grep \"<\"".format(bsdspillfile,wgspillfile)
  res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
  result = res.communicate()[0].strip().split("\n")
  with open(diffspillfile,"w") as f:
    for line in result:
      line = line.split()
      f.write("%s %s %s %s\n"%(line[1],line[2],line[3],line[4]))
    

# =================================================================================
def pot_history(t2krun=-1,mrrun=-1,bsd_ver="",mode=""):
  setup = Setup.Setup()
  bsdspillfile = "%s/spill_bsd_t2krun%d_mrrun%03d.txt" %(setup.SPILL_LOG_DIR,int(t2krun),int(mrrun))
  wgspillfile  = "%s/spill_wg_t2krun%d_mrrun%03d.txt"  %(setup.SPILL_LOG_DIR,int(t2krun),int(mrrun))
  diffspillfile= "%s/spill_diff_t2krun%d_mrrun%03d.txt"%(setup.SPILL_LOG_DIR,int(t2krun),int(mrrun))
  if not (\
      os.path.exists(bsdspillfile ) and \
      os.path.exists(wgspillfile  ) and \
      os.path.exists(diffspillfile) ):
    return
  msg = "Making POT history plots."
  with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(msg)
  cmd = "{0} -t {1} -m {2} -v {3}".format(setup.SPILL_EFF,t2krun,mrrun,bsd_ver)
  subprocess.call(cmd,shell=True)

# =================================================================================
def process_now(t2krun=-1,mrrun=-1,bsd_ver="",runid1=-1,runid2=-1,mode=""):
  setup = Setup.Setup()
  sourcefile = "%s/%s/t2krun%d/bsd_run%03d*_*%s.root"%(
      setup.BSD_DIR,bsd_ver,t2krun,mrrun,bsd_ver)
  targetfile = "%s/%s/t2krun%d/merge_bsd_run%03d_%s.root"%(
      setup.BSD_DIR,bsd_ver,t2krun,mrrun,bsd_ver)
  if len(glob.glob(sourcefile))<1:
    msg = "No BSD files: %s"%(sourcefile)
    if mode=="local":
      print msg
    else:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.warning(msg)
    return
  merge_files(sourcefile,targetfile,mode)              #Merge
  bsd_spillcheck    (t2krun,mrrun,bsd_ver,mode)        #Spill check
  wagasci_spillcheck(t2krun,mrrun,runid1,runid2,mode)  #WAGASCI SPILL
  pot_history       (t2krun,mrrun,bsd_ver,mode)        #Plot POT history
  msg = "BSD Analysis has been completed."
  with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(msg)

# =================================================================================

def process_loop():
  setup = Setup.Setup()
  run   = RunSetting.RunSetting()
  t2krun  = run.T2KRUN
  bsd_ver = run.BSD_VER
  mrrun1  = run.MRRUN1
  mrrun2  = run.MRRUN2
  runid1  = run.WAGASCI_RUN1
  runid2  = run.WAGASCI_RUN2
  if not os.path.exists(setup.BSD_FILENUM):
    with open(setup.BSD_FILENUM,"w") as f:
      for mrrun in range(mrrun1,mrrun2+1):
        f.write("%03d 0"%(mrrun))

  while True:
    # Copy BSD files from kyoto server
    rsync_bsdfile.run_now(bsd_ver,t2krun)

    # Check the previous number of BSD files 
    mrrun_list = []
    filenum_list = []
    with open(setup.BSD_FILENUM,"r") as f:
      line = f.readline()
      while line:
        line = line.strip().split()
        if len(line)==2:
          if int(line[0]) in range(mrrun1,mrrun2+1):
            mrrun_list  .append(int(line[0]))
            filenum_list.append(int(line[1]))
        line = f.readline()
    msg = "MRRun = {0}, WAGASCI run = {1}".format(mrrun_list,range(runid1,runid2+1))
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info(msg)

    # If there is a new file, merge all the BSD files and start the process
    for mrrun in range(mrrun1,mrrun2+1):
      sourcefile = "%s/%s/t2krun%d/bsd_run%03d*_*%s.root"%(
        setup.BSD_DIR,run.BSD_VER,run.T2KRUN,mrrun,run.BSD_VER)
      targetfile = "%s/%s/t2krun%d/merge_bsd_run%03d_%s.root"%(
        setup.BSD_DIR,run.BSD_VER,run.T2KRUN,mrrun,run.BSD_VER)
      filenum = len(glob.glob(sourcefile))
      if mrrun in mrrun_list:
        last_filenum = filenum_list[mrrun_list.index(mrrun)]
        if filenum>last_filenum:
          msg = "Found new BSD files. Analysis process starts."
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.info(msg)
          filenum_list[mrrun_list.index(mrrun)] = filenum
          process_now(t2krun,mrrun,bsd_ver,runid1,runid2) #Analysis process
        else:
          msg = "No new BSD files. Nothing has been done."
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.info(msg)
      else:
        mrrun_list.append(mrrun)
        filenum_list.append(0)
    with open(setup.BSD_FILENUM,"w") as f:
      for i in range(len(mrrun_list)):
        f.write("%03d %d\n"%(mrrun_list[i],filenum_list[i]))
    time.sleep(setup.BSD_RSYNC_TIME)

#=================================================================================
def PrintUsage():
  print "Usage:"
  print "1.",sys.argv[0]
  print "2.",sys.argv[0],"now <t2krun> <mrrun> <p06/v01> <wg runid1> <wg runid2>"

# =================================================================================

if __name__ == '__main__':
  mode = "default"
  if len(sys.argv)>1:
    mode = sys.argv[1]
  if mode == "default":
    process_loop()
  elif mode == "now":
    if len(sys.argv)>6:
      t2krun  = int(sys.argv[2])
      mrrun   = int(sys.argv[3])
      bsd_ver = sys.argv[4]
      runid1  = int(sys.argv[5])
      runid2  = int(sys.argv[6])
      rsync_bsdfile.run_now(bsd_ver,t2krun)
      process_now(t2krun,mrrun,bsd_ver,runid1,runid2,"local")
    else:
      PrintUsage()
  else:
    PrintUsage()
