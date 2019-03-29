#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime, math
import serial, binascii
import threading
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

 
# ================================================================================

class ReadThread(QtCore.QThread):

  serdev = serial.Serial()
  mutex  = QtCore.QMutex()
  device = "/dev/ttyACM0"

  def __init__(self,parent=None):
    super(ReadThread,self).__init__(parent)
    self.stopped = False

  def run(self):
    setup = Setup.Setup()
    self.setserial()
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("ReadThread is running")
    with open(setup.SPILL_LOG,"w") as f:
      f.write("")
    time.sleep(1)

    while True:
      line = self.serdev.readline().strip()
      current_spillnb = -1
      if "spillnum=" in line:
        result = line.split("spillnum=")
        if len(result)==2:
          current_spillnb=result[1].strip()
          line_num = 0
          with open(setup.SPILL_LOG,"r") as f:
            line_num = len(f.readlines())
          if line_num>=setup.SPILL_MAXLINE:
            cmd = "sed -i \"1,{0}d\" {1}".format(line_num-setup.SPILL_MAXLINE,setup.SPILL_LOG)
            subprocess.call(cmd,shell=True)
          with open(setup.SPILL_LOG,"a") as f:
            f.write("%s\n"%(current_spillnb))
      self.finished.emit()
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.warning("ReadThread is stopped")
    
  def setserial(self):
    setup = Setup.Setup()
    try:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("setserial: Target device is {0}".format(self.device))
      if self.serdev.isOpen():
        self.serdev.close()
      self.serdev.port             = self.device
      self.serdev.baudrate         = 11520
      self.serdev.bytesize         = 8    #EIGHTBITS
      self.serdev.parity           = "N"  #PARITY_NONE
      self.serdev.stopbits         = 1    #STOPBITS_ONE
      self.serdev.timeout          = 3.0  #sec
      self.serdev.xonxoff          = False 
      self.serdev.rtscts           = False
      self.serdev.writeTimeout     = None
      self.serdev.dsrdtr           = False
      self.serdev.interCharTimeout = None
      self.serdev.open()
    except:
      msg = "Failed to open the serial port: {0}".format(self.device)
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.error("{0}".format(msg))
# ================================================================================

class spillNb(QtGui.QWidget):

  def __init__(self):
    super(spillNb, self).__init__() 
    self.initUI()
  
  def initUI(self):

    setup = Setup.Setup()

    # Histogram
    self.pic = QtGui.QLabel("histgram",self)
    self.pic.setGeometry(0,0,600,500)
    self.pic.setPixmap(QtGui.QPixmap(setup.SPILL_PIC))

    self.timer = QtCore.QTimer(self)
    self.timer.timeout.connect(self.changePic)
    self.timer.start(setup.SPILL_TIME_PLOT)

    #Thread for reading
    self.thread_read = ReadThread(self)
    self.thread_read.start()

    # layout
    layout = QtGui.QGridLayout(self)
    layout.addWidget(self.pic  ,0,0)

  def changePic(self):
    setup = Setup.Setup()
    cmd = "nohup {0} > /dev/null 2>&1 &".format(setup.SPILL_PLOT)
    subprocess.call(cmd,shell=True)
    time.sleep(0.5)
    picname= setup.SPILL_PIC
    self.pic.setPixmap(QtGui.QPixmap(picname))

  # ================================
  # App manipulation 
  def quitApp(self):
    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to quit?", QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if reply == QtGui.QMessageBox.Yes:
      QtGui.QApplication.quit()
