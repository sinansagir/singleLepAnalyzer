#!/usr/bin/python

from ROOT import gROOT,TGraph,TCanvas,TLatex,TLine
import os,sys,math,itertools
from numpy import linspace
from array import array

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

lumiPlot = '12.9'
lumiStr = '12p892'
distribution = 'ST'
signal = 'X53X53'
chiral = 'left'
limitDir='/user_data/ssagir/x53x53_limits_2016/templates_ST_2016_9_6/all/'#_beforeRebinning/'
postfix = '' # for plot names in order to save them as different files
isRebinned='_rebinned_stat0p3'
xrange_min=700.
xrange_max=1200.
yrange_min=.0003+.01
yrange_max=3.05

massPoints = [700,800,900,1000,1100,1200]#,1300,1400,1500,1600]
mass = array('d', massPoints)
masserr = array('d', [0]*len(massPoints))
mass_str = [str(item) for item in massPoints]

theory_xsec_dicts = {'700':0.455,'800':0.196,'900':0.0903,'1000':0.0440,'1100':0.0224,'1200':0.0118,'1300':0.00639,'1400':0.00354,'1500':0.00200,'1600':0.001148}
theory_xsec = [theory_xsec_dicts[item] for item in mass_str]
xsec = array('d', [1]*len(massPoints)) # scales the limits

theory = TGraph(len(mass))
for i in range(len(mass)):
	theory.SetPoint(i, mass[i], theory_xsec[i])

def getSensitivity(index, exp):
	a1=mass[index]-mass[index-1]
	b1=mass[index]-mass[index-1]
	c1=0
	a2=exp[index]-exp[index-1]
	b2=theory_xsec[index]-theory_xsec[index-1]
	c2=theory_xsec[index-1]-exp[index-1]
	s = (c1*b2-c2*b1)/(a1*b2-a2*b1)
	t = (a1*c2-a2*c1)/(a1*b2-a2*b1)
	return mass[index-1]+s*(mass[index]-mass[index-1]), exp[index-1]+s*(exp[index]-exp[index-1])

# cutStrings = [x for x in os.walk(limitDir).next()[1]]
# cutStrings = ['lep30_MET150_NJets4_NBJets0_DR0.75_1jet450_2jet150_3jet0', #minMlb
# 			  'lep30_MET150_NJets4_NBJets0_DR1_1jet450_2jet150_3jet0',
# 			  'lep80_MET150_NJets4_NBJets0_DR1_1jet450_2jet150_3jet0',
# 			  'lep30_MET100_NJets4_NBJets0_DR1_1jet450_2jet150_3jet0',
# 			  'lep80_MET100_NJets4_NBJets0_DR1_1jet450_2jet150_3jet0',
# 			  'lep30_MET150_NJets4_NBJets0_DR1_1jet200_2jet90_3jet0',
# 			  'lep80_MET100_NJets4_NBJets0_DR1_1jet200_2jet90_3jet0',
# 			  ]
cutStrings = ['lep30_MET100_NJets3_NBJets0_DR0.75_1jet250_2jet50_3jet0', #ST
			  'lep30_MET100_NJets3_NBJets0_DR1_1jet250_2jet50_3jet0',
			  'lep30_MET100_NJets4_NBJets0_DR1_1jet250_2jet50_3jet0',
			  'lep80_MET100_NJets3_NBJets0_DR1_1jet250_2jet50_3jet0',
			  'lep80_MET100_NJets4_NBJets0_DR1_1jet250_2jet50_3jet0',
			  'lep80_MET100_NJets4_NBJets0_DR1_1jet200_2jet90_3jet0',
			  ]
observed = {}
expected = {}
expected68 = {}
expected95 = {}
crossingList = {}
ind=0
for cutString in cutStrings:
	plotLimits = True
	for kutle in mass_str:
		if not os.path.exists(limitDir+'/'+cutString+'/limits_templates_'+distribution+'_'+signal+'M'+kutle+chiral+'_'+lumiStr+'fb'+isRebinned+'_expected.txt'): 
			plotLimits = False
	if not plotLimits: continue
	if (ind % 500)==0: 
		print "Finished",ind,"out of",len(cutStrings) 
		print cutString
	cutString0 = cutString

	exp   =array('d',[0 for i in range(len(mass))])
	experr=array('d',[0 for i in range(len(mass))])
	obs   =array('d',[0 for i in range(len(mass))])
	obserr=array('d',[0 for i in range(len(mass))])
	exp68H=array('d',[0 for i in range(len(mass))])
	exp68L=array('d',[0 for i in range(len(mass))])
	exp95H=array('d',[0 for i in range(len(mass))])
	exp95L=array('d',[0 for i in range(len(mass))])

	observed[cutString] = TGraph(len(mass))
	expected[cutString] = TGraph(len(mass))

	isCrossed = False
	for i in range(len(mass)):
		lims = {}

		fobs = open(limitDir+'/'+cutString+'/limits_templates_'+distribution+'_'+signal+'M'+mass_str[i]+chiral+'_'+lumiStr+'fb'+isRebinned+'_observed.txt', 'rU')
		linesObs = fobs.readlines()
		fobs.close()

		fexp = open(limitDir+'/'+cutString+'/limits_templates_'+distribution+'_'+signal+'M'+mass_str[i]+chiral+'_'+lumiStr+'fb'+isRebinned+'_expected.txt', 'rU')
		linesExp = fexp.readlines()
		fexp.close()

		lims[-1] = float(linesObs[1].strip().split()[1])
		obs[i] = float(linesObs[1].strip().split()[1]) * xsec[i]
		obserr[i] = 0

		lims[.5] = float(linesExp[1].strip().split()[1])
		exp[i] = float(linesExp[1].strip().split()[1]) * xsec[i]
		experr[i] = 0
		lims[.16] = float(linesExp[1].strip().split()[4])
		exp68L[i] = float(linesExp[1].strip().split()[4]) * xsec[i]
		lims[.84] = float(linesExp[1].strip().split()[5])
		exp68H[i] = float(linesExp[1].strip().split()[5]) * xsec[i]
		lims[.025] = float(linesExp[1].strip().split()[2])
		exp95L[i] = float(linesExp[1].strip().split()[2]) * xsec[i]
		lims[.975] = float(linesExp[1].strip().split()[3])
		exp95H[i] = float(linesExp[1].strip().split()[3]) * xsec[i]

		exp95L[i]=(exp[i]-exp95L[i])
		exp95H[i]=abs(exp[i]-exp95H[i])
		exp68L[i]=(exp[i]-exp68L[i])
		exp68H[i]=abs(exp[i]-exp68H[i])
		observed[cutString].SetPoint(i,mass[i],obs[i])
		expected[cutString].SetPoint(i,mass[i],exp[i])

		if i!=0: 
			if(exp[i]>theory_xsec[i] and exp[i-1]<theory_xsec[i-1]) or (exp[i]<theory_xsec[i] and exp[i-1]>theory_xsec[i-1]):
				xcross,ycross = getSensitivity(i,exp)
				crossingList[cutString]=xcross
				isCrossed = True

		round_i = 5
	if not isCrossed:
		crossingList[cutString]=0

	ind+=1
	observed[cutString].SetLineColor(ROOT.kBlack)
	observed[cutString].SetLineWidth(2)
	observed[cutString].SetMarkerStyle(20)							
	expected[cutString].SetLineColor(ind)
	expected[cutString].SetLineWidth(2)
	expected[cutString].SetLineStyle(1)

sensitivity = 0
insensitivity = 999999
sensitivityStr = 'None'
insensitivityStr = 'None'
for key in crossingList.keys():
	print key,crossingList[key]
	if crossingList[key]>sensitivity: 
		sensitivity = crossingList[key]
		sensitivityStr = key
	if crossingList[key]==0: print key
	elif crossingList[key]<insensitivity: 
		insensitivity = crossingList[key]
		insensitivityStr = key
print "********************************************************************************"
print "Run over", ind, "sets of cuts"
print "********************************************************************************"
print "The best set of cuts are ", sensitivityStr
print "with sensitivity up to ", sensitivity, "GeV"
print "********************************************************************************"
print "The worst set of cuts are ", insensitivityStr
print "with sensitivity up to ", insensitivity, "GeV"

if sensitivityStr!='None': cutString0 = sensitivityStr
                                               
c0 = TCanvas("c0","Limits", 1000, 800)
c0.SetBottomMargin(0.15)
c0.SetRightMargin(0.06)
c0.SetLogy()
	
expected[cutString0].Draw('AL')
expected[cutString0].GetYaxis().SetRangeUser(yrange_min,yrange_max)
expected[cutString0].GetXaxis().SetRangeUser(xrange_min,xrange_max)
if 'X53' in signal:
	expected[cutString0].GetXaxis().SetTitle('X_{5/3} mass [GeV]')
	expected[cutString0].GetYaxis().SetTitle('#sigma(X_{5/3}#bar{X}_{5/3})[pb] - '+chiral.replace('left','LH').replace('right','RH'))
else:
	expected[cutString0].GetXaxis().SetTitle('T mass [GeV]')
	expected[cutString0].GetYaxis().SetTitle('#sigma(T#bar{T})[pb]')

for key in expected.keys():
	if key == cutString0: continue
	expected[key].Draw("same")

theory.SetLineColor(2)
theory.SetLineStyle(1)
theory.SetLineWidth(2)
theory.Draw("same")

sensitivityline = TLine(sensitivity,yrange_min,sensitivity,yrange_max)
sensitivityline.Draw("same")
insensitivityline = TLine(insensitivity,yrange_min,insensitivity,yrange_max)
insensitivityline.Draw("same")

prelimtex = TLatex()
prelimtex.SetNDC()
prelimtex.SetTextSize(0.03)
prelimtex.SetTextAlign(11) # align right
prelimtex.DrawLatex(0.58, 0.96, "CMS Preliminary, " + str(lumiPlot) + " fb^{-1} (13 TeV)")

folder='.'
if not os.path.exists(folder+'/'+limitDir.split('/')[-2]+'plots'): os.system('mkdir '+folder+'/'+limitDir.split('/')[-2]+'plots')
c0.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+distribution+postfix+'_logy.root')
c0.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+distribution+postfix+'_logy.pdf')
c0.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+distribution+postfix+'_logy.png')
c0.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+distribution+postfix+'_logy.eps')

c1 = TCanvas("c1","Limits", 1000, 800)
c1.SetBottomMargin(0.15)
c1.SetRightMargin(0.06)
#c1.SetLogy()
	
expected[cutString0].Draw('AL')
expected[cutString0].GetYaxis().SetRangeUser(yrange_min,yrange_max)
expected[cutString0].GetXaxis().SetRangeUser(xrange_min,xrange_max)
if 'X53' in signal:
	expected[cutString0].GetXaxis().SetTitle('X_{5/3} mass [GeV]')
	expected[cutString0].GetYaxis().SetTitle('#sigma(X_{5/3}#bar{X}_{5/3})[pb] - '+chiral.replace('left','LH').replace('right','RH'))
else:
	expected[cutString0].GetXaxis().SetTitle('T mass [GeV]')
	expected[cutString0].GetYaxis().SetTitle('#sigma(T#bar{T})[pb]')


for key in expected.keys():
	if key == cutString0: continue
	expected[key].Draw("same")

theory.SetLineColor(2)
theory.SetLineStyle(1)
theory.SetLineWidth(2)
theory.Draw("same")

sensitivityline = TLine(sensitivity,yrange_min,sensitivity,yrange_max)
sensitivityline.Draw("same")
insensitivityline = TLine(insensitivity,yrange_min,insensitivity,yrange_max)
insensitivityline.Draw("same")

prelimtex = TLatex()
prelimtex.SetNDC()
prelimtex.SetTextSize(0.03)
prelimtex.SetTextAlign(11) # align right
prelimtex.DrawLatex(0.58, 0.96, "CMS Preliminary, " + str(lumiPlot) + " fb^{-1} (13 TeV)")

folder='.'
c1.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+distribution+postfix+'_liny.root')
c1.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+distribution+postfix+'_liny.pdf')
c1.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+distribution+postfix+'_liny.png')
c1.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+distribution+postfix+'_liny.eps')


