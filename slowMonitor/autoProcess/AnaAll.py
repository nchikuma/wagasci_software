#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math, glob
import threading
sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup




############################################################################################

def Decode(rawfile1,rawfile2,calibfile,mode):
  setup = Setup.Setup()
  if os.path.exists(rawfile1) and os.path.exists(rawfile2):
    cmd = "%s -rf %s -i %s &>> %s"%(setup.PROCESS_DECODE,rawfile1,calibfile,setup.DECODE_LOG)
    if mode=="default": print cmd
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
    subprocess.call(cmd,shell=True)
    cmd = "%s -rf %s -i %s &>> %s"%(setup.PROCESS_DECODE,rawfile2,calibfile,setup.DECODE_LOG)
    if mode=="default": print cmd
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
    subprocess.call(cmd,shell=True)
    return True
  else:
    msg ="No such raw files. %s %s"%(rawfile1, rawfile2)
    if mode=="default": print msg
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.warning(msg)

    return False

############################################################################################

def MakeHist(decodefile1,decodefile2,mode):
  setup = Setup.Setup()
  if os.path.exists(decodefile1) and os.path.exists(decodefile2):
    cmd = "%s -rf %s &>> %s"%(setup.PROCESS_HIST,decodefile1,setup.HIST_LOG)
    if mode=="default": print cmd
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
    subprocess.call(cmd,shell=True)
    cmd = "%s -rf %s &>> %s"%(setup.PROCESS_HIST,decodefile2,setup.HIST_LOG)
    if mode=="default": print cmd
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
    subprocess.call(cmd,shell=True)
    return True
  else:
    msg = "No decoded files. %s %s"%(decodefile1, decodefile2)
    if mode=="default": print msg
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.warning(msg)

    return False
  
############################################################################################

def Recon(decodefile1,decodefile2,acqname,mode):
  setup = Setup.Setup()
  if os.path.exists(decodefile1) and os.path.exists(decodefile2):
    cmd = "%s -f %s &>> %s"%(setup.PROCESS_RECON,acqname,setup.RECON_LOG)
    if mode=="default": print cmd
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
    subprocess.call(cmd,shell=True)
    return True
  else:
    msg =  "No decoded files. %s %s"%(decodefile1, decodefile2)
    if mode=="default": print msg
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.warning(msg)

    return False

############################################################################################

def AnaHist(histfile1,histfile2,configfile,mode):
  setup = Setup.Setup()
  if os.path.exists(histfile1) and os.path.exists(histfile2):
    cmd = "%s -f %s -i %s -d %d -m %d &>> %s"%(
        setup.PROCESS_ANAHIST, histfile1, configfile, 1, 11, setup.ANAHIST_LOG)
    if mode=="default": print cmd
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
    subprocess.call(cmd,shell=True)
    cmd = "%s -f %s -i %s -d %d -m %d &>> %s"%(
        setup.PROCESS_ANAHIST, histfile2, configfile, 2, 11, setup.ANAHIST_LOG)
    if mode=="default": print cmd
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
    subprocess.call(cmd,shell=True)
    return True
  else:
    msg =  "No hist files. %s %s"%(histfile1, histfile2)
    if mode=="default": print msg
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.warning(msg)

    return False

############################################################################################

def AnaHistSummary(xmldir1,xmldir2,mode):
  setup = Setup.Setup()
  if os.path.exists(xmldir1) and os.path.exists(xmldir2):
    cmd = "%s -f %s -m %d &>> %s"%(
        setup.PROCESS_ANAHISTSUM, xmldir1, 11, setup.ANAHIST_LOG)
    if mode=="default": print cmd
    elif mode=="auto" : 
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
    subprocess.call(cmd,shell=True)
    cmd = "%s -f %s -m %d &>> %s"%(
        setup.PROCESS_ANAHISTSUM, xmldir2, 11, setup.ANAHIST_LOG)
    if mode=="default": print cmd
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
    subprocess.call(cmd,shell=True)
    return True
  else:
    msg =  "No xml directories. %s %s"%(xmldir1,xmldir2)
    if mode=="default": print msg
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.warning(msg)
    return False

############################################################################################

def DQCheck(acqname,xmldir1,xmldir2,reconfile,calibfile,mode,merge=""):
  setup = Setup.Setup()
  if os.path.exists(xmldir1) and os.path.exists(xmldir2) \
    and os.path.exists(calibfile) and os.path.exists(reconfile):
    if merge=="merge":
      cmd = "%s -f %s -o %s -c %s -r %s &>> %s"%(
          setup.PROCESS_DQCHECK, 
          acqname,setup.DQ_MERGE_DIR,calibfile,setup.MERGE_DIR,setup.ANAHIST_LOG) 
    else:
      cmd = "%s -f %s -c %s &>> %s"%(setup.PROCESS_DQCHECK, acqname, calibfile, setup.ANAHIST_LOG)
        
    if mode=="default": print cmd
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
    subprocess.call(cmd,shell=True)
    return True
  else:
    msg =  "Not existing file, out of either xml, recon, or calibfile, %s %s %s %s"%(
        xmldir1,xmldir2,calibfile,reconfile)
    if mode=="default": print msg
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.warning(msg)
    return False

############################################################################################

def DQHistory(mode,merge=""):
  setup = Setup.Setup()
  if merge=="merge":
    cmd = "%s -f %s &>> %s"%(setup.PROCESS_DQHISTORY,setup.DQ_MERGE_DIR, setup.ANAHIST_LOG)
  else:
    cmd = "%s &>> %s"%(setup.PROCESS_DQHISTORY, setup.ANAHIST_LOG)
    
  if mode=="default": print cmd
  elif mode=="auto" :
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd)
  subprocess.call(cmd,shell=True)
  return True

############################################################################################
def SpillCheck(runid,acqid):
  setup = Setup.Setup()
  cmd = "%s -r %d -s %d &>> %s"%(setup.SPILL_CHECK,int(runid),int(acqid),setup.BSD_ANA_LOG)
  subprocess.call(cmd,shell=True)
  
############################################################################################

def DataQuality(
    runid,acqid,
    histfile1,histfile2,configfile,xmldir1,xmldir2,
    reconfile,calibfile,acqname,mode,merge=""):
  AnaHist(histfile1,histfile2,configfile,mode)
  AnaHistSummary(xmldir1,xmldir2,mode)
  DQCheck(acqname,xmldir1,xmldir2,reconfile,calibfile,mode,merge)
  if merge=="":
    SpillCheck(runid,acqid)
  return True

############################################################################################

def RemoveDecode(decodefile1,decodefile2,histfile1,histfile2,reconfile,mode):
  return True
  #setup = Setup.Setup()
  #if os.path.exists(decodefile1) and os.path.exists(decodefile2)\
  #     and os.path.exists(histfile1) and os.path.exists(histfile2)\
  #     and os.path.exists(reconfile):
  #  os.remove(decodefile1)
  #  os.remove(decodefile2)
  #  return True
  #else:
  #  msg =  "Already removed %s %s"%(decodefile1, decodefile2)
  #  if mode=="default":
  #    print msg
  #  elif mode=="auto":
  #    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
  #      logger.logger.warning(msg)

  #  return False

############################################################################################


def analysis_all(runid=-1,acqid=-1,mode="default"):
  setup = Setup.Setup()

  calibname = setup.get_calibname(runid,acqid)
  if calibname==None:
    msg = "No such runid/acqid, %08d, %03d"%(runid, acqid)
    if mode == "default": 
      print msg
    elif mode == "auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info(msg)
    return

  runidname = "%05d"%(runid)
  acqidname = "%03d"%(acqid)
  
  rawfile1 = glob.glob("%s/%s_%s*/%s_%s_%s*_dif_1_1_1.raw"%(
        setup.BACKUPDATA_DIR,
        setup.RUNNAME,runidname,
        setup.RUNNAME,runidname,acqidname))
  rawfile2 = glob.glob("%s/%s_%s*/%s_%s_%s*_dif_1_1_2.raw"%(
        setup.BACKUPDATA_DIR,
        setup.RUNNAME,runidname,
        setup.RUNNAME,runidname,acqidname))
  if (not len(rawfile1)==1) or (not len(rawfile2)==1): 
    msg =  "There is no such files, otherwise too many files : %s ; %s"%(rawfile1 , rawfile2)
    if mode=="default": print msg
    elif mode=="auto":
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.warning(msg)
    return
  rawfile1 = rawfile1[0]
  rawfile2 = rawfile2[0]
  suffix = rawfile1.replace("%s/%s_%s"%(
        setup.BACKUPDATA_DIR,
        setup.RUNNAME,runidname),"").split("/")[0]
  
  rawfile1 = "%s/%s_%s%s/%s_%s_%s%s_dif_1_1_1.raw"%(
        setup.BACKUPDATA_DIR,
        setup.RUNNAME,runidname,suffix,
        setup.RUNNAME,runidname,acqidname,suffix)
  rawfile2 = "%s/%s_%s%s/%s_%s_%s%s_dif_1_1_2.raw"%(
        setup.BACKUPDATA_DIR,
        setup.RUNNAME,runidname,suffix,
        setup.RUNNAME,runidname,acqidname,suffix)
  configfile = "%s/%s_%s%s/%s_%s_%s%s.xml"%(
        setup.BACKUPDATA_DIR,
        setup.RUNNAME,runidname,suffix,
        setup.RUNNAME,runidname,acqidname,suffix)
  calibfile = "%s/%s/calib_result.xml"%(setup.CALIB_DIR,calibname)
  decodefile1 = "%s/%s_%s_%s%s_dif_1_1_1_tree.root"%(
        setup.DECODE_DATA_DIR,setup.RUNNAME,runidname,acqidname,suffix)
  decodefile2 = "%s/%s_%s_%s%s_dif_1_1_2_tree.root"%(
        setup.DECODE_DATA_DIR,setup.RUNNAME,runidname,acqidname,suffix)
  histfile1 = "%s/%s_%s_%s%s_dif_1_1_1_hist.root"%(
        setup.HIST_DATA_DIR,setup.RUNNAME,runidname,acqidname,suffix)
  histfile2 = "%s/%s_%s_%s%s_dif_1_1_2_hist.root"%(
        setup.HIST_DATA_DIR,setup.RUNNAME,runidname,acqidname,suffix)
  xmldir1 = "%s/%s_%s_%s%s_dif_1_1_1"%(
        setup.XML_DATA_DIR,setup.RUNNAME,runidname,acqidname,suffix)
  xmldir2 = "%s/%s_%s_%s%s_dif_1_1_2"%(
        setup.XML_DATA_DIR,setup.RUNNAME,runidname,acqidname,suffix)

  decodeacqname = "%s/%s_%s_%s%s"%(
        setup.DECODE_DATA_DIR,setup.RUNNAME,runidname,acqidname,suffix)
  acqname = "%s_%s_%s%s"%(
        setup.RUNNAME,runidname,acqidname,suffix)
  reconfile = "%s/%s_%s_%s%s_recon.root"%(
        setup.RECON_DATA_DIR,setup.RUNNAME,runidname,acqidname,suffix)

  state = setup.get_process_state(runid,acqid)
  if state==1 or state==2: 
    setup.set_process_state(runid,acqid,1,2)
    if Decode(rawfile1,rawfile2,calibfile,mode):
      if os.path.exists(decodefile1) and os.path.exists(decodefile2):
        setup.set_process_state(runid,acqid,2,3)
      else:
        setup.set_process_state(runid,acqid,2,92)
    else:
      setup.set_process_state(runid,acqid,2,92)

  state = setup.get_process_state(runid,acqid)
  if state==3 or state==4:
    setup.set_process_state(runid,acqid,3,4)
    if MakeHist(decodefile1,decodefile2,mode):
      if os.path.exists(histfile1) and os.path.exists(histfile2):
        setup.set_process_state(runid,acqid,4,5)
      else:
        setup.set_process_state(runid,acqid,4,94)
    else:
      setup.set_process_state(runid,acqid,4,94)

  state = setup.get_process_state(runid,acqid)
  if state==5 or state==6:
    setup.set_process_state(runid,acqid,5,6)
    if Recon(decodefile1,decodefile2,decodeacqname,mode):
      if os.path.exists(reconfile):
        setup.set_process_state(runid,acqid,6,7)
      else:
        setup.set_process_state(runid,acqid,6,96)
    else:
      setup.set_process_state(runid,acqid,6,96)

  state = setup.get_process_state(runid,acqid)
  if state==7 or state==8:
    setup.set_process_state(runid,acqid,7,8)
    if DataQuality(
        runid,acqid,
        histfile1,histfile2,configfile,xmldir1,xmldir2,reconfile,calibfile,acqname,mode):
      setup.set_process_state(runid,acqid,8,9)
    else:
      setup.set_process_state(runid,acqid,8,98)

  state = setup.get_process_state(runid,acqid)
  if state==9 or state==10:
    setup.set_process_state(runid,acqid,9,10)
    if RemoveDecode(decodefile1,decodefile2,histfile1,histfile2,reconfile,mode):
      setup.set_process_state(runid,acqid,10,11)
    else:
      setup.set_process_state(runid,acqid,10,100)



############################################################################################

def dq_all(runid="",acqidlist=[],mode="default"):
  setup = Setup.Setup()
  mergelist1="" 
  mergelist2="" 
  mergelist3="" 
  calibname = setup.get_calibname(int(runid),0)
  calibfile = "%s/%s/calib_result.xml"%(setup.CALIB_DIR,calibname)
  configfile = "" 

  target_found = False
  mergelist = []
  for i in range(9):
    mergelist.append("%03d"%((int(acqidlist[0])/9)*9+i))
  for nid in range(len(mergelist)):
    state = setup.get_process_state(int(runid),int(mergelist[nid]))
    if state==11 or state==12 or state==13: 
      setup.set_process_state(int(runid),int(mergelist[nid]),11,12)
      runidname = "%05d"%(int(runid))
      acqidname = "%03d"%(int(mergelist[nid]))

      rawfile1 = glob.glob("%s/%s_%s*/%s_%s_%s*_dif_1_1_1.raw"%(
            setup.BACKUPDATA_DIR,
            setup.RUNNAME,runidname,
            setup.RUNNAME,runidname,acqidname))
      rawfile2 = glob.glob("%s/%s_%s*/%s_%s_%s*_dif_1_1_2.raw"%(
            setup.BACKUPDATA_DIR,
            setup.RUNNAME,runidname,
            setup.RUNNAME,runidname,acqidname))
      if (not len(rawfile1)==1) or (not len(rawfile2)==1): 
        msg =  "There is no such files, otherwise too many files : %s ; %s"%(rawfile1 , rawfile2)
        if mode=="default": print msg
        elif mode=="auto":
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.warning(msg)
        return
      rawfile1 = rawfile1[0]
      rawfile2 = rawfile2[0]
      suffix = rawfile1.replace("%s/%s_%s"%(
            setup.BACKUPDATA_DIR,
            setup.RUNNAME,runidname),"").split("/")[0]
      histfile1 = "%s/%s_%s_%s%s_dif_1_1_1_hist.root"%(
            setup.HIST_DATA_DIR,setup.RUNNAME,runidname,acqidname,suffix)
      histfile2 = "%s/%s_%s_%s%s_dif_1_1_2_hist.root"%(
            setup.HIST_DATA_DIR,setup.RUNNAME,runidname,acqidname,suffix)
      reconfile = "%s/%s_%s_%s%s_recon.root"%(
            setup.RECON_DATA_DIR,setup.RUNNAME,runidname,acqidname,suffix)

      if(configfile==""):
        configfile = "%s/%s_%s%s/%s_%s_%s%s.xml"%(
            setup.BACKUPDATA_DIR,
            setup.RUNNAME,runidname,suffix,
            setup.RUNNAME,runidname,acqidname,suffix)
      if os.path.exists(histfile1) and os.path.exists(histfile2) and os.path.exists(reconfile):
        space = " "
        mergelist1 = mergelist1 + histfile1 + space
        mergelist2 = mergelist2 + histfile2 + space
        mergelist3 = mergelist3 + reconfile + space
        target_found = True
    #end state==11
  #end nid
  
  if target_found:
    mergename   = "merge_%05d_%03d_%03d"     %(int(runid),int(acqidlist[0])/9*9,int(acqidlist[0])/9*9+8)
    merge_hist1 = "%s/%s_dif_1_1_1_hist.root"%(setup.MERGE_DIR   ,mergename)         
    merge_hist2 = "%s/%s_dif_1_1_2_hist.root"%(setup.MERGE_DIR   ,mergename)         
    merge_recon = "%s/%s_recon.root"         %(setup.MERGE_DIR   ,mergename)         
    xmldir1     = "%s/%s_dif_1_1_1"          %(setup.XML_DATA_DIR,mergename)
    xmldir2     = "%s/%s_dif_1_1_2"          %(setup.XML_DATA_DIR,mergename)

    cmd1 = "hadd -f %s %s &>> /dev/null"%(merge_hist1,mergelist1)
    cmd2 = "hadd -f %s %s &>> /dev/null"%(merge_hist2,mergelist2)
    cmd3 = "hadd -f %s %s &>> /dev/null"%(merge_recon,mergelist3)

    if mode=="default": print cmd1
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd1)
    subprocess.call(cmd1,shell=True)
    time.sleep(1)

    if mode=="default": print cmd2
    elif mode=="auto" :
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd2)
    subprocess.call(cmd2,shell=True)
    time.sleep(1)

    if mode=="default": print cmd3
    elif mode=="auto" : 
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.info(cmd3)
    subprocess.call(cmd3,shell=True)
    time.sleep(1)

    DataQuality(
        runid,acqid,
        merge_hist1,merge_hist2,configfile,xmldir1,xmldir2,
        merge_recon,calibfile,mergename,mode,"merge")
    DQHistory(mode,"merge")

    if len(acqidlist)==9:
      for acqid in acqidlist:
        setup.set_process_state(int(runid),int(acqid),12,13)

  else:
    msg = "No target was found: %s %s"%(runid,acqidlist)
    if mode=="default": print msg
    elif mode=="auto" : 
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger: logger.logger.warning(msg)




def PrintUsage():
  print "Usage1: {0} ana <runid> <acqid>".format(sys.argv[0])
  print "Usage2: {0} dq  <runid> <acqid-begin> <acqid-end>".format(sys.argv[0])

############################################################################################

if __name__ == '__main__':

  setup = Setup.Setup()

  if len(sys.argv)<4:
    PrintUsage()
    exit(0)
  process = sys.argv[1]

  if process=="ana":
    if (not sys.argv[2].isdigit()) or (not sys.argv[3].isdigit()):
      PrintUsage()
      exit(0)
    process = sys.argv[1]
    runid   = int(sys.argv[2])
    acqid   = int(sys.argv[3])
    mode    = "default"
    if len(sys.argv)>4:
      mode = sys.argv[4]
    analysis_all(runid,acqid,mode)

  elif process=="dq":
    if len(sys.argv)<5:
      PrintUsage()
      exit(0)
    if (not sys.argv[2].isdigit()) or (not sys.argv[3].isdigit()) or (not sys.argv[4].isdigit()):
      PrintUsage()
      exit(0)
    process = sys.argv[1]
    runid   = sys.argv[2]
    acqid   = []
    for i in range(int(sys.argv[3]),int(sys.argv[4])):
      acqid.append("%03d"%(i))
    mode    = "default"
    if len(sys.argv)>5:
      mode = sys.argv[5]
    dq_all(runid,acqid,mode)
  else:
    print "Usage: {0} ana <runid> <acqid>".format(sys.argv[0])
    exit(0)
   
