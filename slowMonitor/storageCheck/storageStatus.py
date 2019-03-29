#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math
import serial, binascii
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup, storageCheck

class storage_status(QtGui.QWidget):

  def __init__(self):
    super(storage_status, self).__init__() 
    self.initUI()
  
  def initUI(self):
    setup = Setup.Setup()

    # Histogram
    self.pic = QtGui.QLabel("Storage Status",self)
    self.pic.setPixmap(QtGui.QPixmap(setup.STORAGE_PIC))

    self.filewatch = QtCore.QFileSystemWatcher(self)
    self.filewatch.fileChanged.connect(self.changePic)
    self.filewatch.addPath(setup.STORAGE_PIC)

    # Timer for making plots
    self.state_timer = QtCore.QTimer(self)
    self.state_timer.timeout.connect(self.makePic)
    self.state_timer.start(setup.STORAGE_CHECK_TIME*1000) #msec

    # layout
    layout = QtGui.QGridLayout(self)
    layout.addWidget(self.pic,0,0)

  def changePic(self):
    setup = Setup.Setup()
    self.pic.setPixmap(QtGui.QPixmap(setup.STORAGE_PIC))

  def makePic(self):
    setup = Setup.Setup()
    storageCheck.run_now()
    cmd = "nohup {0} > /dev/null &".format(setup.STORAGE_PLOT)
    subprocess.call(cmd,shell=True)
    msg = "Storage plot is renewed."
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info(msg)
    self.changePic()
