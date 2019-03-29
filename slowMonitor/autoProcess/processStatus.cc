#include "../include/Setup.h"

int main(int argc, char* argv[]){
  if(argc<2){
    return 0;
  }
  int min_runid = std::atoi(argv[1]);
  int max_runid = std::atoi(argv[2]);
  int bin_runid = max_runid - min_runid;
  if(bin_runid<1){
    return 0;
  }
  const int state_min =  0;
  const int state_max = 11;//13;
  gStyle->SetOptStat(0);
  gStyle->SetPalette(1);
  std::ifstream ifs(AUTO_RUNID_LIST);
  TH2F *h = new TH2F("","",bin_runid,min_runid,max_runid,600,0.,600.);
  h->GetXaxis()->SetTitle("Run ID");
  h->GetYaxis()->SetTitle("Acq ID");
  h->GetXaxis()->CenterTitle();
  h->GetYaxis()->CenterTitle();
  h->GetXaxis()->SetNdivisions(505);
  h->GetXaxis()->CenterLabels();
  h->GetXaxis()->SetTickLength(0);
  h->GetYaxis()->SetTickLength(0);
  h->SetMaximum(state_max);
  h->SetMinimum(state_min);
  int num_acq = 0;
  if(ifs){
    std::string str;
    while(getline(ifs,str)){
      std::istringstream sstr(str);
      int i=0;
      int runid = -1;
      int acqid = -1;
      int state = -1;
      while(getline(sstr,str,' ')){
        if     (i==0){runid=std::stoi(str.c_str());}
        else if(i==1){acqid=std::stoi(str.c_str());}
        else if(i==2){state=std::stoi(str.c_str());}
        i++;
      }
      h->Fill(runid,acqid+1,state);
      num_acq++;
    }
  }
  ifs.close();

  TH2F *h2 = new TH2F("","",
      state_max-state_min,state_min,state_max+1,
      state_max-state_min,state_min,state_max+1);
  h2->SetMaximum(state_max);
  h2->SetMinimum(state_min);
  h2->GetXaxis()->CenterTitle();
  h2->GetYaxis()->CenterTitle();
  h2->GetXaxis()->SetNdivisions(505);
  h2->GetXaxis()->SetLabelSize(0.);
  h2->GetYaxis()->SetLabelSize(0.);
  h2->GetXaxis()->SetTickLength(0);
  for(int i=state_min;i<=state_max;i++){
    h2->Fill(i,i,i);
  }

  TCanvas *c1 = new TCanvas("c1","c1");
  TPad *pad1 = new TPad("pad1","pad1",0.0,0.0,0.8,1.0);
  TPad *pad2 = new TPad("pad2","pad2",0.8,0.0,1.0,1.0);
  c1->SetGridx(1);
  c1->SetGridy(1);
  c1->cd(0);
  pad1->Draw();
  pad2->Draw();
  pad1->cd();
  h->Draw("colz");
  pad2->cd();
  h2->Draw("colz");
  TLegend *leg[7];
  for(int i=state_min;i<=state_max;i++){
    std::string name("");
    if     (i==0) name  = "1.Copy";
    else if(i==2) name  = "3.Decode";
    else if(i==4) name  = "5.Hist";
    else if(i==6) name  = "7.Recon";
    else if(i==8) name  = "9.DQ";
    else if(i==10) name = "11.Removed";
    //else if(i==12) name = "13.DQ History";
    if(i%2==0){
      leg[i/2] = new TLegend(0.2,((double)i  )/(state_max)*0.8+0.1,
                             0.8,((double)i+1)/(state_max)*0.8+0.1);
      leg[i/2]->SetHeader(name.c_str());
      leg[i/2]->SetFillStyle(0);
      leg[i/2]->SetBorderSize(0);
      leg[i/2]->SetTextSize(0.13);
      leg[i/2]->Draw();
    }
  }

  std::string picname = RUN_STATUS_PIC;
  c1->Print(picname.c_str());
  char* cmd = Form("%s %s %d %d",EPS2PNG,picname.c_str(),
      (int)(CONV_X),(int)(CONV_Y));
  system(cmd);

  return 0;
}
