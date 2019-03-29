#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import alarm_status, Setup

# ================================================================================

class GUI(QtGui.QWidget):
  def __init__(self):
    super(GUI, self).__init__()
    self.initUI()
  
  def initUI(self):
    setup = Setup.Setup()
    qtab = QtGui.QTabWidget()
    qtab.addTab(alarm_status.status_window(), 'Status')
    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(qtab)
    self.setLayout(hbox)
    self.setGeometry(
        setup.ALARM_POS_X,
        setup.ALARM_POS_Y,
        setup.ALARM_SIZE_X,
        setup.ALARM_SIZE_Y)
    self.setWindowTitle('Alarms for slow monitor')
    self.show()

  def closeEvent(self,event): 
    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to quit?", QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if reply == QtGui.QMessageBox.Yes: event.accept() 
    else                             : event.ignore()


# ================================================================================

def main():
  app = QtGui.QApplication(sys.argv)
  gui = GUI()
  sys.exit(app.exec_())

# ================================================================================

if __name__ == '__main__':
  main()
