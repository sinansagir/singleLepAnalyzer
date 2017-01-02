{
  Double_t dy, dx, x, y, a, m, tZ;
  Double_t bW[21]={0.0,0.0,0.0,0.0,0.0,0.000,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,0.999};//0.5,
  Double_t tH[21]={0.0,0.2,0.4,0.6,0.8,0.999,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.000};//0.25
  //  int Mexp[21]={0, 0, 757, 786, 815, 848, 0, 723, 768, 792, 824, 742, 769, 791, 816, 792, 805, 827, 847, 853, 882};
  //  int Mobs[21]={781, 833, 871, 892, 917, 943, 804, 847, 878, 897, 926, 848, 870, 890, 910, 880, 891, 903, 907, 919, 946};
  int Mexp[21]={0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 710, 720, 733, 744, 789, 791, 793, 843, 845, 884};
  int Mobs[21]={0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 750, 751, 758, 768, 813, 812, 817, 870, 869, 905};

  TH2D *Hobs = new TH2D("Hobs",";B(tH);B(bW)",6,-0.1,1.1,6,-0.1,1.1);
  TH2D *Hexp = new TH2D("Hexp",";B(tH);B(bW)",6,-0.1,1.1,6,-0.1,1.1);
  for(int i = 0; i < 21; i++){
    if(Mexp[i] == 0 && Mobs[i] == 0) continue;
    Hobs->Fill(tH[i],bW[i],Mobs[i]);
    Hexp->Fill(tH[i],bW[i],Mexp[i]);
  }


  // create graph
  TCanvas *c1 = new TCanvas("c1","Graph Draw Options",1000,800);
  c1->GetFrame()->SetFillColor(42);
  c1->GetFrame()->SetLineColor(kWhite);
  
  c1->SetRightMargin(0.16);
  c1->SetTopMargin(0.10);
  c1->SetBottomMargin(0.10);
  
  gStyle->SetOptStat(0);
  gStyle->SetPalette(57);
  
  Hexp->GetZaxis()->SetRangeUser(700,900);
  Hexp->Draw("colz");
  
  TLatex t1;
  t1.SetTextAlign(22);
  t1.SetTextSize(0.040);
  
  for(int i = 0; i < 21; i++){
    if(Mexp[i] < 700) t1.DrawLatex(tH[i]+0.01,bW[i],"< 700");
    else{
     char value[10];
     std::snprintf(value, sizeof(value),"%i",Mexp[i]);     
     t1.DrawLatex(tH[i],bW[i],value);
   }
  } 
  
  t1.SetTextAlign(11);
  t1.DrawLatex(-0.1,1.15,"CMS 2.3/2.6/2.7 fb^{-1} (13 TeV)");
  t1.SetTextAlign(22);
  t1.SetTextAngle(-90);
  t1.DrawLatex(1.32,0.47,"expected T quark mass limit (GeV)");

  c1->Print("boxesSL_exp.png");
  c1->Print("boxesSL_exp.pdf");
  c1->Print("boxesSL_exp.C");
  c1->Print("boxesSL_exp.root");
  
  //---------------------------------
  
  TCanvas *c2 = new TCanvas("c2","Graph Draw Options",1000,800);
  c2->GetFrame()->SetFillColor(42);
  c2->GetFrame()->SetLineColor(kWhite);
  
  c2->SetRightMargin(0.16);
  c2->SetTopMargin(0.12);
  c2->SetBottomMargin(0.12);
  
  gStyle->SetOptStat(0);
  gStyle->SetPalette(57);
  
  Hobs->GetZaxis()->SetRangeUser(700,900);
  Hobs->Draw("colz");
  
  TLatex t2;
  t2.SetTextAlign(22);
  t2.SetTextSize(0.040);
  
  for(int i = 0; i < 21; i++){
    if(Mobs[i] < 700) t2.DrawLatex(tH[i]+0.01,bW[i],"< 700");
    else{
      char value[10];
      std::snprintf(value, sizeof(value),"%i",Mobs[i]);     
      t2.DrawLatex(tH[i],bW[i],value);
    }
  } 
  
  t2.SetTextAlign(11);
  t2.DrawLatex(-0.1,1.15,"CMS 2.3/2.6/2.7 fb^{-1} (13 TeV)");
  t2.SetTextAlign(22);
  t2.SetTextAngle(-90);
  t2.DrawLatex(1.32,0.47,"observed T quark mass limit (GeV)");
  
  c2->Print("boxesSL_obs.png");
  c2->Print("boxesSL_obs.pdf");
  c2->Print("boxesSL_obs.C");
  c2->Print("boxesSL_obs.root");

  //////////////////
  /*
  int MexpB[21]={0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 722, 0, 0, 740, 0, 736, 717};
  int MobsB[21]={0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 731, 760, 768, 771, 794, 817, 809, 832, 835};

  TH2D *HobsB = new TH2D("HobsB",";B(bH);B(tW)",6,-0.1,1.1,6,-0.1,1.1);
  TH2D *HexpB = new TH2D("HexpB",";B(bH);B(tW)",6,-0.1,1.1,6,-0.1,1.1);
  for(int i = 0; i < 21; i++){
    if(MexpB[i] != 0) HexpB->Fill(tH[i],bW[i],MexpB[i]);
    if(MobsB[i] != 0) HobsB->Fill(tH[i],bW[i],MobsB[i]);
  }

  
  // create graph
  TCanvas *c4 = new TCanvas("c4","Graph Draw Options",1000,800);
  c4->GetFrame()->SetFillColor(42);
  c4->GetFrame()->SetLineColor(kWhite);
  
  c4->SetRightMargin(0.16);
  c4->SetTopMargin(0.10);
  c4->SetBottomMargin(0.10);
  
  gStyle->SetOptStat(0);
  gStyle->SetPalette(57);
  
  HexpB->GetZaxis()->SetRangeUser(700,830);
  HexpB->Draw("colz");
  
  TLatex t4;
  t4.SetTextAlign(22);
  t4.SetTextSize(0.040);
  
  for(int i = 0; i < 21; i++){
    if(MexpB[i] < 700) t4.DrawLatex(tH[i]+0.01,bW[i],"< 700");
    else{
      char value[10];
      std::snprintf(value, sizeof(value),"%i",MexpB[i]);     
      t4.DrawLatex(tH[i],bW[i],value);
    }
  } 
  
  t4.SetTextAlign(11);
  t4.DrawLatex(-0.1,1.15,"CMS 2.3/2.6/2.7 fb^{-1} (13 TeV)");
  t4.SetTextAlign(22);
  t4.SetTextAngle(-90);
  t4.DrawLatex(1.32,0.47,"expected B quark mass limit (GeV)");
  
  c4->Print("boxesComb_expB.png");
  c4->Print("boxesComb_expB.pdf");
  c4->Print("boxesComb_expB.C");
  c4->Print("boxesComb_expB.root");
  
  //---------------------------------

  TCanvas *c3 = new TCanvas("c3","Graph Draw Options",1000,800);
  c3->GetFrame()->SetFillColor(42);
  c3->GetFrame()->SetLineColor(kWhite);
  
  c3->SetRightMargin(0.16);
  c3->SetTopMargin(0.12);
  c3->SetBottomMargin(0.12);
  
  gStyle->SetOptStat(0);
  gStyle->SetPalette(57);
  
  HobsB->GetZaxis()->SetRangeUser(700,830);
  HobsB->Draw("colz");

  TLatex t5;
  t5.SetTextAlign(22);
  t5.SetTextSize(0.040);
  
  for(int i = 0; i < 21; i++){
    if(MobsB[i] < 700) t5.DrawLatex(tH[i]+0.01,bW[i],"< 700");
    else{
      char value[10];
      std::snprintf(value, sizeof(value),"%i",MobsB[i]);     
      t5.DrawLatex(tH[i],bW[i],value);
    }
  } 
  
  t5.SetTextAlign(11);
  t5.DrawLatex(-0.1,1.15,"CMS 2.3/2.6/2.7 fb^{-1} (13 TeV)");
  t5.SetTextAlign(22);
  t5.SetTextAngle(-90);
  t5.DrawLatex(1.32,0.47,"observed B quark mass limit (GeV)");
  
  c3->Print("boxesComb_obsB.png");
  c3->Print("boxesComb_obsB.pdf");
  c3->Print("boxesComb_obsB.C");
  c3->Print("boxesComb_obsB.root");
*/

}
