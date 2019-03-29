#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################################################################
#  The parameters should be changed according to the current run status.                   #
#                                                                                          #
#  2017/09/23                                                                              #
#  Naruhiro Chikuma                                                                        #
#  The University of Tokyo                                                                 #
#                                                                                          #
############################################################################################

import os, subprocess,datetime

class RunSetting:
  def __init__(self):

    self.T2KRUN = 9
    self.MRRUN1 = 77 #initial MR RUN
    self.MRRUN2 = 77 #current (last) MR RUN
    self.BSD_VER = "p06"
    self.WAGASCI_RUN1 = 113 #initial WAGASCI RUN
    self.WAGASCI_RUN2 = 130 #max WAGASCI RUN
    self.INGRID_RUN1 = 31159 #initial INGRID RUN
    self.INGRID_RUN2 = 31330 #max INGRID RUN


  def __enter__(self):
    return self

  def __exit__(self,exc_type,exc_value,traceback):
    return True
