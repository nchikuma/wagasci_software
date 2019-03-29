#include "../include/Setup.h"

#define FILENAME "storageCheck.cc"

int main(){

  std::string str;
  double daq_size,daq_used,daq_avail,daq_percent;
  double ana_size,ana_used,ana_avail,ana_percent;
  double acc_size,acc_used,acc_avail,acc_percent;

  std::ifstream ifs1;
  ifs1.open(STORAGE_FILE_DAQ, std::ios::in );
  if(!ifs1){
    std::cout << "The file is not opened:" << STORAGE_FILE_DAQ << std::endl;
    return 1;
  }
  getline(ifs1,str);
  ifs1 >> daq_size >> daq_used >> daq_avail >> daq_percent;
  ifs1.close();

  std::ifstream ifs2;
  ifs2.open(STORAGE_FILE_ANA, std::ios::in );
  if(!ifs2){
    std::cout << "The file is not opened:" << STORAGE_FILE_ANA << std::endl;
    return 1;
  }
  getline(ifs2,str);
  ifs2 >> ana_size >> ana_used >> ana_avail >> ana_percent;
  ifs2.close();

  std::ifstream ifs3;
  ifs3.open(STORAGE_FILE_ACCESS, std::ios::in );
  if(!ifs3){
    std::cout << "The file is not opened:" << STORAGE_FILE_ACCESS << std::endl;
    return 1;
  }
  getline(ifs3,str);
  ifs3 >> acc_size >> acc_used >> acc_avail >> acc_percent;
  ifs3.close();

  gStyle->SetOptStat(0);
  gStyle->SetPalette(1);
  TCanvas *c1 = new TCanvas("c1","c1",CANVAS_X*2,CANVAS_Y*2);
  c1->cd(0);
  c1->SetLeftMargin(0.15);
  c1->SetRightMargin(0.11);

  TH2F *h1 = new TH2F("storage","storage",5000,0,5.,4,0.,4.);
  for(int i=0;i<5000;i++){
    if     (i*1e-3<daq_used) h1->SetBinContent(i+1,1,daq_percent);
    else if(i*1e-3<daq_size) h1->SetBinContent(i+1,1,1.); 
    if     (i*1e-3<ana_used) h1->SetBinContent(i+1,2,ana_percent);
    else if(i*1e-3<ana_size) h1->SetBinContent(i+1,2,1.); 
    if     (i*1e-3<acc_used) h1->SetBinContent(i+1,3,acc_percent);
    else if(i*1e-3<acc_size) h1->SetBinContent(i+1,3,1.);
  }
  h1->SetTitle("");
  h1->GetXaxis()->SetTitle("Storage [GB]");
  h1->GetYaxis()->SetBinLabel(1,"daq");
  h1->GetYaxis()->SetBinLabel(2,"ana");
  h1->GetYaxis()->SetBinLabel(3,"access");
  h1->GetYaxis()->SetBinLabel(4,"");
  h1->GetYaxis()->SetLabelSize(0.07);
  ((TGaxis*)h1->GetXaxis())->SetMaxDigits(3);
  h1->SetMaximum(100.);
  h1->SetMinimum(0.);
  h1->Draw("colz");

  TLegend* leg1 = new TLegend(0.3,0.7,0.9,0.8);
  TLegend* leg2 = new TLegend(0.3,0.6,0.9,0.7);
  TLegend* leg3 = new TLegend(0.3,0.5,0.9,0.6);
  leg1->SetFillStyle(0);
  leg2->SetFillStyle(0);
  leg3->SetFillStyle(0);
  leg1->SetBorderSize(0);
  leg2->SetBorderSize(0);
  leg3->SetBorderSize(0);
  leg1->SetTextSize(0.05);
  leg2->SetTextSize(0.05);
  leg3->SetTextSize(0.05);
  leg1->SetHeader(Form("%3.1f%% Used (wagasci-daq)",daq_percent));
  leg2->SetHeader(Form("%3.1f%% Used (wagasci-ana)",ana_percent));
  leg3->SetHeader(Form("%3.1f%% Used (wagasci-access)",acc_percent));
  leg1->Draw();
  leg2->Draw();
  leg3->Draw();


  struct tm tm;
  char buf[50];
  time_t t = time(NULL);
  localtime_r(&t, &tm);
  std::string time_info;
  str = asctime_r(&tm,buf);
  std::istringstream sstr(str);
  getline(sstr,time_info);
  TLegend *leg4 = new TLegend(0.2,0.8,0.9,0.9);
  leg4->SetFillStyle(0);
  leg4->SetBorderSize(0);
  leg4->SetTextSize(0.05);
  leg4->SetHeader(time_info.c_str());
  leg4->Draw();


  c1->Print(STORAGE_PIC);
  delete c1;
  return 0;
}
