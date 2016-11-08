#!/usr/bin/python

from ROOT import gROOT,TGraph,TCanvas,TLatex,TLine,TLegend
import os,sys,math,itertools
from numpy import linspace
from array import array

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

blind = True
lumiPlot = '33.6'
signal = 'HTB'
postfix = '' # for plot names in order to save them as different files
xrange_min=180.
xrange_max=500.
yrange_min=.3+.01
yrange_max=20.05

massPoints = [180,200,250,300,350,400,450,500]
mass = array('d', massPoints)
masserr = array('d', [0]*len(massPoints))
mass_str = [str(item) for item in massPoints]

theory_xsec_dicts = {'180':0.919,'200':0.783951,'250':0.4982015,'300':0.324766,'350':0.2184385,'400':0.148574,'450':0.104141,'500':0.0735225}
theory_xsec = [theory_xsec_dicts[item] for item in mass_str]
xsec = array('d', [1]*len(massPoints)) # scales the limits

theory = TGraph(len(mass))
for i in range(len(mass)):
	theory.SetPoint(i, mass[i], theory_xsec[i])

limFiles   = ['/user_data/ssagir/HTB_limits_2016/templates_BDT_ATLAS_All_2016_11_3/SR/lep50_MET30_NJets4p_NBJets2_1jet50_2jet40/limits_templates_BDT_HTBM180_33p59fb_rebinned_stat0p3_expected.txt',
			  '/user_data/ssagir/HTB_limits_2016/templates_BDT_ATLAS_All_2016_11_3/all/lep50_MET30_NJets4p_NBJets2_1jet50_2jet40/limits_templates_BDT_HTBM180_33p59fb_rebinned_stat0p3_expected.txt',
			  '/user_data/ssagir/HTB_limits_2016/templates_HT_ATLAS_2016_11_3/SR/lep50_MET30_NJets4p_NBJets2_1jet50_2jet40/limits_templates_HT_HTBM180_33p59fb_rebinned_stat0p3_expected.txt',
			  '/user_data/ssagir/HTB_limits_2016/templates_HT_ATLAS_2016_11_3/all/lep50_MET30_NJets4p_NBJets2_1jet50_2jet40/limits_templates_HT_HTBM180_33p59fb_rebinned_stat0p3_expected.txt',
			  '/user_data/ssagir/HTB_limits_2016/templates_BDT_trainedMassesFor3pB_2016_11_3/all/lep50_MET30_NJets4p_NBJets2_1jet50_2jet40/limits_templates_BDT_HTBM180_33p59fb_rebinned_stat0p3_expected.txt',
			  '/user_data/ssagir/HTB_limits_2016/templates_BDT_trainedMasses_2016_11_2/all/lep50_MET30_NJets4p_NBJets2_1jet50_2jet40/limits_templates_BDT_HTBM180_33p59fb_rebinned_stat0p3_expected.txt',
			  '/user_data/ssagir/HTB_limits_2016/templates_BDT_2016_11_2/all/lep50_MET30_NJets4p_NBJets2_1jet50_2jet40/limits_templates_BDT_HTBM180_33p59fb_rebinned_stat0p3_expected.txt',
			  '/user_data/ssagir/HTB_limits_2016/templates_HT_SR_True_New_2016_9_12_toys5000/all/lep50_MET30_1jet50_2jet40_NJets4_NBJets0_3jet0_4jet0_5jet0_DR0_1Wjet0_1bjet0_HT0_ST0_minMlb0/limits_templates_HT_HTBM180_12p892fb_rebinned_statSR0p3_expected.txt'
			  ]

limLegs    = ['BDT -- trained all signals for 3+b -- (4SR)',
			  'BDT -- trained all signals for 3+b -- (4SR+4CR)',
			  'HT -- (4SR)',
			  'HT -- (4SR+4CR)',
			  'BDT -- trained all signals for 3+b -- 2,3+b',
			  'BDT -- trained all signals for 2+b -- 2,3+b',
			  'BDT -- trained 500 GeV for 2+b -- 2,3+b',
			  'HT -- 0,1,2,3+b',
			  ]

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

		fexp = open(limFile.replace(signal+'M180',signal+'M'+mass_str[i]), 'rU')
		linesExp = fexp.readlines()
		fexp.close()

		if not blind: fobs = open(limFile.replace(signal+'M180',signal+'M'+mass_str[i]).replace('_expected.txt','_observed.txt'), 'rU')
		else: fobs = open(limFile.replace(signal+'M180',signal+'M'+mass_str[i]), 'rU')
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
theory.SetLineStyle(1)
theory.SetLineWidth(2)
#theory.Draw("same")

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
c0.SaveAs(folder+'/overlayPlots/overlayPlots_v2.pdf')
c0.SaveAs(folder+'/overlayPlots/overlayPlots_v2.png')
c0.SaveAs(folder+'/overlayPlots/overlayPlots_v2.eps')

