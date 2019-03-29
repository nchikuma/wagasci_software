#include "../include/Setup.h"

#define FILENAME "waterSensor.cc"

bool comp(const std::vector<double> &v1, const std::vector<double> &v2){
  return v1[0] < v2[0];
};

int main(){
  std::ifstream ifs;
  ifs.open(WATER_LOG, std::ios::in );
  std::vector<std::vector<double> > data_array;
  std::vector<double> tmp;

  std::string str,date,datetime;
  if(!(ifs >> str)) return 0; // for removing header
  while(ifs >> str){
    date = str;
    ifs >> str;
    std::istringstream sstr(str);
    int i = 0;
    int data_time=0;
    while(getline(sstr,str,',')){
      if(i==0){
        datetime = str;
        std::string timestr = "20"+date+" "+datetime;
        struct tm tm;
        memset(&tm,0,sizeof(struct tm));
        strptime(timestr.c_str(),"%Y-%m-%d %H:%M:%S",&tm);
        data_time = mktime(&tm);
        tmp.push_back((double)data_time);
      }
      else{ tmp.push_back(atof(str.c_str())); }
      i++;
    }
    data_array.push_back(tmp);
    if(tmp.size()!=WATER_NUMCH+1){
      std::string msg = Form("Data is broken: Only %d channels were found.",i-1);
      set_logger(FILENAME,ALARM_TYPE_ERROR,msg);
      continue;
    }
    tmp.clear();
  }
  ifs.close();

  int data_point = (int)data_array.size();
  std::sort(data_array.begin(),data_array.end(),comp);

  double current_data;
  std::string current_time;
  for(int i=0;i<WATER_NUMPLOT;i++){
    int npoint;
    std::string picname;
    switch(i){
      case 0: npoint=WATER_NUM1;picname=WATER_PIC1;break;
      case 1: npoint=WATER_NUM2;picname=WATER_PIC2;break;
      case 2: npoint=WATER_NUM3;picname=WATER_PIC3;break;
      case 3: npoint=WATER_NUM4;picname=WATER_PIC4;break;
      default: std::cout << "Too many plots" << std::endl; return 1; break;
    }
    TCanvas *c1 = new TCanvas("c1","c1",CANVAS_X,CANVAS_Y);
    c1->cd(0);
    TGraph *g1[WATER_NUMCH];
    TLegend *leg1  = new TLegend(0.9,0.12,0.99,0.5);
    leg1->SetFillStyle(0);
    leg1->SetBorderSize(0);
    leg1->SetTextFont(WATER_FONT1);
    TLegend *leg2[WATER_NUMCH], *leg3;
    for(int j=0;j<WATER_NUMCH;j++){
      int color;
      std::string name="", title="",opt="";
      double leg2_x, leg2_y;
      switch(j){
        case 0: color=WATER_COLOR0;name="CH1" ;opt="APL"    ;leg2_x=0.13;leg2_y=0.25;break;
        case 1: color=WATER_COLOR1;name="CH2" ;opt="PL same";leg2_x=0.28;leg2_y=0.25;break;
        case 2: color=WATER_COLOR2;name="CH3" ;opt="PL same";leg2_x=0.43;leg2_y=0.25;break;
        case 3: color=WATER_COLOR3;name="CH4" ;opt="PL same";leg2_x=0.58;leg2_y=0.25;break;
        case 4: color=WATER_COLOR4;name="CH5" ;opt="PL same";leg2_x=0.73;leg2_y=0.25;break;
        case 5: color=WATER_COLOR5;name="CH6" ;opt="PL same";leg2_x=0.13;leg2_y=0.20;break;
        case 6: color=WATER_COLOR6;name="CH7" ;opt="PL same";leg2_x=0.28;leg2_y=0.20;break;
        case 7: color=WATER_COLOR7;name="CH8" ;opt="PL same";leg2_x=0.43;leg2_y=0.20;break;
        case 8: color=WATER_COLOR8;name="CH9" ;opt="PL same";leg2_x=0.58;leg2_y=0.20;break;
        case 9: color=WATER_COLOR9;name="CH10";opt="PL same";leg2_x=0.73;leg2_y=0.20;break;
        default: std::cout << "Too many channels" << std::endl; return 1; break;
      }
      if(data_point<npoint) npoint=data_point;
      g1[j] = new TGraph(npoint);
      for(int k=0;k<npoint;k++){
        g1[j]->SetPoint(k,
            data_array[data_point-npoint+k][  0],
            data_array[data_point-npoint+k][j+1]+0.1*(j-4) 
            );
      }
      g1[j]->SetMarkerSize(0.3);
      g1[j]->SetMarkerStyle(WATER_MAKER_STYLE);
      g1[j]->SetMarkerColor(color);
      g1[j]->SetLineColor  (color);
      g1[j]->GetXaxis()->SetTimeDisplay(1);
      g1[j]->GetXaxis()->SetTimeFormat("#splitline{%Y/%m/%d}{%H:%M}");
      g1[j]->GetXaxis()->SetTimeOffset(0,"jst");
      g1[j]->GetXaxis()->SetLabelOffset(0.03);
      g1[j]->GetXaxis()->SetLabelSize(0.02);
      g1[j]->GetXaxis()->SetLabelFont(WATER_LABEL_FONT);
      g1[j]->SetTitle(title.c_str());
      g1[j]->SetMaximum(WATER_MAX); 
      g1[j]->SetMinimum(WATER_MIN);
      g1[j]->Draw(opt.c_str());
      leg1->AddEntry(g1[j],name.c_str(),"p");

      if(i==0){
        current_data = data_array[data_point-2][j+1];
        if(j==0){
          time_t current_time_t = data_array[data_point-2][0];
          struct tm tm;
          localtime_r(&current_time_t,&tm);
          char buf[50];
          std::string str = asctime_r(&tm,buf);
          std::istringstream sstr(str);
          getline(sstr,current_time);
        }
      }

#ifdef ALARM_ON
      if(i==0){
        bool alarm_on = false;
        if(j==0&&(!WATER_MASK0)&&(current_data<WATER_THRES0)){alarm_on=true;}
        if(j==1&&(!WATER_MASK1)&&(current_data<WATER_THRES1)){alarm_on=true;}
        if(j==2&&(!WATER_MASK2)&&(current_data<WATER_THRES2)){alarm_on=true;}
        if(j==3&&(!WATER_MASK3)&&(current_data<WATER_THRES3)){alarm_on=true;}
        if(j==4&&(!WATER_MASK4)&&(current_data<WATER_THRES4)){alarm_on=true;}
        if(j==5&&(!WATER_MASK5)&&(current_data<WATER_THRES5)){alarm_on=true;}
        if(j==6&&(!WATER_MASK6)&&(current_data<WATER_THRES6)){alarm_on=true;}
        if(j==7&&(!WATER_MASK7)&&(current_data<WATER_THRES7)){alarm_on=true;}
        if(j==8&&(!WATER_MASK8)&&(current_data<WATER_THRES8)){alarm_on=true;}
        if(j==9&&(!WATER_MASK9)&&(current_data<WATER_THRES9)){alarm_on=true;}
        if(alarm_on){
          std::string msg = Form("!!!ALARM!!! Water Level Sensor CH%d",j+1);
          set_logger(FILENAME,ALARM_TYPE_ERROR,msg);
          set_alarm(ALARM_LIST_WATER);
        }
      }
#endif
      std::string data_text = Form("CH%d: %2.1f[V]",j+1,current_data);
      leg2[j] = new TLegend(leg2_x,leg2_y,leg2_x+0.15,leg2_y+0.05);
      leg2[j]->SetFillStyle(0);
      leg2[j]->SetBorderSize(0);
      leg2[j]->SetHeader(data_text.c_str());
      leg2[j]->SetTextSize(0.03);
      leg2[j]->SetTextFont(WATER_FONT2);
      leg2[j]->Draw();
      if(j==0){
        leg3 = new TLegend(0.15,0.30,0.30,0.35);
        leg3->SetFillStyle(0);
        leg3->SetBorderSize(0);
        leg3->SetHeader(current_time.c_str());
        leg3->SetTextSize(0.03);
        leg3->SetTextFont(WATER_FONT3);
        leg3->Draw();
      }
    } //j
    leg1->Draw();
    c1->Print(picname.c_str());
    char* cmd = Form("%s %s %d %d",EPS2PNG,picname.c_str(),
        (int)(CONV_X),(int)(CONV_Y));
    system(cmd);
    delete c1;
  }//i
  return 0;
}
