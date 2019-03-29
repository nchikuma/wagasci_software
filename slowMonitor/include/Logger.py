#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################################################################
#  This Logger system could be imported for each slow monitor system written in python.    #
#  Threre are tags to tell the log status, such as;                                        #
#     - debug                                                                              #
#     - info                                                                               #
#     - warning                                                                            #
#     - error                                                                              #
#     - critical                                                                           #
#                                                                                          #
#  2017/09/23                                                                              #
#  Naruhiro Chikuma                                                                        #
#  The University of Tokyo                                                                 #
#                                                                                          #
############################################################################################

from logging import getLogger, StreamHandler, FileHandler,Formatter, DEBUG

class Logger:
  def __init__(self,logfile=None):
    self.logger = getLogger(__name__)
    self.handler = None
    if not logfile: 
      self.handler = StreamHandler()
    else: 
      self.handler = FileHandler(str(logfile))
    formatter = Formatter('[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s] %(message)s')
    self.handler.setLevel(DEBUG)
    self.handler.setFormatter(formatter)
    self.logger.setLevel(DEBUG)
    self.logger.addHandler(self.handler)
    self.logger.propagate = False

  def __enter__(self):
    return self

  def __exit__(self,exc_type,exc_value,traceback):
    if self.handler: 
      self.handler.close()
      self.logger.removeHandler(self.handler)
    return True
