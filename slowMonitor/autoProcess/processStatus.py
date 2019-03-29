#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math
import serial, binascii
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

class process_status(QtGui.QWidget):

  def __init__(self):
    super(process_status, self).__init__() 
    self.initUI()
  
  def initUI(self):
    setup = Setup.Setup()
    self.auto_process_runid_time = os.stat(setup.AUTO_RUNID_LIST).st_mtime

    # Histogram
    self.pic = QtGui.QLabel("Run Status",self)
    self.pic.setPixmap(QtGui.QPixmap(setup.RUN_STATUS_PIC))

    self.filewatch = QtCore.QFileSystemWatcher(self)
    self.filewatch.fileChanged.connect(self.changePic)
    self.filewatch.addPath(setup.RUN_STATUS_PIC)

    # Timer for making plots
    self.state_timer = QtCore.QTimer(self)
    self.state_timer.timeout.connect(self.makePic)
    self.state_timer.start(2000) #sec

    # layout
    layout = QtGui.QGridLayout(self)
    layout.addWidget(self.pic  ,0,0)

  def changePic(self):
    setup = Setup.Setup()
    self.pic.setPixmap(QtGui.QPixmap(setup.RUN_STATUS_PIC))

  def makePic(self):
    setup = Setup.Setup()
    if not os.stat(setup.AUTO_RUNID_LIST).st_mtime == self.auto_process_runid_time:
      run_id = -1
      with open(setup.COPY_RUNID_FILE,"r") as f:
        run_id = int(f.read())
      cmd = "nohup {0} {1} {2} &>> /dev/null &"\
          .format(setup.RUN_STATUS_PLOT,run_id-4,run_id+1)
      subprocess.call(cmd,shell=True)
      msg = "Process status plot is renewed."
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info(msg)
      self.changePic()
    self.auto_process_runid_time = os.stat(setup.AUTO_RUNID_LIST).st_mtime
