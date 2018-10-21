#!/usr/bin/python

from ROOT import gROOT,TGraph,TCanvas,TLatex,TLine,TLegend
import os,sys,math,itertools,json
from numpy import linspace
from array import array

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

lumiPlot = '36.8'
signal = 'X53X53'
chiral = 'right'
postfix = ''#'_noSyst'
xrange_min=700.
xrange_max=1600.
yrange_min=.0003+.01
yrange_max=6.05

massPoints = [700,800,900,1000,1100,1200,1300,1400,1500,1600]
mass = array('d', massPoints)
masserr = array('d', [0]*len(massPoints))
mass_str = [str(item) for item in massPoints]

theory_xsec_dicts = {'700':0.455,'800':0.196,'900':0.0903,'1000':0.0440,'1100':0.0224,'1200':0.0118,'1300':0.00639,'1400':0.00354,'1500':0.00200,'1600':0.001148}
theory_xsec = [theory_xsec_dicts[item] for item in mass_str]
xsec = array('d', [1]*len(massPoints)) # scales the limits

theory = TGraph(len(mass))
for i in range(len(mass)):
	theory.SetPoint(i, mass[i], theory_xsec[i])

sigFiles   = [ #compare different optimized selections and discriminants
              '/user_data/ssagir/x53x53_limits_2016/templates_2017_2_7_discovery'+postfix+'/all/templates_ST_X53X53M800left_36p814fb_rebinned_stat0p3.json',
              '/user_data/ssagir/x53x53_limits_2016/templates_2017_2_7_discovery'+postfix+'/all/templates_minMlb_X53X53M800left_36p814fb_rebinned_stat0p3.json',
              #'/user_data/ssagir/x53x53_limits_2016/templates_lep60_2017_2_10'+postfix+'/all/templates_ST_X53X53M800left_36p814fb_rebinned_stat0p3.json',
              #'/user_data/ssagir/x53x53_limits_2016/templates_lep60_2017_2_10'+postfix+'/all/templates_minMlb_X53X53M800left_36p814fb_rebinned_stat0p3.json',
			  ]

sigLegs    = [
              'ST -- lepPt>80 GeV',
              'minMlb -- lepPt>80 GeV',
              #'ST -- lepPt>60 GeV',
              #'minMlb -- lepPt>60 GeV',
			  ]

significance = {}
ind=0
comMass = 1000
maxSignificanceCut = ''
minSignificanceCut = ''
maxSignificance = -1
minSignificance = 1e9
for sigFile in sigFiles:
	plotLimits = True
	for kutle in mass_str:
		if not os.path.exists(sigFile.replace(signal+'M800',signal+'M'+mass_str[i]).replace('left',chiral)): 
			plotLimits = False
	if not plotLimits: continue

	expSigs_ = []
	masses_ = []
	for i in range(len(mass)):
		try:
			fsig = open(sigFile.replace(signal+'M800',signal+'M'+mass_str[i]).replace('left',chiral))
			linesSig = json.load(fsig)
			fsig.close()
			expSig = linesSig[0][0]
			#print fsig, expSig>5
			if expSig<5:
				expSigs_.append(expSig)
				masses_.append(mass[i])
				#significance[sigFile].SetPoint(i,mass[i],expSig)
			else: print "Expected Significance:",expSig,"SKIPPING"
		except: 
			print "NO JSON:",sigFile,mass[i]
			pass

	significance[sigFile] = TGraph(len(masses_))
	for i in range(len(masses_)): significance[sigFile].SetPoint(i,masses_[i],expSigs_[i])
	ind+=1							
	significance[sigFile].SetLineColor(ind)
	significance[sigFile].SetLineWidth(2)
	significance[sigFile].SetLineStyle(1)
                                               
c0 = TCanvas("c0","Limits", 1000, 800)
c0.SetBottomMargin(0.15)
c0.SetRightMargin(0.06)
#c0.SetLogy()
	
significance[sigFiles[0]].Draw('AL')
significance[sigFiles[0]].GetYaxis().SetRangeUser(yrange_min,yrange_max)
significance[sigFiles[0]].GetXaxis().SetRangeUser(xrange_min,xrange_max)
if 'X53' in signal:
	significance[sigFiles[0]].GetXaxis().SetTitle('X_{5/3} mass [GeV]')
	significance[sigFiles[0]].GetYaxis().SetTitle('Expected Significance - '+chiral.replace('left','LH').replace('right','RH'))
else:
	significance[sigFiles[0]].GetXaxis().SetTitle('T mass [GeV]')
	significance[sigFiles[0]].GetYaxis().SetTitle('Expected Significance ')

for key in significance.keys():
	if key == sigFiles[0]: continue
	significance[key].Draw("same")

leg = TLegend(.35,.70,.93,.93)
leg.AddEntry(significance[sigFiles[0]], sigLegs[0], "l")
i=-1
for sigFile in sigFiles:
	i+=1
	if sigFile == sigFiles[0]: continue
	leg.AddEntry(significance[sigFile], sigLegs[i], "l")
	
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
c0.SaveAs(folder+'/overlayPlots/2017_2_10/significance_'+chiral.replace('left','LH').replace('right','RH')+postfix+'2.pdf')
c0.SaveAs(folder+'/overlayPlots/2017_2_10/significance_'+chiral.replace('left','LH').replace('right','RH')+postfix+'2.png')
c0.SaveAs(folder+'/overlayPlots/2017_2_10/significance_'+chiral.replace('left','LH').replace('right','RH')+postfix+'2.eps')

