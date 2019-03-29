#include "../include/Setup.h"

#define FILENAME "tempSensor.cc"

void ReadFile(
    std::string& filename,
    std::vector<double> &xx,
    std::vector<std::vector<double>> &yy,
    std::string &current_time,
    int mode=0);

int main(int argc,char* argv[]){


  int mode = 0;
  int start_year = -1;
  int stop_year  = -1;
  int start_mon  = -1;
  int stop_mon   = -1;
  int start_day  = -1;
  int stop_day   = -1;
  if(argc==4){
    std::string mode_str  = argv[1];
    std::string start_str = argv[2];
    std::string stop_str  = argv[3];
    if(mode_str=="all"&&start_str.size()==8&&stop_str.size()==8){
      mode = 1;
      start_year = atoi(start_str.substr(0,4).c_str());
      start_mon  = atoi(start_str.substr(4,2).c_str());
      start_day  = atoi(start_str.substr(6,2).c_str());
      stop_year  = atoi(stop_str .substr(0,4).c_str());
      stop_mon   = atoi(stop_str .substr(4,2).c_str());
      stop_day   = atoi(stop_str .substr(6,2).c_str());
      std::cout << "start_year =" << start_year << std::endl;
      std::cout << "start_mon  =" << start_mon  << std::endl;
      std::cout << "start_day  =" << start_day  << std::endl;
      std::cout << "stop_year  =" << stop_year  << std::endl;
      std::cout << "stop_mon   =" << stop_mon   << std::endl;
      std::cout << "stop_day   =" << stop_day   << std::endl;

    }
    else{
      std::cout << "Usage:" << std::endl;
      std::cout << argv[0] << std::endl;
      std::cout << argv[0] << " all < start (yyyymmdd)> < stop (yyyymmdd)>" << std::endl;
      return 0;
    }
  }
  else if(argc!=1){
    std::cout << "Usage:" << std::endl;
    std::cout << argv[0] << std::endl;
    std::cout << argv[0] << " all < start (yyyymmdd)> < stop (yyyymmdd)>" << std::endl;
    return 0;
  }


  std::vector<double> xx;
  std::vector<std::vector<double> > yy(TEMP_NUMCH);
  std::string current_time;

  if(mode==0){
    std::string filename = TEMP_LOG;
    ReadFile(filename,xx,yy,current_time);
  }
  else if(mode==1){
    int iy=start_year;
    int im=start_mon;
    int id=start_day;
    while(true){
      std::string filename
        = Form("/home/data/monitor_log/%04d%02d%02d/temperature.log",iy,im,id);
      ReadFile(filename,xx,yy,current_time,mode);

      if(iy>=stop_year&&im>=stop_mon&&id>=stop_day){break;}
      if(id==31){
        id = 1;
        if(im==12){im=1;iy++;}
        else{im++;}
      }
      else{id++;}
    }
  }

  //for(int i=0;i<(int)xx.size();i++){
  //  std::cout << xx[i] 
  //    << " " << yy[0][i] 
  //    << " " << yy[1][i] 
  //    << " " << yy[2][i] 
  //    << " " << yy[3][i] 
  //    << std::endl;
  //}

#ifdef ALARM_ON
  bool alarm_on = false;
  std::vector<int> alarm_ch;
  double current_temp0 = yy[0].back();
  double current_humi0 = yy[1].back();
  double current_temp1 = yy[2].back();
  double current_humi1 = yy[3].back();
  if((!TEMP_MASK0)&&(fabs(current_temp0-TEMP_NOMINAL_TEMP0)>TEMP_LIMIT_DIF_TEMP0))
  {alarm_on=true;alarm_ch.push_back(0);}
  if((!TEMP_MASK1)&&(fabs(current_humi0-TEMP_NOMINAL_HUMI0)>TEMP_LIMIT_DIF_HUMI0))
  {alarm_on=true;alarm_ch.push_back(1);}
  if((!TEMP_MASK2)&&(fabs(current_temp1-TEMP_NOMINAL_TEMP1)>TEMP_LIMIT_DIF_TEMP1))
  {alarm_on=true;alarm_ch.push_back(2);}
  if((!TEMP_MASK3)&&(fabs(current_humi1-TEMP_NOMINAL_HUMI1)>TEMP_LIMIT_DIF_HUMI1))
  {alarm_on=true;alarm_ch.push_back(3);}
  if(alarm_on){
    int j=0;
    std::string msg;
    while(j<(int)alarm_ch.size()){
      if     (alarm_ch[j]==0){
        msg = Form("Temp0=%3.1f (Allowed %3.1f +/- %3.1f)",current_temp0,TEMP_NOMINAL_TEMP0,TEMP_LIMIT_DIF_TEMP0);
        set_logger(FILENAME,ALARM_TYPE_ERROR,msg);
      }
      else if(alarm_ch[j]==1){
        msg = Form("Humi0=%3.1f (Allowed %3.1f +/- %3.1f)",current_humi0,TEMP_NOMINAL_HUMI0,TEMP_LIMIT_DIF_HUMI0);
        set_logger(FILENAME,ALARM_TYPE_ERROR,msg);
      }
      else if(alarm_ch[j]==2){
        msg = Form("Temp1=%3.1f (Allowed %3.1f +/- %3.1f)",current_temp1,TEMP_NOMINAL_TEMP1,TEMP_LIMIT_DIF_TEMP1);
        set_logger(FILENAME,ALARM_TYPE_ERROR,msg);
      }
      else if(alarm_ch[j]==3){
        msg = Form("Humi1=%3.1f (Allowed %3.1f +/- %3.1f)",current_humi1,TEMP_NOMINAL_HUMI1,TEMP_LIMIT_DIF_HUMI1);
        set_logger(FILENAME,ALARM_TYPE_ERROR,msg);
      }
      j++;
    }
    set_alarm(ALARM_LIST_TEMP);
  }
#endif

  int data_point = (int)xx.size();
  int num_plot = 1;
  if(mode==0) num_plot = TEMP_NUMPLOT;
  for(int i=0;i<num_plot;i++){
    int npoint;
    std::string picname;
    if(mode==0){
      switch(i){
        case 0: npoint=TEMP_NUM1;picname=TEMP_PIC1;break;
        case 1: npoint=TEMP_NUM2;picname=TEMP_PIC2;break;
        case 2: npoint=TEMP_NUM3;picname=TEMP_PIC3;break;
        case 3: npoint=TEMP_NUM4;picname=TEMP_PIC4;break;
        default: std::cout << "Too many plots" << std::endl; return 1; break;
      }
    }
    else if(mode==1){
      npoint  = data_point;
      picname = TEMP_PIC_ALL;
    }
    TCanvas *c1 = new TCanvas("c1","c1",CANVAS_X,CANVAS_Y);
    c1->cd(0);
    TGraph *g1[TEMP_NUMCH];
    TLegend *leg1  = new TLegend(0.7,0.72,0.89,0.9);
    leg1->SetFillStyle(0);
    leg1->SetBorderSize(0);
    leg1->SetTextFont(TEMP_FONT1);
    TLegend *leg2[TEMP_NUMCH], *leg3;
    double min1=TEMP_MIN_RANGE_TEMP; double max1=TEMP_MAX_RANGE_TEMP;
    double min2=TEMP_MIN_RANGE_HUMI; double max2=TEMP_MAX_RANGE_HUMI;
    double norm0 = (max1-min1)/(max2-min2);
    double offs0 = min1-min2*norm0;
    for(int j=0;j<TEMP_NUMCH;j++){
      if(mode==1&&(j==1||j==3)){continue;}
      int color;
      std::string name="", title="",opt="";
      double norm = 1.0;
      double offs  = 0.0;
      switch(j){
        case 0: color=TEMP_COLOR0;name="TEMP1 " ;opt="APL"    ;norm=1.00 ;offs=0.0  ;break;
        case 1: color=TEMP_COLOR1;name="HUMID1" ;opt="PL same";norm=norm0;offs=offs0;break;
        case 2: color=TEMP_COLOR2;name="TEMP2 " ;opt="PL same";norm=1.00 ;offs=0.0  ;break;
        case 3: color=TEMP_COLOR3;name="HUMID2" ;opt="PL same";norm=norm0;offs=offs0;break;
        default: std::cout << "Too many channels" << std::endl; return 1; break;
      }
      if(data_point<npoint) npoint=data_point;
      g1[j] = new TGraph(npoint);
      for(int k=0;k<npoint;k++){
        g1[j]->SetPoint(k,
            xx[data_point-npoint+k],
            yy[j][data_point-npoint+k]*norm+offs);
      }
      if     (mode==0) g1[j]->SetMarkerSize(0.5);
      else if(mode==1) g1[j]->SetMarkerSize(0.1);
      g1[j]->SetMarkerStyle(TEMP_MAKER_STYLE);
      g1[j]->SetMarkerColor(color);
      g1[j]->SetLineColor  (color);
      g1[j]->GetXaxis()->SetTimeDisplay(1);
      g1[j]->GetXaxis()->SetTimeFormat("#splitline{%Y/%m/%d}{%H:%M}");
      g1[j]->GetXaxis()->SetTimeOffset(0,"jst");
      g1[j]->GetXaxis()->SetLabelOffset(0.03);
      g1[j]->GetYaxis()->SetLabelOffset(100);
      g1[j]->GetXaxis()->SetLabelSize(0.02);
      g1[j]->SetTitle(title.c_str());
      g1[j]->SetMaximum(max1); 
      g1[j]->SetMinimum(min1);
      g1[j]->Draw(opt.c_str());
      leg1->AddEntry(g1[j],name.c_str(),"p");
      std::string data_text,data_suffix;
      double leg2_x, leg2_y;
      switch(j){
        case 0: data_text="Temp1";data_suffix="C";leg2_x=0.15;leg2_y=0.70;break;
        case 1: data_text="Humi1";data_suffix="%";leg2_x=0.35;leg2_y=0.70;break;
        case 2: data_text="Temp2";data_suffix="C";leg2_x=0.15;leg2_y=0.75;break;
        case 3: data_text="Humi2";data_suffix="%";leg2_x=0.35;leg2_y=0.75;break;
        default: std::cout << "Too many channels" << std::endl; return 1; break;
      }
      data_text += Form(":%4.2f ",yy[j].back());
      data_text += data_suffix;
      leg2[j] = new TLegend(leg2_x,leg2_y,leg2_x+0.15,leg2_y+0.05);
      leg2[j]->SetFillStyle(0);
      leg2[j]->SetBorderSize(0);
      leg2[j]->SetHeader(data_text.c_str());
      leg2[j]->SetTextSize(0.03);
      leg2[j]->SetTextFont(TEMP_FONT2);
      leg2[j]->Draw();
    }
    leg3 = new TLegend(0.15,0.80,0.35,0.85);
    leg3->SetFillStyle(0);
    leg3->SetBorderSize(0);
    leg3->SetHeader(current_time.c_str());
    leg3->SetTextSize(0.03);
    leg3->SetTextFont(TEMP_FONT3);
    leg3->Draw();

    double x1  = g1[0]->GetXaxis()->GetBinLowEdge(1);
    double x2  = g1[0]->GetXaxis()->GetBinUpEdge(g1[0]->GetXaxis()->GetNbins());
    TGaxis* axis1 = new TGaxis(x1,min1,x1,max1,min1,max1,510,"");
    axis1->SetLineColor(TEMP_COLOR0);
    axis1->SetTitle("Temparature [deg C]");
    axis1->Draw();
    axis1 = new TGaxis(x2,min1,x2,max1,min2,max2,510,"+L");
    axis1->SetTitle("Humidity [%]");
    axis1->SetLineColor(TEMP_COLOR3);
    axis1->Draw();
    leg1->Draw();
    c1->Print(picname.c_str());
    char* cmd = Form("%s %s %d %d",EPS2PNG,picname.c_str(),
        (int)(CONV_X),(int)(CONV_Y));
    system(cmd);
    delete c1;
  }
  return 0;
}


void ReadFile(
    std::string& filename,
    std::vector<double> &xx,
    std::vector<std::vector<double>> &yy,
    std::string &current_time,
    int mode)
{
  std::ifstream ifs;
  if(mode==1){
    std::cout << "Reading ... : " << filename << std::endl;
  }
  ifs.open(filename, std::ios::in );
  std::string str;
  if(!ifs){
    std::cout << "The file is not opened:" << filename << std::endl;
    return;
  }
  getline(ifs,str); // To remove the first line //TODO
  while(getline(ifs,str)){
    std::istringstream sstr(str);

    std::string date,unixtime,temp1,temp2,humid1,humid2;
    std::string dev1,dev2;
    getline(sstr,str,'[');
    getline(sstr,date,'|');
    getline(sstr,str,'=');
    getline(sstr,unixtime,']');
    getline(sstr,dev1,'|');
    getline(sstr,dev2);

    if(dev1=="USBRH not found"){ temp1  = "0.0"; humid1 = "0.0"; }
    else{
      std::istringstream sstr1(dev1);
      getline(sstr1,str   ,':');
      getline(sstr1,temp1 ,'C');
      getline(sstr1,str   ,':');
      getline(sstr1,humid1,'%');
    }
    if(dev2=="USBRH not found"){ temp2  = "0.0"; humid2 = "0.0"; } 
    else{
      std::istringstream sstr2(dev2);
      getline(sstr2,str   ,':');
      getline(sstr2,temp2 ,'C');
      getline(sstr2,str   ,':');
      getline(sstr2,humid2,'%');
    }

#ifdef DEBUG
    std::cout << date     << std::endl;
    std::cout << unixtime << std::endl;
    std::cout << dev1     << std::endl;
    std::cout << dev2     << std::endl;
    std::cout << temp1  << std::endl;
    std::cout << humid1 << std::endl;
    std::cout << temp2  << std::endl;
    std::cout << humid2 << std::endl;
#endif

    double unixtime_d,temp1_d,humid1_d,temp2_d,humid2_d;
    unixtime_d = std::atof(unixtime.c_str());
    if(unixtime_d==0){
#ifdef ALARM_ON
        std::string msg = "Readout data do not contain time information.";
        set_logger(FILENAME,ALARM_TYPE_ERROR,msg);
        set_alarm(ALARM_LIST_TEMP);
#endif
      continue;
    }
    if(mode==1&&xx.size()>0){
      if(xx.back()>unixtime_d){continue;}
    }
    current_time = date;

    temp1_d    = std::atof(temp1 .c_str());
    humid1_d   = std::atof(humid1.c_str());
    temp2_d    = std::atof(temp2 .c_str());
    humid2_d   = std::atof(humid2.c_str());

    if(temp1_d==0||humid1_d==0||temp2_d==0||humid2_d==0){
#ifdef ALARM_ON
        std::string msg = "Readout data have a wrong format.";
        set_logger(FILENAME,ALARM_TYPE_ERROR,msg);
        set_alarm(ALARM_LIST_TEMP);
#endif
      continue;
    }
    xx.push_back   (unixtime_d);
    yy[0].push_back(temp1_d   );
    yy[1].push_back(humid1_d  );
    yy[2].push_back(temp2_d   );
    yy[3].push_back(humid2_d  );
  }
  ifs.close();
}
