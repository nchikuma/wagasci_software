#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, time, subprocess, datetime
from PyQt4 import QtGui, QtCore

sys.path.append("{0}/../include/".format(os.path.abspath(os.path.dirname(__file__))))
import spillNb, Setup, MyStyle

# ================================================================================

class GUI(QtGui.QWidget):
  def __init__(self):
    super(GUI, self).__init__()
    self.initUI()
  
  def initUI(self):
    setup = Setup.Setup()
    self.qtab = QtGui.QTabWidget()
    self.qtab.addTab(spillNb.spillNb(), 'SpillNb')
    hbox = QtGui.QHBoxLayout()
    hbox.addWidget(self.qtab)
    self.setLayout(hbox)
    self.setGeometry(
        setup.SPILL_POS_X,
        setup.SPILL_POS_Y,
        setup.SPILL_SIZE_X,
        setup.SPILL_SIZE_Y)
    self.setMyStyle()

    self.setWindowTitle('SpillNb')
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
