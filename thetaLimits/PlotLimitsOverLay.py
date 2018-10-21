#!/usr/bin/python

from ROOT import gROOT,TGraph,TCanvas,TLatex,TLine,TLegend
import os,sys,math,itertools
from numpy import linspace
from array import array

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

blind = True
lumiPlot = '36.8'
signal = 'X53X53'
chiral = 'left'
postfix = '' # for plot names in order to save them as different files
xrange_min=700.
xrange_max=1600.
yrange_min=.002+.00001
yrange_max=0.205

mass_str = ['700','800','900','1000','1100','1200','1300','1400','1500','1600']
theory_xsec = [0.455,0.196,0.0903,0.0440,0.0224,0.0118,0.00639,0.00354,0.00200,0.001148,0.000666,0.000391][:len(mass_str)]#pb

massPoints = [int(mass) for mass in mass_str]
mass = array('d', massPoints)
masserr = array('d', [0]*len(massPoints))
mass_str = [str(item) for item in massPoints]

theory_xsec_dicts = {mass_str[ind]:theory_xsec[ind] for ind in range(len(mass_str))}
theory_xsec = [theory_xsec_dicts[item] for item in mass_str]
xsec = array('d', [1]*len(massPoints)) # scales the limits

theory = TGraph(len(mass))
for i in range(len(mass)):
	theory.SetPoint(i, mass[i], theory_xsec[i])

limFiles   = [ #compare different optimized selections and discriminants
              '/user_data/ssagir/x53x53_limits_2016/templates_2017_2_10/all/limits_templates_ST_X53X53M800left_36p814fb_rebinned_stat0p3_expected.txt',
              '/user_data/ssagir/x53x53_limits_2016/templates_2017_2_10/all/limits_templates_minMlb_X53X53M800left_36p814fb_rebinned_stat0p3_expected.txt',
              '/user_data/ssagir/x53x53_limits_2016/templates_lep60_2017_2_10/all/limits_templates_ST_X53X53M800left_36p814fb_rebinned_stat0p3_expected.txt',
              '/user_data/ssagir/x53x53_limits_2016/templates_lep60_2017_2_10/all/limits_templates_minMlb_X53X53M800left_36p814fb_rebinned_stat0p3_expected.txt',
			  ]

limLegs    = [
              'ST -- lepPt>80 GeV',
              'minMlb -- lepPt>80 GeV',
              'ST -- lepPt>60 GeV',
              'minMlb -- lepPt>60 GeV',
			  ]

# limFiles   = [ #compare different optimized selections and discriminants
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all/limits_templates_YLD_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all/limits_templates_YLD_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
# 			  ]
# 
# limLegs    = [
#               'optimize ST -- use Counting',
#               'optimize ST -- use ST',
#               'optimize ST -- use minMlb',
#               'optimize minMlb -- use Counting',
#               'optimize minMlb -- use ST',
#               'optimize minMlb -- use minMlb',
# 			  ]

# limFiles   = [ #compare different binning and selections for minMlb
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p15_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p25_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p15_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p25_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
# 			  ]
# 
# limLegs    = [
#               'optimize ST -- use minMlb -- 15%',
#               'optimize ST -- use minMlb -- 25%',
#               'optimize ST -- use minMlb -- 30%',
#               'optimize minMlb -- use minMlb -- 15%',
#               'optimize minMlb -- use minMlb -- 25%',
#               'optimize minMlb -- use minMlb -- 30%',
# 			  ]
# 
# limFiles   = [ #compare different binning and selections for ST
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p15_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p25_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p15_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p25_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
# 			  ]
# 
# limLegs    = [
#               'optimize ST -- use ST -- 15%',
#               'optimize ST -- use ST -- 25%',
#               'optimize ST -- use ST -- 30%',
#               'optimize minMlb -- use ST -- 15%',
#               'optimize minMlb -- use ST -- 25%',
#               'optimize minMlb -- use ST -- 30%',
# 			  ]

# limFiles   = [ #compare different optimized selections and discriminants with and w/o syst. unc. (w/o=50% on bkgs and 10% on sig)
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
# 
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all_noShpSys/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_STselect/all_noShpSys/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all_noShpSys/limits_templates_ST_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
#               '/user_data/ssagir/x53x53_limits_2016/templates_2016_11_18_wJSF_minMlbselect/all_noShpSys/limits_templates_minMlb_X53X53M800left_36p0fb_rebinned_stat0p3_expected.txt',
# 			  ]
# 
# limLegs    = [
#               'optimize ST -- use ST',
#               'optimize ST -- use minMlb',
#               'optimize minMlb -- use ST',
#               'optimize minMlb -- use minMlb',
# 
#               'optimize ST -- use ST (no shape syst)',
#               'optimize ST -- use minMlb (no shape syst)',
#               'optimize minMlb -- use ST (no shape syst)',
#               'optimize minMlb -- use minMlb (no shape syst)',
# 			  ]

observed = {}
expected = {}
crossingList = {}
ind=0
skipped=[]
for limFile in limFiles:
	exp   =array('d',[0 for i in range(len(mass))])
	experr=array('d',[0 for i in range(len(mass))])
	obs   =array('d',[0 for i in range(len(mass))])
	obserr=array('d',[0 for i in range(len(mass))])

	observed[limFile] = TGraph(len(mass))
	expected[limFile] = TGraph(len(mass))

	isCrossed = False
	for i in range(len(mass)):
		lims = {}

		fexp = open(limFile.replace(signal+'M800',signal+'M'+mass_str[i]).replace('left',chiral), 'rU')
		linesExp = fexp.readlines()
		fexp.close()

		if not blind: fobs = open(limFile.replace(signal+'M800',signal+'M'+mass_str[i]).replace('left',chiral).replace('_expected.txt','_observed.txt'), 'rU')
		else: fobs = open(limFile.replace(signal+'M800',signal+'M'+mass_str[i]).replace('left',chiral), 'rU')
		linesObs = fobs.readlines()
		fobs.close()

		lims[-1] = float(linesObs[1].strip().split()[1])
		obs[i] = float(linesObs[1].strip().split()[1]) * xsec[i]
		obserr[i] = 0

		lims[.5] = float(linesExp[1].strip().split()[1])
		exp[i] = float(linesExp[1].strip().split()[1]) * xsec[i]
		experr[i] = 0

		observed[limFile].SetPoint(i,mass[i],obs[i])
		expected[limFile].SetPoint(i,mass[i],exp[i])

	ind+=1
	observed[limFile].SetLineColor(ROOT.kBlack)
	observed[limFile].SetLineWidth(2)
	observed[limFile].SetMarkerStyle(20)							
	expected[limFile].SetLineColor(ind)
	expected[limFile].SetLineWidth(2)
	expected[limFile].SetLineStyle(1)
                                               
c0 = TCanvas("c0","Limits", 1000, 800)
c0.SetBottomMargin(0.15)
c0.SetRightMargin(0.06)
c0.SetLogy()
	
expected[limFiles[0]].Draw('AL')
expected[limFiles[0]].GetYaxis().SetRangeUser(yrange_min,yrange_max)
expected[limFiles[0]].GetXaxis().SetRangeUser(xrange_min,xrange_max)
if 'X53' in signal:
	expected[limFiles[0]].GetXaxis().SetTitle('X_{5/3} mass [GeV]')
	expected[limFiles[0]].GetYaxis().SetTitle('#sigma(X_{5/3}#bar{X}_{5/3})[pb] - '+chiral.replace('left','LH').replace('right','RH'))
elif signal=='HTB':
	expected[limFiles[0]].GetXaxis().SetTitle("H^{#pm} mass [GeV]")
	expected[limFiles[0]].GetYaxis().SetTitle("#sigma#times(H^{#pm}#rightarrowtb)[pb]")
else:
	expected[limFiles[0]].GetXaxis().SetTitle('T mass [GeV]')
	expected[limFiles[0]].GetYaxis().SetTitle('#sigma(T#bar{T})[pb]')

for limFile in limFiles:
	if limFile == limFiles[0]: continue
	expected[limFile].Draw("same")

theory.SetLineColor(2)
theory.SetLineStyle(2)
theory.SetLineWidth(2)
theory.Draw("same")

leg = TLegend(.35,.70,.93,.93)
leg.AddEntry(expected[limFiles[0]], limLegs[0], "l")
i=-1
for limFile in limFiles:
	i+=1
	if limFile == limFiles[0]: continue
	leg.AddEntry(expected[limFile], limLegs[i], "l")

prelimtex = TLatex()
prelimtex.SetNDC()
prelimtex.SetTextSize(0.03)
prelimtex.SetTextAlign(11) # align right
prelimtex.DrawLatex(0.58, 0.96, "CMS Preliminary, " + str(lumiPlot) + " fb^{-1} (13 TeV)")

leg.SetShadowColor(0);
leg.SetFillColor(0);
leg.SetLineColor(0);
leg.Draw() 

folder='.'
c0.SaveAs(folder+'/overlayPlots/2017_2_10/overlayPlots_'+chiral.replace('left','LH').replace('right','RH')+'.pdf')
c0.SaveAs(folder+'/overlayPlots/2017_2_10/overlayPlots_'+chiral.replace('left','LH').replace('right','RH')+'.png')
c0.SaveAs(folder+'/overlayPlots/2017_2_10/overlayPlots_'+chiral.replace('left','LH').replace('right','RH')+'.eps')

