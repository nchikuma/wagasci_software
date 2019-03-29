#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime, math
import serial, binascii
import threading
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

# ================================================================================

class ZupClass(QtGui.QWidget):

  # Class variables
  current_adr = "1"
  current_cmd = "ADR"
  current_var = "1"
  recved_cmd  = ""
  isRecved = False

  def set_current_adr(self,var=""): ZupClass.current_adr=var 
  def set_current_cmd(self,var=""): ZupClass.current_cmd=var 
  def set_current_var(self,var=""): ZupClass.current_var=var 
  def set_recved_cmd (self,var=""): ZupClass.recved_cmd=var 
  def set_isRecved(self,var=False): ZupClass.isRecved=var
  def setup_cmd(self,adr="",cmd="",var=""):
    if self.isValid_format(adr,cmd,var):
      self.set_current_adr(adr)
      self.set_current_cmd(cmd)
      self.set_current_var(var)
      isOK = True
    else: isOK = False
    return isOK

  def isValid_format(self,adr="",cmd="",var="",isTx=True):
    setup = Setup.Setup()
    index = -1
    if adr in setup.LAMBDA_ADDR_LIST: index = setup.LAMBDA_ADDR_LIST.index(adr)
    else:
      msg = "Unknown address"
      QtGui.QMessageBox.warning(self, "Warning",msg)
      return False
    var_split = var.split(".")
    res = True
    form = ""
    if isTx:
      if cmd in setup.LAMBDA_SET_CMD_LIST:
        form = setup.LAMBDA_SET_CMD_FORM[setup.LAMBDA_SET_CMD_LIST.index(cmd)][index]
        form_split = form.split(".")
        if not len(var_split)==len(form_split): res = False
        else:
          for i in range(len(form_split)):
            if   not len(var_split[i])==len(form_split[i]): res = False
            elif not str(var_split[i]).isdigit()          : res = False
      else:
        if not var=="": res = False
    else:
      if cmd in setup.LAMBDA_CHECK_CMD_LIST:
        form = setup.LAMBDA_CHECK_RES_FORM[setup.LAMBDA_CHECK_CMD_LIST.index(cmd)][index]
        form_split = form.split(".")
        if not len(var_split)==len(form_split): res = False
        for i in range(len(form_split)):
          if   not len(var_split[i])==len(form_split[i]): res = False
          elif not str(var_split[i]).isdigit()          : res = False
      else:
        if not var=="": res = False
    if not res:
      msg = "Invalid variable format.<adr,cmd,var>=<{0},{1},{2}>"\
             .format(adr,cmd,form)
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.error("{0}".format(msg))
      res = False
    return res
 
# ================================================================================

class ReadThread(QtCore.QThread):

  recved_cmd = QtCore.pyqtSignal(str)
  serdev = serial.Serial()
  mutex = QtCore.QMutex()

  def __init__(self,parent=None):
    super(ReadThread,self).__init__(parent)
    self.stopped = True
    self.last_st = 0.0

  def run(self):
    setup = Setup.Setup()
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("ReadThread is running")
    while not self.stopped:
      if not self.stopped:
        self.cmd_rx()
        self.finished.emit()
      else:
        break
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.warning("ReadThread is stopped")
    
  def stop(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = True
   
  def setup(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = False
  
  def cmd_rx(self):
    zup = ZupClass()
    res_cmd = self.serdev.readline()
    if res_cmd != "":
      self.recved_cmd.emit(res_cmd)
      zup.set_recved_cmd(res_cmd)

 # ================================================================================

class VolCtrl(QtGui.QWidget):

  def __init__(self,parent=None,adr="",vol="",cur=""):
    super(VolCtrl,self).__init__(parent) 
    self.initUI(parent,adr,vol,cur)
  
  def initUI(self,parent,adr,vol,cur):
    setup = Setup.Setup()

    self.adrvalue = adr
    self.volvalue = ""
    self.vol_set  = vol 
    if adr==setup.LAMBDA_HV_ADDR :self.cur_set  = str(float(cur)+0.0001)
    else: self.cur_set = cur
    self.outputON = False
    self.thread_rampup   = threading.Thread()
    self.thread_rampdown = threading.Thread()

  def setZeroVol(self,parent=None):
    setup = Setup.Setup()
    if parent.status.thread_check.isAlive() or\
       parent.thread_status.isAlive() or\
       parent.HVoutput.volctrl.thread_rampup.isAlive() or\
       parent.HVoutput.volctrl.thread_rampdown.isAlive() or\
       parent.LVoutput.volctrl.thread_rampup.isAlive() or\
       parent.LVoutput.volctrl.thread_rampdown.isAlive():
      msg = "Anohter thread is running. Wait for it finished."
      QtGui.QMessageBox.warning(self,"Error",msg)
      return
    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to set 0V and switch OFF?",
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if reply == QtGui.QMessageBox.No: return
    zup = ZupClass()
    if   self.adrvalue==setup.LAMBDA_HV_ADDR: var=["00.0","00.00","00.0"]
    elif self.adrvalue==setup.LAMBDA_LV_ADDR: var=["0.00","0.000","0.00"]
    if zup.setup_cmd(self.adrvalue,"UVP",var[0]): parent.cmd_tx()
    if zup.setup_cmd(self.adrvalue,"VOL",var[1]): parent.cmd_tx()
    if zup.setup_cmd(self.adrvalue,"OVP",var[2]): parent.cmd_tx()
    if zup.setup_cmd(self.adrvalue,"OUT","0"   ): parent.cmd_tx()
    self.outputON = False

  def setvolvalue(self,var=""): self.vol_set = var
  def setcurvalue(self,var=""): self.cur_set = var

  def ctrlVoltage(self,parent=None,ramp="+"):
    setup = Setup.Setup()
    if parent.status.thread_check.isAlive() or\
       parent.thread_status.isAlive() or\
       parent.HVoutput.volctrl.thread_rampup.isAlive() or\
       parent.HVoutput.volctrl.thread_rampdown.isAlive() or\
       parent.LVoutput.volctrl.thread_rampup.isAlive() or\
       parent.LVoutput.volctrl.thread_rampdown.isAlive():
      msg = "Anohter thread is running. Wait for it finished."
      QtGui.QMessageBox.warning(self,"Error",msg)
      return
    elif not ramp in ["+","-"]:
      msg = "ctrlVoltage: select ramp value: '+' or '-'"
      QtGui.QMessageBox.warning(self,"Error",msg)
      return
    elif not parent.thread_read.isRunning():
      msg = "RX Thread is not running."
      QtGui.QMessageBox.warning(self,"Error",msg)
      return
    elif ramp == "-":
      adr = self.adrvalue
      tmp = parent.getStatus("OUT?",adr)
      if   tmp=="1": self.outputON=True
      elif tmp=="0": self.outputON=False
      else: return

      self.volvalue = parent.getStatus("VOL!",adr)
      if self.volvalue=="": return

      if   (not self.outputON) and (not float(self.volvalue)==0.0):
        msg = "Output is already OFF, but VOL is not set 0.0V\n Do you want to set 0.0V?"
      elif (not self.outputON) and (float(self.volvalue)==0.0):
        msg = "Output is OFF, and VOL is set 0.0V.\nNothing will be done."
        QtGui.QMessageBox.information(self, "Information",msg)
        return
      else: #self.outputON==True
        msg = "Output is now ON.\nAre you sure to decrease {0}V -> 0.0V, and to switch OFF?".format(self.volvalue)
      reply = QtGui.QMessageBox.question(self, 'Message',msg,
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
      if reply == QtGui.QMessageBox.No: return

      self.thread_rampdown = threading.Thread(target=self.rampVoldown,args=(parent,adr,))
      self.thread_rampdown.start()

    elif ramp == "+":
      adr = self.adrvalue
      tmp = parent.getStatus("OUT?",adr)
      if   tmp=="1": self.outputON=True
      elif tmp=="0": self.outputON=False
      else: return
      
      self.volvalue = parent.getStatus("VOL!",adr)
      if self.volvalue=="": return

      if   (not self.outputON) and (not float(self.volvalue)==0.0):
        msg = "Output is OFF, but VOL is not set 0.0V.\nAre you sure to set 0V first, to switch ON,\nand then to increase 0V -> {0}V?".format(self.vol_set)
      elif (not self.outputON) and (float(self.volvalue)==0.0):
        msg = "Output is OFF, and VOL is set 0.0V.\nAre you sure to switch ON first,\nand then to increase {0}V -> {1}V?".format(self.volvalue,self.vol_set)
      elif (self.outputON)     and (float(self.volvalue)>=0.0) and (float(self.volvalue)<float(self.vol_set)):
        msg = "Output is already ON.\n \
        Are you sure to increase {0}V -> {1}V?".format(self.volvalue,self.vol_set)
      elif (self.outputON)     and (float(self.volvalue)<float(self.vol_set)+setup.LAMBDA_VOL_DIFF_LIM):
        msg = "Output is already ON, and VOL is set {0}\nNothing will be done".format(self.volvalue)
        QtGui.QMessageBox.warning(self, "Warning",msg)
        return
      else:
        msg = "Too large voltage({0}V).\nIf it was not intended, Set 0V and check the hardware.".format(self.volvalue)
        QtGui.QMessageBox.critical(self, "Error",msg)
        return
      reply = QtGui.QMessageBox.question(self, 'Message',msg,
        QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
      if reply == QtGui.QMessageBox.No: return

      self.thread_rampup = threading.Thread(target=self.rampVolup,args=(parent,adr,))
      self.thread_rampup.start()
  
  def rampVolup(self,parent=None,adr="1"):
    setup = Setup.Setup()
    if   adr==setup.LAMBDA_HV_ADDR: parent.stateHV="RUN"
    elif adr==setup.LAMBDA_LV_ADDR: parent.stateLV="RUN"
    zup = ZupClass()
    setVol = float(self.vol_set)
    isSuccess = False
    if not self.SetAndCheck(parent,adr,"CUR",self.cur_set):
      if   adr==setup.LAMBDA_HV_ADDR: parent.stateHV="ERR"
      elif adr==setup.LAMBDA_LV_ADDR: parent.stateLV="ERR"
      isSuccess = False
    else:
      while True:
        if (not self.outputON) and (not float(self.volvalue)==0.0):
          tmp = ["%05.3f"%(0.0),"%05.2f"%(0.0)]
          if not self.SetAndCheck(parent,adr,"VOL",tmp[setup.LAMBDA_ADDR_LIST.index(adr)]): break
          else: self.volvalue=tmp[setup.LAMBDA_ADDR_LIST.index(adr)]
        elif (not self.outputON) and (float(self.volvalue)==0.0):
          if not self.SetAndCheck(parent,adr,"OUT","1"): break
          else: self.outputON=True
        elif (self.outputON) and (float(self.volvalue)>=0.0) and (float(self.volvalue)<setVol):
          tmpVol = float(self.volvalue)
          loopDone  = False
          while True:
            if loopDone: break
            else       : tmpVol += setup.LAMBDA_VOL_STEP[setup.LAMBDA_ADDR_LIST.index(adr)]
            if tmpVol > setVol: 
              tmpVol = setVol
              loopDone = True
            tmpOvp = tmpVol*(1.+setup.LAMBDA_VOL_PROTECT) 
            tmpUvp = tmpVol*(1.-setup.LAMBDA_VOL_PROTECT) 
            if tmpUvp < 0.: tmpUvp = 0.
            if   adr==setup.LAMBDA_HV_ADDR: varstr=["%04.1f"%(tmpOvp),"%05.2f"%(tmpVol),"%04.1f"%(tmpUvp)]
            elif adr==setup.LAMBDA_LV_ADDR: varstr=["%04.2f"%(tmpOvp),"%05.3f"%(tmpVol),"%04.2f"%(tmpUvp)]
            if not self.SetAndCheck(parent,adr,"OVP",varstr[0]): break
            if not self.SetAndCheck(parent,adr,"VOL",varstr[1]): break
            if not self.SetAndCheck(parent,adr,"UVP",varstr[2]): break
          isSuccess = loopDone
          break
        elif (self.outputON) and (float(self.volvalue)<setVol+setup.LAMBDA_VOL_DIFF_LIM):
          isSuccess = True
          break
        else: 
          break
      #while
      if self.outputON:outputstr="ON " 
      else:outputstr="OFF"
      if adr==setup.LAMBDA_HV_ADDR:
        parent.status.le9.setText("OUTPUT {0}".format(outputstr))
        parent.status.le1.setText("VOL:{0}V".format(parent.getStatus("VOL?",adr)))
        parent.status.le2.setText("CUR:{0}A".format(parent.getStatus("CUR?",adr)))
      elif adr==setup.LAMBDA_LV_ADDR:
        parent.status.le10.setText("OUTPUT {0}".format(outputstr))
        parent.status.le5 .setText("VOL:{0}V".format(parent.getStatus("VOL?",adr)))
        parent.status.le6 .setText("CUR:{0}A".format(parent.getStatus("CUR?",adr)))
      self.volvalue = parent.getStatus("VOL!",adr)
    #if not self.SetAndCheck("CUR") => else

    if isSuccess:
      if   adr==setup.LAMBDA_HV_ADDR: 
        parent.isHVset=True
        parent.stateHV="OK"
      elif adr==setup.LAMBDA_LV_ADDR: 
        parent.isLVset=True
        parent.stateLV="OK"
    else:
      if   adr==setup.LAMBDA_HV_ADDR: parent.stateHV="ERR"
      elif adr==setup.LAMBDA_LV_ADDR: parent.stateLV="ERR"
    return isSuccess

  def rampVoldown(self,parent=None,adr="1"):
    setup = Setup.Setup()
    if   adr==setup.LAMBDA_HV_ADDR: parent.stateHV="RUN"
    elif adr==setup.LAMBDA_LV_ADDR: parent.stateLV="RUN"
    zup = ZupClass()
    setVol = float(self.vol_set)
    isSuccess = False
    if (not self.outputON) and (not float(self.volvalue)==0.0):
      tmp = ["%05.3f"%(0.0),"%05.2f"%(0.0)]
      if zup.setup_cmd(adr,"VOL",tmp[setup.LAMBDA_ADDR_LIST.index(adr)]): 
        parent.cmd_tx()
        isSuccess = True
    elif (not self.outputON) and (float(self.volvalue)==0.0):
      isSuccess = True
    else: #self.outputON==True
      tmpVol = float(self.volvalue)
      loopDone  = False
      while True:
        if loopDone: break
        else       : tmpVol -= setup.LAMBDA_VOL_STEP[setup.LAMBDA_ADDR_LIST.index(adr)]
        if tmpVol < 0.0: 
          tmpVol = 0.0
          loopDone = True
        if tmpVol==0.0: tmpOvp = 2.5
	else          : tmpOvp = tmpVol*(1.+setup.LAMBDA_VOL_PROTECT)
        tmpUvp = tmpVol*(1.-setup.LAMBDA_VOL_PROTECT) 
        if   adr==setup.LAMBDA_HV_ADDR: varstr=["%04.1f"%(tmpOvp),"%05.2f"%(tmpVol),"%04.1f"%(tmpUvp)]
        elif adr==setup.LAMBDA_LV_ADDR: varstr=["%04.2f"%(tmpOvp),"%05.3f"%(tmpVol),"%04.2f"%(tmpUvp)]
        if not self.SetAndCheck(parent,adr,"UVP",varstr[2]): break
        if not self.SetAndCheck(parent,adr,"VOL",varstr[1]): break
        if not self.SetAndCheck(parent,adr,"OVP",varstr[0]): break
      if loopDone:
        if zup.setup_cmd(adr,"OUT","0"):
          parent.cmd_tx()
          isSuccess = True
          self.outputON = False

    if self.outputON:outputstr="ON " 
    else:outputstr="OFF"
    if adr==setup.LAMBDA_HV_ADDR:
      parent.status.le9.setText("OUTPUT {0}".format(outputstr))
      parent.status.le1.setText("VOL:{0}V".format(parent.getStatus("VOL?",adr)))
      parent.status.le2.setText("CUR:{0}A".format(parent.getStatus("CUR?",adr)))
    elif adr==setup.LAMBDA_LV_ADDR:
      parent.status.le10.setText("OUTPUT {0}".format(outputstr))
      parent.status.le5 .setText("VOL:{0}V".format(parent.getStatus("VOL?",adr)))
      parent.status.le6 .setText("CUR:{0}A".format(parent.getStatus("CUR?",adr)))
    self.volvalue = parent.getStatus("VOL!",adr)
    
    if isSuccess:
      if   adr==setup.LAMBDA_HV_ADDR: 
        parent.isHVset=False
        parent.stateHV="WAIT"
      elif adr==setup.LAMBDA_LV_ADDR: 
        parent.isLVset=False
        parent.stateLV="WAIT"
    else:
      if   adr==setup.LAMBDA_HV_ADDR: parent.stateHV="ERR"
      elif adr==setup.LAMBDA_LV_ADDR: parent.stateLV="ERR"
    return isSuccess

  def SetAndCheck(self,parent=None,adr="",cmd="",var=""):
    setup = Setup.Setup()
    isOK = False
    if not (cmd in ["OUT","VOL","OVP","UVP","CUR"]): isOK=False
    else:
      i=0
      zup = ZupClass()
      while True:
        if i>setup.LAMBDA_NUMREP_CHECK:
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.error("SetAndCheck: Failed {0} times to set value <{1},{2},{3}>"\
              .format(setup.LAMBDA_NUMREP_CHECK,adr,cmd,var))
          isOK=False
          break
        elif zup.setup_cmd(adr,cmd,var): 
          parent.cmd_tx()
          if (cmd in ["CUR"]):
            res = parent.getStatus("{0}!".format(cmd),adr)
            if adr==setup.LAMBDA_HV_ADDR:
              if (float(res)<=float(var)) and (float(res)>=(float(var)-0.0007)): 
                isOK=True
                break
              else: i+=1
            else: #LV
              if math.fabs(float(res)-float(var))<=float(var)*0.1: 
                isOK=True
                break
              else: i+=1
          else:
            res = parent.getStatus("{0}?".format(cmd),adr)
            if(cmd in ["VOL","OVP","UVP"]) and (math.fabs(float(res)-float(var))<=setup.LAMBDA_VOL_DIFF_LIM): 
              isOK=True
              break
            elif cmd=="OUT" and int(res)==int(var): 
              isOK=True
              break
            else: i+=1
        else: 
          isOK=False
          i+=1
    return isOK

 # ================================================================================

class HVOutputControl(QtGui.QWidget):

  def __init__(self,parent=None):
    super(HVOutputControl, self).__init__(parent) 
    self.initUI(parent)
  
  def initUI(self,parent):
    setup = Setup.Setup()

    self.volctrl = VolCtrl(parent,setup.LAMBDA_HV_ADDR,setup.LAMBDA_NOMINAL_HVV,setup.LAMBDA_NOMINAL_HVI)

    self.le1 = QtGui.QLineEdit(self.volctrl.vol_set,self)
    self.le2 = QtGui.QLineEdit(setup.LAMBDA_NOMINAL_HVI,self)
    self.label1 = QtGui.QLabel("V",self)
    self.label2 = QtGui.QLabel("A",self)
    self.btn  = QtGui.QPushButton("Ramp Up",self)
    self.btn2 = QtGui.QPushButton("Ramp Down",self)
    self.btn3 = QtGui.QPushButton("Set 0V ",self)

    self.le1.textChanged[str].connect(self.volctrl.setvolvalue)
    self.le2.setReadOnly(True)
    self.btn .clicked.connect(lambda: self.volctrl.ctrlVoltage(parent,"+"))
    self.btn2.clicked.connect(lambda: self.volctrl.ctrlVoltage(parent,"-"))
    self.btn3.clicked.connect(lambda: self.volctrl.setZeroVol (parent))
     
    layout = QtGui.QGridLayout(self)
    layout.addWidget(self.le1    ,0,0)
    layout.addWidget(self.le2    ,1,0)
    layout.addWidget(self.label1 ,0,1)
    layout.addWidget(self.label2 ,1,1)
    layout.addWidget(self.btn    ,0,2)
    layout.addWidget(self.btn2   ,1,2)
    layout.addWidget(self.btn3   ,2,2)
    #layout.setColumnStretch(0,3)
    #layout.setColumnStretch(1,1)
    #layout.setColumnStretch(2,3)
    self.gbox = QtGui.QGroupBox("HV Output ctrl")
    self.gbox.setLayout(layout)
    #self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
    self.resize(setup.LAMBDA_CTRL_SIZE_X*0.1,setup.LAMBDA_CTRL_SIZE_Y*0.1)



  
# ================================================================================

class LVOutputControl(QtGui.QWidget):

  def __init__(self,parent=None):
    super(LVOutputControl, self).__init__(parent) 
    self.initUI(parent)
  
  def initUI(self,parent):
    setup = Setup.Setup()

    self.volctrl = VolCtrl(parent,setup.LAMBDA_LV_ADDR,setup.LAMBDA_NOMINAL_LVV,setup.LAMBDA_MAX_LVI)

    self.le1 = QtGui.QLineEdit(self.volctrl.vol_set,self)
    self.le2 = QtGui.QLineEdit(self.volctrl.cur_set,self)
    self.label1 = QtGui.QLabel("V",self)
    self.label2 = QtGui.QLabel("A",self)
    self.btn  = QtGui.QPushButton("Ramp Up",self)
    self.btn2 = QtGui.QPushButton("Ramp Down",self)
    self.btn3 = QtGui.QPushButton("Set 0V",self)

    self.le1.textChanged[str].connect(self.volctrl.setvolvalue)
    self.le2.textChanged[str].connect(self.volctrl.setcurvalue)
    self.btn .clicked.connect(lambda: self.volctrl.ctrlVoltage(parent,"+"))
    self.btn2.clicked.connect(lambda: self.volctrl.ctrlVoltage(parent,"-"))
    self.btn3.clicked.connect(lambda: self.volctrl.setZeroVol (parent))
       
    layout = QtGui.QGridLayout(self)
    layout.addWidget(self.le1    ,0,0)
    layout.addWidget(self.le2    ,1,0)
    layout.addWidget(self.label1 ,0,1)
    layout.addWidget(self.label2 ,1,1)
    layout.addWidget(self.btn    ,0,2)
    layout.addWidget(self.btn2   ,1,2)
    layout.addWidget(self.btn3   ,2,2)
    #layout.setColumnStretch(0,3)
    #layout.setColumnStretch(1,1)
    #layout.setColumnStretch(2,3)
    self.gbox = QtGui.QGroupBox("LV Output ctrl")
    self.gbox.setLayout(layout)
    #self.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding)
    self.resize(setup.LAMBDA_CTRL_SIZE_X*0.1,setup.LAMBDA_CTRL_SIZE_Y*0.1)


# ================================================================================

class StatusTable(QtGui.QWidget):

  def __init__(self,parent=None):
    super(StatusTable, self).__init__(parent) 
    self.initUI(parent)
  
  def initUI(self,parent):
    setup = Setup.Setup()
    self.thread_check = threading.Thread()
    self.timelabel = QtGui.QLabel("",self)
    self.le1  = QtGui.QLineEdit(self)
    self.le2  = QtGui.QLineEdit(self)
    self.le5  = QtGui.QLineEdit(self)
    self.le6  = QtGui.QLineEdit(self)
    self.le9  = QtGui.QLineEdit(self)
    self.le10 = QtGui.QLineEdit(self)
    self.le1 .setReadOnly(True)
    self.le2 .setReadOnly(True)
    self.le5 .setReadOnly(True)
    self.le6 .setReadOnly(True)
    self.le9 .setReadOnly(True)
    self.le10.setReadOnly(True)

    self.btn1 = QtGui.QPushButton("Check now",self)
    self.btn1.clicked.connect(lambda: self.check_thread(parent))
    self.btn2 = QtGui.QPushButton("Monitoring : Stopped ",self)
    self.btn2.setStyleSheet("background-color: %s"%(setup.LAMBDA_COL_BTN_OFF))
    self.btn2.clicked.connect(parent.btnclick_timer)

    layout1 = QtGui.QGridLayout(self)
    layout1.addWidget(self.le9,0,0)
    layout1.addWidget(self.le1,0,1)
    layout1.addWidget(self.le2,1,1)

    self.gbox1 = QtGui.QGroupBox("HV Status")
    self.gbox1.setLayout(layout1)
    layout2 = QtGui.QGridLayout(self)
    layout2.addWidget(self.le10,0,0)
    layout2.addWidget(self.le5 ,0,1)
    layout2.addWidget(self.le6 ,1,1)
    self.gbox2 = QtGui.QGroupBox("LV Status")
    self.gbox2.setLayout(layout2)
    layout = QtGui.QGridLayout(self)
    layout.addWidget(self.timelabel,0,0)
    layout.addWidget(self.gbox1,1,0,1,2)
    layout.addWidget(self.gbox2,1,2,1,2)
    layout.addWidget(self.btn1 ,0,2)
    layout.addWidget(self.btn2 ,0,3)
    self.gbox = QtGui.QGroupBox("Status table")
    self.gbox.setLayout(layout)
    
    parent.stateHV = "WAIT"
    parent.stateLV = "WAIT"

  def check_thread(self,parent=None):
    if not parent.thread_read.isRunning():
      msg = "RX Thread is not running."
      QtGui.QMessageBox.warning(self,"Error",msg)
      return
    if parent.status.thread_check.isAlive() or\
       parent.thread_status.isAlive() or\
       parent.HVoutput.volctrl.thread_rampup.isAlive() or\
       parent.HVoutput.volctrl.thread_rampdown.isAlive() or\
       parent.LVoutput.volctrl.thread_rampup.isAlive() or\
       parent.LVoutput.volctrl.thread_rampdown.isAlive():
      msg = "Anohter thread is running. Wait for it finished."
      QtGui.QMessageBox.warning(self,"Error",msg)
      return
    self.thread_check = threading.Thread(target=self.check_status,args=(parent,))
    self.thread_check.start()

  def check_status(self,parent=None):
    setup = Setup.Setup()
    if parent.getStatus("OUT?",setup.LAMBDA_HV_ADDR)=="0":outputstr="OFF" 
    else:outputstr="ON "
    self.le9.setText("OUTPUT {0}".format(outputstr))
    self.le1.setText("VOL:{0}V".format(parent.getStatus("VOL?",setup.LAMBDA_HV_ADDR)))
    self.le2.setText("CUR:{0}A".format(parent.getStatus("CUR?",setup.LAMBDA_HV_ADDR)))
    if parent.getStatus("OUT?",setup.LAMBDA_LV_ADDR)=="0":outputstr="OFF" 
    else:outputstr="ON "
    parent.status.le10.setText("OUTPUT {0}".format(outputstr))
    self.le5.setText("VOL:{0}V".format(parent.getStatus("VOL?",setup.LAMBDA_LV_ADDR)))
    self.le6.setText("CUR:{0}A".format(parent.getStatus("CUR?",setup.LAMBDA_LV_ADDR)))
    d = datetime.datetime.today()
    self.timestr = d.strftime("%Y-%m-%d %H:%M:%S")
    self.timelabel.setText(self.timestr)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("Status is checked.")
 
# ================================================================================

class BasicCmd(QtGui.QWidget):

  def __init__(self,parent=None):
    super(BasicCmd, self).__init__(parent) 
    self.initUI(parent)
  
  def initUI(self,parent):
    setup = Setup.Setup()
    self.adr = "1"
    self.cmd = "ADR"
    self.var = "1"
    self.combo1 = QtGui.QComboBox(self)
    self.combo1.addItems(setup.LAMBDA_CMD_LIST)
    self.combo1.activated.connect(self.btn_enable)
    self.combo1.activated.connect(self.setformat)
    self.combo2 = QtGui.QComboBox(self)
    self.combo2.addItems(setup.LAMBDA_ADDR_LIST)
    self.combo2.activated.connect(self.btn_enable)
    self.combo2.activated.connect(self.setformat)
    self.le = QtGui.QLineEdit(self)
    self.le.setMaxLength(10)
    self.le.setTextMargins(0,0,0,0)
    self.le.textChanged.connect(self.btn_enable)
    self.btn = QtGui.QPushButton("Send",self)
    self.btn.clicked.connect(lambda: self.sendBasicCmd(parent))
    self.editor1 = QtGui.QLineEdit(self)
    self.editor2 = QtGui.QLineEdit(self)
    self.editor1.setReadOnly(True)        
    self.editor2.setReadOnly(True)        
    self.editor1.setTextMargins(0,0,0,0)
    self.editor2.setTextMargins(0,0,0,0)


    layout = QtGui.QGridLayout(self)
    layout.addWidget(self.combo2,0,0)
    layout.addWidget(self.combo1,0,1)
    layout.addWidget(self.le    ,0,2)
    layout.addWidget(self.btn   ,1,2)
    layout.addWidget(self.editor1,1,0,1,2)
    layout.addWidget(self.editor2,2,0,1,2)
    layout.setColumnStretch(0,1)
    layout.setColumnStretch(1,1)
    self.gbox = QtGui.QGroupBox("Basic Cmd")
    self.gbox.setLayout(layout)

  def sendBasicCmd(self,parent):
    if parent.status.thread_check.isAlive() or\
       parent.thread_status.isAlive() or\
       parent.HVoutput.volctrl.thread_rampup.isAlive() or\
       parent.HVoutput.volctrl.thread_rampdown.isAlive() or\
       parent.LVoutput.volctrl.thread_rampup.isAlive() or\
       parent.LVoutput.volctrl.thread_rampdown.isAlive():
      msg = "Anohter thread is running. Wait for it finished."
      QtGui.QMessageBox.warning(self,"Error",msg)
      return
    zup = ZupClass()
    self.adr = self.combo2.currentText()
    self.cmd = self.combo1.currentText()
    self.var = self.le.text()
    if zup.setup_cmd(self.adr,self.cmd,self.var): parent.cmd_tx()

  def btn_enable(self):
    self.btn.setEnabled(True)

  def setformat(self):
    setup = Setup.Setup()
    self.adr = self.combo2.currentText()
    self.cmd = self.combo1.currentText()
    if   self.adr==setup.LAMBDA_LV_ADDR: index=0
    elif self.adr==setup.LAMBDA_HV_ADDR: index=1
    else:
      msg = "Unknown address"
      QtGui.QMessageBox.warning(self, "Warning",msg)
      return
    if self.cmd in setup.LAMBDA_SET_CMD_LIST:
      self.var = setup.LAMBDA_SET_CMD_FORM[setup.LAMBDA_SET_CMD_LIST.index(self.cmd)][index]
      self.le.setEnabled(True)
      self.le.setText(self.var)
    else:
      self.var = ""
      self.le.setText(self.var)
      self.le.setEnabled(False)
  
# ================================================================================
  
class SetButton( QtGui.QWidget ):
  def __init__( self, parent=None ):
    super( SetButton, self ).__init__( parent )
    self.initUI(parent)

  def initUI(self,parent):
    setup = Setup.Setup()
    self.btn1 = QtGui.QPushButton('Serial Port : Disconnected',self)
    self.btn1.setStyleSheet("background-color: %s"%(setup.LAMBDA_COL_BTN_OFF))
    self.btn1.clicked.connect(parent.setserial)
    self.btn3 = QtGui.QPushButton("Monitoring : Stopped ",self)
    self.btn3.setStyleSheet("background-color: %s"%(setup.LAMBDA_COL_BTN_OFF))
    self.btn3.clicked.connect(parent.btnclick_timer)


    layout = QtGui.QGridLayout( self )
    layout.addWidget(self.btn1,0,0)
    layout.addWidget(self.btn3,0,1)
    self.gbox = QtGui.QGroupBox()
    self.gbox.setLayout(layout)


# ================================================================================
# Functions : string manipulation 

def insertstr(s="",pos=-1,x=""):
  return x.join([s[:pos],s[pos:]])

def str2ascii(string=""):
  tmp = binascii.hexlify(string)
  for i in xrange(len(tmp)-2, 0, -2):
    tmp = insertstr(tmp,i,'\\x')
  return str('\\x'+tmp)


# ================================================================================

class ps_ctrl(QtGui.QWidget):

  # Class variables
  serdev  = serial.Serial()

  def __init__(self):
    super(ps_ctrl, self).__init__() 
    self.initUI()
  
  def initUI(self):

    setup = Setup.Setup()

    # Serial Port & Baud rate
    self.device = "/dev/ttyS1"
    self.baudrate = 600

    # Variables
    self.status_hvon = ""
    self.status_hv  = "" 
    self.status_hvi = "" 
    self.status_hop = "" 
    self.status_hup = ""
    self.status_lvon = "" 
    self.status_lv  = "" 
    self.status_lvi = "" 
    self.status_lop = "" 
    self.status_lup = ""
    self.isHVset = False 
    self.isLVset = False

    # Check state
    self.stateHV = ""
    self.stateLV = ""
    self.state_timer = QtCore.QTimer(self)
    self.state_timer.timeout.connect(self.setStateColor)
    self.state_timer.start(2000)

    # Widgets
    self.basic    = BasicCmd(self)
    self.status   = StatusTable(self)
    self.HVoutput = HVOutputControl(self)
    self.LVoutput = LVOutputControl(self)
    #self.setbtn   = SetButton(self)  


    #Thread for reading
    self.thread_read = ReadThread(self)
    self.thread_read.recved_cmd.connect(self.RecvCmd)
    self.thread_read.serdev = self.serdev
    #self.setthread()

    #Timer for monitoring
    self.thread_status = threading.Thread()
    self.threads = []
    self.timer = QtCore.QTimer(self)
    self.timer.timeout.connect(self.status_thread)

    self.setserial()
    self.thread_read.setup()
    self.thread_read.start()
    self.btnclick_timer()
    

    # Layout
    self.layout = QtGui.QGridLayout(self)
    #layout.addWidget(self.HVoutput.gbox ,0,0,1,2)
    #layout.addWidget(self.LVoutput.gbox ,0,2,1,2)
    #layout.addWidget(self.status.gbox   ,1,0,1,4)
    #layout.addWidget(self.basic.gbox    ,2,0,1,4)
    #layout.addWidget(self.setbtn.gbox   ,3,1,1,3)
    self.layout.addWidget(self.HVoutput.gbox ,0,0)
    self.layout.addWidget(self.LVoutput.gbox ,0,1)
    self.layout.addWidget(self.status.gbox   ,1,0,1,2)
    self.layout.addWidget(self.basic.gbox    ,2,0,1,2)
    #layout.addWidget(self.setbtn.gbox   ,3,0,1,2)
    #layout.setRowStretch(0,2)
    #layout.setRowStretch(1,2)
    #layout.setRowStretch(2,1)
    self.setLayout(self.layout)
    self.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
    self.resize(setup.LAMBDA_CTRL_SIZE_X*0.3,setup.LAMBDA_CTRL_SIZE_Y*0.3)

  # ================================
  # Commands sender/receiver

  def cmd_tx(self):
    zup =  ZupClass()
    setup = Setup.Setup()

    adr = zup.current_adr
    cmd = zup.current_cmd
    var = zup.current_var

    adrCmd = ":ADR{0};".format(str(adr).zfill(2))
    TxCmd  = ":{0}{1};".format(cmd,var)
    cmd_log = "ADDR = {0}".format(adr) \
      + "/ current_cmd = {0}".format(cmd)\
      + "/ current_var = {0}".format(var)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("cmd_tx: %s"%(cmd_log))
    self.basic.editor1.setText(cmd_log)
    cmd_start = "\\x05\\x02"
    cmd_end   = "\\x03\\x04"
    cmd_tx1 = cmd_start + str2ascii(adrCmd) + cmd_end
    cmd_tx2 = cmd_start + str2ascii(TxCmd)  + cmd_end
    if cmd not in setup.LAMBDA_CMD_LIST:
      msg = zup.current_cmd + " does NOT exist in the cmd list."
      QtGui.QMessageBox.warning(self, "Warning",msg)     
    else:
      if self.serdev.isOpen():
        echo_tmp = "echo -e '{0}' >> {1}".format(cmd_tx1,self.device)
        res = subprocess.Popen(echo_tmp,shell=True)
        res.wait()
        echo_tmp = "echo -e '{0}' >> {1}".format(cmd_tx2,self.device)
        res = subprocess.Popen(echo_tmp,shell=True)
        res.wait()
      else:
        msg = "The serial port is NOT open: {0}".format(self.device)
        QtGui.QMessageBox.warning(self, "Warning",msg)

  def SendCmd(seld,addr="",cmd="",var=""):
      zup = ZupClass()
      zup.setup_cmd(addr,cmd,var)
      self.cmd_tx()
   
  @QtCore.pyqtSlot(str)
  def RecvCmd(self,res_cmd):
    zup =  ZupClass()
    result="ADR{0} {1}".format(str(zup.current_adr).zfill(2),zup.recved_cmd)
    self.basic.editor2.setText(result)
    if not self.thread_read.isRunning():
      self.thread_read.setup()
      self.thread_read.start()


  # ================================
  # Monitoring commands

  def btnclick_timer(self):
    setup = Setup.Setup()
    if self.status.thread_check.isAlive() or\
       self.thread_status.isAlive() or\
       self.HVoutput.volctrl.thread_rampup.isAlive() or\
       self.HVoutput.volctrl.thread_rampdown.isAlive() or\
       self.LVoutput.volctrl.thread_rampup.isAlive() or\
       self.LVoutput.volctrl.thread_rampdown.isAlive():
      msg = "Anohter thread is running. Wait for it finished."
      QtGui.QMessageBox.warning(self,"Error",msg)
      return
    if not self.timer.isActive():
      if self.thread_read.isRunning():
        self.btn_enable(False)
        self.timer.start(setup.LAMBDA_TIME_READ)
        self.status.btn2.setStyleSheet("background-color: %s"%(setup.LAMBDA_COL_BTN_ON))
        self.status.btn2.setText("Monitoring : Running")
        #self.setbtn.btn3.setStyleSheet("background-color: %s"%(setup.LAMBDA_COL_BTN_ON))
        #self.setbtn.btn3.setText("Monitoring : Running")
        #self.setbtn.btn2.setEnabled(False)
      else:
        msg = "RX Thread is not running."
        QtGui.QMessageBox.warning(self,"Error",msg)
        return
    else:
      self.btn_enable(True)
      self.timer.stop()
      self.status.btn2.setStyleSheet("background-color: %s"%(setup.LAMBDA_COL_BTN_OFF))
      self.status.btn2.setText("Monitoring : Stoped ")
      #self.setbtn.btn3.setStyleSheet("background-color: %s"%(setup.LAMBDA_COL_BTN_OFF))
      #self.setbtn.btn3.setText("Monitoring : Stoped ")
      #self.setbtn.btn2.setEnabled(True)

  def status_thread(self):
    setup = Setup.Setup()
    if self.status.thread_check.isAlive() or\
       self.thread_status.isAlive() or\
       self.HVoutput.volctrl.thread_rampup.isAlive() or\
       self.HVoutput.volctrl.thread_rampdown.isAlive() or\
       self.LVoutput.volctrl.thread_rampup.isAlive() or\
       self.LVoutput.volctrl.thread_rampdown.isAlive():
      msg = "Anohter thread is running. Monitoring is skipped this time.\n"
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.warning("%s"%(msg))
      return
    #self.thread_status = threading.Thread(target=self.status_monitor)
    #self.threads.append(self.thread_status)
    #self.thread_status.start()
    self.status_monitor()

  def status_monitor(self):
    setup = Setup.Setup()
    if self.thread_read.isRunning():
      if self.getStatus("OUT?",setup.LAMBDA_HV_ADDR)=="1": self.status_hvon="ON"
      else                                      : self.status_hvon="OFF"
      self.status_hv  = self.getStatus("VOL?",setup.LAMBDA_HV_ADDR)
      self.status_hvi = self.getStatus("CUR?",setup.LAMBDA_HV_ADDR)
      self.status_hop = self.getStatus("OVP?",setup.LAMBDA_HV_ADDR)
      self.status_hup = self.getStatus("UVP?",setup.LAMBDA_HV_ADDR)
      if self.getStatus("OUT?",setup.LAMBDA_LV_ADDR)=="1": self.status_lvon="ON"
      else                                      : self.status_lvon="OFF"
      self.status_lv  = self.getStatus("VOL?",setup.LAMBDA_LV_ADDR)
      self.status_lvi = self.getStatus("CUR?",setup.LAMBDA_LV_ADDR)
      self.status_lop = self.getStatus("OVP?",setup.LAMBDA_LV_ADDR)
      self.status_lup = self.getStatus("UVP?",setup.LAMBDA_LV_ADDR)
      self.status.le9 .setText("OUTPUT {0}".format(self.status_hvon))
      self.status.le1 .setText("VOL:{0}V"  .format(self.status_hv  ))
      self.status.le2 .setText("CUR:{0}A"  .format(self.status_hvi ))
      #self.status.le3 .setText("OVP:{0}V"  .format(self.status_hop ))
      #self.status.le4 .setText("UVP:{0}V"  .format(self.status_hup ))
      self.status.le10.setText("OUTPUT {0}".format(self.status_lvon))
      self.status.le5 .setText("VOL:{0}V"  .format(self.status_lv  ))
      self.status.le6 .setText("CUR:{0}A"  .format(self.status_lvi ))
      #self.status.le7 .setText("OVP:{0}V"  .format(self.status_lop ))
      #self.status.le8 .setText("UVP:{0}V"  .format(self.status_lup ))
      d = datetime.datetime.today()
      self.timestr = d.strftime("%Y-%m-%d %H:%M:%S")
      self.timeutc = d.strftime("%s")
      self.status.timelabel.setText(self.timestr)
      
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("status_monitor: HV=> OUTPUT {0} VOL:{1}V CUR:{2}A OVP:{3}V UVP:{4}V / LV=> OUTPUT {5} VOL:{6}V CUR:{7}A OVP:{8}V UVP:{9}V"\
             .format(self.status_hvon,self.status_hv,self.status_hvi,\
                     self.status_hop,self.status_hup,self.status_lvon,\
                     self.status_lv,self.status_lvi,self.status_lop,self.status_lup))
      if not os.path.isfile(setup.LAMBDA_LOG):
        subprocess.call("echo -e "" > {0}".format(setup.LAMBDA_LOG),shell=True)
      status_values = "{0} {1} {2} {3} {4} {5} {6} {7}".format(\
               self.status_hv,self.status_hvi,self.status_hop,self.status_hup,\
               self.status_lv,self.status_lvi,self.status_lop,self.status_lup)
      cmd="sed -i '1s/^/{0} {1}\\n/' {2}".format(self.timeutc,status_values,setup.LAMBDA_LOG)
      subprocess.call(cmd,shell=True)
      cmd="nohup {0} > /dev/null 2>&1 &".format(setup.LAMBDA_PLOT)
      subprocess.call(cmd,shell=True)
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("New plots are made.")

      if self.status_hvon=="ON": self.isHVset=True 
      if self.status_lvon=="ON": self.isLVset=True

      if self.status_hv =="" or self.status_hvi=="" or\
         self.status_hop=="" or self.status_hup=="" or\
         self.status_lv =="" or self.status_lvi=="" or\
         self.status_lop=="" or self.status_lup=="":
        setup.set_alarm("Lambda PS")
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.warning("!!!!WAGASCI ALARM!!!!!: status_monitor")
          subprocess.call(cmd,shell=True)
        self.stateHV="ERR"
        self.stateLV="ERR"
      elif self.isHVset and self.isLVset:
        if math.fabs(float(self.status_hv )-float(setup.LAMBDA_NOMINAL_HVV))>setup.LAMBDA_LIMIT_DIFF_HVV or\
                     float(self.status_hvi)-float(setup.LAMBDA_NOMINAL_HVI) >setup.LAMBDA_LIMIT_DIFF_HVI or\
           math.fabs(float(self.status_lv )-float(setup.LAMBDA_NOMINAL_LVV))>setup.LAMBDA_LIMIT_DIFF_LVV or\
           math.fabs(float(self.status_lvi)-float(setup.LAMBDA_NOMINAL_LVI))>setup.LAMBDA_LIMIT_DIFF_LVI:
          setup.set_alarm("Lambda PS")
          msg = "Measured: HV->[{0}V,{1}A],LV->[{2}V,{3}A];".format(
              float(self.status_hv ),
              float(self.status_hvi),
              float(self.status_lv ),
              float(self.status_lvi))
          msg +="Allowed: HV->[{0}:{1}], HVi->[{2},{3}], LV->[{4},{5}], LVi->[{6},{7}]".format(
              float(setup.LAMBDA_NOMINAL_HVV)-setup.LAMBDA_LIMIT_DIFF_HVV, 
              float(setup.LAMBDA_NOMINAL_HVV)+setup.LAMBDA_LIMIT_DIFF_HVV,
              float(setup.LAMBDA_NOMINAL_HVI)-setup.LAMBDA_LIMIT_DIFF_HVI, 
              float(setup.LAMBDA_NOMINAL_HVI)+setup.LAMBDA_LIMIT_DIFF_HVI,
              float(setup.LAMBDA_NOMINAL_LVV)-setup.LAMBDA_LIMIT_DIFF_LVV, 
              float(setup.LAMBDA_NOMINAL_LVV)+setup.LAMBDA_LIMIT_DIFF_LVV,
              float(setup.LAMBDA_NOMINAL_LVI)-setup.LAMBDA_LIMIT_DIFF_LVI, 
              float(setup.LAMBDA_NOMINAL_LVI)+setup.LAMBDA_LIMIT_DIFF_LVI)
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.error(msg)
          subprocess.call(cmd,shell=True)
          self.stateHV="ERR"
          self.stateLV="ERR"
        else:
          self.stateHV="OK"
          self.stateLV="OK"
      else:
        self.stateHV="WAIT"
        self.stateLV="WAIT"
    else:
      msg = "RX thread is not running."
      QtGui.QMessageBox.warning(self,"Error",msg)

  def setStateColor(self):
    setup = Setup.Setup()
    if self.stateHV=="OK":
      self.status.gbox1.setStyleSheet("background-color: #%s"%(setup.LAMBDA_COL_STATUS_OK))
    elif self.stateHV=="RUN":
      self.status.gbox1.setStyleSheet("background-color: #%s"%(setup.LAMBDA_COL_STATUS_RUN))
    elif self.stateHV=="WAIT":
      self.status.gbox1.setStyleSheet("background-color: #%s"%(setup.LAMBDA_COL_STATUS_WAIT))
    elif self.stateHV=="ERR":
      self.status.gbox1.setStyleSheet("background-color: #%s"%(setup.LAMBDA_COL_STATUS_ERR))
    else:
      self.status.gbox1.setStyleSheet("")
    if self.stateLV=="OK":
      self.status.gbox2.setStyleSheet("background-color: #%s"%(setup.LAMBDA_COL_STATUS_OK))
    elif self.stateLV=="RUN":
      self.status.gbox2.setStyleSheet("background-color: #%s"%(setup.LAMBDA_COL_STATUS_RUN))
    elif self.stateLV=="WAIT":
      self.status.gbox2.setStyleSheet("background-color: #%s"%(setup.LAMBDA_COL_STATUS_WAIT))
    elif self.stateLV=="ERR":
      self.status.gbox2.setStyleSheet("background-color: #%s"%(setup.LAMBDA_COL_STATUS_ERR))
    else:
      self.status.gbox2.setStyleSheet("")
      
  # ================================
  # App commands

  def setserial(self):
    setup = Setup.Setup()
    try:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("setserial: Target device is {0}".format(self.device))
      if self.serdev.isOpen():
        self.serdev.close()
      ps_ctrl.serdev.port             = self.device
      ps_ctrl.serdev.baudrate         = self.baudrate
      ps_ctrl.serdev.bytesize         = 8    #EIGHTBITS
      ps_ctrl.serdev.parity           = "N"  #PARITY_NONE
      ps_ctrl.serdev.stopbits         = 1    #STOPBITS_ONE
      ps_ctrl.serdev.timeout          = 3.0  #sec
      ps_ctrl.serdev.xonxoff          = True 
      ps_ctrl.serdev.rtscts           = False
      ps_ctrl.serdev.writeTimeout     = None
      ps_ctrl.serdev.dsrdtr           = False
      ps_ctrl.serdev.interCharTimeout = None
      ps_ctrl.serdev.open()
      #self.setbtn.btn1.setStyleSheet("background-color: %s"%(setup.LAMBDA_COL_BTN_ON))
      #self.setbtn.btn1.setText("Port{0}:Connected".format(self.device))
    except:
      #self.setbtn.btn1.setStyleSheet("background-color: %s"%(setup.LAMBDA_COL_BTN_OFF))
      #self.setbtn.btn1.setText("Serial Port : Disconnected")
      msg = "Failed to open the serial port: {0}".format(self.device)
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.error("{0}".format(msg))

  def btn_enable(self,boolean=False):
    self.basic.btn    .setEnabled(boolean)
    self.status.btn1  .setEnabled(boolean)
    self.HVoutput.btn .setEnabled(boolean)
    self.HVoutput.btn2.setEnabled(boolean)
    self.HVoutput.btn3.setEnabled(boolean)
    self.LVoutput.btn .setEnabled(boolean)
    self.LVoutput.btn2.setEnabled(boolean)
    self.LVoutput.btn3.setEnabled(boolean)

  # ================================
  # Checking commands
  def sendCheckCmd(self,cmd="",addr=1):
    setup = Setup.Setup()
    if not cmd in setup.LAMBDA_CHECK_CMD_LIST:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.error("sendCheckCmd: Wrong cmd name for checking the status.\n")
      return
    zup = ZupClass()
    zup.setup_cmd(str(addr),"{0}".format(cmd),"")
    self.cmd_tx()

  def getStatus(self,cmd="",adr="1"):
    setup = Setup.Setup()
    zup = ZupClass()
    i = 0
    result = ""
    while True:
      self.sendCheckCmd(cmd,adr)
      cmd_res = setup.LAMBDA_CHECK_RES_LIST[setup.LAMBDA_CHECK_CMD_LIST.index(cmd)]
      time.sleep(setup.LAMBDA_TIME_TILL_RECV)
      result = zup.recved_cmd
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("getStaus: %s"%(result.strip()))
      if i>setup.LAMBDA_NUMREP_CHECK:
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.error(
            "Error: getStatus: Failed to get correct response from ZUP (ADDR:{0},CMD:{1})"\
            .format(adr,cmd))
        return ""
      elif cmd_res == result[0:2]: break
      else: i+=1
    var_res = str(result[2:-1].replace(" ","").replace("\r",""))
    if zup.isValid_format(adr,cmd,var_res,False): return var_res
    else:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.error(
          "Error: getStatus: response has an invalid variable (ADDR:{0},CMD:{1})"\
          .format(adr,cmd))
      return ""

  # ================================
  # App manipulation 
  def quitApp(self):
    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to quit?", QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if reply == QtGui.QMessageBox.Yes:
      QtGui.QApplication.quit()
