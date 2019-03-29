#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math
import serial, binascii
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import Logger, Setup

class lambdaps_hist(QtGui.QWidget):

  def __init__(self):
    super(lambdaps_hist, self).__init__() 
    self.initUI()
  
  def initUI(self):
    setup = Setup.Setup()

    # Histogram
    self.pic = QtGui.QLabel("histgram",self)
    self.pic.setGeometry(0,0,600,500)
    self.pic.setPixmap(QtGui.QPixmap(setup.LAMBDA_PIC1))

    self.filewatch = QtCore.QFileSystemWatcher(self)
    self.filewatch.fileChanged.connect(self.changePic)
    self.filewatch.addPath(setup.LAMBDA_PIC1)
    self.filewatch.addPath(setup.LAMBDA_PIC2)
    self.filewatch.addPath(setup.LAMBDA_PIC3)
    self.filewatch.addPath(setup.LAMBDA_PIC4)
    self.time = datetime.datetime.today().strftime('%s')

    # Period select
    self.combo = QtGui.QComboBox(self)
    self.combo.addItem("10 min")
    self.combo.addItem("1 hour")
    self.combo.addItem("1 day ")
    self.combo.addItem("3 days")
    self.combo.activated.connect(self.changePic)

    # layout
    layout = QtGui.QGridLayout(self)
    layout.addWidget(self.pic  ,0,0)
    layout.addWidget(self.combo,1,0)

  def changePic(self):
    setup = Setup.Setup()
    if   self.combo.currentIndex()==0: picname=setup.LAMBDA_PIC1
    elif self.combo.currentIndex()==1: picname=setup.LAMBDA_PIC2
    elif self.combo.currentIndex()==2: picname=setup.LAMBDA_PIC3
    elif self.combo.currentIndex()==3: picname=setup.LAMBDA_PIC4
    self.pic.setPixmap(QtGui.QPixmap(picname))
