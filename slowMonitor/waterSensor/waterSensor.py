#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math
import serial, binascii
import threading
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup


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
      logger.logger.info("file watch thread is running...")
    while not self.stopped:
      timestamp    = int(os.stat(self.targetfile).st_mtime)
      current_time = int(datetime.datetime.today().strftime("%s"))
      if timestamp == self.last_ts:
        if current_time-timestamp>setup.WATER_NOUPDATE_WARNING:
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.error("FileWatcher: Water level sensor has not been updated for {0} sec."\
                            .format(setup.WATER_NOUPDATE_WARNING))
          setup.set_alarm("Water Level")
        else: pass
      elif timestamp > self.last_ts:
        self.last_ts = timestamp
        self.finished.emit()
      else:
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.error("FileWatcher: timestamp of {0} shows the past to the last one"\
                          .format(setup.WATER_LOG))
          setup.set_alarm("Water Level")
      time.sleep(setup.WATER_TIME_FILEWATCH)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.warning("sound thread is stopped")
    
  def stop(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = True
   
  def setup(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = False
 
# ================================================================================


class watersensor_hist(QtGui.QWidget):

  def __init__(self):
    super(watersensor_hist, self).__init__() 
    self.initUI()
  
  def initUI(self):

    setup = Setup.Setup()
    self.timelabel = QtGui.QLabel("",self)
    d = datetime.datetime.today()
    self.starttimeutc = d.strftime("%s")

    # Histogram
    self.pic = QtGui.QLabel("histgram",self)
    self.pic.setPixmap(QtGui.QPixmap(setup.WATER_PIC1))
    
    self.thread_filewatch = FileWatcher(self,target=setup.WATER_LOG)
    self.thread_filewatch.last_ts = os.stat(setup.WATER_LOG).st_mtime
    self.thread_filewatch.finished.connect(self.makePic)
    self.thread_filewatch.finished.connect(self.changePic)
    self.thread_filewatch.start()

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
    if   self.combo.currentIndex()==0: picname=setup.WATER_PIC1
    elif self.combo.currentIndex()==1: picname=setup.WATER_PIC2
    elif self.combo.currentIndex()==2: picname=setup.WATER_PIC3
    elif self.combo.currentIndex()==3: picname=setup.WATER_PIC4
    self.pic.setPixmap(QtGui.QPixmap(picname))

  def makePic(self):
    setup = Setup.Setup()
    d = datetime.datetime.today()
    self.timestr = d.strftime("%Y-%m-%d %H:%M:%S")
    self.timelabel.setText(self.timestr)
    if self.threads.isAlive():
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.warning("The privious thread is still running. This is skipped.")
      return
    self.thread_check = threading.Thread(target=self.makePlot,args=(self.starttimeutc,))
    self.thread_check.start()

  def makePlot(self,time=""):
    setup = Setup.Setup()
    cmd = "nohup {0} >> /dev/null 2>&1 &".format(setup.WATER_PLOT)
    subprocess.call(cmd,shell=True)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("New plots are made. {0}".format(cmd))

