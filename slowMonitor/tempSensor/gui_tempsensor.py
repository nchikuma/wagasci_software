#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys, os, time, subprocess, datetime, math
import serial, binascii
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import tempSensor, Setup

class GUI(QtGui.QWidget):
  def __init__(self):
    super(GUI, self).__init__()
    self.initUI()
  
  def initUI(self):
    setup = Setup.Setup()
    qtab = QtGui.QTabWidget()
    qtab.addTab(tempSensor.tempsensor_hist(), 'Temparature Sensor')
    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(qtab)
    self.setLayout(hbox)
    self.setGeometry(
        setup.TEMP_POS_X,
        setup.TEMP_POS_Y,
        setup.TEMP_SIZE_X,
        setup.TEMP_SIZE_Y)

    self.setWindowTitle('Temparature Sensor')
    self.show()

  def closeEvent(self,event): 
    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to quit?", QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if reply == QtGui.QMessageBox.Yes:
      event.accept() 
    else: 
      event.ignore()


# ================================================================================

def main():
  app = QtGui.QApplication(sys.argv)
  gui = GUI()
  sys.exit(app.exec_())

# ================================================================================

if __name__ == '__main__':
  main()
