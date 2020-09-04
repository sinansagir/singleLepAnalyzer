#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools,fnmatch
from ROOT import gROOT,TFile,TH1F
from array import array
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
#from weights import *
from modSyst import *
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

year='R17'
saveKey = ''#'_ttHFupLFdown'
cutString = ''#'lep30_MET100_NJets4_DR1_1jet250_2jet50'
theDir = 'kinematics_SR_'+year+'_nonjetsf_2020_8_31'
outDir = os.getcwd()+'/'+theDir+'/'+cutString

writeSummaryHists = True
scaleSignalXsecTo1pb = False # !!!!!Make sure you know signal x-sec used in input files to this script. If this is True, it will scale signal histograms by 1/x-sec in weights.py!!!!!
lumiScaleCoeff = 1. # Rescale luminosity used in doHists.py
ttHFsf = 4.7/3.9 # from TOP-18-002 (v34) Table 4, set it to 1, if no ttHFsf is wanted.
ttLFsf = -1 # if it is set to -1, ttLFsf is calculated based on ttHFsf in order to keep overall normalization unchanged. Otherwise, it will be used as entered. If no ttLFsf is wanted, set it to 1.
doAllSys = True
doHDsys = True
doUEsys = True
doPDF = True
addCRsys = False
systematicList = ['pileup','prefire','muRFcorrd','muR','muF','isr','fsr','btag','mistag','jec','jer','hotstat','hotcspur','hotclosure','njet','njetsf'] # ,'tau32','jmst','jmrt','tau21','jmsW','jmrW','tau21pt','ht','trigeff','toppt'
normalizeRENORM_PDF = False #normalize the renormalization/pdf uncertainties to nominal templates --> normalizes signal processes only !!!!
rebinBy = -1 #performs a regular rebinning with "Rebin(rebinBy)", put -1 if rebinning is not wanted
zero = 1E-12
removeThreshold = 0.015 # If a process/totalBkg is less than the threshold, the process will be removed in the output files!

ttbarGrupList = ['ttnobb','ttbb']
bkgGrupList = ttbarGrupList+['top','ewk','qcd']
ttbarProcList = ['ttjj','ttcc','ttbb','tt1b','tt2b']
bkgProcList = ttbarProcList+['T','TTV','TTXY','WJets','ZJets','VV','qcd']
bkgProcs = {}
bkgProcs['WJets'] = ['WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800']
if year=='R17':
	bkgProcs['WJets']+= ['WJetsMG12001','WJetsMG12002','WJetsMG12003','WJetsMG25002','WJetsMG25003','WJetsMG25004']
elif year=='R18':
	bkgProcs['WJets']+= ['WJetsMG1200','WJetsMG2500']
bkgProcs['ZJets']  = ['DYMG200','DYMG400','DYMG600','DYMG800','DYMG1200','DYMG2500']
bkgProcs['VV']     = ['WW','WZ','ZZ']
TTlist = ['TTJetsHad','TTJets2L2nu','TTJetsSemiLepNjet9bin','TTJetsSemiLepNjet0','TTJetsSemiLepNjet9']
bkgProcs['tt1b']  = [tt+'TT1b' for tt in TTlist]
bkgProcs['tt2b']  = [tt+'TT2b' for tt in TTlist]
bkgProcs['ttbj']  = bkgProcs['tt1b'] + bkgProcs['tt2b']
bkgProcs['ttbb']  = [tt+'TTbb' for tt in TTlist]
bkgProcs['ttcc']  = [tt+'TTcc' for tt in TTlist]
bkgProcs['ttjj']  = [tt+'TTjj' for tt in TTlist if tt!='TTJetsSemiLepNjet0']
if year=='R17':
	bkgProcs['ttjj'] += ['TTJetsSemiLepNjet0TTjj'+tt for tt in ['1','2','3','4','5']]
elif year=='R18':
	bkgProcs['ttjj'] += ['TTJetsSemiLepNjet0TTjj'+tt for tt in ['1','2']]
bkgProcs['ttnobb']  = bkgProcs['ttjj'] + bkgProcs['ttcc'] + bkgProcs['tt1b'] + bkgProcs['tt2b']
bkgProcs['T'] = ['Ts','Tt','Tbt','TtW','TbtW']
if year=='R17': bkgProcs['T']+= ['Tbs']
bkgProcs['TTV'] = ['TTWl','TTZlM10','TTZlM1to10','TTHB','TTHnoB']
bkgProcs['TTXY']= ['TTHH','TTTJ','TTTW','TTWH','TTWW','TTWZ','TTZH','TTZZ']
bkgProcs['qcd'] = ['QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000']
bkgProcs['top'] = bkgProcs['T']+bkgProcs['TTV']+bkgProcs['TTXY']#+bkgProcs['TTJets']
bkgProcs['ewk'] = bkgProcs['WJets']+bkgProcs['ZJets']+bkgProcs['VV']
dataList = ['DataE','DataM']#,'DataJ']

htProcs = ['ewk','WJets','qcd']
topptProcs = ['ttjj','ttcc','ttbb','tt1b','tt2b','ttbj','ttnobb']
for hf in ['jj','cc','bb','1b','2b']:
	bkgProcs['tt'+hf+'_hdup'] = ['TTJetsHadHDAMPupTT'+hf,'TTJets2L2nuHDAMPupTT'+hf,'TTJetsSemiLepHDAMPupTT'+hf]
	bkgProcs['tt'+hf+'_hddn'] = ['TTJetsHadHDAMPdnTT'+hf,'TTJets2L2nuHDAMPdnTT'+hf,'TTJetsSemiLepHDAMPdnTT'+hf]
	bkgProcs['tt'+hf+'_ueup'] = ['TTJetsHadUEupTT'+hf,'TTJets2L2nuUEupTT'+hf,'TTJetsSemiLepUEupTT'+hf]
	bkgProcs['tt'+hf+'_uedn'] = ['TTJetsHadUEdnTT'+hf,'TTJets2L2nuUEdnTT'+hf,'TTJetsSemiLepUEdnTT'+hf]
for syst in ['hdup','hddn','ueup','uedn']:
	bkgProcs['ttbj_'+syst] = bkgProcs['tt1b_'+syst] + bkgProcs['tt2b_'+syst]
	bkgProcs['ttnobb_'+syst] = bkgProcs['ttjj_'+syst] + bkgProcs['ttcc_'+syst]+bkgProcs['tt1b_'+syst] + bkgProcs['tt2b_'+syst]

whichSignal = 'tttt' #HTB, TT, BB, X53 or tttt
massList = [690]#range(800,1600+1,100)
sigList = [whichSignal+'M'+str(mass) for mass in massList]
if whichSignal=='tttt': sigList = [whichSignal]
if whichSignal=='X53': 
	sigList = [whichSignal+'LHM'+str(mass) for mass in [1100,1200,1400,1700]]
	sigList+= [whichSignal+'RHM'+str(mass) for mass in range(900,1700+1,100)]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
elif whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
else: decays = [''] #there is only one possible decay mode!

doBRScan = False
BRs={}
BRs['BW']=[0.0,0.50,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
BRs['TH']=[0.5,0.25,0.0,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]
BRs['TZ']=[0.5,0.25,1.0,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
nBRconf=len(BRs['BW'])
if not doBRScan: nBRconf=1

if year=='R17':
	from weights17 import *
else:
	from weights18 import *

lumiStr = str(targetlumi/1000).replace('.','p')+'fb' # 1/fb
if theDir.startswith('kinematics'): removeThreshold = 0.0
if not doAllSys: 
	doHDsys = False
	doUEsys = False
	doPDF = False
# if doPDF: writeSummaryHists = False

lumiSys = 0.025 # lumi uncertainty
if year=='R17': lumiSys = 0.023
eltrigSys = 0.0 #electron trigger uncertainty
mutrigSys = 0.0 #muon trigger uncertainty
elIdSys = 0.03 #electron id uncertainty
muIdSys = 0.03 #muon id uncertainty
elIsoSys = 0.0 #electron isolation uncertainty
muIsoSys = 0.0 #muon isolation uncertainty
#njetSys = 0.048
#if year=='R17': njetSys = 0.075
elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)#+njetSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)#+njetSys**2)

if not os.path.exists(outDir): 
	print outDir,'DOES NOT EXIST!!!'
	os._exit(1)
isEMlist = ['E','M']
catList = ['is'+x for x in os.walk(outDir).next()[1] if x.startswith('E_') or x.startswith('M_')]
catList.sort()
tagList = [x[4:] for x in catList if 'isE' in x]
nhottlist = list(set([x.split('_')[0] for x in tagList]))
nttaglist = list(set([x.split('_')[1] for x in tagList]))
nWtaglist = list(set([x.split('_')[2] for x in tagList]))
nbtaglist = list(set([x.split('_')[3] for x in tagList]))
njetslist = list(set([x.split('_')[4] for x in tagList]))

for tag in tagList:
	modTag = tag[tag.find('nT'):tag.find('nJ')-3]
	modelingSys['data_'+modTag] = 0.
	modelingSys['qcd_'+modTag] = 0.
	if not addCRsys: #else CR uncertainties are defined in modSyst.py module 
		for proc in bkgProcs.keys():
			modelingSys[proc+'_'+modTag] = 0.

def gettime():
	return str(round((time.time() - start_time)/60,2))+'mins'

###########################################################
#################### CATEGORIZATION #######################
###########################################################
def makeCatTemplates(datahists,sighists,bkghists,discriminant):
	yieldTable = {}
	yieldStatErrTable = {}
	for cat in catList:
		histoPrefix=discriminant+'_'+lumiStr+'_'+cat
		yieldTable[histoPrefix]={}
		yieldStatErrTable[histoPrefix]={}
		if doAllSys:
			for syst in systematicList:
				for ud in ['Up','Down']:
					yieldTable[histoPrefix+syst+ud]={}
			
		if doHDsys:
			yieldTable[histoPrefix+'hdUp']={}
			yieldTable[histoPrefix+'hdDown']={}
		if doUEsys:
			yieldTable[histoPrefix+'ueUp']={}
			yieldTable[histoPrefix+'ueDown']={}

	for BRind in range(nBRconf):
		BRconfStr=''
		if doBRScan: BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
		print "       BR Configuration:"+BRconfStr
		#Initialize dictionaries for histograms
		hists={}
		for cat in catList:
			print "              processing cat: "+cat,gettime()
			histoPrefix=discriminant+'_'+lumiStr+'_'+cat
			i=BRconfStr+cat

			#Group data processes
			hists['data'+i] = datahists[histoPrefix+'_'+dataList[0]].Clone(histoPrefix+'__DATA')
			for dat in dataList:
				if dat!=dataList[0]: hists['data'+i].Add(datahists[histoPrefix+'_'+dat])
			
			#Group processes
			for proc in bkgProcList+bkgGrupList:
				hists[proc+i] = bkghists[histoPrefix+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc)
				for bkg in bkgProcs[proc]:
					if bkg!=bkgProcs[proc][0]: hists[proc+i].Add(bkghists[histoPrefix+'_'+bkg])
	
			#get signal
			for signal in sigList:
				hists[signal+i] = sighists[histoPrefix+'_'+signal+decays[0]].Clone(histoPrefix+'__sig')
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
							if syst=='toppt' and proc not in topptProcs: continue
							if syst=='ht' and proc not in htProcs: continue
							hists[proc+i+syst+ud] = bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkgProcs[proc][0]].Clone(histoPrefix+'__'+proc+'__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							for bkg in bkgProcs[proc]:
								if bkg!=bkgProcs[proc][0]: hists[proc+i+syst+ud].Add(bkghists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+bkg])
						if syst=='toppt' or syst=='ht': continue
						for signal in sigList:
							hists[signal+i+syst+ud] = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decays[0]].Clone(histoPrefix+'__sig__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'))
							if doBRScan: hists[signal+i+syst+ud].Scale(BRs[decays[0][:2]][BRind]*BRs[decays[0][2:]][BRind]/(BR[decays[0][:2]]*BR[decays[0][2:]]))
							for decay in decays:
								htemp = sighists[histoPrefix.replace(discriminant,discriminant+syst+ud)+'_'+signal+decay].Clone()
								if doBRScan: htemp.Scale(BRs[decay[:2]][BRind]*BRs[decay[2:]][BRind]/(BR[decay[:2]]*BR[decay[2:]]))
								if decay!=decays[0]: hists[signal+i+syst+ud].Add(htemp)
			if doPDF:
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
											
			if doHDsys:
				for proc in bkgProcList+bkgGrupList:
					if proc+'_hdup' not in bkgProcs.keys(): continue
					hists[proc+i+'hdUp'] = bkghists[histoPrefix+'_'+bkgProcs[proc+'_hdup'][0]].Clone(histoPrefix+'__'+proc+'__hdamp__plus')
					hists[proc+i+'hdDown'] = bkghists[histoPrefix+'_'+bkgProcs[proc+'_hddn'][0]].Clone(histoPrefix+'__'+proc+'__hdamp__minus')
					for bkg in bkgProcs[proc+'_hdup']:
						if bkg!=bkgProcs[proc+'_hdup'][0]: hists[proc+i+'hdUp'].Add(bkghists[histoPrefix+'_'+bkg])
					for bkg in bkgProcs[proc+'_hddn']:
						if bkg!=bkgProcs[proc+'_hddn'][0]: hists[proc+i+'hdDown'].Add(bkghists[histoPrefix+'_'+bkg])
			if doUEsys:
				for proc in bkgProcList+bkgGrupList:
					if proc+'_ueup' not in bkgProcs.keys(): continue
					hists[proc+i+'ueUp'] = bkghists[histoPrefix+'_'+bkgProcs[proc+'_ueup'][0]].Clone(histoPrefix+'__'+proc+'__ue__plus')
					hists[proc+i+'ueDown'] = bkghists[histoPrefix+'_'+bkgProcs[proc+'_uedn'][0]].Clone(histoPrefix+'__'+proc+'__ue__minus')
					for bkg in bkgProcs[proc+'_ueup']:
						if bkg!=bkgProcs[proc+'_ueup'][0]: hists[proc+i+'ueUp'].Add(bkghists[histoPrefix+'_'+bkg])
					for bkg in bkgProcs[proc+'_uedn']:
						if bkg!=bkgProcs[proc+'_uedn'][0]: hists[proc+i+'ueDown'].Add(bkghists[histoPrefix+'_'+bkg])
		
			for hist in hists.keys(): hists[hist].SetDirectory(0)

			#scale tt+bb (and optionally scale down tt+nobb)
			if ttHFsf!=1 and 'ttbb' in ttbarGrupList:
				print "                     SCALING tt+bb BY A FACTOR OF",ttHFsf,gettime()
				Nttbb = hists['ttbb'+i].Integral()
				Nttnobb = 0.
				for tt in ttbarGrupList:
					if tt!='ttbb': Nttnobb += hists[tt+i].Integral()
				ttLFsf_ = ttLFsf
				if ttLFsf==-1: ttLFsf_ = 1. + ( 1-ttHFsf ) * ( Nttbb/Nttnobb )
				hists['ttbb'+i].Scale(ttHFsf)
				for tt in list(set(ttbarProcList+ttbarGrupList)):
					if tt!='ttbb': hists[tt+i].Scale(ttLFsf_)
				if doAllSys:
					for syst in systematicList:
						hists['ttbb'+i+syst+'Up'].Scale(ttHFsf)
						hists['ttbb'+i+syst+'Down'].Scale(ttHFsf)
						for tt in list(set(ttbarProcList+ttbarGrupList)):
							if tt!='ttbb': #scale down tt+nobb
								hists[tt+i+syst+'Up'].Scale(ttLFsf_)
								hists[tt+i+syst+'Down'].Scale(ttLFsf_)
				if doPDF:
					for pdfInd in range(100): 
						hists['ttbb'+i+'pdf'+str(pdfInd)].Scale(ttHFsf)
						for tt in list(set(ttbarProcList+ttbarGrupList)):
							if tt!='ttbb': #scale down tt+nobb
								hists[tt+i+'pdf'+str(pdfInd)].Scale(ttLFsf_)
				if doHDsys:
					hists['ttbb'+i+'hdUp'].Scale(ttHFsf)
					hists['ttbb'+i+'hdDown'].Scale(ttHFsf)
					for tt in list(set(ttbarProcList+ttbarGrupList)):
						if tt!='ttbb': #scale down tt+nobb
							hists[tt+i+'hdUp'].Scale(ttLFsf_)
							hists[tt+i+'hdDown'].Scale(ttLFsf_)
				if doUEsys:
					hists['ttbb'+i+'ueUp'].Scale(ttHFsf)
					hists['ttbb'+i+'ueDown'].Scale(ttHFsf)
					for tt in list(set(ttbarProcList+ttbarGrupList)):
						if tt!='ttbb': #scale down tt+nobb
							hists[tt+i+'ueUp'].Scale(ttLFsf_)
							hists[tt+i+'ueDown'].Scale(ttLFsf_)
										
			#+/- 1sigma variations of shape systematics
			if doAllSys:
				for syst in systematicList:
					for ud in ['Up','Down']:
						for proc in bkgGrupList+bkgProcList+sigList:
							if syst=='toppt' and proc not in topptProcs: continue
							if syst=='ht' and proc not in htProcs: continue
							yieldTable[histoPrefix+syst+ud][proc] = hists[proc+i+syst+ud].Integral()
			if doHDsys:
				for proc in bkgProcList+bkgGrupList:
					if proc+'_hdup' not in bkgProcs.keys(): continue
					yieldTable[histoPrefix+'hdUp'][proc] = hists[proc+i+'hdUp'].Integral()
					yieldTable[histoPrefix+'hdDown'][proc] = hists[proc+i+'hdDown'].Integral()
			if doUEsys:
				for proc in bkgProcList+bkgGrupList:
					if proc+'_ueup' not in bkgProcs.keys(): continue
					yieldTable[histoPrefix+'ueUp'][proc] = hists[proc+i+'ueUp'].Integral()
					yieldTable[histoPrefix+'ueDown'][proc] = hists[proc+i+'ueDown'].Integral()

			#prepare yield table
			for proc in bkgGrupList+bkgProcList+sigList+['data']: yieldTable[histoPrefix][proc] = hists[proc+i].Integral()
			yieldTable[histoPrefix]['totBkg'] = sum([hists[proc+i].Integral() for proc in bkgGrupList])
			yieldTable[histoPrefix]['dataOverBkg']= yieldTable[histoPrefix]['data']/(yieldTable[histoPrefix]['totBkg']+zero)

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
			print "       SCALING SIGNAL TEMPLATES TO 1pb ...",gettime()
			for signal in sigList:
				for cat in catList:
					i=BRconfStr+cat
					hists[signal+i].Scale(1./xsec[signal])
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt' or syst=='ht': continue
							hists[signal+i+syst+'Up'].Scale(1./xsec[signal])
							hists[signal+i+syst+'Down'].Scale(1./xsec[signal])
							if normalizeRENORM_PDF and (syst.startswith('mu') or syst=='pdf'):
								hists[signal+i+syst+'Up'].Scale(hists[signal+i].Integral()/hists[signal+i+syst+'Up'].Integral())
								hists[signal+i+syst+'Down'].Scale(hsihistsg[signal+i].Integral()/hists[signal+i+syst+'Down'].Integral())
					if doPDF:
						for pdfInd in range(100): 
							hists[signal+i+'pdf'+str(pdfInd)].Scale(1./xsec[signal])

		#Theta templates:
		print "       WRITING THETA TEMPLATES: "
		for signal in sigList:
			print "              ... "+signal,gettime()
			thetaRfileName = outDir+'/templates_'+discriminant+'_'+signal+BRconfStr+'_'+lumiStr+saveKey+'.root'
			thetaRfile = TFile(thetaRfileName,'RECREATE')
			for cat in catList:
				i=BRconfStr+cat
				totBkg_ = sum([hists[proc+i].Integral() for proc in bkgGrupList])
				for proc in bkgGrupList+[signal]:
					if proc in bkgGrupList and hists[proc+i].Integral()/totBkg_ <= removeThreshold:
						print proc+i,'IS',
						if hists[proc+i].Integral()==0: print 'EMPTY! SKIPPING ...'
						else: print '< '+str(removeThreshold*100)+'% OF TOTAL BKG! SKIPPING ...'
						continue
					hists[proc+i].Write()
					if doAllSys:
						for syst in systematicList:
							if syst=='toppt' and proc not in topptProcs: continue
							if syst=='ht' and proc not in htProcs: continue
							if hists[proc+i+syst+'Up'].Integral()==0: hists[proc+i+syst+'Up'].SetBinContent(1,zero)
							if hists[proc+i+syst+'Down'].Integral()==0: hists[proc+i+syst+'Down'].SetBinContent(1,zero)
							hists[proc+i+syst+'Up'].Write()
							hists[proc+i+syst+'Down'].Write()
					if doPDF:
						for pdfInd in range(100): hists[proc+i+'pdf'+str(pdfInd)].Write()
					if doHDsys:
						if proc+'_hdup' not in bkgProcs.keys(): continue
						hists[proc+i+'hdUp'].Write()
						hists[proc+i+'hdDown'].Write()
					if doUEsys:
						if proc+'_ueup' not in bkgProcs.keys(): continue
						hists[proc+i+'ueUp'].Write()
						hists[proc+i+'ueDown'].Write()
				hists['data'+i].Write()
			thetaRfile.Close()

		#Combine templates:
		print "       WRITING COMBINE TEMPLATES: "
		combineRfileName = outDir+'/templates_'+discriminant+BRconfStr+'_'+lumiStr+saveKey+'.root'
		combineRfile = TFile(combineRfileName,'RECREATE')
		for cat in catList:
			print "              ... "+cat,gettime()
			i=BRconfStr+cat
			for signal in sigList:
				hists[signal+i].SetName(hists[signal+i].GetName().replace('__sig','__'+signal))
				hists[signal+i].Write()
				if doAllSys:
					for syst in systematicList:
						if syst=='toppt' or syst=='ht': continue
						hists[signal+i+syst+'Up'].SetName(hists[signal+i+syst+'Up'].GetName().replace('__sig','__'+signal).replace('__plus','Up'))
						hists[signal+i+syst+'Down'].SetName(hists[signal+i+syst+'Down'].GetName().replace('__sig','__'+signal).replace('__minus','Down'))
						hists[signal+i+syst+'Up'].Write()
						hists[signal+i+syst+'Down'].Write()
				if doPDF:
					for pdfInd in range(100): 
						hists[signal+i+'pdf'+str(pdfInd)].SetName(hists[signal+i+'pdf'+str(pdfInd)].GetName().replace('__sig','__'+signal))
						hists[signal+i+'pdf'+str(pdfInd)].Write()
			totBkg_ = sum([hists[proc+i].Integral() for proc in bkgGrupList])
			for proc in bkgGrupList:
				if hists[proc+i].Integral()/totBkg_ <= removeThreshold:
					print proc+i,'IS',
					if hists[proc+i].Integral()==0: print 'EMPTY! SKIPPING ...'
					else: print '< '+str(removeThreshold*100)+'% OF TOTAL BKG! SKIPPING ...'
					continue
				hists[proc+i].SetName(hists[proc+i].GetName())
				if hists[proc+i].Integral() == 0: hists[proc+i].SetBinContent(1,zero)
				hists[proc+i].Write()
				if doAllSys:
					for syst in systematicList:
						if syst=='toppt' and proc not in topptProcs: continue
						if syst=='ht' and proc not in htProcs: continue
						hists[proc+i+syst+'Up'].SetName(hists[proc+i+syst+'Up'].GetName().replace('__plus','Up'))
						hists[proc+i+syst+'Down'].SetName(hists[proc+i+syst+'Down'].GetName().replace('__minus','Down'))
						hists[proc+i+syst+'Up'].Write()
						hists[proc+i+syst+'Down'].Write()
				if doPDF:
					for pdfInd in range(100): 
						hists[proc+i+'pdf'+str(pdfInd)].SetName(hists[proc+i+'pdf'+str(pdfInd)].GetName())
						hists[proc+i+'pdf'+str(pdfInd)].Write()
				if doHDsys:
					if proc+'_hdup' not in bkgProcs.keys(): continue
					hists[proc+i+'hdUp'].SetName(hists[proc+i+'hdUp'].GetName().replace('__plus','Up'))
					hists[proc+i+'hdDown'].SetName(hists[proc+i+'hdDown'].GetName().replace('__minus','Down'))
					hists[proc+i+'hdUp'].Write()
					hists[proc+i+'hdDown'].Write()
				if doUEsys:
					if proc+'_ueup' not in bkgProcs.keys(): continue
					hists[proc+i+'ueUp'].SetName(hists[proc+i+'ueUp'].GetName().replace('__plus','Up'))
					hists[proc+i+'ueDown'].SetName(hists[proc+i+'ueDown'].GetName().replace('__minus','Down'))
					hists[proc+i+'ueUp'].Write()
					hists[proc+i+'ueDown'].Write()
			hists['data'+i].SetName(hists['data'+i].GetName().replace('DATA','data_obs'))
			hists['data'+i].Write()
		combineRfile.Close()

		print "       WRITING SUMMARY TEMPLATES: "
		for signal in sigList:
			if not writeSummaryHists: break
			print "              ... "+signal,gettime()
			yldRfileName = outDir+'/templates_YLD_'+signal+BRconfStr+'_'+lumiStr+saveKey+'.root'
			yldRfile = TFile(yldRfileName,'RECREATE')
			for isEM in isEMlist:	
				for proc in bkgGrupList+['data',signal]:
					yldHists = {}
					yldHists[isEM+proc]=TH1F('YLD_'+lumiStr+'_is'+isEM+'_nHOT0p_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA'),'',len(tagList),0,len(tagList))
					if doAllSys and proc!='data':
						for syst in systematicList:
							for ud in ['Up','Down']:
								if syst=='toppt' and proc not in topptProcs: continue
								if syst=='ht' and proc not in htProcs: continue
								yldHists[isEM+proc+syst+ud]=TH1F('YLD_'+lumiStr+'_is'+isEM+'_nHOT0p_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'),'',len(tagList),0,len(tagList))
					if doHDsys and proc+'_hdup' in bkgProcs.keys(): 
						yldHists[isEM+proc+'hdUp']  =TH1F('YLD_'+lumiStr+'_is'+isEM+'_nHOT0p_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__hdamp__plus','',len(tagList),0,len(tagList))
						yldHists[isEM+proc+'hdDown']=TH1F('YLD_'+lumiStr+'_is'+isEM+'_nHOT0p_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__hdamp__minus','',len(tagList),0,len(tagList))
					if doUEsys and proc+'_ueup' in bkgProcs.keys(): 
						yldHists[isEM+proc+'ueUp']  =TH1F('YLD_'+lumiStr+'_is'+isEM+'_nHOT0p_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__ue__plus','',len(tagList),0,len(tagList))
						yldHists[isEM+proc+'ueDown']=TH1F('YLD_'+lumiStr+'_is'+isEM+'_nHOT0p_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__ue__minus','',len(tagList),0,len(tagList))
					ibin = 1
					for cat in catList:
						if 'is'+isEM not in cat: continue
						nhottag = cat.split('_')[-5][4:]
						nttag = cat.split('_')[-4][2:]
						nWtag = cat.split('_')[-3][2:]
						nbtag = cat.split('_')[-2][2:]
						njets = cat.split('_')[-1][2:]
						binStr = ''
						if nhottag!='0p':
							if 'p' in nhottag: binStr+='#geq'+nhottag[:-1]+'res-t/'
							else: binStr+=nhottag+'res-t/'
						if nttag!='0p':
							if 'p' in nttag: binStr+='#geq'+nttag[:-1]+'t/'
							else: binStr+=nttag+'t/'
						if nWtag!='0p':
							if 'p' in nWtag: binStr+='#geq'+nWtag[:-1]+'W/'
							else: binStr+=nWtag+'W/'
						if nbtag!='0p':
							if 'p' in nbtag: binStr+='#geq'+nbtag[:-1]+'b/'
							else: binStr+=nbtag+'b/'
						if njets!='0p' and len(njetslist)>1:
							if 'p' in njets: binStr+='#geq'+njets[:-1]+'j'
							else: binStr+=njets+'j'
						if binStr.endswith('/'): binStr=binStr[:-1]
						histoPrefix=discriminant+'_'+lumiStr+'_'+cat
						yldHists[isEM+proc].SetBinContent(ibin,yieldTable[histoPrefix][proc])
						yldHists[isEM+proc].SetBinError(ibin,yieldStatErrTable[histoPrefix][proc])
						yldHists[isEM+proc].GetXaxis().SetBinLabel(ibin,binStr)
						if doAllSys and proc!='data':
							for syst in systematicList:
								for ud in ['Up','Down']:
									if syst=='toppt' and proc not in topptProcs: continue
									if syst=='ht' and proc not in htProcs: continue
									yldHists[isEM+proc+syst+ud].SetBinContent(ibin,yieldTable[histoPrefix+syst+ud][proc])
									yldHists[isEM+proc+syst+ud].GetXaxis().SetBinLabel(ibin,binStr)
						if doHDsys and proc+'_hdup' in bkgProcs.keys(): 
							yldHists[isEM+proc+'hdUp'].SetBinContent(ibin,yieldTable[histoPrefix+'hdUp'][proc])
							yldHists[isEM+proc+'hdUp'].GetXaxis().SetBinLabel(ibin,binStr)
							yldHists[isEM+proc+'hdDown'].SetBinContent(ibin,yieldTable[histoPrefix+'hdDown'][proc])
							yldHists[isEM+proc+'hdDown'].GetXaxis().SetBinLabel(ibin,binStr)
						if doUEsys and proc+'_ueup' in bkgProcs.keys(): 
							yldHists[isEM+proc+'ueUp'].SetBinContent(ibin,yieldTable[histoPrefix+'ueUp'][proc])
							yldHists[isEM+proc+'ueUp'].GetXaxis().SetBinLabel(ibin,binStr)
							yldHists[isEM+proc+'ueDown'].SetBinContent(ibin,yieldTable[histoPrefix+'ueDown'][proc])
							yldHists[isEM+proc+'ueDown'].GetXaxis().SetBinLabel(ibin,binStr)
						ibin+=1
					yldHists[isEM+proc].Write()
					if doAllSys and proc!='data':
						for syst in systematicList:
							for ud in ['Up','Down']:
								if syst=='toppt' and proc not in topptProcs: continue
								if syst=='ht' and proc not in htProcs: continue
								yldHists[isEM+proc+syst+ud].Write()
					if doHDsys and proc+'_hdup' in bkgProcs.keys(): 
						yldHists[isEM+proc+'hdUp'].Write()
						yldHists[isEM+proc+'hdDown'].Write()
					if doUEsys and proc+'_ueup' in bkgProcs.keys(): 
						yldHists[isEM+proc+'ueUp'].Write()
						yldHists[isEM+proc+'ueDown'].Write()
			yldRfile.Close()
				
		print "       PRODUCING YIELD TABLES: ",gettime()
		table = []
		table.append(['CUTS:',cutString])
		table.append(['break'])
		table.append(['break'])
		
		#yields without background grouping
		print "              yields without background grouping",gettime()
		table.append(['YIELDS']+[proc for proc in bkgProcList+['data']])
		for cat in catList:
			row = [cat]
			histoPrefix=discriminant+'_'+lumiStr+'_'+cat
			for proc in bkgProcList+['data']:
				row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
			table.append(row)			
		table.append(['break'])
		table.append(['break'])
		
		#yields with top,ewk,qcd grouping
		print "              yields with background grouping",gettime()
		table.append(['YIELDS']+[proc for proc in bkgGrupList+['data']])
		for cat in catList:
			row = [cat]
			histoPrefix=discriminant+'_'+lumiStr+'_'+cat
			for proc in bkgGrupList+['data']:
				row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
			table.append(row)
		table.append(['break'])
		table.append(['break'])
		
		#yields for signals
		print "              yields for signals",gettime()
		table.append(['YIELDS']+[proc for proc in sigList])
		for cat in catList:
			row = [cat]
			histoPrefix=discriminant+'_'+lumiStr+'_'+cat
			for proc in sigList:
				row.append(str(yieldTable[histoPrefix][proc])+' $\pm$ '+str(yieldStatErrTable[histoPrefix][proc]))
			table.append(row)

		#yields for AN tables (yields in e/m channels)
		print "              yields in e/m channels",gettime()
		for isEM in isEMlist:
			if isEM=='E': corrdSys = elcorrdSys
			if isEM=='M': corrdSys = mucorrdSys
			for thetag in nhottlist:
				table.append(['break'])
				table.append(['','is'+isEM+'_'+thetag+'_yields'])
				table.append(['break'])
				table.append(['YIELDS']+[cat for cat in catList if 'is'+isEM in cat and thetag in cat]+['\\\\'])
				for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
					row = [proc]
					for cat in catList:
						if not ('is'+isEM in cat and thetag in cat): continue
						modTag = cat[cat.find('nT'):cat.find('nJ')-3]
						histoPrefix=discriminant+'_'+lumiStr+'_'+cat
						yieldtemp = 0.
						yielderrtemp = 0.
						if proc=='totBkg' or proc=='dataOverBkg':
							for bkg in bkgGrupList:
								try:
									yieldtemp += yieldTable[histoPrefix][bkg]+zero
									yielderrtemp += yieldStatErrTable[histoPrefix][bkg]**2
									yielderrtemp += (modelingSys[bkg+'_'+modTag]*yieldTable[histoPrefix][bkg])**2
								except:
									print "Missing",bkg,"for channel:",cat
									pass
							yielderrtemp += (corrdSys*yieldtemp)**2
							if proc=='dataOverBkg':
								dataTemp = yieldTable[histoPrefix]['data']+zero
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
						if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefix][proc])))
						else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
					row.append('\\\\')
					table.append(row)
		
		#yields for PAS tables (yields in e/m channels combined)
		print "              yields in e/m channels combined",gettime()
		for thetag in nhottlist:
			table.append(['break'])
			table.append(['','isL_'+thetag+'_yields'])
			table.append(['break'])
			table.append(['YIELDS']+[cat.replace('isE','isL') for cat in catList if 'isE' in cat and thetag in cat]+['\\\\'])
			for proc in bkgGrupList+['totBkg','data','dataOverBkg']+sigList:
				row = [proc]
				for cat in catList:
					if not ('isE' in cat and thetag in cat): continue
					modTag = cat[cat.find('nT'):cat.find('nJ')-3]
					histoPrefixE = discriminant+'_'+lumiStr+'_'+cat
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
								yieldtemp  += yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]+zero
								yielderrtemp += yieldStatErrTable[histoPrefixE][bkg]**2+yieldStatErrTable[histoPrefixM][bkg]**2
								yielderrtemp += (modelingSys[bkg+'_'+modTag]*(yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]))**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
							except:
								print "Missing",bkg,"for channel:",cat
								pass
						yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
						if proc=='dataOverBkg':
							dataTemp = yieldTable[histoPrefixE]['data']+yieldTable[histoPrefixM]['data']+zero
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
						if proc not in sigList: yielderrtemp += (modelingSys[proc+'_'+modTag]*yieldtemp)**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
						yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
					yielderrtemp = math.sqrt(yielderrtemp)
					if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefixE][proc]+yieldTable[histoPrefixM][proc])))
					else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
				row.append('\\\\')
				table.append(row)

		#systematics
		print "              systematics",gettime()
		if doAllSys:
			table.append(['break'])
			table.append(['','Systematics'])
			table.append(['break'])
			for proc in bkgGrupList+sigList:
				table.append([proc]+[cat for cat in catList]+['\\\\'])
				for syst in sorted(systematicList+['hd','ue']):
					for ud in ['Up','Down']:
						row = [syst+ud]
						for cat in catList:
							histoPrefix = discriminant+'_'+lumiStr+'_'+cat
							nomHist = histoPrefix
							shpHist = histoPrefix+syst+ud
							try: row.append(' & '+str(round(yieldTable[shpHist][proc]/(yieldTable[nomHist][proc]+zero),2)))
							except:
								if not ((syst=='toppt' and proc not in topptProcs) or (syst=='ht' and proc not in htProcs) or (syst=='hd' and (proc+'_hdup' not in bkgProcs.keys() or not doHDsys)) or (syst=='ue' and (proc+'_ueup' not in bkgProcs.keys() or not doUEsys))):
									print "Missing",proc,"for channel:",cat,"and systematic:",syst
								pass
						row.append('\\\\')
						table.append(row)
				table.append(['break'])
			
		print "              writing table",gettime()
		if addCRsys: out=open(outDir+'/yields_addCRunc_'+discriminant+BRconfStr+'_'+lumiStr+saveKey+'.txt','w')
		else: out=open(outDir+'/yields_'+discriminant+BRconfStr+'_'+lumiStr+saveKey+'.txt','w')
		printTable(table,out)
		out.close()
	print "       CLEANING UP ... ",gettime()
	for hist in hists.keys(): del hists[hist]
	for hist in datahists.keys(): del datahists[hist]
	for hist in sighists.keys(): del sighists[hist]
	for hist in bkghists.keys(): del bkghists[hist]
	return

iPlotList = [x.replace('bkghists_','')[:-2] for x in os.listdir(outDir+'/'+catList[0][2:]) if 'bkghists_' in x and '.p' in x]

print "WORKING DIR:",outDir
print "Templates:",iPlotList
for iPlot in iPlotList:
	datahists = {}
	bkghists  = {}
	sighists  = {}
	if len(sys.argv)>1 and iPlot!=sys.argv[1]: continue
	print "LOADING DISTRIBUTION: "+iPlot,gettime()
	#if iPlot!="HT": continue
	for cat in catList:
		print "         ",cat[2:],gettime()
		datahists.update(pickle.load(open(outDir+'/'+cat[2:]+'/datahists_'+iPlot+'.p','rb')))
		bkghists.update(pickle.load(open(outDir+'/'+cat[2:]+'/bkghists_'+iPlot+'.p','rb')))
		sighists.update(pickle.load(open(outDir+'/'+cat[2:]+'/sighists_'+iPlot+'.p','rb')))
	
	#Re-scale lumi
	if lumiScaleCoeff!=1.:
		print "       SCALING LUMINOSITY BY A FACTOR OF",lumiScaleCoeff,gettime()
		for key in bkghists.keys(): bkghists[key].Scale(lumiScaleCoeff)
		for key in sighists.keys(): sighists[key].Scale(lumiScaleCoeff)
	
	#Rebin
	if rebinBy>0:
		print "       REBINNING HISTOGRAMS: MERGING",rebinBy,"BINS ...",gettime()
		for data in datahists.keys(): datahists[data] = datahists[data].Rebin(rebinBy)
		for bkg in bkghists.keys():   bkghists[bkg] = bkghists[bkg].Rebin(rebinBy)
		for sig in sighists.keys():   sighists[sig] = sighists[sig].Rebin(rebinBy)

 	#Negative Bin Correction
 	print "       CORRECTING NEGATIVE BINS ...",gettime()
 	count=0
 	for bkg in bkghists.keys(): 
 		if count%100000==0: print "       ",round(count*100/len(bkghists.keys()))
 		negBinCorrection(bkghists[bkg])
 		count+=1
 	count=0
 	for sig in sighists.keys(): 
 		if count%100000==0: print "       ",round(count*100/len(sighists.keys()))
 		negBinCorrection(sighists[sig])
 		count+=1

 	#OverFlow Correction
 	print "       CORRECTING OVER(UNDER)FLOW BINS ...",gettime()
 	count=0
 	for data in datahists.keys(): 
 		if count%100000==0: print "       ",round(count*100/len(datahists.keys()))
 		overflow(datahists[data])
 		underflow(datahists[data])
 		count+=1
 	count=0
 	for bkg in bkghists.keys():
 		if count%100000==0: print "       ",round(count*100/len(bkghists.keys()))
 		overflow(bkghists[bkg])
 		underflow(bkghists[bkg])
 		count+=1
 	count=0
 	for sig in sighists.keys():
 		if count%100000==0: print "       ",round(count*100/len(sighists.keys()))
 		overflow(sighists[sig])
 		underflow(sighists[sig])
 		count+=1

	print "       STARTING TO PRODUCE TEMPLATES ...",gettime()
	makeCatTemplates(datahists,sighists,bkghists,iPlot)

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


