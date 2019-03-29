#include "../include/Setup.h"

int main(int argc, char* argv[]){

  gStyle->SetTimeOffset(-788918400);
  std::ifstream ifs;
  ifs.open(LAMBDA_LOG, std::ios::in );
  std::deque<double> xx;
  std::deque<std::deque<double>> yy(LAMBDA_NUMCH);

  double tmp, current_time, last_time;
  int npoint[LAMBDA_NUMPLOT];
  for(int j=0;j<LAMBDA_NUMPLOT;j++){npoint[j]=0;}
  if(ifs >> current_time){
    for(int j=0;j<LAMBDA_NUMPLOT;j++) npoint[j]++;
    xx.push_front(current_time);
    for(int j=0;j<LAMBDA_NUMCH;j++){
      ifs >> tmp; 
      yy[j].push_front(tmp);
    }
    last_time = current_time;
  }
  else return 0;
  while(ifs >> tmp){
    if(tmp>last_time){
      std::cout<<"Time order is strange: "<< (int)tmp << std::endl;
      std::string tmpstr;
      getline(ifs,tmpstr);
      continue;
    }
    last_time = tmp;
    if(tmp>current_time-LAMBDA_TIME1){npoint[0]++;}
    if(tmp>current_time-LAMBDA_TIME2){npoint[1]++;}
    if(tmp>current_time-LAMBDA_TIME3){npoint[2]++;}
    if(tmp>current_time-LAMBDA_TIME4){npoint[3]++;}else{break;}
    xx.push_front(tmp);
    for(int j=0;j<LAMBDA_NUMCH;j++){
      ifs >> tmp; yy[j].push_front(tmp);
    }
  }
  ifs.close();
  for(int i=0;i<LAMBDA_NUMPLOT;i++){
    TCanvas *c1 = new TCanvas("c1","c1",CANVAS_X,CANVAS_Y);
    c1->cd(0);
    TPad *pad1[2]; 
    TGraph *g1[8];
    TLegend *leg1[2], *leg2[4],*leg3[2];
    TGaxis *axis1[2][2];
    for(int j=0;j<2;j++){
      pad1[j] = new TPad("pad1","pad1",0.01,0.01+0.5*j,0.99,0.49+0.5*j);
      pad1[j]->Range(0.,0.,1.,1.);
      c1->cd(0);
      pad1[j]->Draw();
      leg1[j] = new TLegend(0.00,0.12,0.08,0.3);
      leg1[j]->SetFillStyle(0);
      leg1[j]->SetBorderSize(0);
    }
    for(int j=0;j<LAMBDA_NUMCH;j++){
      int color, ipad;
      double min, max;
      std::string name="", title="",opt="";
      switch(j%4){
        case 0: color=LAMBDA_COLOR_VOL;name="VOL";opt="APL"    ;break;
        case 1: color=LAMBDA_COLOR_CUR;name="CUR";opt="PL same";break;
        case 2: color=LAMBDA_COLOR_OVP;name="OVP";opt="PL same";break;
        case 3: color=LAMBDA_COLOR_UVP;name="UVP";opt="PL same";break;
      }
      switch(j/4){
        case 0: ipad=0;title="HV status";min=LAMBDA_HV_MIN;max=LAMBDA_HV_MAX;break;
        case 1: ipad=1;title="LV status";min=LAMBDA_LV_MIN;max=LAMBDA_LV_MAX;break;
      }
      std::vector<double> yy_tmp;
      std::copy(yy[j].begin(),yy[j].end(),std::back_inserter(yy_tmp));
      g1[j] = new TGraph(npoint[i]);
      for(int k=0;k<npoint[i];k++){
        g1[j]->SetPoint(k,
            xx[npoint[LAMBDA_NUMPLOT-1]-npoint[i]+k],
            yy[j][npoint[LAMBDA_NUMPLOT-1]-npoint[i]+k]);
      }

      g1[j]->SetMarkerSize(0.5);
      g1[j]->SetMarkerStyle(LAMBDA_MAKER_STYLE);
      g1[j]->SetMarkerColor(color);
      g1[j]->SetLineColor  (color);
      g1[j]->GetXaxis()->SetTimeDisplay(1);
      g1[j]->GetXaxis()->SetTimeFormat("#splitline{%m/%d}{%H:%M}");
      g1[j]->GetXaxis()->SetTimeOffset(0,"jst");
      g1[j]->GetXaxis()->SetLabelOffset(0.03);
      g1[j]->GetXaxis()->SetLabelSize(0.05);
      g1[j]->GetYaxis()->SetLabelSize(0.);
      g1[j]->SetTitle(title.c_str());
      g1[j]->SetMaximum(max); g1[j]->SetMinimum(min);
      if(j%4!=1) leg1[ipad]->AddEntry(g1[j],name.c_str(),"p");
      pad1[ipad]->cd(); 
      g1[j]->Draw(opt.c_str());
      if(j%4==3){ 
        leg1[ipad]->Draw();
        double min2,max2;
        double x1  = g1[j]->GetXaxis()->GetBinLowEdge(1);
        double x2  = g1[j]->GetXaxis()->GetBinUpEdge(g1[j]->GetXaxis()->GetNbins());
        double y1,y2;
        if(ipad==0){min2=LAMBDA_HV_MIN/LAMBDA_NORM_CUR_HV;max2=LAMBDA_HV_MAX/LAMBDA_NORM_CUR_HV;y1=LAMBDA_HV_MIN;y2=LAMBDA_HV_MAX;}
        else       {min2=LAMBDA_LV_MIN/LAMBDA_NORM_CUR_LV;max2=LAMBDA_LV_MAX/LAMBDA_NORM_CUR_LV;y1=LAMBDA_LV_MIN;y2=LAMBDA_LV_MAX;}
        axis1[ipad][0] = new TGaxis(x1,y1,x1,y2,y1,y2,510,"");
        axis1[ipad][0]->SetLineColor(LAMBDA_COLOR_VOL);
        axis1[ipad][0]->SetTitle("Voltage [V]");
        axis1[ipad][0]->CenterTitle();
        axis1[ipad][0]->SetTitleSize(0.07);
        axis1[ipad][0]->SetTitleOffset(0.40);
        axis1[ipad][0]->SetLabelSize(0.05);
        axis1[ipad][0]->Draw();
        axis1[ipad][1] = new TGaxis(x2,y1,x2,y2,min2,max2,510,"+L");
        axis1[ipad][1]->SetLineColor(LAMBDA_COLOR_CUR);
        axis1[ipad][1]->SetTitle("Current [A]");
        axis1[ipad][1]->CenterTitle();
        axis1[ipad][1]->SetTitleSize(0.07);
        axis1[ipad][1]->SetTitleOffset(0.65);
        axis1[ipad][1]->SetLabelSize(0.05);
        axis1[ipad][1]->Draw();
      }
      std::string suffix="",data_txt="",data_time="";
      double leg2_x, leg2_y;
      switch(j%4){
        case 0: suffix="V";leg2_x=0.15;leg2_y=0.70;break;
        case 1: suffix="A";leg2_x=0.40;leg2_y=0.70;break;
      }
      switch(j/4){
        case 0: ipad=0;break;
        case 1: ipad=1;break;
      }
      if(j%4==0||j%4==1){
        data_txt = Form("%s:%04.2f[%s]",name.c_str(),yy[j].back(),suffix.c_str());
        int id = j/4*2+j%4;
        pad1[ipad]->cd();
        leg2[id] = new TLegend(leg2_x,leg2_y,leg2_x+0.3,leg2_y+0.1);
        leg2[id]->SetFillStyle(0);
        leg2[id]->SetBorderSize(0);
        leg2[id]->SetHeader(data_txt.c_str());
        leg2[id]->SetTextSize(0.08);
        leg2[id]->Draw();
      }
      if(j%4==0){
        time_t currenttime_t = xx.back();
        struct tm tm;
        localtime_r(&currenttime_t,&tm);
        char buf[50];
        std::string str = asctime_r(&tm,buf);
        std::istringstream sstr(str);
        getline(sstr,data_time);
        pad1[ipad]->cd();
        leg3[ipad] = new TLegend(0.15,0.80,0.40,0.90);
        leg3[ipad]->SetFillStyle(0);
        leg3[ipad]->SetBorderSize(0);
        leg3[ipad]->SetHeader(data_time.c_str());
        leg3[ipad]->SetTextSize(0.08);
        leg3[ipad]->Draw();
      }
    }

    std::string picname;
    if     (i==0) picname = LAMBDA_PIC1;
    else if(i==1) picname = LAMBDA_PIC2;
    else if(i==2) picname = LAMBDA_PIC3;
    else if(i==3) picname = LAMBDA_PIC4;
    c1->Print(picname.c_str());
    char* cmd = Form("%s %s %d %d",EPS2PNG,picname.c_str(),
        (int)(CONV_X),(int)(CONV_Y));
    system(cmd);
    delete c1;
  }
  return 0;
}
