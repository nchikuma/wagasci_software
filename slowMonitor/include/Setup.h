#ifndef __SETUP_SLOWMONITOR_H__
#define __SETUP_SLOWMONITOR_H__


// ############################################################################################
// #  Here are a part of the fixed parameters used in the slow monitor system.                #
// #  These paramters could be used to compile C++ pragrams.                                  #
// #  These must be identical to the other setting file "setup.py".                           #
// #                                                                                          #
// #  2017/09/23                                                                              #
// #  Naruhiro Chikuma                                                                        #
// #  The University of Tokyo                                                                 #
// #                                                                                          #
// ############################################################################################
  
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <fstream>
#include <vector>
#include <deque>
#include <string.h>
#include <sstream>
#include <TGraph.h>
#include <TGraph2D.h>
#include <TCanvas.h>
#include <TGaxis.h>
#include <TFrame.h>
#include <TH1.h>
#include <TH2.h>
#include <TROOT.h>
#include <TApplication.h>
#include <TStyle.h>
#include <TLegend.h>
#include <TText.h>

#define SLOWMONITOR_DIR "/usr/local/src/wagasci_software/slowMonitor"

#define SLOWMONITOR_LOG "/home/data/monitor_log/slowmonitor.log"
#define ALARM_LOG       "/home/data/monitor_log/alarm.log"
#define AUTO_RUNID_LIST "/home/data/runid/auto_process_runid_list.txt"
#define RUN_STATUS_PIC  "/home/data/monitor_log/run_status.eps"
#define ALARM_ON

#define EPS2PNG         "/usr/local/src/wagasci_software/slowMonitor/script/eps2png.sh"
#define CANVAS_X 300
#define CANVAS_Y 300
#define CANVAS_X2 250
#define CANVAS_Y2 230
#define CONV_X CANVAS_X*0.25
#define CONV_Y CANVAS_Y*0.25

#define LAMBDA_LOG      "/home/data/monitor_log/lambda_history.log"
#define LAMBDA_PIC1     "/home/data/monitor_log/lambda_history1.eps"
#define LAMBDA_PIC2     "/home/data/monitor_log/lambda_history2.eps"
#define LAMBDA_PIC3     "/home/data/monitor_log/lambda_history3.eps"
#define LAMBDA_PIC4     "/home/data/monitor_log/lambda_history4.eps"
//these will be converted into png
#define LAMBDA_TIME1 600    //sec //10 min //updated every 30sec
#define LAMBDA_TIME2 3600   //sec //1 hour
#define LAMBDA_TIME3 86400  //sec //1 day
#define LAMBDA_TIME4 259200 //sec //3 days
#define LAMBDA_NUMCH 8
#define LAMBDA_NUMPLOT 4
#define LAMBDA_HV_MAX 100.0
#define LAMBDA_HV_MIN 0.0
#define LAMBDA_LV_MAX 10.0
#define LAMBDA_LV_MIN 0.0
#define LAMBDA_NORM_CUR_HV 1.0e+4
#define LAMBDA_NORM_CUR_LV 1.0
#define LAMBDA_COLOR_VOL 61
#define LAMBDA_COLOR_OVP 81
#define LAMBDA_COLOR_UVP 71
#define LAMBDA_COLOR_CUR 91
#define LAMBDA_MAKER_STYLE 11

#define TEMP_LOG  "/home/data/monitor_log/temperature.log"
#define TEMP_PIC1 "/home/data/monitor_log/temperature_history1.eps"
#define TEMP_PIC2 "/home/data/monitor_log/temperature_history2.eps"
#define TEMP_PIC3 "/home/data/monitor_log/temperature_history3.eps"
#define TEMP_PIC4 "/home/data/monitor_log/temperature_history4.eps"
#define TEMP_PIC_ALL "/home/data/monitor_log/temperature_history_all.eps"
//these will be converted into png
#define TEMP_NUMPLOT 4
#define TEMP_NUM1 60    //10 min //updated every 10sec
#define TEMP_NUM2 360   //1 hour
#define TEMP_NUM3 8640  //1 day
#define TEMP_NUM4 25920 //3 days
#define TEMP_NUMCH 4
#define TEMP_NOMINAL_TEMP0 20.0 //deg C
#define TEMP_NOMINAL_TEMP1 20.0 //deg C
#define TEMP_NOMINAL_HUMI0 35.0 //%
#define TEMP_NOMINAL_HUMI1 25.0 //%
#define TEMP_LIMIT_DIF_TEMP0 5.0  //def C
#define TEMP_LIMIT_DIF_TEMP1 5.0  //def C
#define TEMP_LIMIT_DIF_HUMI0 20.0 //%
#define TEMP_LIMIT_DIF_HUMI1 20.0 //%
#define TEMP_MASK0 false
#define TEMP_MASK1 false
#define TEMP_MASK2 false
#define TEMP_MASK3 false
#define TEMP_MAX_RANGE_TEMP 30.0
#define TEMP_MIN_RANGE_TEMP 10.0
#define TEMP_MAX_RANGE_HUMI 90.0
#define TEMP_MIN_RANGE_HUMI 00.0
#define TEMP_COLOR0 94
#define TEMP_COLOR1 59
#define TEMP_COLOR2 99
#define TEMP_COLOR3 69
#define TEMP_MAKER_STYLE 11
#define TEMP_FONT1 62
#define TEMP_FONT2 25
#define TEMP_FONT3 25
#define TEMP_LABEL_FONT 62

#define WATER_LOG  "/home/data/monitor_log/WAGASCI.csv"
#define WATER_PIC1 "/home/data/monitor_log/waterlevel_history1.eps" 
#define WATER_PIC2 "/home/data/monitor_log/waterlevel_history2.eps"
#define WATER_PIC3 "/home/data/monitor_log/waterlevel_history3.eps"
#define WATER_PIC4 "/home/data/monitor_log/waterlevel_history4.eps"
//these will be converted into png
#define WATER_NUMPLOT 4
#define WATER_NUM1 30    //10 min //updated every 20sec
#define WATER_NUM2 180   //1 hour
#define WATER_NUM3 4320  //1 day
#define WATER_NUM4 12960 //3 days
#define WATER_NUMCH 10
#define WATER_THRES0 2.0 //2.5 //V
#define WATER_THRES1 2.0 //2.5 //V
#define WATER_THRES2 2.0 //2.5 //V
#define WATER_THRES3 2.0 //2.5 //V
#define WATER_THRES4 2.0 //2.5 //V
#define WATER_THRES5 2.0 //2.5 //V
#define WATER_THRES6 2.0 //2.5 //V
#define WATER_THRES7 2.0 //2.5 //V
#define WATER_THRES8 2.0 //2.5 //V
#define WATER_THRES9 2.0 //2.5 //V
#define WATER_MASK0 false // MASK0 for CH1 of the data logger
#define WATER_MASK1 true 
#define WATER_MASK2 false
#define WATER_MASK3 false
#define WATER_MASK4 false
#define WATER_MASK5 false
#define WATER_MASK6 true
#define WATER_MASK7 false
#define WATER_MASK8 true
#define WATER_MASK9 true
#define WATER_COLOR0 59  // COLOR0 for CH1 of the data logger
#define WATER_COLOR1 68
#define WATER_COLOR2 71
#define WATER_COLOR3 77
#define WATER_COLOR4 88
#define WATER_COLOR5 91
#define WATER_COLOR6 95
#define WATER_COLOR7 99
#define WATER_COLOR8 51
#define WATER_COLOR9 7
#define WATER_MAKER_STYLE 11
#define WATER_MIN -4.0 //V
#define WATER_MAX  4.0 //V
#define WATER_FONT1 62
#define WATER_FONT2 25
#define WATER_FONT3 25
#define WATER_LABEL_FONT 62

#define RAWDATASIZE1 "/usr/local/src/wagasci_software/slowMonitor/datasizeMonitor/filesize1.log"
#define RAWDATASIZE2 "/usr/local/src/wagasci_software/slowMonitor/datasizeMonitor/filesize2.log"

#define SPILL_LOG "/usr/local/src/wagasci_software/slowMonitor/spillNb/spillNb.log"
#define SPILL_MAXLINE 100
#define SPILL_PIC "/home/data/monitor_log/spillnb_history.png"

#define STORAGE_FILE_DAQ    "/usr/local/src/wagasci_software/slowMonitor/storageCheck/storage_daq.log"
#define STORAGE_FILE_ANA    "/usr/local/src/wagasci_software/slowMonitor/storageCheck/storage_ana.log"
#define STORAGE_FILE_ACCESS "/usr/local/src/wagasci_software/slowMonitor/storageCheck/storage_access.log"
#define STORAGE_PIC         "/home/data/monitor_log/storage.png"



void set_alarm(const std::string name);
#define ALARM_LIST_LAMBDA "Lambda PS"
#define ALARM_LIST_WATER  "Water Level"
#define ALARM_LIST_CCC    "CCC State"
#define ALARM_LIST_TEMP   "Temperature"
#define ALARM_LIST_TIME   "Time Sync"
#define ALARM_LIST_HDD    "HDD Status"
#define ALARM_LIST_SPILL  "Spill Gap"

void set_logger(const std::string filename,const std::string log_type,const std::string msg);
#define ALARM_TYPE_DEBUG    "DEBUG"
#define ALARM_TYPE_INGO     "INFO"
#define ALARM_TYPE_WARNING  "WARNING"
#define ALARM_TYPE_ERROR    "ERROR"
#define ALARM_TYPE_CRITICAL "CRITICAL"


#endif
