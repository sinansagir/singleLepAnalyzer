#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools,getopt
from ROOT import TH1D,gROOT,TFile,TTree
from numpy import linspace
parent = os.path.dirname(os.getcwd())
thisdir= os.path.dirname(os.getcwd()+'/')
sys.path.append(thisdir)
from weights import *
from analyze import *
from samples import *
from utils import *

"""
Note: 
--Each process in step1 (or step2) directories should have the root files hadded! 
--The code will look for <step1Dir>/<process>_hadd.root for nominal trees.
The uncertainty shape shifted files will be taken from <step1Dir>/../<shape>/<process>_hadd.root,
where <shape> is for example "JECUp". hadder.py can be used to prepare input files this way! 
--Each process given in the lists below must have a definition in "samples.py"
--Check the set of cuts in "analyze.py"
"""

gROOT.SetBatch(1)
start_time = time.time()

year = 'R17'
iPlot = 'HT' #choose a discriminant from plotList below!
region = 'PS'
isCategorized = 0
tagABCDnn= '_nJ6pnB2p'
doJetRwt= 0
doAllSys= True
doHDsys = False
doUEsys = False
doPDF = True
if not doAllSys:
	doHDsys = False
	doUEsys = False
	doPDF = False

isEMlist  = ['E','M']
nhottlist = ['0','1p']
nttaglist = ['0','1p']
nWtaglist = ['0','1p']
nbtaglist = ['2','3','4p']
njetslist = ['4','5','6','7','8','9','10p']
if not isCategorized: 
	nhottlist = ['0p']
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['2p']
	njetslist = ['4p']

try: 
	opts, args = getopt.getopt(sys.argv[2:], "", ["iPlot=",
	                                              "region=",
	                                              "isCategorized=",
	                                              "year=",
	                                              "isEM=",
	                                              "nhott=",
	                                              "nttag=",
	                                              "nWtag=",
	                                              "nbtag=",
	                                              "njets=",
	                                              "step1dir=",
	                                              ])
	print opts,args
except getopt.GetoptError as err:
	print str(err)
	sys.exit(1)

for opt, arg in opts:
	print opt, arg
	if opt == '--iPlot': iPlot = arg
	elif opt == '--region': region = arg
	elif opt == '--isCategorized': isCategorized = int(arg)
	elif opt == '--year': year = arg
	elif opt == '--isEM': isEMlist = [str(arg)]
	elif opt == '--nhott': nhottlist = [str(arg)]
	elif opt == '--nttag': nttaglist = [str(arg)]
	elif opt == '--nWtag': nWtaglist = [str(arg)]
	elif opt == '--nbtag': nbtaglist = [str(arg)]
	elif opt == '--njets': njetslist = [str(arg)]
	elif opt == '--step1dir': step1dir = str(arg)
#if tagABCDnn != '': tagABCDnn+=region

lumiStr = str(targetlumi/1000).replace('.','p')+'fb' # 1/fb
#step1Dir = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+year[1:]+'_Oct2019_4t_072820_step1hadds/nominal'
# step1Dir = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+year[1:]+'_Oct2019_4t_07282020_step2/nominal'
step1Dir = step1dir+'/nominal'

bkgList = [
		  'DYMG200','DYMG400','DYMG600','DYMG800','DYMG1200','DYMG2500',
		  'WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800',
		  
		  'TTJetsHadTT1b','TTJetsHadTT2b','TTJetsHadTTbb','TTJetsHadTTcc','TTJetsHadTTjj',
		  'TTJetsSemiLepNjet0TT1b','TTJetsSemiLepNjet0TT2b','TTJetsSemiLepNjet0TTbb','TTJetsSemiLepNjet0TTcc',#'TTJetsSemiLepNjet0TTjj',
		  'TTJetsSemiLepNjet0TTjj1','TTJetsSemiLepNjet0TTjj2',
		  'TTJetsSemiLepNjet9TT1b','TTJetsSemiLepNjet9TT2b','TTJetsSemiLepNjet9TTbb','TTJetsSemiLepNjet9TTcc','TTJetsSemiLepNjet9TTjj',
		  'TTJetsSemiLepNjet9binTT1b','TTJetsSemiLepNjet9binTT2b','TTJetsSemiLepNjet9binTTbb','TTJetsSemiLepNjet9binTTcc','TTJetsSemiLepNjet9binTTjj',
		  'TTJets2L2nuTT1b','TTJets2L2nuTT2b','TTJets2L2nuTTbb','TTJets2L2nuTTcc','TTJets2L2nuTTjj',
		  
		  'Ts','Tt','Tbt','TtW','TbtW', 
		  'TTHH','TTTJ','TTTW','TTWH','TTWW','TTWZ','TTZH','TTZZ',
		  'TTWl','TTZlM10','TTZlM1to10','TTHB','TTHnoB',#'TTWq',
          'WW','WZ','ZZ',
		  'QCDht200','QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000',
		  ]
if year=='R16':
	bkgList+= ['TTJetsSemiLepNjet0TTjj3','TTJetsSemiLepNjet0TTjj4','TTJetsSemiLepNjet0TTjj5','WJetsMG1200','WJetsMG2500']
elif year=='R17':
	bkgList+= ['WJetsMG12001','WJetsMG12002','WJetsMG12003','WJetsMG25001','WJetsMG25002','WJetsMG25003','WJetsMG25004',
			   'TTJetsSemiLepNjet0TTjj3','TTJetsSemiLepNjet0TTjj4','TTJetsSemiLepNjet0TTjj5','Tbs']
elif year=='R18':
	bkgList+= ['WJetsMG1200','WJetsMG2500']#,'Tbs']
ttFlvs = []#'_tt2b','_ttbb','_ttb','_ttcc','_ttlf']
#for ind in range(len(bkgList)):
#	if 'TTJetsSemiLep' in bkgList[ind]: bkgList[ind]=bkgList[ind].replace('TTJetsSemiLep','TTJetsSemiLepInc')
dataList = ['DataE','DataM']#,'DataJ']

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

hdampList = [#hDamp samples
'TTJets2L2nuHDAMPdnTT1b','TTJets2L2nuHDAMPdnTT2b','TTJets2L2nuHDAMPdnTTbb','TTJets2L2nuHDAMPdnTTcc','TTJets2L2nuHDAMPdnTTjj',
'TTJets2L2nuHDAMPupTT1b','TTJets2L2nuHDAMPupTT2b','TTJets2L2nuHDAMPupTTbb','TTJets2L2nuHDAMPupTTcc','TTJets2L2nuHDAMPupTTjj',
'TTJetsHadHDAMPdnTT1b','TTJetsHadHDAMPdnTT2b','TTJetsHadHDAMPdnTTbb','TTJetsHadHDAMPdnTTcc','TTJetsHadHDAMPdnTTjj',
'TTJetsHadHDAMPupTT1b','TTJetsHadHDAMPupTT2b','TTJetsHadHDAMPupTTbb','TTJetsHadHDAMPupTTcc','TTJetsHadHDAMPupTTjj',
'TTJetsSemiLepHDAMPdnNjet0TT1b','TTJetsSemiLepHDAMPdnNjet0TT2b','TTJetsSemiLepHDAMPdnNjet0TTbb','TTJetsSemiLepHDAMPdnNjet0TTcc','TTJetsSemiLepHDAMPdnNjet0TTjj',
'TTJetsSemiLepHDAMPupNjet0TT1b','TTJetsSemiLepHDAMPupNjet0TT2b','TTJetsSemiLepHDAMPupNjet0TTbb','TTJetsSemiLepHDAMPupNjet0TTcc','TTJetsSemiLepHDAMPupNjet0TTjj',
'TTJetsSemiLepHDAMPdnNjet9TT1b','TTJetsSemiLepHDAMPdnNjet9TT2b','TTJetsSemiLepHDAMPdnNjet9TTbb','TTJetsSemiLepHDAMPdnNjet9TTcc','TTJetsSemiLepHDAMPdnNjet9TTjj',
'TTJetsSemiLepHDAMPupNjet9TT1b','TTJetsSemiLepHDAMPupNjet9TT2b','TTJetsSemiLepHDAMPupNjet9TTbb','TTJetsSemiLepHDAMPupNjet9TTcc','TTJetsSemiLepHDAMPupNjet9TTjj',
'TTJetsSemiLepHDAMPdnNjet9binTT1b','TTJetsSemiLepHDAMPdnNjet9binTT2b','TTJetsSemiLepHDAMPdnNjet9binTTbb','TTJetsSemiLepHDAMPdnNjet9binTTcc','TTJetsSemiLepHDAMPdnNjet9binTTjj',
'TTJetsSemiLepHDAMPupNjet9binTT1b','TTJetsSemiLepHDAMPupNjet9binTT2b','TTJetsSemiLepHDAMPupNjet9binTTbb','TTJetsSemiLepHDAMPupNjet9binTTcc','TTJetsSemiLepHDAMPupNjet9binTTjj',
]
ueList = [#UE samples
'TTJets2L2nuUEdnTT1b','TTJets2L2nuUEdnTT2b','TTJets2L2nuUEdnTTbb','TTJets2L2nuUEdnTTcc','TTJets2L2nuUEdnTTjj',
'TTJets2L2nuUEupTT1b','TTJets2L2nuUEupTT2b','TTJets2L2nuUEupTTbb','TTJets2L2nuUEupTTcc','TTJets2L2nuUEupTTjj',
'TTJetsHadUEdnTT1b','TTJetsHadUEdnTT2b','TTJetsHadUEdnTTbb','TTJetsHadUEdnTTcc','TTJetsHadUEdnTTjj',
'TTJetsHadUEupTT1b','TTJetsHadUEupTT2b','TTJetsHadUEupTTbb','TTJetsHadUEupTTcc','TTJetsHadUEupTTjj',
'TTJetsSemiLepUEdnNjet0TT1b','TTJetsSemiLepUEdnNjet0TT2b','TTJetsSemiLepUEdnNjet0TTbb','TTJetsSemiLepUEdnNjet0TTcc','TTJetsSemiLepUEdnNjet0TTjj',
'TTJetsSemiLepUEupNjet0TT1b','TTJetsSemiLepUEupNjet0TT2b','TTJetsSemiLepUEupNjet0TTbb','TTJetsSemiLepUEupNjet0TTcc','TTJetsSemiLepUEupNjet0TTjj',
'TTJetsSemiLepUEdnNjet9TT1b','TTJetsSemiLepUEdnNjet9TT2b','TTJetsSemiLepUEdnNjet9TTbb','TTJetsSemiLepUEdnNjet9TTcc','TTJetsSemiLepUEdnNjet9TTjj',
'TTJetsSemiLepUEupNjet9TT1b','TTJetsSemiLepUEupNjet9TT2b','TTJetsSemiLepUEupNjet9TTbb','TTJetsSemiLepUEupNjet9TTcc','TTJetsSemiLepUEupNjet9TTjj',
'TTJetsSemiLepUEdnNjet9binTT1b','TTJetsSemiLepUEdnNjet9binTT2b','TTJetsSemiLepUEdnNjet9binTTbb','TTJetsSemiLepUEdnNjet9binTTcc','TTJetsSemiLepUEdnNjet9binTTjj',
'TTJetsSemiLepUEupNjet9binTT1b','TTJetsSemiLepUEupNjet9binTT2b','TTJetsSemiLepUEupNjet9binTTbb','TTJetsSemiLepUEupNjet9binTTcc','TTJetsSemiLepUEupNjet9binTTjj',
]
runData = True
runBkgs = True
runSigs = True
#for ind in range(len(hdampList)):
#        if 'TTJetsSemiLep' in hdampList[ind]: hdampList[ind]=hdampList[ind].replace('TTJetsSemiLep','TTJetsSemiLepInc')
#for ind in range(len(ueList)):
#        if 'TTJetsSemiLep' in ueList[ind]: ueList[ind]=ueList[ind].replace('TTJetsSemiLep','TTJetsSemiLepInc')
# cutList = {'elPtCut':50,'muPtCut':50,'metCut':60,'mtCut':60,'jet1PtCut':0,'jet2PtCut':0,'jet3PtCut':0,'AK4HTCut':510}

cutList = {'elPtCut':20,'muPtCut':20,'metCut':60,'mtCut':60,'jet1PtCut':0,'jet2PtCut':0,'jet3PtCut':0,'AK4HTCut':500}
if year=='R16': 
	cutList['elPtCut'] = 35
	cutList['muPtCut'] = 26

# cutList = {'elPtCut':50,'muPtCut':50,'metCut':60,'mtCut':60,'jet1PtCut':0,'jet2PtCut':0,'jet3PtCut':0,'AK4HTCut':500}

cutString  = 'el'+str(int(cutList['elPtCut']))+'mu'+str(int(cutList['muPtCut']))
cutString += '_MET'+str(int(cutList['metCut']))+'_MT'+str(cutList['mtCut'])
cutString += '_1jet'+str(int(cutList['jet1PtCut']))+'_2jet'+str(int(cutList['jet2PtCut']))+str(int(cutList['jet3PtCut']))

cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
if region=='TTCR': pfix='ttbar_'
elif region=='WJCR': pfix='wjets_'
else: pfix='templates_'
if not isCategorized: pfix='kinematics_'+region+'_'
pfix+=iPlot
pfix+='_TEST_'+datestr#+'_'+timestr
         		
def readTree(file):
	if not os.path.exists(file): 
		print "Error: File does not exist! Aborting ...",file
		os._exit(1)
	tFile = TFile(file,'READ')
	tTree = tFile.Get('ljmet')
	return tFile, tTree 

bigbins = [0,50,100,125,150,175,200,225,250,275,300,325,350,375,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,5000]

nbin_multiplier=1

plotList = {#discriminantName:(discriminantLJMETName, binning, xAxisLabel)
	'deltaRAK8':('minDR_leadAK8otherAK8',linspace(0,5,51).tolist(),';min #DeltaR(1^{st} AK8 jet, other AK8 jet)'),
	'MTlmet':('MT_lepMet',linspace(0,250,51).tolist(),';M_{T}(l,#slash{E}_{T}) [GeV]'),
	'NPV'   :('nPV_MultiLepCalc',linspace(0, 60, 61).tolist(),';PV multiplicity'),
	'nTrueInt':('nTrueInteractions_MultiLepCalc',linspace(0, 75, 76).tolist(),';# true interactions'),
	'lepPt' :('leptonPt_MultiLepCalc',linspace(0, 600, 121).tolist(),';Lepton p_{T} [GeV]'),
	'lepEta':('leptonEta_MultiLepCalc',linspace(-4, 4, 41).tolist(),';Lepton #eta'),
	'JetEta':('theJetEta_JetSubCalc_PtOrdered',linspace(-4, 4, 41).tolist(),';AK4 jet #eta'),
	'JetPt' :('theJetPt_JetSubCalc_PtOrdered',linspace(0, 1500, 51).tolist(),';jet p_{T} [GeV]'),
	'Jet1Pt':('theJetPt_JetSubCalc_PtOrdered[0]',linspace(0, 1500, 51).tolist(),';p_{T}(j_{1}) [GeV]'),
	'Jet2Pt':('theJetPt_JetSubCalc_PtOrdered[1]',linspace(0, 1500, 51).tolist(),';p_{T}(j_{2}) [GeV]'),
	'Jet3Pt':('theJetPt_JetSubCalc_PtOrdered[2]',linspace(0, 800, 51).tolist(),';p_{T}(j_{3}) [GeV]'),
	'Jet4Pt':('theJetPt_JetSubCalc_PtOrdered[3]',linspace(0, 500, 51).tolist(),';p_{T}(j_{4}) [GeV]'),
	'Jet5Pt':('theJetPt_JetSubCalc_PtOrdered[4]',linspace(0, 500, 51).tolist(),';p_{T}(j_{5}) [GeV]'),
	'Jet6Pt':('theJetPt_JetSubCalc_PtOrdered[5]',linspace(0, 500, 51).tolist(),';p_{T}(j_{6}) [GeV]'),
	'JetPtBins' :('theJetPt_JetSubCalc_PtOrdered',linspace(0,2000,21).tolist(),';AK4 jet p_{T} [GeV]'),
	'Jet1PtBins':('theJetPt_JetSubCalc_PtOrdered[0]',linspace(0,2000,21).tolist(),';p_{T}(j_{1}) [GeV]'),
	'Jet2PtBins':('theJetPt_JetSubCalc_PtOrdered[1]',linspace(0,2000,21).tolist(),';p_{T}(j_{2}) [GeV]'),
	'Jet3PtBins':('theJetPt_JetSubCalc_PtOrdered[2]',linspace(0,2000,21).tolist(),';p_{T}(j_{3}) [GeV]'),
	'Jet4PtBins':('theJetPt_JetSubCalc_PtOrdered[3]',linspace(0,2000,21).tolist(),';p_{T}(j_{4}) [GeV]'),
	'Jet5PtBins':('theJetPt_JetSubCalc_PtOrdered[4]',linspace(0,2000,21).tolist(),';p_{T}(j_{5}) [GeV]'),
	'Jet6PtBins':('theJetPt_JetSubCalc_PtOrdered[5]',linspace(0,2000,21).tolist(),';p_{T}(j_{6}) [GeV]'),
	#'MET'   :('corr_met_MultiLepCalc',linspace(0, 1000, 51).tolist(),';#slash{E}_{T} [GeV]'),
	'MET'   :('corr_met_MultiLepCalc',linspace(0, 1000, 51).tolist(),';p_{T}^{miss} [GeV]'),
	'NJets' :('NJets_JetSubCalc',linspace(0, 15, 16).tolist(),';AK4 jet multiplicity'),
	'NBJets':('NJetsCSVwithSF_JetSubCalc',linspace(0, 10, 11).tolist(),';b-tagged jet multiplicity'),
	'NBJetsNoSF':('NJetsCSV_JetSubCalc',linspace(0, 10, 11).tolist(),';b-tagged jet multiplicity'),
	'NDCSVBJets':('NJetsCSVwithSF_MultiLepCalc',linspace(0, 10, 11).tolist(),';b-tagged jet multiplicity'),
	'NDCSVBJetsNoSF':('NJetsCSV_MultiLepCalc',linspace(0, 10, 11).tolist(),';b-tagged jet multiplicity'),
	'NWJets':('NJetsWtagged',linspace(0, 6, 7).tolist(),';W-tagged jet multiplicity'),
	'NTJets':('NJetsTtagged',linspace(0, 4, 5).tolist(),';t-tagged jet multiplicity'),
	'NJetsAK8':('NJetsAK8_JetSubCalc',linspace(0, 8, 9).tolist(),';AK8 jet multiplicity'),
	'JetPtAK8':('theJetAK8Pt_JetSubCalc_PtOrdered',linspace(0, 1500, 51).tolist(),';AK8 jet p_{T} [GeV]'),
	'JetPtBinsAK8':('theJetAK8Pt_JetSubCalc_PtOrdered',bigbins,';AK8 jet p_{T} [GeV];'),
	'JetEtaAK8':('theJetAK8Eta_JetSubCalc_PtOrdered',linspace(-4, 4, 41).tolist(),';AK8 jet #eta'),
	'Tau21'  :('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 jet #tau_{2}/#tau_{1}'),
	'Tau21Nm1'  :('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 jet #tau_{2}/#tau_{1}'),
	'Tau32'  :('theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 jet #tau_{3}/#tau_{2}'),
	'Tau32Nm1'  :('theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 jet #tau_{3}/#tau_{2}'),
	'Pruned' :('theJetAK8PrunedMass_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet pruned mass [GeV]'),
	'PrunedSmeared' :('theJetAK8PrunedMass_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet pruned mass [GeV]'),
	'PrunedSmearedNm1' :('theJetAK8PrunedMassWtagUncerts_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet pruned mass [GeV]'),
	'SoftDropMass' :('theJetAK8SoftDropCorr_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet soft-drop mass [GeV]'),
	'SoftDropMassNm1W' :('theJetAK8SoftDropCorr_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet soft-drop mass [GeV]'),
	'SoftDropMassNm1t' :('theJetAK8SoftDropCorr_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 jet soft-drop mass [GeV]'),
	'mindeltaR':('minDR_lepJet',linspace(0, 4, 51).tolist(),';#DeltaR(l, closest jet)'),
	'deltaRjet1':('deltaR_lepJets[0]',linspace(0, 5, 51).tolist(),';#DeltaR(l,j_{1})'),
	'deltaRjet2':('deltaR_lepJets[1]',linspace(0, 5, 51).tolist(),';#DeltaR(l,j_{2})'),
	'deltaRjet3':('deltaR_lepJets[2]',linspace(0, 5, 51).tolist(),';#DeltaR(l,j_{3})'),
	'nLepGen':('NLeptonDecays_TpTpCalc',linspace(0,10,11).tolist(),';N lepton decays from TT'),
	'METphi':('corr_met_phi_MultiLepCalc',linspace(-3.2,3.2,65).tolist(),';#phi(#slash{E}_{T})'),
	'lepPhi':('leptonPhi_MultiLepCalc',linspace(-3.2,3.2,65).tolist(),';#phi(l)'),
	'lepDxy':('leptonDxy_MultiLepCalc',linspace(-0.02,0.02,51).tolist(),';lepton xy impact param [cm]'),
	'lepDz':('leptonDz_MultiLepCalc',linspace(-0.1,0.1,51).tolist(),';lepton z impact param [cm]'),
	'lepCharge':('leptonCharge_MultiLepCalc',linspace(-2,2,5).tolist(),';lepton charge'),
	'lepIso':('leptonMiniIso_MultiLepCalc',linspace(0,0.1,51).tolist(),';lepton mini isolation'),
	'Tau1':('theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #tau_{1}'),
	'Tau2':('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #tau_{2}'),
	'Tau3':('theJetAK8NjettinessTau3_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #tau_{3}'),
	'JetPhi':('theJetPhi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK4 Jet #phi'),
	'JetPhiAK8':('theJetAK8Phi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK8 Jet #phi'),
	'Bjet1Pt':('BJetLeadPt',linspace(0,1500,51).tolist(),';p_{T}(b_{1}) [GeV]'),  ## B TAG
	'Wjet1Pt':('WJetLeadPt',linspace(0,1500,51).tolist(),';p_{T}(W_{1}) [GeV]'),
	'Tjet1Pt':('TJetLeadPt',linspace(0,1500,51).tolist(),';p_{T}(t_{1}) [GeV]'),
	'topMass':('recLeptonicTopMass',linspace(0,1500,51).tolist(),';M^{rec}(t) [GeV]'),
	'topPt':('recLeptonicTopPt',linspace(0,1500,51).tolist(),';p_{T}^{rec}(t) [GeV]'),
	'minMlj':('minMleppJet',linspace(0,1000,51).tolist(),';min[M(l,j)] [GeV], j #neq b'),
	'minMljDR':('deltaRlepJetInMinMljet',linspace(0,5,51).tolist(),';#DeltaR(l,j) with min[M(l,j)], j #neq b'),
	'minMljDPhi':('deltaPhilepJetInMinMljet',linspace(0,5,51).tolist(),';#Delta#phi(l,jet) with min[M(l,j)], j #neq b'),
	'minMlbDR':('deltaRlepbJetInMinMlb',linspace(0,5,51).tolist(),';#DeltaR(l,b) with min[M(l,b)]'), ## B TAG
	'minMlbDPhi':('deltaPhilepbJetInMinMlb',linspace(0,5,51).tolist(),';#Delta#phi(l,b) with min[M(l,b)]'), ## B TAG
	'nonMinMlbDR':('deltaRlepbJetNotInMinMlb',linspace(0,5,51).tolist(),';#DeltaR(l,b), b #neq b in min[M(l,b)]'),  ## B TAG
	'MWb1':('M_taggedW_bjet1',linspace(0,1000,51).tolist(),';M(W_{jet},b_{1}) [GeV]'), ## B TAG
	'MWb2':('M_taggedW_bjet2',linspace(0,1000,51).tolist(),';M(W_{jet},b_{2}) [GeV]'), ## 2 B TAG
	'deltaRlb1':('deltaRlepbJet1',linspace(0,5,51).tolist(),';#DeltaR(l,b_{1})'), ## B TAG
	'deltaRlb2':('deltaRlepbJet2',linspace(0,5,51).tolist(),';#DeltaR(l,b_{2})'), ## 2 B TAG
	'deltaRtW':('deltaRtopWjet',linspace(0,5,51).tolist(),';#DeltaR(reco t, W jet)'),
	'deltaRlW':('deltaRlepWjet',linspace(0,5,51).tolist(),';#DeltaR(l,W_{jet})'),
	'deltaRWb1':('deltaRtaggedWbJet1',linspace(0,5,51).tolist(),';#DeltaR(W_{jet},b_{1})'), ## B TAG
	'deltaRWb2':('deltaRtaggedWbJet2',linspace(0,5,51).tolist(),';#DeltaR(W_{jet},b_{2})'), ## 2 B TAG
	'deltaPhilb1':('deltaPhilepbJet1',linspace(0,5,51).tolist(),';#Delta#phi(l,b_{1})'), ## B TAG
	'deltaPhilb2':('deltaPhilepbJet2',linspace(0,5,51).tolist(),';#Delta#phi(l,b_{2})'), ## 2 B TAG
	'deltaPhitW':('deltaPhitopWjet',linspace(0,5,51).tolist(),';#Delta#phi(t_{lep}, W_{jet})'),
	'deltaPhilW':('deltaPhilepWjet',linspace(0,5,51).tolist(),';#Delta#phi(l, W_{jet})'),
	'deltaPhiWb1':('deltaPhitaggedWbJet1',linspace(0,5,51).tolist(),';#Delta#phi(W_{jet},b_{1})'), ## B TAG
	'deltaPhiWb2':('deltaPhitaggedWbJet2',linspace(0,5,51).tolist(),';#Delta#phi(W_{jet},b_{2})'), ## 2 B TAG
	'WjetPt':('WJetTaggedPt',linspace(0,1500,51).tolist(),';p_{T}(W_{jet}) [GeV]'),
	'PtRel':('ptRel_lepJet',linspace(0,500,51).tolist(),';p_{T,rel}(l, closest jet) [GeV]'),
	'deltaPhiLMET':('deltaPhi_lepMET',linspace(-3.2,3.2,51).tolist(),';#Delta#phi(l,#slash{E}_{T})'),
	'NHOTtJets':('topNtops_HOTTaggerCalc',linspace(0, 5, 6).tolist(),';resolved t-tagged jet multiplicity'),
	'NresolvedTops1pNoSF':('NresolvedTops1pFakeNoSF',linspace(0, 5, 6).tolist(),';resolved t-tagged jet multiplicity (1% fake)'),
	'NresolvedTops2pNoSF':('NresolvedTops2pFakeNoSF',linspace(0, 5, 6).tolist(),';resolved t-tagged jet multiplicity (2% fake)'),
	'NresolvedTops5pNoSF':('NresolvedTops5pFakeNoSF',linspace(0, 5, 6).tolist(),';resolved t-tagged jet multiplicity (5% fake)'),
	'NresolvedTops10pNoSF':('NresolvedTops10pFakeNoSF',linspace(0, 5, 6).tolist(),';resolved t-tagged jet multiplicity (10% fake)'),
	'NresolvedTops1p':('NresolvedTops1pFake',linspace(0, 5, 6).tolist(),';resolved t-tagged jet multiplicity (1% fake)'),
	'NresolvedTops2p':('NresolvedTops2pFake',linspace(0, 5, 6).tolist(),';resolved t-tagged jet multiplicity (2% fake)'),
	'NresolvedTops5p':('NresolvedTops5pFake',linspace(0, 5, 6).tolist(),';resolved t-tagged jet multiplicity (5% fake)'),
	'NresolvedTops10p':('NresolvedTops10pFake',linspace(0, 5, 6).tolist(),';resolved t-tagged jet multiplicity (10% fake)'),
	'HOTtPt':('topPt_HOTTaggerCalc',linspace(0, 1000, 51).tolist(),';resolved t-tagged jet p_{T} [GeV]'),
	'HOTtEta':('topEta_HOTTaggerCalc',linspace(-4, 4, 41).tolist(),';resolved t-tagged jet #eta'),
	'HOTtPhi':('topPhi_HOTTaggerCalc',linspace(-3.2,3.2,65).tolist(),';resolved t-tagged jet #phi'),
	'HOTtMass':('topMass_HOTTaggerCalc',linspace(0, 500, 51).tolist(),';resolved t-tagged jet mass [GeV]'),
	'HOTtDisc':('topDiscriminator_HOTTaggerCalc',linspace(0,1,51).tolist(),';resolved t-tagged jet discriminator'),
	'HOTtNconst':('topNconstituents_HOTTaggerCalc',linspace(0, 10, 11).tolist(),';resolved t-tagged jet # constituents'),
	'HOTtNAK4':('topNAK4_HOTTaggerCalc',linspace(0, 15, 16).tolist(),';resolved t-tagged jet # AK4 jets'),
	'HOTtDRmax':('topDRmax_HOTTaggerCalc',linspace(0,1,51).tolist(),';resolved t-tagged jet DRmax'),
	'HOTtDThetaMax':('topDThetaMax_HOTTaggerCalc',linspace(0,1,51).tolist(),';resolved t-tagged jet DThetaMax'),
	'HOTtDThetaMin':('topDThetaMin_HOTTaggerCalc',linspace(0,1,51).tolist(),';resolved t-tagged jet DThetaMin'),
	'isHTgt500Njetge9':('isHTgt500Njetge9',linspace(0,2,3).tolist(),';isHTgt500Njetge9'),
	'NJets_vs_NBJets':('NJets_JetSubCalc:NJetsCSV_JetSubCalc',linspace(0, 15, 16).tolist(),';AK4 jet multiplicity',linspace(0, 10, 11).tolist(),';b-tagged jet multiplicity'),
	'HT_vs_HTb':('AK4HT:HT_bjets',linspace(0, 3000, 121).tolist(),';H_{T} [GeV]',linspace(0, 3000, 121).tolist(),';H_{T}^{b} [GeV]'),
	'HT_vs_maxJJJpt':('AK4HT:maxJJJpt',linspace(0, 3000, 121).tolist(),';H_{T} [GeV]',linspace(0, 1500, 101).tolist(),';max[p_{T}^{jjj}] [GeV]'),
	'HTb_vs_maxJJJpt':('HT_bjets:maxJJJpt',linspace(0, 3000, 121).tolist(),';H_{T}^{b} [GeV]',linspace(0, 1500, 101).tolist(),';max[p_{T}^{jjj}] [GeV]'),
	'genHT':('AK4GenHT',linspace(0, 4000, 161).tolist(),';H_{T}^{gen} [GeV]'),
	'genNJets':('NAK4GenJets',linspace(0, 15, 16).tolist(),';gen AK4 jet multiplicity'),

	'maxJJJpt':('maxJJJpt',linspace(0, 1500, 101).tolist(),';max[p_{T}^{jjj}] [GeV]'),
	'HTb':('HT_bjets',linspace(0, 3000, 121).tolist(),';H_{T}^{b} [GeV]'),
	'HT':('AK4HT',linspace(0, 3000, 121).tolist(),';H_{T} [GeV]'),
	'ST':('AK4HTpMETpLepPt',linspace(0, 4000, 161).tolist(),';S_{T} [GeV]'),
	'minMlb':('minMleppBjet',linspace(0, 1000, 101).tolist(),';min[M(l,b)] [GeV]'),
	'minMlbSBins':('minMleppBjet',linspace(0, 1000, 1001).tolist(),';min[M(l,b)] [GeV]'),
	'BDT':('BDT',linspace(-1, 1, 201).tolist(),';BDT'),
	
	
	
	'NJetsCSV_MultiLepCalc':('NJetsCSV_MultiLepCalc',linspace(0, 20, (21-1)*nbin_multiplier+1).tolist(),';b-tagged jet mult. no SF'),

	'thirddeepjetb':('thirddeepjetb',linspace(-2, 1.5, (51-1)*nbin_multiplier+1).tolist(),';DeepJet(3rdDeepJetJet)'),
	'fourthdeepjetb':('fourthdeepjetb',linspace(-2, 1.5, (51-1)*nbin_multiplier+1).tolist(),';DeepJet(4thDeepJetJet)'),
	'HOTGoodTrijet2_deepjet_Jetnotdijet':('HOTGoodTrijet2_deepjet_Jetnotdijet', linspace(-2.2, 1.2, (101-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet2_deepjet_Jetnotdijet'),
	'NJetsCSV_JetSubCalc':('NJetsCSV_JetSubCalc',linspace(0, 10, (11-1)*nbin_multiplier+1).tolist(),';b-tagged DeepJet jet mult. no SF'),

	# BDT input
	'AK4HT':('AK4HT',linspace(0, 4000, (101-1)*nbin_multiplier+1).tolist(),';H_{T} [GeV]'),
	'AK4HTpMETpLepPt':('AK4HTpMETpLepPt',linspace(0, 4000, (101-1)*nbin_multiplier+1).tolist(),';S_{T} [GeV]'),
	'minMleppBjet':('minMleppBjet',linspace(0, 1000, (101-1)*nbin_multiplier+1).tolist(),';min[M(l,b)] [GeV]'),
	'leptonPt_MultiLepCalc' :('leptonPt_MultiLepCalc',linspace(0, 600, (121-1)*nbin_multiplier+1).tolist(),';Lepton p_{T} [GeV]'),
	'corr_met_MultiLepCalc'   :('corr_met_MultiLepCalc',linspace(0, 1500, (51-1)*nbin_multiplier+1).tolist(),';#slash{E}_{T} [GeV]'),
	'NJets_JetSubCalc' :('NJets_JetSubCalc',linspace(0, 25, (26-1)*nbin_multiplier+1).tolist(),';AK4 jet multiplicity'),
	'NJetsCSVwithSF_MultiLepCalc':('NJetsCSVwithSF_MultiLepCalc',linspace(0, 10, (11-1)*nbin_multiplier+1).tolist(),';b-tagged jet multiplicity'),
	'NJetsTtagged':('NJetsTtagged',linspace(0, 4, (5-1)*nbin_multiplier+1).tolist(),';t-tagged jet multiplicity'),
	'MT_lepMet':('MT_lepMet',linspace(0,250,(51-1)*nbin_multiplier+1).tolist(),';M_{T}(l,#slash{E}_{T}) [GeV]'),

	'BDTtrijet2':('BDTtrijet2',linspace(-1, 1, (101-1)*nbin_multiplier+1).tolist(), ';BDTtrijet2'),
	'thirdcsvb_bb':('thirdcsvb_bb',linspace(-2, 1.5, (51-1)*nbin_multiplier+1).tolist(),';DeepCSV(3rdDeepCSVJet)'),
	'fourthcsvb_bb':('fourthcsvb_bb',linspace(-2, 1.5, (51-1)*nbin_multiplier+1).tolist(),';DeepCSV(4thDeepCSVJet)'),
	'fifthJetPt':('fifthJetPt',linspace(0, 400, (101-1)*nbin_multiplier+1).tolist(), ';p_{T}(j_{5}) [GeV]'),
	'BDTtrijet3':('BDTtrijet3',linspace(-1, 1, (101-1)*nbin_multiplier+1).tolist(), ';BDTtrijet3'),
	'sixthJetPt':('sixthJetPt',linspace(0, 400, (51-1)*nbin_multiplier+1).tolist(), ';p_{T}(j_{6}) [GeV]'),
	'BDTtrijet1':('BDTtrijet1',linspace(-1, 1, (101-1)*nbin_multiplier+1).tolist(), ';BDTtrijet1'),
	'MT2bb':('MT2bb',linspace(0, 400, (51-1)*nbin_multiplier+1).tolist(), ';MT2bb [GeV]'),
	'mass_maxJJJpt':('mass_maxJJJpt',linspace(0, 3000, (101-1)*nbin_multiplier+1).tolist(), ';M(jjj) with max[p_{T}(jjj)] [GeV]'),
	'hemiout':('hemiout', linspace(0, 3000, (101-1)*nbin_multiplier+1).tolist(), ';Hemiout [GeV]'),
	'Aplanarity':('Aplanarity',linspace(0, 0.5, (51-1)*nbin_multiplier+1).tolist(), ';Aplanarity'),
	'centrality':('centrality',linspace(0, 1.0, (51-1)*nbin_multiplier+1).tolist(), ';Centrality'),
	'HT_bjets':('HT_bjets',linspace(0, 1800, (101-1)*nbin_multiplier+1).tolist(),';HT(bjets) [GeV]'),
	'FW_momentum_1':('FW_momentum_1',linspace(0, 1.0, (51-1)*nbin_multiplier+1).tolist(), ';1^{st} FW moment [GeV]'),
	'mass_lepBJet0':('mass_lepBJet0',linspace(0, 1800, (101-1)*nbin_multiplier+1).tolist(), ';M(l,b_{1}) [GeV]'),
	'mass_lepBJet_mindr':('mass_lepBJet_mindr',linspace(0, 800, (51-1)*nbin_multiplier+1).tolist(), ';M(l,b) with min[#DeltaR(l,b)] [GeV]'),
	'deltaR_lepBJet_maxpt':('deltaR_lepBJet_maxpt',linspace(0, 6.0, (51-1)*nbin_multiplier+1).tolist(), ';#DeltaR(l,b)] with max[p_{T}(l,b)]'),
	'Sphericity':('Sphericity',linspace(0, 1.0, (51-1)*nbin_multiplier+1).tolist(), ';Sphericity'),
	'deltaR_lepbJetInMinMlb':('deltaR_lepbJetInMinMlb',linspace(0, 6.0, (51-1)*nbin_multiplier+1).tolist(),';#DeltaR(l,b) with min M(l, b)'),
	'minDR_lepBJet':('minDR_lepBJet',linspace(0, 6.0, (51-1)*nbin_multiplier+1).tolist(), ';min[#DeltaR(l,b)]'),
	'mass_maxBBmass':('mass_maxBBmass',linspace(0, 2000, (101-1)*nbin_multiplier+1).tolist(), ';max[M(b,b)] [GeV]'),
	'deltaR_minBB':('deltaR_minBB',linspace(0, 6.0, (51-1)*nbin_multiplier+1).tolist(), ';min[#DeltaR(b,b)]'),
	'aveBBdr':('aveBBdr',linspace(0, 6.0, (51-1)*nbin_multiplier+1).tolist(),';ave[#DeltaR(b,b)]'),
	'ratio_HTdHT4leadjets':('ratio_HTdHT4leadjets',linspace(0, 2.6, (51-1)*nbin_multiplier+1).tolist(),';HT/HT(4 leading jets)'),
	'aveCSVpt':('aveCSVpt',linspace(-0.3, 1.1, (101-1)*nbin_multiplier+1).tolist(),';p_{T} weighted CSV'),
	'mass_lepJets0':('mass_lepJets0', linspace(0, 2200, (101-1)*nbin_multiplier+1).tolist(),';M(l,j_{1}) [GeV]'),
	'mass_minBBdr':('mass_minBBdr', linspace(0, 1400, (51-1)*nbin_multiplier+1).tolist(),';M(b,b) with min[#DeltaR(b,b)] [GeV]'),
	'mass_minLLdr':('mass_minLLdr', linspace(0, 600, (51-1)*nbin_multiplier+1).tolist(),';M(j,j) with min[#DeltaR(j,j)], j #neq b [GeV]'),
	'theJetLeadPt':('theJetLeadPt', linspace(0, 1500, (101-1)*nbin_multiplier+1).tolist(),';p_{T}(j_{1}) [GeV]'),
	'FW_momentum_5':('FW_momentum_5', linspace(0, 0.7, (101-1)*nbin_multiplier+1).tolist(),';5^{th} FW moment [GeV]'),
	'deltaR_lepJetInMinMljet':('deltaR_lepJetInMinMljet', linspace(0, 4.5, (101-1)*nbin_multiplier+1).tolist(),';#DeltaR(l,j) with min M(l, j)'),
	'secondJetPt':('secondJetPt',linspace(0, 2500, (101-1)*nbin_multiplier+1).tolist(), ';p_{T}(j_{2}) [GeV]'),
	'BJetLeadPt':('BJetLeadPt', linspace(0, 2000, (101-1)*nbin_multiplier+1).tolist(),';p_{T}(b_{1}) [GeV]'),
	'csvJet4':('csvJet4', linspace(-2.2, 1.2, (101-1)*nbin_multiplier+1).tolist(),';DeepCSV(4thPtJet)'),
	'lepDR_minBBdr':('lepDR_minBBdr', linspace(-1, 10, (51-1)*nbin_multiplier+1).tolist(),';#DeltaR(l,bb) with min[#DeltaR(b,b)]'),
	'deltaEta_maxBB':('deltaEta_maxBB', linspace(-6, 11, (51-1)*nbin_multiplier+1).tolist(),';max[#Delta#eta(b,b)]'),
	'FW_momentum_0':('FW_momentum_0', linspace(0, 1, (51-1)*nbin_multiplier+1).tolist(),';0^{th} FW moment [GeV]'),
	'FW_momentum_2':('FW_momentum_2', linspace(0, 1, (51-1)*nbin_multiplier+1).tolist(),';2^{nd} FW moment [GeV]'),
	'FW_momentum_3':('FW_momentum_3', linspace(0, 1, (51-1)*nbin_multiplier+1).tolist(),';3^{rd} FW moment [GeV]'),
	'FW_momentum_4':('FW_momentum_4', linspace(0, 1, (51-1)*nbin_multiplier+1).tolist(),';4^{th} FW moment [GeV]'),
	'FW_momentum_6':('FW_momentum_6', linspace(0, 1, (51-1)*nbin_multiplier+1).tolist(),';6^{th} FW moment [GeV]'),
	'mass_lepJets1':('mass_lepJets1', linspace(0, 3000, (101-1)*nbin_multiplier+1).tolist(),';M(l,j_{2}) [GeV]'),
	'mass_lepJets2':('mass_lepJets2', linspace(0, 3000, (101-1)*nbin_multiplier+1).tolist(),';M(l,j_{3}) [GeV]'),
	'PtFifthJet':('PtFifthJet', linspace(-1, 2000, (101-1)*nbin_multiplier+1).tolist(),';5^{th} jet p_{T}, b-jet first [GeV]'),
	'deltaPhi_lepJetInMinMljet':('deltaPhi_lepJetInMinMljet', linspace(-4, 4, (51-1)*nbin_multiplier+1).tolist(),';#DeltaPhi(l,j) with min M(l, j)'),
	'deltaPhi_lepbJetInMinMlb':('deltaPhi_lepbJetInMinMlb', linspace(-11, 5, (101-1)*nbin_multiplier+1).tolist(),';#DeltaPhi(l,b) with min M(l, b)'),
	'M_allJet_W':('M_allJet_W', linspace(0, 10000, (201-1)*nbin_multiplier+1).tolist(),';M(allJets, leptoninc W) [GeV]'),
	'csvJet3':('csvJet3', linspace(-2.2, 1.2, (101-1)*nbin_multiplier+1).tolist(),';DeepCSV(3rdPtJet)'),
	'HT_2m':('HT_2m', linspace(-20, 5000, (201-1)*nbin_multiplier+1).tolist(),';HTwoTwoPtBjets [GeV]'),
	'BDTtrijet4':('BDTtrijet4', linspace(-1, 1, (51-1)*nbin_multiplier+1).tolist(),';trijet4 discriminator'),
	'NresolvedTops1pFake':('NresolvedTops1pFake', linspace(0, 5, (6-1)*nbin_multiplier+1).tolist(),';resolvedTop multiplicity'),
	'NJetsWtagged':('NJetsWtagged', linspace(0, 5, (6-1)*nbin_multiplier+1).tolist(),';W multiplicity'),
	'HOTGoodTrijet1_mass':('HOTGoodTrijet1_mass', linspace(0, 300, (51-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet1_mass [GeV]'),
	'HOTGoodTrijet1_dijetmass':('HOTGoodTrijet1_dijetmass', linspace(0, 250, (51-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet1_dijetmass [GeV]'),
	'HOTGoodTrijet1_pTratio':('HOTGoodTrijet1_pTratio', linspace(0, 1, (51-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet1_pTratio'),
	'HOTGoodTrijet1_dRtridijet':('HOTGoodTrijet1_dRtridijet', linspace(0, 4, (51-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet1_dRtridijet'),
	'HOTGoodTrijet1_dRtrijetJetnotdijet':('HOTGoodTrijet1_dRtrijetJetnotdijet', linspace(0, 4, (51-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet1_dRtrijetJetnotdijet'),
	'HOTGoodTrijet1_csvJetnotdijet':('HOTGoodTrijet1_csvJetnotdijet', linspace(-2.2, 1.2, (101-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet1_csvJetnotdijet'),
	'HOTGoodTrijet2_mass':('HOTGoodTrijet2_mass', linspace(0, 300, (51-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet2_mass [GeV]'),
	'HOTGoodTrijet2_dijetmass':('HOTGoodTrijet2_dijetmass', linspace(0, 250, (51-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet2_dijetmass [GeV]'),
	'HOTGoodTrijet2_pTratio':('HOTGoodTrijet2_pTratio', linspace(0, 1, (51-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet2_pTratio'),
	'HOTGoodTrijet2_dRtridijet':('HOTGoodTrijet2_dRtridijet', linspace(0, 4, (51-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet2_dRtridijet'),
	'HOTGoodTrijet2_dRtrijetJetnotdijet':('HOTGoodTrijet2_dRtrijetJetnotdijet', linspace(0, 4, (51-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet2_dRtrijetJetnotdijet'),
	'HOTGoodTrijet2_csvJetnotdijet':('HOTGoodTrijet2_csvJetnotdijet', linspace(-2.2, 1.2, (101-1)*nbin_multiplier+1).tolist(),';HOTGoodTrijet2_csvJetnotdijet'),

	'thirdcsvb_bb_BTagBHad':('thirdcsvb_bb_BTagBHad',linspace(-2, 1.5, (51-1)*nbin_multiplier+1).tolist(),';DeepCSV(3rdDeepCSVJet) BTagBHad'),
	'thirdcsvb_bb_BTagNBHad':('thirdcsvb_bb_BTagNBHad',linspace(-2, 1.5, (51-1)*nbin_multiplier+1).tolist(),';DeepCSV(3rdDeepCSVJet) BTagNBHad'),
	'thirdcsvb_bb_NBTagBHad':('thirdcsvb_bb_NBTagBHad',linspace(-2, 1.5, (51-1)*nbin_multiplier+1).tolist(),';DeepCSV(3rdDeepCSVJet) NBTagBHad'),
	'thirdcsvb_bb_NBTagNBHad':('thirdcsvb_bb_NBTagNBHad',linspace(-2, 1.5, (51-1)*nbin_multiplier+1).tolist(),';DeepCSV(3rdDeepCSVJet) NBTagNBHad'),


	'DNN_disc_6j_40vars':('DNN_disc_6j_40vars',linspace(0, 1, 201).tolist(),';DNN_{6j,40v}'),
	'DNN_disc_6j_50vars':('DNN_disc_6j_50vars',linspace(0, 1, 201).tolist(),';DNN_{6j,50v}'),
	'DNN_disc_6j_76vars':('DNN_disc_6j_76vars',linspace(0, 1, 201).tolist(),';DNN_{6j,76v}'),
	'DNN_disc_4j_40vars':('DNN_disc_4j_40vars',linspace(0, 1, 201).tolist(),';DNN_{4j,40v}'),
	'DNN_disc_4j_50vars':('DNN_disc_4j_50vars',linspace(0, 1, 201).tolist(),';DNN_{4j,50v}'),
	'DNN_disc_4j_76vars':('DNN_disc_4j_76vars',linspace(0, 1, 201).tolist(),';DNN_{4j,76v}'),

	'XGB':('XGB',linspace(0, 1, 201).tolist(),';XGB'),
	'XGB_RS':('XGB_RS',linspace(0, 1, 201).tolist(),';XGB_RS'),
	
	'btagCSVWeight':('btagCSVWeight',linspace(0, 5, 1001).tolist(),';btagCSVWeight'),
	'btagCSV2DWeight_HTnj':('btagCSV2DWeight_HTnj',linspace(0, 5, 1001).tolist(),';btagCSV2DWeight_HTnj'),
	'btagTotWeight':('btagCSVWeight*btagCSV2DWeight_HTnj',linspace(0, 5, 1001).tolist(),';btagTotWeight'),

	# 'nPV_MultiLepCalc':('BDT_tt',linspace(-1, 1, 201).tolist(),';N_{PV}'),

	'BDT_tt':('BDT_tt',linspace(-1, 1, 201).tolist(),';BDT(tt)'),
	'BDT_ttH':('BDT_ttH',linspace(-1, 1, 201).tolist(),';BDT(ttH)'),
	'BDT_ttbb':('BDT_ttbb',linspace(-1, 1, 201).tolist(),';BDT(ttbb)'),

	'BDTsum':('BDT_tt + BDT_ttH + BDT_ttbb',linspace(-3, 3, 201).tolist(),';BDT(tt+ttH+ttbb)'),#BDT_tt + BDT_ttH + BDT_ttbb
	'BDTprod':('(1+BDT_tt) * (1+BDT_ttH) * (1+BDT_ttbb)',linspace(0, 8, 201).tolist(),';BDT(tt*ttH*ttbb)'),#(1+BDT_tt) * (1+BDT_ttH) * (1+BDT_ttbb)

	'BDTtt+tth':('BDT_tt+BDT_ttH',linspace(-2, 2, 201).tolist(),';BDT(tt+tth)'),#BDT_tt+BDT_ttH
	'BDTtth+ttbb':('BDT_ttH+BDT_ttbb',linspace(-2, 2, 201).tolist(),';BDT(tth+ttbb)'),#BDT_ttH+BDT_ttbb
	'BDTtt+ttbb':('BDT_tt+BDT_ttbb',linspace(-2, 2, 201).tolist(),';BDT(tt+ttbb)'),#BDT_tt+BDT_ttbb

	'BDTtt*tth':('(1+BDT_tt)*(1+BDT_ttH)',linspace(0,4, 201).tolist(),';BDT(tt*tth)'),#(1+BDT_tt)*(1+BDT_ttH)
	'BDTtth*ttbb':('(1+BDT_ttH)*(1+BDT_ttbb)',linspace(0,4, 201).tolist(),';BDT(tth*ttbb)'),#(1+BDT_ttH)*(1+BDT_ttbb)
	'BDTtt*ttbb':('(1+BDT_tt)*(1+BDT_ttbb)',linspace(0,4, 201).tolist(),';BDT(tt*ttbb)'),#(1+BDT_tt)*(1+BDT_ttbb)

	'BDTtt+tthVSttbb':('BDT_tt+BDT_ttH:BDT_ttbb',linspace(-2, 2, 21).tolist(),';BDT(tt+tth)',linspace(-1, 1, 21).tolist(),';BDT(ttbb)'),#BDT_tt+BDT_ttH vs BDT_ttbb
	'BDTtth+ttbbVStt':('BDT_ttH+BDT_ttbb:BDT_tt',linspace(-2, 2, 21).tolist(),';BDT(tth+ttbb)',linspace(-1, 1, 21).tolist(),';BDT(tt)'),#BDT_tt vs BDT_ttH+BDT_ttbb
	'BDTtt+ttbbVStth':('BDT_tt+BDT_ttbb:BDT_ttH',linspace(-2, 2, 21).tolist(),';BDT(tt+ttbb)',linspace(-1, 1, 21).tolist(),';BDT(tth)'),#BDT_tt+BDT_ttbb vs BDT_ttH 

	'BDTtt*tthVSttbb':('(1+BDT_tt)*(1+BDT_ttH):(1+BDT_ttbb)',linspace(0, 4, 21).tolist(),';BDT(tt*tth)',linspace(0, 2, 21).tolist(),';BDT(ttbb)'),#(1+BDT_tt)*(1+BDT_ttH) vs (1+BDT_ttbb)
	'BDTtth*ttbbVStt':('(1+BDT_ttH)*(1+BDT_ttbb):(1+BDT_tt)',linspace(0, 4, 21).tolist(),';BDT(tth*ttbb)',linspace(0, 2, 21).tolist(),';BDT(tt)'),#(1+BDT_tt) vs (1+BDT_ttH)*(1+BDT_ttbb)
	'BDTtt*ttbbVStth':('(1+BDT_tt)*(1+BDT_ttbb):(1+BDT_ttH)',linspace(0, 4, 21).tolist(),';BDT(tt*ttbb)',linspace(0, 2, 21).tolist(),';BDT(tth)'),#(1+BDT_tt)*(1+BDT_ttbb) vs (1+BDT_ttH)  

	}

formulas=[]
if year=='R16':
	formulas=['0.161392213863*(((BDT_tt+1)/2)**(3.56925019116-1))*((1-((BDT_tt+1)/2))**(2.01882334842-1))+2609.86460705*(((BDT_tt+1)/2)**(17.5543222955-1))*((1-((BDT_tt+1)/2))**(7.09320356567-1))', 
	'0.210062930065*(((BDT_ttH+1)/2)**(3.42210681906-1))*((1-((BDT_ttH+1)/2))**(2.59375440288-1))+0.231071133492*(((BDT_ttH+1)/2)**(5.32060470182-1))*((1-((BDT_ttH+1)/2))**(2.54357167004-1))', 
	'60.4443511616*(((BDT_ttbb+1)/2)**(6.40102354493-1))*((1-((BDT_ttbb+1)/2))**(8.00662703815-1))+79.8750757749*(((BDT_ttbb+1)/2)**(11.0539053232-1))*((1-((BDT_ttbb+1)/2))**(4.80503245508-1))']
	
elif year=='R17':
	formulas=['1.80285607805*(((BDT_tt+1)/2)**(4.47878238245-1))*((1-((BDT_tt+1)/2))**(6.20318556649-1))+0.662781522535*(((BDT_tt+1)/2)**(5.90466486371-1))*((1-((BDT_tt+1)/2))**(2.41500321437-1))', 
	'2.72151626622*(((BDT_ttH+1)/2)**(4.73700764643-1))*((1-((BDT_ttH+1)/2))**(4.6125214758-1))+37.1132208779*(((BDT_ttH+1)/2)**(13.9232333459-1))*((1-((BDT_ttH+1)/2))**(4.04261462352-1))', 
	'186.309313064*(((BDT_ttbb+1)/2)**(6.78975967148-1))*((1-((BDT_ttbb+1)/2))**(9.90153049205-1))+32.7478765599*(((BDT_ttbb+1)/2)**(9.41806330245-1))*((1-((BDT_ttbb+1)/2))**(4.49649165325-1))']

elif year=='R18':
	formulas=['0.124534243951*(((BDT_tt+1)/2)**(3.39535418049-1))*((1-((BDT_tt+1)/2))**(1.85602173784-1))+676.875360617*(((BDT_tt+1)/2)**(18.0775148802-1))*((1-((BDT_tt+1)/2))**(6.1689408943-1))', 
	'1.10918667877*(((BDT_ttH+1)/2)**(4.2182693221-1))*((1-((BDT_ttH+1)/2))**(3.88616870942-1))+9.64766083427*(((BDT_ttH+1)/2)**(12.3568700088-1))*((1-((BDT_ttH+1)/2))**(3.52160124479-1))', 
	'8.39651180513*(((BDT_ttbb+1)/2)**(5.63835388879-1))*((1-((BDT_ttbb+1)/2))**(5.44458402604-1))+817.942828051*(((BDT_ttbb+1)/2)**(15.8949232503-1))*((1-((BDT_ttbb+1)/2))**(5.5909367171-1))']

plotList['LBDT']=('('+formulas[0]+')*('+formulas[1]+')*('+formulas[2]+')',linspace(0, 1, 201).tolist(),';LBDT(tt*ttH*ttbb)')
plotList['LBDTtt*tthVSttbb']=('('+formulas[0]+')*('+formulas[1]+'):('+formulas[2]+')',linspace(0, 1, 21).tolist(),';LBDT(tt*tth)',linspace(0, 1, 21).tolist(),';LBDT(ttbb)')
plotList['LBDTtth*ttbbVStt']=('('+formulas[1]+')*('+formulas[2]+'):('+formulas[0]+')',linspace(0, 1, 21).tolist(),';LBDT(tth*ttbb)',linspace(0, 1, 21).tolist(),';LBDT(tt)')
plotList['LBDTtt*ttbbVStth' ]=('('+formulas[0]+')*('+formulas[2]+'):('+formulas[1]+')',linspace(0, 1, 21).tolist(),';LBDT(tt*ttbb)',linspace(0, 1, 21).tolist(),';LBDT(tth)')

print "PLOTTING:",iPlot
print "         LJMET Variable:",plotList[iPlot][0]
print "         X-AXIS TITLE  :",plotList[iPlot][2]
print "         BINNING USED  :",plotList[iPlot][1]

catList = ['is'+cat[0]+'_nHOT'+cat[1]+'_nT'+cat[2]+'_nW'+cat[3]+'_nB'+cat[4]+'_nJ'+cat[5] for cat in list(itertools.product(isEMlist,nhottlist,nttaglist,nWtaglist,nbtaglist,njetslist))]
nCats  = len(catList)

shapesFiles = ['JEC','JER']#,
# 'JEC_Total','JEC_FlavorQCD',
# 'JEC_RelativeBal','JEC_RelativeSample_'+year.replace('R','20'),
# 'JEC_Absolute','JEC_Absolute_'+year.replace('R','20'),
# 'JEC_HF','JEC_HF_'+year.replace('R','20'),
# 'JEC_EC2','JEC_EC2_'+year.replace('R','20'),
# 'JEC_BBEC1','JEC_BBEC1_'+year.replace('R','20')]
#if year == 'R18': shapesFiles += ['hem']

tTreeData = {}
tFileData = {}
catInd = 1
for cat in catList:
	if not runData: break
	catDir = catList[2:]
	datahists = {}
	if len(sys.argv)>1: outDir=sys.argv[1]
	else: 
		outDir = os.getcwd()
		outDir+='/'+pfix
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+cutString
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+catDir
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
	for data in dataList: 
		tFileData[data],tTreeData[data]=readTree(step1Dir+'/'+samples[data]+'_hadd.root')
		datahists.update(analyze(tTreeData,data,'',cutList,'',False,doPDF,iPlot,plotList[iPlot],cat,region,year))
		if catInd==nCats: 
			del tFileData[data]
			del tTreeData[data]
	pickle.dump(datahists,open(outDir+'/datahists_'+iPlot+'.p','wb'))
	catInd+=1

tTreeBkg = {}
tFileBkg = {}
catInd = 1
for cat in catList:
	if not runBkgs: break
	catDir = catList[2:]
	bkghists  = {}
	if len(sys.argv)>1: outDir=sys.argv[1]
	else: 
		outDir = os.getcwd()
		outDir+='/'+pfix
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+cutString
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+catDir
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
	for bkg in bkgList: 
		if 'TTJets' in bkg and tagABCDnn!='': tFileBkg[bkg],tTreeBkg[bkg]=readTree(step1Dir.replace('_step3','_step3_ABCDnn')+'/'+samples[bkg]+'_ABCDnn_hadd.root')
		else: tFileBkg[bkg],tTreeBkg[bkg]=readTree(step1Dir+'/'+samples[bkg]+'_hadd.root')
		if doAllSys:
			for syst in shapesFiles:
				for ud in ['Up','Down']:
					tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=readTree(step1Dir.replace('nominal',syst+ud.lower())+'/'+samples[bkg]+'_hadd.root')
		bkghists.update(analyze(tTreeBkg,bkg,'',cutList,tagABCDnn,doAllSys,doPDF,iPlot,plotList[iPlot],cat,region,year))
		if 'TTJets' in bkg and len(ttFlvs)!=0:
			for flv in ttFlvs: bkghists.update(analyze(tTreeBkg,bkg,flv,cutList,tagABCDnn,doAllSys,doPDF,iPlot,plotList[iPlot],cat,region,year))
		if catInd==nCats: 
			del tFileBkg[bkg]
			del tTreeBkg[bkg]
		if doAllSys and catInd==nCats:
			for syst in shapesFiles:
				for ud in ['Up','Down']: 
					del tFileBkg[bkg+syst+ud]
					del tTreeBkg[bkg+syst+ud]
	if doHDsys: 
		for hdamp in hdampList: 
			tFileBkg[hdamp],tTreeBkg[hdamp]=readTree(step1Dir+'/'+samples[hdamp]+'_hadd.root')
			for syst in shapesFiles:
				for ud in ['Up','Down']:
					tFileBkg[hdamp+syst+ud],tTreeBkg[hdamp+syst+ud]=None,None
			bkghists.update(analyze(tTreeBkg,hdamp,'',cutList,'',False,doPDF,iPlot,plotList[iPlot],cat,region,year))
			if catInd==nCats: 
				del tFileBkg[hdamp]
				del tTreeBkg[hdamp]
	if doUEsys: 
		for ue in ueList: 
			tFileBkg[ue],tTreeBkg[ue]=readTree(step1Dir+'/'+samples[ue]+'_hadd.root')
			for syst in shapesFiles:
				for ud in ['Up','Down']:
					tFileBkg[ue+syst+ud],tTreeBkg[ue+syst+ud]=None,None
			bkghists.update(analyze(tTreeBkg,ue,'',cutList,'',False,doPDF,iPlot,plotList[iPlot],cat,region,year))
			if catInd==nCats: 
				del tFileBkg[ue]
				del tTreeBkg[ue]
	pickle.dump(bkghists,open(outDir+'/bkghists_'+iPlot+'.p','wb'))
	catInd+=1

tTreeSig = {}
tFileSig = {}
catInd = 1
for cat in catList:
	if not runSigs: break
	catDir = catList[2:]
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
	for sig in sigList: 
		for decay in decays: 
			tFileSig[sig+decay],tTreeSig[sig+decay]=readTree(step1Dir+'/'+samples[sig+decay]+'_hadd.root')
			if doAllSys:
				for syst in shapesFiles:
					for ud in ['Up','Down']:
						print "        "+syst+ud
						tFileSig[sig+decay+syst+ud],tTreeSig[sig+decay+syst+ud]=readTree(step1Dir.replace('nominal',syst+ud.lower())+'/'+samples[sig+decay]+'_hadd.root')
			sighists.update(analyze(tTreeSig,sig+decay,'',cutList,'',doAllSys,doPDF,iPlot,plotList[iPlot],cat,region,year))
			if catInd==nCats: 
				del tFileSig[sig+decay]
				del tTreeSig[sig+decay]
			if doAllSys and catInd==nCats:
				for syst in shapesFiles:
					for ud in ['Up','Down']: 
						del tFileSig[sig+decay+syst+ud]
						del tTreeSig[sig+decay+syst+ud]
	pickle.dump(sighists,open(outDir+'/sighists_'+iPlot+'.p','wb'))
	catInd+=1

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))

