#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

# ================================================================================
def stop_system(target=-1):
  setup = Setup.Setup()
  if target>len(setup.MANAGER_SYSTEM_LIST): 
    pass
  else:
    cmd = "ps ux | grep \"{0}\" | grep -v \"grep\" | wc -l".\
            format(setup.MANAGER_SYSTEM_LIST[target])
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result = res.communicate()[0].strip()
    if not result.isdigit():
      pass
    else:
      if int(result)!=0:
        cmd = "ps ux | grep \"{0}\" | grep -v \"grep\" | head -n 1".\
               format(setup.MANAGER_SYSTEM_LIST[target])
        res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        result = res.communicate()[0].strip().split()[1]
        if not result.isdigit():
          pass
        else:
          cmd = "kill -9 {0}".format(result)
          subprocess.call(cmd,shell=True)
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.info("Stopped a process: {0}".format(setup.MANAGER_SYSTEM_LIST[target]))
      else:
        pass

def start_system(target=-1):
  setup = Setup.Setup()
  if target>len(setup.MANAGER_SYSTEM_LIST):
    pass
  else:
    cmd = "ps ux | grep \"{0}\" | grep -v \"grep\" | wc -l".\
            format(setup.MANAGER_SYSTEM_LIST[target])
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result = res.communicate()[0].strip()
    if not result.isdigit():
      pass
    else:
      if int(result)==0:
        cmd = "nohup {0} 1>>{1} 2>&1 &".format(setup.MANAGER_SYSTEM_LIST[target],setup.SLOWMONITOR_LOG)
        subprocess.call(cmd,shell=True)
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.info("Started a process: {0}".format(setup.MANAGER_SYSTEM_LIST[target]))
      else:
        pass

def check_system(target=-1):
  setup = Setup.Setup()
  if target>len(setup.MANAGER_SYSTEM_LIST):
    return -1
  else:
    cmd = "ps ux | grep \"{0}\" | grep -v \"grep\" | wc -l".\
            format(setup.MANAGER_SYSTEM_LIST[target])
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result = res.communicate()[0].strip()
    if not result.isdigit():
      return -1
    else:
      return int(result)

def stop_system_all():
  setup = Setup.Setup()
  for process in setup.MANAGER_SYSTEM_LIST:
    cmd = "ps ux | grep \"{0}\" | grep -v \"grep\" | wc -l".\
            format(process)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result = res.communicate()[0].strip()
    if not result.isdigit():
      pass
    else:
      if int(result)!=0:
        cmd = "ps ux | grep \"{0}\" | grep -v \"grep\" | head -n 1".\
               format(process)
        res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
        result = res.communicate()[0].strip().split()[1]
        if not result.isdigit():
          pass
        else:
          cmd = "kill -9 {0}".format(result)
          subprocess.call(cmd,shell=True)
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.info("Stopped a process: {0}".format(process))
      else:
        pass
   

def start_system_all():
  setup = Setup.Setup()
  for process in setup.MANAGER_SYSTEM_LIST:
    cmd = "ps ux | grep \"{0}\" | grep -v \"grep\" | wc -l".\
            format(process)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result = res.communicate()[0].strip()
    if not result.isdigit():
      pass
    else:
      if int(result)==0:
        cmd = "nohup {0} 1>>{1} 2>&1 &".format(process,setup.SLOWMONITOR_LOG)
        subprocess.call(cmd,shell=True)
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.info("Started a process: {0}".format(process))
      else:
        pass


# ================================================================================

class StatusThread(QtCore.QThread):

  mutex = QtCore.QMutex()

  def __init__(self,parent=None,nb_monitor=0):
    super(StatusThread,self).__init__(parent)
    self.state = []
    self.nb_monitor = nb_monitor
    for i in range(self.nb_monitor): self.state.append("Unknown")
    self.stopped = False

  def run(self):
    setup = Setup.Setup()
    while not self.stopped:
      self.checkAll()
      self.finished.emit()
      time.sleep(setup.MANAGER_TIME_STATECHECK) #sec
    
  def stop(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = True
   
  def setup(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = False

  def checkAll(self):
    for i in range(self.nb_monitor):
      state_id = check_system(i)
      if   state_id==-1: self.state[i]="Unknown"
      elif state_id==0 : self.state[i]="Not running"
      elif state_id==1 : self.state[i]="Running"
      elif state_id>1  : self.state[i]="Too many running"
 
# ================================================================================

class systemManager( QtGui.QWidget ):
  def __init__( self, parent=None ):
    super( systemManager, self ).__init__( parent )
    self.initUI(parent)

  def initUI(self,parent):
    setup = Setup.Setup()

    self.nb_monitor = len(setup.MANAGER_SYSTEM_LIST)
    self.btn = []
    for monitor in setup.MANAGER_SYSTEM_NAME:
      self.btn.append(QtGui.QPushButton(monitor,self))
    self.btnstop  = QtGui.QPushButton('Stop All' ,self)
    self.btnstart = QtGui.QPushButton('Start All',self)

    for i in range(self.nb_monitor):
      self.btn[i].clicked.connect(lambda state,x=i: self.monitorCtrl(x))
      #self.btn[i].setText(setup.MANAGER_SYSTEM_NAME[i])
    self.btnstop .clicked.connect(self.stop_all)
    self.btnstart.clicked.connect(self.start_all)


    self.thread_state = StatusThread(self,nb_monitor=self.nb_monitor)
    self.thread_state.finished.connect(self.changeColor)
    self.thread_state.start()


    layout = QtGui.QGridLayout( self )
    for i in range(len(self.btn)):
      x = int(i%2)
      y = int(i/2)
      layout.addWidget(self.btn[i],y,x)
    y = int(len(self.btn)/2)+int(len(self.btn)%2)
    layout.addWidget(self.btnstart ,y,0)
    layout.addWidget(self.btnstop  ,y,1)

  def changeColor(self):
    setup = Setup.Setup()
    for i in range(self.nb_monitor):
      if self.thread_state.state[i]=="Running":
        self.btn[i].setStyleSheet("background-color: %s; color: white"%(
              setup.MANAGER_COL_BTN_OK))
      elif self.thread_state.state[i]=="Not running":
        self.btn[i].setStyleSheet("background-color: %s"%(
              setup.MANAGER_COL_BTN_NG))
      else:
        self.btn[i].setStyleSheet("background-color: %s"%(setup.MANAGER_COL_BTN_UNKNOWN))
    self.btn_enable(True)

  def monitorCtrl(self,i=-1):
    setup = Setup.Setup()
    self.btn_enable(False)
    state_id = check_system(i)
    if   state_id==1: #Running
      stop_system(i)
    elif state_id==0: #Not running  
      start_system(i)
    elif state_id>1: #Too many running 
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.warning("Too many of monitor id={0} are running".format(i))
    else: 
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.warning("Unknown monitor id={0}".format(i))

  def stop_all(self):
    self.btn_enable(False)
    stop_system_all()

  def start_all(self):
    self.btn_enable(False)
    start_system_all()

  def btn_enable(self,enable=True):
    for btn in self.btn: btn.setEnabled(enable)
    self.btnstop.setEnabled(enable)
    self.btnstart.setEnabled(enable)


