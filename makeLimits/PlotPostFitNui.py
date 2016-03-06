from ROOT import *
from array import array
from math import *
import os,sys,pickle

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

blind=False
saveKey=''
lumiPlot = '2.3'
lumiStr = '2p318'
spin=''#'right'
discriminant='minMlb'
histPrefix=discriminant+'_'+str(lumiStr)+'fb'+spin
stat=''#0.75
isRebinned='_rebinned'+str(stat).replace('.','p')
tempKey='all_forPostFitNuis'
limitDir='/user_data/ssagir/limits/templates_minMlb_tau21LT0p6_tptp_2016_3_4/'+tempKey+'/'
cutString='lep40_MET75_1jet300_2jet150_NJets3_NBJets0_3jet100_4jet0_5jet0_DR1_1Wjet0_1bjet0_HT0_ST0_minMlb0'
LH700file='/templates_'+discriminant+'_TTM800'+spin+'_'+str(lumiStr)+'fb'+isRebinned+'.p'

parVals=pickle.load(open(limitDir+cutString+LH700file,'rb'))

nuisNam = []
nuisVal = []
nuisErr = []
for nuis in parVals['sig'].keys():
	if nuis=='__cov' or nuis=='__nll': continue
	nuisNam.append(nuis)
	nuisVal.append(parVals['sig'][nuis][0][0])
	nuisErr.append(parVals['sig'][nuis][0][1])
	print nuis,"=",parVals['sig'][nuis][0][0],"+/-",parVals['sig'][nuis][0][1]

nuisNam = [
			'pdfNew',
			'muRFcorrdNew',
			'q2',
			'toppt',
			'tau21',
			'jms',
			'jmr',
			'jsf',
			'btag',
			'jer',
			'jec',
			'pileup',
			'top1pW3pBSys',
			'top1pW2BSys',
			'top1pW1BSys',
			'top1pW0BSys',
			'top0W3pBSys',
			'top0W2BSys',
			'top0W1BSys',
			'top0W0BSys',
			'ewk1pW3pBSys',
			'ewk1pW2BSys',
			'ewk1pW1BSys',
			'ewk1pW0BSys',
			'ewk0W3pBSys',
			'ewk0W2BSys',
			'ewk0W1BSys',
			'ewk0W0BSys',
			'muTrigSys',
			'elTrigSys',
			'muIsoSys',
			'elIsoSys',
			'muIdSys',
			'elIdSys',
			'lumiSys',
			]

nuisNamPlot = [
			'PDF',
			'muRF',
			'Q^{2}',
			'Top Pt',
			'Tau21',
			'JMS',
			'JMR',
			'JSF',
			'Btag',
			'JER',
			'JEC',
			'pileup',
			'top_1+W_3+b',
			'top_1+W_2b',
			'top_1+W_1b',
			'top_1+W_0b',
			'top_0W_3+b',
			'top_0W_2b',
			'top_0W_1b',
			'top_0W_0b',
			'ewk_1+W_3+b',
			'ewk_1+W_2b',
			'ewk_1+W_1b',
			'ewk_1+W_0b',
			'ewk_0W_3+b',
			'ewk_0W_2b',
			'ewk_0W_1b',
			'ewk_0W_0b',
			'muTrig',
			'elTrig',
			'muIso',
			'elIso',
			'muId',
			'elId',
			'lumi',
			]

nuisVal = []
nuisErr = []
for i in range(len(nuisNam)):
	nuis = nuisNam[i]
	nuisVal.append(parVals['sig'][nuis][0][0])
	nuisErr.append(parVals['sig'][nuis][0][1])
nNuis = len(nuisNam)

g   = TGraphAsymmErrors(nNuis)
g68 = TGraph(2*nNuis+7)
g95 = TGraph(2*nNuis+7)
for i in range(nNuis):
	g.SetPoint(i, nuisVal[i], i+1.5)
	g.SetPointEXlow(i, nuisErr[i])
	g.SetPointEXhigh(i, nuisErr[i])
for a in xrange(0, nNuis+3):
	g68.SetPoint(a, -1, a)
	g95.SetPoint(a, -1.99, a)
	g68.SetPoint(a+1+nNuis+2, 1, nNuis+2-a)
	g95.SetPoint(a+1+nNuis+2, 1.99, nNuis+2-a)

g.SetLineStyle(1)
g.SetLineWidth(1)
g.SetLineColor(1)
g.SetMarkerStyle(21)
g.SetMarkerSize(1.25)
g68.SetFillColor(ROOT.kGreen)
g95.SetFillColor(ROOT.kYellow)

c = TCanvas('PostFit', 'PostFit', 1000, 1200)
c.SetTopMargin(0.06)
c.SetRightMargin(0.06)
c.SetBottomMargin(0.12)
c.SetLeftMargin(0.25)
c.SetTickx()
c.SetTicky()
	
g95.Draw('AF')
g68.Draw('F')
g.Draw('P')


prim_hist = g95.GetHistogram() 
ax_1 = prim_hist.GetYaxis()
ax_2 = prim_hist.GetXaxis()

g95.SetTitle('')
ax_2.SetTitle('post-fit values')
#ax_2.SetTitle('deviation in units of #sigma')
ax_1.SetTitleSize(0.050)
ax_2.SetTitleSize(0.050)
ax_1.SetTitleOffset(1.4)
ax_2.SetTitleOffset(1.0)
ax_1.SetLabelSize(0.05)
#ax_2.SetLabelSize(0.05)
ax_1.SetRangeUser(0, nNuis+2)
ax_2.SetRangeUser(-2.2, 2.2)

ax_1.Set(nNuis+2, 0, nNuis+2)
ax_1.SetNdivisions(-414)
#ax_2.SetNdivisions(-505)
for i in range(nNuis):
	ax_1.SetBinLabel(i+2, nuisNamPlot[i])

g95.GetHistogram().Draw('axis,same')
c.Modified()
c.Update()

c.SaveAs('postFitNuis.root')
c.SaveAs('postFitNuis.pdf')
c.SaveAs('postFitNuis.png')
c.SaveAs('postFitNuis.C')


