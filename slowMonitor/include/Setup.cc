#include "Setup.h"

void set_alarm(const std::string name)
{
  std::ifstream ifs(ALARM_LOG);
  bool is_exist = ifs.is_open();
  ifs.close();
  if(!is_exist){
    std::ofstream ofs(ALARM_LOG);
    ofs << "" << std::endl;
    ofs.close();
  }

  struct tm tm;
  time_t t = time(NULL);
  localtime_r(&t, &tm);
  time_t unixtime = mktime(&tm);

  char* cmd = Form("sed -i '1s/^/%d\\/%s\\n/' %s",(int)unixtime,name.c_str(),ALARM_LOG);
  system(cmd);
  return;
}

void set_logger(
    const std::string filename,
    const std::string log_type,
    const std::string msg
    )
{
  struct tm tm;
  char buf[50];
  time_t t = time(NULL);
  localtime_r(&t, &tm);

  std::string time_info;
  std::string str = asctime_r(&tm,buf);
  std::istringstream sstr(str);
  getline(sstr,time_info);

  std::ofstream ofslog(SLOWMONITOR_LOG, std::ios::app);
  ofslog 
    << "[" << time_info << "]" 
    << "[" << filename  << "]" 
    << "[" << log_type  << "]";
  ofslog << msg << std::endl;
  ofslog.close();
}
