#include "../include/Setup.h"

#define FILENAME "spillNb.cc"

int main(){

  std::ifstream ifs;
  ifs.open(SPILL_LOG, std::ios::in );
  if(!ifs){
    std::cout << "The file is not opened:" << TEMP_LOG << std::endl;
    return 1;
  }
  gStyle->SetOptStat(0);
  TCanvas *c1 = new TCanvas("c1","c1",CANVAS_X2,CANVAS_Y2);
  c1->cd(0);

  std::string str;
  std::vector<int> spillnb(SPILL_MAXLINE);
  int tmp = 0;
  int i = 0;
  while(ifs >> std::hex >> tmp && i<SPILL_MAXLINE){
    if(tmp!=0){
      spillnb[i] = tmp;
      i++;
    }
  }
  ifs.close();
  double max, min;
  int datanum;
  if(i!=0){
    max = spillnb[i-1]+5;
    min = spillnb[0]  -5;
    datanum = i;
  }
  else{
    max = 0.;
    min = -110.;
    datanum = 100;
    for(int j=0;j<datanum;j++){
      spillnb[j] = -1;
    }
  }
  if(max-min<110){
    max = min + 110.;
  }
  int bin = max - min;
  TH1F *h1 = new TH1F("","",bin,min,max);
  h1->SetFillColor(kBlue);
  h1->SetMinimum(0.);
  h1->SetMaximum(2.);
  for(int j=0;j<datanum;j++){
    if(j!=0){
      int diff = spillnb[j]-spillnb[j-1];
      if(diff>1){
        std::string msg = "There is a spill gap";
        //set_logger(FILENAME,ALARM_TYPE_ERROR,msg);
        //set_alarm(ALARM_LIST_SPILL);
      }
      else if(diff<1){
        std::string msg = "There are overlapped spills.";
        //set_logger(FILENAME,ALARM_TYPE_ERROR,msg);
        //set_alarm(ALARM_LIST_SPILL);
      }
    }
    h1->Fill(spillnb[j]);
  }
  h1->Draw("HIST");
  TLegend* leg = new TLegend(0.2,0.5,0.9,0.6);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->SetTextSize(0.07);
  leg->SetHeader(Form("Current SpillNb=%d",spillnb[i-1]));
  leg->Draw();

  struct tm tm;
  char buf[50];
  time_t t = time(NULL);
  localtime_r(&t, &tm);
  std::string time_info;
  str = asctime_r(&tm,buf);
  std::istringstream sstr(str);
  getline(sstr,time_info);
  TLegend *leg1 = new TLegend(0.2,0.6,0.9,0.7);
  leg1->SetFillStyle(0);
  leg1->SetBorderSize(0);
  leg1->SetTextSize(0.07);
  leg1->SetHeader(time_info.c_str());
  leg1->Draw();


  c1->Print(SPILL_PIC);
  delete h1;
  delete c1;
  return 0;
}
