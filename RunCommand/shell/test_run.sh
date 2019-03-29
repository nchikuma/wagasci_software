#!/bin/sh
# -*- coding: utf-8 -*-
# 
# Copyright 2012-2015 Frédéric Magniette, Miguel Rubio-Roy
# This file is part of Calicoes.

. /opt/pyrame/ports.sh

$WAGASCI_RUNCOMMANDDIR/python/test_run.py "$@"
if test $? -eq 1; then
  exit 1
fi
