from ROOT import *
from array import array
from math import *
import os,sys,pickle

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

post = sys.argv[1]

blind=False
saveKey=''
lumiPlot = '35.9'
lumiStr = '36p814'
spin=''#'right'
discriminant='minMlbST'
histPrefix=discriminant+'_'+str(lumiStr)+'fb'+spin
stat='0.3'#0.75
isRebinned='_rebinned'
tempKey='templates4CRhtSR_postfit'
limitDir='/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/limitsOct17/'+tempKey+'/'
cutString=''#SelectionFile'
LH700file='/templates_'+discriminant+'_TTM1000_bW0p5_tZ0p25_tH0p25_36p814fb_BKGNORM_rebinned_stat0p3_'+post+'.p' #

print limitDir+cutString+LH700file

parVals=pickle.load(open(limitDir+cutString+LH700file,'rb'))

nuisNam = []
nuisVal = []
nuisErr = []
for nuis in parVals[''].keys(): #TpTp_M-0800'].keys():
	if nuis=='__cov' or nuis=='__nll' or nuis=='__chi2' or nuis=='__ks': continue
	nuisNam.append(nuis)
	nuisVal.append(parVals[''][nuis][0][0])
	nuisErr.append(parVals[''][nuis][0][1])
	print nuis,"=",parVals[''][nuis][0][0],"+/-",parVals[''][nuis][0][1]


nuisNam = [
	#'ewk_rate',
	#'top_rate',
	#'qcdsys',
	'elIdSys', #'sfel_id',#
	'muIdSys', #'sfmu_id',#
	'elIsoSys', #'sfel_iso',#
	'muIsoSys', #'sfmu_iso',#
	'elRecoSys', #'sfel_gsf',#
	'muRecoSys', #'sfmu_trk',#
	'eeeTrigSys',
	'eemTrigSys',
	'emmTrigSys',
	'mmmTrigSys',
	'eeTrigSysBD',
	'eeTrigSysEH',
	'emTrigSysBD',
	'emTrigSysEH',
	'mmTrigSysBD',
	'mmTrigSysEH',
	'trigeffEl',
	'trigeffMu',
	'elPRsys',
	'muPRsys',
	'elFR',
	'muFR',
	'muFReta',
	'FRsys',	
	'ChargeMisIDUnc',
	'FakeRate',
	'elFakeRate',
	'muFakeRate',
	#'sfel_trig',#
	#'sfmu_trig',#
	'lumiSys', #'luminosity',#
	'pileup',#
	'jec',
	'jer',
	'jsf',
	'htag_prop', #'higgs_prop',
	'mistag',#
	'btag',#
	'tau21',
	'taupt',
	'jmr',
	'jms',
	'toppt',
	'muRFcorrdNewTop',
	'muRFcorrdNewEwk',
	'muRFcorrdNewQCD',#
	'QCDscale',
	'muRFcorrdNewEwk1L',#
	'EWKscale',
	'muRFcorrdNewSingleTop',#
	'SingleTopscale',
	'muRFcorrdNewTTbar',#
	'TTbarscale',
	'pdfNew',#
	#'QCD_rate',
	#'DYJets_rate',
	#'Diboson_rate',
	#'SingleTop_rate',
	#'WJets_rate',
	#'TTbar_rate',
	]

nuisNamPlot = [
	#'EWK flat',
	#'TOP flat',
	#'QCD flat',
	'ID: e',
	'ID: #mu',
	'Iso: e',
	'Iso: #mu',
	'Reco: e',
	'Reco: #mu',
	'Trigger: eee',
	'Trigger: ee#mu',
	'Trigger: e#mu#mu',
	'Trigger: #mu#mu#mu',
	'Trigger: ee (B-D)',
	'Trigger: ee (E-H)',
	'Trigger: e#mu (B-D)',
	'Trigger: e#mu (E-H)',
	'Trigger: #mu#mu (B-D)',
	'Trigger: #mu#mu (E-H)',
	'Trigger: e',
	'Trigger: #mu',
	'Prompt rate 3L: e',
	'Prompt rate 3L: #mu',
	'Fake rate 3L: e',
	'Fake rate 3L: #mu',
	'Fake rate 3L: #mu, #eta',
	'Fake rate 3L: syst.',	
	'Charge mis-ID 2L',
	'Fake rate 2L',
	'Fake rate 2L: e',
	'Fake rate 2L: #mu',
	'Lumi',
	'Pileup',
	'JES',
	'JER',
	'HT scaling',
	'H tag: py8/hw',
	'B tag: udsg',
	'B tag: bc',
	'W tag: #tau_{2}/#tau_{1}',
	'W tag: #tau_{2}/#tau_{1} p_T',
	'W/H tag: smear',
	'W/H tag: scale',
	'Top p_{T}',
	'ME Scale t#bar{t}+X',
	'ME Scale VV(V)',
	'ME Shape QCD',
	'ME Rate QCD',
	'ME Shape W/Z',
	'ME Rate W/Z',
	'ME Shape single t',
	'ME Rate single t',
	'ME Shape t#bar{t}',
	'ME Rate t#bar{t}',
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
delNam = []
delPlot = []
nsuccess=0
print 'initial length',len(nuisNam)
for inui in range(len(nuisNam)):
	nuis = nuisNam[inui]
	try:
		nuisVal.append(parVals[''][nuis][0][0])
		nuisErr.append(parVals[''][nuis][0][1])
		nsuccess+=1
	except:
		delNam.append(nuisNam[inui])
		delPlot.append(nuisNamPlot[inui])		 
		print 'removing',nuisNam[inui]

for nui in delNam: nuisNam.remove(nui)
for nui in delPlot: nuisNamPlot.remove(nui)

nNuis = len(nuisNam)
print 'end length',nNuis

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

c = TCanvas('PostFit', 'PostFit', 1000, 1600)
c.SetTopMargin(0.04)
c.SetRightMargin(0.04)
c.SetBottomMargin(0.10)
c.SetLeftMargin(0.27)
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
ax_2.SetRangeUser(-3.2, 3.2)

ax_1.Set(nNuis+2, 0, nNuis+2)
ax_1.SetNdivisions(-414)
#ax_2.SetNdivisions(-505)
for i in range(nNuis):
	ax_1.SetBinLabel(i+2, nuisNamPlot[i])

g95.GetHistogram().Draw('axis,same')
c.Modified()
c.Update()

type = 'SLBO'
if post=='comb': type = 'CombBO'
if 'comb123' in post: type = 'Comb123BO'
if post=='ssdl': type = '2LBO'
if 'asimov' in tempKey: type = 'SLBO_asimov'

c.SaveAs(limitDir+'postFitNuis_'+type+'_'+post+'.root')
c.SaveAs(limitDir+'postFitNuis_'+type+'_'+post+'.pdf')
c.SaveAs(limitDir+'postFitNuis_'+type+'_'+post+'.png')
c.SaveAs(limitDir+'postFitNuis_'+type+'_'+post+'.C')

