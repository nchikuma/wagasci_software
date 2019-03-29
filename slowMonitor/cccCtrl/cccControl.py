#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime
import threading
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup


# ================================================================================

class QuitBottun( QtGui.QWidget ):
  def __init__( self, parent=None ):
    super( QuitBottun, self ).__init__( parent )
    self.initUI(parent)

  def initUI(self,parent):
    self.btn = QtGui.QPushButton('Quit',self)
    self.btn.clicked.connect(parent.quitApp)

    layout = QtGui.QVBoxLayout( self )
    layout.addWidget(self.btn)
    self.gbox = QtGui.QGroupBox("")
    self.gbox.setLayout(layout)

# ================================================================================

class StatusTable( QtGui.QWidget ):
  def __init__( self, parent=None ):
    super( StatusTable, self ).__init__( parent )
    self.initUI(parent)

  def initUI(self,parent):
    setup = Setup.Setup()

    self.label1 = QtGui.QLabel("Trigger Mode",self)
    self.label2 = QtGui.QLabel("Int. Spill",self)
    self.label1.setGeometry(0,0,80,10)
    self.label2.setGeometry(0,0,80,10)
    self.le1 = QtGui.QLineEdit("",self)
    self.le2 = QtGui.QLineEdit("",self)
    self.le1.setReadOnly(True)
    self.le2.setReadOnly(True)
    self.le1.setGeometry(0,0,300,10)
    self.le2.setGeometry(0,0,300,10)
    layout_table = QtGui.QGridLayout(self)
    layout_table.addWidget(self.label1,0,0)
    layout_table.addWidget(self.label2,1,0)
    layout_table.addWidget(self.le1   ,0,1)
    layout_table.addWidget(self.le2   ,1,1)
    gbox_table = QtGui.QGroupBox()
    gbox_table.setLayout(layout_table)

    self.timelabel = QtGui.QLabel("",self)
    self.timelabel.setGeometry(0,0,100,10)
  
    updatestr = "  Updated every " + str(int(setup.CCC_UPDATE_TIME/1000)) + "sec"
    labelupdate = QtGui.QLabel(updatestr,self)
    labelupdate.setGeometry(0,0,100,10)
 
    self.btnstop = QtGui.QPushButton('Stop',self)
    self.btnstop.clicked.connect(lambda: self.kill_timer(parent))
   
    self.btnstart = QtGui.QPushButton('Running',self)
    self.btnstart.setStyleSheet("background-color: %s"%(setup.CCC_COL_BTN_ON))
    self.btnstart.clicked.connect(lambda: self.start_timer(parent))
   
    self.btncheck = QtGui.QPushButton('Check',self)
    self.btncheck.clicked.connect(parent.status_thread)

    layout = QtGui.QGridLayout( self )
    layout.addWidget(self.timelabel,0,0)
    layout.addWidget(labelupdate,0,1)
    layout.addWidget(gbox_table,1,0,1,3)
    layout.addWidget(self.btnstart,2,0)
    layout.addWidget(self.btnstop,2,1)
    layout.addWidget(self.btncheck,2,2)
    self.gbox = QtGui.QGroupBox("Status Table")
    self.gbox.setLayout(layout)
    
    self.make_timer(parent)

  def setColor(self,state=""):
    setup = Setup.Setup()
    if state=="OK":
      self.gbox.setStyleSheet("background-color: #%s"%(setup.CCC_COL_STATUS_OK))
    elif state=="RUN":
      self.gbox.setStyleSheet("background-color: #%s"%(setup.CCC_COL_STATUS_RUN))
    elif state=="ERR":
      self.gbox.setStyleSheet("background-color: #%s"%(setup.CCC_COL_STATUS_ERR))
    else:
      self.gbox.setStyleSheet("background-color: #%s"%(setup.CCC_COL_STATUS_WAIT))
      
  
  def make_timer(self,parent=None):
    setup = Setup.Setup()
    self.timer = QtCore.QTimer(self)
    self.timer.timeout.connect(parent.status_check)
    self.btnstart.setStyleSheet("")
    self.btnstart.setText("Start")
    self.btnstop.setStyleSheet("background-color: %s"%(setup.CCC_COL_BTN_OFF))
    self.btnstop.setText("Stopped")

  def kill_timer(self,parent=None):
    setup = Setup.Setup()
    self.timer.stop()
    self.btnstart.setStyleSheet("")
    self.btnstart.setText("Start")
    self.btnstop.setStyleSheet("background-color: %s"%(setup.CCC_COL_BTN_OFF))
    self.btnstop.setText("Stopped")
    parent.setBtnEnable(True)

  def start_timer(self,parent=None):
    setup = Setup.Setup()
    if self.timer.isActive():
      msg = "Status check thread has already been active" 
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.warning("{0}".format(msg))
    else:
      self.timer.start(setup.CCC_UPDATE_TIME) #msec
      self.btnstart.setStyleSheet("background-color: %s"%(setup.CCC_COL_BTN_ON))
      self.btnstart.setText("Running")
      self.btnstop.setStyleSheet("")
      self.btnstop.setText("Stop")

    parent.setBtnEnable(False)




# ================================================================================

class TrigModeBox( QtGui.QWidget ):
  def __init__( self, parent=None ):
    super( TrigModeBox, self ).__init__( parent )
    self.initUI(parent)

  def initUI(self,parent):
  
    trig_array = ["OFF","External spill","Internal spill",\
                    "Nu Beam trigger","Sequential mode","TEST"]
    self.combo = QtGui.QComboBox(self)
    self.combo.addItems(trig_array)
    self.combo.activated.connect(self.btn_enable)        
    self.btn = QtGui.QPushButton('Set',self)
    self.btn.clicked.connect(parent.trig_thread)

    layout = QtGui.QGridLayout( self )
    layout.addWidget(self.combo,0,0,1,2)
    layout.addWidget(self.btn  ,0,2)
    self.gbox = QtGui.QGroupBox("Trigger Mode")
    self.gbox.setLayout(layout)

  def btn_enable(self):
    self.btn.setEnabled(True)

# ================================================================================

class InternalSpillConfig( QtGui.QWidget ):
  def __init__( self, parent=None ):
    super( InternalSpillConfig, self ).__init__( parent )
    self.initUI(parent)

  def initUI(self,parent):
    
    self.le1 = QtGui.QLineEdit("260",self)
    self.le2 = QtGui.QLineEdit("5",self)
    self.le1.textChanged.connect(self.btn_enable)
    self.le2.textChanged.connect(self.btn_enable)
    self.combo1 = QtGui.QComboBox(self)
    self.combo2 = QtGui.QComboBox(self)
    time_unit = ["ms","us"]
    self.combo1.addItems(time_unit)
    self.combo2.addItems(time_unit)
    self.combo1.activated.connect(self.btn_enable)        
    self.combo2.activated.connect(self.btn_enable)        
    self.btn = QtGui.QPushButton('Set',self)
    self.btn.clicked.connect(parent.spil_thread)

    layout = QtGui.QGridLayout( self )
    layout.addWidget(self.le1,0,0,1,2)
    layout.addWidget(self.le2,1,0,1,2)
    layout.addWidget(self.combo1,0,2)
    layout.addWidget(self.combo2,1,2)
    layout.addWidget(self.btn,1,3)
    self.gbox = QtGui.QGroupBox("Internal spill config")
    self.gbox.setLayout(layout)

  def btn_enable(self):
    self.btn.setEnabled(True)

# ================================================================================

class ccc_ctrl(QtGui.QWidget):

  def __init__(self):
    super(ccc_ctrl, self).__init__() 
    self.initUI()
  
  def initUI(self):
 
    # Status variables
    self.current_trigmode = 0
    self.current_period = 100 #ms
    self.current_active = 2   #ms
    self.status_spill_miss    = 0
    self.status_spill_fast    = 0
    self.state = ""
 
    # Class objects
    self.status  = StatusTable(self)
    self.trigmod = TrigModeBox(self)
    self.intspil = InternalSpillConfig(self)

    self.le1 = QtGui.QLineEdit("",self)
    self.le2 = QtGui.QLineEdit("",self)
    self.le1.setReadOnly(True)
    self.le2.setReadOnly(True)
    self.le1.setGeometry(0,0,100,10)
    self.le2.setGeometry(0,0,100,10)
    layout_le = QtGui.QGridLayout( self )
    layout_le.addWidget(self.le1,0,0)
    layout_le.addWidget(self.le2,1,0)
    self.gbox_le = QtGui.QGroupBox("Cmd Log")
    self.gbox_le.setLayout(layout_le)

    # Thread
    self.thread_trig   = threading.Thread()
    self.thread_spill  = threading.Thread()
    self.thread_status = threading.Thread()

    # Timer for changing status color
    self.timer_state = QtCore.QTimer(self)
    self.timer_state.timeout.connect(lambda: self.status.setColor(self.state))
    self.timer_state.start(5000)
    

    # Layout
    layout = QtGui.QGridLayout(self)
    layout.addWidget(self.trigmod.gbox,0,0)
    layout.addWidget(self.intspil.gbox,0,1)
    layout.addWidget(self.status.gbox ,1,0,1,2)
    layout.addWidget(self.gbox_le     ,2,0,1,2)

    self.status_thread()
    self.status.start_timer(self)


  def spil_thread(self):
    if self.thread_spill.isAlive() or\
       self.thread_trig.isAlive() or\
       self.thread_status.isAlive():
      msg = "Another thread is running. Wait for it finished."
      QtGui.QMessageBox.warning(self, "Warning",msg)
      return
    self.thread_spill = threading.Thread(target=self.set_spilinfo)
    self.thread_spill.start()

  def set_spilinfo(self):
    setup = Setup.Setup()
    norm = [1e+3, 1] #ms,us
    cmd = setup.CCC_SCRIPT_DIR + "/" + "spill_setinfo.sh"
    if os.path.isfile(cmd) and os.access(cmd,os.X_OK):
      self.current_period = int(str(self.intspil.le1.text()),10)
      self.current_active = int(str(self.intspil.le2.text()),10)
      time_per = self.current_period*norm[self.intspil.combo1.currentIndex()]
      time_act = self.current_active*norm[self.intspil.combo2.currentIndex()]
      cmd_per = cmd + " p " + str(int(time_per))
      cmd_act = cmd + " a " + str(int(time_act))
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("{0}".format(cmd_per.strip()))
        logger.logger.info("{0}".format(cmd_act.strip()))
      res = subprocess.Popen(cmd_per,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      stdlog,errlog = res.communicate()
      stdlog = stdlog.replace("\n",";").strip()
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("{0}".format(stdlog))
      for i in range(len(errlog)):
        errlog[0] += errlog[i].replace("\n",";").strip()
      if len(errlog)>0:
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.warning("{0}".format(errlog[0]))
      self.le1.setText(cmd_per)
      self.le2.setText(stdlog)
      res = subprocess.Popen(cmd_act,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      stdlog,errlog = res.communicate()
      stdlog = stdlog.replace("\n",";").strip()
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("{0}".format(stdlog))
      for i in range(len(errlog)):
        errlog[0] += errlog[i].replace("\n",";").strip()
      if len(errlog)>0:
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.warning("{0}".format(errlog[0]))
      self.le1.setText(cmd_act)
      self.le2.setText(stdlog)
    else:
      msg = cmd + " does NOT exist, or is not exectable."
      QtGui.QMessageBox.warning(self, "Warning",msg)
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.error("{0}".format(msg))
  
  def trig_thread(self):
    if self.thread_spill.isAlive() or\
       self.thread_trig.isAlive() or\
       self.thread_status.isAlive(): 
      msg = "Another thread is running. Wait for it finished."
      QtGui.QMessageBox.warning(self, "Warning",msg)
      return
    self.thread_trig = threading.Thread(target=self.set_trigmode)
    self.thread_trig.start()

  def set_trigmode(self):
    setup = Setup.Setup()
    self.current_trigmode = self.trigmod.combo.currentIndex()
    script_array = ["off","external","internal","beam","continuous"]
    if self.current_trigmode<len(script_array):
      spill_script = "spill_" + script_array[self.current_trigmode] + ".sh"
    else:
      QtGui.QMessageBox.warning(self, "Warning", "No such a trigger mode.")
      return
    cmd = setup.CCC_SCRIPT_DIR + "/" + spill_script
    if os.path.isfile(cmd) and os.access(cmd,os.X_OK):
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("{0}".format(cmd.strip()))
      res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
      stdlog,errlog = res.communicate()
      stdlog = stdlog.replace("\n",";").strip()
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.info("{0}".format(stdlog))
      for i in range(len(errlog)):
        errlog[0] += errlog[i].replace("\n",";").strip()
      if len(errlog)>0:
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.warning("{0}".format(errlog[0]))
      self.le1.setText(cmd)
      self.le2.setText(stdlog)
    else:
      msg = cmd + " does NOT exist, or is not exectable."
      QtGui.QMessageBox.warning(self, "Warning",msg)
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.warning("{0}".format(msg))


  def status_thread(self):
    setup = Setup.Setup()
    if self.thread_spill.isAlive() or\
       self.thread_trig.isAlive() or\
       self.thread_status.isAlive():
      msg = "Another thread is running. Status monitoring is skipped this time."
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.loggger.warning("{0}".format(msg))
      return
    self.thread_status = threading.Thread(target=self.status_check)
    self.thread_status.start()

  def status_check(self):
    setup = Setup.Setup()
    cmd_list = ["spill_getstate.sh","spill_getinfo.sh"]
    state = ""
    for var in range(len(cmd_list)):
      cmd = setup.CCC_SCRIPT_DIR + "/" + cmd_list[var]
      if os.path.isfile(cmd) and os.access(cmd,os.X_OK):
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.info("{0}".format(cmd.strip()))
        res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        stdlog,errlog = res.communicate()
        stdlog = stdlog.replace("\n",";").strip()
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.info("{0}".format(stdlog))
        for i in range(len(errlog)):
          errlog[0] += errlog[i].replace("\n",";").strip()
        if len(errlog)>0:
          with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
            logger.logger.warning("{0}".format(errlog[0]))
        self.le1.setText(cmd)
        self.le2.setText(stdlog)
        if var == 0:
          statepos  = stdlog.find("STATE:")
          statestop = stdlog.find("mode")
          statestr  = stdlog[statepos+0:statestop+4]
          self.status.le1.setText(statestr)
          if   statestr=="STATE:3 Continuous mode"    : state="OK"
          elif statestr=="STATE:1 Internal spill mode": state="RUN"
          elif statestr=="STATE:0 DEBUG mode"         : state="RUN"
          else                                        : 
            state="ERR"
            d = datetime.datetime.today()
            timestr = d.strftime("%Y-%m-%d %H:%M:%S")
            with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
              logger.logger.error("CCC state is not as expected. {0}".format(statestr))
            setup.set_alarm("CCC State")
        elif var == 1:
          periodpos  = stdlog.find("SPILL period:")
          periodstop = stdlog.find("[ms]")
          activepos  = stdlog.find("SPILL active:")
          activestop = stdlog.find("[us]")
          statestr   = stdlog[periodpos:periodstop+4] \
                      + " |  " \
                      + stdlog[activepos:activestop+4]
          self.status.le2.setText(statestr)
      else:
        msg = cmd + " does NOT exist, or is not exectable." 
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.error("{0}".format(msg))
        self.kill_timer()

    d = datetime.datetime.today()
    self.timestr = d.strftime("%Y-%m-%d %H:%M:%S")
    self.status.timelabel.setText(self.timestr)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("Current status is {0}".format(state))
    self.state = state

  def setBtnEnable(self,var=True):
    self.trigmod.combo .setEnabled(var)
    self.trigmod.btn   .setEnabled(var)
    self.intspil.le1   .setEnabled(var)
    self.intspil.le2   .setEnabled(var)
    self.intspil.combo1.setEnabled(var)
    self.intspil.combo2.setEnabled(var)
    self.intspil.btn   .setEnabled(var)

  def ccc_check(self):
    setup = Setup.Setup()
    cmd = "{0}/ccc_check.sh".format(setup.CCC_SCRIPT_DIR)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,\
                                          stderr=subprocess.PIPE)
    res_out, res_err = res.communicate()
    if str(res_out).replace("\n","")=="0% packet loss": return True
    else: return False

  def quitApp(self):
    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to quit?", QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if reply == QtGui.QMessageBox.Yes:
      QtGui.QApplication.quit()
