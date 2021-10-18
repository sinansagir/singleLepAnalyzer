#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools,getopt
from ROOT import TH1D,gROOT,TFile,TTree
from numpy import linspace
parent = os.path.dirname(os.getcwd())
thisdir= os.path.dirname(os.getcwd()+'/')
sys.path.append(parent)
#from weights import *
from analyze import *
#from samples import *
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
doJetRwt= 0
doAllSys= False
doHDsys = False
doUEsys = False
doPDF = True
if not doAllSys:
	doHDsys = False
	doUEsys = False
	doPDF = False

isEMlist  = ['E','M']
nhottlist = ['0p']
nttaglist = ['0','1p']
nWtaglist = ['0','1p']
nbtaglist = ['1','2p']
njetslist = ['4p']
if not isCategorized: 
	nhottlist = ['0p']
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['1p']
	njetslist = ['3p']

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

if year=='R16':
	from weights16 import *
	from samples16 import *
elif year=='R17':
	from weights17 import *
	from samples17 import *
elif year=='R18':
	from weights18 import *
	from samples18 import *

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
step1Dir = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+year[1:]+'_Oct2019_X53_061321_step1hadds/nominal'

bkgList = [
		  'DYMG200','DYMG400','DYMG600','DYMG800','DYMG1200','DYMG2500',
		  'WJetsMG200','WJetsMG400','WJetsMG600','WJetsMG800',
		  
          'TTJetsHad0','TTJetsHad700','TTJetsHad1000',
          'TTJetsSemiLep01','TTJetsSemiLep02','TTJetsSemiLep700','TTJetsSemiLep1000',
          'TTJets2L2nu0','TTJets2L2nu700','TTJets2L2nu1000',
          'TTJets700mtt','TTJets1000mtt',
		  
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
			   'TTJetsSemiLep03','TTJetsSemiLep04','TTJetsSemiLep05','Tbs']
elif year=='R18':
	bkgList+= ['WJetsMG1200','WJetsMG2500']
ttFlvs = []#'_tt2b','_ttbb','_ttb','_ttcc','_ttlf']

dataList = ['DataE','DataM']#,'DataJ']

whichSignal = 'X53' #HTB, TT, BB, X53 or tttt
massList = range(900,1800,100)
sigList = [whichSignal+'M'+str(mass) for mass in massList]
if whichSignal=='tttt': sigList = [whichSignal]
if whichSignal=='X53': 
	if year == 'R17': 
		sigList = [whichSignal+'LHM'+str(mass) for mass in [1100,1200,1400,1700]]
		sigList+= [whichSignal+'RHM'+str(mass) for mass in range(900,1700+1,100)]
	elif year == 'R18': 
		sigList = [whichSignal+'LHM'+str(mass) for mass in [1100,1200,1400,1500,1700]]
		sigList+= [whichSignal+'RHM'+str(mass) for mass in range(900,1700+1,100)]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
elif whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
else: decays = [''] #there is only one possible decay mode!

hdampList = [#hDamp samples
'TTJets2L2nuHDAMPdnTTbb','TTJets2L2nuHDAMPdnTTcc','TTJets2L2nuHDAMPdnTTjj',
'TTJets2L2nuHDAMPupTTbb','TTJets2L2nuHDAMPupTTcc','TTJets2L2nuHDAMPupTTjj',
'TTJetsHadHDAMPdnTTbb','TTJetsHadHDAMPdnTTcc','TTJetsHadHDAMPdnTTjj',
'TTJetsHadHDAMPupTTbb','TTJetsHadHDAMPupTTcc','TTJetsHadHDAMPupTTjj',
'TTJetsSemiLepHDAMPdnTTbb','TTJetsSemiLepHDAMPdnTTcc','TTJetsSemiLepHDAMPdnTTjj',
'TTJetsSemiLepHDAMPupTTbb','TTJetsSemiLepHDAMPupTTcc','TTJetsSemiLepHDAMPupTTjj',
]
ueList = [#UE samples
'TTJets2L2nuUEdnTTbb','TTJets2L2nuUEdnTTcc','TTJets2L2nuUEdnTTjj',
'TTJets2L2nuUEupTTbb','TTJets2L2nuUEupTTcc','TTJets2L2nuUEupTTjj',
'TTJetsHadUEdnTTbb','TTJetsHadUEdnTTcc','TTJetsHadUEdnTTjj',
'TTJetsHadUEupTTbb','TTJetsHadUEupTTcc','TTJetsHadUEupTTjj',
'TTJetsSemiLepUEdnTTbb','TTJetsSemiLepUEdnTTcc','TTJetsSemiLepUEdnTTjj',
'TTJetsSemiLepUEupTTbb','TTJetsSemiLepUEupTTcc','TTJetsSemiLepUEupTTjj',
]
runData = True
runBkgs = True
runSigs = True

#X5/3 2016
cutList = {'lepPtCut':80,'metCut':100,'mtCut':0,'drCut':0,'jet1PtCut':250,'jet2PtCut':150, 'jet3PtCut':0, 'AK4HTCut':510}
if (region=='SR' or 'CR' in region) and (iPlot=='ST' or iPlot=='HT'):
    cutList = {'lepPtCut':80,'metCut':100,'mtCut':0,'drCut':1,'jet1PtCut':250,'jet2PtCut':150, 'jet3PtCut':0, 'AK4HTCut':510}

cutString  = 'lep'+str(int(cutList['lepPtCut']))
cutString += '_MET'+str(int(cutList['metCut']))+'_MT'+str(cutList['mtCut'])+'_DR'+str(cutList['drCut'])
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
	#'MET'   :('corr_met_MultiLepCalc',linspace(0, 1500, 51).tolist(),';#slash{E}_{T} [GeV]'),
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
	'mindeltaR':('minDR_lepJet',linspace(0, 5, 51).tolist(),';#DeltaR(l, closest jet)'),
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

	'HT':('AK4HT',linspace(0, 4000, 101).tolist(),';H_{T} [GeV]'),
	'ST':('AK4HTpMETpLepPt',linspace(0, 4000, 101).tolist(),';S_{T} [GeV]'),
#	'minMlb':('minMleppBjet',linspace(0, 1000, 51).tolist(),';min[M(l,b)] [GeV]'),
#	'HT':('AK4HT',linspace(450, 4000, 711).tolist(),';H_{T} [GeV]'),
#	'ST':('AK4HTpMETpLepPt',linspace(650, 4000, 671).tolist(),';S_{T} [GeV]'),
	'minMlb':('minMleppBjet',linspace(0, 1000, 101).tolist(),';min[M(l,b)] [GeV]'),
	'minMlbSBins':('minMleppBjet',linspace(0, 1000, 1001).tolist(),';min[M(l,b)] [GeV]'),
	'BDT':('BDT',linspace(-1, 1, 201).tolist(),';BDT'),
	}

print "PLOTTING:",iPlot
print "         LJMET Variable:",plotList[iPlot][0]
print "         X-AXIS TITLE  :",plotList[iPlot][2]
print "         BINNING USED  :",plotList[iPlot][1]

catList = ['is'+cat[0]+'_nHOT'+cat[1]+'_nT'+cat[2]+'_nW'+cat[3]+'_nB'+cat[4]+'_nJ'+cat[5] for cat in list(itertools.product(isEMlist,nhottlist,nttaglist,nWtaglist,nbtaglist,njetslist))]
nCats  = len(catList)

shapesFiles = ['JEC','JER']

tTreeData = {}
tFileData = {}
catInd = 1
for cat in catList:
	if not runData: break
	catDir = cat[2:]
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
		datahists.update(analyze(tTreeData,data,'',cutList,False,doPDF,iPlot,plotList[iPlot],cat,region,year))
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
	catDir = cat[2:]
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
		tFileBkg[bkg],tTreeBkg[bkg]=readTree(step1Dir+'/'+samples[bkg]+'_hadd.root')
		if doAllSys:
			for syst in shapesFiles:
				for ud in ['Up','Down']:
					tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=readTree(step1Dir.replace('nominal',syst+ud.lower())+'/'+samples[bkg]+'_hadd.root')
		bkghists.update(analyze(tTreeBkg,bkg,'',cutList,doAllSys,doPDF,iPlot,plotList[iPlot],cat,region,year))
		if 'TTJets' in bkg and len(ttFlvs)!=0:
			for flv in ttFlvs: bkghists.update(analyze(tTreeBkg,bkg,flv,cutList,doAllSys,doPDF,iPlot,plotList[iPlot],cat,region,isCategorized))
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
			bkghists.update(analyze(tTreeBkg,hdamp,'',cutList,False,doPDF,iPlot,plotList[iPlot],cat,region,year))
			if catInd==nCats: 
				del tFileBkg[hdamp]
				del tTreeBkg[hdamp]
	if doUEsys: 
		for ue in ueList: 
			tFileBkg[ue],tTreeBkg[ue]=readTree(step1Dir+'/'+samples[ue]+'_hadd.root')
			for syst in shapesFiles:
				for ud in ['Up','Down']:
					tFileBkg[ue+syst+ud],tTreeBkg[ue+syst+ud]=None,None
			bkghists.update(analyze(tTreeBkg,ue,'',cutList,False,doPDF,iPlot,plotList[iPlot],cat,region,year))
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
	catDir = cat[2:]
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
						tFileSig[sig+decay+syst+ud],tTreeSig[sig+decay+syst+ud]=readTree(step1Dir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[sig+decay]+'_hadd.root')
			sighists.update(analyze(tTreeSig,sig+decay,'',cutList,doAllSys,doPDF,iPlot,plotList[iPlot],cat,region,year))
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

