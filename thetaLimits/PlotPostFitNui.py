from ROOT import *
from array import array
from math import *
import os,sys,pickle

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

blind=False
saveKey=''
lumiPlot = '36.4'
lumiStr = '36p0'
spin=''#'right'
discriminant='minMlb'
histPrefix=discriminant+'_'+str(lumiStr)+'fb'+spin
stat='0.3'#0.75
isRebinned='_rebinned'
tempKey='all_postfit'
limitDir='/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/limits/templates_Wkshp/'+tempKey+'/'
cutString=''#SelectionFile'
LH700file='/templates_'+discriminant+'_TTM900_36p0fb_rebinned_stat0p3_noQ2.p' #

print limitDir+cutString+LH700file

parVals=pickle.load(open(limitDir+cutString+LH700file,'rb'))

nuisNam = []
nuisVal = []
nuisErr = []
for nuis in parVals[''].keys(): #TpTp_M-0800'].keys():
	if nuis=='__cov' or nuis=='__nll': continue
	nuisNam.append(nuis)
	nuisVal.append(parVals[''][nuis][0][0])
	nuisErr.append(parVals[''][nuis][0][1])
	print nuis,"=",parVals[''][nuis][0][0],"+/-",parVals[''][nuis][0][1]


nuisNam = [
	'ewksys',
	'topsys',
	'qcdsys',
	'elIdSys',#
	'muIdSys',#
	'elIsoSys',#
	'muIsoSys',#
	'elTrigSys',#
	'muTrigSys',#
	'lumiSys',#
	'pileup',#
	'jec',
	'jer',
	#'higgs_smear',
	#'higgs_py2hw',
	#'btag_udsg', #'mistag',#
	#'btag_bc', #'btag',#
	'jsf',
	'tau21',
	'toppt',
	#'q2',
	'muRFcorrdNew',#
	'pdfNew',#
	#'QCD_rate',
	#'DYJets_rate',
	#'Diboson_rate',
	#'SingleTop_rate',
	#'WJets_rate',
	#'TTbar_rate',
	]

nuisNamPlot = [
	'EWK flat',
	'TOP flat',
	'QCD flat',
	'ID: e',
	'ID: #mu',
	'Iso: e',
	'Iso: #mu',
	'Trigger: e',
	'Trigger: #mu',
	'Lumi',
	'Pileup',
	'JES',
	'JER',
	#'H tag: smear',
	#'H tag: py8/hw',
	#'B tag: udsg',
	#'B tag: bc',
	'Jet pT weight',
	#'W tag: res',
	#'W tag: scale',
	'W tag: #tau_{2}/#tau_{1}',
	#'W tag: #tau_{2}/#tau_{1} p_{T}-dep.',
	'Top p_{T}',
	#'Top shower',
	'ME Scale',
	'PDF',
	#'QCD rate',
	#'DY+jets rate',
	#'VV rate',
	#'Single t rate',
	#'W+jets rate',
	#'t#bar{t} rate',
	]

nuisVal = []
nuisErr = []
for i in range(len(nuisNam)):
	nuis = nuisNam[i]
	nuisVal.append(parVals[''][nuis][0][0])
	nuisErr.append(parVals[''][nuis][0][1])
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

c = TCanvas('PostFit', 'PostFit', 1000, 1400)
c.SetTopMargin(0.04)
c.SetRightMargin(0.04)
c.SetBottomMargin(0.10)
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

c.SaveAs(limitDir+'postFitNuis_SLBO_noQ2.root')
c.SaveAs(limitDir+'postFitNuis_SLBO_noQ2.pdf')
c.SaveAs(limitDir+'postFitNuis_SLBO_noQ2.png')
c.SaveAs(limitDir+'postFitNuis_SLBO_noQ2.C')


