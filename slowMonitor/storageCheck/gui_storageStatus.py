#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
sys.path.append("{0}/../lambdaPS/".format(os.path.abspath(os.path.dirname(__file__))))
sys.path.append("{0}/../tempSensor/".format(os.path.abspath(os.path.dirname(__file__))))
sys.path.append("{0}/../waterSensor/".format(os.path.abspath(os.path.dirname(__file__))))
sys.path.append("{0}/../autoProcess/".format(os.path.abspath(os.path.dirname(__file__))))
import lambdaHist, tempSensor, waterSensor, processStatus, Setup, MyStyle, storageStatus

# ================================================================================

class GUI(QtGui.QWidget):
  def __init__(self):
    super(GUI, self).__init__()
    self.initUI()
  
  def initUI(self):
    setup = Setup.Setup()
    self.qtab = QtGui.QTabWidget()
    self.qtab.addTab(storageStatus.storage_status(), 'Storage' )
    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(self.qtab)
    self.setLayout(hbox)
    self.setGeometry(
        setup.HIST_POS_X,
        setup.HIST_POS_Y,
        setup.HIST_SIZE_X,
        setup.HIST_SIZE_Y)
    self.setMyStyle()

    self.setWindowTitle('History')
    self.show()

  def closeEvent(self,event): 
    reply = QtGui.QMessageBox.question(self, 'Message',
        "Are you sure to quit?", QtGui.QMessageBox.Yes | 
        QtGui.QMessageBox.No, QtGui.QMessageBox.No) 
    if reply == QtGui.QMessageBox.Yes:
      event.accept() 
    else: 
      event.ignore()

  def setMyStyle(self):
    style = MyStyle.MyStyle()
    self              .setStyleSheet(style.style_widget)
    self.qtab         .setStyleSheet(style.style_tab)
    self.qtab.tabBar().setStyleSheet(style.style_tab_bar)



# ================================================================================

def main():
  app = QtGui.QApplication(sys.argv)
  gui = GUI()
  sys.exit(app.exec_())

# ================================================================================

if __name__ == '__main__':
  main()
