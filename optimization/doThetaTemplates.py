#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools,getopt
from ROOT import TH1D,gROOT,TFile,TTree
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from numpy import linspace
from weights import *
from analyze import *
from samples import *
from utils import *

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
step1Dir = '/user_data/ssagir/LJMet_1lep_101916_step2preSel/nominal'

region = 'SR' #no need to change
isotrig = 1
doJetRwt = 0
iPlot='ST'
scaleSignalXsecTo1pb = True # this has to be "True" if you are making templates for limit calculation!!!!!!!!
scaleLumi = False
lumiScaleCoeff = 3990./2318.
doAllSys = False
doQ2sys = True
if not doAllSys: doQ2sys = False
systematicList = ['pileup','jec','jer','btag','tau21','mistag','muR','muF','muRFcorrd','toppt','jsf','topsf','trigeff']
normalizeRENORM_PDF = False #normalize the renormalization/pdf uncertainties to nominal templates --> normalizes both the background and signal processes !!!!

bkgList = [
	'DY',
	'WJetsMG100',
	'WJetsMG200',
	'WJetsMG400',
	'WJetsMG600',
	'WJetsMG800',
	'WJetsMG1200',
	'WJetsMG2500',
	'WW','WZ','ZZ',
	'TTJetsPH0to1000inc',
	'TTJetsPH1000toINFinc',
	'TTJetsPH1000mtt',
	'TTWl','TTWq',
	'TTZl','TTZq',
	'Tt','Tbt','Ts',
	'TtW','TbtW',
	#'QCDht100','QCDht200',
	'QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000',
	]
q2List  = [#energy scale sample to be processed
	       'TTJetsPHQ2U','TTJetsPHQ2D',
	       #'TtWQ2U','TbtWQ2U',
	       #'TtWQ2D','TbtWQ2D',
	       ]
			       
bkgProcList = ['TTJets','T','TTW','TTZ','WJets','ZJets','VV','QCD']
wjetList  = ['WJetsMG100','WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500'] 
zjetList  = ['DY']
vvList    = ['WW','WZ','ZZ']
ttwList   = ['TTWl','TTWq']
ttzList   = ['TTZl','TTZq']
ttjetList = ['TTJetsPH1000toINFinc','TTJetsPH1000mtt']
ttjetList+= ['TTJetsPH0to1000inc']
#ttjetList+= ['TTJetsPH0to1000inc1','TTJetsPH0to1000inc2','TTJetsPH0to1000inc3','TTJetsPH0to1000inc4','TTJetsPH0to1000inc5','TTJetsPH0to1000inc6','TTJetsPH0to1000inc7','TTJetsPH0to1000inc8']
tList     = ['Tt','Tbt','Ts','TtW','TbtW']

bkgGrupList = ['top','ewk','qcd']
topList = ttjetList+ttwList+ttzList+tList
ewkList = wjetList+zjetList+vvList
qcdList = ['QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000']#'QCDht100','QCDht200',
dataList = ['DataEPRC','DataEPRB','DataEPRD','DataMPRC','DataMPRB','DataMPRD']

q2UpList   = ttwList+ttzList+tList+['TTJetsPHQ2U']#,'TtWQ2U','TbtWQ2U']
q2DownList = ttwList+ttzList+tList+['TTJetsPHQ2D']#,'TtWQ2D','TbtWQ2D']

whichSignal = 'X53X53' #TT, BB, or X53X53
signalMassRange = [700,1600]
sigList = [whichSignal+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100)]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in range(signalMassRange[0],signalMassRange[1]+100,100) for chiral in ['left','right']]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
if whichSignal=='X53X53': decays = [''] #decays to tWtW 100% of the time

doBRScan = False
BRs={}
BRs['BW']=[0.0,0.50,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
BRs['TH']=[0.5,0.25,0.0,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]
BRs['TZ']=[0.5,0.25,1.0,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
nBRconf=len(BRs['BW'])
if not doBRScan: nBRconf=1

lepPtCut=80
metCut=100
njetsCut=4
nbjetsCut=0
drCut=1
jet1PtCut=200
jet2PtCut=90
jet3PtCut=0
jet4PtCut=0
jet5PtCut=0
Wjet1PtCut=0
bjet1PtCut=0
htCut=0
stCut=0
minMlbCut=0

isEMlist =['E','M']
nttaglist=['0','1p']
nWtaglist=['0','1p']
nbtaglist=['1','2p']
catList = ['is'+item[0]+'_nT'+item[1]+'_nW'+item[2]+'_nB'+item[3] for item in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist))]
tagList = ['nT'+item[0]+'_nW'+item[1]+'_nB'+item[2] for item in list(itertools.product(nttaglist,nWtaglist,nbtaglist))]

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

cutString  = 'lep'+str(int(cutList['lepPtCut']))+'_MET'+str(int(cutList['metCut']))
cutString += '_NJets'+str(int(cutList['njetsCut']))#+'_NBJets'+str(int(cutList['nbjetsCut']))
cutString += '_DR'+str(cutList['drCut'])+'_1jet'+str(int(cutList['jet1PtCut']))
cutString += '_2jet'+str(int(cutList['jet2PtCut']))#+'_3jet'+str(int(cutList['jet3PtCut']))
# cutString += '_4jet'+str(int(cutList['jet4PtCut']))+'_5jet'+str(int(cutList['jet5PtCut']))
# cutString += '_1Wjet'+str(cutList['Wjet1PtCut'])+'_1bjet'+str(cutList['bjet1PtCut'])
# cutString += '_HT'+str(cutList['htCut'])+'_ST'+str(cutList['stCut'])+'_minMlb'+str(cutList['minMlbCut'])

cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='templates_minMlb_'
pfix+=datestr+'_'+timestr

if len(sys.argv)>1: outDir=sys.argv[1]
else: 
	outDir = os.getcwd()+'/'
	outDir+=pfix
	if not os.path.exists(outDir): os.system('mkdir '+outDir)
	if not os.path.exists(outDir+'/'+cutString): os.system('mkdir '+outDir+'/'+cutString)
	outDir+='/'+cutString

lumiSys = 0.062 #lumi uncertainty
eltrigSys = 0.03 #electron trigger uncertainty
mutrigSys = 0.011 #muon trigger uncertainty
elIdSys = 0.01 #electron id uncertainty
muIdSys = 0.011 #muon id uncertainty
elIsoSys = 0.01 #electron isolation uncertainty
muIsoSys = 0.03 #muon isolation uncertainty
elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)

modelingSys = { #top modeling uncertainty from ttbar CR (correlated across e/m)
			   'top_nT0_nW0_nB1'   :0.,
			   'top_nT0_nW0_nB2p'  :0.,
			   'top_nT0_nW1p_nB1'  :0.,
			   'top_nT0_nW1p_nB2p' :0.,
			   'top_nT1p_nW0_nB1'  :0.,
			   'top_nT1p_nW0_nB2p' :0.,
			   'top_nT1p_nW1p_nB1' :0.,
			   'top_nT1p_nW1p_nB2p':0.,
			   
			   'ewk_nT0_nW0_nB1'   :0.,
			   'ewk_nT0_nW0_nB2p'  :0.,
			   'ewk_nT0_nW1p_nB1'  :0.,
			   'ewk_nT0_nW1p_nB2p' :0.,
			   'ewk_nT1p_nW0_nB1'  :0.,
			   'ewk_nT1p_nW0_nB2p' :0.,
			   'ewk_nT1p_nW1p_nB1' :0.,
			   'ewk_nT1p_nW1p_nB2p':0.,
			   }
for tag in tagList:
	modTag = tag[tag.find('nT'):]
	modelingSys['data_'+modTag] = 0.
	modelingSys['qcd_'+modTag] = 0.
	#modelingSys['ewk_'+modTag] = 0.
	#modelingSys['top_'+modTag] = 0.
		 
postTag = 'isSR_'
###########################################################
#################### CATEGORIZATION #######################
###########################################################
def makeThetaCats(datahists,sighists,bkghists,discriminant):
	yieldTable = {}
	yieldStatErrTable = {}
	for cat in catList:
		histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
		yieldTable[histoPrefix]={}
		yieldStatErrTable[histoPrefix]={}
		if doAllSys:
			for syst in systematicList:
				for ud in ['Up','Down']:
					yieldTable[histoPrefix+syst+ud]={}
			
		if doQ2sys:
			yieldTable[histoPrefix+'q2Up']={}
			yieldTable[histoPrefix+'q2Down']={}

	for BRind in range(nBRconf):
		BRconfStr=''
		if doBRScan: BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
		print "       BR Configuration:"+BRconfStr
		#Initialize dictionaries for histograms
		hsig,htop,hewk,hqcd,hdata={},{},{},{},{}
		hwjets,hzjets,httjets,ht,httw,httz,hvv={},{},{},{},{},{},{}
		for cat in catList:
			print "              processing cat: "+cat
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
			i=BRconfStr+cat
			
			#Group processes
			hwjets[i] = bkghists[histoPrefix+'_'+wjetList[0]].Clone(histoPrefix+'_WJets')
			hzjets[i] = bkghists[histoPrefix+'_'+zjetList[0]].Clone(histoPrefix+'_ZJets')
			httjets[i] = bkghists[histoPrefix+'_'+ttjetList[0]].Clone(histoPrefix+'_TTJets')
			ht[i] = bkghists[histoPrefix+'_'+tList[0]].Clone(histoPrefix+'_T')
			httw[i] = bkghists[histoPrefix+'_'+ttwList[0]].Clone(histoPrefix+'_TTW')
			httz[i] = bkghists[histoPrefix+'_'+ttzList[0]].Clone(histoPrefix+'_TTZ')
			hvv[i] = bkghists[histoPrefix+'_'+vvList[0]].Clone(histoPrefix+'_VV')
			for bkg in ttjetList:
				if bkg!=ttjetList[0]: httjets[i].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in wjetList:
				if bkg!=wjetList[0]: hwjets[i].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in ttwList:
				if bkg!=ttwList[0]: httw[i].Add(bkghists[histoPrefix+'_'+bkg])
			for bkg in ttzList:
				if bkg!=ttzList[0]: httz[i].Add(bkghists[histoPrefix+'_'+bkg])
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
			for signal in sigList:
				i=BRconfStr+cat+signal
				hsig[i] = sighists[histoPrefix+'_'+signal+decays[0]].Clone(histoPrefix+'__sig')
				if doBRScan: hsig[i].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
				for decay in decays:
					if decay!=decays[0]:
						htemp = sighists[histoPrefix+'_'+signal+decay].Clone()
						if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
						hsig[i].Add(htemp)
			i=BRconfStr+cat

			#systematics
			if doAllSys:
				for syst in systematicList:
					for ud in ['Up','Down']:
						if syst!='toppt':
							hqcd[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							hewk[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							htop[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+topList[0]].Clone(histoPrefix+'__top__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							for bkg in qcdList: 
								if bkg!=qcdList[0]: hqcd[syst+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
							for bkg in ewkList: 
								if bkg!=ewkList[0]: hewk[syst+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
							for bkg in topList: 
								if bkg!=topList[0]: htop[syst+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
							for signal in sigList:
								i=BRconfStr+cat+signal
								hsig[syst+ud+str(i)] = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
								if doBRScan: hsig[syst+ud+str(i)].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
								for decay in decays:
									htemp = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decay].Clone()
									if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
									if decay!=decays[0]: hsig[syst+ud+str(i)].Add(htemp)
							i=BRconfStr+cat
						if syst=='toppt': # top pt is only on the ttbar sample, so it needs special treatment!
							htop[syst+ud+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+ttjetList[0]].Clone(histoPrefix+'__top__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							for bkg in ttjetList: 
								if bkg!=ttjetList[0]: htop[syst+ud+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
							for bkg in topList: 
								if bkg not in ttjetList: htop[syst+ud+str(i)].Add(bkghists[histoPrefix+'_'+bkg])
				for pdfInd in range(100):
					hqcd['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+qcdList[0]].Clone(histoPrefix+'__qcd__pdf'+str(pdfInd))
					hewk['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+ewkList[0]].Clone(histoPrefix+'__ewk__pdf'+str(pdfInd))
					htop['pdf'+str(pdfInd)+'_'+str(i)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+topList[0]].Clone(histoPrefix+'__top__pdf'+str(pdfInd))
					for bkg in qcdList: 
						if bkg!=qcdList[0]: hqcd['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					for bkg in ewkList: 
						if bkg!=ewkList[0]: hewk['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					for bkg in topList: 
						if bkg!=topList[0]: htop['pdf'+str(pdfInd)+'_'+str(i)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
					for signal in sigList:
						i=BRconfStr+cat+signal
						hsig['pdf'+str(pdfInd)+'_'+str(i)] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__pdf'+str(pdfInd))
						if doBRScan: hsig['pdf'+str(pdfInd)+'_'+str(i)].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
						for decay in decays:
							htemp = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decay].Clone()
							if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
							if decay!=decays[0]:hsig['pdf'+str(pdfInd)+'_'+str(i)].Add(htemp)
					i=BRconfStr+cat
											
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
			yieldTable[histoPrefix]['TTW']    = httw[i].Integral()
			yieldTable[histoPrefix]['TTZ']    = httz[i].Integral()
			yieldTable[histoPrefix]['TTJets'] = httjets[i].Integral()
			yieldTable[histoPrefix]['T']      = ht[i].Integral()
			yieldTable[histoPrefix]['QCD']    = hqcd[i].Integral()
			for signal in sigList: 
				i=BRconfStr+cat+signal
				yieldTable[histoPrefix][signal] = hsig[i].Integral()
			i=BRconfStr+cat
	
			#+/- 1sigma variations of shape systematics
			if doAllSys:
				for syst in systematicList:
					for ud in ['Up','Down']:
						yieldTable[histoPrefix+syst+ud]['top']    = htop[syst+ud+str(i)].Integral()
						if syst!='toppt':
							yieldTable[histoPrefix+syst+ud]['ewk']    = hewk[syst+ud+str(i)].Integral()
							yieldTable[histoPrefix+syst+ud]['qcd']    = hqcd[syst+ud+str(i)].Integral()
							yieldTable[histoPrefix+syst+ud]['totBkg'] = htop[syst+ud+str(i)].Integral()+hewk[syst+ud+str(i)].Integral()+hqcd[syst+ud+str(i)].Integral()
							for signal in sigList: 
								i=BRconfStr+cat+signal
								yieldTable[histoPrefix+syst+ud][signal] = hsig[syst+ud+str(i)].Integral()
							i=BRconfStr+cat
				
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
			yieldStatErrTable[histoPrefix]['TTW']    = 0.
			yieldStatErrTable[histoPrefix]['TTZ']    = 0.
			yieldStatErrTable[histoPrefix]['TTJets'] = 0.
			yieldStatErrTable[histoPrefix]['T']      = 0.
			yieldStatErrTable[histoPrefix]['QCD']    = 0.
			for signal in sigList: yieldStatErrTable[histoPrefix][signal] = 0.

			for ibin in range(1,htop[i].GetXaxis().GetNbins()+1):
				yieldStatErrTable[histoPrefix]['top']    += htop[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['ewk']    += hewk[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['qcd']    += hqcd[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['totBkg'] += htop[i].GetBinError(ibin)**2+hewk[i].GetBinError(ibin)**2+hqcd[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['data']   += hdata[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['WJets']  += hwjets[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['ZJets']  += hzjets[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['VV']     += hvv[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['TTW']    += httw[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['TTZ']    += httz[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['TTJets'] += httjets[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['T']      += ht[i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['QCD']    += hqcd[i].GetBinError(ibin)**2
				for signal in sigList: 
					i=BRconfStr+cat+signal
					yieldStatErrTable[histoPrefix][signal] += hsig[i].GetBinError(ibin)**2
				i=BRconfStr+cat
			for key in yieldStatErrTable[histoPrefix].keys(): yieldStatErrTable[histoPrefix][key] = math.sqrt(yieldStatErrTable[histoPrefix][key])

		#scale signal cross section to 1pb
		print "SCALING SIGNAL TEMPLATES TO 1pb ..."
		if scaleSignalXsecTo1pb:
			for signal in sigList:
				thetaRfileName = outDir+'/templates_'+discriminant+'_'+signal+BRconfStr+'_'+lumiStr+'fb'+'.root'
				thetaRfile = TFile(thetaRfileName,'RECREATE')
				for cat in catList:
					i=BRconfStr+cat+signal
					hsig[i].Scale(1./xsec[signal])
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt': continue
							hsig[syst+'Up'+str(i)].Scale(1./xsec[signal])
							hsig[syst+'Down'+str(i)].Scale(1./xsec[signal])
							if normalizeRENORM_PDF and (syst.startswith('mu') or syst=='pdf'):
								hsig[syst+'Up'+str(i)].Scale(hsig[i].Integral()/hsig[syst+'Up'+str(i)].Integral())
								hsig[syst+'Down'+str(i)].Scale(hsig[i].Integral()/hsig[syst+'Down'+str(i)].Integral())
						for pdfInd in range(100): 
							hsig['pdf'+str(pdfInd)+'_'+str(i)].Scale(1./xsec[signal])

		#Theta templates:
		print "WRITING THETA TEMPLATES: "
		for signal in sigList:
			print "              ...writing: "+signal
			thetaRfileName = outDir+'/templates_'+discriminant+'_'+signal+BRconfStr+'_'+lumiStr+'fb'+'.root'
			thetaRfile = TFile(thetaRfileName,'RECREATE')
			for cat in catList:
				i=BRconfStr+cat+signal
				if hsig[i].Integral() > 0:
					hsig[i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt': continue
							hsig[syst+'Up'+str(i)].Write()
							hsig[syst+'Down'+str(i)].Write()
						for pdfInd in range(100): hsig['pdf'+str(pdfInd)+'_'+str(i)].Write()
				i=BRconfStr+cat
				if htop[i].Integral() > 0:
					htop[i].Write()
					if doAllSys:
						for syst in systematicList:
							htop[syst+'Up'+str(i)].Write()
							htop[syst+'Down'+str(i)].Write()
						for pdfInd in range(100): htop['pdf'+str(pdfInd)+'_'+str(i)].Write()
					if doQ2sys:
						htop['q2Up'+str(i)].Write()
						htop['q2Down'+str(i)].Write()
				if hewk[i].Integral() > 0:
					hewk[i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt': continue
							hewk[syst+'Up'+str(i)].Write()
							hewk[syst+'Down'+str(i)].Write()
						for pdfInd in range(100): hewk['pdf'+str(pdfInd)+'_'+str(i)].Write()
				if hqcd[i].Integral() > 0:
					hqcd[i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt': continue
							hqcd[syst+'Up'+str(i)].Write()
							hqcd[syst+'Down'+str(i)].Write()
						for pdfInd in range(100): hqcd['pdf'+str(pdfInd)+'_'+str(i)].Write()
				hdata[i].Write()
			thetaRfile.Close()

		#Combine templates:
		print "WRITING COMBINE TEMPLATES: "
		combineRfileName = outDir+'/templates_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.root'
		combineRfile = TFile(combineRfileName,'RECREATE')
		for cat in catList:
			print "              ...writing: "+cat
			i=BRconfStr+cat
			for signal in sigList:
				mass = [str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100) if str(mass) in signal][0]
				i=BRconfStr+cat+signal
				hsig[i].SetName(hsig[i].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass))
				hsig[i].Write()
				if doAllSys:
					for syst in systematicList:
						if syst=='toppt': continue
						hsig[syst+'Up'+str(i)].SetName(hsig[syst+'Up'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass).replace('__plus','Up'))
						hsig[syst+'Down'+str(i)].SetName(hsig[syst+'Down'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass).replace('__minus','Down'))
						hsig[syst+'Up'+str(i)].Write()
						hsig[syst+'Down'+str(i)].Write()
					for pdfInd in range(100): 
						hsig['pdf'+str(pdfInd)+'_'+str(i)].SetName(hsig['pdf'+str(pdfInd)+'_'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass))
						hsig['pdf'+str(pdfInd)+'_'+str(i)].Write()
			i=BRconfStr+cat
			htop[i].SetName(htop[i].GetName().replace('fb_','fb_'+postTag))
			htop[i].Write()
			if doAllSys:
				for syst in systematicList:
					htop[syst+'Up'+str(i)].SetName(htop[syst+'Up'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
					htop[syst+'Down'+str(i)].SetName(htop[syst+'Down'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
					htop[syst+'Up'+str(i)].Write()
					htop[syst+'Down'+str(i)].Write()
				for pdfInd in range(100): 
					htop['pdf'+str(pdfInd)+'_'+str(i)].SetName(htop['pdf'+str(pdfInd)+'_'+str(i)].GetName().replace('fb_','fb_'+postTag))
					htop['pdf'+str(pdfInd)+'_'+str(i)].Write()
			if doQ2sys:
				htop['q2Up'+str(i)].SetName(htop['q2Up'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
				htop['q2Down'+str(i)].SetName(htop['q2Down'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
				htop['q2Up'+str(i)].Write()
				htop['q2Down'+str(i)].Write()
			hewk[i].SetName(hewk[i].GetName().replace('fb_','fb_'+postTag))
			hewk[i].Write()
			if doAllSys:
				for syst in systematicList:
					if syst=='toppt': continue
					hewk[syst+'Up'+str(i)].SetName(hewk[syst+'Up'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
					hewk[syst+'Down'+str(i)].SetName(hewk[syst+'Down'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
					hewk[syst+'Up'+str(i)].Write()
					hewk[syst+'Down'+str(i)].Write()
				for pdfInd in range(100): 
					hewk['pdf'+str(pdfInd)+'_'+str(i)].SetName(hewk['pdf'+str(pdfInd)+'_'+str(i)].GetName().replace('fb_','fb_'+postTag))
					hewk['pdf'+str(pdfInd)+'_'+str(i)].Write()
			hqcd[i].SetName(hqcd[i].GetName().replace('fb_','fb_'+postTag))
			hqcd[i].Write()
			if doAllSys:
				for syst in systematicList:
					if syst=='toppt': continue
					hqcd[syst+'Up'+str(i)].SetName(hqcd[syst+'Up'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
					hqcd[syst+'Down'+str(i)].SetName(hqcd[syst+'Down'+str(i)].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
					hqcd[syst+'Up'+str(i)].Write()
					hqcd[syst+'Down'+str(i)].Write()
				for pdfInd in range(100): 
					hqcd['pdf'+str(pdfInd)+'_'+str(i)].SetName(hqcd['pdf'+str(pdfInd)+'_'+str(i)].GetName().replace('fb_','fb_'+postTag))
					hqcd['pdf'+str(pdfInd)+'_'+str(i)].Write()
			hdata[i].SetName(hdata[i].GetName().replace('fb_','fb_'+postTag).replace('DATA','data_obs'))
			hdata[i].Write()
		combineRfile.Close()

		table = []
		table.append(['CUTS:',cutString])
		table.append(['break'])
		table.append(['break'])
		
		#yields without background grouping
		table.append(['YIELDS']+[proc for proc in bkgProcList+['data']])
		for cat in catList:
			row = [cat]
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
			for proc in bkgProcList+['data']:
				row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
			table.append(row)			
		table.append(['break'])
		table.append(['break'])
		
		#yields with top,ewk,qcd grouping
		table.append(['YIELDS']+[proc for proc in bkgGrupList+['data']])
		for cat in catList:
			row = [cat]
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
			for proc in bkgGrupList+['data']:
				row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
			table.append(row)
		table.append(['break'])
		table.append(['break'])
		
		#yields for signals
		table.append(['YIELDS']+[proc for proc in sigList])
		for cat in catList:
			row = [cat]
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
			for proc in sigList:
				row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
			table.append(row)

		#yields for AN tables (yields in e/m channels)
		for isEM in isEMlist:
			if isEM=='E': corrdSys = elcorrdSys
			if isEM=='M': corrdSys = mucorrdSys
			for nttag in nttaglist:
				table.append(['break'])
				table.append(['','is'+isEM+'_nT'+nttag+'_yields'])
				table.append(['break'])
				table.append(['YIELDS']+[cat for cat in catList if 'is'+isEM in cat and 'nT'+nttag in cat]+['\\\\'])
				for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
					row = [proc]
					for cat in catList:
						if not ('is'+isEM in cat and 'nT'+nttag in cat): continue
						modTag = cat[cat.find('nT'):]
						histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
						yieldtemp = 0.
						yielderrtemp = 0.
						if proc=='totBkg' or proc=='dataOverBkg':
							for bkg in bkgGrupList:
								try:
									yieldtemp += yieldTable[histoPrefix][bkg]
									yielderrtemp += yieldStatErrTable[histoPrefix][bkg]**2
									yielderrtemp += (modelingSys[bkg+'_'+modTag]*yieldTable[histoPrefix][bkg])**2
								except:
									print "Missing",bkg,"for channel:",cat
									pass
							yielderrtemp += (corrdSys*yieldtemp)**2
							if proc=='dataOverBkg':
								dataTemp = yieldTable[histoPrefix]['data']+1e-20
								dataTempErr = yieldStatErrTable[histoPrefix]['data']**2
								yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
								yieldtemp = dataTemp/yieldtemp
						else:
							try:
								yieldtemp += yieldTable[histoPrefix][proc]
								yielderrtemp += yieldStatErrTable[histoPrefix][proc]**2
							except:
								print "Missing",proc,"for channel:",cat
								pass
							if proc not in sigList: yielderrtemp += (modelingSys[proc+'_'+modTag]*yieldtemp)**2
							yielderrtemp += (corrdSys*yieldtemp)**2
						yielderrtemp = math.sqrt(yielderrtemp)
						if proc=='data': row.append(' & '+str(round_sig(yieldTable[histoPrefix][proc],2)))
						else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
					row.append('\\\\')
					table.append(row)
		
		#yields for PAS tables (yields in e/m channels combined)
		for nttag in nttaglist:
			table.append(['break'])
			table.append(['','isL_nT'+nttag+'_yields'])
			table.append(['break'])
			table.append(['YIELDS']+[cat.replace('isE','isL') for cat in catList if 'isE' in cat and 'nT'+nttag in cat]+['\\\\'])
			for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
				row = [proc]
				for cat in catList:
					if not ('isE' in cat and 'nT'+nttag in cat): continue
					modTag = cat[cat.find('nT'):]
					histoPrefixE = discriminant+'_'+lumiStr+'fb_'+cat
					histoPrefixM = histoPrefixE.replace('isE','isM')
					yieldtemp = 0.
					yieldtempE = 0.
					yieldtempM = 0.
					yielderrtemp = 0. 
					if proc=='totBkg' or proc=='dataOverBkg':
						for bkg in bkgGrupList:
							try:
								yieldtempE += yieldTable[histoPrefixE][bkg]
								yieldtempM += yieldTable[histoPrefixM][bkg]
								yieldtemp += yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]
								yielderrtemp += yieldStatErrTable[histoPrefixE][bkg]**2+yieldStatErrTable[histoPrefixM][bkg]**2
								yielderrtemp += (modelingSys[bkg+'_'+modTag]*(yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]))**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
							except:
								print "Missing",bkg,"for channel:",cat
								pass
						yielderrtemp += (elcorrdSys*yieldtempE+mucorrdSys*yieldtempM)**2
						if proc=='dataOverBkg':
							dataTemp = yieldTable[histoPrefixE]['data']+yieldTable[histoPrefixM]['data']+1e-20
							dataTempErr = yieldStatErrTable[histoPrefixE]['data']**2+yieldStatErrTable[histoPrefixM]['data']**2
							yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
							yieldtemp = dataTemp/yieldtemp
					else:
						try:
							yieldtempE += yieldTable[histoPrefixE][proc]
							yieldtempM += yieldTable[histoPrefixM][proc]
							yieldtemp += yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc]
							yielderrtemp += yieldStatErrTable[histoPrefixE][proc]**2+yieldStatErrTable[histoPrefixM][proc]**2
						except:
							print "Missing",proc,"for channel:",cat
							pass
						if proc not in sigList: yielderrtemp += (modelingSys[proc+'_'+modTag]*yieldtemp)**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						yielderrtemp += (elcorrdSys*yieldtempE+mucorrdSys*yieldtempM)**2
					yielderrtemp = math.sqrt(yielderrtemp)
					if proc=='data': row.append(' & '+str(round_sig(yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc],2)))
					else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
				row.append('\\\\')
				table.append(row)

		#systematics
		table.append(['break'])
		table.append(['','Systematics'])
		table.append(['break'])
		for proc in bkgGrupList+sigList:
			table.append([proc]+[cat for cat in catList]+['\\\\'])
			for syst in sorted(systematicList+['q2']):
				for ud in ['Up','Down']:
					row = [syst+ud]
					for cat in catList:
						histoPrefix = discriminant+'_'+lumiStr+'fb_'+cat
						nomHist = histoPrefix
						shpHist = histoPrefix+syst+ud
						try: row.append(' & '+str(round_sig(yieldTable[shpHist][proc]/(yieldTable[nomHist][proc]+1e-20),2)))
						except:
							if (syst=='toppt' or syst=='q2') and proc not in sigList:
								print "Missing",proc,"for channel:",cat,"and systematic:",syst
							pass
					row.append('\\\\')
					table.append(row)
			table.append(['break'])
			
		out=open(outDir+'/yields_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.txt','w')
		printTable(table,out)

def readTree(file):
	if not os.path.exists(file): 
		print "Error: File does not exist! Aborting ...",file
		os._exit(1)
	tFile = TFile(file,'READ')
	tTree = tFile.Get('ljmet')
	return tFile, tTree 

print "READING TREES"
shapesFiles = ['jec','jer']
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
	'HT':('AK4HT',linspace(0, 5000, 51).tolist(),';H_{T} (GeV);'),
	'ST':('AK4HTpMETpLepPt',linspace(0, 5000, 51).tolist(),';S_{T} (GeV);'),
	'minMlb':('minMleppBjet',linspace(0, 800, 51).tolist(),';min[M(l,b)] (GeV);'),
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
	isEM  = cat.split('_')[0].replace('is','')
	nttag = cat.split('_')[1].replace('nT','')
	nwtag = cat.split('_')[2].replace('nW','')
	nbtag = cat.split('_')[3].replace('nB','')
	category = {'isEM':isEM,'nttag':nttag,'nWtag':nwtag,'nbtag':nbtag}
	for data in dataList: 
		datahists.update(analyze(tTreeData,data,cutList,isotrig,False,doJetRwt,iPlot,plotList[iPlot],category,region))
		if catInd==nCats: del tFileData[data]
	for bkg in bkgList: 
		bkghists.update(analyze(tTreeBkg,bkg,cutList,isotrig,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region))
		if catInd==nCats: del tFileBkg[bkg]
		if doAllSys and catInd==nCats:
			for syst in shapesFiles:
				for ud in ['Up','Down']: del tFileBkg[bkg+syst+ud]
	for sig in sigList: 
		for decay in decays: 
			sighists.update(analyze(tTreeSig,sig+decay,cutList,isotrig,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region))
			if catInd==nCats: del tFileSig[sig+decay]
			if doAllSys and catInd==nCats:
				for syst in shapesFiles:
					for ud in ['Up','Down']: del tFileSig[sig+decay+syst+ud]
	if doQ2sys: 
		for q2 in q2List: 
			bkghists.update(analyze(tTreeBkg,q2,cutList,isotrig,False,doJetRwt,iPlot,plotList[iPlot],category,region))
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


