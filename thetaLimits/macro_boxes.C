{
  Double_t dy, dx, x, y, a, m, tZ;
  Double_t bW[21]={0.0,0.0,0.0,0.0,0.0,0.000,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,0.999};//0.5,
  Double_t tH[21]={0.0,0.2,0.4,0.6,0.8,0.999,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.000};//0.25
  //int Mexp[21]={1260, 1250, 1240, 1240, 1230, 1230, 1220, 1210, 1200, 1200, 1200, 1190, 1180, 1170, 1180, 1160, 1150, 1150, 1140, 1140, 1160};
  //int Mobs[21]={1300, 1290, 1280, 1280, 1270, 1260, 1270, 1260, 1250, 1240, 1240, 1230, 1210, 1200, 1200, 1180, 1170, 1160, 1120, 1110, 1100};
  // noB0
  //int Mexp[21]={1260, 1250, 1240, 1240, 1230, 1230, 1230, 1220, 1200, 1200, 1200, 1190, 1180, 1170, 1180, 1160, 1150, 1150, 1140, 1140, 1150};
  //int Mobs[21]={1300, 1290, 1290, 1280, 1270, 1260, 1270, 1260, 1260, 1250, 1250, 1240, 1220, 1220, 1220, 1190, 1180, 1180, 1160, 1150, 1140};
  // noCRHB0
  //  int Mexp[21]={1260, 1250, 1240, 1240, 1230, 1230, 1220, 1210, 1200, 1200, 1200, 1190, 1180, 1170, 1180, 1160, 1150, 1150, 1140, 1140, 1160};
  //  int Mobs[21]={1300, 1290, 1280, 1280, 1270, 1270, 1270, 1260, 1250, 1240, 1240, 1230, 1210, 1200, 1200, 1180, 1170, 1160, 1120, 1110, 1120};
  // comb123
  int Mexp[21]={1260, 1260, 1260, 1240, 1240, 1240, 1220, 1220, 1200, 1200, 1210, 1190, 1180, 1180, 1180, 1160, 1150, 1160, 1140, 1140, 1150};               
  int Mobs[21]={1300, 1290, 1290, 1280, 1270, 1270, 1280, 1260, 1260, 1250, 1250, 1240, 1230, 1220, 1220, 1190, 1180, 1180, 1160, 1150, 1140};                

  TH2D *Hobs = new TH2D("Hobs",";B(tH);B(bW)",6,-0.1,1.1,6,-0.1,1.1);
  TH2D *Hexp = new TH2D("Hexp",";B(tH);B(bW)",6,-0.1,1.1,6,-0.1,1.1);
  for(int i = 0; i < 21; i++){
    if(Mexp[i] == 0 && Mobs[i] == 0) continue;
    Hobs->Fill(tH[i],bW[i],Mobs[i]);
    Hexp->Fill(tH[i],bW[i],Mexp[i]);
  }


  // create graph
  TCanvas *c1 = new TCanvas("c1","Graph Draw Options",600,500);
  c1->GetFrame()->SetFillColor(42);
  c1->GetFrame()->SetLineColor(kWhite);
  
  c1->SetRightMargin(0.18);
  c1->SetTopMargin(0.08);
  c1->SetBottomMargin(0.10);
  
  gStyle->SetOptStat(0);
  gStyle->SetPalette(57);
 
  Hexp->GetZaxis()->SetRangeUser(1050,1350);
  Hexp->GetXaxis()->SetTitleSize(0.05);
  Hexp->GetYaxis()->SetTitleSize(0.05);
  Hexp->GetXaxis()->SetLabelSize(0.04);
  Hexp->GetYaxis()->SetLabelSize(0.04);
  Hexp->GetZaxis()->SetLabelSize(0.04);
  Hexp->GetXaxis()->SetTitleOffset(0.9);
  Hexp->GetYaxis()->SetTitleOffset(0.9);
  Hexp->Draw("colz");
  
  TLatex t1;
  t1.SetTextAlign(22);
  t1.SetTextSize(0.044);
  
  for(int i = 0; i < 21; i++){
    if(Mexp[i] < 700) t1.DrawLatex(tH[i]+0.01,bW[i],"< 700");
    else{
     char value[10];
     std::snprintf(value, sizeof(value),"%i",Mexp[i]);     
     t1.DrawLatex(tH[i],bW[i],value);
   }
  } 
  
  // t1.SetTextAlign(11);
  // t1.DrawLatex(-0.1,1.15,"CMS 2.3/2.6/2.7 fb^{-1} (13 TeV)");
  t1.SetTextAlign(22);
  t1.SetTextAngle(-90);
  t1.DrawLatex(1.35,0.48,"95\% CL expected T quark mass limit (GeV)");

  prelimTex=TLatex();
  prelimTex.SetNDC();
  prelimTex.SetTextAlign(31);
  prelimTex.SetTextFont(42);
  prelimTex.SetTextSize(0.05);
  prelimTex.SetLineWidth(2);
  prelimTex.DrawLatex(0.87,0.94,"35.9 fb^{-1} (13 TeV)");
    
  prelimTex2=TLatex();
  prelimTex2.SetNDC();
  prelimTex2.SetTextFont(61);
  prelimTex2.SetTextAlign(31);
  prelimTex2.SetLineWidth(2);
  prelimTex2.SetTextSize(0.08);
  prelimTex2.DrawLatex(0.81,0.83,"CMS");

  prelimTex2b=TLatex();
  prelimTex2b.SetNDC();
  prelimTex2b.SetTextAlign(13);
  prelimTex2b.SetTextFont(52);
  prelimTex2b.SetTextSize(0.055);
  prelimTex2b.SetLineWidth(2);
  //prelimTex2b.DrawLatex(0.255,0.960,"Preliminary");

  c1->Print("boxesComb_exp_comb123.png");
  c1->Print("boxesComb_exp_comb123.pdf");
  c1->Print("boxesComb_exp.C");
  c1->Print("boxesComb_exp.root");
  
  //---------------------------------
  
  TCanvas *c2 = new TCanvas("c2","Graph Draw Options",600,500);
  c2->GetFrame()->SetFillColor(42);
  c2->GetFrame()->SetLineColor(kWhite);
  
  c2->SetRightMargin(0.18);
  c2->SetTopMargin(0.08);
  c2->SetBottomMargin(0.10);
  
  gStyle->SetOptStat(0);
  gStyle->SetPalette(57);
  
  Hobs->GetZaxis()->SetRangeUser(1050,1350);
  Hobs->GetXaxis()->SetTitleSize(0.05);
  Hobs->GetYaxis()->SetTitleSize(0.05);
  Hobs->GetXaxis()->SetLabelSize(0.04);
  Hobs->GetYaxis()->SetLabelSize(0.04);
  Hobs->GetZaxis()->SetLabelSize(0.04);
  Hobs->GetXaxis()->SetTitleOffset(0.9);
  Hobs->GetYaxis()->SetTitleOffset(0.9);
  Hobs->Draw("colz");
  
  TLatex t2;
  t2.SetTextAlign(22);
  t2.SetTextSize(0.044);
  
  for(int i = 0; i < 21; i++){
    if(Mobs[i] < 700) t2.DrawLatex(tH[i]+0.01,bW[i],"< 700");
    else{
      char value[10];
      std::snprintf(value, sizeof(value),"%i",Mobs[i]);     
      t2.DrawLatex(tH[i],bW[i],value);
    }
  } 
  
  // t2.SetTextAlign(11);
  //  t2.DrawLatex(-0.1,1.15,"CMS Preliminary, 35.9 fb^{-1} (13 TeV)");
  t2.SetTextAlign(22);
  t2.SetTextAngle(-90);
  t2.DrawLatex(1.35,0.48,"95\% CL observed T quark mass limit (GeV)");

  prelimTexO=TLatex();
  prelimTexO.SetNDC();
  prelimTexO.SetTextAlign(31);
  prelimTexO.SetTextFont(42);
  prelimTexO.SetTextSize(0.05);
  prelimTexO.SetLineWidth(2);
  prelimTexO.DrawLatex(0.87,0.94,"35.9 fb^{-1} (13 TeV)");
    
  prelimTexO2=TLatex();
  prelimTexO2.SetNDC();
  prelimTexO2.SetTextFont(61);
  prelimTexO2.SetTextAlign(31);
  prelimTexO2.SetLineWidth(2);
  prelimTexO2.SetTextSize(0.08);
  prelimTexO2.DrawLatex(0.81,0.83,"CMS");
  
  c2->Print("boxesComb_obs_comb123.png");
  c2->Print("boxesComb_obs_comb123.pdf");
  c2->Print("boxesComb_obs.C");
  c2->Print("boxesComb_obs.root");

  //////////////////

  //int MexpB[21]={930, 930, 930, 920, 920, 920, 1040, 1040, 1040, 1030, 1040, 1100, 1100, 1100, 1100, 1150, 1150, 1150, 1180, 1180, 1200};
  //int MobsB[21]={960, 960, 940, 920, 900, 900, 1080, 1070, 1070, 1070, 1070, 1150, 1140, 1130, 1140, 1180, 1180, 1170, 1200, 1190, 1220};
  // noB0
  //int MexpB[21]={920, 920, 920, 910, 910, 920, 1040, 1040, 1030, 1030, 1040, 1100, 1100, 1100, 1100, 1150, 1140, 1150, 1180, 1170, 1200};
  //int MobsB[21]={960, 950, 940, 930, 910, 910, 1080, 1080, 1080, 1080, 1080, 1160, 1140, 1140, 1150, 1190, 1180, 1180, 1210, 1200, 1220};
  // noCRHB0
  //  int MexpB[21]={920, 930, 930, 920, 920, 920, 1040, 1040, 1040, 1030, 1040, 1100, 1100, 1100, 1100, 1150, 1150, 1150, 1180, 1180, 1200};
  //  int MobsB[21]={960, 960, 940, 920, 900, 920, 1080, 1070, 1070, 1070, 1070, 1150, 1140, 1130, 1140, 1180, 1180, 1170, 1200, 1190, 1230};
  // comb123
  int MexpB[21]={930, 930, 920, 920, 920, 930, 1050, 1040, 1040, 1040, 1050, 1100, 1100, 1100, 1110, 1160, 1160, 1160, 1190, 1190, 1240};
  int MobsB[21]={960, 960, 950, 920, 910, 910, 1080, 1080, 1080, 1070, 1080, 1150, 1150, 1140, 1160, 1190, 1180, 1180, 1220, 1200, 1240};

  TH2D *HobsB = new TH2D("HobsB",";B(bH);B(tW)",6,-0.1,1.1,6,-0.1,1.1);
  TH2D *HexpB = new TH2D("HexpB",";B(bH);B(tW)",6,-0.1,1.1,6,-0.1,1.1);
  for(int i = 0; i < 21; i++){
    if(MexpB[i] != 0) HexpB->Fill(tH[i],bW[i],MexpB[i]);
    if(MobsB[i] != 0) HobsB->Fill(tH[i],bW[i],MobsB[i]);
  }

  
  // create graph
  TCanvas *c4 = new TCanvas("c4","Graph Draw Options",600,500);
  c4->GetFrame()->SetFillColor(42);
  c4->GetFrame()->SetLineColor(kWhite);
  
  c4->SetRightMargin(0.18);
  c4->SetTopMargin(0.08);
  c4->SetBottomMargin(0.10);
  
  gStyle->SetOptStat(0);
  gStyle->SetPalette(57);
  
  HexpB->GetZaxis()->SetRangeUser(800,1250);
  HexpB->GetXaxis()->SetTitleSize(0.05);
  HexpB->GetYaxis()->SetTitleSize(0.05);
  HexpB->GetXaxis()->SetLabelSize(0.04);
  HexpB->GetYaxis()->SetLabelSize(0.04);
  HexpB->GetZaxis()->SetLabelSize(0.04);
  HexpB->GetXaxis()->SetTitleOffset(0.9);
  HexpB->GetYaxis()->SetTitleOffset(0.9);
  HexpB->Draw("colz");
  
  TLatex t4;
  t4.SetTextAlign(22);
  t4.SetTextSize(0.044);
  
  for(int i = 0; i < 21; i++){
    if(MexpB[i] < 700) t4.DrawLatex(tH[i]+0.01,bW[i],"< 700");
    else{
      char value[10];
      std::snprintf(value, sizeof(value),"%i",MexpB[i]);     
      t4.DrawLatex(tH[i],bW[i],value);
    }
  } 
  
  //  t4.SetTextAlign(11);
  //  t4.DrawLatex(-0.1,1.15,"CMS Preliminary, 35.9 fb^{-1} (13 TeV)");
  t4.SetTextAlign(22);
  t4.SetTextAngle(-90);
  t4.DrawLatex(1.35,0.48,"95\% CL expected B quark mass limit (GeV)");

  prelimTexB=TLatex();
  prelimTexB.SetNDC();
  prelimTexB.SetTextAlign(31);
  prelimTexB.SetTextFont(42);
  prelimTexB.SetTextSize(0.05);
  prelimTexB.SetLineWidth(2);
  prelimTexB.DrawLatex(0.87,0.94,"35.9 fb^{-1} (13 TeV)");
    
  prelimTexB2=TLatex();
  prelimTexB2.SetNDC();
  prelimTexB2.SetTextFont(61);
  prelimTexB2.SetTextAlign(31);
  prelimTexB2.SetLineWidth(2);
  prelimTexB2.SetTextSize(0.08);
  prelimTexB2.DrawLatex(0.81,0.83,"CMS");
  
  c4->Print("boxesComb_expB_comb123.png");
  c4->Print("boxesComb_expB_comb123.pdf");
  c4->Print("boxesComb_expB.C");
  c4->Print("boxesComb_expB.root");
  
  //---------------------------------
  
  TCanvas *c3 = new TCanvas("c3","Graph Draw Options",600,500);
  c3->GetFrame()->SetFillColor(42);
  c3->GetFrame()->SetLineColor(kWhite);
  
  c3->SetRightMargin(0.18);
  c3->SetTopMargin(0.08);
  c3->SetBottomMargin(0.10);
  
  gStyle->SetOptStat(0);
  gStyle->SetPalette(57);
  
  HobsB->GetZaxis()->SetRangeUser(800,1250);
  HobsB->GetXaxis()->SetTitleSize(0.05);
  HobsB->GetYaxis()->SetTitleSize(0.05);
  HobsB->GetXaxis()->SetLabelSize(0.04);
  HobsB->GetYaxis()->SetLabelSize(0.04);
  HobsB->GetZaxis()->SetLabelSize(0.04);
  HobsB->GetXaxis()->SetTitleOffset(0.9);
  HobsB->GetYaxis()->SetTitleOffset(0.9);
  HobsB->Draw("colz");

  TLatex t5;
  t5.SetTextAlign(22);
  t5.SetTextSize(0.044);
  
  for(int i = 0; i < 21; i++){
    if(MobsB[i] < 700) t5.DrawLatex(tH[i]+0.01,bW[i],"< 700");
    else{
      char value[10];
      std::snprintf(value, sizeof(value),"%i",MobsB[i]);     
      t5.DrawLatex(tH[i],bW[i],value);
    }
  } 
  
  //  t5.SetTextAlign(11);
  //  t5.DrawLatex(-0.1,1.15,"CMS Preliminary, 35.9 fb^{-1} (13 TeV)");
  t5.SetTextAlign(22);
  t5.SetTextAngle(-90);
  t5.DrawLatex(1.35,0.48,"95\% CL observed B quark mass limit (GeV)");

  prelimTexOB=TLatex();
  prelimTexOB.SetNDC();
  prelimTexOB.SetTextAlign(31);
  prelimTexOB.SetTextFont(42);
  prelimTexOB.SetTextSize(0.05);
  prelimTexOB.SetLineWidth(2);
  prelimTexOB.DrawLatex(0.87,0.94,"35.9 fb^{-1} (13 TeV)");
    
  prelimTexOB2=TLatex();
  prelimTexOB2.SetNDC();
  prelimTexOB2.SetTextFont(61);
  prelimTexOB2.SetTextAlign(31);
  prelimTexOB2.SetLineWidth(2);
  prelimTexOB2.SetTextSize(0.08);
  prelimTexOB2.DrawLatex(0.81,0.83,"CMS");
  
  c3->Print("boxesComb_obsB_comb123.png");
  c3->Print("boxesComb_obsB_comb123.pdf");
  c3->Print("boxesComb_obsB.C");
  c3->Print("boxesComb_obsB.root");
  

}

