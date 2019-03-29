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

class Setup:
  def __init__(self):

    ##################
    # Servers
    ##################
    self.SERV_DAQ    = "wagasci-daq"
    self.SERV_ANA    = "wagasci-ana"
    self.SERV_ACCESS = "wagasci-access"
    self.SERV_KYOTO  = "kyoto-hepserv"
    self.SERV_KYOTO_BACKUP  = "kyoto"

    ##################
    # Directories
    ##################
    self.SM_LOG_DIR      = "/home/data/monitor_log"
    self.ELOG_DIR        = "/home/data/e_log"
    self.SPILL_LOG_DIR   = "/home/data/spill_history"
    self.PYSCRIPT_DIR    = "/opt/pyrame/rc_scripts"
    self.RUNCMD_DIR      = "/usr/local/src/wagasci_software/RunCommand/shell"
    self.ANALYSIS_DIR    = "/usr/local/src/wagasci_software/Analysis"
    self.SLOWMONITOR_DIR = "/usr/local/src/wagasci_software/slowMonitor"
    self.ALARM_DIR       = "{0}/alarmSystem"    .format(self.SLOWMONITOR_DIR)
    self.CCC_DIR         = "{0}/cccCtrl"        .format(self.SLOWMONITOR_DIR)
    self.DATA_TRANS_DIR  = "{0}/dataTransfer"   .format(self.SLOWMONITOR_DIR)
    self.DELL_HDD_DIR    = "{0}/dellHDD"        .format(self.SLOWMONITOR_DIR)
    self.LAMBDA_DIR      = "{0}/lambdaPS"       .format(self.SLOWMONITOR_DIR)
    self.LOG_BACKUP_DIR  = "{0}/logBackup"      .format(self.SLOWMONITOR_DIR)
    self.RAW_BACKUP_DIR  = "{0}/rawDataBackup"  .format(self.SLOWMONITOR_DIR)
    self.SYSTEM_MAN_DIR  = "{0}/systemManger"   .format(self.SLOWMONITOR_DIR)
    self.SPILL_DIR       = "{0}/spillNb"        .format(self.SLOWMONITOR_DIR)
    self.TEMPERATURE_DIR = "{0}/tempSensor"     .format(self.SLOWMONITOR_DIR)
    self.TIME_SYNC_DIR   = "{0}/timeSync"       .format(self.SLOWMONITOR_DIR)
    self.WATER_DIR       = "{0}/waterSensor"    .format(self.SLOWMONITOR_DIR)
    self.WEB_KYOTO_DIR   = "{0}/webKyoto"       .format(self.SLOWMONITOR_DIR)
    self.HISTORY_DIR     = "{0}/historyGui"     .format(self.SLOWMONITOR_DIR)
    self.REMOTE_CTRL_DIR = "{0}/remoteCtrlGui"  .format(self.SLOWMONITOR_DIR)
    self.AUTO_PROC_DIR   = "{0}/autoProcess"    .format(self.SLOWMONITOR_DIR)
    self.DATA_SIZE_MON   = "{0}/datasizeMonitor".format(self.SLOWMONITOR_DIR)
    self.RUN_CTRL_DIR    = "{0}/runControl"     .format(self.SLOWMONITOR_DIR)
    self.RUN_ELOG_DIR    = "{0}/eLog"           .format(self.SLOWMONITOR_DIR)
    self.STORAGE_DIR     = "{0}/storageCheck"   .format(self.SLOWMONITOR_DIR)

    ##################
    # Log file
    ##################
    self.SLOWMONITOR_LOG  = "{0}/slowmonitor.log"   .format(self.SM_LOG_DIR)
    self.DECODE_LOG       = "{0}/decode.log"        .format(self.SM_LOG_DIR)
    self.RECON_LOG        = "{0}/recon.log"         .format(self.SM_LOG_DIR)
    self.HIST_LOG         = "{0}/hist.log"          .format(self.SM_LOG_DIR)
    self.ANAHIST_LOG      = "{0}/anahist.log"       .format(self.SM_LOG_DIR)
    self.BSD_ANA_LOG      = "{0}/bsd_analysis.log"  .format(self.SM_LOG_DIR)
    self.ALARM_LOG        = "{0}/alarm.log"         .format(self.SM_LOG_DIR) 
    self.TEMP_LOG         = "{0}/temperature.log"   .format(self.SM_LOG_DIR) 
    self.LAMBDA_LOG       = "{0}/lambda_history.log".format(self.SM_LOG_DIR) 
    self.LOG_BACKUP_HOUR  = "00" #every 0 o'clock
    self.LOG_BACKUP_TIME  =  3600 #sec
    self.LINE_MAX_SLOWMONITOR = 30000
    self.LINE_MAX_RECON       = 10000
    self.LINE_MAX_DECODE      = 10000
    self.LINE_MAX_ALARM       = 10000
    self.LINE_MAX_TEMP        = 30000
    self.LINE_MAX_LAMBDA      = 10000

    ##################
    # Alarm system
    ##################
    self.ALARM_ID         = "{0}/alarm_id.txt" .format(self.SM_LOG_DIR)  
    self.ALARM_TIME_FILEWATCH   = 1 #sec
    self.ALARM_TIME_ALARMPERIOD = 5 #sec
    self.ALARM_TIME_RSYNC       = 1 #sec
    self.ALARM_LIST  = [
      "Lambda PS",
      "Water Level",
      "CCC State",
      "Temperature",
      "Time Sync",
      "HDD Status",
      "Spill Gap"
      ]
    self.ALARM_SOUND = [ 
      "/usr/lib64/libreoffice/share/gallery/sounds/cow.wav",
      "/usr/lib64/libreoffice/share/gallery/sounds/space.wav",
      "/usr/lib64/libreoffice/share/gallery/sounds/gong.wav",
      "/usr/lib64/libreoffice/share/gallery/sounds/train.wav",
      "/usr/lib64/libreoffice/share/gallery/sounds/kongas.wav",
      "/usr/lib64/libreoffice/share/gallery/sounds/glasses.wav",
      "/usr/lib64/libreoffice/share/gallery/sounds/wallewal.wav"
      ]
    self.ALARM_SRC_ADDR = "wagasci-alarm@wagasci-login"
    self.ALARM_DST_ADDR = "nchikuma@hep.phys.s.u-tokyo.ac.jp, tamura@hep.phys.s.u-tokyo.ac.jp, kenichi@ocupc1.hep.osaka-cu.ac.jp, inoue@ocupc1.hep.osaka-cu.ac.jp, azuma@ocupc1.hep.osaka-cu.ac.jp"
    self.ALARM_MAIL_SUB = "!!!WARNING from WAGASCI!!!"

    self.ALARM_REPLYTO  = "nchikuma@hep.phys.s.u-tokyo.ac.jp"
    self.ALARM_NBLINE   = 100

    ##################
    # Lambda PS
    ##################   
    self.LAMBDA_PLOT      = "{0}/lambdaPS"           .format(self.LAMBDA_DIR) 
    self.LAMBDA_PIC1      = "{0}/lambda_history1.png".format(self.SM_LOG_DIR) 
    self.LAMBDA_PIC2      = "{0}/lambda_history2.png".format(self.SM_LOG_DIR) 
    self.LAMBDA_PIC3      = "{0}/lambda_history3.png".format(self.SM_LOG_DIR) 
    self.LAMBDA_PIC4      = "{0}/lambda_history4.png".format(self.SM_LOG_DIR) 
    self.LAMBDA_TIME_READ = 30000 #msec
    self.LAMBDA_LV_ADDR = "1" #address for Zup PS module. This should be identical to the address set at module
    self.LAMBDA_HV_ADDR = "2"

    # Current limit for HV is available about every 0.6mA, but it's not exact.
    # Ensure the exact value by measuring if you need.
    self.LAMBDA_HVCUR_LIMIT_ARRAY = ["0.0006","0.0013","0.0019","0.0026","0.0032","0.0039","0.0046","0.0052"] 

    #Nominal values for HV/LV voltage and current.
    #The current value is just for its upper limit. (Should be string)
    self.LAMBDA_NOMINAL_HVV = "56.10" #V
    self.LAMBDA_NOMINAL_HVI = self.LAMBDA_HVCUR_LIMIT_ARRAY[1] #A
    self.LAMBDA_NOMINAL_LVV = "5.000" #V
    self.LAMBDA_MAX_LVI     = "07.00" #A
    self.LAMBDA_NOMINAL_LVI = "04.50" #A

    #Accepted difference from the nominal values above
    self.LAMBDA_LIMIT_DIFF_HVV = 0.2   #V
    self.LAMBDA_LIMIT_DIFF_HVI = 0.001 #A
    self.LAMBDA_LIMIT_DIFF_LVV = 0.2   #V
    self.LAMBDA_LIMIT_DIFF_LVI = 1.0   #A

    #Parameters for ramping up/down voltage of HV/LV.
    self.LAMBDA_NUMREP_CHECK    = 5
    self.LAMBDA_VOL_STEP        = [ 5.0, 3.0] #V per TIME_TILL_RECV*3
    self.LAMBDA_VOL_PROTECT     = 0.2 #fraction to nominal
    self.LAMBDA_VOL_DIFF_LIM    = 0.3 #V 
    self.LAMBDA_TIME_TILL_RECV  = 1.0 #sec

    #Colors
    self.LAMBDA_COL_BTN_ON      = "green"
    self.LAMBDA_COL_BTN_OFF     = "red"
    self.LAMBDA_COL_STATUS_ERR  = "f6cece"
    self.LAMBDA_COL_STATUS_OK   = "cef6ce"
    self.LAMBDA_COL_STATUS_WAIT = "f6e3ce"
    self.LAMBDA_COL_STATUS_RUN  = "ceecf5"

    self.LAMBDA_CMD_LIST = [
      "ADR","DCL","RMT","RMT?","REV?","MDL?",                          # -- Initialization & ID
      "STA?","ALM?","STP?","STT?",                                     # -- Status control 
      "VOL!","CUR!","VOL?","CUR?","OUT?","OVP?","UVP?","AST?","FLD?",  # -- read Output control
      "VOL","CUR","OUT","OVP","UVP","AST","FLD"                        # -- set Output control
    ]
    self.LAMBDA_SET_CMD_LIST = ["ADR","RMT","VOL","CUR","OUT","OVP","UVP","AST","FLD"]
    self.LAMBDA_SET_CMD_FORM = [
      ["00","00"],["0","0"],["0.000","00.00"],["00.00","0.0000"],
      ["0","0"],["0.00","00.0"],["0.00","00.0"],["0","0"],["0","0"] 
    ]
    self.LAMBDA_CHECK_CMD_LIST = ["RMT?","STA?","ALM?","STP?","VOL!","CUR!","VOL?","CUR?","OUT?", "OVP?","UVP?","AST?","FLD?"]
    self.LAMBDA_CHECK_RES_LIST = ["RM","OS","AL","PS","SV","SA","AV","AA","OT","OP","UP","AS","FD"]
    self.LAMBDA_CHECK_RES_FORM = [
      ["0","0"],["00000000","00000000"],["00000","00000"],["00000","00000"],
      ["0.000","00.00"],["00.00","0.0000"],["0.000","00.00"],["00.00","0.0000"],["0","0"],
      ["0.00","00.0"],["0.00","00.0"],["0","0"],["0","0"]
    ]
    self.LAMBDA_ADDR_LIST = [self.LAMBDA_LV_ADDR,self.LAMBDA_HV_ADDR]


    #####################
    # Temperature Sensor
    #####################   
    self.TEMP_PIC1 ="{0}/temperature_history1.png".format(self.SM_LOG_DIR) 
    self.TEMP_PIC2 ="{0}/temperature_history2.png".format(self.SM_LOG_DIR) 
    self.TEMP_PIC3 ="{0}/temperature_history3.png".format(self.SM_LOG_DIR) 
    self.TEMP_PIC4 ="{0}/temperature_history4.png".format(self.SM_LOG_DIR) 
    self.TEMP_PLOT ="{0}/tempSensor"              .format(self.TEMPERATURE_DIR) 
    self.TEMP_READ ="{0}/tempSensor.sh"           .format(self.TEMPERATURE_DIR) 
    self.TEMP_TIME_FILEWATCH = 30 #sec
    self.TEMP_NOUPDATE_WARNING = 3600 #sec
    self.TEMP_TIME_READ = 10 #sec 

    #####################
    # Spill number monitor
    #####################   
    self.SPILL_PIC  ="{0}/spillnb_history.png".format(self.SM_LOG_DIR) 
    self.SPILL_LOG  ="{0}/spillNb.log"        .format(self.SPILL_DIR) 
    self.SPILL_PLOT ="{0}/spillNb"            .format(self.SPILL_DIR) 
    self.SPILL_MAXLINE   = 100
    self.SPILL_TIME_PLOT = 3000 #msec 

    #####################
    # CCC control
    #####################   
    self.CCC_SCRIPT_DIR   = "{0}/script"      .format(self.CCC_DIR)
    self.CCC_UPDATE_TIME  = 600000 #msec   
    self.CCC_COL_BTN_ON  = "green"
    self.CCC_COL_BTN_OFF = "red"
    self.CCC_COL_STATUS_ERR  = "f6cece"
    self.CCC_COL_STATUS_OK   = "cef6ce"
    self.CCC_COL_STATUS_WAIT = "f6e3ce"
    self.CCC_COL_STATUS_RUN  = "ceecf5"

    #####################
    # Water level sensor
    #####################   
    self.WATER_LOG  ="{0}/WAGASCI.csv"            .format(self.SM_LOG_DIR) 
    self.WATER_PIC1 ="{0}/waterlevel_history1.png".format(self.SM_LOG_DIR) 
    self.WATER_PIC2 ="{0}/waterlevel_history2.png".format(self.SM_LOG_DIR) 
    self.WATER_PIC3 ="{0}/waterlevel_history3.png".format(self.SM_LOG_DIR) 
    self.WATER_PIC4 ="{0}/waterlevel_history4.png".format(self.SM_LOG_DIR) 
    self.WATER_PLOT ="{0}/waterSensor"            .format(self.WATER_DIR)
    self.WATER_TIME_FILEWATCH = 30 #sec
    self.WATER_NOUPDATE_WARNING = 3600 #sec

    ########################
    # Data copy from DAQ PC
    ########################
    self.RAWDATA_SERV  = "wagasci-daq"
    self.RAWDATA_DIR   = "/home/data/prototech/wagasci"
    self.RUNID_FILE    = "/opt/calicoes/config/runid.txt"
    self.ACQID_FILE    = "/opt/calicoes/config/acqid.txt"
    self.RUNNAME       = "run"
    self.BACKUPDATA_DIR = "/home/data/daqdata"
    self.ID_DIR         = "/home/data/runid"
    self.COPY_RUNID_FILE    = "{0}/runid.txt".format(self.ID_DIR)
    self.COPY_ACQID_FILE    = "{0}/acqid.txt".format(self.ID_DIR)
    self.COPY_DONE_ID_FILE  = "{0}/copy_done_runid.txt".format(self.ID_DIR)
    self.COPY_UPDATE_PERIOD = 300 #sec

    #####################
    # HDD Status
    #####################
    self.HDD_CHECK = "{0}/script/CheckPdisk.sh".format(self.DELL_HDD_DIR)
    self.HDD_TIME_LOOP = 3600 #sec

    #####################
    # Storage check
    #####################
    self.STORAGE_FILE_DAQ    = "{0}/storage_daq.log"   .format(self.STORAGE_DIR)
    self.STORAGE_FILE_ANA    = "{0}/storage_ana.log"   .format(self.STORAGE_DIR)
    self.STORAGE_FILE_ACCESS = "{0}/storage_access.log".format(self.STORAGE_DIR)
    self.STORAGE_PLOT        = "{0}/storageCheck"      .format(self.STORAGE_DIR)
    self.STORAGE_PIC         = "{0}/storage.png"       .format(self.SM_LOG_DIR)
    self.STORAGE_CHECK_TIME = 3600 #sec

    #####################
    # Server time sync
    #####################
    self.SERV_TIME_CHECK_HOUR = "13" #every 2 o'clock
    self.SERV_TIME_CHECK_TIME = 3600 #sec
    self.MAX_TIME_DIFF = 2

    ########################
    # Auto process
    ########################
    self.CALIB_ID_FILE     = "{0}/calib_id.txt".format(self.ID_DIR)
    self.DECODE_DATA_DIR   = "/home/data/decode"
    self.HIST_DATA_DIR     = "/home/data/hist"
    self.RECON_DATA_DIR    = "/home/data/recon"
    self.CALIB_DIR         = "/home/data/calibration"
    self.DQ_MERGE_DIR      = "/home/data/dq_merge"
    self.MERGE_DIR         = "/home/data/merge"
    self.BSD_DIR           = "/home/data/bsd"
    self.XML_DATA_DIR      = "/home/data/xmlfile"
    self.DQ_HISTORY_DIR    = "/home/data/dq_history"
    self.AUTO_RUNID_LIST   = "{0}/auto_process_runid_list.txt".format(self.ID_DIR)
    self.PROCESS_DECODE    = "{0}/bin/Decoder"         .format(self.ANALYSIS_DIR)
    self.PROCESS_HIST      = "{0}/bin/wgMakeHist"      .format(self.ANALYSIS_DIR)
    self.PROCESS_RECON     = "{0}/bin/wgRecon"         .format(self.ANALYSIS_DIR)
    self.PROCESS_ANAHIST   = "{0}/bin/wgAnaHist"       .format(self.ANALYSIS_DIR)
    self.PROCESS_ANAHISTSUM= "{0}/bin/wgAnaHistSummary".format(self.ANALYSIS_DIR)
    self.PROCESS_DQCHECK   = "{0}/bin/wgDQCheck"       .format(self.ANALYSIS_DIR)
    self.PROCESS_DQHISTORY = "{0}/bin/wgDQHistory"     .format(self.ANALYSIS_DIR)
    self.BSD_SPILLCHECK    = "{0}/bin/wgBsdSpillCheck" .format(self.ANALYSIS_DIR)
    self.SPILL_CHECK       = "{0}/bin/wgSpillCheck"    .format(self.ANALYSIS_DIR)
    self.SPILL_EFF         = "{0}/bin/wgSpillEff"      .format(self.ANALYSIS_DIR)
    self.MAX_PROCESS_THREAD = 3
    self.RUN_STATUS_PIC     = "{0}/run_status.png".format(self.SM_LOG_DIR)
    self.RUN_STATUS_PLOT    = "{0}/processStatus" .format(self.AUTO_PROC_DIR)
    self.BACKUP_KYOTO_DIR   = "/export/scraid4/data1/wagasci_daq"
    self.BACKUP_KYOTO_RUNID = "{0}/backup_kyoto_runid_list.txt".format(self.ID_DIR)
    self.BACKUP_KYOTO_TIME  = 3600 #sec every 1hour
    self.BSD_RSYNC_TIME     = 1200 #sec every 20min
    self.BSD_FILENUM        = "{0}/bsd_filenum.txt".format(self.ID_DIR)

    #####################
    # Kyoto hep serv
    #####################
    self.KYOTO_TIME_RSYNC = 1200 #sec
    self.KYOTO_WEB_LOCAL = "{0}/web_page".format(self.WEB_KYOTO_DIR)
    self.KYOTO_WEB_DIR   = "/mnt/hep_web/hep_web/member/ingrid/wagasci_monitor"
    self.KYOTO_WEB_LOG   = "/mnt/hep_web/hep_web/member/ingrid/wagasci_monitor/log"
    self.KYOTO_WEB_ADDR  = "https://www-he.scphys.kyoto-u.ac.jp/member/ingrid/wagasci_monitor"
    self.KYOTO_LOG_ZIP   = "log_figure.tgz"
    self.KYOTO_DQ_ZIP  = "dq_figure.tgz"

    #####################
    # Run Control
    #####################
    self.CALIB_CMD   = "{0}/calibration_run_new.sh".format(self.RUNCMD_DIR)
    self.WAGASCI_RUN = "{0}/wagasci_run.py"        .format(self.PYSCRIPT_DIR)
    self.STOP_SCRIPT = "{0}/stop_script.py"        .format(self.PYSCRIPT_DIR)
    self.RUNCTRL_LOG = "{0}/runcontrol.log"        .format(self.RUN_CTRL_DIR)

    #####################
    # e-Log System
    #####################
    self.ELOG_YEAR   = range(2017,2030)
    self.ELOG_MONTH  = range(0,13)
    self.ELOG_DAY    = range(0,32)
    self.ELOG_HOUR   = range(0,24)
    self.ELOG_MINUTE = range(0,60)
    self.ELOG_CATEGORY = ["Run status","Calibration","Power supply","Other hardware","Software","Others"]
    self.ELOG_ID     = "{0}/elog_id.txt".format(self.ELOG_DIR)
    self.ELOG_SRC_ADDR = "wagasci-elog@wagasci-login"
    self.ELOG_DST_ADDR = "nchikuma@hep.phys.s.u-tokyo.ac.jp, tamura@hep.phys.s.u-tokyo.ac.jp, kenichi@ocupc1.hep.osaka-cu.ac.jp, inoue@ocupc1.hep.osaka-cu.ac.jp, azuma@ocupc1.hep.osaka-cu.ac.jp"
    self.ELOG_REPLYTO  = "nchikuma@hep.phys.s.u-tokyo.ac.jp"

    #####################
    # System manager
    #####################
    self.MANAGER_SYSTEM_NAME = [
      "RunCtrl & e-Log",
      "Slow Monitor",
      "History Plots",
      "Auto Analysis",
      "Auto Data Quality",
      "Auto BSD Process",
      "Rsync Raw Data",
      "Backup Kyoto",
      "Backup KEKCC",
      "Rsync Alarm Log",
      "Web Upload",
      "HDD Check",
      "Log Backup",
      "Time Sync",
      "Running Raw Data",
      "Spill Number"
      ]
    self.MANAGER_SYSTEM_LIST = [  #The order must be identical to those in SYSTEM_NAME
      "{0}/gui_eLog.py"         .format(self.RUN_ELOG_DIR),    #"RunCtrl & e-Log"
      "{0}/gui_remoteCtrl.py"   .format(self.REMOTE_CTRL_DIR), #"Slow Monitor"
      "{0}/gui_history.py"      .format(self.HISTORY_DIR),     #"History Plots"
      "{0}/auto_process.py"     .format(self.AUTO_PROC_DIR),   #"Auto Analysis"
      "{0}/auto_dq_history.py"  .format(self.AUTO_PROC_DIR),   #"Auto Data Quality"
      "{0}/auto_bsd_analysis.py".format(self.AUTO_PROC_DIR),   #"Auto BSD Process"
      "{0}/rsync_rawdata.py"    .format(self.AUTO_PROC_DIR),   #"Rsync Raw Data"
      "{0}/backup_Kyoto.py"     .format(self.AUTO_PROC_DIR),   #"Backup Kyoto"
      "{0}/backup_KEKCC.py"     .format(self.AUTO_PROC_DIR),   #"Backup KEKCC"
      "{0}/rsync_alarm.py"      .format(self.ALARM_DIR),       #"Rsync Alarm Log"
      "{0}/rsync_webKyoto.py"   .format(self.WEB_KYOTO_DIR),   #"Web Upload"
      "{0}/run_HDDcheck.py"     .format(self.DELL_HDD_DIR),    #"HDD Check"
      "{0}/run_logBackup.py"    .format(self.LOG_BACKUP_DIR),  #"Log Backup"
      "{0}/run_timeCheck.py"    .format(self.TIME_SYNC_DIR),   #"Time Sync"
      "{0}/datasizeMonitor"     .format(self.DATA_SIZE_MON),   #"Running Raw Data"
      "{0}/gui_spillNb.py"      .format(self.SPILL_DIR)        #"Spill Number"
      ]
    self.MANAGER_TIME_STATECHECK = 5 #sec
    self.MANAGER_LISTFILE = "/usr/local/src/wagasci_software/runControl/monitor_list_ana.sh"
    self.MANAGER_CHECK="/usr/local/src/wagasci_software/runControl/check_monitor_ana.sh"
    self.MANAGER_START="/usr/local/src/wagasci_software/runControl/start_monitor_ana.sh"
    self.MANAGER_STOP ="/usr/local/src/wagasci_software/runControl/stop_monitor_ana.sh"
    self.MANAGER_COL_BTN_OK = "green"
    self.MANAGER_COL_BTN_NG  = "red"
    self.MANAGER_COL_BTN_UNKNOWN  = "yellow"

    ####################
    # Geometry
    #####################   
    self.HIST_SIZE_X    = 600
    self.HIST_SIZE_Y    = 600
    self.CTRL_SIZE_X    = 600
    self.CTRL_SIZE_Y    = 600
    self.ELOG_SIZE_X    = 600
    self.ELOG_SIZE_Y    = 600
    self.SPILL_SIZE_X   = 250
    self.SPILL_SIZE_Y   = 250
    self.ALARM_SIZE_X   = 300
    self.ALARM_SIZE_Y   = 300
    self.MANAGER_SIZE_X = 300
    self.MANAGER_SIZE_Y = 300

    self.HIST_POS_X    = 0
    self.HIST_POS_Y    = 0
    self.CTRL_POS_X    = 650
    self.CTRL_POS_Y    = 0
    self.SPILL_POS_X   = 280
    self.SPILL_POS_Y   = 780
    self.ALARM_POS_X   = 1610
    self.ALARM_POS_Y   = 720
    self.MANAGER_POS_X = 1300
    self.MANAGER_POS_Y = 720
    self.ELOG_POS_X    = 1300
    self.ELOG_POS_Y    = 0


    self.RUNCTRL_SIZE_X = 400
    self.RUNCTRL_SIZE_Y = 200
    self.WATER_SIZE_X = 600
    self.WATER_SIZE_Y = 800
    self.TEMP_SIZE_X = 600
    self.TEMP_SIZE_Y = 800
    self.LAMBDA_CTRL_SIZE_X = 600
    self.LAMBDA_CTRL_SIZE_Y = 800
    self.LAMBDA_HIST_SIZE_X = 600
    self.LAMBDA_HIST_SIZE_Y = 800
    self.CCC_SIZE_X = 600
    self.CCC_SIZE_Y = 800

    self.RUNCTRL_POS_X = 1300
    self.RUNCTRL_POS_Y = 550
    self.WATER_POS_X = 0 
    self.WATER_POS_Y = 0
    self.TEMP_POS_X = 0
    self.TEMP_POS_Y = 0
    self.LAMBDA_CTRL_POS_X = 0
    self.LAMBDA_CTRL_POS_Y = 0
    self.LAMBDA_HIST_POS_X = 0
    self.LAMBDA_HIST_POS_Y = 0
    self.CCC_POS_X = 0
    self.CCC_POS_Y = 0



  def set_alarm(self,alarm=""):
    if alarm in self.ALARM_LIST:
      if not os.path.isfile(self.ALARM_LOG):
        subprocess.call("echo -e "" > {0}".format(ALARM_LOG),shell=True)
      timeutc = datetime.datetime.today().strftime("%s")
      cmd="sed -i '1s/^/{0}\/{1}\\n/' {2}".format(timeutc,alarm,self.ALARM_LOG)
      subprocess.call(cmd,shell=True)

  def insertstr(self,s="",pos=-1,x=""):
    return x.join([s[:pos],s[pos:]])

  def str2ascii(self,string=""):
    tmp = binascii.hexlify(string)
    for i in xrange(len(tmp)-2, 0, -2):
      tmp = self.insertstr(tmp,i,'\\x')
    return str('\\x'+tmp)

  def set_process_state(self,runid=-1,acqid=-1,ini=-1,fin=-1):
    cmd = "sed -i 's/%05d %03d %d/%05d %03d %d/' %s"%(
        runid,acqid,ini,
        runid,acqid,fin,
        self.AUTO_RUNID_LIST)
    subprocess.call(cmd,shell=True)

  def get_process_state(self,runid=-1,acqid=-1):
    cmd = "cat %s | grep '%05d %03d'"%(self.AUTO_RUNID_LIST,runid,acqid)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result = str(res.communicate()[0].replace("\n","")).split()
    if len(result)!=4 or (not result[2].isdigit()):
      return -1
    else:
      return int(result[2])

  def get_calibname(self,runid=-1,acqid=-1):
    cmd = "cat %s | grep '%05d %03d'"%(self.AUTO_RUNID_LIST,runid,acqid)
    res = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE)
    result = str(res.communicate()[0].replace("\n","")).split()
    if len(result)!=4:
      return None
    else:
      return result[3]


  def __enter__(self):
    return self

  def __exit__(self,exc_type,exc_value,traceback):
    return True
