#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools
from numpy import linspace
from weights import *
from samples import *
import ROOT as R

R.gROOT.SetBatch(1)
start_time = time.time()

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

isTTbarCR = False # else it is Wjets

if isTTbarCR: 
	from analyzeTTJetsCR import *
else:
	from analyzeWJetsCR import *
		       
bkgStackList = ['WJets','ZJets','VV','TTW','TTZ','TTJets','T','QCD']
wjetList  = ['WJetsMG100','WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500']
zjetList  = ['DY50']
vvList    = ['WW','WZ','ZZ']
ttwList   = ['TTWl','TTWq']
ttzList   = ['TTZl','TTZq']
#ttjetList = ['TTJetsPH']
ttjetList = ['TTJetsPH0to700inc','TTJetsPH700to1000inc','TTJetsPH1000toINFinc','TTJetsPH700mtt','TTJetsPH1000mtt']
tList     = ['Tt','Ts','TtW','TbtW']

dataList = ['DataERRC','DataERRD','DataEPRD','DataMRRC','DataMRRD','DataMPRD']

whichSignal = 'X53X53' #TT, BB, or X53X53
signalMassRange = [700,1600]
sigList = [whichSignal+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100)]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in range(signalMassRange[0],signalMassRange[1]+100,100) for chiral in ['left','right']]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
if whichSignal=='X53X53': decays = [''] #decays to tWtW 100% of the time

#topList = ['TTJetsPH','TTWl','TTZl','TTWq','TTZq','Tt','Ts','TtW','TbtW']
topList = ['TTJetsPH0to700inc','TTJetsPH700to1000inc','TTJetsPH1000toINFinc','TTJetsPH700mtt','TTJetsPH1000mtt','TTWl','TTZl','TTWq','TTZq','Tt','Ts','TtW','TbtW']
ewkList = ['DY50','WJetsMG100','WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500','WW','WZ','ZZ']
qcdList = ['QCDht100','QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000']

scaleSignalXsecTo1pb = False # this has to be "True" if you are making templates for limit calculation!!!!!!!!
scaleLumi = False
lumiScaleCoeff = 2318./2263.
doAllSys = True
systematicList = ['pileup','jec','jer','jmr','jms','btag','tau21','pdf','pdfNew','muR','muF','muRFcorrd','toppt','jsf','muRFenv','muRFcorrdNew','muRFdecorrdNew']
normalizeRENORM_PDF = True #normalize the renormalization/pdf uncertainties to nominal templates
doQ2sys = True
q2UpList   = ['TTWl','TTZl','TTWq','TTZq','TTJetsPHQ2U','Tt','TtW','TtWQ2U','TbtWQ2U']
q2DownList = ['TTWl','TTZl','TTWq','TTZq','TTJetsPHQ2D','Tt','TtW','TtWQ2D','TbtWQ2D']

cutString  = ''#'lep40_MET75_1jet300_2jet150_NJets3_NBJets0_3jet100_4jet0_5jet0_DR1_1Wjet0_1bjet0_HT0_ST0_minMlb0'
if isTTbarCR: pfix='ttbar_x53x53_2016_3_8_18_20_49'
else: pfix='wjets_x53x53_2016_3_8_18_15_58'
iPlot='minMlb'

outDir = os.getcwd()+'/'
outDir+=pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
if not os.path.exists(outDir+'/'+cutString): os.system('mkdir '+outDir+'/'+cutString)
outDir+='/'+cutString

isEMlist =['E','M']
if isTTbarCR: 
	nttaglist = ['0','1p'] #if '0p', the cut will not be applied
	nWtaglist = ['0','1p']
	nbtaglist = ['0','1','2p']
else: 
	nttaglist = ['0p'] #if '0p', the cut will not be applied
	nWtaglist = ['0','1p']
	nbtaglist = ['0']
catList = list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist))
tagList = list(itertools.product(nttaglist,nWtaglist,nbtaglist))

def negBinCorrection(hist): #set negative bin contents to zero and adjust the normalization
	norm0=hist.Integral()
	for iBin in range(0,hist.GetNbinsX()+2):
		if hist.GetBinContent(iBin)<0: hist.SetBinContent(iBin,0)
	if hist.Integral()!=0 and norm0>0: hist.Scale(norm0/hist.Integral())

def overflow(hist):
	nBinsX=hist.GetXaxis().GetNbins()
	content=hist.GetBinContent(nBinsX)+hist.GetBinContent(nBinsX+1)
	error=math.sqrt(hist.GetBinError(nBinsX)**2+hist.GetBinError(nBinsX+1)**2)
	hist.SetBinContent(nBinsX,content)
	hist.SetBinError(nBinsX,error)
	hist.SetBinContent(nBinsX+1,0)
	hist.SetBinError(nBinsX+1,0)

lumiSys = 0.027 #2.7% lumi uncertainty
trigSys = 0.05 #5% trigger uncertainty
lepIdSys = 0.01 #1% lepton id uncertainty
lepIsoSys = 0.01 #1% lepton isolation uncertainty
topXsecSys = 0.#0.055 #5.5% top x-sec uncertainty --> covered by PDF and muRF uncertainties
ewkXsecSys = 0.#0.05 #5% ewk x-sec uncertainty --> covered by PDF and muRF uncertainties
qcdXsecSys = 0.#0.50 #50% qcd x-sec uncertainty --> covered by PDF and muRF uncertainties
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2)

addSys = {} #additional uncertainties for specific processes
for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]
	addSys['top_'+tagStr]   = topXsecSys
	addSys['TTJets_'+tagStr]= topXsecSys
	addSys['T_'+tagStr]     = topXsecSys
	addSys['TTW_'+tagStr]   = topXsecSys
	addSys['TTZ_'+tagStr]   = topXsecSys
	addSys['ewk_'+tagStr]   = ewkXsecSys
	addSys['WJets_'+tagStr] = ewkXsecSys
	addSys['ZJets_'+tagStr] = ewkXsecSys
	addSys['VV_'+tagStr]    = ewkXsecSys
	addSys['qcd_'+tagStr]   = qcdXsecSys
	addSys['QCD_'+tagStr]   = qcdXsecSys

def round_sig(x,sig=2):
	try:
		return round(x, sig-int(math.floor(math.log10(abs(x))))-1)
	except:
		return round(x,5)

###########################################################
#################### CATEGORIZATION #######################
###########################################################
def makeThetaCats(datahists,sighists,bkghists,discriminant):

	## This function categorizes the events into electron/muon --> 0/1p W-tag! --> 1/2p b-tag (the same as Cat1, but there is no 4p/3p jets requirement here)
	## Input  histograms (datahists,sighists,bkghists) must have corresponding histograms returned from analyze.py##

	## INITIALIZE DICTIONARIES FOR YIELDS AND THEIR UNCERTAINTIES ##
	yieldTable = {}
	yieldStatErrTable = {} #what is actually stored in this is the square of the uncertainty
	for cat in catList:
		tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		catStr = 'is'+cat[0]+'_'+tagStr
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		yieldTable[histoPrefix]={}
		yieldStatErrTable[histoPrefix]={}
		if doAllSys:
			for systematic in systematicList:
				for ud in ['Up','Down']:
					yieldTable[histoPrefix+systematic+ud]={}
				
		if doQ2sys:
			yieldTable[histoPrefix+'q2Up']={}
			yieldTable[histoPrefix+'q2Down']={}

	## WRITING HISTOGRAMS IN ROOT FILE ##
	i=0
	for signal in sigList:
		outputRfile = R.TFile(outDir+'/templates_'+discriminant+'_'+signal+'_'+lumiStr+'fb.root','RECREATE')
		hsig,htop,hewk,hqcd,hdata={},{},{},{},{}
		hwjets,hzjets,httjets,ht,httw,httz,hvv={},{},{},{},{},{},{}
		for cat in catList:
			tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr = 'is'+cat[0]+'_'+tagStr
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr

			#Group processes
			hwjets[catStr] = bkghists[histoPrefix+'_'+wjetList[0]].Clone(histoPrefix+'_WJets')
			hzjets[catStr] = bkghists[histoPrefix+'_'+zjetList[0]].Clone(histoPrefix+'_ZJets')
			httjets[catStr] = bkghists[histoPrefix+'_'+ttjetList[0]].Clone(histoPrefix+'_TTJets')
			ht[catStr] = bkghists[histoPrefix+'_'+tList[0]].Clone(histoPrefix+'_T')
			httw[catStr] = bkghists[histoPrefix+'_'+ttwList[0]].Clone(histoPrefix+'_TTW')
			httz[catStr] = bkghists[histoPrefix+'_'+ttzList[0]].Clone(histoPrefix+'_TTZ')
			hvv[catStr] = bkghists[histoPrefix+'_'+vvList[0]].Clone(histoPrefix+'_VV')
			for bkg in ttjetList:
				if bkg!=ttjetList[0]: httjets[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in wjetList:
				if bkg!=wjetList[0]: hwjets[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in ttwList:
				if bkg!=ttwList[0]: httw[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in ttzList:
				if bkg!=ttzList[0]: httz[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in tList:
				if bkg!=tList[0]: ht[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in zjetList:
				if bkg!=zjetList[0]: hzjets[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in vvList:
				if bkg!=vvList[0]: hvv[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			
			#Group QCD processes
			hqcd[catStr] = bkghists[histoPrefix+'_'+qcdList[0]].Clone(histoPrefix+'__qcd')
			for bkg in qcdList: 
				if bkg!=qcdList[0]: hqcd[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			
			#Group EWK processes
			hewk[catStr] = bkghists[histoPrefix+'_'+ewkList[0]].Clone(histoPrefix+'__ewk')
			for bkg in ewkList:
				if bkg!=ewkList[0]: hewk[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			
			#Group TOP processes
			htop[catStr] = bkghists[histoPrefix+'_'+topList[0]].Clone(histoPrefix+'__top')
			for bkg in topList:
				if bkg!=topList[0]: htop[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			
			#get signal
			hsig[catStr] = sighists[histoPrefix+'_'+signal+decays[0]].Clone(histoPrefix+'__sig')
			for decay in decays:
				if decay!=decays[0]: hsig[catStr].Add(sighists[histoPrefix+'_'+signal+decay])

			#systematics
			if doAllSys:
				for systematic in systematicList:
					if systematic=='pdfNew' or systematic=='muRFcorrdNew' or systematic=='muRFdecorrdNew': continue
					for ud in ['Up','Down']:
						if systematic!='toppt':
							hqcd[systematic+ud+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
							hewk[systematic+ud+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
							htop[systematic+ud+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+topList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
							hsig[systematic+ud+catStr] = sighists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
							for bkg in qcdList: 
								if bkg!=qcdList[0]: hqcd[systematic+ud+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
							for bkg in ewkList: 
								if bkg!=ewkList[0]: hewk[systematic+ud+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
							for bkg in topList: 
								if bkg!=topList[0]: htop[systematic+ud+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
							for decay in decays:
								if decay!=decays[0]: hsig[systematic+ud+catStr].Add(sighists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+signal+decay])
						if systematic=='toppt': # top pt is only on the ttbar sample, so it needs special treatment!
							htop[systematic+ud+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ttjetList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
							for bkg in ttjetList: 
								if bkg!=ttjetList[0]: htop[systematic+ud+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
							for bkg in topList: 
								if bkg not in ttjetList: htop[systematic+ud+catStr].Add(bkghists[histoPrefix+'_'+bkg])

				htop['muRFcorrdNewUp'+catStr] = htop['muRFcorrdUp'+catStr].Clone(histoPrefix+'__top__muRFcorrdNew__plus')
				htop['muRFcorrdNewDown'+catStr] = htop['muRFcorrdUp'+catStr].Clone(histoPrefix+'__top__muRFcorrdNew__minus')
				hewk['muRFcorrdNewUp'+catStr] = hewk['muRFcorrdUp'+catStr].Clone(histoPrefix+'__ewk__muRFcorrdNew__plus')
				hewk['muRFcorrdNewDown'+catStr] = hewk['muRFcorrdUp'+catStr].Clone(histoPrefix+'__ewk__muRFcorrdNew__minus')
				hqcd['muRFcorrdNewUp'+catStr] = hqcd['muRFcorrdUp'+catStr].Clone(histoPrefix+'__qcd__muRFcorrdNew__plus')
				hqcd['muRFcorrdNewDown'+catStr] = hqcd['muRFcorrdUp'+catStr].Clone(histoPrefix+'__qcd__muRFcorrdNew__minus')
				hsig['muRFcorrdNewUp'+catStr] = hsig['muRFcorrdUp'+catStr].Clone(histoPrefix+'__sig__muRFcorrdNew__plus')
				hsig['muRFcorrdNewDown'+catStr] = hsig['muRFcorrdUp'+catStr].Clone(histoPrefix+'__sig__muRFcorrdNew__minus')

				htop['muRFdecorrdNewUp'+catStr] = htop['muRFcorrdUp'+catStr].Clone(histoPrefix+'__top__muRFdecorrdNew__plus')
				htop['muRFdecorrdNewDown'+catStr] = htop['muRFcorrdUp'+catStr].Clone(histoPrefix+'__top__muRFdecorrdNew__minus')
				hewk['muRFdecorrdNewUp'+catStr] = hewk['muRFcorrdUp'+catStr].Clone(histoPrefix+'__ewk__muRFdecorrdNew__plus')
				hewk['muRFdecorrdNewDown'+catStr] = hewk['muRFcorrdUp'+catStr].Clone(histoPrefix+'__ewk__muRFdecorrdNew__minus')
				hqcd['muRFdecorrdNewUp'+catStr] = hqcd['muRFcorrdUp'+catStr].Clone(histoPrefix+'__qcd__muRFdecorrdNew__plus')
				hqcd['muRFdecorrdNewDown'+catStr] = hqcd['muRFcorrdUp'+catStr].Clone(histoPrefix+'__qcd__muRFdecorrdNew__minus')
				hsig['muRFdecorrdNewUp'+catStr] = hsig['muRFcorrdUp'+catStr].Clone(histoPrefix+'__sig__muRFdecorrdNew__plus')
				hsig['muRFdecorrdNewDown'+catStr] = hsig['muRFcorrdUp'+catStr].Clone(histoPrefix+'__sig__muRFdecorrdNew__minus')

				# nominal,renormWeights[4],renormWeights[2],renormWeights[1],renormWeights[0],renormWeights[5],renormWeights[3]
				histPrefixList = ['','muRUp','muRDown','muFUp','muFDown','muRFcorrdUp','muRFcorrdDown']
				for ibin in range(1,htop[catStr].GetNbinsX()+1):
					weightListTop = [htop[item+catStr].GetBinContent(ibin) for item in histPrefixList]	
					weightListEwk = [hewk[item+catStr].GetBinContent(ibin) for item in histPrefixList]	
					weightListQcd = [hqcd[item+catStr].GetBinContent(ibin) for item in histPrefixList]	
					weightListSig = [hsig[item+catStr].GetBinContent(ibin) for item in histPrefixList]
					indTopRFcorrdUp = weightListTop.index(max(weightListTop))
					indTopRFcorrdDn = weightListTop.index(min(weightListTop))
					indEwkRFcorrdUp = weightListEwk.index(max(weightListEwk))
					indEwkRFcorrdDn = weightListEwk.index(min(weightListEwk))
					indQcdRFcorrdUp = weightListQcd.index(max(weightListQcd))
					indQcdRFcorrdDn = weightListQcd.index(min(weightListQcd))
					indSigRFcorrdUp = weightListSig.index(max(weightListSig))
					indSigRFcorrdDn = weightListSig.index(min(weightListSig))

					indTopRFdecorrdUp = weightListTop.index(max(weightListTop[:-2]))
					indTopRFdecorrdDn = weightListTop.index(min(weightListTop[:-2]))
					indEwkRFdecorrdUp = weightListEwk.index(max(weightListEwk[:-2]))
					indEwkRFdecorrdDn = weightListEwk.index(min(weightListEwk[:-2]))
					indQcdRFdecorrdUp = weightListQcd.index(max(weightListQcd[:-2]))
					indQcdRFdecorrdDn = weightListQcd.index(min(weightListQcd[:-2]))
					indSigRFdecorrdUp = weightListSig.index(max(weightListSig[:-2]))
					indSigRFdecorrdDn = weightListSig.index(min(weightListSig[:-2]))
					
					htop['muRFcorrdNewUp'+catStr].SetBinContent(ibin,htop[histPrefixList[indTopRFcorrdUp]+catStr].GetBinContent(ibin))
					htop['muRFcorrdNewDown'+catStr].SetBinContent(ibin,htop[histPrefixList[indTopRFcorrdDn]+catStr].GetBinContent(ibin))
					hewk['muRFcorrdNewUp'+catStr].SetBinContent(ibin,hewk[histPrefixList[indEwkRFcorrdUp]+catStr].GetBinContent(ibin))
					hewk['muRFcorrdNewDown'+catStr].SetBinContent(ibin,hewk[histPrefixList[indEwkRFcorrdDn]+catStr].GetBinContent(ibin))
					hqcd['muRFcorrdNewUp'+catStr].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFcorrdUp]+catStr].GetBinContent(ibin))
					hqcd['muRFcorrdNewDown'+catStr].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFcorrdDn]+catStr].GetBinContent(ibin))
					hsig['muRFcorrdNewUp'+catStr].SetBinContent(ibin,hsig[histPrefixList[indSigRFcorrdUp]+catStr].GetBinContent(ibin))
					hsig['muRFcorrdNewDown'+catStr].SetBinContent(ibin,hsig[histPrefixList[indSigRFcorrdDn]+catStr].GetBinContent(ibin))
					htop['muRFdecorrdNewUp'+catStr].SetBinContent(ibin,htop[histPrefixList[indTopRFdecorrdUp]+catStr].GetBinContent(ibin))
					htop['muRFdecorrdNewDown'+catStr].SetBinContent(ibin,htop[histPrefixList[indTopRFdecorrdDn]+catStr].GetBinContent(ibin))
					hewk['muRFdecorrdNewUp'+catStr].SetBinContent(ibin,hewk[histPrefixList[indEwkRFdecorrdUp]+catStr].GetBinContent(ibin))
					hewk['muRFdecorrdNewDown'+catStr].SetBinContent(ibin,hewk[histPrefixList[indEwkRFdecorrdDn]+catStr].GetBinContent(ibin))
					hqcd['muRFdecorrdNewUp'+catStr].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFdecorrdUp]+catStr].GetBinContent(ibin))
					hqcd['muRFdecorrdNewDown'+catStr].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFdecorrdDn]+catStr].GetBinContent(ibin))
					hsig['muRFdecorrdNewUp'+catStr].SetBinContent(ibin,hsig[histPrefixList[indSigRFdecorrdUp]+catStr].GetBinContent(ibin))
					hsig['muRFdecorrdNewDown'+catStr].SetBinContent(ibin,hsig[histPrefixList[indSigRFdecorrdDn]+catStr].GetBinContent(ibin))

					htop['muRFcorrdNewUp'+catStr].SetBinError(ibin,htop[histPrefixList[indTopRFcorrdUp]+catStr].GetBinError(ibin))
					htop['muRFcorrdNewDown'+catStr].SetBinError(ibin,htop[histPrefixList[indTopRFcorrdDn]+catStr].GetBinError(ibin))
					hewk['muRFcorrdNewUp'+catStr].SetBinError(ibin,hewk[histPrefixList[indEwkRFcorrdUp]+catStr].GetBinError(ibin))
					hewk['muRFcorrdNewDown'+catStr].SetBinError(ibin,hewk[histPrefixList[indEwkRFcorrdDn]+catStr].GetBinError(ibin))
					hqcd['muRFcorrdNewUp'+catStr].SetBinError(ibin,hqcd[histPrefixList[indQcdRFcorrdUp]+catStr].GetBinError(ibin))
					hqcd['muRFcorrdNewDown'+catStr].SetBinError(ibin,hqcd[histPrefixList[indQcdRFcorrdDn]+catStr].GetBinError(ibin))
					hsig['muRFcorrdNewUp'+catStr].SetBinError(ibin,hsig[histPrefixList[indSigRFcorrdUp]+catStr].GetBinError(ibin))
					hsig['muRFcorrdNewDown'+catStr].SetBinError(ibin,hsig[histPrefixList[indSigRFcorrdDn]+catStr].GetBinError(ibin))
					htop['muRFdecorrdNewUp'+catStr].SetBinError(ibin,htop[histPrefixList[indTopRFdecorrdUp]+catStr].GetBinError(ibin))
					htop['muRFdecorrdNewDown'+catStr].SetBinError(ibin,htop[histPrefixList[indTopRFdecorrdDn]+catStr].GetBinError(ibin))
					hewk['muRFdecorrdNewUp'+catStr].SetBinError(ibin,hewk[histPrefixList[indEwkRFdecorrdUp]+catStr].GetBinError(ibin))
					hewk['muRFdecorrdNewDown'+catStr].SetBinError(ibin,hewk[histPrefixList[indEwkRFdecorrdDn]+catStr].GetBinError(ibin))
					hqcd['muRFdecorrdNewUp'+catStr].SetBinError(ibin,hqcd[histPrefixList[indQcdRFdecorrdUp]+catStr].GetBinError(ibin))
					hqcd['muRFdecorrdNewDown'+catStr].SetBinError(ibin,hqcd[histPrefixList[indQcdRFdecorrdDn]+catStr].GetBinError(ibin))
					hsig['muRFdecorrdNewUp'+catStr].SetBinError(ibin,hsig[histPrefixList[indSigRFdecorrdUp]+catStr].GetBinError(ibin))
					hsig['muRFdecorrdNewDown'+catStr].SetBinError(ibin,hsig[histPrefixList[indSigRFdecorrdDn]+catStr].GetBinError(ibin))
	
				for pdfInd in range(100):
					hqcd['pdf'+str(pdfInd)+'_'+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__pdf'+str(pdfInd))
					hewk['pdf'+str(pdfInd)+'_'+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__pdf'+str(pdfInd))
					htop['pdf'+str(pdfInd)+'_'+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+topList[0]].Clone(histoPrefix+'__top__pdf'+str(pdfInd))
					hsig['pdf'+str(pdfInd)+'_'+catStr] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__pdf'+str(pdfInd))
					for bkg in qcdList: 
						if bkg!=qcdList[0]: hqcd['pdf'+str(pdfInd)+'_'+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					for bkg in ewkList: 
						if bkg!=ewkList[0]: hewk['pdf'+str(pdfInd)+'_'+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					for bkg in topList: 
						if bkg!=topList[0]: htop['pdf'+str(pdfInd)+'_'+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					for decay in decays:
						if decay!=decays[0]:hsig['pdf'+str(pdfInd)+'_'+catStr].Add(sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decay])
				htop['pdfNewUp'+catStr] = htop['pdf0_'+catStr].Clone(histoPrefix+'__top__pdfNew__plus')
				htop['pdfNewDown'+catStr] = htop['pdf0_'+catStr].Clone(histoPrefix+'__top__pdfNew__minus')
				hewk['pdfNewUp'+catStr] = hewk['pdf0_'+catStr].Clone(histoPrefix+'__ewk__pdfNew__plus')
				hewk['pdfNewDown'+catStr] = hewk['pdf0_'+catStr].Clone(histoPrefix+'__ewk__pdfNew__minus')
				hqcd['pdfNewUp'+catStr] = hqcd['pdf0_'+catStr].Clone(histoPrefix+'__qcd__pdfNew__plus')
				hqcd['pdfNewDown'+catStr] = hqcd['pdf0_'+catStr].Clone(histoPrefix+'__qcd__pdfNew__minus')
				hsig['pdfNewUp'+catStr] = hsig['pdf0_'+catStr].Clone(histoPrefix+'__sig__pdfNew__plus')
				hsig['pdfNewDown'+catStr] = hsig['pdf0_'+catStr].Clone(histoPrefix+'__sig__pdfNew__minus')
				for ibin in range(1,htop['pdfNewUp'+catStr].GetNbinsX()+1):
					weightListTop = [htop['pdf'+str(pdfInd)+'_'+catStr].GetBinContent(ibin) for pdfInd in range(100)]
					weightListEwk = [hewk['pdf'+str(pdfInd)+'_'+catStr].GetBinContent(ibin) for pdfInd in range(100)]
					weightListQcd = [hqcd['pdf'+str(pdfInd)+'_'+catStr].GetBinContent(ibin) for pdfInd in range(100)]
					weightListSig = [hsig['pdf'+str(pdfInd)+'_'+catStr].GetBinContent(ibin) for pdfInd in range(100)]
					indTopPDFUp = sorted(range(len(weightListTop)), key=lambda k: weightListTop[k])[83]
					indTopPDFDn = sorted(range(len(weightListTop)), key=lambda k: weightListTop[k])[15]
					indEwkPDFUp = sorted(range(len(weightListEwk)), key=lambda k: weightListEwk[k])[83]
					indEwkPDFDn = sorted(range(len(weightListEwk)), key=lambda k: weightListEwk[k])[15]
					indQcdPDFUp = sorted(range(len(weightListQcd)), key=lambda k: weightListQcd[k])[83]
					indQcdPDFDn = sorted(range(len(weightListQcd)), key=lambda k: weightListQcd[k])[15]
					indSigPDFUp = sorted(range(len(weightListSig)), key=lambda k: weightListSig[k])[83]
					indSigPDFDn = sorted(range(len(weightListSig)), key=lambda k: weightListSig[k])[15]
					
					htop['pdfNewUp'+catStr].SetBinContent(ibin,htop['pdf'+str(indTopPDFUp)+'_'+catStr].GetBinContent(ibin))
					htop['pdfNewDown'+catStr].SetBinContent(ibin,htop['pdf'+str(indTopPDFDn)+'_'+catStr].GetBinContent(ibin))
					hewk['pdfNewUp'+catStr].SetBinContent(ibin,hewk['pdf'+str(indEwkPDFUp)+'_'+catStr].GetBinContent(ibin))
					hewk['pdfNewDown'+catStr].SetBinContent(ibin,hewk['pdf'+str(indEwkPDFDn)+'_'+catStr].GetBinContent(ibin))
					hqcd['pdfNewUp'+catStr].SetBinContent(ibin,hqcd['pdf'+str(indQcdPDFUp)+'_'+catStr].GetBinContent(ibin))
					hqcd['pdfNewDown'+catStr].SetBinContent(ibin,hqcd['pdf'+str(indQcdPDFDn)+'_'+catStr].GetBinContent(ibin))
					hsig['pdfNewUp'+catStr].SetBinContent(ibin,hsig['pdf'+str(indSigPDFUp)+'_'+catStr].GetBinContent(ibin))
					hsig['pdfNewDown'+catStr].SetBinContent(ibin,hsig['pdf'+str(indSigPDFDn)+'_'+catStr].GetBinContent(ibin))

					htop['pdfNewUp'+catStr].SetBinError(ibin,htop['pdf'+str(indTopPDFUp)+'_'+catStr].GetBinError(ibin))
					htop['pdfNewDown'+catStr].SetBinError(ibin,htop['pdf'+str(indTopPDFDn)+'_'+catStr].GetBinError(ibin))
					hewk['pdfNewUp'+catStr].SetBinError(ibin,hewk['pdf'+str(indEwkPDFUp)+'_'+catStr].GetBinError(ibin))
					hewk['pdfNewDown'+catStr].SetBinError(ibin,hewk['pdf'+str(indEwkPDFDn)+'_'+catStr].GetBinError(ibin))
					hqcd['pdfNewUp'+catStr].SetBinError(ibin,hqcd['pdf'+str(indQcdPDFUp)+'_'+catStr].GetBinError(ibin))
					hqcd['pdfNewDown'+catStr].SetBinError(ibin,hqcd['pdf'+str(indQcdPDFDn)+'_'+catStr].GetBinError(ibin))
					hsig['pdfNewUp'+catStr].SetBinError(ibin,hsig['pdf'+str(indSigPDFUp)+'_'+catStr].GetBinError(ibin))
					hsig['pdfNewDown'+catStr].SetBinError(ibin,hsig['pdf'+str(indSigPDFDn)+'_'+catStr].GetBinError(ibin))
						
			if doQ2sys:
				htop['q2Up'+catStr] = bkghists[histoPrefix+'_'+q2UpList[0]].Clone(histoPrefix+'__top__q2__plus')
				htop['q2Down'+catStr] = bkghists[histoPrefix+'_'+q2DownList[0]].Clone(histoPrefix+'__top__q2__minus')
				for ind in range(1,len(q2UpList)):
					htop['q2Up'+catStr].Add(bkghists[histoPrefix+'_'+q2UpList[ind]])
					htop['q2Down'+catStr].Add(bkghists[histoPrefix+'_'+q2DownList[ind]])
			
			#Group data processes
			hdata[catStr] = datahists[histoPrefix+'_'+dataList[0]].Clone(histoPrefix+'__DATA')
			print datahists[histoPrefix+'_'+dat].Integral()
			for dat in dataList:
				if dat!=dataList[0]: hdata[catStr].Add(datahists[histoPrefix+'_'+dat])

			#prepare yield table
			yieldTable[histoPrefix]['top']    = htop[catStr].Integral()
			yieldTable[histoPrefix]['ewk']    = hewk[catStr].Integral()
			yieldTable[histoPrefix]['qcd']    = hqcd[catStr].Integral()
			yieldTable[histoPrefix]['totBkg'] = htop[catStr].Integral()+hewk[catStr].Integral()+hqcd[catStr].Integral()
			yieldTable[histoPrefix]['data']   = hdata[catStr].Integral()
			yieldTable[histoPrefix]['dataOverBkg']= yieldTable[histoPrefix]['data']/yieldTable[histoPrefix]['totBkg']
			yieldTable[histoPrefix]['WJets']  = hwjets[catStr].Integral()
			yieldTable[histoPrefix]['ZJets']  = hzjets[catStr].Integral()
			yieldTable[histoPrefix]['VV']     = hvv[catStr].Integral()
			yieldTable[histoPrefix]['TTW']    = httw[catStr].Integral()
			yieldTable[histoPrefix]['TTZ']    = httz[catStr].Integral()
			yieldTable[histoPrefix]['TTJets'] = httjets[catStr].Integral()
			yieldTable[histoPrefix]['T']      = ht[catStr].Integral()
			yieldTable[histoPrefix]['QCD']    = hqcd[catStr].Integral()
			yieldTable[histoPrefix][signal]   = hsig[catStr].Integral()
			
			#+/- 1sigma variations of shape systematics
			if doAllSys:
				for systematic in systematicList:
					for ud in ['Up','Down']:
						yieldTable[histoPrefix+systematic+ud]['top']    = htop[systematic+ud+catStr].Integral()
						if systematic!='toppt':
							yieldTable[histoPrefix+systematic+ud]['ewk']    = hewk[systematic+ud+catStr].Integral()
							yieldTable[histoPrefix+systematic+ud]['qcd']    = hqcd[systematic+ud+catStr].Integral()
							yieldTable[histoPrefix+systematic+ud]['totBkg'] = htop[systematic+ud+catStr].Integral()+hewk[systematic+ud+catStr].Integral()+hqcd[systematic+ud+catStr].Integral()
							yieldTable[histoPrefix+systematic+ud][signal]   = hsig[systematic+ud+catStr].Integral()
						
			if doQ2sys:
				yieldTable[histoPrefix+'q2Up']['top']    = htop['q2Up'+catStr].Integral()
				yieldTable[histoPrefix+'q2Down']['top']    = htop['q2Down'+catStr].Integral()

			#prepare MC yield error table
			yieldStatErrTable[histoPrefix]['top']    = 0.
			yieldStatErrTable[histoPrefix]['ewk']    = 0.
			yieldStatErrTable[histoPrefix]['qcd']    = 0.
			yieldStatErrTable[histoPrefix]['totBkg'] = 0.
			yieldStatErrTable[histoPrefix]['data']   = 0.
			yieldStatErrTable[histoPrefix]['dataOverBkg']= 0.
			yieldStatErrTable[histoPrefix]['WJets']  = 0.
			yieldStatErrTable[histoPrefix]['ZJets']  = 0.
			yieldStatErrTable[histoPrefix]['VV']     = 0.
			yieldStatErrTable[histoPrefix]['TTW']    = 0.
			yieldStatErrTable[histoPrefix]['TTZ']    = 0.
			yieldStatErrTable[histoPrefix]['TTJets'] = 0.
			yieldStatErrTable[histoPrefix]['T']      = 0.
			yieldStatErrTable[histoPrefix]['QCD']    = 0.
			yieldStatErrTable[histoPrefix][signal]   = 0.

			for ibin in range(1,hsig[catStr].GetXaxis().GetNbins()+1):
				yieldStatErrTable[histoPrefix]['top']    += htop[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['ewk']    += hewk[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['qcd']    += hqcd[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['totBkg'] += htop[catStr].GetBinError(ibin)**2+hewk[catStr].GetBinError(ibin)**2+hqcd[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['data']   += hdata[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['WJets']  += hwjets[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['ZJets']  += hzjets[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['VV']     += hvv[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['TTW']    += httw[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['TTZ']    += httz[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['TTJets'] += httjets[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['T']      += ht[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['QCD']    += hqcd[catStr].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix][signal]   += hsig[catStr].GetBinError(ibin)**2

			#scale signal cross section to 1pb
			if scaleSignalXsecTo1pb: hsig[catStr].Scale(1./xsec[signal])
			#write theta histograms in root file, avoid having processes with no event yield (to make theta happy) 
			if hsig[catStr].Integral() > 0:  
				hsig[catStr].Write()
				if doAllSys:
					for systematic in systematicList:
						if systematic=='toppt': continue
						if scaleSignalXsecTo1pb: 
							hsig[systematic+'Up'+catStr].Scale(1./xsec[signal])
							hsig[systematic+'Down'+catStr].Scale(1./xsec[signal])
						if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
							hsig[systematic+'Up'+catStr].Scale(hsig[catStr].Integral()/hsig[systematic+'Up'+catStr].Integral())
							hsig[systematic+'Down'+catStr].Scale(hsig[catStr].Integral()/hsig[systematic+'Down'+catStr].Integral())
						hsig[systematic+'Up'+catStr].Write()
						hsig[systematic+'Down'+catStr].Write()
					for pdfInd in range(100): hsig['pdf'+str(pdfInd)+'_'+catStr].Write()
			if htop[catStr].Integral() > 0:  
				htop[catStr].Write()
				if doAllSys:
					for systematic in systematicList:
						if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
							htop[systematic+'Up'+catStr].Scale(htop[catStr].Integral()/htop[systematic+'Up'+catStr].Integral())
							htop[systematic+'Down'+catStr].Scale(htop[catStr].Integral()/htop[systematic+'Down'+catStr].Integral())  
						htop[systematic+'Up'+catStr].Write()
						htop[systematic+'Down'+catStr].Write()
					for pdfInd in range(100): htop['pdf'+str(pdfInd)+'_'+catStr].Write()
				if doQ2sys:
					htop['q2Up'+catStr].Write()
					htop['q2Down'+catStr].Write()
			if hewk[catStr].Integral() > 0:  
				hewk[catStr].Write()
				if doAllSys:
					for systematic in systematicList:
						if systematic=='toppt': continue
						if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
							hewk[systematic+'Up'+catStr].Scale(hewk[catStr].Integral()/hewk[systematic+'Up'+catStr].Integral())
							hewk[systematic+'Down'+catStr].Scale(hewk[catStr].Integral()/hewk[systematic+'Down'+catStr].Integral())  
						hewk[systematic+'Up'+catStr].Write()
						hewk[systematic+'Down'+catStr].Write()
					for pdfInd in range(100): hewk['pdf'+str(pdfInd)+'_'+catStr].Write()
			if hqcd[catStr].Integral() > 0:  
				hqcd[catStr].Write()
				if doAllSys:
					for systematic in systematicList:
						if systematic == 'pdf' or systematic == 'pdfNew' or systematic == 'muR' or systematic == 'muF' or systematic == 'muRFcorrd' or systematic=='toppt': continue
						hqcd[systematic+'Up'+catStr].Write()
						hqcd[systematic+'Down'+catStr].Write()
					for pdfInd in range(100): hqcd['pdf'+str(pdfInd)+'_'+catStr].Write()
			hdata[catStr].Write()
			i+=1
		outputRfile.Close()
	
	stdout_old = sys.stdout
	logFile = open(outDir+'/yields_'+discriminant+'_'+lumiStr+'fb.txt','a')
	sys.stdout = logFile

	## PRINTING YIELD TABLE WITH STATISTICAL UNCERTAINTIES ##
	#first print table without background grouping
	ljust_i = 1
	print 'CUTS:',cutString
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	for bkg in bkgStackList: print bkg.ljust(ljust_i),
	print 'data'.ljust(ljust_i),
	print
	for cat in catList:
		tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		catStr='is'+cat[0]+'_'+tagStr
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		print (catStr).ljust(ljust_i),
		for bkg in bkgStackList:
			print str(yieldTable[histoPrefix][bkg]).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['data']).ljust(ljust_i),
		print

	print 'YIELDS ERRORS'
	for cat in catList:
		tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		catStr='is'+cat[0]+'_'+tagStr
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		print (catStr).ljust(ljust_i),
		for bkg in bkgStackList:
			print str(math.sqrt(yieldStatErrTable[histoPrefix][bkg])).ljust(ljust_i),
		print str(math.sqrt(yieldStatErrTable[histoPrefix]['data'])).ljust(ljust_i),
		print

	#now print with top,ewk,qcd grouping
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	print 'ewk'.ljust(ljust_i),
	print 'top'.ljust(ljust_i),
	print 'qcd'.ljust(ljust_i),
	print 'data'.ljust(ljust_i),
	print
	for cat in catList:
		tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		catStr='is'+cat[0]+'_'+tagStr
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		print (catStr).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['ewk']).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['top']).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['qcd']).ljust(ljust_i),
		print str(yieldTable[histoPrefix]['data']).ljust(ljust_i),
		print

	print 'YIELDS ERRORS'
	for cat in catList:
		tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		catStr='is'+cat[0]+'_'+tagStr
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		print (catStr).ljust(ljust_i),
		print str(math.sqrt(yieldStatErrTable[histoPrefix]['ewk'])).ljust(ljust_i),
		print str(math.sqrt(yieldStatErrTable[histoPrefix]['top'])).ljust(ljust_i),
		print str(math.sqrt(yieldStatErrTable[histoPrefix]['qcd'])).ljust(ljust_i),
		print str(math.sqrt(yieldStatErrTable[histoPrefix]['data'])).ljust(ljust_i),
		print

	#print yields for signals
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	for sig in sigList: print sig.ljust(ljust_i),
	print
	for cat in catList:
		tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		catStr='is'+cat[0]+'_'+tagStr
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		print (catStr).ljust(ljust_i),
		for sig in sigList:
			print str(yieldTable[histoPrefix][sig]).ljust(ljust_i),
		print

	print 'YIELDS ERRORS'
	for cat in catList:
		tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		catStr='is'+cat[0]+'_'+tagStr
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		print (catStr).ljust(ljust_i),
		for sig in sigList:
			print str(math.sqrt(yieldStatErrTable[histoPrefix][sig])).ljust(ljust_i),
		print
				
	#print for AN tables
	print
	print "FOR AN (errors are statistical+normalization systematics): "
	print
	print 'YIELDS ELECTRON+JETS'.ljust(20*ljust_i), 
	for cat in catList:
		tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		catStr='is'+cat[0]+'_'+tagStr
		if cat[0]!='E': continue
		print (catStr).ljust(ljust_i),
	print
	for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
		print process.ljust(ljust_i),
		for cat in catList:
			tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr='is'+cat[0]+'_'+tagStr
			if cat[0]!='E': continue
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
			if process=='dataOverBkg':
				dataTemp = yieldTable[histoPrefix]['data']+1e-20
				dataTempErr = yieldStatErrTable[histoPrefix]['data']
				totBkgTemp = yieldTable[histoPrefix]['totBkg']+1e-20
				totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg'] # statistical error squared
				totBkgTempErr += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
				totBkgTempErr += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
				totBkgTempErr += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
				totBkgTempErr += (corrdSys*totBkgTemp)**2
				dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
				print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
			else:
				yieldtemp = yieldTable[histoPrefix][process]
				yielderrtemp = yieldStatErrTable[histoPrefix][process]
				if process=='totBkg': 
					yielderrtemp += (corrdSys*yieldtemp)**2
					yielderrtemp += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
					yielderrtemp += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
					yielderrtemp += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
				elif process in sigList: 
					yielderrtemp += (corrdSys*yieldtemp)**2
				elif process!='data': 
					yielderrtemp += (corrdSys*yieldtemp)**2
					yielderrtemp += (addSys[process+'_'+tagStr]*yieldTable[histoPrefix][process])**2
				if process=='data': print ' & '+str(int(yieldtemp)),
				elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
				else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		print '\\\\',
		print
	print
	print 'YIELDS MUON+JETS'.ljust(20*ljust_i), 
	for cat in catList:
		tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		catStr='is'+cat[0]+'_'+tagStr
		if cat[0]!='M': continue
		print (catStr).ljust(ljust_i),
	print
	for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
		print process.ljust(ljust_i),
		for cat in catList:
			tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr='is'+cat[0]+'_'+tagStr
			if cat[0]!='M': continue
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
			if process=='dataOverBkg':
				dataTemp = yieldTable[histoPrefix]['data']+1e-20
				dataTempErr = yieldStatErrTable[histoPrefix]['data']
				totBkgTemp = yieldTable[histoPrefix]['totBkg']+1e-20
				totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg'] # statistical error squared
				totBkgTempErr += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
				totBkgTempErr += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
				totBkgTempErr += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
				totBkgTempErr += (corrdSys*totBkgTemp)**2
				dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
				print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
			else:
				yieldtemp = yieldTable[histoPrefix][process]
				yielderrtemp = yieldStatErrTable[histoPrefix][process]
				if process=='totBkg': 
					yielderrtemp += (corrdSys*yieldtemp)**2
					yielderrtemp += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
					yielderrtemp += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
					yielderrtemp += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
				elif process in sigList: 
					yielderrtemp += (corrdSys*yieldtemp)**2
				elif process!='data': 
					yielderrtemp += (corrdSys*yieldtemp)**2
					yielderrtemp += (addSys[process+'_'+tagStr]*yieldTable[histoPrefix][process])**2
				if process=='data': print ' & '+str(int(yieldtemp)),
				elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
				else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		print '\\\\',
		print
		
	#print for AN tables systematics
	if doAllSys:
		print
		print "FOR AN (shape systematic percentaces): "
		print
		print 'YIELDS'.ljust(20*ljust_i), 
		for cat in catList:
			tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr='is'+cat[0]+'_'+tagStr
			print (catStr).ljust(ljust_i),
		print
		for process in ['ewk','top']+sigList:
			print process.ljust(ljust_i),
			print
			for ud in ['Up','Down']:
				for systematic in systematicList:
					if systematic=='toppt' and process!='top': continue
					print (systematic+ud).ljust(ljust_i),
					for cat in catList:
						tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
						catStr='is'+cat[0]+'_'+tagStr
						histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
						print ' & '+str(round_sig(yieldTable[histoPrefix+systematic+ud][process]/(yieldTable[histoPrefix][process]+1e-20),2)),
					print '\\\\',
					print
				if process!='top': continue
				print ('q2'+ud).ljust(ljust_i),
				for cat in catList:
					tagStr='nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
					catStr='is'+cat[0]+'_'+tagStr
					histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
					print ' & '+str(round_sig(yieldTable[histoPrefix+'q2'+ud][process]/(yieldTable[histoPrefix][process]+1e-20),2)),
				print '\\\\',
				print
		
	print
	print "FOR PAS (errors are statistical+normalization systematics): " #combines e/m channels
	print
	print 'YIELDS'.ljust(20*ljust_i), 
	for tag in tagList:
		tagStr = 'nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]
		print (tagStr).ljust(ljust_i),
	print
	for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
		print process.ljust(ljust_i),
		for tag in tagList:
			tagStr = 'nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]
			histoPrefix=discriminant+'_'+lumiStr+'fb_isE'+'_'+tagStr
			if process=='dataOverBkg':
				dataTemp = yieldTable[histoPrefix]['data']+yieldTable[histoPrefix.replace('_isE','_isM')]['data']+1e-20
				dataTempErr = yieldStatErrTable[histoPrefix]['data']+yieldStatErrTable[histoPrefix.replace('_isE','_isM')]['data']
				totBkgTemp = yieldTable[histoPrefix]['totBkg']+yieldTable[histoPrefix.replace('_isE','_isM')]['totBkg']+1e-20
				totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg']+yieldStatErrTable[histoPrefix.replace('_isE','_isM')]['totBkg'] # statistical error squared
				totBkgTempErr += (addSys['top_'+tagStr]*(yieldTable[histoPrefix]['top']+yieldTable[histoPrefix.replace('_isE','_isM')]['top']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
				totBkgTempErr += (addSys['ewk_'+tagStr]*(yieldTable[histoPrefix]['ewk']+yieldTable[histoPrefix.replace('_isE','_isM')]['ewk']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
				totBkgTempErr += (addSys['qcd_'+tagStr]*(yieldTable[histoPrefix]['qcd']+yieldTable[histoPrefix.replace('_isE','_isM')]['qcd']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
				totBkgTempErr += (corrdSys*totBkgTemp)**2
				dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
				print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
			else:
				yieldtemp = yieldTable[histoPrefix][process]+yieldTable[histoPrefix.replace('_isE','_isM')][process]
				yielderrtemp = yieldStatErrTable[histoPrefix][process]++yieldStatErrTable[histoPrefix.replace('_isE','_isM')][process]
				if process=='totBkg': 
					yielderrtemp += (corrdSys*yieldtemp)**2
					yielderrtemp += (addSys['top_'+tagStr]*(yieldTable[histoPrefix]['top']+yieldTable[histoPrefix.replace('_isE','_isM')]['top']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					yielderrtemp += (addSys['ewk_'+tagStr]*(yieldTable[histoPrefix]['ewk']+yieldTable[histoPrefix.replace('_isE','_isM')]['ewk']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					yielderrtemp += (addSys['qcd_'+tagStr]*(yieldTable[histoPrefix]['qcd']+yieldTable[histoPrefix.replace('_isE','_isM')]['qcd']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
				elif process in sigList: 
					yielderrtemp += (corrdSys*yieldtemp)**2
				elif process!='data': 
					yielderrtemp += (corrdSys*yieldtemp)**2
					yielderrtemp += (addSys[process+'_'+tagStr]*(yieldTable[histoPrefix][process]+yieldTable[histoPrefix.replace('_isE','_isM')][process]))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
				if process=='data': print ' & '+str(int(yieldtemp)),
				elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
				else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		print '\\\\',
		print
		
	sys.stdout = stdout_old
	logFile.close()

###########################################################
################ CATEGORIZATION DECAYS ####################
###########################################################
def makeThetaCatsIndDecays(datahists,sighists,bkghists,discriminant):

	## This function categorizes the events into electron/muon --> 0/1p W-tag! --> 1/2p b-tag (the same as Cat1, but there is no 4p/3p jets requirement here)
	## Input  histograms (datahists,sighists,bkghists) must have corresponding histograms returned from analyze.py##

	## INITIALIZE DICTIONARIES FOR YIELDS AND THEIR UNCERTAINTIES ##
	yieldTable = {}
	yieldStatErrTable = {} #what is actually stored in this is the square of the uncertainty
	for cat in catList:
		tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		catStr = 'is'+cat[0]+'_'+tagStr
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		yieldTable[histoPrefix]={}
		yieldStatErrTable[histoPrefix]={}
		if doAllSys:
			for systematic in systematicList:
				for ud in ['Up','Down']:
					yieldTable[histoPrefix+systematic+ud]={}
				
		if doQ2sys:
			yieldTable[histoPrefix+'q2Up']={}
			yieldTable[histoPrefix+'q2Down']={}

	## WRITING HISTOGRAMS IN ROOT FILE ##
	i=0
	for decay in decays:
		for signal in sigList:
			outputRfile = R.TFile(outDir+'/templates_'+discriminant+'_'+signal+decay+'_'+lumiStr+'fb.root','RECREATE')
			hsig,htop,hewk,hqcd,hdata={},{},{},{},{}
			hwjets,hzjets,httjets,ht,httw,httz,hvv={},{},{},{},{},{},{}
			for cat in catList:
				tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
				catStr = 'is'+cat[0]+'_'+tagStr
				histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr

				#Group processes
				hwjets[catStr] = bkghists[histoPrefix+'_'+wjetList[0]].Clone(histoPrefix+'_WJets')
				hzjets[catStr] = bkghists[histoPrefix+'_'+zjetList[0]].Clone(histoPrefix+'_ZJets')
				httjets[catStr] = bkghists[histoPrefix+'_'+ttjetList[0]].Clone(histoPrefix+'_TTJets')
				ht[catStr] = bkghists[histoPrefix+'_'+tList[0]].Clone(histoPrefix+'_T')
				httw[catStr] = bkghists[histoPrefix+'_'+ttwList[0]].Clone(histoPrefix+'_TTW')
				httz[catStr] = bkghists[histoPrefix+'_'+ttzList[0]].Clone(histoPrefix+'_TTZ')
				hvv[catStr] = bkghists[histoPrefix+'_'+vvList[0]].Clone(histoPrefix+'_VV')
				for bkg in ttjetList:
					if bkg!=ttjetList[0]: httjets[catStr].Add(bkghists[histoPrefix+'_'+bkg])
				for bkg in wjetList:
					if bkg!=wjetList[0]: hwjets[catStr].Add(bkghists[histoPrefix+'_'+bkg])
				for bkg in ttwList:
					if bkg!=ttwList[0]: httw[catStr].Add(bkghists[histoPrefix+'_'+bkg])
				for bkg in ttzList:
					if bkg!=ttzList[0]: httz[catStr].Add(bkghists[histoPrefix+'_'+bkg])
				for bkg in tList:
					if bkg!=tList[0]: ht[catStr].Add(bkghists[histoPrefix+'_'+bkg])
				for bkg in zjetList:
					if bkg!=zjetList[0]: hzjets[catStr].Add(bkghists[histoPrefix+'_'+bkg])
				for bkg in vvList:
					if bkg!=vvList[0]: hvv[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			
				#Group QCD processes
				hqcd[catStr] = bkghists[histoPrefix+'_'+qcdList[0]].Clone(histoPrefix+'__qcd')
				for bkg in qcdList: 
					if bkg!=qcdList[0]: hqcd[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			
				#Group EWK processes
				hewk[catStr] = bkghists[histoPrefix+'_'+ewkList[0]].Clone(histoPrefix+'__ewk')
				for bkg in ewkList:
					if bkg!=ewkList[0]: hewk[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			
				#Group TOP processes
				htop[catStr] = bkghists[histoPrefix+'_'+topList[0]].Clone(histoPrefix+'__top')
				for bkg in topList:
					if bkg!=topList[0]: htop[catStr].Add(bkghists[histoPrefix+'_'+bkg])
			
				#get signal
				hsig[catStr] = sighists[histoPrefix+'_'+signal+decay].Clone(histoPrefix+'__sig')

				#systematics
				if doAllSys:
					for systematic in systematicList:
						if systematic=='pdfNew' or systematic=='muRFcorrdNew' or systematic=='muRFdecorrdNew': continue
						for ud in ['Up','Down']:
							if systematic!='toppt':
								hqcd[systematic+ud+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
								hewk[systematic+ud+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
								htop[systematic+ud+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+topList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
								hsig[systematic+ud+catStr] = sighists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+signal+decay].Clone(histoPrefix+'__sig__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
								for bkg in qcdList: 
									if bkg!=qcdList[0]: hqcd[systematic+ud+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
								for bkg in ewkList: 
									if bkg!=ewkList[0]: hewk[systematic+ud+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
								for bkg in topList: 
									if bkg!=topList[0]: htop[systematic+ud+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
							if systematic=='toppt': # top pt is only on the ttbar sample, so it needs special treatment!
								htop[systematic+ud+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ttjetList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
								for bkg in ttjetList: 
									if bkg!=ttjetList[0]: htop[systematic+ud+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
								for bkg in topList: 
									if bkg not in ttjetList: htop[systematic+ud+catStr].Add(bkghists[histoPrefix+'_'+bkg])

					htop['muRFcorrdNewUp'+catStr] = htop['muRFcorrdUp'+catStr].Clone(histoPrefix+'__top__muRFcorrdNew__plus')
					htop['muRFcorrdNewDown'+catStr] = htop['muRFcorrdUp'+catStr].Clone(histoPrefix+'__top__muRFcorrdNew__minus')
					hewk['muRFcorrdNewUp'+catStr] = hewk['muRFcorrdUp'+catStr].Clone(histoPrefix+'__ewk__muRFcorrdNew__plus')
					hewk['muRFcorrdNewDown'+catStr] = hewk['muRFcorrdUp'+catStr].Clone(histoPrefix+'__ewk__muRFcorrdNew__minus')
					hqcd['muRFcorrdNewUp'+catStr] = hqcd['muRFcorrdUp'+catStr].Clone(histoPrefix+'__qcd__muRFcorrdNew__plus')
					hqcd['muRFcorrdNewDown'+catStr] = hqcd['muRFcorrdUp'+catStr].Clone(histoPrefix+'__qcd__muRFcorrdNew__minus')
					hsig['muRFcorrdNewUp'+catStr] = hsig['muRFcorrdUp'+catStr].Clone(histoPrefix+'__sig__muRFcorrdNew__plus')
					hsig['muRFcorrdNewDown'+catStr] = hsig['muRFcorrdUp'+catStr].Clone(histoPrefix+'__sig__muRFcorrdNew__minus')

					htop['muRFdecorrdNewUp'+catStr] = htop['muRFcorrdUp'+catStr].Clone(histoPrefix+'__top__muRFdecorrdNew__plus')
					htop['muRFdecorrdNewDown'+catStr] = htop['muRFcorrdUp'+catStr].Clone(histoPrefix+'__top__muRFdecorrdNew__minus')
					hewk['muRFdecorrdNewUp'+catStr] = hewk['muRFcorrdUp'+catStr].Clone(histoPrefix+'__ewk__muRFdecorrdNew__plus')
					hewk['muRFdecorrdNewDown'+catStr] = hewk['muRFcorrdUp'+catStr].Clone(histoPrefix+'__ewk__muRFdecorrdNew__minus')
					hqcd['muRFdecorrdNewUp'+catStr] = hqcd['muRFcorrdUp'+catStr].Clone(histoPrefix+'__qcd__muRFdecorrdNew__plus')
					hqcd['muRFdecorrdNewDown'+catStr] = hqcd['muRFcorrdUp'+catStr].Clone(histoPrefix+'__qcd__muRFdecorrdNew__minus')
					hsig['muRFdecorrdNewUp'+catStr] = hsig['muRFcorrdUp'+catStr].Clone(histoPrefix+'__sig__muRFdecorrdNew__plus')
					hsig['muRFdecorrdNewDown'+catStr] = hsig['muRFcorrdUp'+catStr].Clone(histoPrefix+'__sig__muRFdecorrdNew__minus')

					# nominal,renormWeights[4],renormWeights[2],renormWeights[1],renormWeights[0],renormWeights[5],renormWeights[3]
					histPrefixList = ['','muRUp','muRDown','muFUp','muFDown','muRFcorrdUp','muRFcorrdDown']
					for ibin in range(1,htop[catStr].GetNbinsX()+1):
						weightListTop = [htop[item+catStr].GetBinContent(ibin) for item in histPrefixList]	
						weightListEwk = [hewk[item+catStr].GetBinContent(ibin) for item in histPrefixList]	
						weightListQcd = [hqcd[item+catStr].GetBinContent(ibin) for item in histPrefixList]	
						weightListSig = [hsig[item+catStr].GetBinContent(ibin) for item in histPrefixList]
						indTopRFcorrdUp = weightListTop.index(max(weightListTop))
						indTopRFcorrdDn = weightListTop.index(min(weightListTop))
						indEwkRFcorrdUp = weightListEwk.index(max(weightListEwk))
						indEwkRFcorrdDn = weightListEwk.index(min(weightListEwk))
						indQcdRFcorrdUp = weightListQcd.index(max(weightListQcd))
						indQcdRFcorrdDn = weightListQcd.index(min(weightListQcd))
						indSigRFcorrdUp = weightListSig.index(max(weightListSig))
						indSigRFcorrdDn = weightListSig.index(min(weightListSig))

						indTopRFdecorrdUp = weightListTop.index(max(weightListTop[:-2]))
						indTopRFdecorrdDn = weightListTop.index(min(weightListTop[:-2]))
						indEwkRFdecorrdUp = weightListEwk.index(max(weightListEwk[:-2]))
						indEwkRFdecorrdDn = weightListEwk.index(min(weightListEwk[:-2]))
						indQcdRFdecorrdUp = weightListQcd.index(max(weightListQcd[:-2]))
						indQcdRFdecorrdDn = weightListQcd.index(min(weightListQcd[:-2]))
						indSigRFdecorrdUp = weightListSig.index(max(weightListSig[:-2]))
						indSigRFdecorrdDn = weightListSig.index(min(weightListSig[:-2]))
					
						htop['muRFcorrdNewUp'+catStr].SetBinContent(ibin,htop[histPrefixList[indTopRFcorrdUp]+catStr].GetBinContent(ibin))
						htop['muRFcorrdNewDown'+catStr].SetBinContent(ibin,htop[histPrefixList[indTopRFcorrdDn]+catStr].GetBinContent(ibin))
						hewk['muRFcorrdNewUp'+catStr].SetBinContent(ibin,hewk[histPrefixList[indEwkRFcorrdUp]+catStr].GetBinContent(ibin))
						hewk['muRFcorrdNewDown'+catStr].SetBinContent(ibin,hewk[histPrefixList[indEwkRFcorrdDn]+catStr].GetBinContent(ibin))
						hqcd['muRFcorrdNewUp'+catStr].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFcorrdUp]+catStr].GetBinContent(ibin))
						hqcd['muRFcorrdNewDown'+catStr].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFcorrdDn]+catStr].GetBinContent(ibin))
						hsig['muRFcorrdNewUp'+catStr].SetBinContent(ibin,hsig[histPrefixList[indSigRFcorrdUp]+catStr].GetBinContent(ibin))
						hsig['muRFcorrdNewDown'+catStr].SetBinContent(ibin,hsig[histPrefixList[indSigRFcorrdDn]+catStr].GetBinContent(ibin))
						htop['muRFdecorrdNewUp'+catStr].SetBinContent(ibin,htop[histPrefixList[indTopRFdecorrdUp]+catStr].GetBinContent(ibin))
						htop['muRFdecorrdNewDown'+catStr].SetBinContent(ibin,htop[histPrefixList[indTopRFdecorrdDn]+catStr].GetBinContent(ibin))
						hewk['muRFdecorrdNewUp'+catStr].SetBinContent(ibin,hewk[histPrefixList[indEwkRFdecorrdUp]+catStr].GetBinContent(ibin))
						hewk['muRFdecorrdNewDown'+catStr].SetBinContent(ibin,hewk[histPrefixList[indEwkRFdecorrdDn]+catStr].GetBinContent(ibin))
						hqcd['muRFdecorrdNewUp'+catStr].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFdecorrdUp]+catStr].GetBinContent(ibin))
						hqcd['muRFdecorrdNewDown'+catStr].SetBinContent(ibin,hqcd[histPrefixList[indQcdRFdecorrdDn]+catStr].GetBinContent(ibin))
						hsig['muRFdecorrdNewUp'+catStr].SetBinContent(ibin,hsig[histPrefixList[indSigRFdecorrdUp]+catStr].GetBinContent(ibin))
						hsig['muRFdecorrdNewDown'+catStr].SetBinContent(ibin,hsig[histPrefixList[indSigRFdecorrdDn]+catStr].GetBinContent(ibin))

						htop['muRFcorrdNewUp'+catStr].SetBinError(ibin,htop[histPrefixList[indTopRFcorrdUp]+catStr].GetBinError(ibin))
						htop['muRFcorrdNewDown'+catStr].SetBinError(ibin,htop[histPrefixList[indTopRFcorrdDn]+catStr].GetBinError(ibin))
						hewk['muRFcorrdNewUp'+catStr].SetBinError(ibin,hewk[histPrefixList[indEwkRFcorrdUp]+catStr].GetBinError(ibin))
						hewk['muRFcorrdNewDown'+catStr].SetBinError(ibin,hewk[histPrefixList[indEwkRFcorrdDn]+catStr].GetBinError(ibin))
						hqcd['muRFcorrdNewUp'+catStr].SetBinError(ibin,hqcd[histPrefixList[indQcdRFcorrdUp]+catStr].GetBinError(ibin))
						hqcd['muRFcorrdNewDown'+catStr].SetBinError(ibin,hqcd[histPrefixList[indQcdRFcorrdDn]+catStr].GetBinError(ibin))
						hsig['muRFcorrdNewUp'+catStr].SetBinError(ibin,hsig[histPrefixList[indSigRFcorrdUp]+catStr].GetBinError(ibin))
						hsig['muRFcorrdNewDown'+catStr].SetBinError(ibin,hsig[histPrefixList[indSigRFcorrdDn]+catStr].GetBinError(ibin))
						htop['muRFdecorrdNewUp'+catStr].SetBinError(ibin,htop[histPrefixList[indTopRFdecorrdUp]+catStr].GetBinError(ibin))
						htop['muRFdecorrdNewDown'+catStr].SetBinError(ibin,htop[histPrefixList[indTopRFdecorrdDn]+catStr].GetBinError(ibin))
						hewk['muRFdecorrdNewUp'+catStr].SetBinError(ibin,hewk[histPrefixList[indEwkRFdecorrdUp]+catStr].GetBinError(ibin))
						hewk['muRFdecorrdNewDown'+catStr].SetBinError(ibin,hewk[histPrefixList[indEwkRFdecorrdDn]+catStr].GetBinError(ibin))
						hqcd['muRFdecorrdNewUp'+catStr].SetBinError(ibin,hqcd[histPrefixList[indQcdRFdecorrdUp]+catStr].GetBinError(ibin))
						hqcd['muRFdecorrdNewDown'+catStr].SetBinError(ibin,hqcd[histPrefixList[indQcdRFdecorrdDn]+catStr].GetBinError(ibin))
						hsig['muRFdecorrdNewUp'+catStr].SetBinError(ibin,hsig[histPrefixList[indSigRFdecorrdUp]+catStr].GetBinError(ibin))
						hsig['muRFdecorrdNewDown'+catStr].SetBinError(ibin,hsig[histPrefixList[indSigRFdecorrdDn]+catStr].GetBinError(ibin))

					for pdfInd in range(100):
						hqcd['pdf'+str(pdfInd)+'_'+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__pdf'+str(pdfInd))
						hewk['pdf'+str(pdfInd)+'_'+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__pdf'+str(pdfInd))
						htop['pdf'+str(pdfInd)+'_'+catStr] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+topList[0]].Clone(histoPrefix+'__top__pdf'+str(pdfInd))
						hsig['pdf'+str(pdfInd)+'_'+catStr] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decay].Clone(histoPrefix+'__sig__pdf'+str(pdfInd))
						for bkg in qcdList: 
							if bkg!=qcdList[0]: hqcd['pdf'+str(pdfInd)+'_'+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
						for bkg in ewkList: 
							if bkg!=ewkList[0]: hewk['pdf'+str(pdfInd)+'_'+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
						for bkg in topList: 
							if bkg!=topList[0]: htop['pdf'+str(pdfInd)+'_'+catStr].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					htop['pdfNewUp'+catStr] = htop['pdf0_'+catStr].Clone(histoPrefix+'__top__pdfNew__plus')
					htop['pdfNewDown'+catStr] = htop['pdf0_'+catStr].Clone(histoPrefix+'__top__pdfNew__minus')
					hewk['pdfNewUp'+catStr] = hewk['pdf0_'+catStr].Clone(histoPrefix+'__ewk__pdfNew__plus')
					hewk['pdfNewDown'+catStr] = hewk['pdf0_'+catStr].Clone(histoPrefix+'__ewk__pdfNew__minus')
					hqcd['pdfNewUp'+catStr] = hqcd['pdf0_'+catStr].Clone(histoPrefix+'__qcd__pdfNew__plus')
					hqcd['pdfNewDown'+catStr] = hqcd['pdf0_'+catStr].Clone(histoPrefix+'__qcd__pdfNew__minus')
					hsig['pdfNewUp'+catStr] = hsig['pdf0_'+catStr].Clone(histoPrefix+'__sig__pdfNew__plus')
					hsig['pdfNewDown'+catStr] = hsig['pdf0_'+catStr].Clone(histoPrefix+'__sig__pdfNew__minus')
					for ibin in range(1,htop['pdfNewUp'+catStr].GetNbinsX()+1):
						weightListTop = [htop['pdf'+str(pdfInd)+'_'+catStr].GetBinContent(ibin) for pdfInd in range(100)]
						weightListEwk = [hewk['pdf'+str(pdfInd)+'_'+catStr].GetBinContent(ibin) for pdfInd in range(100)]
						weightListQcd = [hqcd['pdf'+str(pdfInd)+'_'+catStr].GetBinContent(ibin) for pdfInd in range(100)]
						weightListSig = [hsig['pdf'+str(pdfInd)+'_'+catStr].GetBinContent(ibin) for pdfInd in range(100)]
						indTopPDFUp = sorted(range(len(weightListTop)), key=lambda k: weightListTop[k])[83]
						indTopPDFDn = sorted(range(len(weightListTop)), key=lambda k: weightListTop[k])[15]
						indEwkPDFUp = sorted(range(len(weightListEwk)), key=lambda k: weightListEwk[k])[83]
						indEwkPDFDn = sorted(range(len(weightListEwk)), key=lambda k: weightListEwk[k])[15]
						indQcdPDFUp = sorted(range(len(weightListQcd)), key=lambda k: weightListQcd[k])[83]
						indQcdPDFDn = sorted(range(len(weightListQcd)), key=lambda k: weightListQcd[k])[15]
						indSigPDFUp = sorted(range(len(weightListSig)), key=lambda k: weightListSig[k])[83]
						indSigPDFDn = sorted(range(len(weightListSig)), key=lambda k: weightListSig[k])[15]
						htop['pdfNewUp'+catStr].SetBinContent(ibin,htop['pdf'+str(indTopPDFUp)+'_'+catStr].GetBinContent(ibin))
						htop['pdfNewDown'+catStr].SetBinContent(ibin,htop['pdf'+str(indTopPDFDn)+'_'+catStr].GetBinContent(ibin))
						hewk['pdfNewUp'+catStr].SetBinContent(ibin,hewk['pdf'+str(indEwkPDFUp)+'_'+catStr].GetBinContent(ibin))
						hewk['pdfNewDown'+catStr].SetBinContent(ibin,hewk['pdf'+str(indEwkPDFDn)+'_'+catStr].GetBinContent(ibin))
						hqcd['pdfNewUp'+catStr].SetBinContent(ibin,hqcd['pdf'+str(indQcdPDFUp)+'_'+catStr].GetBinContent(ibin))
						hqcd['pdfNewDown'+catStr].SetBinContent(ibin,hqcd['pdf'+str(indQcdPDFDn)+'_'+catStr].GetBinContent(ibin))
						hsig['pdfNewUp'+catStr].SetBinContent(ibin,hsig['pdf'+str(indSigPDFUp)+'_'+catStr].GetBinContent(ibin))
						hsig['pdfNewDown'+catStr].SetBinContent(ibin,hsig['pdf'+str(indSigPDFDn)+'_'+catStr].GetBinContent(ibin))
						
				if doQ2sys:
					htop['q2Up'+catStr] = bkghists[histoPrefix+'_'+q2UpList[0]].Clone(histoPrefix+'__top__q2__plus')
					htop['q2Down'+catStr] = bkghists[histoPrefix+'_'+q2DownList[0]].Clone(histoPrefix+'__top__q2__minus')
					for ind in range(1,len(q2UpList)):
						htop['q2Up'+catStr].Add(bkghists[histoPrefix+'_'+q2UpList[ind]])
						htop['q2Down'+catStr].Add(bkghists[histoPrefix+'_'+q2DownList[ind]])
			
				#Group data processes
				hdata[catStr] = datahists[histoPrefix+'_'+dataList[0]].Clone(histoPrefix+'__DATA')
				for dat in dataList:
					if dat!=dataList[0]: hdata[catStr].Add(datahists[histoPrefix+'_'+dat])

				#prepare yield table
				yieldTable[histoPrefix]['top']    = htop[catStr].Integral()
				yieldTable[histoPrefix]['ewk']    = hewk[catStr].Integral()
				yieldTable[histoPrefix]['qcd']    = hqcd[catStr].Integral()
				yieldTable[histoPrefix]['totBkg'] = htop[catStr].Integral()+hewk[catStr].Integral()+hqcd[catStr].Integral()
				yieldTable[histoPrefix]['data']   = hdata[catStr].Integral()
				yieldTable[histoPrefix]['dataOverBkg']= yieldTable[histoPrefix]['data']/yieldTable[histoPrefix]['totBkg']
				yieldTable[histoPrefix]['WJets']  = hwjets[catStr].Integral()
				yieldTable[histoPrefix]['ZJets']  = hzjets[catStr].Integral()
				yieldTable[histoPrefix]['VV']     = hvv[catStr].Integral()
				yieldTable[histoPrefix]['TTW']    = httw[catStr].Integral()
				yieldTable[histoPrefix]['TTZ']    = httz[catStr].Integral()
				yieldTable[histoPrefix]['TTJets'] = httjets[catStr].Integral()
				yieldTable[histoPrefix]['T']      = ht[catStr].Integral()
				yieldTable[histoPrefix]['QCD']    = hqcd[catStr].Integral()
				yieldTable[histoPrefix][signal]   = hsig[catStr].Integral()
			
				#+/- 1sigma variations of shape systematics
				if doAllSys:
					for systematic in systematicList:
						for ud in ['Up','Down']:
							yieldTable[histoPrefix+systematic+ud]['top']    = htop[systematic+ud+catStr].Integral()
							if systematic!='toppt':
								yieldTable[histoPrefix+systematic+ud]['ewk']    = hewk[systematic+ud+catStr].Integral()
								yieldTable[histoPrefix+systematic+ud]['qcd']    = hqcd[systematic+ud+catStr].Integral()
								yieldTable[histoPrefix+systematic+ud]['totBkg'] = htop[systematic+ud+catStr].Integral()+hewk[systematic+ud+catStr].Integral()+hqcd[systematic+ud+catStr].Integral()
								yieldTable[histoPrefix+systematic+ud][signal]   = hsig[systematic+ud+catStr].Integral()
						
				if doQ2sys:
					yieldTable[histoPrefix+'q2Up']['top']    = htop['q2Up'+catStr].Integral()
					yieldTable[histoPrefix+'q2Down']['top']    = htop['q2Down'+catStr].Integral()

				#prepare MC yield error table
				yieldStatErrTable[histoPrefix]['top']    = 0.
				yieldStatErrTable[histoPrefix]['ewk']    = 0.
				yieldStatErrTable[histoPrefix]['qcd']    = 0.
				yieldStatErrTable[histoPrefix]['totBkg'] = 0.
				yieldStatErrTable[histoPrefix]['data']   = 0.
				yieldStatErrTable[histoPrefix]['dataOverBkg']= 0.
				yieldStatErrTable[histoPrefix]['WJets']  = 0.
				yieldStatErrTable[histoPrefix]['ZJets']  = 0.
				yieldStatErrTable[histoPrefix]['VV']     = 0.
				yieldStatErrTable[histoPrefix]['TTW']    = 0.
				yieldStatErrTable[histoPrefix]['TTZ']    = 0.
				yieldStatErrTable[histoPrefix]['TTJets'] = 0.
				yieldStatErrTable[histoPrefix]['T']      = 0.
				yieldStatErrTable[histoPrefix]['QCD']    = 0.
				yieldStatErrTable[histoPrefix][signal]   = 0.

				for ibin in range(1,hsig[catStr].GetXaxis().GetNbins()+1):
					yieldStatErrTable[histoPrefix]['top']    += htop[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['ewk']    += hewk[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['qcd']    += hqcd[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['totBkg'] += htop[catStr].GetBinError(ibin)**2+hewk[catStr].GetBinError(ibin)**2+hqcd[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['data']   += hdata[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['WJets']  += hwjets[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['ZJets']  += hzjets[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['VV']     += hvv[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['TTW']    += httw[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['TTZ']    += httz[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['TTJets'] += httjets[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['T']      += ht[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['QCD']    += hqcd[catStr].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix][signal]   += hsig[catStr].GetBinError(ibin)**2

				#scale signal cross section to 1pb
				if scaleSignalXsecTo1pb: hsig[catStr].Scale(1./xsec[signal])
				BRcoeff = 1.
				if decay[:2]!=decay[2:]: BRcoeff = 2.
				hsig[catStr].Scale(1./(BRcoeff*BR[decay[:2]]*BR[decay[2:]]))
				#write theta histograms in root file, avoid having processes with no event yield (to make theta happy) 
				if hsig[catStr].Integral() > 0:  
					hsig[catStr].Write()
					if doAllSys:
						for systematic in systematicList:
							if systematic=='toppt': continue
							if scaleSignalXsecTo1pb: 
								hsig[systematic+'Up'+catStr].Scale(1./xsec[signal])
								hsig[systematic+'Down'+catStr].Scale(1./xsec[signal])
							hsig[systematic+'Up'+catStr].Scale(1./(BRcoeff*BR[decay[:2]]*BR[decay[2:]]))
							hsig[systematic+'Down'+catStr].Scale(1./(BRcoeff*BR[decay[:2]]*BR[decay[2:]]))
							if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
								hsig[systematic+'Up'+catStr].Scale(hsig[catStr].Integral()/hsig[systematic+'Up'+catStr].Integral())
								hsig[systematic+'Down'+catStr].Scale(hsig[catStr].Integral()/hsig[systematic+'Down'+catStr].Integral())
							hsig[systematic+'Up'+catStr].Write()
							hsig[systematic+'Down'+catStr].Write()
						for pdfInd in range(100): hsig['pdf'+str(pdfInd)+'_'+catStr].Write()
				if htop[catStr].Integral() > 0:  
					htop[catStr].Write()
					if doAllSys:
						for systematic in systematicList:
							if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
								htop[systematic+'Up'+catStr].Scale(htop[catStr].Integral()/htop[systematic+'Up'+catStr].Integral())
								htop[systematic+'Down'+catStr].Scale(htop[catStr].Integral()/htop[systematic+'Down'+catStr].Integral())  
							htop[systematic+'Up'+catStr].Write()
							htop[systematic+'Down'+catStr].Write()
						for pdfInd in range(100): htop['pdf'+str(pdfInd)+'_'+catStr].Write()
					if doQ2sys:
						htop['q2Up'+catStr].Write()
						htop['q2Down'+catStr].Write()
				if hewk[catStr].Integral() > 0:  
					hewk[catStr].Write()
					if doAllSys:
						for systematic in systematicList:
							if systematic=='toppt': continue
							if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
								hewk[systematic+'Up'+catStr].Scale(hewk[catStr].Integral()/hewk[systematic+'Up'+catStr].Integral())
								hewk[systematic+'Down'+catStr].Scale(hewk[catStr].Integral()/hewk[systematic+'Down'+catStr].Integral()) 
							hewk[systematic+'Up'+catStr].Write()
							hewk[systematic+'Down'+catStr].Write()
						for pdfInd in range(100): hewk['pdf'+str(pdfInd)+'_'+catStr].Write()
				if hqcd[catStr].Integral() > 0:  
					hqcd[catStr].Write()
					if doAllSys:
						for systematic in systematicList:
							if systematic == 'pdf' or systematic == 'pdfNew' or systematic == 'muR' or systematic == 'muF' or systematic == 'muRFcorrd' or systematic=='toppt': continue
							hqcd[systematic+'Up'+catStr].Write()
							hqcd[systematic+'Down'+catStr].Write()
						for pdfInd in range(100): hqcd['pdf'+str(pdfInd)+'_'+catStr].Write()
				hdata[catStr].Write()
				i+=1
			outputRfile.Close()
	
		stdout_old = sys.stdout
		logFile = open(outDir+'/yields_'+discriminant+'_'+lumiStr+'fb_'+decay+'.txt','a')
		sys.stdout = logFile

		## PRINTING YIELD TABLE WITH STATISTICAL UNCERTAINTIES ##
		#first print table without background grouping
		ljust_i = 1
		print 'CUTS:',cutString
		print
		print 'YIELDS'.ljust(20*ljust_i), 
		for bkg in bkgStackList: print bkg.ljust(ljust_i),
		print 'data'.ljust(ljust_i),
		print
		for cat in catList:
			tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr = 'is'+cat[0]+'_'+tagStr
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
			print (catStr).ljust(ljust_i),
			for bkg in bkgStackList:
				print str(yieldTable[histoPrefix][bkg]).ljust(ljust_i),
			print str(yieldTable[histoPrefix]['data']).ljust(ljust_i),
			print

		print 'YIELDS ERRORS'
		for cat in catList:
			tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr = 'is'+cat[0]+'_'+tagStr
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
			print (catStr).ljust(ljust_i),
			for bkg in bkgStackList:
				print str(math.sqrt(yieldStatErrTable[histoPrefix][bkg])).ljust(ljust_i),
			print str(math.sqrt(yieldStatErrTable[histoPrefix]['data'])).ljust(ljust_i),
			print

		#now print with top,ewk,qcd grouping
		print
		print 'YIELDS'.ljust(20*ljust_i), 
		print 'ewk'.ljust(ljust_i),
		print 'top'.ljust(ljust_i),
		print 'qcd'.ljust(ljust_i),
		print 'data'.ljust(ljust_i),
		print
		for cat in catList:
			tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr = 'is'+cat[0]+'_'+tagStr
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
			print (catStr).ljust(ljust_i),
			print str(yieldTable[histoPrefix]['ewk']).ljust(ljust_i),
			print str(yieldTable[histoPrefix]['top']).ljust(ljust_i),
			print str(yieldTable[histoPrefix]['qcd']).ljust(ljust_i),
			print str(yieldTable[histoPrefix]['data']).ljust(ljust_i),
			print

		print 'YIELDS ERRORS'
		for cat in catList:
			tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr = 'is'+cat[0]+'_'+tagStr
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
			print (catStr).ljust(ljust_i),
			print str(math.sqrt(yieldStatErrTable[histoPrefix]['ewk'])).ljust(ljust_i),
			print str(math.sqrt(yieldStatErrTable[histoPrefix]['top'])).ljust(ljust_i),
			print str(math.sqrt(yieldStatErrTable[histoPrefix]['qcd'])).ljust(ljust_i),
			print str(math.sqrt(yieldStatErrTable[histoPrefix]['data'])).ljust(ljust_i),
			print

		#print yields for signals
		print
		print 'YIELDS'.ljust(20*ljust_i), 
		for sig in sigList: print sig.ljust(ljust_i),
		print
		for cat in catList:
			tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr = 'is'+cat[0]+'_'+tagStr
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
			print (catStr).ljust(ljust_i),
			for sig in sigList:
				print str(yieldTable[histoPrefix][sig]).ljust(ljust_i),
			print

		print 'YIELDS ERRORS'
		for cat in catList:
			tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr = 'is'+cat[0]+'_'+tagStr
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
			print (catStr).ljust(ljust_i),
			for sig in sigList:
				print str(math.sqrt(yieldStatErrTable[histoPrefix][sig])).ljust(ljust_i),
			print
				
		#print for AN tables
		print
		print "FOR AN (errors are statistical+normalization systematics): "
		print
		print 'YIELDS ELECTRON+JETS'.ljust(20*ljust_i), 
		for cat in catList:
			tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr = 'is'+cat[0]+'_'+tagStr
			if cat[0]!='E': continue
			print (catStr).ljust(ljust_i),
		print
		for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
			print process.ljust(ljust_i),
			for cat in catList:
				tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
				catStr = 'is'+cat[0]+'_'+tagStr
				if cat[0]!='E': continue
				histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
				if process=='dataOverBkg':
					dataTemp = yieldTable[histoPrefix]['data']+1e-20
					dataTempErr = yieldStatErrTable[histoPrefix]['data']
					totBkgTemp = yieldTable[histoPrefix]['totBkg']+1e-20
					totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg'] # statistical error squared
					totBkgTempErr += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
					totBkgTempErr += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
					totBkgTempErr += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
					totBkgTempErr += (corrdSys*totBkgTemp)**2
					dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
					print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
				else:
					yieldtemp = yieldTable[histoPrefix][process]
					yielderrtemp = yieldStatErrTable[histoPrefix][process]
					if process=='totBkg': 
						yielderrtemp += (corrdSys*yieldtemp)**2
						yielderrtemp += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
						yielderrtemp += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
						yielderrtemp += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
					elif process in sigList: 
						yielderrtemp += (corrdSys*yieldtemp)**2
					elif process!='data': 
						yielderrtemp += (corrdSys*yieldtemp)**2
						yielderrtemp += (addSys[process+'_'+tagStr]*yieldTable[histoPrefix][process])**2
					if process=='data': print ' & '+str(int(yieldtemp)),
					elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
					else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
			print '\\\\',
			print
		print
		print 'YIELDS MUON+JETS'.ljust(20*ljust_i), 
		for cat in catList:
			tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
			catStr = 'is'+cat[0]+'_'+tagStr
			if cat[0]!='M': continue
			print (catStr).ljust(ljust_i),
		print
		for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
			print process.ljust(ljust_i),
			for cat in catList:
				tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
				catStr = 'is'+cat[0]+'_'+tagStr
				if cat[0]!='M': continue
				histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
				if process=='dataOverBkg':
					dataTemp = yieldTable[histoPrefix]['data']+1e-20
					dataTempErr = yieldStatErrTable[histoPrefix]['data']
					totBkgTemp = yieldTable[histoPrefix]['totBkg']+1e-20
					totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg'] # statistical error squared
					totBkgTempErr += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
					totBkgTempErr += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
					totBkgTempErr += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
					totBkgTempErr += (corrdSys*totBkgTemp)**2
					dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
					print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
				else:
					yieldtemp = yieldTable[histoPrefix][process]
					yielderrtemp = yieldStatErrTable[histoPrefix][process]
					if process=='totBkg': 
						yielderrtemp += (corrdSys*yieldtemp)**2
						yielderrtemp += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
						yielderrtemp += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
						yielderrtemp += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
					elif process in sigList: 
						yielderrtemp += (corrdSys*yieldtemp)**2
					elif process!='data': 
						yielderrtemp += (corrdSys*yieldtemp)**2
						yielderrtemp += (addSys[process+'_'+tagStr]*yieldTable[histoPrefix][process])**2
					if process=='data': print ' & '+str(int(yieldtemp)),
					elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
					else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
			print '\\\\',
			print
		
		#print for AN tables systematics
		if doAllSys:
			print
			print "FOR AN (shape systematic percentaces): "
			print
			print 'YIELDS'.ljust(20*ljust_i), 
			for cat in catList:
				tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
				catStr = 'is'+cat[0]+'_'+tagStr
				print (catStr).ljust(ljust_i),
			print
			for process in ['ewk','top']+sigList:
				print process.ljust(ljust_i),
				print
				for ud in ['Up','Down']:
					for systematic in systematicList:
						if systematic=='toppt' and process!='top': continue
						print (systematic+ud).ljust(ljust_i),
						for cat in catList:
							tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
							catStr = 'is'+cat[0]+'_'+tagStr
							histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
							print ' & '+str(round_sig(yieldTable[histoPrefix+systematic+ud][process]/(yieldTable[histoPrefix][process]+1e-20),2)),
						print '\\\\',
						print
					if process!='top': continue
					print ('q2'+ud).ljust(ljust_i),
					for cat in catList:
						tagStr = 'nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
						catStr = 'is'+cat[0]+'_'+tagStr
						histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
						print ' & '+str(round_sig(yieldTable[histoPrefix+'q2'+ud][process]/(yieldTable[histoPrefix][process]+1e-20),2)),
					print '\\\\',
					print
		
		print
		print "FOR PAS (errors are statistical+normalization systematics): " #combines e/m channels
		print
		print 'YIELDS'.ljust(20*ljust_i), 
		for tag in tagList:
			tagStr = 'nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]
			print (tagStr).ljust(ljust_i),
		print
		for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
			print process.ljust(ljust_i),
			for tag in tagList:
				tagStr = 'nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]
				histoPrefix=discriminant+'_'+lumiStr+'fb_isE'+'_'+tagStr
				if process=='dataOverBkg':
					dataTemp = yieldTable[histoPrefix]['data']+yieldTable[histoPrefix.replace('_isE','_isM')]['data']+1e-20
					dataTempErr = yieldStatErrTable[histoPrefix]['data']+yieldStatErrTable[histoPrefix.replace('_isE','_isM')]['data']
					totBkgTemp = yieldTable[histoPrefix]['totBkg']+yieldTable[histoPrefix.replace('_isE','_isM')]['totBkg']+1e-20
					totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg']+yieldStatErrTable[histoPrefix.replace('_isE','_isM')]['totBkg'] # statistical error squared
					totBkgTempErr += (addSys['top_'+tagStr]*(yieldTable[histoPrefix]['top']+yieldTable[histoPrefix.replace('_isE','_isM')]['top']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					totBkgTempErr += (addSys['ewk_'+tagStr]*(yieldTable[histoPrefix]['ewk']+yieldTable[histoPrefix.replace('_isE','_isM')]['ewk']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					totBkgTempErr += (addSys['qcd_'+tagStr]*(yieldTable[histoPrefix]['qcd']+yieldTable[histoPrefix.replace('_isE','_isM')]['qcd']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					totBkgTempErr += (corrdSys*totBkgTemp)**2
					dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
					print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
				else:
					yieldtemp = yieldTable[histoPrefix][process]+yieldTable[histoPrefix.replace('_isE','_isM')][process]
					yielderrtemp = yieldStatErrTable[histoPrefix][process]++yieldStatErrTable[histoPrefix.replace('_isE','_isM')][process]
					if process=='totBkg': 
						yielderrtemp += (corrdSys*yieldtemp)**2
						yielderrtemp += (addSys['top_'+tagStr]*(yieldTable[histoPrefix]['top']+yieldTable[histoPrefix.replace('_isE','_isM')]['top']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						yielderrtemp += (addSys['ewk_'+tagStr]*(yieldTable[histoPrefix]['ewk']+yieldTable[histoPrefix.replace('_isE','_isM')]['ewk']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						yielderrtemp += (addSys['qcd_'+tagStr]*(yieldTable[histoPrefix]['qcd']+yieldTable[histoPrefix.replace('_isE','_isM')]['qcd']))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					elif process in sigList: 
						yielderrtemp += (corrdSys*yieldtemp)**2
					elif process!='data': 
						yielderrtemp += (corrdSys*yieldtemp)**2
						yielderrtemp += (addSys[process+'_'+tagStr]*(yieldTable[histoPrefix][process]+yieldTable[histoPrefix.replace('_isE','_isM')][process]))**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					if process=='data': print ' & '+str(int(yieldtemp)),
					elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
					else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
			print '\\\\',
			print
		
		sys.stdout = stdout_old
		logFile.close()

datahists = {}
bkghists  = {}
sighists  = {}
for cat in catList:
	catStr = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
	print "LOADING: ",catStr
	datahists.update(pickle.load(open(outDir+'/'+catStr+'/datahists.p','rb')))
	bkghists.update(pickle.load(open(outDir+'/'+catStr+'/bkghists.p','rb')))
	sighists.update(pickle.load(open(outDir+'/'+catStr+'/sighists.p','rb')))
if scaleLumi:
	for key in bkghists.keys(): bkghists[key].Scale(lumiScaleCoeff)
	for key in sighists.keys(): sighists[key].Scale(lumiScaleCoeff)

print "MAKING CATEGORIES FOR TOTAL SIGNALS ..."
makeThetaCats(datahists,sighists,bkghists,iPlot)
# print "MAKING CATEGORIES FOR DECAY CHANNELS ..."
# if len(decays)>1: makeThetaCatsIndDecays(datahists,sighists,bkghists,iPlot)

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


