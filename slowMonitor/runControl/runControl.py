#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime, threading
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

# ================================================================================

class runControl( QtGui.QWidget ):
  def __init__( self, parent=None ):
    super( runControl, self ).__init__( parent )
    self.initUI(parent)

  def initUI(self,parent):
    setup = Setup.Setup()

    self.state_wagscirun   = 0
    self.state_calibration = 0
    self.state_internalrun = 0
    self.runid = 0
    self.acqid = 0
    self.calibname = ""
    self.log_totalline = 0
    self.log_lastline  = 0

    self.timer1 = QtCore.QTimer(self)
    self.timer1.timeout.connect(self.check_runid)
    self.timer1.start(5000)
    self.timer2 = QtCore.QTimer(self)
    self.timer2.timeout.connect(self.check_log)
    self.timer2.start(3000)


    self.label1 = QtGui.QLabel("RunID:?????",self)
    self.label2 = QtGui.QLabel("AcqID:???"  ,self)
    self.label3 = QtGui.QLabel("Status WAGASCI Run:%-12s"%("Stopped"),self)
    self.label4 = QtGui.QLabel("Status Calibration:%-12s"%("Stopped"),self)
    self.label1.setGeometry(0,0,10,100)
    self.label2.setGeometry(0,0,10,100)
    self.label3.setGeometry(0,0,10,100)
    self.label4.setGeometry(0,0,10,100)
    self.layout1 = QtGui.QGridLayout()
    self.layout1.addWidget(self.label1,0,0)
    self.layout1.addWidget(self.label2,1,0)
    self.layout1.addWidget(self.label3,0,1)
    self.layout1.addWidget(self.label4,1,1)
    self.gbox1 = QtGui.QGroupBox("")
    self.gbox1.setLayout(self.layout1)

    self.btn1 = QtGui.QPushButton("Start Run"   ,self)
    self.btn2 = QtGui.QPushButton("Calibration" ,self)
    self.btn3 = QtGui.QPushButton("Stop"        ,self)
    self.btn4 = QtGui.QPushButton("Reconfigure" ,self)
    self.btn5 = QtGui.QPushButton("Internal Run",self)

    self.btn1.clicked.connect(self.throw_wagasci_run )
    self.btn2.clicked.connect(self.throw_calibration )
    self.btn3.clicked.connect(self.throw_stop_script )
    self.btn4.clicked.connect(self.throw_reconfigure )
    self.btn5.clicked.connect(self.throw_internal_run)

    self.te = QtGui.QTextEdit("")
    self.te.setReadOnly(True)

    layout = QtGui.QGridLayout( self )
    layout.addWidget(self.gbox1,0,0,1,3)
    layout.addWidget(self.btn1,1,0)
    layout.addWidget(self.btn5,1,1)
    layout.addWidget(self.btn2,1,2)
    layout.addWidget(self.btn3,2,1)
    layout.addWidget(self.btn4,2,0)
    layout.addWidget(self.te  ,3,0,1,3)


  def throw_wagasci_run(self):
    if self.state_wagscirun>0 or self.state_calibration>0:
      QtGui.QMessageBox.information(self, 'Message',"Some other process is running.")
      return

    setup = Setup.Setup()
    cmd = "ssh {0} cat {1}".format(setup.SERV_DAQ,setup.RUNID_FILE)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result = res.communicate()[0].strip()
    runid = int(result)
    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to start wagasci run? \nNext Run ID = %d"%(runid+1), QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if not reply == QtGui.QMessageBox.Yes:
      return
    thread = threading.Thread(target=self.start_wagasci_run)
    thread.start()

  def throw_internal_run(self):
    if self.state_wagscirun>0 or self.state_calibration>0:
      QtGui.QMessageBox.information(self, 'Message',"Some other process is running.")
      return

    setup = Setup.Setup()
    cmd = "ssh {0} cat {1}".format(setup.SERV_DAQ,setup.RUNID_FILE)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result = res.communicate()[0].strip()
    runid = int(result)
    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to start wagasci run? \nNext Run ID = %d"%(runid+1), QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if not reply == QtGui.QMessageBox.Yes:
      return
    thread = threading.Thread(target=self.start_internal_run)
    thread.start()

  def throw_reconfigure(self):
    if self.state_wagscirun>0 or self.state_calibration>0:
      QtGui.QMessageBox.information(self, 'Message',"Some other process is running.")
      return

    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to start reconfigure?", QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if not reply == QtGui.QMessageBox.Yes:
      return
    thread = threading.Thread(target=self.start_reconfigure)
    thread.start()

  def throw_calibration(self):
    if self.state_wagscirun>0 or self.state_calibration>0:
      QtGui.QMessageBox.information(self, 'Message',"Some other process is running.")
      return

    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to start calibration run?", QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if not reply == QtGui.QMessageBox.Yes:
      return
    thread = threading.Thread(target=self.start_calibration)
    thread.start()

  def throw_stop_script(self):
    if self.state_wagscirun==0 and self.state_calibration==0 and self.state_internalrun==0:
      QtGui.QMessageBox.information(self, 'Message',"Nothing is running.")
      return

    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to stop the current run?", QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if not reply == QtGui.QMessageBox.Yes:
      return
    thread = threading.Thread(target=self.stop_script)
    thread.start()

  def check_runid(self):
    setup = Setup.Setup()
    cmd = "ssh {0} cat {1}".format(setup.SERV_DAQ,setup.RUNID_FILE)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    self.runid = int(res.communicate()[0])
    self.label1.setText("RunaID:%05d"%(self.runid))
    cmd = "ssh {0} cat {1}".format(setup.SERV_DAQ,setup.ACQID_FILE)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    self.acqid = int(res.communicate()[0])
    self.label2.setText("AcqID:%03d"%(self.acqid))
    cmd = "ssh {0} ps ux | grep {1} | grep -v grep | wc -l".format(
        setup.SERV_DAQ,setup.WAGASCI_RUN)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    self.state_wagscirun = int(res.communicate()[0])
    if self.state_wagscirun==0:
      self.label3.setText("Status WAGASCI Run:%-12s"%("Stopped"))
      self.label3.setStyleSheet("background-color: yellow")
    elif self.state_wagscirun==1:
      if self.state_internalrun==0:
        self.label3.setText("Status WAGASCI Run:%-12s"%("Running"))
        self.label3.setStyleSheet("background-color: green")
      else:
        self.label3.setText("Status WAGASCI Run:%-12s"%("!!Internal spill!!"))
        self.label3.setStyleSheet("background-color: orange")
    else:
      self.label3.setText("Status WAGASCI Run:%-12s"%("Too many runs"))
      self.label3.setStyleSheet("background-color: red")
    cmd = "ps ux | grep \"/bin/sh {0}\" | grep -v grep | wc -l".format(setup.CALIB_CMD)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    self.state_calibration = int(res.communicate()[0])
    if self.state_calibration==0:
      self.label4.setText("Status Calibration:%-12s"%("Stopped"))
      self.label4.setStyleSheet("background-color: yellow")
    elif self.state_calibration==1:
      self.label4.setText("Status Calibration:%-12s"%("Running"))
      self.label4.setStyleSheet("background-color: green")
    else:
      self.label4.setText("Status Calibration:%-12s"%("Too many runs"))
      self.label4.setStyleSheet("background-color: red")

  def check_log(self):
    setup = Setup.Setup()
    if not os.path.exists(setup.RUNCTRL_LOG):
      with open(setup.RUNCTRL_LOG,"w") as f:
        f.write("")
    cmd = "cat {0} | wc -l".format(setup.RUNCTRL_LOG)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    line = int(res.communicate()[0].strip())
    if line==self.log_lastline:
      return
    elif line<self.log_lastline:
      cmd = "cat {0}".format(setup.RUNCTRL_LOG)
      res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
      result = res.communicate()
      for i in range(len(result)):
        var = result[i]
        if i==0:
          if not var==None: self.te.setText("{0}".format(var))
        else:
          if not var==None: 
            self.te.moveCursor( QtGui.QTextCursor.End )
            self.te.insertPlainText("{0}".format(var))
    else:
      cmd = "sed -n '{0},{1}p' {2}".format(
          self.log_lastline+1,line,setup.RUNCTRL_LOG)
      res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
      for var in res.communicate():
        if not var==None: 
          self.te.moveCursor( QtGui.QTextCursor.End )
          self.te.insertPlainText("{0}".format(var))
    self.log_lastline = line
      
# ================================================================================
  def stop_script(self):
    self.state_internalrun = 0
    setup = Setup.Setup()
    with open(setup.RUNCTRL_LOG,"w") as f:
      f.write("")
    cmd = "ssh {0} python {1} &>> {2}".format(
        setup.SERV_DAQ,setup.STOP_SCRIPT,setup.RUNCTRL_LOG)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("{0}".format(cmd.replace("\n",";")))
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    for var in result:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("{0}".format(var.replace("\n",";")))
 
  def start_wagasci_run(self):
    setup = Setup.Setup()
    with open(setup.RUNCTRL_LOG,"w") as f:
      f.write("")
    cmd = "ssh {0} python {1} &>> {2}".format(
        setup.SERV_DAQ,setup.WAGASCI_RUN,setup.RUNCTRL_LOG)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("{0}".format(cmd.replace("\n",";")))
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    for var in result:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("{0}".format(var.replace("\n",";")))

  def start_internal_run(self):
    self.state_internalrun = 1
    setup = Setup.Setup()
    with open(setup.RUNCTRL_LOG,"w") as f:
      f.write("")
    cmd = "ssh {0} python {1} 20 600 internal &>> {2}".format(
        setup.SERV_DAQ,setup.WAGASCI_RUN,setup.RUNCTRL_LOG)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("{0}".format(cmd.replace("\n",";")))
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    for var in result:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("{0}".format(var.replace("\n",";")))

  def start_reconfigure(self):
    setup = Setup.Setup()
    with open(setup.RUNCTRL_LOG,"w") as f:
      f.write("")
    cmd = "ssh {0} systemctl restart pyrame &>> {1}".format(
        setup.SERV_DAQ,setup.RUNCTRL_LOG)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("{0}".format(cmd.replace("\n",";")))
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    for var in result:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("{0}".format(var.replace("\n",";")))
    cmd = "ssh {0} reconfigure.sh &>> {1}".format(
        setup.SERV_DAQ,setup.RUNCTRL_LOG)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("{0}".format(cmd.replace("\n",";")))
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    for var in result:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("{0}".format(var.replace("\n",";")))

  def start_calibration(self):
    setup = Setup.Setup()
    with open(setup.RUNCTRL_LOG,"w") as f:
      f.write("")
    cmd = "{0} &>> {1}".format(setup.CALIB_CMD,setup.RUNCTRL_LOG)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("{0}".format(cmd.replace("\n",";")))
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    for var in result:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("{0}".format(var.replace("\n",";")))

    cmd = "tail -n 1 {0}".format(setup.RUNCTRL_LOG)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result = res.communicate()[0].strip()
    if not result=="====== DONE. ======":
      self.te.moveCursor( QtGui.QTextCursor.End )
      self.te.insertPlainText("!!!Calibration was not completed.!!!")
      return
    with open(setup.CALIB_ID_FILE,"r") as f:
      line = f.readline().split()
      if len(line)==2:
        self.calibname = line[1]
    picturename="{0}/{1}/image/Gain.png".format(setup.CALIB_DIR,self.calibname)
    if os.path.exists(picturename):
      picture = QtGui.QTextImageFormat()
      picture.setName(picturename)
      picture.setWidth(550)
      textcursor = QtGui.QTextCursor(self.te.textCursor())
      self.te.moveCursor( QtGui.QTextCursor.End )
      textcursor.insertImage(picture)
    else:
      self.te.moveCursor( QtGui.QTextCursor.End )
      self.te.insertPlainText("!!!There is no result image {0}!!!".format(picture))
    picturename="{0}/{1}/image/Gain_pe3.png".format(setup.CALIB_DIR,self.calibname)
    if os.path.exists(picturename):
      picture = QtGui.QTextImageFormat()
      picture.setName(picturename)
      picture.setWidth(550)
      textcursor = QtGui.QTextCursor(self.te.textCursor())
      self.te.moveCursor( QtGui.QTextCursor.End )
      textcursor.insertImage(picture)
    else:
      self.te.moveCursor( QtGui.QTextCursor.End )
      self.te.insertPlainText("!!!There is no result image {0}!!!".format(picture))

    badchannel = "{0}/{1}/bad_channel.txt".format(setup.CALIB_DIR,self.calibname)
    if os.path.exists(badchannel):
      self.te.moveCursor( QtGui.QTextCursor.End )
      self.te.insertPlainText("\n=== Bad Channel List (thres=2pe) ===\n")
      with open(badchannel,"r") as f:
        line = f.readline()
        while line:
          self.te.moveCursor( QtGui.QTextCursor.End )
          self.te.insertPlainText("{0}\n".format(line.strip()))
          line = f.readline()
    else:
      self.te.moveCursor( QtGui.QTextCursor.End )
      self.te.insertPlainText("!!!There is no bad channel list {0}!!!".format(badchannel))

    badchannel = "{0}/{1}/bad_channel_pe3.txt".format(setup.CALIB_DIR,self.calibname)
    if os.path.exists(badchannel):
      self.te.moveCursor( QtGui.QTextCursor.End )
      self.te.insertPlainText("\n===Bad Channel List (thres=3pe)===\n")
      with open(badchannel,"r") as f:
        line = f.readline()
        while line:
          self.te.moveCursor( QtGui.QTextCursor.End )
          self.te.insertPlainText("{0}\n".format(line.strip()))
          line = f.readline()
    else:
      self.te.moveCursor( QtGui.QTextCursor.End )
      self.te.insertPlainText("!!!There is no bad channel list {0}!!!".format(badchannel))
