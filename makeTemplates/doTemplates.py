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

region='WJCR' #SR,TTCR,WJCR
isCategorized=True
cutString=''#'lep30_MET100_NJets4_DR1_1jet250_2jet50'
if region=='SR': pfix='templates_'
if region=='TTCR': pfix='ttbar_'
if region=='WJCR': pfix='wjets_'
if not isCategorized: pfix='kinematicsST_'+region+'_'
pfix+='ST_2016_11_13_wJSF'
outDir = os.getcwd()+'/'+pfix+'/'+cutString

scaleSignalXsecTo1pb = True # this has to be "True" if you are making templates for limit calculation!!!!!!!!
scaleLumi = True
lumiScaleCoeff = 33590./36000.
doAllSys = True
doQ2sys = True
if not doAllSys: doQ2sys = False
addCRsys = False
systematicList = ['pileup','jec','jer','btag','mistag','tau21','topsf','toppt','muR','muF','muRFcorrd','jsf','trigeff']
normalizeRENORM_PDF = False #normalize the renormalization/pdf uncertainties to nominal templates --> normalizes signal processes only !!!!
		       
bkgProcList = ['TTJets','T','TTW','TTZ','WJets','ZJets','VV','QCD']
wjetList  = ['WJetsMG100','WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500'] 
zjetList  = ['DY']
vvList    = ['WW','WZ','ZZ']
ttwList   = ['TTWl','TTWq']
ttzList   = ['TTZl','TTZq']
ttjetList = ['TTJetsPH0to700inc','TTJetsPH700to1000inc','TTJetsPH1000toINFinc','TTJetsPH700mtt','TTJetsPH1000mtt']
tList     = ['Tt','Tbt','Ts','TtW','TbtW']

bkgGrupList = ['top','ewk','qcd']
topList = ttjetList+ttwList+ttzList+tList
ewkList = wjetList+zjetList+vvList
qcdList = ['QCDht100','QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000']
dataList= ['DataEPRH','DataMPRH','DataERRBCDEFG','DataMRRBCDEFG']

q2UpList   = ttwList+ttzList+tList+['TTJetsPHQ2U']#,'TtWQ2U','TbtWQ2U']
q2DownList = ttwList+ttzList+tList+['TTJetsPHQ2D']#,'TtWQ2D','TbtWQ2D']

whichSignal = 'X53X53' #HTB, TT, BB, or X53X53
signalMassRange = [700,1600]
sigList = [whichSignal+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100)]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in range(signalMassRange[0],signalMassRange[1]+100,100) for chiral in ['left','right']]
if whichSignal=='HTB': sigList = [whichSignal+'M'+str(mass) for mass in [180]+range(signalMassRange[0],signalMassRange[1]+50,50)]
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

isEMlist =['E','M']
if region=='SR': nttaglist=['0','1p']
else: nttaglist = ['0p']
if region=='TTCR': nWtaglist = ['0p']
else: nWtaglist=['0','1p']
if region=='WJCR': nbtaglist = ['0']
else: nbtaglist=['1','2p']
if not isCategorized: 	
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['1p']
	if region=='WJCR': nbtaglist = ['0']
njetslist=['4p']
if region=='PS': njetslist=['3p']
catList = ['is'+item[0]+'_nT'+item[1]+'_nW'+item[2]+'_nB'+item[3]+'_nJ'+item[4] for item in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))]
tagList = ['nT'+item[0]+'_nW'+item[1]+'_nB'+item[2]+'_nJ'+item[3] for item in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]

lumiSys = 0.062 #lumi uncertainty
eltrigSys = 0.03 #electron trigger uncertainty
mutrigSys = 0.011 #muon trigger uncertainty
elIdSys = 0.01 #electron id uncertainty
muIdSys = 0.011 #muon id uncertainty
elIsoSys = 0.01 #electron isolation uncertainty
muIsoSys = 0.03 #muon isolation uncertainty

elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)

for tag in tagList:
	modTag = tag[tag.find('nT'):tag.find('nJ')-3]
	modelingSys['data_'+modTag] = 0.
	modelingSys['qcd_'+modTag] = 0.
	if not addCRsys: modelingSys['ewk_'+modTag],modelingSys['top_'+modTag] = 0.,0.
	
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
		print "       SCALING SIGNAL TEMPLATES TO 1pb ..."
		if scaleSignalXsecTo1pb:
			for signal in sigList:
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
		print "       WRITING THETA TEMPLATES: "
		for signal in sigList:
			print "              ... "+signal
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
		print "       WRITING COMBINE TEMPLATES: "
		combineRfileName = outDir+'/templates_'+discriminant+BRconfStr+'_'+lumiStr+'fb'+'.root'
		combineRfile = TFile(combineRfileName,'RECREATE')
		for cat in catList:
			print "              ... "+cat
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

		print "       WRITING SUMMARY TEMPLATES: "
		for signal in sigList:
			print "              ... "+signal
			yldRfileName = outDir+'/templates_YLD_'+signal+BRconfStr+'_'+lumiStr+'fb.root'
			yldRfile = TFile(yldRfileName,'RECREATE')
			for isEM in isEMlist:	
				for proc in bkgGrupList+['totBkg','data',signal]:
					yldHists = {}
					yldHists[isEM+proc]=TH1F('YLD_'+lumiStr+'fb_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA'),'',len(tagList),0,len(tagList))
					if doAllSys and proc!='data':
						for syst in systematicList:
							for ud in ['Up','Down']:
								if proc!='top' and syst=='toppt': continue
								yldHists[isEM+proc+syst+ud]=TH1F('YLD_'+lumiStr+'fb_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__'+syst+'__'+ud.replace('Up','plus').replace('Down','minus'),'',len(tagList),0,len(tagList))
					if doQ2sys and proc=='top': 
						yldHists[isEM+proc+'q2Up']  =TH1F('YLD_'+lumiStr+'fb_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__q2__plus','',len(tagList),0,len(tagList))
						yldHists[isEM+proc+'q2Down']=TH1F('YLD_'+lumiStr+'fb_is'+isEM+'_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data','DATA')+'__q2__minus','',len(tagList),0,len(tagList))
					ibin = 1
					for cat in catList:
						if 'is'+isEM not in cat: continue
						nttag = cat.split('_')[-4][2:]
						nWtag = cat.split('_')[-3][2:]
						nbtag = cat.split('_')[-2][2:]
						njets = cat.split('_')[-1][2:]
						binStr = ''
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
						histoPrefix=discriminant+'_'+lumiStr+'fb_'+cat
						yldHists[isEM+proc].SetBinContent(ibin,yieldTable[histoPrefix][proc])
						yldHists[isEM+proc].SetBinError(ibin,yieldStatErrTable[histoPrefix][proc])
						yldHists[isEM+proc].GetXaxis().SetBinLabel(ibin,binStr)
						if doAllSys and proc!='data':
							for syst in systematicList:
								for ud in ['Up','Down']:
									if proc!='top' and syst=='toppt': continue
									yldHists[isEM+proc+syst+ud].SetBinContent(ibin,yieldTable[histoPrefix+syst+ud][proc])
									yldHists[isEM+proc+syst+ud].GetXaxis().SetBinLabel(ibin,binStr)
						if doQ2sys and proc=='top': 
							yldHists[isEM+proc+'q2Up'].SetBinContent(ibin,yieldTable[histoPrefix+'q2Up'][proc])
							yldHists[isEM+proc+'q2Up'].GetXaxis().SetBinLabel(ibin,binStr)
							yldHists[isEM+proc+'q2Down'].SetBinContent(ibin,yieldTable[histoPrefix+'q2Down'][proc])
							yldHists[isEM+proc+'q2Down'].GetXaxis().SetBinLabel(ibin,binStr)
						ibin+=1
					yldHists[isEM+proc].Write()
					if doAllSys and proc!='data':
						for syst in systematicList:
							for ud in ['Up','Down']:
								if proc!='top' and syst=='toppt': continue
								yldHists[isEM+proc+syst+ud].Write()
					if doQ2sys and proc=='top': 
						yldHists[isEM+proc+'q2Up'].Write()
						yldHists[isEM+proc+'q2Down'].Write()
			yldRfile.Close()
				
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
						modTag = cat[cat.find('nT'):cat.find('nJ')-3]
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
						if proc=='data': row.append(' & '+str(int(yieldTable[histoPrefix][proc])))
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
					modTag = cat[cat.find('nT'):cat.find('nJ')-3]
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
								yielderrtemp += (modelingSys[bkg+'_'+modTag]*(yieldTable[histoPrefixE][bkg]+yieldTable[histoPrefixM][bkg]))**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
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
						if proc not in sigList: yielderrtemp += (modelingSys[proc+'_'+modTag]*yieldtemp)**2 #(modelingSys*(Nelectron+Nmuon))**2 --> correlated across e/m
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
				for syst in sorted(systematicList+['q2']):
					for ud in ['Up','Down']:
						row = [syst+ud]
						for cat in catList:
							histoPrefix = discriminant+'_'+lumiStr+'fb_'+cat
							nomHist = histoPrefix
							shpHist = histoPrefix+syst+ud
							try: row.append(' & '+str(round(yieldTable[shpHist][proc]/(yieldTable[nomHist][proc]+1e-20),2)))
							except:
								if (syst=='toppt' or syst=='q2') and (proc not in sigList and proc!='ewk' and proc!='qcd'):
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
for file in findfiles(outDir+'/'+catList[0][2:]+'/', '*.p'):
    if 'bkghists' not in file: continue
    iPlotList.append(file.split('_')[-1][:-2])

print "WORKING DIR:",outDir
for iPlot in iPlotList:
	datahists = {}
	bkghists  = {}
	sighists  = {}
	if iPlot=='minMlj': continue
	print "LOADING DISTRIBUTION: "+iPlot
	for cat in catList:
		print "         ",cat[2:]
		datahists.update(pickle.load(open(outDir+'/'+cat[2:]+'/datahists_'+iPlot+'.p','rb')))
		bkghists.update(pickle.load(open(outDir+'/'+cat[2:]+'/bkghists_'+iPlot+'.p','rb')))
		sighists.update(pickle.load(open(outDir+'/'+cat[2:]+'/sighists_'+iPlot+'.p','rb')))
	if scaleLumi:
		for key in bkghists.keys(): bkghists[key].Scale(lumiScaleCoeff)
		for key in sighists.keys(): sighists[key].Scale(lumiScaleCoeff)

	print "       MAKING CATEGORIES FOR TOTAL SIGNALS ..."
	makeThetaCats(datahists,sighists,bkghists,iPlot)

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


