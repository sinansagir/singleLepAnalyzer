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

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
step1Dir = '/user_data/ssagir/LJMet_1lep_111516_step2preSel/nominal'

"""
Note: 
--Each process in step1 (or step2) directories should have the root files hadded! 
--The code will look for <step1Dir>/<process>_hadd.root for nominal trees.
The uncertainty shape shifted files will be taken from <step1Dir>/../<shape>/<process>_hadd.root,
where <shape> is for example "JECUp". hadder.py can be used to prepare input files this way! 
--Each process given in the lists below must have a definition in "samples.py"
--Check the set of cuts in "analyze.py"
"""

bkgList = [
	'DY',
	'WJetsMG',
	'WJetsMG100',
	'WJetsMG200',
	'WJetsMG400',
	'WJetsMG600',
	'WJetsMG800',
	'WJetsMG1200',
	'WJetsMG2500',
	'WW','WZ','ZZ',
	'TTJetsPH0to700inc','TTJetsPH700to1000inc','TTJetsPH1000toINFinc',
	'TTJetsPH700mtt','TTJetsPH1000mtt',
	'TTWl','TTWq',
	'TTZl','TTZq',
	'Tt','Tbt','Ts',
	'TtW','TbtW',
	'QCDht100','QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000',
	]

dataList = ['DataEPRH','DataMPRH','DataERRBCDEFG','DataMRRBCDEFG']#'DataEPRC','DataEPRB','DataEPRD','DataMPRC','DataMPRB','DataMPRD']

whichSignal = 'X53X53' #HTB, TT, BB, or X53X53
signalMassRange = [700,1600]
sigList = [whichSignal+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100)]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in range(signalMassRange[0],signalMassRange[1]+100,100) for chiral in ['left','right']]
if whichSignal=='HTB': sigList = [whichSignal+'M'+str(mass) for mass in [180]+range(signalMassRange[0],signalMassRange[1]+50,50)]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
if whichSignal=='X53X53': decays = [''] #decays to tWtW 100% of the time
if whichSignal=='HTB': decays = ['']

iPlot = 'minMlb' #choose a discriminant from plotList below!
if len(sys.argv)>2: iPlot=sys.argv[2]
region = 'SR'
if len(sys.argv)>3: region=sys.argv[3]
isCategorized = 1
if len(sys.argv)>4: isCategorized=int(sys.argv[4])
isotrig = 1
doJetRwt= 1
doAllSys= True
doQ2sys = True
q2List  = [#energy scale sample to be processed
	       'TTJetsPHQ2U','TTJetsPHQ2D',
	       #'TtWQ2U','TbtWQ2U',
	       #'TtWQ2D','TbtWQ2D',
	       ]

# if iPlot=='ST': cutList = {'lepPtCut':30,'metCut':100,'njetsCut':4,'drCut':1,'jet1PtCut':250,'jet2PtCut':150,'jet3PtCut':0}
# else:           cutList = {'lepPtCut':30,'metCut':150,'njetsCut':4,'drCut':1,'jet1PtCut':450,'jet2PtCut':150,'jet3PtCut':0}
cutList = {'lepPtCut':30,'metCut':100,'njetsCut':4,'drCut':1,'jet1PtCut':250,'jet2PtCut':150,'jet3PtCut':0}
if region=='PS':cutList = {'lepPtCut':30,'metCut':100,'njetsCut':3,'drCut':0,'jet1PtCut':200,'jet2PtCut':90, 'jet3PtCut':0}
#'lep30_MET100_NJets3_NBJets0_DR0_1jet200_2jet50_3jet0', preSel
#'lep30_MET150_NJets4_NBJets0_DR1_1jet450_2jet150_3jet0', #minMlb
#'lep30_MET100_NJets4_NBJets0_DR1_1jet250_2jet50_3jet0', #ST change to 'lep30_MET100_NJets4_NBJets0_DR1_1jet250_2jet150_3jet0' for trigger HT400

cutString  = 'lep'+str(int(cutList['lepPtCut']))+'_MET'+str(int(cutList['metCut']))
#cutString += '_NJets'+str(int(cutList['njetsCut']))
#cutString += '_NBJets'+str(int(cutList['nbjetsCut']))
cutString += '_DR'+str(cutList['drCut'])+'_1jet'+str(int(cutList['jet1PtCut']))
cutString += '_2jet'+str(int(cutList['jet2PtCut']))#+'_3jet'+str(int(cutList['jet3PtCut']))
# cutString += '_4jet'+str(int(cutList['jet4PtCut']))+'_5jet'+str(int(cutList['jet5PtCut']))
# cutString += '_1Wjet'+str(cutList['Wjet1PtCut'])+'_1bjet'+str(cutList['bjet1PtCut'])
# cutString += '_HT'+str(cutList['htCut'])+'_ST'+str(cutList['stCut'])+'_minMlb'+str(cutList['minMlbCut'])

cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
if region=='TTCR': pfix='ttbar_'
elif region=='WJCR': pfix='wjets_'
else: pfix='templates_'
if not isCategorized: pfix='kinematics_'+region+'_'
pfix+=iPlot
pfix+='_'+datestr#+'_'+timestr
		
if len(sys.argv)>5: isEMlist=[str(sys.argv[5])]
else: 
	if not isCategorized: isEMlist=['E','M','L']
	else: isEMlist = ['E','M']
if len(sys.argv)>6: nttaglist=[str(sys.argv[6])]
else: 
	if not isCategorized: nttaglist = ['0p']
	if region=='SR': nttaglist=['0','1p']
	else: nttaglist = ['0p']
if len(sys.argv)>7: nWtaglist=[str(sys.argv[7])]
else: 
	if not isCategorized: nWtaglist = ['0p']
	if region=='TTCR': nWtaglist = ['0p']
	else: nWtaglist=['0','1p']
if len(sys.argv)>8: nbtaglist=[str(sys.argv[8])]
else: 
	if not isCategorized: nbtaglist = ['1p']
	if region=='WJCR': nbtaglist = ['0']
	else: nbtaglist=['1','2p']
if len(sys.argv)>9: njetslist=[str(sys.argv[9])]
else: njetslist=['4p']

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

#bigbins = [0,50,100,150,200,250,300,350,400,450,500,600,700,800,1000,1200,1500]
bigbins = [0,50,100,125,150,175,200,225,250,275,300,325,350,375,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,5000]

plotList = {#discriminantName:(discriminantLJMETName, binning, xAxisLabel)
	'deltaRAK8':('minDR_leadAK8otherAK8',linspace(0,5,51).tolist(),';min #DeltaR(1^{st} AK8 jet, other AK8 jet)'),
	'MTlmet':('MT_lepMet',linspace(0,250,51).tolist(),';M_{T}(l,#slash{E}_{T}) [GeV]'),
	'NPV'   :('nPV_singleLepCalc',linspace(0, 40, 41).tolist(),';PV multiplicity;'),
	'lepPt' :('leptonPt_singleLepCalc',linspace(0, 1000, 51).tolist(),';Lepton p_{T} [GeV];'),
	'lepEta':('leptonEta_singleLepCalc',linspace(-4, 4, 41).tolist(),';Lepton #eta;'),
	'JetEta':('theJetEta_JetSubCalc_PtOrdered',linspace(-4, 4, 41).tolist(),';AK4 Jet #eta;'),
	'JetPt' :('theJetPt_JetSubCalc_PtOrdered',linspace(0, 1500, 51).tolist(),';jet p_{T} [GeV];'),
	'Jet1Pt':('theJetPt_JetSubCalc_PtOrdered[0]',linspace(0, 1500, 51).tolist(),';1^{st} AK4 Jet p_{T} [GeV];'),
	'Jet2Pt':('theJetPt_JetSubCalc_PtOrdered[1]',linspace(0, 1500, 51).tolist(),';2^{nd} AK4 Jet p_{T} [GeV];'),
	'Jet2Pt':('theJetPt_JetSubCalc_PtOrdered[1]',linspace(0, 1500, 51).tolist(),';2^{nd} AK4 Jet p_{T} [GeV];'),
	'Jet3Pt':('theJetPt_JetSubCalc_PtOrdered[2]',linspace(0, 800, 51).tolist(),';3^{rd} AK4 Jet p_{T} [GeV];'),
	'Jet4Pt':('theJetPt_JetSubCalc_PtOrdered[3]',linspace(0, 500, 51).tolist(),';4^{th} AK4 Jet p_{T} [GeV];'),
	'Jet5Pt':('theJetPt_JetSubCalc_PtOrdered[4]',linspace(0, 500, 51).tolist(),';5^{th} AK4 Jet p_{T} [GeV];'),
	'Jet6Pt':('theJetPt_JetSubCalc_PtOrdered[5]',linspace(0, 500, 51).tolist(),';6^{th} AK4 Jet p_{T} [GeV];'),
	'JetPtBins' :('theJetPt_JetSubCalc_PtOrdered',linspace(0,2000,21).tolist(),';AK4 Jet p_{T} [GeV];'),
	'Jet1PtBins':('theJetPt_JetSubCalc_PtOrdered[0]',linspace(0,2000,21).tolist(),';1^{st} AK4 Jet p_{T} [GeV];'),
	'Jet2PtBins':('theJetPt_JetSubCalc_PtOrdered[1]',linspace(0,2000,21).tolist(),';2^{nd} AK4 Jet p_{T} [GeV];'),
	'Jet3PtBins':('theJetPt_JetSubCalc_PtOrdered[2]',linspace(0,2000,21).tolist(),';3^{rd} AK4 Jet p_{T} [GeV];'),
	'Jet4PtBins':('theJetPt_JetSubCalc_PtOrdered[3]',linspace(0,2000,21).tolist(),';4^{th} AK4 Jet p_{T} [GeV];'),
	'Jet5PtBins':('theJetPt_JetSubCalc_PtOrdered[4]',linspace(0,2000,21).tolist(),';5^{th} AK4 Jet p_{T} [GeV];'),
	'Jet6PtBins':('theJetPt_JetSubCalc_PtOrdered[5]',linspace(0,2000,21).tolist(),';6^{th} AK4 Jet p_{T} [GeV];'),
	'MET'   :('corr_met_singleLepCalc',linspace(0, 1500, 51).tolist(),';#slash{E}_{T} [GeV];'),
	'NJets' :('NJets_JetSubCalc',linspace(0, 15, 16).tolist(),';jet multiplicity;'),
	'NBJets':('NJetsCSVwithSF_JetSubCalc',linspace(0, 10, 11).tolist(),';b tag multiplicity;'),
	'NWJets':('NJetsWtagged_0p6',linspace(0, 6, 7).tolist(),';W tag multiplicity;'),
	'NTJets':('NJetsTtagged_0p81',linspace(0, 4, 5).tolist(),';t tag multiplicity;'),
	'NJetsAK8':('NJetsAK8_JetSubCalc',linspace(0, 8, 9).tolist(),';AK8 Jet multiplicity;'),
	'JetPtAK8':('theJetAK8Pt_JetSubCalc_PtOrdered',linspace(0, 1500, 51).tolist(),';AK8 Jet p_{T} [GeV];'),
	'JetPtBinsAK8':('theJetAK8Pt_JetSubCalc_PtOrdered',bigbins,';AK8 Jet p_{T} [GeV];'),
	'JetEtaAK8':('theJetAK8Eta_JetSubCalc_PtOrdered',linspace(-4, 4, 41).tolist(),';AK8 Jet #eta;'),
	'Tau21'  :('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{2}/#tau_{1};'),
	'Tau21Nm1'  :('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{2}/#tau_{1};'),
	'Tau32'  :('theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{3}/#tau_{2};'),
	'Tau32Nm1'  :('theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{3}/#tau_{2};'),
	'Pruned' :('theJetAK8PrunedMass_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 Jet Pruned mass [GeV];'),
	'PrunedSmeared' :('theJetAK8PrunedMass_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 Jet Pruned mass [GeV];'),
	'PrunedSmearedNm1' :('theJetAK8PrunedMassWtagUncerts_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 Jet Pruned mass [GeV];'),
	'SoftDropMass' :('theJetAK8SoftDropMass_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet soft drop mass [GeV];'),
	'SoftDropMassNm1' :('theJetAK8SoftDropMass_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet soft drop mass [GeV];'),
	'mindeltaR':('minDR_lepJet',linspace(0, 5, 51).tolist(),';min #DeltaR(l, jet);'),
	'deltaRjet1':('deltaR_lepJets[0]',linspace(0, 5, 51).tolist(),';#DeltaR(l, 1^{st} jet);'),
	'deltaRjet2':('deltaR_lepJets[1]',linspace(0, 5, 51).tolist(),';#DeltaR(l, 2^{nd} jet);'),
	'deltaRjet3':('deltaR_lepJets[2]',linspace(0, 5, 51).tolist(),';#DeltaR(l, 3^{rd} jet);'),
	'nLepGen':('NLeptonDecays_TpTpCalc',linspace(0,10,11).tolist(),';N lepton decays from TT'),
	'METphi':('corr_met_phi_singleLepCalc',linspace(-3.2,3.2,65).tolist(),';#phi(#slash{E}_{T})'),
	'lepPhi':('leptonPhi_singleLepCalc',linspace(-3.2,3.2,65).tolist(),';#phi(l)'),
	'lepDxy':('leptonDxy_singleLepCalc',linspace(-0.02,0.02,51).tolist(),';lepton xy impact param [cm]'),
	'lepDz':('leptonDz_singleLepCalc',linspace(-0.1,0.1,51).tolist(),';lepton z impact param [cm]'),
	'lepCharge':('leptonCharge_singleLepCalc',linspace(-2,2,5).tolist(),';lepton charge'),
	'lepIso':('leptonMiniIso_singleLepCalc',linspace(0,0.2,51).tolist(),';lepton mini isolation'),
	'Tau1':('theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #tau_{1}'),
	'Tau2':('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #tau_{2}'),
	'JetPhi':('theJetPhi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK4 Jet #phi'),
	'JetPhiAK8':('theJetAK8Phi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK8 Jet #phi'),
	'Bjet1Pt':('BJetLeadPt',linspace(0,1500,51).tolist(),';1^{st} b jet p_{T} [GeV]'),  ## B TAG
	'Wjet1Pt':('WJetLeadPt',linspace(0,1500,51).tolist(),';1^{st} W jet p_{T} [GeV]'),
	'Tjet1Pt':('TJetLeadPt',linspace(0,1500,51).tolist(),';1^{st} t jet p_{T} [GeV]'),
	'topMass':('topMass',linspace(0,1500,51).tolist(),';reconstructed M(t) [GeV]'),
	'topPt':('topPt',linspace(0,1500,51).tolist(),';reconstructed pT(t) [GeV]'),
	'minMlj':('minMleppJet',linspace(0,1000,51).tolist(),';min[M(l,jet)] [GeV], 0 b tags'),
	'minMljDR':('deltaRlepJetInMinMljet',linspace(0,5,51).tolist(),';#DeltaR(l,jet) from min[M(l,jet)], 0 b tags'),
	'minMljDPhi':('deltaPhilepJetInMinMljet',linspace(0,5,51).tolist(),';#Delta#phi(l,jet) from min[M(l,jet)], 0 b tags'),
	'minMlbDR':('deltaRlepbJetInMinMlb',linspace(0,5,51).tolist(),';#DeltaR(l,b) from min[M(l,b)], > 1 b tags'), ## B TAG
	'minMlbDPhi':('deltaPhilepbJetInMinMlb',linspace(0,5,51).tolist(),';#Delta#phi(l,b) from min[M(l,b)], > 1 b tags'), ## B TAG
	'nonMinMlbDR':('deltaRlepbJetNotInMinMlb',linspace(0,5,51).tolist(),';#DeltaR(l,b) not in min[M(l,b)], > 1 b tags'),  ## B TAG
	'MWb1':('M_taggedW_bjet1',linspace(0,1000,51).tolist(),';M(W jet, 1^{st} b jet) [GeV]'), ## B TAG
	'MWb2':('M_taggedW_bjet2',linspace(0,1000,51).tolist(),';M(W jet, 2^{nd} b jet) [GeV]'), ## 2 B TAG
	'deltaRlb1':('deltaRlepbJet1',linspace(0,5,51).tolist(),';#DeltaR(l, 1^{st} b jet)'), ## B TAG
	'deltaRlb2':('deltaRlepbJet2',linspace(0,5,51).tolist(),';#DeltaR(l, 2^{nd} b jet)'), ## 2 B TAG
	'deltaRtW':('deltaRtopWjet',linspace(0,5,51).tolist(),';#DeltaR(reco t, W jet)'),
	'deltaRlW':('deltaRlepWjet',linspace(0,5,51).tolist(),';#DeltaR(l, W jet)'),
	'deltaRWb1':('deltaRtaggedWbJet1',linspace(0,5,51).tolist(),';#DeltaR(W, 1^{st} b jet)'), ## B TAG
	'deltaRWb2':('deltaRtaggedWbJet2',linspace(0,5,51).tolist(),';#DeltaR(W, 2^{nd} b jet)'), ## 2 B TAG
	'deltaPhilb1':('deltaPhilepbJet1',linspace(0,5,51).tolist(),';#Delta#phi(l, 1^{st} b jet)'), ## B TAG
	'deltaPhilb2':('deltaPhilepbJet2',linspace(0,5,51).tolist(),';#Delta#phi(l, 2^{nd} b jet)'), ## 2 B TAG
	'deltaPhitW':('deltaPhitopWjet',linspace(0,5,51).tolist(),';#Delta#phi(reco t, W jet)'),
	'deltaPhilW':('deltaPhilepWjet',linspace(0,5,51).tolist(),';#Delta#phi(l, W jet)'),
	'deltaPhiWb1':('deltaPhitaggedWbJet1',linspace(0,5,51).tolist(),';#Delta#phi(W, 1^{st} b jet)'), ## B TAG
	'deltaPhiWb2':('deltaPhitaggedWbJet2',linspace(0,5,51).tolist(),';#Delta#phi(W, 2^{nd} b jet)'), ## 2 B TAG
	'WjetPt':('WJetTaggedPt',linspace(0,1500,51).tolist(),';W jet p_{T} [GeV]'),
	'PtRel':('ptRel_lepJet',linspace(0,500,51).tolist(),';p_{T,rel}(l, closest jet) [GeV]'),

	'HT':('AK4HT',linspace(0, 5000, 51).tolist(),';H_{T} (GeV);'),
	'ST':('AK4HTpMETpLepPt',linspace(0, 5000, 51).tolist(),';S_{T} (GeV);'),
	'minMlb':('minMleppBjet',linspace(0, 800, 51).tolist(),';min[M(l,b)] (GeV);'),
	}

print "PLOTTING:",iPlot
print "         LJMET Variable:",plotList[iPlot][0]
print "         X-AXIS TITLE  :",plotList[iPlot][2]
print "         BINNING USED  :",plotList[iPlot][1]

catList = list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))
nCats  = len(catList)
catInd = 1
for cat in catList:
 	catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
 	datahists = {}
 	bkghists  = {}
 	sighists  = {}
 	if len(sys.argv)>1: outDir=sys.argv[1]
 	else: 
		outDir = os.getcwd()
		outDir+='/'+pfix
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+cutString
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+catDir
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
 	category = {'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4]}
 	for data in dataList: 
 		datahists.update(analyze(tTreeData,data,cutList,isotrig,False,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
 		if catInd==nCats: del tFileData[data]
 	for bkg in bkgList: 
 		bkghists.update(analyze(tTreeBkg,bkg,cutList,isotrig,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
 		if catInd==nCats: del tFileBkg[bkg]
 		if doAllSys and catInd==nCats:
 			for syst in shapesFiles:
 				for ud in ['Up','Down']: del tFileBkg[bkg+syst+ud]
 	for sig in sigList: 
 		for decay in decays: 
 			sighists.update(analyze(tTreeSig,sig+decay,cutList,isotrig,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
 			if catInd==nCats: del tFileSig[sig+decay]
 			if doAllSys and catInd==nCats:
 				for syst in shapesFiles:
 					for ud in ['Up','Down']: del tFileSig[sig+decay+syst+ud]
 	if doQ2sys: 
 		for q2 in q2List: 
 			bkghists.update(analyze(tTreeBkg,q2,cutList,isotrig,False,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
 			if catInd==nCats: del tFileBkg[q2]

 	#Negative Bin Correction
 	for bkg in bkghists.keys(): negBinCorrection(bkghists[bkg])

 	#OverFlow Correction
 	for data in datahists.keys(): overflow(datahists[data])
 	for bkg in bkghists.keys():   overflow(bkghists[bkg])
 	for sig in sighists.keys():   overflow(sighists[sig])

 	pickle.dump(datahists,open(outDir+'/datahists_'+iPlot+'.p','wb'))
	pickle.dump(bkghists,open(outDir+'/bkghists_'+iPlot+'.p','wb'))
	pickle.dump(sighists,open(outDir+'/sighists_'+iPlot+'.p','wb'))
 	catInd+=1

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))

