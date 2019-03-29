#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math
import serial, binascii
from xml.etree import ElementTree
from xml.dom   import minidom
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

class e_log(QtGui.QWidget):

  def __init__(self):
    super(e_log, self).__init__() 
    self.initUI()
  
  def initUI(self):
    setup = Setup.Setup()

    if not os.path.exists(setup.ELOG_ID):
      with open(setup.ELOG_ID,"w") as f:
        f.write("0")
    self.elog_id = 0

    self.submitbtn1 = QtGui.QPushButton("Submit",self)
    self.submitbtn1.clicked.connect(lambda: self.submit(False))
    self.submitbtn2 = QtGui.QPushButton("Submit (Current time)",self)
    self.submitbtn2.clicked.connect(lambda: self.submit(True))

    self.newbtn = QtGui.QPushButton("New",self)
    self.newbtn.clicked.connect(self.newlog)


    self.label1  = QtGui.QLabel("Author",self)
    self.label2  = QtGui.QLabel("Category",self)
    self.label3  = QtGui.QLabel("Subject",self)
    self.label4  = QtGui.QLabel("Content",self)

    self.author  = QtGui.QLineEdit("Author",self)
    self.category= QtGui.QComboBox(self)
    self.category.addItems(setup.ELOG_CATEGORY)
    self.subject = QtGui.QLineEdit("Subject",self)
    self.content = QtGui.QTextEdit("Content")
    self.year    = QtGui.QComboBox(self)
    self.month   = QtGui.QComboBox(self)
    self.day     = QtGui.QComboBox(self)
    self.hour    = QtGui.QComboBox(self)
    self.minute  = QtGui.QComboBox(self)
    self.slash1  = QtGui.QLabel("/",self)
    self.slash2  = QtGui.QLabel("/",self)
    self.colon   = QtGui.QLabel(":",self)
    for var in setup.ELOG_YEAR:
      self.year.addItem("%d"%(var))
    for var in setup.ELOG_MONTH:
      self.month.addItem("%d"%(var))
    for var in setup.ELOG_DAY:
      self.day.addItem("%d"%(var))
    for var in setup.ELOG_HOUR:
      self.hour.addItem("%d"%(var))
    for var in setup.ELOG_MINUTE:
      self.minute.addItem("%d"%(var))

    self.int_year   = -1
    self.int_month  = -1
    self.int_day    = -1
    self.int_hour   = -1
    self.int_minute = -1
    self.gettime()
    self.setconbotime()
 
    # layout
    date_layout = QtGui.QHBoxLayout()
    date_layout.addWidget(self.year)
    date_layout.addWidget(self.slash1)
    date_layout.addWidget(self.month)
    date_layout.addWidget(self.slash2)
    date_layout.addWidget(self.day)
    date_layout.addWidget(self.hour)
    date_layout.addWidget(self.colon)
    date_layout.addWidget(self.minute)
    self.date_gbox = QtGui.QGroupBox("Date")
    self.date_gbox.setLayout(date_layout)

    layout = QtGui.QGridLayout(self)
    layout.setColumnStretch(0,1)
    layout.setColumnStretch(1,3)
    layout.setColumnStretch(2,3)
    layout.setColumnStretch(3,3)
    layout.addWidget(self.date_gbox ,0,0,1,2)
    layout.addWidget(self.newbtn    ,0,3)
    layout.addWidget(self.label1    ,1,0)
    layout.addWidget(self.author    ,1,1,1,3)
    layout.addWidget(self.label2    ,2,0)
    layout.addWidget(self.category  ,2,1,1,3)
    layout.addWidget(self.label3    ,3,0)
    layout.addWidget(self.subject   ,3,1,1,3)
    layout.addWidget(self.label4    ,4,0)
    layout.addWidget(self.content   ,4,1,1,3)
    layout.addWidget(self.submitbtn1,5,1)
    layout.addWidget(self.submitbtn2,5,2)

  #####################################################

  def submit(self,current_time=True):
    setup = Setup.Setup()
    with open(setup.ELOG_ID,"r") as f:
      self.elog_id = int(f.readline())
    if current_time:
      self.gettime()
    else:
      self.getconbotime()

    msg = "Are you sure to submit?\nDate:%04d/%02d/%02d %02d:%02d\nAuthour:%s\nCategory:%s\nSubject:%s\nContent:%s"%(
        self.int_year,self.int_month,self.int_day,self.int_hour,self.int_minute,
        str(self.author.text()),
        str(self.category.currentText()),
        str(self.subject.text()),
        str(self.content.toPlainText()).replace("\n",";"))
    reply = QtGui.QMessageBox.question(self, 'Message',
        msg, QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if not reply == QtGui.QMessageBox.Yes:
      return

    
    top = ElementTree.Element("e_log")
    elogid = ElementTree.SubElement(top,"elog_id")
    elogid.text = "%d"%(self.elog_id)
    date = ElementTree.SubElement(top,"date")
    date.text = "%04d/%02d/%02d %02d:%02d"%(
        self.int_year,self.int_month,self.int_day,self.int_hour,self.int_minute)
    author = ElementTree.SubElement(top,"author")
    author.text = str(self.author.text())
    category = ElementTree.SubElement(top,"category")
    category.text = str(self.category.currentText())
    subject = ElementTree.SubElement(top,"subject")
    subject.text = str(self.subject.text())
    content = ElementTree.SubElement(top,"content")
    content.text = str(self.content.toPlainText()).replace("\n",";")

    tree = ElementTree.tostring(top,"utf-8")
    reparsed = minidom.parseString(tree)
    with open("%s/elog_%08d.xml"%(setup.ELOG_DIR,self.elog_id),"w") as f:
      f.write(reparsed.toprettyxml(indent="  "))
    with open(setup.ELOG_ID,"w") as f:
      f.write("%d"%(self.elog_id+1))

    self.setconbotime()
    self.uploadWeb()
    self.sendMail()

  #####################################################

  def newlog(self):
    msg = "Are you sure to clear the current log and make a new log?"
    reply = QtGui.QMessageBox.question(self, 'Message',
        msg, QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if not reply == QtGui.QMessageBox.Yes:
      return

    setup = Setup.Setup()
    self.gettime()
    self.setconbotime()
    self.author .setText("Author")
    self.content.setText("Content")

  #####################################################

  def gettime(self):
    setup = Setup.Setup()
    d = datetime.datetime.today()
    self.int_year   = int(d.strftime("%Y"))
    self.int_month  = int(d.strftime("%m"))
    self.int_day    = int(d.strftime("%d"))
    self.int_hour   = int(d.strftime("%H"))
    self.int_minute = int(d.strftime("%M"))
   
  #####################################################

  def getconbotime(self):
    setup = Setup.Setup()
    self.int_year   = int(self.year  .currentText())
    self.int_month  = int(self.month .currentText())
    self.int_day    = int(self.day   .currentText())
    self.int_hour   = int(self.hour  .currentText())
    self.int_minute = int(self.minute.currentText())
  
  #####################################################

  def setconbotime(self):
    setup = Setup.Setup()
    if self.int_year   in setup.ELOG_YEAR and \
       self.int_month  in setup.ELOG_MONTH and \
       self.int_day    in setup.ELOG_DAY and\
       self.int_hour   in setup.ELOG_HOUR and\
       self.int_minute in setup.ELOG_MINUTE:
      self.year  .setCurrentIndex(setup.ELOG_YEAR  .index(self.int_year  ))
      self.month .setCurrentIndex(setup.ELOG_MONTH .index(self.int_month ))
      self.day   .setCurrentIndex(setup.ELOG_DAY   .index(self.int_day   ))
      self.hour  .setCurrentIndex(setup.ELOG_HOUR  .index(self.int_hour  ))
      self.minute.setCurrentIndex(setup.ELOG_MINUTE.index(self.int_minute))
    else:
      msg = "The current time is out of the range of set time.\nCheck Setup.py"
      QtGui.QMessageBox.info(self, msg)
      return

  #####################################################

  def uploadWeb(self):
    setup = Setup.Setup()
    cmd = "rsync -avz {0} {1}:{2} >> /dev/null".format(setup.ELOG_DIR,setup.SERV_KYOTO,setup.KYOTO_WEB_DIR)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("{0}".format(cmd.replace("\n",";")))
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    result = res.communicate()
    stdlog = ""
    for i in range(len(result)):
      stdlog += result[i].replace("\n",";")
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("{0}".format(stdlog))


  #####################################################

  def sendMail(self):
    setup = Setup.Setup()
    sub = "[wagasci e-log#%08d:%s]"%(self.elog_id,str(self.category.currentText()))
    header = "From: {0}\nTo: {1}\nSubject: {2}\nReply-To: {3}\n"\
              .format(setup.ELOG_SRC_ADDR,setup.ELOG_DST_ADDR,sub,setup.ELOG_REPLYTO)
    header += "====================\n"
    header += "This message is automatically sent from wagasci-analysis server,\n"
    header += "Do NOT reply to this address, but please ask {0}\n".format(setup.ELOG_REPLYTO)
    header += "====================\n"
    header += "Check the WAGASCI Monitor webpage.\n"
    header += "{0}\n".format(setup.KYOTO_WEB_ADDR)
    header += "----- New e-log has been submitted. -----\n"
    elogid = "%d"%(self.elog_id)
    date = "%04d/%02d/%02d %02d:%02d"%(
        self.int_year,self.int_month,self.int_day,self.int_hour,self.int_minute)
    author = str(self.author.text())
    category = str(self.category.currentText())
    subject = str(self.subject.text())
    content = str(self.content.toPlainText())
    header += "\n----\n ID: %s"%(elogid)
    header += "\n----\n Author: %s"%(author)
    header += "\n----\n Category: %s"%(category)
    header += "\n----\n Subject: %s"%(subject)
    header += "\n----\n Content: %s"%(content)
    header = "echo -e \"{0}\"".format(header)
    cmd = "{0} | sendmail -i -f {1} {2}".format(header,setup.ELOG_SRC_ADDR,setup.ELOG_DST_ADDR)
    with Logger.Logger(setup.SLOWMONITOR_LOG) as logger:
      logger.logger.info("{0}".format(cmd.replace("\n",";")))
    subprocess.call(cmd,shell=True)
