#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools,fnmatch
from ROOT import gROOT,TFile,TH1F
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from weights import *
from modSyst import *
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

<<<<<<< HEAD
region='PS' #PS,SR,TTCR,WJCR
isCategorized=False
pfix='templates'+region
if not isCategorized: pfix='kinematics'+region
pfix+='_HighPU'
outDir = os.getcwd()+'/'+pfix+'/'

scaleSignalXsecTo1pb = True # this has to be "True" if you are making templates for limit calculation!!!!!!!!
scaleLumi = True
lumiScaleCoeff = 41530./41298.
doAllSys = False
addCRsys = False
systematicList = ['muRFcorrd','pileup','prefire','jec','btag','jsf','Teff','Tmis','Heff','Hmis','Zeff','Zmis','Weff','Wmis','Beff','Bmis','Jeff','Jmis']#,'toppt']
if isCategorized: systematicList = ['muRFcorrd','pileup','prefire','jec','btag','jsf','muR','muF','Teff','Tmis','Heff','Hmis','Zeff','Zmis','Weff','Wmis','Beff','Bmis','Jeff','Jmis']#,'pdf','toppt',]
=======
region='SRalgos' #PS,PSalgos,SR,SRalgos,CR,NoDR
isCategorized=False
pfix='templates'+region
if not isCategorized: pfix='kinematics'+region
pfix+='_Oct11'
outDir = os.getcwd()+'/'+pfix+'/'

scaleSignalXsecTo1pb = True # this has to be "True" if you are making templates for limit calculation!!!!!!!!
scaleLumi = False
lumiScaleCoeff = 35867./36814.
doAllSys = True
addCRsys = False
#systematicList = ['pileup','jec','jer','tau21','jmr','jms','muR','muF','muRFcorrd','jsf','toppt','trigeff','btag','mistag','taupt']#,,'topsf'
systematicList = ['pileup','jsf','muRFcorrd','toppt']
>>>>>>> upstream/tptp_94X
normalizeRENORM_PDF = False #normalize the renormalization/pdf uncertainties to nominal templates --> normalizes signal processes only !!!!
		       
bkgGrupList = ['top','ewk','qcd']
bkgProcList = ['TTJets','WJets','ZJets','qcd','TTV','T']
bkgProcs = {}
<<<<<<< HEAD
bkgProcs['WJets']  = ['WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500'] #'WJetsMG200',
bkgProcs['ZJets']  = ['DYMG']#200','DYMG400','DYMG600','DYMG800','DYMG1200','DYMG2500']
bkgProcs['VV']     = ['WW','WZ','ZZ']
bkgProcs['TTV']    = ['TTW','TTZ','TTH']#,'TTWq','TTZq']
bkgProcs['TTJets'] = ['TTJetsSemiLep0','TTJetsSemiLep700','TTJetsSemiLep1000','TTJetsHad0','TTJetsHad700','TTJetsHad1000',
		      'TTJets2L2nu0','TTJets2L2nu700','TTJets2L2nu1000','TTJetsPH700mtt','TTJetsPH1000mtt']
bkgProcs['T']      = ['Tt','Tbt','Ts','Tbs','TtW','TbtW']
bkgProcs['qcd'] = ['QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000']#'QCDht200',
bkgProcs['top'] = bkgProcs['TTJets']+bkgProcs['T']+bkgProcs['TTV']
bkgProcs['ewk'] = bkgProcs['WJets']+bkgProcs['ZJets']+bkgProcs['VV'] 
dataList = [
	'DataERRBCDEF',
	'DataMRRBCDEF'
	#'Data18EG',
	#'Data18MU',
=======
bkgProcs['WJets']  = ['WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500'] 
bkgProcs['ZJets']  = ['DY']
#bkgProcs['VV']     = ['WW','WZ','ZZ'] ## ADDME
bkgProcs['TTV']    = ['TTWl','TTZl']#,'TTWq','TTZq'] ## ADDME
bkgProcs['TTJets'] = ['TTJetsSemiLep0','TTJetsSemiLep700','TTJetsSemiLep1000','TTJetsHad0','TTJetsHad700','TTJetsHad1000',
		      'TTJets2L2nu0','TTJets2L2nu700','TTJets2L2nu1000','TTJetsPH700mtt','TTJetsPH1000mtt']
bkgProcs['T']      = ['Tt','Tbt','Ts','TtW','TbtW']
bkgProcs['qcd'] = ['QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000']
bkgProcs['top'] = bkgProcs['TTJets']+bkgProcs['T']+bkgProcs['TTV']
bkgProcs['ewk'] = bkgProcs['WJets']+bkgProcs['ZJets']#+bkgProcs['VV'] 
dataList = [
	'DataERRBCDEF',
	'DataMRRBCDEF'
>>>>>>> upstream/tptp_94X
	]

topptProcs = ['top','TTJets']

<<<<<<< HEAD
whichSignal = 'TT' #HTB, TT, BB, or X53X53
=======
whichSignal = 'TT' #TT, BB, or X53X53
>>>>>>> upstream/tptp_94X
massList = range(1100,1800+1,100)
sigList = [whichSignal+'M'+str(mass) for mass in massList]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in massList for chiral in ['left','right']]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': 
	decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
	sigList.remove('BBM1700')
if whichSignal=='X53X53': decays = [''] #decays to tWtW 100% of the time
if whichSignal=='HTB': decays = ['']

doBRScan = False
if isCategorized and 'SR' in region: doBRScan = True
BRs={}
BRs['BW']=[0.0,0.50,1.0,0.0,0.0]#,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
BRs['TH']=[0.5,0.25,0.0,1.0,0.0]#,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]
BRs['TZ']=[0.5,0.25,0.0,0.0,1.0]#,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
nBRconf=len(BRs['BW'])
if not doBRScan: nBRconf=1

isEMlist =['E','M']
algolist = ['all']
<<<<<<< HEAD
if isCategorized or 'algos' in region or 'SR' in region: algolist = ['DeepAK8']#,'BEST'],'DeepAK8DC']
taglist = ['all']
if isCategorized: 
	taglist=['notV','notVtH','notVtZ','notVbW','taggedtHbW','taggedtZbW','taggedtZHtZH','taggedbWbW']
	if 'Counts' in pfix: taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH','notVtH','notVtZ','notVbW',
					'notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W']
	#isEMlist =['L']
	#taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH','notVtZ','notVbW','notVtH',
	#	 'notV3W0Z0H0T',
	#	 'notV2W0Z0H0T','notV2pW0Z0H1pT','notV2pW0Z1pH0pT','notV2pW1pZ0pH0pT',
	#	 'notV1W0Z0H0T','notV1W0Z1H0T','notV1W0Z0H1pT','notV1W0Z1H1pT','notV1W0Z2pH0pT','notV1W1Z0H0pT','notV1W1Z1pH0pT','notV1W2pZ0pH0pT',
	#	 'notV0W0Z0H0T','notV0W0Z1H0T','notV0W0Z0H1pT','notV0W0Z1H1pT','notV0W0Z2pH0pT','notV0W1Z0H0pT','notV0W1Z1pH0pT','notV0W2pZ0pH0pT']

	
# catList = ['is'+item[0]+'_nH'+item[1]+'_nW'+item[2]+'_nB'+item[3]+'_nJ'+item[4] for item in list(itertools.product(isEMlist,nHtaglist,nWtaglist,nbtaglist,njetslist))]
# #print catList
# tagList = ['nH'+item[0]+'_nW'+item[1]+'_nB'+item[2]+'_nJ'+item[3] for item in list(itertools.product(nHtaglist,nWtaglist,nbtaglist,njetslist))]
# #print tagList

# if isCategorized:
# 	for cat in catList:
# 		print cat
# 		if 'nH1b' in cat or 'nH2b' in cat:
# 			#print 'found H: ',cat
# 			if 'nW0p' not in cat: 
# 				catList.remove(cat)
# 				tagList.remove(cat[4:])
# 			if 'nB1p' not in cat: 
# 				catList.remove(cat)
# 				tagList.remove(cat[4:])
# 		else: # nH0 in SR, nH0p in CRs
# 			#print 'No H: ',cat[4:]
# 			if region != 'TTCR' and 'nW0p' in cat: 
# 				catList.remove(cat)
# 				tagList.remove(cat[4:])
# 			if 'nB1p' in cat: 
# 				catList.remove(cat)
# 				tagList.remove(cat[4:])

#catList = list(itertools.product(isEMlist,taglist,algolist))
#tagList = list(itertools.product(taglist,algolist))
catList = ['is'+item[0]+'_'+item[1]+'_'+item[2] for item in list(itertools.product(isEMlist,taglist,algolist))]
#tagList = [item[0] for item in list(itertools.product(taglist))]

lumiSys = 0.023 #lumi uncertainty
eltrigSys = 0.03 #electron trigger uncertainty
mutrigSys = 0.03 #muon trigger uncertainty
=======
if isCategorized or 'algos' in region: algolist = ['BEST','DeepAK8','DeepAK8DC']
taglist = ['all']
if isCategorized: taglist=['taggedbWbW','taggedtHbW','taggedtHtH','taggedtZbW','taggedtZtH','taggedtZtZ','taggedtZHtZH','notV']
	
catList = ['is'+item[0]+'_'+item[1]+'_'+item[2] for item in list(itertools.product(isEMlist,taglist,algolist))]

lumiSys = 0.024 #lumi uncertainty
eltrigSys = 0.01 #electron trigger uncertainty
mutrigSys = 0.01 #muon trigger uncertainty
>>>>>>> upstream/tptp_94X
elIdSys = 0.02 #electron id uncertainty
muIdSys = 0.02 #muon id uncertainty
elIsoSys = 0.01 #electron isolation uncertainty
muIsoSys = 0.01 #muon isolation uncertainty

elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)

if 'CR' in region: postTag = 'isCR_'
else: postTag = 'isSR_'
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
			
	for BRind in range(nBRconf):
		BRconfStr=''
		if doBRScan: BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
		print "       BR Configuration:"+BRconfStr
		#Initialize dictionaries for histograms
		hists={}
		print "RESETTING HISTS. NOW CATLIST = ",catList
		print "SIGLIST = ",sigList
		print "BRCONFSTR = ",BRconfStr
		for cat in catList:
			print "              processing cat: "+cat
			histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
			i=BRconfStr+cat
			#Group data processes
			hists['data'+i] = datahists[histoPrefix+'_'+dataList[0]].Clone(histoPrefix+'__DATA')
			for dat in dataList:
<<<<<<< HEAD
			      	#print 'dataList member',dat,'with integral',datahists[histoPrefix+'_'+dat].Integral()
=======
			      	print 'dataList member',dat,'with integral',datahists[histoPrefix+'_'+dat].Integral()
>>>>>>> upstream/tptp_94X
				if dat!=dataList[0]: hists['data'+i].Add(datahists[histoPrefix+'_'+dat])
			
			#Group processes
			for proc in bkgProcList+bkgGrupList:
				hists[proc+i] = bkghists[histoPrefix+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc)
				for bkg in bkgProcs[proc]:
					#print 'bkgList member',bkg,'with integral',bkghists[histoPrefix+'_'+bkg].Integral()
					if bkg!=bkgProcs[proc][0]: hists[proc+i].Add(bkghists[histoPrefix+'_'+bkg])

			#get signal
			for signal in sigList:
				hists[signal+i] = sighists[histoPrefix+'_'+signal+decays[0]].Clone(histoPrefix+'__sig')
				#print "Adding to hists...",signal+i
				if doBRScan: hists[signal+i].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
				for decay in decays:
					if decay!=decays[0]:
						htemp = sighists[histoPrefix+'_'+signal+decay].Clone()
						if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
						hists[signal+i].Add(htemp)
		#systematics
			if doAllSys:
				for syst in systematicList:
					for ud in ['Up','Down']:
						for proc in bkgProcList+bkgGrupList:
							if syst=='pdf': continue
							if syst=='toppt' and proc not in topptProcs: continue
							hists[proc+i+syst+ud] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc+'__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							for bkg in bkgProcs[proc]:
								if bkg!=bkgProcs[proc][0]: hists[proc+i+syst+ud].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
						if syst=='toppt' or syst=='pdf': continue
						for signal in sigList:
							hists[signal+i+syst+ud] = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							if doBRScan: hists[signal+i+syst+ud].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
							for decay in decays:
								htemp = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decay].Clone()
								if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
								if decay!=decays[0]: hists[signal+i+syst+ud].Add(htemp)
				if 'pdf' in systematicList:
					for pdfInd in range(100):
						for proc in bkgProcList+bkgGrupList:
							hists[proc+i+'pdf'+str(pdfInd)] = bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc+'__pdf'+str(pdfInd))
							for bkg in bkgProcs[proc]:
								if bkg!=bkgProcs[proc][0]: hists[proc+i+'pdf'+str(pdfInd)].Add(bkghists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+bkg])
						for signal in sigList:
							hists[signal+i+'pdf'+str(pdfInd)] = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__pdf'+str(pdfInd))
							if doBRScan: hists[signal+i+'pdf'+str(pdfInd)].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
							for decay in decays:
								htemp = sighists[histoPrefix.replace(discriminant,discriminant+'pdf'+str(pdfInd))+'_'+signal+decay].Clone()
								if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
								if decay!=decays[0]:hists[signal+i+'pdf'+str(pdfInd)].Add(htemp)
														
			#+/- 1sigma variations of shape systematics
			if doAllSys:
				for syst in systematicList:
					for ud in ['Up','Down']:
						for proc in bkgGrupList+bkgProcList+sigList:
							if syst=='toppt' and proc not in topptProcs: continue
							yieldTable[histoPrefix+syst+ud][proc] = hists[proc+i+syst+ud].Integral()
			#prepare yield table
			for proc in bkgGrupList+bkgProcList+sigList+['data']: yieldTable[histoPrefix][proc] = hists[proc+i].Integral()
			yieldTable[histoPrefix]['totBkg'] = sum([hists[proc+i].Integral() for proc in bkgGrupList])
			### REMEBER THIS SPOT
			#if yieldTable[histoPrefix]['totBkg'] == 0: continue
			yieldTable[histoPrefix]['dataOverBkg']= yieldTable[histoPrefix]['data']/yieldTable[histoPrefix]['totBkg']

			#prepare MC yield error table
			for proc in bkgGrupList+bkgProcList+sigList+['data']: yieldStatErrTable[histoPrefix][proc] = 0.
			yieldStatErrTable[histoPrefix]['totBkg'] = 0.
			yieldStatErrTable[histoPrefix]['dataOverBkg']= 0.

			for ibin in range(1,hists[bkgGrupList[0]+i].GetXaxis().GetNbins()+1):
				for proc in bkgGrupList+bkgProcList+sigList+['data']: yieldStatErrTable[histoPrefix][proc] += hists[proc+i].GetBinError(ibin)**2
				yieldStatErrTable[histoPrefix]['totBkg'] += sum([hists[proc+i].GetBinError(ibin)**2 for proc in bkgGrupList])
			for key in yieldStatErrTable[histoPrefix].keys(): yieldStatErrTable[histoPrefix][key] = math.sqrt(yieldStatErrTable[histoPrefix][key])

		#scale signal cross section to 1pb
		if scaleSignalXsecTo1pb:
			print "       SCALING SIGNAL TEMPLATES TO 1pb ..."
			for signal in sigList:
				for cat in catList:
					i=BRconfStr+cat
					hists[signal+i].Scale(1./xsec[signal])
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt' or syst=='pdf': continue
							hists[signal+i+syst+'Up'].Scale(1./xsec[signal])
							hists[signal+i+syst+'Down'].Scale(1./xsec[signal])
							if normalizeRENORM_PDF and (syst.startswith('mu') or syst=='pdf'):
<<<<<<< HEAD
								try:
									hists[signal+i+syst+'Up'].Scale(hists[signal+i].Integral()/hists[signal+i+syst+'Up'].Integral())
									hists[signal+i+syst+'Down'].Scale(hists[signal+i].Integral()/hists[signal+i+syst+'Down'].Integral())
								except:
									print "Couldn't normalize MU for",signal,i
									pass
=======
								hists[signal+i+syst+'Up'].Scale(hists[signal+i].Integral()/hists[signal+i+syst+'Up'].Integral())
								hists[signal+i+syst+'Down'].Scale(hsihistsg[signal+i].Integral()/hists[signal+i+syst+'Down'].Integral())
>>>>>>> upstream/tptp_94X
						if 'pdf' in systematicList:
							for pdfInd in range(100): 
								hists[signal+i+'pdf'+str(pdfInd)].Scale(1./xsec[signal])

		#Theta templates:
		print "       WRITING THETA TEMPLATES: "
		for signal in sigList:
			print "              ... "+signal
			thetaRfileName = outDir+'/templates_'+discriminant+'_'+signal+BRconfStr+'_'+lumiStr+'fb'+'.root'
			thetaRfile = TFile(thetaRfileName,'RECREATE')
			for cat in catList:
				i=BRconfStr+cat
				for proc in bkgGrupList:
					if hists[proc+i].Integral() > 0:
						hists[proc+i].Write()
						if doAllSys:
							for syst in systematicList:
								if syst=='toppt' and proc not in topptProcs: continue
								if syst=='pdf': continue
								hists[proc+i+syst+'Up'].Write()
								hists[proc+i+syst+'Down'].Write()
							if 'pdf' in systematicList:
								for pdfInd in range(100): hists[proc+i+'pdf'+str(pdfInd)].Write()
<<<<<<< HEAD
				for proc in [signal]:
					hists[proc+i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt' and proc not in topptProcs: continue
							if syst=='pdf': continue
							hists[proc+i+syst+'Up'].Write()
							hists[proc+i+syst+'Down'].Write()
						if 'pdf' in systematicList:
							for pdfInd in range(100): hists[proc+i+'pdf'+str(pdfInd)].Write()
=======
>>>>>>> upstream/tptp_94X
				hists['data'+i].Write()
			thetaRfile.Close()

		#Combine templates:
		'''
		print "       WRITING COMBINE TEMPLATES: "
		combineRfileName = outDir+'/templates_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.root'
		combineRfile = TFile(combineRfileName,'RECREATE')
		for cat in catList:
			print "              ... "+cat
			i=BRconfStr+cat
			for signal in sigList:
				mass = [str(mass) for mass in massList if str(mass) in signal][0]
				hists[signal+i].SetName(hists[signal+i].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass))
				hists[signal+i].Write()
				if doAllSys:
					for syst in systematicList:
						if syst=='toppt': continue
						hists[signal+i+syst+'Up'].SetName(hists[signal+i+syst+'Up'].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass).replace('__plus','Up'))
						hists[signal+i+syst+'Down'].SetName(hists[signal+i+syst+'Down'].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass).replace('__minus','Down'))
						hists[signal+i+syst+'Up'].Write()
						hists[signal+i+syst+'Down'].Write()
					for pdfInd in range(100): 
						hists[signal+i+'pdf'+str(pdfInd)].SetName(hists[signal+i+'pdf'+str(pdfInd)].GetName().replace('fb_','fb_'+postTag).replace('__sig','__'+signal.replace('M'+mass,'')+'M'+mass))
						hists[signal+i+'pdf'+str(pdfInd)].Write()
			for proc in bkgGrupList:
				hists[proc+i].SetName(hists[proc+i].GetName().replace('fb_','fb_'+postTag))
				hists[proc+i].Write()
				if doAllSys:
					for syst in systematicList:
						if syst=='toppt' and proc not in topptProcs: continue
						hists[proc+i+syst+'Up'].SetName(hists[proc+i+syst+'Up'].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
						hists[proc+i+syst+'Down'].SetName(hists[proc+i+syst+'Down'].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
						hists[proc+i+syst+'Up'].Write()
						hists[proc+i+syst+'Down'].Write()
					for pdfInd in range(100): 
						hists[proc+i+'pdf'+str(pdfInd)].SetName(hists[proc+i+'pdf'+str(pdfInd)].GetName().replace('fb_','fb_'+postTag))
						hists[proc+i+'pdf'+str(pdfInd)].Write()
				if doQ2sys:
					if proc+'_q2up' not in bkgProcs.keys(): continue
					hists[proc+i+'q2Up'].SetName(hists[proc+i+'q2Up'].GetName().replace('fb_','fb_'+postTag).replace('__plus','Up'))
					hists[proc+i+'q2Down'].SetName(hists[proc+i+'q2Down'].GetName().replace('fb_','fb_'+postTag).replace('__minus','Down'))
					hists[proc+i+'q2Up'].Write()
					hists[proc+i+'q2Down'].Write()
			hists['data'+i].SetName(hists['data'+i].GetName().replace('fb_','fb_'+postTag).replace('DATA','data_obs'))
			hists['data'+i].Write()
		combineRfile.Close()
		'''
<<<<<<< HEAD
=======
		######### THIS CRASHED SO WE COMMENTED IT OUT FOR NOW ###########
>>>>>>> upstream/tptp_94X
		# print "       WRITING SUMMARY TEMPLATES: "
		# for signal in sigList:
		# 	print "              ... "+signal
		# 	yldRfileName = outDir+'/templates_YLD_'+signal+BRconfStr+'_'+lumiStr+'fb.root'
		# 	yldRfile = TFile(yldRfileName,'RECREATE')
		# 	for isEM in isEMlist:	
		# 		for proc in bkgGrupList+['data',signal]:
		# 			yldHists = {}
		# 			yldHists[isEM+proc]=TH1F('YLD_'+lumiStr+'fb_is'+isEM+'_nH0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA'),'',len(tagList),0,len(tagList))
		# 			if doAllSys and proc!='data':
		# 				for syst in systematicList:
		# 					for ud in ['Up','Down']:
		# 						if syst=='toppt' and proc not in topptProcs: continue
		# 						yldHists[isEM+proc+syst+ud]=TH1F('YLD_'+lumiStr+'fb_is'+isEM+'_nH0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'),'',len(tagList),0,len(tagList))
		# 			ibin = 1
		# 			for cat in catList:
		# 				if 'is'+isEM not in cat: continue
		# 				nHtag = cat.split('_')[-4][2:]
		# 				nWtag = cat.split('_')[-3][2:]
		# 				nbtag = cat.split('_')[-2][2:]
		# 				njets = cat.split('_')[-1][2:]
		# 				binStr = ''
		# 				if nHtag!='0p':
		# 					if 'p' in nHtag: binStr+='#geq'+nHtag[:-1]+'t/'
		# 					else: binStr+=nHtag+'t/'
		# 				if nWtag!='0p':
		# 					if 'p' in nWtag: binStr+='#geq'+nWtag[:-1]+'W/'
		# 					else: binStr+=nWtag+'W/'
		# 				if nbtag!='0p':
		# 					if 'p' in nbtag: binStr+='#geq'+nbtag[:-1]+'b/'
		# 					else: binStr+=nbtag+'b/'
		# 				if njets!='0p' and len(njetslist)>1:
		# 					if 'p' in njets: binStr+='#geq'+njets[:-1]+'j'
		# 					else: binStr+=njets+'j'
		# 				if binStr.endswith('/'): binStr=binStr[:-1]
		# 				histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
		# 				yldHists[isEM+proc].SetBinContent(ibin,yieldTable[histoPrefix][proc])
		# 				yldHists[isEM+proc].SetBinError(ibin,yieldStatErrTable[histoPrefix][proc])
		# 				yldHists[isEM+proc].GetXaxis().SetBinLabel(ibin,binStr)
		# 				if doAllSys and proc!='data':
		# 					for syst in systematicList:
		# 						for ud in ['Up','Down']:
		# 							if syst=='toppt' and proc not in topptProcs: continue
		# 							yldHists[isEM+proc+syst+ud].SetBinContent(ibin,yieldTable[histoPrefix+syst+ud][proc])
		# 							yldHists[isEM+proc+syst+ud].GetXaxis().SetBinLabel(ibin,binStr)
		# 				ibin+=1
		# 			yldHists[isEM+proc].Write()
		# 			if doAllSys and proc!='data':
		# 				for syst in systematicList:
		# 					for ud in ['Up','Down']:
		# 						if syst=='toppt' and proc not in topptProcs: continue
		# 						yldHists[isEM+proc+syst+ud].Write()
		#	yldRfile.Close()
				
		table = []
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
<<<<<<< HEAD
			if isEM=='L': corrdSys = math.sqrt(elcorrdSys*elcorrdSys + mucorrdSys*mucorrdSys)
		#	g in nHtaglist:
=======

>>>>>>> upstream/tptp_94X
			table.append(['break'])
			table.append(['','is'+isEM+'_yields'])
			table.append(['break'])
			table.append(['YIELDS']+[cat for cat in catList if 'is'+isEM in cat]+['\\\\'])
			for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
				row = [proc]
				for cat in catList:
					if not ('is'+isEM in cat): continue
					histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
					yieldtemp = 0.
					yielderrtemp = 0.
					if proc=='totBkg' or proc=='dataOverBkg':
						for bkg in bkgGrupList:
							try:
								yieldtemp += yieldTable[histoPrefix][bkg]
								yielderrtemp += yieldStatErrTable[histoPrefix][bkg]**2
								yielderrtemp += (modelingSys[bkg]*yieldTable[histoPrefix][bkg])**2
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
						if proc not in sigList: yielderrtemp += (modelingSys[proc]*yieldtemp)**2
						yielderrtemp += (corrdSys*yieldtemp)**2
					yielderrtemp = math.sqrt(yielderrtemp)
					if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefix][proc])))
					else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
				row.append('\\\\')
				table.append(row)
		
		#yields for PAS tables (yields in e/m channels combined)
<<<<<<< HEAD
		#for nHtag in nHtaglist:
=======
>>>>>>> upstream/tptp_94X
		table.append(['break'])
		table.append(['','isL'+'_yields'])
		table.append(['break'])
		table.append(['YIELDS']+[cat.replace('isE','isL') for cat in catList if 'isE' in cat]+['\\\\'])
		for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
			row = [proc]
			for cat in catList:
				if not ('isE' in cat): continue
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
							yieldtemp  += yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]
							yielderrtemp += yieldStatErrTable[histoPrefixE][bkg]**2+yieldStatErrTable[histoPrefixM][bkg]**2
							yielderrtemp += (modelingSys[bkg]*(yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]))**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						except:
							print "Missing",bkg,"for channel:",cat
							pass
					yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
					if proc=='dataOverBkg':
						dataTemp = yieldTable[histoPrefixE]['data']+yieldTable[histoPrefixM]['data']+1e-20
						dataTempErr = yieldStatErrTable[histoPrefixE]['data']**2+yieldStatErrTable[histoPrefixM]['data']**2
						yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
						yieldtemp = dataTemp/yieldtemp
				else:
					try:
						yieldtempE += yieldTable[histoPrefixE][proc]
						yieldtempM += yieldTable[histoPrefixM][proc]
						yieldtemp  += yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc]
						yielderrtemp += yieldStatErrTable[histoPrefixE][proc]**2+yieldStatErrTable[histoPrefixM][proc]**2
					except:
						print "Missing",proc,"for channel:",cat
						pass
					if proc not in sigList: yielderrtemp += (modelingSys[proc]*yieldtemp)**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
					yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
				yielderrtemp = math.sqrt(yielderrtemp)
				if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc])))
				else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
			row.append('\\\\')
			table.append(row)

		#systematics
		if doAllSys:
			table.append(['break'])
			table.append(['','Systematics'])
			table.append(['break'])
			for proc in bkgGrupList+sigList:
				table.append([proc]+[cat for cat in catList]+['\\\\'])
				for syst in sorted(systematicList):
					for ud in ['Up','Down']:
						row = [syst+ud]
						for cat in catList:
							histoPrefix = discriminant+'_'+lumiStr+'fb_'+cat
							nomHist = histoPrefix
							shpHist = histoPrefix+syst+ud
							try: row.append(' & '+str(round(yieldTable[shpHist][proc]/(yieldTable[nomHist][proc]+1e-20),2)))
							except:
								if not ((syst=='toppt' and proc not in topptProcs)):
									print "Missing",proc,"for channel:",cat,"and systematic:",syst
								pass
						row.append('\\\\')
						table.append(row)
				table.append(['break'])
			
		if not addCRsys: out=open(outDir+'/yields_noCRunc_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.txt','w')
		else: out=open(outDir+'/yields_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.txt','w')
		printTable(table,out)

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

iPlotList = []
print 'outDir:',outDir,'catList[0][2:]',catList[0][2:]
for file in findfiles(outDir+'/'+catList[0][2:]+'/', '*.p'):
    if 'bkghists' not in file: continue
    if not os.path.exists(file.replace('bkghists','datahists')): continue
    if not os.path.exists(file.replace('bkghists','sighists')): continue
    iPlotList.append(file.split('_')[-1][:-2])
#iPlotList = ['HT']
print 'Plot list:',iPlotList

checkprint = False
for iPlot in iPlotList:
<<<<<<< HEAD
	#if 'CR' in region:
		#if iPlot == 'probSumDecay': continue
		#if iPlot == 'probSumFour': continue
	#if region == 'SR' and isCategorized:
	#	if iPlot == 'ST': continue
	datahists = {} 
	bkghists  = {}
	sighists  = {}
	#if iPlot!='HT': continue
=======
	datahists = {} 
	bkghists  = {}
	sighists  = {}

>>>>>>> upstream/tptp_94X
	print "LOADING DISTRIBUTION: "+iPlot
	for cat in catList:
		print "         ",cat[2:]
		datahists.update(pickle.load(open(outDir+'/'+cat[2:]+'/datahists_'+iPlot+'.p','rb')))
		bkghists.update(pickle.load(open(outDir+'/'+cat[2:]+'/bkghists_'+iPlot+'.p','rb')))
		sighists.update(pickle.load(open(outDir+'/'+cat[2:]+'/sighists_'+iPlot+'.p','rb')))
	if scaleLumi:
		for key in bkghists.keys(): bkghists[key].Scale(lumiScaleCoeff)	    		
		for key in sighists.keys(): sighists[key].Scale(lumiScaleCoeff)

	checkprint = False
	print 'sighists check:'
	for key in sighists:
		if 'MET_' in key and 'TTM800' in key: print key
	print "       MAKING CATEGORIES FOR TOTAL SIGNALS ..."
<<<<<<< HEAD
	#try:
	makeThetaCats(datahists,sighists,bkghists,iPlot)
	#except:
	#	print 'makeThetaCats failed for iPlot:',iPlot
	#	pass
=======
	try:
		makeThetaCats(datahists,sighists,bkghists,iPlot)
	except:
		print 'makeThetaCats failed for iPlot:',iPlot
		pass
>>>>>>> upstream/tptp_94X

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))
