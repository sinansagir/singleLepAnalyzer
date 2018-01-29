#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools,getopt
from ROOT import TH1D,gROOT,TFile,TTree
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from numpy import linspace
from weights import *
from analyzeOptim import *
from samples import *

gROOT.SetBatch(1)
start_time = time.time()

"""
Note: 
--Each process in step1 (or step2) directories should have the root files hadded! 
--The code will look for <step1Dir>/<process>_hadd.root for nominal trees.
The uncertainty shape shifted files will be taken from <step1Dir>/../<shape>/<process>_hadd.root,
where <shape> is for example "JECUp". hadder.py can be used to prepare input files this way! 
--Each process given in the lists below must have a definition in "samples.py"
--Check the set of cuts in "analyze.py"
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
step1Dir = '/user_data/jhogan/LJMet80X_1lepTT_030217_step2slimmed/nominal'

region = 'SR' #no need to change
isotrig = 1
doJetRwt = 0
iPlot='minMlbST'
scaleSignalXsecTo1pb = True # this has to be "True" if you are making templates for limit calculation!!!!!!!!
scaleLumi = True
lumiScaleCoeff = 35867./36814.
doAllSys = True
doQ2sys = False
if not doAllSys: doQ2sys = False
systematicList = ['muRFcorrd']#'pileup','jec','jer','btag','tau21','mistag','muR','muF','muRFcorrd','toppt','jsf','topsf','trigeff']
normalizeRENORM_PDF = False #normalize the renormalization/pdf uncertainties to nominal templates --> normalizes both the background and signal processes !!!!

bkgList = [
	'DYMG',
	'WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500',
	'WW','WZ','ZZ',
	'TTJetsPH0to700inc','TTJetsPH700to1000inc','TTJetsPH1000toINFinc',
	'TTJetsPH700mtt','TTJetsPH1000mtt',
	'Tt','Tbt','Ts','TtW','TbtW',
	'QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000',
	]

dataList = ['DataERRBCDEFGH','DataMRRBCDEFGH']
q2List  = [#energy scale sample to be processed
	       #'TTJetsPHQ2U','TTJetsPHQ2D',
	       #'TtWQ2U','TbtWQ2U',
	       #'TtWQ2D','TbtWQ2D',
	       ]
			       
bkgStackList = ['ZJets','VV','T','QCD','WJets','TTJets']
wjetList  = ['WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500'] 
zjetList  = ['DYMG']
ttwList = []
ttzList = []
vvList    = ['WW','WZ','ZZ']
ttjetList = ['TTJetsPH0to700inc','TTJetsPH700to1000inc','TTJetsPH1000toINFinc','TTJetsPH700mtt','TTJetsPH1000mtt']
tList     = ['Tt','Tbt','Ts','TtW','TbtW']

topList = ttjetList+tList
ewkList = wjetList+vvList
qcdList = ['QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000']#'QCDht100',

q2UpList   = tList+ttjetList#['TTJetsPHQ2U']#,'TtWQ2U','TbtWQ2U']
q2DownList = tList+ttjetList#['TTJetsPHQ2D']#,'TtWQ2D','TbtWQ2D']

whichSignal = 'TT' #HTB, TT, BB, or X53X53
massList = range(800,1800+1,100)
sigList = [whichSignal+'M'+str(mass) for mass in massList]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in massList for chiral in ['left','right']]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
if whichSignal=='X53X53': decays = [''] #decays to tWtW 100% of the time
if whichSignal=='HTB': decays = ['']

doBRScan = False
BRs={}
BRs['BW']=[0.0,0.50,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
BRs['TH']=[0.5,0.25,0.0,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]
BRs['TZ']=[0.5,0.25,1.0,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
nBRconf=len(BRs['BW'])
if not doBRScan: nBRconf=1

lepPtCut=60
metCut=75
njetsCut=3
nbjetsCut=0
drCut=3.0
jet1PtCut=300
jet2PtCut=150
jet3PtCut=100
jet4PtCut=0
jet5PtCut=0
Wjet1PtCut=0
bjet1PtCut=0
htCut=0
stCut=0
minMlbCut=0

isEMlist =['E','M']
nHtaglist=['0','1b','2b']
nWtaglist=['0','0p','1p']
nbtaglist=['0','1','1p','2','3p']
allcats = list(itertools.product(isEMlist,nHtaglist,nWtaglist,nbtaglist))
tagList = []
catList = [cat for cat in allcats if ((cat[1] == '0' and cat[2] != '0p' and cat[3] != '1p') or ('b' in cat[1] and cat[2] == '0p' and cat[3] == '1p'))]

print catList

try: 
	opts, args = getopt.getopt(sys.argv[2:], "", ["lepPtCut=",
	                                              "jet1PtCut=",
	                                              "jet2PtCut=",
	                                              "jet3PtCut=",
	                                              "jet4PtCut=",
	                                              "jet5PtCut=",
	                                              "metCut=",
	                                              "njetsCut=",
	                                              "nbjetsCut=",
	                                              "drCut=",
	                                              "Wjet1PtCut=",
	                                              "bjet1PtCut=",
	                                              "htCut=",
	                                              "stCut=",
	                                              "minMlbCut=",
	                                              ])
	print opts,args
except getopt.GetoptError as err:
	print str(err)
	sys.exit(1)

for o, a in opts:
	print o, a
	if o == '--lepPtCut': lepPtCut = float(a)
	if o == '--metCut': metCut = float(a)
	if o == '--njetsCut': njetsCut = float(a)
	if o == '--nbjetsCut': nbjetsCut = float(a)
	if o == '--drCut': drCut = float(a)
	if o == '--jet1PtCut': jet1PtCut = float(a)
	if o == '--jet2PtCut': jet2PtCut = float(a)
	if o == '--jet3PtCut': jet3PtCut = float(a)
	if o == '--jet4PtCut': jet4PtCut = float(a)
	if o == '--jet5PtCut': jet5PtCut = float(a)
	if o == '--Wjet1PtCut': Wjet1PtCut = float(a)
	if o == '--bjet1PtCut': bjet1PtCut = float(a)
	if o == '--htCut': htCut = float(a)
	if o == '--stCut': stCut = float(a)
	if o == '--minMlbCut': minMlbCut = float(a)

cutList = {'lepPtCut':lepPtCut,
		   'metCut':metCut,
		   'njetsCut':njetsCut,
		   'nbjetsCut':nbjetsCut,
		   'drCut':drCut,
		   'jet1PtCut':jet1PtCut,
		   'jet2PtCut':jet2PtCut,
		   'jet3PtCut':jet3PtCut,
		   'jet4PtCut':jet4PtCut,
		   'jet5PtCut':jet5PtCut,
		   'Wjet1PtCut':Wjet1PtCut,
		   'bjet1PtCut':bjet1PtCut,
		   'htCut':htCut,
		   'stCut':stCut,
		   'minMlbCut':minMlbCut,
		   }

cutString  = 'MET'+str(int(cutList['metCut']))+'_1jet'+str(int(cutList['jet1PtCut']))
cutString += '_2jet'+str(int(cutList['jet2PtCut']))+'_3jet'+str(int(cutList['jet3PtCut']))

cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='templates_OpTest'
#pfix+=datestr+'_'+timestr

if len(sys.argv)>1: outDir=sys.argv[1]
else: 
	outDir = os.getcwd()+'/'
	outDir+=pfix
	if not os.path.exists(outDir): os.system('mkdir '+outDir)
	if not os.path.exists(outDir+'/'+cutString): os.system('mkdir '+outDir+'/'+cutString)
	outDir+='/'+cutString

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

lumiSys = 0.026 #2.7% lumi uncertainty
eltrigSys = 0.05 #5% trigger uncertainty
mutrigSys = 0.05 #5% trigger uncertainty
elIdSys = 0.02 #1% lepton id uncertainty
muIdSys = 0.03 #1% lepton id uncertainty
elIsoSys = 0.01 #1% lepton isolation uncertainty
muIsoSys = 0.01 #1% lepton isolation uncertainty
elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)


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
		tagStr = 'nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ3p'
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
	for BRind in range(nBRconf):
		BRconfStr=''
		if doBRScan: BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
		print "       BR Configuration:"+BRconfStr
		for signal in sigList:
			outputRfileName = outDir+'/templates_'+discriminant+'_'+signal+BRconfStr+'_'+lumiStr+'fb'+'.root'
			outputRfile = TFile(outputRfileName,'RECREATE')
			hsig,htop,hewk,hqcd,hdata={},{},{},{},{}
			hwjets,hzjets,httjets,ht,httw,httz,hvv={},{},{},{},{},{},{}
			for cat in catList:
				tagStr = 'nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ3p'
				catStr = 'is'+cat[0]+'_'+tagStr
				histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr

				#Group processes
				hwjets[i] = bkghists[histoPrefix+'_'+wjetList[0]].Clone(histoPrefix+'_WJets')
				hzjets[i] = bkghists[histoPrefix+'_'+zjetList[0]].Clone(histoPrefix+'_ZJets')
				httjets[i] = bkghists[histoPrefix+'_'+ttjetList[0]].Clone(histoPrefix+'_TTJets')
				ht[i] = bkghists[histoPrefix+'_'+tList[0]].Clone(histoPrefix+'_T')
				#httw[i] = bkghists[histoPrefix+'_'+ttwList[0]].Clone(histoPrefix+'_TTW')
				#httz[i] = bkghists[histoPrefix+'_'+ttzList[0]].Clone(histoPrefix+'_TTZ')
				hvv[i] = bkghists[histoPrefix+'_'+vvList[0]].Clone(histoPrefix+'_VV')
				for bkg in ttjetList:
					if bkg!=ttjetList[0]: httjets[i].Add(bkghists[histoPrefix+'_'+bkg])
				for bkg in wjetList:
					if bkg!=wjetList[0]: hwjets[i].Add(bkghists[histoPrefix+'_'+bkg])
				# for bkg in ttwList:
				# 	if bkg!=ttwList[0]: httw[i].Add(bkghists[histoPrefix+'_'+bkg])
				# for bkg in ttzList:
				# 	if bkg!=ttzList[0]: httz[i].Add(bkghists[histoPrefix+'_'+bkg])
				for bkg in tList:
					if bkg!=tList[0]: ht[i].Add(bkghists[histoPrefix+'_'+bkg])
				for bkg in zjetList:
					if bkg!=zjetList[0]: hzjets[i].Add(bkghists[histoPrefix+'_'+bkg])
				for bkg in vvList:
					if bkg!=vvList[0]: hvv[i].Add(bkghists[histoPrefix+'_'+bkg])
		
				#Group QCD processes
				hqcd[i] = bkghists[histoPrefix+'_'+qcdList[0]].Clone(histoPrefix+'__qcd')
				for bkg in qcdList: 
					if bkg!=qcdList[0]: 
						hqcd[i].Add(bkghists[histoPrefix+'_'+bkg])
		
				#Group EWK processes
				hewk[i] = bkghists[histoPrefix+'_'+ewkList[0]].Clone(histoPrefix+'__ewk')
				for bkg in ewkList:
					if bkg!=ewkList[0]: hewk[i].Add(bkghists[histoPrefix+'_'+bkg])
		
				#Group TOP processes
				htop[i] = bkghists[histoPrefix+'_'+topList[0]].Clone(histoPrefix+'__top')
				for bkg in topList:
					if bkg!=topList[0]: htop[i].Add(bkghists[histoPrefix+'_'+bkg])
		
				#get signal
				hsig[i] = sighists[histoPrefix+'_'+signal+decays[0]].Clone(histoPrefix+'__sig')
				if doBRScan: hsig[i].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
				for decay in decays:
					if decay!=decays[0]:
						htemp = sighists[histoPrefix+'_'+signal+decay].Clone()
						if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
						hsig[i].Add(htemp)

				#systematics
				if doAllSys:
					for systematic in systematicList:
						for ud in ['Up','Down']:
							if systematic!='toppt':
								hqcd[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
								hewk[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
								htop[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+topList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
								hsig[systematic+ud+str(i)] = sighists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
								if doBRScan: hsig[systematic+ud+str(i)].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
								for bkg in qcdList: 
									if bkg!=qcdList[0]: hqcd[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
								for bkg in ewkList: 
									if bkg!=ewkList[0]: hewk[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
								for bkg in topList: 
									if bkg!=topList[0]: htop[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
								for decay in decays:
									htemp = sighists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+signal+decay].Clone()
									if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
									if decay!=decays[0]: hsig[systematic+ud+str(i)].Add(htemp)
							if systematic=='toppt': # top pt is only on the ttbar sample, so it needs special treatment!
								htop[systematic+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+ttjetList[0]].Clone(histoPrefix+'__top__'+systematic+'__'+ud.replace('Up','plus').replace('Down','minus'))
								for bkg in ttjetList: 
									if bkg!=ttjetList[0]: htop[systematic+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+systematic+ud)+'_'+bkg])
								for bkg in topList: 
									if bkg not in ttjetList: htop[systematic+ud+str(i)].Add(bkghists[histoPrefix+'_'+bkg])
					# for pdfInd in range(100):
					# 	hqcd['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__pdf'+str(pdfInd))
					# 	hewk['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__pdf'+str(pdfInd))
					# 	htop['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+topList[0]].Clone(histoPrefix+'__top__pdf'+str(pdfInd))
					# 	hsig['pdf'+str(pdfInd)+'_'+str(i)] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__pdf'+str(pdfInd))
					# 	if doBRScan: hsig['pdf'+str(pdfInd)+'_'+str(i)].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
					# 	for bkg in qcdList: 
					# 		if bkg!=qcdList[0]: hqcd['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					# 	for bkg in ewkList: 
					# 		if bkg!=ewkList[0]: hewk['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					# 	for bkg in topList: 
					# 		if bkg!=topList[0]: htop['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					# 	for decay in decays:
					# 		htemp = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decay].Clone()
					# 		if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
					# 		if decay!=decays[0]:hsig['pdf'+str(pdfInd)+'_'+str(i)].Add(htemp)
												
				if doQ2sys:
					htop['q2Up'+str(i)] = bkghists[histoPrefix+'_'+q2UpList[0]].Clone(histoPrefix+'__top__q2__plus')
					htop['q2Down'+str(i)] = bkghists[histoPrefix+'_'+q2DownList[0]].Clone(histoPrefix+'__top__q2__minus')
					for ind in range(1,len(q2UpList)):
						htop['q2Up'+str(i)].Add(bkghists[histoPrefix+'_'+q2UpList[ind]])
						htop['q2Down'+str(i)].Add(bkghists[histoPrefix+'_'+q2DownList[ind]])
		
				#Group data processes
				hdata[i] = datahists[histoPrefix+'_'+dataList[0]].Clone(histoPrefix+'__DATA')
				for dat in dataList:
					if dat!=dataList[0]: hdata[i].Add(datahists[histoPrefix+'_'+dat])

				#prepare yield table
				yieldTable[histoPrefix]['top']    = htop[i].Integral()
				yieldTable[histoPrefix]['ewk']    = hewk[i].Integral()
				yieldTable[histoPrefix]['qcd']    = hqcd[i].Integral()
				yieldTable[histoPrefix]['totBkg'] = htop[i].Integral()+hewk[i].Integral()+hqcd[i].Integral()
				yieldTable[histoPrefix]['data']   = hdata[i].Integral()
				yieldTable[histoPrefix]['dataOverBkg']= yieldTable[histoPrefix]['data']/yieldTable[histoPrefix]['totBkg']
				yieldTable[histoPrefix]['WJets']  = hwjets[i].Integral()
				yieldTable[histoPrefix]['ZJets']  = hzjets[i].Integral()
				yieldTable[histoPrefix]['VV']     = hvv[i].Integral()
				# yieldTable[histoPrefix]['TTW']    = httw[i].Integral()
				# yieldTable[histoPrefix]['TTZ']    = httz[i].Integral()
				yieldTable[histoPrefix]['TTJets'] = httjets[i].Integral()
				yieldTable[histoPrefix]['T']      = ht[i].Integral()
				yieldTable[histoPrefix]['QCD']    = hqcd[i].Integral()
				yieldTable[histoPrefix][signal]   = hsig[i].Integral()
		
				#+/- 1sigma variations of shape systematics
				if doAllSys:
					for systematic in systematicList:
						for ud in ['Up','Down']:
							yieldTable[histoPrefix+systematic+ud]['top']    = htop[systematic+ud+str(i)].Integral()
							if systematic!='toppt':
								yieldTable[histoPrefix+systematic+ud]['ewk']    = hewk[systematic+ud+str(i)].Integral()
								yieldTable[histoPrefix+systematic+ud]['qcd']    = hqcd[systematic+ud+str(i)].Integral()
								yieldTable[histoPrefix+systematic+ud]['totBkg'] = htop[systematic+ud+str(i)].Integral()+hewk[systematic+ud+str(i)].Integral()+hqcd[systematic+ud+str(i)].Integral()
								yieldTable[histoPrefix+systematic+ud][signal]   = hsig[systematic+ud+str(i)].Integral()
					
				if doQ2sys:
					yieldTable[histoPrefix+'q2Up']['top']    = htop['q2Up'+str(i)].Integral()
					yieldTable[histoPrefix+'q2Down']['top']    = htop['q2Down'+str(i)].Integral()

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
				# yieldStatErrTable[histoPrefix]['TTW']    = 0.
				# yieldStatErrTable[histoPrefix]['TTZ']    = 0.
				yieldStatErrTable[histoPrefix]['TTJets'] = 0.
				yieldStatErrTable[histoPrefix]['T']      = 0.
				yieldStatErrTable[histoPrefix]['QCD']    = 0.
				yieldStatErrTable[histoPrefix][signal]   = 0.

				for ibin in range(1,hsig[i].GetXaxis().GetNbins()+1):
					yieldStatErrTable[histoPrefix]['top']    += htop[i].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['ewk']    += hewk[i].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['qcd']    += hqcd[i].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['totBkg'] += htop[i].GetBinError(ibin)**2+hewk[i].GetBinError(ibin)**2+hqcd[i].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['data']   += hdata[i].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['WJets']  += hwjets[i].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['ZJets']  += hzjets[i].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['VV']     += hvv[i].GetBinError(ibin)**2
					# yieldStatErrTable[histoPrefix]['TTW']    += httw[i].GetBinError(ibin)**2
					# yieldStatErrTable[histoPrefix]['TTZ']    += httz[i].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['TTJets'] += httjets[i].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['T']      += ht[i].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix]['QCD']    += hqcd[i].GetBinError(ibin)**2
					yieldStatErrTable[histoPrefix][signal]   += hsig[i].GetBinError(ibin)**2

				#scale signal cross section to 1pb
				#write theta histograms in root file, avoid having processes with no event yield (to make theta happy) 
				if hsig[i].Integral() > 0:  
					if scaleSignalXsecTo1pb: hsig[i].Scale(1./xsec[signal])
					hsig[i].Write()
					if doAllSys:
						for systematic in systematicList:
							if systematic=='toppt': continue
							if scaleSignalXsecTo1pb: 
								hsig[systematic+'Up'+str(i)].Scale(1./xsec[signal])
								hsig[systematic+'Down'+str(i)].Scale(1./xsec[signal])
							if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
								hsig[systematic+'Up'+str(i)].Scale(hsig[i].Integral()/hsig[systematic+'Up'+str(i)].Integral())
								hsig[systematic+'Down'+str(i)].Scale(hsig[i].Integral()/hsig[systematic+'Down'+str(i)].Integral())
							hsig[systematic+'Up'+str(i)].Write()
							hsig[systematic+'Down'+str(i)].Write()
						#for pdfInd in range(100): hsig['pdf'+str(pdfInd)+'_'+str(i)].Write()
				if htop[i].Integral() > 0:  
					htop[i].Write()
					if doAllSys:
						for systematic in systematicList:
							# if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
							# 	htop[systematic+'Up'+str(i)].Scale(htop[i].Integral()/htop[systematic+'Up'+str(i)].Integral())
							# 	htop[systematic+'Down'+str(i)].Scale(htop[i].Integral()/htop[systematic+'Down'+str(i)].Integral())  
							htop[systematic+'Up'+str(i)].Write()
							htop[systematic+'Down'+str(i)].Write()
						#for pdfInd in range(100): htop['pdf'+str(pdfInd)+'_'+str(i)].Write()
					if doQ2sys:
						htop['q2Up'+str(i)].Write()
						htop['q2Down'+str(i)].Write()
				if hewk[i].Integral() > 0:  
					hewk[i].Write()
					if doAllSys:
						for systematic in systematicList:
							if systematic=='toppt': continue
							# if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
							# 	hewk[systematic+'Up'+str(i)].Scale(hewk[i].Integral()/hewk[systematic+'Up'+str(i)].Integral())
							# 	hewk[systematic+'Down'+str(i)].Scale(hewk[i].Integral()/hewk[systematic+'Down'+str(i)].Integral()) 
							hewk[systematic+'Up'+str(i)].Write()
							hewk[systematic+'Down'+str(i)].Write()
						#for pdfInd in range(100): hewk['pdf'+str(pdfInd)+'_'+str(i)].Write()
				if hqcd[i].Integral() > 0:  
					hqcd[i].Write()
					if doAllSys:
						for systematic in systematicList:
							if systematic=='toppt': continue
							# if normalizeRENORM_PDF and (systematic.startswith('mu') or systematic=='pdf'):
							# 	hqcd[systematic+'Up'+str(i)].Scale(hqcd[i].Integral()/hqcd[systematic+'Up'+str(i)].Integral())
							# 	hqcd[systematic+'Down'+str(i)].Scale(hqcd[i].Integral()/hqcd[systematic+'Down'+str(i)].Integral()) 
							hqcd[systematic+'Up'+str(i)].Write()
							hqcd[systematic+'Down'+str(i)].Write()
						#for pdfInd in range(100): hqcd['pdf'+str(pdfInd)+'_'+str(i)].Write()
				hdata[i].Write()
				i+=1
			outputRfile.Close()
	
		# stdout_old = sys.stdout
		# logFile = open(outDir+'/yields_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.txt','a')
		# sys.stdout = logFile

		# ## PRINTING YIELD TABLE WITH STATISTICAL UNCERTAINTIES ##
		# #first print table without background grouping
		# ljust_i = 1
		# print 'CUTS:',cutString
		# print
		# print 'YIELDS'.ljust(20*ljust_i), 
		# for bkg in bkgStackList: print bkg.ljust(ljust_i),
		# print 'data'.ljust(ljust_i),
		# print
		# for cat in catList:
		# 	tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 	catStr='is'+cat[0]+'_'+tagStr
		# 	histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		# 	print (catStr).ljust(ljust_i),
		# 	for bkg in bkgStackList:
		# 		print str(yieldTable[histoPrefix][bkg]).ljust(ljust_i),
		# 	print str(yieldTable[histoPrefix]['data']).ljust(ljust_i),
		# 	print

		# print 'YIELDS ERRORS'
		# for cat in catList:
		# 	tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 	catStr='is'+cat[0]+'_'+tagStr
		# 	histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		# 	print (catStr).ljust(ljust_i),
		# 	for bkg in bkgStackList:
		# 		print str(math.sqrt(yieldStatErrTable[histoPrefix][bkg])).ljust(ljust_i),
		# 	print str(math.sqrt(yieldStatErrTable[histoPrefix]['data'])).ljust(ljust_i),
		# 	print

		# #now print with top,ewk,qcd grouping
		# print
		# print 'YIELDS'.ljust(20*ljust_i), 
		# print 'ewk'.ljust(ljust_i),
		# print 'top'.ljust(ljust_i),
		# print 'qcd'.ljust(ljust_i),
		# print 'data'.ljust(ljust_i),
		# print
		# for cat in catList:
		# 	tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 	catStr='is'+cat[0]+'_'+tagStr
		# 	histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		# 	print (catStr).ljust(ljust_i),
		# 	print str(yieldTable[histoPrefix]['ewk']).ljust(ljust_i),
		# 	print str(yieldTable[histoPrefix]['top']).ljust(ljust_i),
		# 	print str(yieldTable[histoPrefix]['qcd']).ljust(ljust_i),
		# 	print str(yieldTable[histoPrefix]['data']).ljust(ljust_i),
		# 	print

		# print 'YIELDS ERRORS'
		# for cat in catList:
		# 	tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 	catStr='is'+cat[0]+'_'+tagStr
		# 	histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		# 	print (catStr).ljust(ljust_i),
		# 	print str(math.sqrt(yieldStatErrTable[histoPrefix]['ewk'])).ljust(ljust_i),
		# 	print str(math.sqrt(yieldStatErrTable[histoPrefix]['top'])).ljust(ljust_i),
		# 	print str(math.sqrt(yieldStatErrTable[histoPrefix]['qcd'])).ljust(ljust_i),
		# 	print str(math.sqrt(yieldStatErrTable[histoPrefix]['data'])).ljust(ljust_i),
		# 	print

		# #print yields for signals
		# print
		# print 'YIELDS'.ljust(20*ljust_i), 
		# for sig in sigList: print sig.ljust(ljust_i),
		# print
		# for cat in catList:
		# 	tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 	catStr='is'+cat[0]+'_'+tagStr
		# 	histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		# 	print (catStr).ljust(ljust_i),
		# 	for sig in sigList:
		# 		print str(yieldTable[histoPrefix][sig]).ljust(ljust_i),
		# 	print

		# print 'YIELDS ERRORS'
		# for cat in catList:
		# 	tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 	catStr='is'+cat[0]+'_'+tagStr
		# 	histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		# 	print (catStr).ljust(ljust_i),
		# 	for sig in sigList:
		# 		print str(math.sqrt(yieldStatErrTable[histoPrefix][sig])).ljust(ljust_i),
		# 	print
				
		# #print for AN tables
		# print
		# print "FOR AN (errors are statistical+normalization systematics): "
		# print
		# print 'YIELDS ELECTRON+JETS'.ljust(20*ljust_i), 
		# for cat in catList:
		# 	tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 	catStr='is'+cat[0]+'_'+tagStr
		# 	if cat[0]!='E': continue
		# 	print (catStr).ljust(ljust_i),
		# print
		# for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
		# 	print process.ljust(ljust_i),
		# 	for cat in catList:
		# 		tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 		catStr='is'+cat[0]+'_'+tagStr
		# 		if cat[0]!='E': continue
		# 		histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		# 		if process=='dataOverBkg':
		# 			dataTemp = yieldTable[histoPrefix]['data']+1e-20
		# 			dataTempErr = yieldStatErrTable[histoPrefix]['data']
		# 			totBkgTemp = yieldTable[histoPrefix]['totBkg']+1e-20
		# 			totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg'] # statistical error squared
		# 			totBkgTempErr += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
		# 			totBkgTempErr += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
		# 			totBkgTempErr += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
		# 			totBkgTempErr += (elcorrdSys*totBkgTemp)**2
		# 			dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
		# 			print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
		# 		else:
		# 			yieldtemp = yieldTable[histoPrefix][process]
		# 			yielderrtemp = yieldStatErrTable[histoPrefix][process]
		# 			if process=='totBkg': 
		# 				yielderrtemp += (elcorrdSys*yieldtemp)**2
		# 				yielderrtemp += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
		# 				yielderrtemp += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
		# 				yielderrtemp += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
		# 			elif process in sigList: 
		# 				yielderrtemp += (elcorrdSys*yieldtemp)**2
		# 			elif process!='data': 
		# 				yielderrtemp += (elcorrdSys*yieldtemp)**2
		# 				yielderrtemp += (addSys[process+'_'+tagStr]*yieldTable[histoPrefix][process])**2
		# 			if process=='data': print ' & '+str(int(yieldtemp)),
		# 			elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		# 			else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		# 	print '\\\\',
		# 	print
		# print
		# print 'YIELDS MUON+JETS'.ljust(20*ljust_i), 
		# for cat in catList:
		# 	tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 	catStr='is'+cat[0]+'_'+tagStr
		# 	if cat[0]!='M': continue
		# 	print (catStr).ljust(ljust_i),
		# print
		# for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
		# 	print process.ljust(ljust_i),
		# 	for cat in catList:
		# 		tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 		catStr='is'+cat[0]+'_'+tagStr
		# 		if cat[0]!='M': continue
		# 		histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		# 		if process=='dataOverBkg':
		# 			dataTemp = yieldTable[histoPrefix]['data']+1e-20
		# 			dataTempErr = yieldStatErrTable[histoPrefix]['data']
		# 			totBkgTemp = yieldTable[histoPrefix]['totBkg']+1e-20
		# 			totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg'] # statistical error squared
		# 			totBkgTempErr += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
		# 			totBkgTempErr += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
		# 			totBkgTempErr += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
		# 			totBkgTempErr += (mucorrdSys*totBkgTemp)**2
		# 			dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
		# 			print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
		# 		else:
		# 			yieldtemp = yieldTable[histoPrefix][process]
		# 			yielderrtemp = yieldStatErrTable[histoPrefix][process]
		# 			if process=='totBkg': 
		# 				yielderrtemp += (mucorrdSys*yieldtemp)**2
		# 				yielderrtemp += (addSys['top_'+tagStr]*yieldTable[histoPrefix]['top'])**2
		# 				yielderrtemp += (addSys['ewk_'+tagStr]*yieldTable[histoPrefix]['ewk'])**2
		# 				yielderrtemp += (addSys['qcd_'+tagStr]*yieldTable[histoPrefix]['qcd'])**2
		# 			elif process in sigList: 
		# 				yielderrtemp += (mucorrdSys*yieldtemp)**2
		# 			elif process!='data': 
		# 				yielderrtemp += (mucorrdSys*yieldtemp)**2
		# 				yielderrtemp += (addSys[process+'_'+tagStr]*yieldTable[histoPrefix][process])**2
		# 			if process=='data': print ' & '+str(int(yieldtemp)),
		# 			elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		# 			else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		# 	print '\\\\',
		# 	print
		
		# #print for AN tables systematics
		# if doAllSys:
		# 	print
		# 	print "FOR AN (shape systematic percentaces): "
		# 	print
		# 	print 'YIELDS'.ljust(20*ljust_i), 
		# 	for cat in catList:
		# 		tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 		catStr='is'+cat[0]+'_'+tagStr
		# 		print (catStr).ljust(ljust_i),
		# 	print
		# 	for process in ['ewk','top']+sigList:
		# 		print process.ljust(ljust_i),
		# 		print
		# 		for ud in ['Up','Down']:
		# 			for systematic in systematicList:
		# 				if systematic=='toppt' and process!='top': continue
		# 				print (systematic+ud).ljust(ljust_i),
		# 				for cat in catList:
		# 					tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 					catStr='is'+cat[0]+'_'+tagStr
		# 					histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		# 					print ' & '+str(round_sig(yieldTable[histoPrefix+systematic+ud][process]/(yieldTable[histoPrefix][process]+1e-20),2)),
		# 				print '\\\\',
		# 				print
		# 			if process!='top': continue
		# 			print ('q2'+ud).ljust(ljust_i),
		# 			for cat in catList:
		# 				tagStr='nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		# 				catStr='is'+cat[0]+'_'+tagStr
		# 				histoPrefix=discriminant+'_'+lumiStr+'fb_'+catStr
		# 				print ' & '+str(round_sig(yieldTable[histoPrefix+'q2'+ud][process]/(yieldTable[histoPrefix][process]+1e-20),2)),
		# 			print '\\\\',
		# 			print
		
		# print
		# print "FOR PAS (errors are statistical+normalization systematics): " #combines e/m channels
		# print
		# print 'YIELDS'.ljust(20*ljust_i), 
		# for tag in tagList:
		# 	tagStr = 'nH'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]
		# 	print (tagStr).ljust(ljust_i),
		# print
		# for process in bkgStackList+['ewk','top','qcd','totBkg','data','dataOverBkg']+sigList:
		# 	print process.ljust(ljust_i),
		# 	for tag in tagList:
		# 		tagStr = 'nH'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]
		# 		histoPrefix=discriminant+'_'+lumiStr+'fb_isE'+'_'+tagStr
		# 		if process=='dataOverBkg':
		# 			dataTemp = yieldTable[histoPrefix]['data']+yieldTable[histoPrefix.replace('_isE','_isM')]['data']+1e-20
		# 			dataTempErr = yieldStatErrTable[histoPrefix]['data']+yieldStatErrTable[histoPrefix.replace('_isE','_isM')]['data']
		# 			# get electron systs -- correlated across samples but not e/m
		# 			totBkgTemp = yieldTable[histoPrefix]['totBkg']
		# 			totBkgTempErr = yieldStatErrTable[histoPrefix]['totBkg']+(elcorrdSys*totBkgTemp)**2
		# 			# add muon systs
		# 			totBkgTemp = yieldTable[histoPrefix.replace('_isE','_isM')]['totBkg']
		# 			totBkgTempErr += yieldStatErrTable[histoPrefix]['totBkg']+(mucorrdSys*totBkgTemp)**2					
		# 			# set count to el+mu
		# 			totBkgTemp = yieldTable[histoPrefix]['totBkg']+yieldTable[histoPrefix.replace('_isE','_isM')]['totBkg']+1e-20
		# 			totBkgTempErr += (addSys['top_'+tagStr]*(yieldTable[histoPrefix]['top']+yieldTable[histoPrefix.replace('_isE','_isM')]['top']))**2
		# 			totBkgTempErr += (addSys['ewk_'+tagStr]*(yieldTable[histoPrefix]['ewk']+yieldTable[histoPrefix.replace('_isE','_isM')]['ewk']))**2
		# 			totBkgTempErr += (addSys['qcd_'+tagStr]*(yieldTable[histoPrefix]['qcd']+yieldTable[histoPrefix.replace('_isE','_isM')]['qcd']))**2
		# 			dataOverBkgErr = ((dataTemp/totBkgTemp)**2)*(dataTempErr/dataTemp**2+totBkgTempErr/totBkgTemp**2)
		# 			print ' & '+str(round_sig(dataTemp/totBkgTemp,5))+' $\pm$ '+str(round_sig(math.sqrt(dataOverBkgErr),2)),
		# 		else:
		# 			# get electron systs
		# 			yieldtemp = yieldTable[histoPrefix][process]
		# 			yielderrtemp = yieldStatErrTable[histoPrefix][process]+(elcorrdSys*yieldtemp)**2
		# 			# add muon systs
		# 			yieldtemp = yieldTable[histoPrefix.replace('_isE','_isM')][process]
		# 			yielderrtemp += yieldStatErrTable[histoPrefix][process]+(mucorrdSys*yieldtemp)**2					
		# 			# set count to el+mu
		# 			yieldtemp = yieldTable[histoPrefix][process]+yieldTable[histoPrefix.replace('_isE','_isM')][process]+1e-20
		# 			if process=='totBkg': 
		# 				yielderrtemp += (addSys['top_'+tagStr]*(yieldTable[histoPrefix]['top']+yieldTable[histoPrefix.replace('_isE','_isM')]['top']))**2
		# 				yielderrtemp += (addSys['ewk_'+tagStr]*(yieldTable[histoPrefix]['ewk']+yieldTable[histoPrefix.replace('_isE','_isM')]['ewk']))**2
		# 				yielderrtemp += (addSys['qcd_'+tagStr]*(yieldTable[histoPrefix]['qcd']+yieldTable[histoPrefix.replace('_isE','_isM')]['qcd']))**2
		# 			elif process!='data' and process not in sigList: 
		# 				yielderrtemp += (addSys[process+'_'+tagStr]*(yieldTable[histoPrefix][process]+yieldTable[histoPrefix.replace('_isE','_isM')][process]))**2
		# 			if process=='data': print ' & '+str(int(yieldtemp)),
		# 			elif process not in sigList: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		# 			else: print ' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(math.sqrt(yielderrtemp),2)),
		# 	print '\\\\',
		# 	print
		
		# sys.stdout = stdout_old
		# logFile.close()

def readTree(file):
	if not os.path.exists(file): 
		print "Error: File does not exist! Aborting ...",file
		os._exit(1)
	tFile = TFile(file,'READ')
	tTree = tFile.Get('ljmet')
	return tFile, tTree 

print "READING TREES"
shapesFiles = []#'jec','jer']
tTreeData = {}
tFileData = {}
for data in dataList:
	print "READING:", data
	tFileData[data],tTreeData[data]=readTree(step1Dir+'/'+samples[data]+'_hadd.root')

tTreeSig = {}
tFileSig = {}
for sig in sigList:
	for decay in decays:
		print "READING:", sig+decay
		print "        nominal"
		tFileSig[sig+decay],tTreeSig[sig+decay]=readTree(step1Dir+'/'+samples[sig+decay]+'_hadd.root')
		if doAllSys:
			for syst in shapesFiles:
				for ud in ['Up','Down']:
					print "        "+syst+ud
					tFileSig[sig+decay+syst+ud],tTreeSig[sig+decay+syst+ud]=readTree(step1Dir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[sig+decay]+'_hadd.root')

tTreeBkg = {}
tFileBkg = {}
for bkg in bkgList+q2List:
	if bkg in q2List and not doQ2sys: continue
	print "READING:",bkg
	print "        nominal"
	tFileBkg[bkg],tTreeBkg[bkg]=readTree(step1Dir+'/'+samples[bkg]+'_hadd.root')
	if doAllSys:
		for syst in shapesFiles:
			for ud in ['Up','Down']:
				if bkg in q2List:
					tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=None,None
				else:
					print "        "+syst+ud
					tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=readTree(step1Dir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+'_hadd.root')
print "FINISHED READING"

plotList = {#discriminantName:(discriminantLJMETName, binning, xAxisLabel)
	'HT':('AK4HT',linspace(0, 5000, 101).tolist(),';H_{T} (GeV);'),
	'ST':('AK4HTpMETpLepPt',linspace(0, 5000, 101).tolist(),';S_{T} (GeV);'),
	'minMlb':('minMleppBjet',linspace(0, 1000, 101).tolist(),';min[M(l,b)] (GeV);'),
	'minMlbST':('minMleppBjet',linspace(0, 1000, 101).tolist(),';min[M(l,b)] (GeV);'),
	}

print "PLOTTING:",iPlot
print "         LJMET Variable:",plotList[iPlot][0]
print "         X-AXIS TITLE  :",plotList[iPlot][2]
print "         BINNING USED  :",plotList[iPlot][1]

nCats  = len(catList)
catInd = 1
datahists = {}
bkghists  = {}
sighists  = {}
for cat in catList:
	catDir = cat[0]+'_nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
	category = {'isEM':cat[0],'nHtag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':'3p'}

	print catDir
	print category

	for data in dataList: 
		datahists.update(analyze(tTreeData,data,cutList,isotrig,False,doJetRwt,iPlot,plotList[iPlot],category,region,True))
		if catInd==nCats: del tFileData[data]
	for bkg in bkgList: 
		bkghists.update(analyze(tTreeBkg,bkg,cutList,isotrig,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region,True))
		if catInd==nCats: del tFileBkg[bkg]
		if doAllSys and catInd==nCats:
			for syst in shapesFiles:
				for ud in ['Up','Down']: del tFileBkg[bkg+syst+ud]
	for sig in sigList: 
		for decay in decays: 
			sighists.update(analyze(tTreeSig,sig+decay,cutList,isotrig,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region,True))
			if catInd==nCats: del tFileSig[sig+decay]
			if doAllSys and catInd==nCats:
				for syst in shapesFiles:
					for ud in ['Up','Down']: del tFileSig[sig+decay+syst+ud]
	if doQ2sys: 
		for q2 in q2List: 
			bkghists.update(analyze(tTreeBkg,q2,cutList,isotrig,False,doJetRwt,iPlot,plotList[iPlot],category,region,True))
			if catInd==nCats: del tFileBkg[q2]
	catInd+=1

#Negative Bin Correction
for bkg in bkghists.keys(): negBinCorrection(bkghists[bkg])

#OverFlow Correction
for data in datahists.keys(): overflow(datahists[data])
for bkg in bkghists.keys():   overflow(bkghists[bkg])
for sig in sighists.keys():   overflow(sighists[sig])

print "MAKING CATEGORIES FOR TOTAL SIGNALS ..."
makeThetaCats(datahists,sighists,bkghists,iPlot)

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


