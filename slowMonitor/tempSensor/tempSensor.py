#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math
import serial, binascii
import threading
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

#================================================================================

class ReadThread(QtCore.QThread):

  mutex = QtCore.QMutex()

  def __init__(self,parent=None):
    super(ReadThread,self).__init__(parent)
    self.stopped = False

  def run(self):
    setup = Setup.Setup()
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("Temparature read thread is running...")
    while not self.stopped:
      d = datetime.datetime.today()
      timestr  = d.strftime("%Y/%m/%d %H:%M:%S")
      unixtime = d.strftime("%s")
      cmd = "usbrh -f1 -1"
      res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
      var1 = res.communicate()[0].strip()
      cmd = "usbrh -f2 -1"
      res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
      var2 = res.communicate()[0].strip()
      result = "[{0}|unixtime={1}]{2}|{3}".format(timestr,unixtime,var1,var2)
      cmd = "echo \"{0}\" >> {1}".format(result,setup.TEMP_LOG)
      subprocess.call(cmd,shell=True)
      time.sleep(setup.TEMP_TIME_READ)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.warning("Temparature read thread is stopped.")
    
  def stop(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = True
   
  def setup(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = False

# ================================================================================

class FileWatcher(QtCore.QThread):

  mutex = QtCore.QMutex()

  def __init__(self,parent=None,target=""):
    super(FileWatcher,self).__init__(parent)
    self.stopped = False
    self.last_ts = 0
    self.targetfile = target

  def run(self):
    setup = Setup.Setup()
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("File watch thread is running...")
    while not self.stopped:
      timestamp    = int(os.stat(self.targetfile).st_mtime)
      current_time = int(datetime.datetime.today().strftime("%s"))
      if timestamp == self.last_ts:
        if current_time-timestamp>setup.TEMP_NOUPDATE_WARNING:
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.error("FileWatcher: Temperature sensor has not been updated for {0} sec."\
                            .format(setup.TEMP_NOUPDATE_WARNING))
          setup.set_alarm("Temperature")
        else: pass
      elif timestamp > self.last_ts:
        self.last_ts = timestamp
        self.finished.emit()
      else:
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.warning("FileWatcher: timestamp of alarm log shows the past to the last one")
        #setup.set_alarm("Temperature")
      time.sleep(setup.TEMP_TIME_FILEWATCH)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.warning("File watch thread is stopped")
    
  def stop(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = True
   
  def setup(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = False
 
# ================================================================================


class tempsensor_hist(QtGui.QWidget):

  def __init__(self):
    super(tempsensor_hist, self).__init__() 
    self.initUI()
  
  def initUI(self):

    setup = Setup.Setup()
    self.timelabel = QtGui.QLabel("",self)

    # Histogram
    self.pic = QtGui.QLabel("histgram",self)
    self.pic.setPixmap(QtGui.QPixmap(setup.TEMP_PIC1))

    if not os.path.isfile(setup.TEMP_LOG):
      with open(setup.TEMP_LOG,"w") as f: f.write("\n")
    self.thread_filewatch = FileWatcher(self,target=setup.TEMP_LOG)
    self.thread_filewatch.last_ts = os.stat(setup.TEMP_LOG).st_mtime
    self.thread_filewatch.finished.connect(self.makePic)
    self.thread_filewatch.start()

    self.thread_read = ReadThread(self)
    self.thread_read.start()

    # Period select
    self.combo = QtGui.QComboBox(self)
    self.combo.addItem("10 min")
    self.combo.addItem("1 hour")
    self.combo.addItem("1 day ")
    self.combo.addItem("3 days")
    self.combo.activated.connect(self.changePic)

    # layout
    layout = QtGui.QGridLayout(self)
    layout.addWidget(self.timelabel,0,0)
    layout.addWidget(self.pic      ,1,0)
    layout.addWidget(self.combo    ,2,0)

    self.threads = threading.Thread()
    
  def changePic(self):
    setup = Setup.Setup()
    if   self.combo.currentIndex()==0: picname=setup.TEMP_PIC1
    elif self.combo.currentIndex()==1: picname=setup.TEMP_PIC2
    elif self.combo.currentIndex()==2: picname=setup.TEMP_PIC3
    elif self.combo.currentIndex()==3: picname=setup.TEMP_PIC4
    self.pic.setPixmap(QtGui.QPixmap(picname))

  def makePic(self):
    setup = Setup.Setup()
    self.changePic()
    d = datetime.datetime.today()
    self.timestr = d.strftime("%Y-%m-%d %H:%M:%S")
    self.timelabel.setText(self.timestr)
    if self.threads.isAlive():
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.warning("The privious thread is still running. This is skipped.")
      return
    self.thread_check = threading.Thread(target=self.makePlot)
    self.thread_check.start()

  def makePlot(self):
    setup = Setup.Setup()
    cmd = "nohup {0} >> /dev/null 2>&1 &".format(setup.TEMP_PLOT)
    subprocess.call(cmd,shell=True)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("New plots are made. {0}".format(cmd))
