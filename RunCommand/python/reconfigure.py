#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import sys
import argparse
import subprocess
import time

OKBLUE= '\033[36m'
ENDC= '\033[0m'
FAIL = '\033[41m'

parser = argparse.ArgumentParser(description="reconfigure.")
parser.add_argument("-f","--xmlfile", help="input xmlfile")
args=parser.parse_args()

cmd =". /opt/pyrame/ports.sh"
subprocess.call(cmd,shell=True)

print OKBLUE+"spill off ..."+ENDC
sys.stdout.flush()
cmd ="ssh wagasci-ana /usr/local/src/wagasci_software/slowMonitor/cccCtrl/script/spill_off.sh"
subprocess.call(cmd,shell=True)
time.sleep(2)

print OKBLUE+"invalidate.sh ..."+ENDC
sys.stdout.flush()
cmd ="invalidate.sh"
subprocess.call(cmd,shell=True)
time.sleep(2)

print OKBLUE+"deinitialize.sh ..."+ENDC
sys.stdout.flush()
cmd ="deinitialize.sh"
subprocess.call(cmd,shell=True)
time.sleep(2)

if(args.xmlfile):
  print OKBLUE+"load_config_file.sh %s"%(args.xmlfile)+ENDC
  sys.stdout.flush()
  cmd="load_config_file.sh %s"%(args.xmlfile)
else:
  print OKBLUE+"load_config_file.sh /opt/calicoes/config/wagasci_config.xml"+ENDC
  sys.stdout.flush()
  cmd="load_config_file.sh /opt/calicoes/config/wagasci_config.xml"
subprocess.call(cmd,shell=True)
time.sleep(2)

print OKBLUE+"initialize.sh ..."+ENDC
sys.stdout.flush()
cmd ="initialize.sh"
subprocess.call(cmd,shell=True)
time.sleep(2)

print OKBLUE+"configure.sh ..."+ENDC
sys.stdout.flush()
cmd ="date"
subprocess.call(cmd,shell=True)
cmd ="configure.sh"

cycle= 0;

while ( cycle < 10 ):
  bool_config=subprocess.call(cmd,shell=True)
  if ( bool_config !=0 ) :
    print FAIL+"**  FAIL TO RECONFIGURE !  **"+ENDC
    sys.stdout.flush()
    cycle=cycle+1
    if cycle == 10 :
      print FAIL+"**  FAIL TO RECONFIGURE 10 times !  **"+ENDC
      sys.stdout.flush()
      sys.exit('*** Error!! ***')
  else :
    print OKBLUE+"**  FINISH RECONFIGURE !  **"+ENDC
    sys.stdout.flush()
    sys.exit(0)
  time.sleep(1)

time.sleep(1)

