#!/usr/bin/python

import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
from modSyst import *
from utils import *
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)
start_time = time.time()

# This script produces plots combining all 3 years.
# It assumes that the paths for different years only differs by the year tag; R16, R17, and R18.

# python plotFullRun2mcat.py BDT 40vars_6j_NJetsCSV_053121lim_newbin1 R18 1p 4p

years_lumi_float = {
'R18':59.97,
'R16':35.867,
'R17':41.53,
}
years_lumi_str = {
'R18':'59p97',
'R16':'35p867',
'R17':'41p53',
}

year=sys.argv[3]
lumiStr= years_lumi_str[year]
lumi=137.4#years_lumi_float[year]#137.4 #for plots
yearstoadd = {
'R16':'35p867',
'R17':'41p53',
}
	
region='SR' #PS,SR,TTCR,WJCR
isCategorized=1
iPlot=sys.argv[1]
# if len(sys.argv)>1: iPlot=str(sys.argv[1])
cutString=''
if region=='SR': pfix='templates_'+year
elif region=='WJCR': pfix='wjets_'+year
elif region=='TTCR': pfix='ttbar_'+year
if not isCategorized: pfix='kinematics_'+region+'_'+year
templateDir=os.getcwd()+'/'+pfix+'_'+sys.argv[2]+'/'+cutString+'/'

isRebinned='_R18bins_rebinned_stat0p3_bdtcorr'#'_rebinned_stat0p3' #post for ROOT file names
if not isCategorized: isRebinned='_rebinned_stat1p1'
saveKey = '_v4' # tag for plot names

sig='tttt' #  choose the 1st signal to plot
sigleg='t#bar{t}t#bar{t}'
scaleSignalsToXsec = False # !!!!!Make sure you know signal x-sec used in input files to this script. If this is True, it will scale signal histograms by x-sec in weights.py!!!!!
scaleSignals = False
sigScaleFact = 10 #put -1 if auto-scaling wanted
useCombineTemplates = True
sigfile='templates_'+iPlot+'_'+sig+'_'+lumiStr+'fb'+isRebinned+'.root'

ttProcList = ['ttnobb','ttbb'] # ['ttjj','ttcc','ttbb','ttbj']
bkgProcList = ttProcList+['ttH','top','ewk','qcd']
if '53' in sig: bkgHistColors = {'tt2b':rt.kRed+3,'tt1b':rt.kRed-3,'ttbj':rt.kRed+3,'ttbb':rt.kRed,'ttcc':rt.kRed-5,'ttjj':rt.kRed-7,'ttnobb':rt.kRed-7,'top':rt.kBlue,'ewk':rt.kMagenta-2,'qcd':rt.kOrange+5,'ttbar':rt.kRed} #4T
elif 'tttt' in sig: 
	#bkgHistColors = {'tt2b':rt.kRed+3,'tt1b':rt.kRed-3,'ttbj':rt.kRed+3,'ttbb':rt.kRed,'ttcc':rt.kRed-5,'ttjj':rt.kRed-7,'ttnobb':rt.kRed-9,'top':rt.kBlue,'ttH':rt.kRed+3,'ewk':rt.kMagenta-2,'qcd':rt.kOrange+5,'ttbar':rt.kRed} #4T
	bkgHistColors = {'ttbb':rt.TColor.GetColor("#d3eeef"),'ttnobb':rt.TColor.GetColor("#cf9ddb"),'ttH':rt.TColor.GetColor("#163d4e"),'top':rt.TColor.GetColor("#54792f"),'ewk':rt.TColor.GetColor("#d07e93"),'qcd':rt.TColor.GetColor("#c1caf3")} #4T
elif 'HTB' in sig: bkgHistColors = {'ttbar':rt.kGreen-3,'wjets':rt.kPink-4,'top':rt.kAzure+8,'ewk':rt.kMagenta-2,'qcd':rt.kOrange+5} #HTB
else: bkgHistColors = {'top':rt.kAzure+8,'ewk':rt.kMagenta-2,'qcd':rt.kOrange+5} #TT
sigColor= rt.kBlack

systematicList = ['pileup','JEC','JER','isr','fsr','muRF','pdf','bdtshape']#,'njet','hdamp','ue','ht','trigeff','toppt','tau32','jmst','jmrt','tau21','jmsW','jmrW','tau21pt']
if year != 'R18': systematicList += ['prefire']
useSmoothShapes = True
if not isCategorized: useSmoothShapes = False
doAllSys = True
addCRsys = False
doOneBand = True
blind = False
yLog  = True
doRealPull = False
compareShapes = False
if not isCategorized: blind = False
if blind: doRealPull,doOneBand = False,False
if doRealPull: doOneBand = False
if not doAllSys: doOneBand = True # Don't change this!
if compareShapes: blind,yLog,scaleSignals,sigScaleFact=True,False,False,-1
zero = 1E-12

isEMlist  = ['E','M']

if useCombineTemplates:
	sigName = sig
	dataName = 'data_obs'
	upTag = 'Up'
	downTag = 'Down'
	sigfile = sigfile.replace(sig+'_','')
else: #theta
	sigName = 'sig'
	dataName = 'DATA'
	upTag = '__plus'
	downTag = '__minus'
if not os.path.exists(templateDir+sigfile):
	print "ERROR: File does not exits: "+templateDir+sigfile
	os._exit(1)
print "READING: "+templateDir+sigfile
RFile = rt.TFile(templateDir+sigfile)
RFiles = {}
RFiles['R16'] = rt.TFile(templateDir.replace(year,'R16')+sigfile.replace(lumiStr,yearstoadd['R16']))
RFiles['R17'] = rt.TFile(templateDir.replace(year,'R17')+sigfile.replace(lumiStr,yearstoadd['R17']))

datahists = [k.GetName() for k in RFile.GetListOfKeys() if '__'+dataName in k.GetName()]
catsElist = [hist[hist.find('fb_')+3:hist.find('__')] for hist in datahists if 'isE_' in hist]
catsElist = [#manually add the list of categories to be displayed together (SHOULD START WITH isE!!)
# 'isE_nHOT1p_nT0p_nW0p_nB2_nJ10p',
# 'isE_nHOT0_nT0p_nW0p_nB3_nJ10p',
# 'isE_nHOT1p_nT0p_nW0p_nB3_nJ10p',
# 'isE_nHOT0_nT0p_nW0p_nB4p_nJ10p',
# 'isE_nHOT1p_nT0p_nW0p_nB4p_nJ10p',

# 'isE_nHOT1p_nT0p_nW0p_nB2_nJ8p',
# 'isE_nHOT0_nT0p_nW0p_nB3_nJ8p',
# 'isE_nHOT0_nT0p_nW0p_nB4p_nJ7p',
# 'isE_nHOT1p_nT0p_nW0p_nB3_nJ8p',
# 'isE_nHOT1p_nT0p_nW0p_nB4p_nJ7p',

'isE_nHOT1p_nT0p_nW0p_nB2_nJ8p',
'isE_nHOT1p_nT0p_nW0p_nB3_nJ8p',
'isE_nHOT1p_nT0p_nW0p_nB4p_nJ8p',

# 'isE_nHOT'+sys.argv[4]+'_nT0p_nW0p_nB'+sys.argv[5]+'_nJ6',
# 'isE_nHOT'+sys.argv[4]+'_nT0p_nW0p_nB'+sys.argv[5]+'_nJ7',
# 'isE_nHOT'+sys.argv[4]+'_nT0p_nW0p_nB'+sys.argv[5]+'_nJ8',
# 'isE_nHOT'+sys.argv[4]+'_nT0p_nW0p_nB'+sys.argv[5]+'_nJ9',
# 'isE_nHOT'+sys.argv[4]+'_nT0p_nW0p_nB'+sys.argv[5]+'_nJ10p',


# 'isE_nHOT0_nT0p_nW0p_nB3_nJ6',
# 'isE_nHOT0_nT0p_nW0p_nB3_nJ7',
# 'isE_nHOT0_nT0p_nW0p_nB3_nJ8',
# 'isE_nHOT0_nT0p_nW0p_nB3_nJ9',
# 'isE_nHOT0_nT0p_nW0p_nB3_nJ10p',
# 'isE_nHOT0_nT0p_nW0p_nB4p_nJ6',
# 'isE_nHOT0_nT0p_nW0p_nB4p_nJ7',
# 'isE_nHOT0_nT0p_nW0p_nB4p_nJ8',
# 'isE_nHOT0_nT0p_nW0p_nB4p_nJ9',
# 'isE_nHOT0_nT0p_nW0p_nB4p_nJ10p',

]
catBound = {}

lumiSys = 0.025 # lumi uncertainty
if year=='R17': lumiSys = 0.023
trigSys = 0.0 # trigger uncertainty
lepIdSys = 0.03 # lepton id uncertainty
lepIsoSys = 0.0 # lepton isolation uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2)#+njetSys**2) #cheating while total e/m values are close

QCDscale_ttbar = 0.0295 #ttbar +2.4%/-3.5% (symmetrize)
QCDscale_top = 0.026 #top +3.1%/-2.1% (symmetrize)
QCDscale_ewk = 0.006 #ewk +0.8%/-0.4% (symmetrize)
pdf_gg = 0.042 #ttbar +/-4.2%
pdf_qg = 0.028 #top +/-2.8%
pdf_qqbar = 0.038 #ewk +/-3.8%
xsec_ttbar = 0.0515 #ttbar (scale+pdf) +4.8%/-5.5% (symmetrize)
xsec_ttH = 0.20
xsec_top = 0.04 #top (scale+pdf) #inflated unc. aligned with OSDL/SSDL ttH/ttV/tt+XY
xsec_ewk = 0.038 #ewk (scale+pdf)
ttHF = 0.04 # 4% ttbb cross section uncertainty (reduced from 13% from before when theory components included)
hDamp = 0.085 # +10%/-7% (symmetrize)
for catEStr in catsElist:
	modTag = catEStr#[catEStr.find('nT'):catEStr.find('nJ')-3]
	modelingSys['data_'+modTag] = 0.
	if not addCRsys: #else CR uncertainties are defined in modSyst.py module
		for proc in bkgProcList:
			modelingSys[proc+'_'+modTag] = 0.
	modelingSys['ttbb_'+modTag]=math.sqrt(xsec_ttbar**2+ttHF**2+hDamp**2)#math.sqrt(QCDscale_ttbar**2+pdf_gg**2+ttHF**2)
	modelingSys['ttnobb_'+modTag]=math.sqrt(xsec_ttbar**2+hDamp**2)#math.sqrt(QCDscale_ttbar**2+pdf_gg**2)
	modelingSys['ttH_'+modTag]=xsec_ttH#math.sqrt(QCDscale_top**2+pdf_qg**2)
	modelingSys['top_'+modTag]=xsec_top#math.sqrt(QCDscale_top**2+pdf_qg**2)
	modelingSys['ewk_'+modTag]=xsec_ewk#math.sqrt(QCDscale_ewk**2+pdf_qqbar**2)

def getNormUnc(hist,ibin,modelingUnc):
	contentsquared = hist.GetBinContent(ibin)**2
	error = corrdSys*corrdSys*contentsquared  #correlated uncertainties
	error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
	return error

def formatUpperHist(histogram,histogramBkg):
	histogram.GetXaxis().SetLabelSize(0)
	histogram.GetXaxis().SetNdivisions(506)

	if blind == True:
		histogram.GetXaxis().SetLabelSize(0.045)
		histogram.GetXaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetLabelSize(0.045)
		histogram.GetYaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetTitleOffset(0.9)
		histogram.GetXaxis().SetTitleOffset(0.5)
		histogram.GetXaxis().SetNdivisions(506)
	else:
		histogram.GetYaxis().SetLabelSize(0.07)
		histogram.GetYaxis().SetTitleSize(0.08)
		histogram.GetYaxis().SetTitleOffset(.71)

	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.0101)
	if not yLog: 
		histogram.SetMinimum(0.015)
	if yLog:
		uPad.SetLogy()
		if not isCategorized:
			histogram.SetMaximum(5e6*histogramBkg.GetMaximum())
		else: histogram.SetMaximum(2e1*histogramBkg.GetMaximum())
	else: histogram.SetMaximum(1.3*histogramBkg.GetMaximum())
		
def formatLowerHist(histogram,disc):
	histogram.GetXaxis().SetLabelSize(0.12)
	histogram.GetXaxis().SetTitleSize(0.15)
	histogram.GetXaxis().SetTitleOffset(0.55)
	histogram.GetXaxis().SetNdivisions(506)

	histogram.GetXaxis().SetNdivisions(506)

	histogram.GetYaxis().SetLabelSize(0.12)
	histogram.GetYaxis().SetTitleSize(0.14)
	histogram.GetYaxis().SetTitleOffset(.37)
	histogram.GetYaxis().SetTitle('Data/Bkg')
	histogram.GetYaxis().SetNdivisions(506)
	if doRealPull: histogram.GetYaxis().SetRangeUser(min(-2.99,0.8*histogram.GetBinContent(histogram.GetMaximumBin())),max(2.99,1.2*histogram.GetBinContent(histogram.GetMaximumBin())))
	else: histogram.GetYaxis().SetRangeUser(0.01,1.99)#0,2.99)
	histogram.GetYaxis().CenterTitle()

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= str(lumi)+" fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 0#11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H = H_ref

iPeriod = 4 #see CMS_lumi.py module for usage!

# references for T, B, L, R
T = 0.10*H_ref
B = 0.25*H_ref 
L = 0.12*W_ref
R = 0.15*W_ref
if blind == True: B = 0.08*H_ref

tagPosX = 0.76
tagPosY = 0.83

bkghists = {}
bkghistsmerged = {}
systHists = {}
totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}
hDataCats = {}
hbkgCats = {}
hsystCats = {}
hsigCats = {}
nBinsBkg = 0
for catEStr in catsElist:
	histPrefix=iPlot+'_'+lumiStr+'fb_'
	histPrefix+=catEStr
	print histPrefix+'__'+dataName
	nBinsBkg += RFile.Get(histPrefix+'__'+dataName).GetNbinsX()
for em in ['E','M','L']:
	xaxislabel = 'H_{T} bins'
	if iPlot=='BDT': xaxislabel = 'BDT bins'
	hDataCats[em] = rt.TH1F('data_'+em,';'+xaxislabel,nBinsBkg,0,nBinsBkg)
	hDataCats[em].Sumw2()
	for proc in bkgProcList:
		hbkgCats[proc+'_'+em] = rt.TH1F(proc+'_'+em,';'+xaxislabel,nBinsBkg,0,nBinsBkg)
		hbkgCats[proc+'_'+em].Sumw2()
		systematicList_ = systematicList[:]
		if 'nB0p' not in catEStr or iPlot=='HTYLD': #systematicList_ += ['mistag','btagcorr','btaguncorr']#,'btag']
			if iPlot=='BDT': systematicList_ += ['CSVshapelf','CSVshapehf','CSVshapehfstats1','CSVshapehfstats2','CSVshapecferr1','CSVshapecferr2','CSVshapelfstats1','CSVshapelfstats2']
			else: systematicList_ += ['mistag','btagcorr','btaguncorr']#,'btag']
		if 'nHOT0p' not in catEStr or iPlot=='HTYLD': systematicList_ += ['hotstat','hotcspur','hotclosure']
		if useSmoothShapes: systematicList_ = ['lowess'+syst for syst in systematicList_]
		for syst in systematicList_:
			for ud in [upTag,downTag]:
				hsystCats[proc+'_'+em+'_'+syst+'_'+ud] = rt.TH1F(proc+'_'+em+'_'+syst+'_'+ud,';'+xaxislabel,nBinsBkg,0,nBinsBkg)
				hsystCats[proc+'_'+em+'_'+syst+'_'+ud].Sumw2()
	hsigCats[em] = rt.TH1F('sig_'+em,';'+xaxislabel,nBinsBkg,0,nBinsBkg)
	hsigCats[em].Sumw2()
catbin = 0
for catEStr in catsElist:
	systematicList_ = systematicList[:]
	if 'nB0p' not in catEStr or iPlot=='HTYLD': #systematicList_ += ['mistag','btagcorr','btaguncorr']#,'btag']
		if iPlot=='BDT': systematicList_ += ['CSVshapelf','CSVshapehf','CSVshapehfstats1','CSVshapehfstats2','CSVshapecferr1','CSVshapecferr2','CSVshapelfstats1','CSVshapelfstats2']
		else: systematicList_ += ['mistag','btagcorr','btaguncorr']#,'btag']
	if 'nHOT0p' not in catEStr or iPlot=='HTYLD': systematicList_ += ['hotstat','hotcspur','hotclosure']
	if useSmoothShapes: systematicList_ = ['lowess'+syst for syst in systematicList_]
	modTag = catEStr#[catEStr.find('nT'):catEStr.find('nJ')-3]
	for isEM in isEMlist:
		histPrefix=iPlot+'_'+lumiStr+'fb_'
		catStr=catEStr.replace('isE','is'+isEM)
		histPrefix+=catStr
		print histPrefix
		totBkg = 0.
		for proc in bkgProcList: 
			try:
				bkghists[proc+catStr] = RFile.Get(histPrefix+'__'+proc).Clone()
				for year_ in RFiles.keys(): bkghists[proc+catStr].Add(RFiles[year_].Get(histPrefix.replace(lumiStr,yearstoadd[year_])+'__'+proc))
				totBkg += bkghists[proc+catStr].Integral()
				for ibin in range(1,bkghists[proc+catStr].GetNbinsX()+1):
					hbkgCats[proc+'_'+isEM].SetBinContent(ibin+catbin,bkghists[proc+catStr].GetBinContent(ibin))
					hbkgCats[proc+'_'+isEM].SetBinError(ibin+catbin,bkghists[proc+catStr].GetBinError(ibin))
			except:
				print "There is no "+proc+"!!! Skipping it....."
				pass
		hData = RFile.Get(histPrefix+'__'+dataName).Clone()
		for year_ in RFiles.keys(): hData.Add(RFiles[year_].Get(histPrefix.replace(lumiStr,yearstoadd[year_])+'__'+dataName))
		for ibin in range(1,hData.GetNbinsX()+1):
			hDataCats[isEM].SetBinContent(ibin+catbin,hData.GetBinContent(ibin))
			hDataCats[isEM].SetBinError(ibin+catbin,hData.GetBinError(ibin))
		hsig = RFile.Get(histPrefix+'__'+sigName).Clone(histPrefix+'__'+sigName)
		for year_ in RFiles.keys(): hsig.Add(RFiles[year_].Get(histPrefix.replace(lumiStr,yearstoadd[year_])+'__'+sigName))
		if scaleSignalsToXsec: hsig.Scale(xsec[sig])
		for ibin in range(1,hsig.GetNbinsX()+1):
			hsigCats[isEM].SetBinContent(ibin+catbin,hsig.GetBinContent(ibin))
			hsigCats[isEM].SetBinError(ibin+catbin,hsig.GetBinError(ibin))

		if doAllSys:
			print systematicList_
			for syst in systematicList_:
				print syst
				for ud in [upTag,downTag]:
					for proc in bkgProcList:
						try: 
							systHists[proc+catStr+syst+ud] = RFile.Get(histPrefix+'__'+proc+'__'+syst+ud).Clone()
							for year_ in RFiles.keys(): systHists[proc+catStr+syst+ud].Add(RFiles[year_].Get(histPrefix.replace(lumiStr,yearstoadd[year_])+'__'+proc+'__'+syst+ud))
							for ibin in range(1,systHists[proc+catStr+syst+ud].GetNbinsX()+1):
								hsystCats[proc+'_'+isEM+'_'+syst+'_'+ud].SetBinContent(ibin+catbin,systHists[proc+catStr+syst+ud].GetBinContent(ibin))
								hsystCats[proc+'_'+isEM+'_'+syst+'_'+ud].SetBinError(ibin+catbin,systHists[proc+catStr+syst+ud].GetBinError(ibin))
						except: 
							print "There is no "+syst+ud+" for "+proc+"!!! Skipping it....."
							pass

		for proc in bkgProcList:
			try: del bkghists[proc+catStr]
			except: pass			
	
	# Making plots for e+jets/mu+jets combined #
	histPrefixE = iPlot+'_'+lumiStr+'fb_'+catEStr
	histPrefixM = iPlot+'_'+lumiStr+'fb_'+catEStr.replace('isE','isM')
	catLStr = catEStr.replace('isE','isL')
	totBkgMerged = 0.
	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+catLStr] = RFile.Get(histPrefixE+'__'+proc).Clone()
			bkghistsmerged[proc+catLStr].Add(RFile.Get(histPrefixM+'__'+proc))
			for year_ in RFiles.keys(): 
				bkghistsmerged[proc+catLStr].Add(RFiles[year_].Get(histPrefixE.replace(lumiStr,yearstoadd[year_])+'__'+proc))
				bkghistsmerged[proc+catLStr].Add(RFiles[year_].Get(histPrefixM.replace(lumiStr,yearstoadd[year_])+'__'+proc))
			for ibin in range(1,bkghistsmerged[proc+catLStr].GetNbinsX()+1):
				hbkgCats[proc+'_L'].SetBinContent(ibin+catbin,bkghistsmerged[proc+catLStr].GetBinContent(ibin))
				hbkgCats[proc+'_L'].SetBinError(ibin+catbin,bkghistsmerged[proc+catLStr].GetBinError(ibin))
			totBkgMerged += bkghistsmerged[proc+catLStr].Integral()
		except:pass
	hDatamerged = RFile.Get(histPrefixE+'__'+dataName).Clone()
	hDatamerged.Add(RFile.Get(histPrefixM+'__'+dataName).Clone())
	for year_ in RFiles.keys(): 
		hDatamerged.Add(RFiles[year_].Get(histPrefixE.replace(lumiStr,yearstoadd[year_])+'__'+dataName))
		hDatamerged.Add(RFiles[year_].Get(histPrefixM.replace(lumiStr,yearstoadd[year_])+'__'+dataName))
	for ibin in range(1,hDatamerged.GetNbinsX()+1):
		hDataCats['L'].SetBinContent(ibin+catbin,hDatamerged.GetBinContent(ibin))
		hDataCats['L'].SetBinError(ibin+catbin,hDatamerged.GetBinError(ibin))
	catBound[catEStr] = [catbin+1,catbin+hDatamerged.GetNbinsX()]
	hsigmerged = RFile.Get(histPrefixE+'__'+sigName).Clone(histPrefixE+'__'+sigName+'merged')
	hsigmerged.Add(RFile.Get(histPrefixM+'__'+sigName).Clone())
	for year_ in RFiles.keys(): 
		hsigmerged.Add(RFiles[year_].Get(histPrefixE.replace(lumiStr,yearstoadd[year_])+'__'+sigName))
		hsigmerged.Add(RFiles[year_].Get(histPrefixM.replace(lumiStr,yearstoadd[year_])+'__'+sigName))
	if scaleSignalsToXsec: hsigmerged.Scale(xsec[sig])
	for ibin in range(1,hsigmerged.GetNbinsX()+1):
		hsigCats['L'].SetBinContent(ibin+catbin,hsigmerged.GetBinContent(ibin))
		hsigCats['L'].SetBinError(ibin+catbin,hsigmerged.GetBinError(ibin))

	if doAllSys:
		for syst in systematicList_:
			for ud in [upTag,downTag]:
				for proc in bkgProcList:
					try: 
						systHists[proc+catLStr+syst+ud] = systHists[proc+catEStr+syst+ud].Clone()
						systHists[proc+catLStr+syst+ud].Add(systHists[proc+catEStr.replace('isE','isM')+syst+ud])
						for ibin in range(1,systHists[proc+catLStr+syst+ud].GetNbinsX()+1):
							hsystCats[proc+'_L_'+syst+'_'+ud].SetBinContent(ibin+catbin,systHists[proc+catLStr+syst+ud].GetBinContent(ibin))
							hsystCats[proc+'_L_'+syst+'_'+ud].SetBinError(ibin+catbin,systHists[proc+catLStr+syst+ud].GetBinError(ibin))
					except: pass
	
	catbin += hData.GetNbinsX()
	
	for proc in bkgProcList:
		try: del bkghistsmerged[proc+catLStr]
		except: pass

for isEM in ['E','M','L']:
	bkgHT = hbkgCats[bkgProcList[0]+'_'+isEM].Clone()
	for proc in bkgProcList:
		if proc==bkgProcList[0]: continue
		try: bkgHT.Add(hbkgCats[proc+'_'+isEM])
		except: pass

	totBkgTemp1[isEM] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
	totBkgTemp2[isEM] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
	totBkgTemp3[isEM] = rt.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))

	for ibin in range(1,hbkgCats[bkgProcList[0]+'_'+isEM].GetNbinsX()+1):
		errorUp = 0.
		errorDn = 0.
		errorStatOnly = bkgHT.GetBinError(ibin)**2
		errorNorm = 0.
		for proc in bkgProcList:
			try: errorNorm += getNormUnc(hbkgCats[proc+'_'+isEM],ibin,modelingSys[proc+'_'+modTag])
			except: pass

		if doAllSys:
			for syst in systematicList_:
				if 'BJetsNoSF' in iPlot and (syst=='btag' or syst=='mistag'): continue
				for proc in bkgProcList:
					try:
						errorPlus = hsystCats[proc+'_'+isEM+'_'+syst+'_'+upTag].GetBinContent(ibin)-hbkgCats[proc+'_'+isEM].GetBinContent(ibin)
						errorMinus = hbkgCats[proc+'_'+isEM].GetBinContent(ibin)-hsystCats[proc+'_'+isEM+'_'+syst+'_'+downTag].GetBinContent(ibin)
						if errorPlus > 0: errorUp += errorPlus**2
						else: errorDn += errorPlus**2
						if errorMinus > 0: errorDn += errorMinus**2
						else: errorUp += errorMinus**2
					except: pass

		totBkgTemp1[isEM].SetPointEYhigh(ibin-1,math.sqrt(errorStatOnly))
		totBkgTemp1[isEM].SetPointEYlow(ibin-1, math.sqrt(errorStatOnly))
		totBkgTemp2[isEM].SetPointEYhigh(ibin-1,math.sqrt(errorStatOnly+errorNorm))
		totBkgTemp2[isEM].SetPointEYlow(ibin-1, math.sqrt(errorStatOnly+errorNorm))
		totBkgTemp3[isEM].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
		totBkgTemp3[isEM].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))

	bkgHTgerr = totBkgTemp3[isEM].Clone()

	if scaleSignals:
		scaleFact = int(bkgHT.GetMaximum()/(hsigCats[isEM].GetMaximum()+zero)) - int(bkgHT.GetMaximum()/(hsigCats[isEM].GetMaximum()+zero)) % 10
		if scaleFact==0: scaleFact=int(bkgHT.GetMaximum()/(hsigCats[isEM].GetMaximum()+zero))
		if scaleFact==0: scaleFact=1
		if sigScaleFact>0: scaleFact=sigScaleFact
	else: scaleFact=1
	hsigCats[isEM].Scale(scaleFact)

			############################################################
	############## Making Plots of e+jets, mu+jets and e/mu+jets 
			############################################################

	drawQCD = False
	try: drawQCD = hbkgCats['qcd'+'_'+isEM].Integral()/bkgHT.Integral()>.005 #don't plot QCD if it is less than 0.5%
	except: pass

	stackbkgHT = rt.THStack("stackbkgHT","")
	bkgProcListNew = bkgProcList[:]
	for proc in bkgProcListNew:
		try: 
			if drawQCD or proc!='qcd': stackbkgHT.Add(hbkgCats[proc+'_'+isEM])
		except: pass
	
	for proc in bkgProcList:
		try: 
			hbkgCats[proc+'_'+isEM].SetLineColor(bkgHistColors[proc])
			hbkgCats[proc+'_'+isEM].SetFillColor(bkgHistColors[proc])
			hbkgCats[proc+'_'+isEM].SetLineWidth(2)
		except: pass

	hsigCats[isEM].SetLineColor(sigColor)
	hsigCats[isEM].SetLineStyle(7)#5)
	hsigCats[isEM].SetFillStyle(0)
	hsigCats[isEM].SetLineWidth(3)
	hsigCats[isEM].GetXaxis().SetTickLength(0) # remove x-axis ticks/labels
	hsigCats[isEM].GetXaxis().SetLabelOffset(999) # remove x-axis ticks/labels

	hDataCats[isEM].SetMarkerStyle(20)
	hDataCats[isEM].SetMarkerSize(1.2)
	hDataCats[isEM].SetMarkerColor(rt.kBlack)
	hDataCats[isEM].SetLineWidth(2)
	hDataCats[isEM].SetLineColor(rt.kBlack)
	hDataCats[isEM].GetXaxis().SetTickLength(0) # remove x-axis ticks/labels
	hDataCats[isEM].GetXaxis().SetLabelOffset(999) # remove x-axis ticks/labels

	bkgHTgerr.SetFillStyle(3004)
	bkgHTgerr.SetFillColor(rt.kBlack)
	bkgHTgerr.SetLineColor(rt.kBlack)

	c1 = rt.TCanvas("c1","c1",50,50,W,H)
	c1.SetFillColor(0)
	c1.SetBorderMode(0)
	c1.SetFrameFillStyle(0)
	c1.SetFrameBorderMode(0)
	#c1.SetTickx(0)
	#c1.SetTicky(0)

	yDiv=0.35
	if blind == True: yDiv=0.0
	uPad=rt.TPad("uPad","",0,yDiv,1,1) #for actual plots

	uPad.SetLeftMargin( L/W )
	uPad.SetRightMargin( R/W )
	uPad.SetTopMargin( T/H )
	uPad.SetBottomMargin( 0.01 )
	if blind == True: uPad.SetBottomMargin( B/H )

	uPad.SetFillColor(0)
	uPad.SetBorderMode(0)
	uPad.SetFrameFillStyle(0)
	uPad.SetFrameBorderMode(0)
	#uPad.SetTickx(0)
	#uPad.SetTicky(0)
	uPad.Draw()
	if blind == False:
		lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner

		lPad.SetLeftMargin( L/W )
		lPad.SetRightMargin( R/W )
		lPad.SetTopMargin( 0.01 )
		lPad.SetBottomMargin( B/H )

		lPad.SetGridy()
		lPad.SetFillColor(0)
		lPad.SetBorderMode(0)
		lPad.SetFrameFillStyle(0)
		lPad.SetFrameBorderMode(0)
		#lPad.SetTickx(0)
		#lPad.SetTicky(0)
		lPad.Draw()
	hDataCats[isEM].SetMaximum(1.8*max(hDataCats[isEM].GetMaximum(),bkgHT.GetMaximum()))
	#hDataCats[isEM].SetMinimum(0.015)
	hDataCats[isEM].SetTitle("")
	hDataCats[isEM].GetYaxis().SetTitle("Events / bin")
	formatUpperHist(hDataCats[isEM],hDataCats[isEM])
	uPad.cd()
	hDataCats[isEM].SetTitle("")
	if compareShapes: hsigCats[isEM].Scale(totBkg/hsigCats[isEM].Integral())
	if not blind: 
		if 'rebinned_stat0p' in isRebinned: hDataCats[isEM].Draw("esamex1")
		else: hDataCats[isEM].Draw("esamex0")
	if blind: 
		#hsigCats[isEM].SetMinimum(0.015)
		hsigCats[isEM].GetYaxis().SetTitle("Events / bin")
		formatUpperHist(hsigCats[isEM],bkgHT)
		hsigCats[isEM].Draw("HIST")
	stackbkgHT.Draw("SAME HIST")
	hsigCats[isEM].Draw("SAME HIST")
	if not blind: 
		if 'rebinned_stat0p' in isRebinned: hDataCats[isEM].Draw("esamex1")
		else: hDataCats[isEM].Draw("esamex0") #redraw data so its not hidden
	uPad.RedrawAxis()
	bkgHTgerr.Draw("SAME E2")
	ulines = {}
	for cat in catBound.keys():
		ulines[cat] = rt.TLine(catBound[cat][1],0,catBound[cat][1],hDataCats[isEM].GetMaximum())
		ulines[cat].Draw()
	
	l_ = uPad.GetLeftMargin()
	r_ = uPad.GetRightMargin()
	
	chLatex = rt.TLatex()
	chLatex.SetNDC()
	chLatex.SetTextSize(0.06)
	if blind: chLatex.SetTextSize(0.04)
	chLatex.SetTextAlign(21) # align center
	tagPosXisEM = 0
	for catStr in catBound.keys():
		tagPosX = l_+(catBound[catStr][0]+(catBound[catStr][1]-catBound[catStr][0])/2.)*(1.-l_-r_)/nBinsBkg
		if tagPosXisEM<tagPosX: tagPosXisEM=tagPosX
		nJString = ''
		nBString = ''
		nHOTString = ''
		nJ = catStr.split('_')[-1].replace('nJ','')
		nB = catStr.split('_')[-2].replace('nB','')
		nHOT = catStr.split('_')[-5].replace('nHOT','')
		if nHOT!='0p': 
			if 'p' in nHOT: nHOTString+='#geq'+nHOT[:-1]+'t'
			else: nHOTString+=nHOT+'t'
		if nB!='0p': 
			if 'p' in nB: nBString+='#geq'+nB[:-1]+'b'
			else: nBString+=nB+'b'
		if nJ!='0p': 
			if 'p' in nJ: nJString+='#geq'+nJ[:-1]+'j'
			else: nJString+=nJ+'j'
		#if tagString.endswith(', '): tagString = tagString[:-2]
		chLatex.DrawLatex(tagPosX, tagPosY, nHOTString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.06, nBString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.12, nJString)
	if isEM=='E': flvString='e+jets'
	elif isEM=='M': flvString='#mu+jets'
	elif isEM=='L': flvString='e/#mu+jets'
	chLatex.DrawLatex(tagPosXisEM, tagPosY-0.21, flvString)

	leg = rt.TLegend(0.85,0.17,0.99,0.87)
	if blind: leg = rt.TLegend(0.85,0.34,0.99,0.87)
	leg.SetShadowColor(0)
	leg.SetFillColor(0)
	leg.SetFillStyle(0)
	leg.SetLineColor(0)
	leg.SetLineStyle(0)
	leg.SetBorderSize(0) 
	leg.SetNColumns(1)
	leg.SetTextFont(62)#42)
	scaleFactStr = ' x'+str(scaleFact)
	if not scaleSignals: scaleFactStr = ''
	if not blind: leg.AddEntry(hDataCats[isEM],"Data","ep")
	if drawQCD: leg.AddEntry(hbkgCats['qcd'+'_'+isEM],"QCD","f")
	try: leg.AddEntry(hbkgCats['ewk'+'_'+isEM],"EWK","f")
	except: pass
	try: leg.AddEntry(hbkgCats['top'+'_'+isEM],"TOP","f")
	except: pass
	try: leg.AddEntry(hbkgCats['ttH'+'_'+isEM],"t#bar{t}+H","f")
	except: pass
	try: leg.AddEntry(hbkgCats['ttnobb'+'_'+isEM],"t#bar{t}+!b#bar{b}","f")
	except: pass
	try: leg.AddEntry(hbkgCats['ttjj'+'_'+isEM],"t#bar{t}+j(j)","f")
	except: pass
	try: leg.AddEntry(hbkgCats['ttcc'+'_'+isEM],"t#bar{t}+c(c)","f")
	except: pass
	if 'tt2b' not in bkgProcList and 'ttnobb' not in bkgProcList:
		try: leg.AddEntry(hbkgCats['ttbb'+'_'+isEM],"t#bar{t}+b(b)","f")
		except: pass
	else:
		try: leg.AddEntry(hbkgCats['ttbb'+'_'+isEM],"t#bar{t}+b#bar{b}","f")
		except: pass
	try: leg.AddEntry(hbkgCats['tt1b'+'_'+isEM],"t#bar{t}+b","f")
	except: pass
	try: leg.AddEntry(hbkgCats['tt2b'+'_'+isEM],"t#bar{t}+2B","f")
	except: pass
	leg.AddEntry(hsigCats[isEM],sigleg+scaleFactStr,"l")
	leg.AddEntry(bkgHTgerr,"Bkg unc","f")
	leg.Draw("same")

	#draw the lumi text on the canvas
	CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)

	uPad.Update()
	uPad.RedrawAxis()
	frame = uPad.GetFrame()
	uPad.Draw()

	if blind == False and not doRealPull:
		lPad.cd()
		pull=hDataCats[isEM].Clone("pull")
		pull.Divide(hDataCats[isEM], bkgHT)
		for binNo in range(1,hDataCats[isEM].GetNbinsX()+1):
			if bkgHT.GetBinContent(binNo)!=0:
				pull.SetBinError(binNo,hDataCats[isEM].GetBinError(binNo)/bkgHT.GetBinContent(binNo))
		pull.SetMaximum(3)
		pull.SetMinimum(0)
		pull.SetFillColor(1)
		pull.SetLineColor(1)
		formatLowerHist(pull,iPlot)
		pull.Draw("E0")#"E1")
	
		BkgOverBkg = pull.Clone("bkgOverbkg")
		BkgOverBkg.Divide(bkgHT, bkgHT)
		pullUncBandTot=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
		for binNo in range(0,hDataCats[isEM].GetNbinsX()+2):
			if bkgHT.GetBinContent(binNo)!=0:
				pullUncBandTot.SetPointEYhigh(binNo-1,totBkgTemp3[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
				pullUncBandTot.SetPointEYlow(binNo-1,totBkgTemp3[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
		pullUncBandTot.SetFillStyle(3013)
		pullUncBandTot.SetFillColor(1)
		pullUncBandTot.SetLineColor(1)
		pullUncBandTot.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		pullUncBandTot.Draw("SAME E2")
	
		pullUncBandNorm=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncNorm"))
		for binNo in range(0,hDataCats[isEM].GetNbinsX()+2):
			if bkgHT.GetBinContent(binNo)!=0:
				pullUncBandNorm.SetPointEYhigh(binNo-1,totBkgTemp2[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
				pullUncBandNorm.SetPointEYlow(binNo-1,totBkgTemp2[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
		pullUncBandNorm.SetFillStyle(3001)
		pullUncBandNorm.SetFillColor(2)
		pullUncBandNorm.SetLineColor(2)
		pullUncBandNorm.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandNorm.Draw("SAME E2")
	
		pullUncBandStat=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncStat"))
		for binNo in range(0,hDataCats[isEM].GetNbinsX()+2):
			if bkgHT.GetBinContent(binNo)!=0:
				pullUncBandStat.SetPointEYhigh(binNo-1,totBkgTemp1[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
				pullUncBandStat.SetPointEYlow(binNo-1,totBkgTemp1[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
		pullUncBandStat.SetFillStyle(3001)
		pullUncBandStat.SetFillColor(3)
		pullUncBandStat.SetLineColor(3)
		pullUncBandStat.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandStat.Draw("SAME E2")

		pullLegend=rt.TLegend(0.14,0.87,0.85,0.96)
		rt.SetOwnership( pullLegend, 0 )   # 0 = release (not keep), 1 = keep
		pullLegend.SetShadowColor(0)
		pullLegend.SetNColumns(3)
		pullLegend.SetFillColor(0)
		pullLegend.SetFillStyle(0)
		pullLegend.SetLineColor(0)
		pullLegend.SetLineStyle(0)
		pullLegend.SetBorderSize(0)
		pullLegend.SetTextFont(42)
		if not doOneBand: 
			pullLegend.AddEntry(pullUncBandStat , "Bkg uncert (stat)" , "f")
			pullLegend.AddEntry(pullUncBandNorm , "Bkg uncert (stat #oplus norm syst)" , "f")
			pullLegend.AddEntry(pullUncBandTot , "Bkg uncert (stat #oplus all syst)" , "f")
		else: 
			if doAllSys: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert (stat #oplus syst)" , "f")
			else: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert (stat)" , "f")
		#pullLegend.AddEntry(pullQ2up , "Q^{2} Up" , "l")
		#pullLegend.AddEntry(pullQ2dn , "Q^{2} Down" , "l")
		pullLegend.Draw("SAME")
		pull.Draw("SAME")
		lPad.RedrawAxis()
		llines = {}
		for cat in catBound.keys():
			llines[cat] = rt.TLine(catBound[cat][1],pull.GetMinimum(),catBound[cat][1],pull.GetMaximum())
			llines[cat].Draw()

	if blind == False and doRealPull:
		lPad.cd()
		pull=hDataCats[isEM].Clone("pull")
		for binNo in range(1,hDataCats[isEM].GetNbinsX()+1):
			if hDataCats[isEM].GetBinContent(binNo)!=0:
				MCerror = 0.5*(totBkgTemp3[isEM].GetErrorYhigh(binNo-1)+totBkgTemp3[isEM].GetErrorYlow(binNo-1))
				pull.SetBinContent(binNo,(hDataCats[isEM].GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(MCerror**2+hDataCats[isEM].GetBinError(binNo)**2))
			else: pull.SetBinContent(binNo,0.)
		pull.SetMaximum(3)
		pull.SetMinimum(-3)
		if '53' in sig or 'tttt' in sig:
			pull.SetFillColor(2)
			pull.SetLineColor(2)
		else:
			pull.SetFillColor(rt.kGray+2)
			pull.SetLineColor(rt.kGray+2)
		formatLowerHist(pull,iPlot)
		pull.GetYaxis().SetTitle('#frac{(obs-bkg)}{uncertainty}')
		pull.Draw("HIST")
		llines = {}
		for cat in catBound.keys():
			llines[cat] = rt.TLine(catBound[cat][1],pull.GetMinimum(),catBound[cat][1],pull.GetMaximum())
			llines[cat].Draw()

	#c1.Write()
	savePrefix = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
	if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
	savePrefix+=histPrefix.replace(lumiStr,str(lumi).replace('.','p')).split('_nHOT')[0]+isRebinned+saveKey
	savePrefix=savePrefix.replace('isM','is'+isEM).replace('_rebinned_stat1p1','')
	if doRealPull: savePrefix+='_pull'
	if yLog: savePrefix+='_logy'
	if blind: savePrefix+='_blind'
	if compareShapes: savePrefix+='_shp'
	if doOneBand: savePrefix+='_totBand'

	if 'isL' in savePrefix:
		# c1.SaveAs(savePrefix+'_'+sys.argv[4]+'_'+sys.argv[5]+'.png')
		c1.SaveAs(savePrefix+'.pdf')
	# c1.SaveAs(savePrefix+'.eps')
	# c1.SaveAs(savePrefix+'.root')
	# c1.SaveAs(savePrefix+'.C')
			
RFile.Close()
for year_ in RFiles.keys(): RFiles[year_].Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


