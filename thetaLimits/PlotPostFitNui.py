from ROOT import *
from array import array
from math import *
import os,sys,pickle

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

isBkgOnly = False
saveKey='test'
lumiPlot = '35.9'
lumiStr = '35p867'
spin='left'#'right'
discriminant='minMlb'#'ST'
saveKey+=discriminant
histPrefix=discriminant+'_'+str(lumiStr)+'fb'+spin
stat='0p3'
cat=str(sys.argv[1])#'_isE_nT0p_nW0p_nB2p'
saveKey=cat
isRebinned='_rebinned_stat'+str(stat).replace('.','p')
if isBkgOnly: isRebinned+='_bkgonly'
tempKey='postfit_test/noMnT1pnW1pnB2p'
limitDir='templates_M17WtSF_2017_3_31_SRpCRplots/'+tempKey+'/'
cutString=''#'lep80_MET100_NJets4_DR1_1jet200_2jet90'
LH700file='/templates_'+discriminant+'_X53X53M900'+spin+'_'+str(lumiStr)+'fb'+isRebinned+cat+'.p'
print LH700file

parVals=pickle.load(open(limitDir+cutString+LH700file,'rb'))

sigproc = 'sig'
if isBkgOnly: sigproc = ''
nuisNam = []
nuisVal = []
nuisErr = []
for nuis in parVals[sigproc].keys():
	if nuis=='__cov' or nuis=='__nll' or nuis=='beta_signal': continue
	nuisNam.append(nuis)
	nuisVal.append(parVals[sigproc][nuis][0][0])
	nuisErr.append(parVals[sigproc][nuis][0][1])
	print nuis,"=",parVals[sigproc][nuis][0][0],"+/-",parVals[sigproc][nuis][0][1]

nuisNamPlot = {
		   'pdfNew':'PDF',
		   'topmuRFcorrdNew':'muRF(TOP)',
		   'ewkmuRFcorrdNew':'muRF(EWK)',
		   'qcdmuRFcorrdNew':'muRF(QCD)',
		   'qcdScale':'muRF(QCD)',
		   'sigmuRFcorrdNew':'muRF(LH-900GeV)',
		   'muRFcorrdNew':'muRF',
		   'toppt':'top p_{T}',
		   'tau21':'#tau_{2}/#tau_{1}',
		   'jms':'JMS',
		   'jmr':'JMR',
		   'taupt':'#tau_{2}/#tau_{1} p_{T}',
		   'topsf':'t-tag',
		   'btag':'b/c-tag',
		   'mistag':'udsg-mistag',
		   'jer':'JER',
		   'jec':'JEC',
		   'pileup':'pileup',
		   'eltrigeff':'elTrig',
		   'mutrigeff':'muTrig',
		   'ht':'HT',
		   'muIsoSys':'muIso',
		   'elIsoSys':'elIso',
		   'muIdSys':'muId',
		   'elIdSys':'elId',
		   'lumiSys':'lumi',
		   'top_rate':'top_rate',
		   'ewk_rate':'ewk_rate',
		   }

#if isBkgOnly: del nuisNam[4]
#nuisNamPlot={}
#for nui in nuisNam: nuisNamPlot[nui]=nui

nuisVal = []
nuisErr = []
for i in range(len(nuisNam)):
	nuis = nuisNam[i]
	nuisVal.append(parVals[sigproc][nuis][0][0])
	nuisErr.append(parVals[sigproc][nuis][0][1])
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
c.SetLeftMargin(0.3)
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
ax_2.SetNdivisions(5,kTRUE)
for i in range(nNuis):
	ax_1.SetBinLabel(i+2, nuisNamPlot[nuisNam[i]])

g95.GetHistogram().Draw('axis,same')
c.Modified()
c.Update()

c.SaveAs(limitDir.replace(tempKey,'')+'postFitNuis'+isRebinned+saveKey+'.pdf')
c.SaveAs(limitDir.replace(tempKey,'')+'postFitNuis'+isRebinned+saveKey+'.eps')
c.SaveAs(limitDir.replace(tempKey,'')+'postFitNuis'+isRebinned+saveKey+'.png')


