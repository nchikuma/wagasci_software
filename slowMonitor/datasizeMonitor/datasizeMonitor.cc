#include "../include/Setup.h"

#define FILENAME "datasizeMonitor.cc"
#define NPOINT 100

int main(){

  // =================
  //initialize
  TROOT root("GUI","GUI");
  TApplication App("App",0,0);
  gStyle->SetStripDecimals(false);

  TCanvas* c1 = new TCanvas("c1","c1",0,730,270,270);
  c1->SetTitle("Running Data Size");

  TGraph *g1 = new TGraph(NPOINT);
  TGraph *g2 = new TGraph(NPOINT);
  for(int i=0;i<NPOINT;i++){
    g1->SetPoint(i,0,0);
    g2->SetPoint(i,0,0);

  }
  g1->SetTitle("");
  g1->SetMarkerColor(2);
  g1->SetMarkerStyle(29);
  g1->SetMarkerSize(1);
  g2->SetTitle("");
  g2->SetMarkerColor(4);
  g2->SetMarkerStyle(33);
  g2->SetMarkerSize(1);
  g1->Draw();
  g2->Draw("same");
  TLegend* leg = new TLegend(0.1,0.2,0.40,0.4);
  leg->SetFillStyle(0);
  leg->SetBorderSize(0);
  leg->AddEntry(g1,"dif1","p");
  leg->AddEntry(g2,"dif2 (x1.1)","p");

  int i=0;
  while(true){
    std::string rawfile1 = "/opt/calicoes/raw_data/running_data_dif_1_1_1.raw";
    std::string rawfile2 = "/opt/calicoes/raw_data/running_data_dif_1_1_2.raw";
    char* cmd1 = Form("ssh wagasci-daq wc -c %s|awk '{print $1}' >%s",rawfile1.c_str(),RAWDATASIZE1);
    system(cmd1);
    char* cmd2 = Form("ssh wagasci-daq wc -c %s|awk '{print $1}' >%s",rawfile2.c_str(),RAWDATASIZE2);
    system(cmd2);
    int filesize1,filesize2;
    std::ifstream ifs1(RAWDATASIZE1);
    if(ifs1) ifs1 >> filesize1;
    else filesize1 = 0;
    ifs1.close();
    std::ifstream ifs2(RAWDATASIZE2);
    if(ifs2) ifs2 >> filesize2;
    else filesize2 = 0;
    ifs2.close();
    if(i==0){
      for(int j=0;j<NPOINT;j++){
        g1->SetPoint(j,i,filesize1);
        g2->SetPoint(j,i,filesize2*1.1);
      }
    }else{
      g1->SetPoint(i%NPOINT,i,filesize1);
      g2->SetPoint(i%NPOINT,i,filesize2*1.1);
    }
    double ymin1 = g1->GetYaxis()->GetXmin();
    double ymin2 = g2->GetYaxis()->GetXmin();
    double ymax1 = g1->GetYaxis()->GetXmax();
    double ymax2 = g2->GetYaxis()->GetXmax();
    double min; if(ymin1>ymin2) min=ymin2; else min=ymin1;
    double max; if(ymax1<ymax2) max=ymax2; else max=ymax1;
    g1->SetMinimum(min);
    g1->SetMaximum(max);
    g1->Draw("AP");
    g2->Draw("P same");
    leg->Draw("same");
    c1->cd(0)->Modified();
    c1->Update();

    sleep(1);
    i++;
  }

  return 0;
}
