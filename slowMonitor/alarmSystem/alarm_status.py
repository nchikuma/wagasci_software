#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

# ================================================================================

class FileWatcher(QtCore.QThread):

  mutex = QtCore.QMutex()

  def __init__(self,parent=None,target=""):
    super(FileWatcher,self).__init__(parent)
    self.stopped = False
    self.last_ts = 0.0
    self.targetfile = target

  def run(self):
    setup = Setup.Setup()
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("file watch thread is running...")
    while not self.stopped:
      timestamp = os.stat(self.targetfile).st_mtime
      if timestamp == self.last_ts: pass
      elif timestamp > self.last_ts:
        self.last_ts = timestamp
        self.finished.emit()
      else:
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.error("FileWatcher: timestamp shows the past to the last one.")
      time.sleep(setup.ALARM_TIME_FILEWATCH)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.warning("sound thread is stopped.")
    
  def stop(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = True
   
  def setup(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = False
  
# ================================================================================

class SoundThread(QtCore.QThread):

  mutex = QtCore.QMutex()
  mailSent = False

  def __init__(self,parent=None):
    super(SoundThread,self).__init__(parent)
    self.stopped = False
    self.alarm_type = []

  def run(self):
    setup = Setup.Setup()
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("sound thread is running...")
    while not self.stopped:
      sub = ""
      for var in setup.ALARM_LIST:
        if var in self.alarm_type:
          cmd = "aplay " + setup.ALARM_SOUND[setup.ALARM_LIST.index(var)]
          subprocess.call(cmd,shell=True)
          self.finished.emit()
          sub += " {0}".format(var)
      if (not sub=="") and (not self.mailSent):
        alarm_id = 0
        with open(setup.ALARM_ID,"r") as f:
          alarm_id = int(f.read())
        with open(setup.ALARM_ID,"w") as f:
          f.write("{0}".format(alarm_id+1))
        sub = "[wagasci#%05d:%s]"%(alarm_id,setup.ALARM_MAIL_SUB) + sub
        cmd = "ssh wagasci-ana cat {0}| grep -v INFO|grep -v \"wc:\"|tail -n {1}|tac".format(
            setup.SLOWMONITOR_LOG,setup.ALARM_NBLINE)
        res = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        msg, ret_err = res.communicate()
        msg = msg.split("\n")
        header = "From: {0}\nTo: {1}\nSubject: {2}\nReply-To: {3}\n"\
                  .format(setup.ALARM_SRC_ADDR,setup.ALARM_DST_ADDR,sub,setup.ALARM_REPLYTO)
        header += "====================\n"
        header += "This message is automatically sent from wagasci-analysis server,\n"
        header += "Do NOT reply to this address, but please ask {0}\n".format(setup.ALARM_REPLYTO)
        header += "====================\n"
        header += "Check the WAGASCI Monitor webpage.\n"
        header += "{0}\n".format(setup.KYOTO_WEB_ADDR)
        header += "-----Error Log-----\n"
        for var in msg: header += "{0}\n".format(var)
        header = "echo -e \"{0}\"".format(header)
        cmd = "{0} | sendmail -i -f {1} {2}".format(header,setup.ALARM_SRC_ADDR,setup.ALARM_DST_ADDR)
        subprocess.call(cmd,shell=True)
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.info("Alarm message has been sent to {0}".format(setup.ALARM_DST_ADDR))
        self.mailSent = True
        cmd = "ssh wagasci-ana {0}/rsync_webKyoto.py now".format(setup.WEB_KYOTO_DIR)
        subprocess.call(cmd,shell=True)
      time.sleep(setup.ALARM_TIME_ALARMPERIOD)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("sound thread is stopped.")
    
  def stop(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = True
   
  def setup(self):
    with QtCore.QMutexLocker(self.mutex):
      self.stopped = False
  
# ================================================================================

class status_window( QtGui.QWidget ):
  def __init__( self, parent=None):
    super( status_window, self ).__init__( parent )
    self.initUI(parent)

  def initUI(self,parent):
    setup = Setup.Setup()

    self.alarm_stopped = []
    for i in range(len(setup.ALARM_LIST)): self.alarm_stopped.append(False)
    self.lasttime_reset \
      = int(datetime.datetime.today().strftime("%s"))
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("============= Alarm system is stated. unixtime=%d"%(self.lasttime_reset))

    self.btn = []
    for alarm in setup.ALARM_LIST:
      self.btn.append(QtGui.QPushButton(alarm,self))
    self.btnreset  = QtGui.QPushButton('Reset All Alarms',self)
    self.btntest   = QtGui.QPushButton('Test sounds',self)
    for i in range(len(setup.ALARM_LIST)):
      self.btn[i].clicked.connect(lambda state,x=i: self.stop_alarm(x))
    self.btnreset.clicked.connect(self.reset_allalarms)
    self.btntest .clicked.connect(self.test_sounds)
    self.combo = QtGui.QComboBox(self)
    self.combo.addItems(setup.ALARM_LIST)
    
    if not os.path.isfile(setup.ALARM_LOG):
      subprocess.call("echo -e "" > {0}".format(setup.ALARM_LOG),shell=True)
    if not os.path.isfile(setup.ALARM_ID):
      subprocess.call("echo '0' > {0}".format(setup.ALARM_ID),shell=True)

    self.thread_sound = SoundThread(self)
    self.thread_sound.start()

    self.thread_filewatch = FileWatcher(self,target=setup.ALARM_LOG)
    self.thread_filewatch.last_ts = os.stat(setup.ALARM_LOG).st_mtime
    self.thread_filewatch.finished.connect(self.set_alarms)
    self.thread_filewatch.start()

    self.check = QtGui.QCheckBox("Stop sending mail")
    self.check.toggled.connect(self.stop_mail)

    layout = QtGui.QGridLayout( self )
    for i in range(len(self.btn)):
      x = int(i%2)
      y = int(i/2)
      layout.addWidget(self.btn[i],y,x)
    y = int(len(self.btn)/2)+int(len(self.btn)%2)
    layout.addWidget(self.btnreset ,y  ,0,1,2)
    layout.addWidget(self.btntest  ,y+1,0)
    layout.addWidget(self.combo    ,y+1,1)
    layout.addWidget(self.check    ,y+2,1)
    layout.setHorizontalSpacing(0)
    layout.setVerticalSpacing(0)

  def stop_alarm(self,i=-1,logger=None):
    setup = Setup.Setup()
    if not (i>-1 and i<len(self.btn)): return
    if not setup.ALARM_LIST[i] in self.thread_sound.alarm_type: return
    self.alarm_stopped[i] = True
    for tmp in range(self.thread_sound.alarm_type.count(setup.ALARM_LIST[i])): 
      self.thread_sound.alarm_type.remove(setup.ALARM_LIST[i])
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("Stop alarm: {0}: timestamp={1}".format(setup.ALARM_LIST[i],self.lasttime_reset))

  def reset_allalarms(self):
    setup = Setup.Setup()
    for i in range(len(setup.ALARM_LIST)): self.alarm_stopped[i] = False
    for i in range(len(self.thread_sound.alarm_type)): 
      del self.thread_sound.alarm_type[0]
    for btn in self.btn: btn.setStyleSheet("")
    cmd = "head {0} -n 1".format(setup.ALARM_LOG)
    res = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    ret, ret_err = res.communicate()
    tmp = ret.replace("\n","").split("/")
    if len(tmp)!=2:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.error("The log text has a wrong format: {0}".format(tmp))
    else: self.lasttime_reset = int(tmp[0])
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("Reset all alarms: timestamp={0}".format(self.lasttime_reset))
    if not self.check.isChecked(): self.thread_sound.mailSent = False

  def set_alarms(self):
    setup = Setup.Setup()
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("Set alarms")
    time = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    cmd = "head {0} -n 1".format(setup.ALARM_LOG)
    res = subprocess.Popen(cmd, shell=True,
                           stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    ret, ret_err = res.communicate()
    tmp = ret.replace("\n","").split("/")
    if len(tmp)!=2:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.error("The log text has a wrong format: {0}".format(tmp))
      return
    if not tmp[0].isdigit():
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.error("The log text has a wrong format: {0}".format(tmp))
      return
    alarm_time  = int(tmp[0])
    alarm_type  = str(tmp[1])
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("time;{0}, last:{1}".format(alarm_time,self.lasttime_reset))
    if alarm_time<=self.lasttime_reset: return
    if alarm_type in setup.ALARM_LIST:
      if not self.alarm_stopped[setup.ALARM_LIST.index(alarm_type)]:
        self.btn[setup.ALARM_LIST.index(alarm_type)]\
                    .setStyleSheet("background-color: red")
        self.thread_sound.alarm_type.append(alarm_type)
        with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
          logger.logger.info("thread alarm list {0}".format(self.thread_sound.alarm_type))
    else:
      with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
        logger.logger.error("Unexpected alarm type: {0}".format(alarm_type))
      return
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("set_alarms... done")

  def test_sounds(self):
    setup = Setup.Setup()
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("Sound test...")
    checkitem = self.combo.currentText()
    setup.set_alarm(checkitem)

  def stop_mail(self):
    self.thread_sound.mailSent = self.check.isChecked()
