import os, sys
from ROOT import TFile, TH2D, TCanvas, TPaletteAxis, gPad, gStyle

limitdir = sys.argv[1]
mass = sys.argv[2]

BR = 'bW0p5_tZ0p25_tH0p25'
if 'BB' in mass: BR = 'tW0p5_bZ0p25_bH0p25'
mass = mass.replace('BB','')

path = limitdir+'/'+BR+'/cmb/'+mass
name = limitdir.replace('limits_templatesCR_June2020','').replace('limits_templatesSRCR_June2020','')

os.chdir(path)

if not os.path.exists('covariance_fit_b.png'):
    print "Running FitDiagnostics with plots"
    os.system('combine -M FitDiagnostics -d workspace.root --saveWorkspace --plots --saveShapes')

fd = TFile.Open("fitDiagnostics.root")
covar = fd.Get("covariance_fit_s");
covar.GetXaxis().SetRange(1,25);
covar.GetYaxis().SetRange(covar.GetNbinsY()-24,covar.GetNbinsY());
covar.SetMarkerSize(1.0)
covar.GetZaxis().SetLabelSize(0.03);

c1 = TCanvas("c1","c1",1200,600)
gStyle.SetOptStat(0)
gStyle.SetPaintTextFormat("%1.2f");
gStyle.SetPaintTextFormat("1.2f");
gPad.SetBottomMargin(0.15)
gPad.SetRightMargin(0.07)
gPad.SetLeftMargin(0.16)
palette = covar.GetListOfFunctions().FindObject("palette");
palette.SetX1NDC(0.93);
palette.SetX2NDC(0.96);
palette.SetY1NDC(0.15);
palette.SetY2NDC(0.9);

covar.Draw("colz text");

c1.SaveAs(name+'_covariance_s.png');
c1.SaveAs(name+'_covariance_s.pdf');

covar = fd.Get("covariance_fit_b");
covar.GetXaxis().SetRange(1,25);
covar.GetYaxis().SetRange(covar.GetNbinsY()-24,covar.GetNbinsY());
covar.SetMarkerSize(1.0)
covar.GetZaxis().SetLabelSize(0.03);

palette = covar.GetListOfFunctions().FindObject("palette");
palette.SetX1NDC(0.93);
palette.SetX2NDC(0.96);
palette.SetY1NDC(0.15);
palette.SetY2NDC(0.9);

covar.Draw("colz text");

c1.SaveAs(name+'_covariance_b.png');
c1.SaveAs(name+'_covariance_b.pdf');

