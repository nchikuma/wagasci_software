#!/usr/bin/python
# -*- coding: utf-8 -*-

############################################################################################
#  Here are all of the fixed parameters used in the slow monitor system written in python. #
#  These must be identical to the other setting file "Setup.h", that is used to compile   #
#  C++ programs and to run SH scripts.                                                     #
#                                                                                          #
#  2017/09/23                                                                              #
#  Naruhiro Chikuma                                                                        #
#  The University of Tokyo                                                                 #
#                                                                                          #
############################################################################################

import os, subprocess,datetime

class MyStyle:
  def __init__(self):

    self.style_widget = "\
       background-color: gray \
       "
       #background-color: #c0fffc \
    self.style_tab = "\
        background-color: white \
        "
    self.style_tab_bar = "\
        border: 1px solid #008080; \
        background-color: #008080; \
        color: white \
        " 

  def __enter__(self):
    return self

  def __exit__(self,exc_type,exc_value,traceback):
    return True
