#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import lambdaPS, lambdaHist, Setup

# ================================================================================

class GUI(QtGui.QWidget):
  def __init__(self):
    super(GUI, self).__init__()
    self.initUI()
  
  def initUI(self):
    setup = Setup.Setup()
    qtab = QtGui.QTabWidget()
    qtab.addTab(lambdaPS.ps_ctrl(), 'Control')
    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(qtab)
    self.setLayout(hbox)
    self.setGeometry(
        setup.LAMBDA_CTRL_POS_X,
        setup.LAMBDA_CTRL_POS_Y,
        setup.LAMBDA_CTRL_SIZE_X,
        setup.LAMBDA_CTRL_SIZE_Y)

    self.setWindowTitle('Lambda PS')
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
