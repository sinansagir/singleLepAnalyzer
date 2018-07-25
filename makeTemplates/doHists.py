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
execfile("/uscms_data/d3/jmanagan/EOSSafeUtils.py")

gROOT.SetBatch(1)
start_time = time.time()

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
step1Dir = 'root://cmseos.fnal.gov//store/user/lpcljm/2018/LJMet94X_1lepTT_072418_step1hadds/nominal'

iPlot = 'Tp2Mass' #minMlb' #choose a discriminant from plotList below!
if len(sys.argv)>2: iPlot=sys.argv[2]
region = 'SR'
if len(sys.argv)>3: region=sys.argv[3]
isCategorized = 1
if len(sys.argv)>4: isCategorized=int(sys.argv[4])
doJetRwt= 1
doAllSys= False

cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
if region=='CR':    pfix='templatesCR_'
if region=='SR':    pfix='templatesSR_'
if region=='PS':    pfix='templatesPS__'
if region=='noDR':  pfix='templatesnoDR_'
if region=='CRinc': pfix='templatesCRinc_'
else: pfix='templatesTEST_'
if not isCategorized: pfix='kinematicsTEST_'+region+''
#pfix+=iPlot
#pfix+='_'+datestr#+'_'+timestr

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
	'WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500',
	#'TTJetsPH',
	#'QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000'
	]

dataList = [
	#'DataERRBCDEFGH','DataMRRBCDEFGH'
	]

whichSignal = 'TT' #HTB, TT, BB, or X53X53
massList = range(1100,1800+1,100)
sigList = [whichSignal+'M'+str(mass) for mass in massList]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in massList for chiral in ['left','right']]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
if whichSignal=='X53X53': decays = [''] #decays to tWtW 100% of the time
if whichSignal=='HTB': decays = ['']

cutList = {'lepPtCut':50,'metCut':55,'nAK8Cut':2,'drCut':3.0,'HTCut':480}
if 'PS' in region :cutList = {'lepPtCut':50,'metCut':55,'nAK8Cut':0,'drCut':10.0,'HTCut':480}
if 'noDR' in region: cutList = {'lepPtCut':50,'metCut':55,'nAK8Cut':2,'drCut':10.0,'HTCut':480}

cutString  = 'lep'+str(int(cutList['lepPtCut']))+'_MET'+str(int(cutList['metCut']))
cutString += '_nAK8'+str(cutList['nAK8Cut'])+'_DR'+str(cutList['drCut'])
cutString += 'HT'+str(cutList['HTCut'])
		
if len(sys.argv)>5: isEMlist=[str(sys.argv[5])]
else: isEMlist = ['E','M']
if len(sys.argv)>6: taglist=[str(sys.argv[6])]
else: 
	if not isCategorized: taglist = ['isVnotV']
	elif region=='SR': taglist=['isV_bWbW','isV_tHbW','isV_tHtH','isV_tZbW','isV_tZtH','isV_tZtZ','notV']
	elif region=='CR': taglist=['isVnotV']
	elif region=='CRinc': taglist=['isV_bWbW','isV_tHbW','isV_tHtH','isV_tZbW','isV_tZtH','isV_tZtZ','notV']
	else: taglist = ['isVnotV']
if len(sys.argv)>7: algolist=[str(sys.argv[7])]
else: algolist = ['BEST','DeepAK8','DeepAK8_decorr']

def readTree(file):
	if not EOSpathExists(file[23:]): 
		print "Error: File does not exist! Aborting ...",file[23:]
		os._exit(1)
	tFile = TFile.Open(file,'READ')
	tTree = tFile.Get('ljmet')
	return tFile, tTree 

print "READING TREES"
shapesFiles = []
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
for bkg in bkgList:
	print "READING:",bkg
	print "        nominal"
	tFileBkg[bkg],tTreeBkg[bkg]=readTree(step1Dir+'/'+samples[bkg]+'_hadd.root')
	if doAllSys:
		for syst in shapesFiles:
			for ud in ['Up','Down']:
      			       	print "        "+syst+ud
		       		tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=readTree(step1Dir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+'_hadd.root')
print "FINISHED READING"

#bigbins = [0,50,100,150,200,250,300,350,400,450,500,600,700,800,1000,1200,1500]
bigbins = [0,50,100,125,150,175,200,225,250,275,300,325,350,375,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2500,3000,3500,4000,5000]

nbins = 51
xmax = 800
if isCategorized and 'SR' in region: 
	nbins = 101
	xmax = 1000

plotList = {#discriminantName:(discriminantLJMETName, binning, xAxisLabel)
	'Tp2Mass':('Tprime2_ALGO_Mass',linspace(0,3000,51).tolist(),';M(T) [GeV])'),
	'deltaRAK8':('minDR_leadAK8otherAK8',linspace(0,5,51).tolist(),';min #DeltaR(1^{st} AK8 jet, other AK8 jet)'),
	'minDRlepAK8':('minDR_lepAK8',linspace(0,5,51).tolist(),';min #DeltaR(l, AK8 jet)'),
	'masslepAK81':('mass_lepAK8s[0]',linspace(0,1500,51).tolist(),';M(l, AK8 jet 1) [GeV]'),
	'masslepAK82':('mass_lepAK8s[1]',linspace(0,1500,51).tolist(),';M(l, AK8 jet 2) [GeV]'),
	'deltaRlepAK81':('deltaR_lepAK8s[0]',linspace(0,5,51).tolist(),';#DeltaR(l, AK8 jet 1)'),
	'deltaRlepAK82':('deltaR_lepAK8s[1]',linspace(0,5,51).tolist(),';#DeltaE(l, AK8 jet 2)'),
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
	'NBJetsNotH':('NJetsCSVnotH_JetSubCalc',linspace(0, 10, 11).tolist(),';b tag multiplicity (not CHS Htag);'),
	'NBJetsNotPH':('NJetsCSVnotPH_JetSubCalc',linspace(0, 10, 11).tolist(),';b tag multiplicity (not Puppi Htag);'),
	'NBJetsNoSF':('NJetsCSV_JetSubCalc',linspace(0, 10, 11).tolist(),';b tag multiplicity;'),
	'NWJets':('NJetsWtagged_0p6',linspace(0, 6, 7).tolist(),';W tag multiplicity (CHS Pruning);'),
	'PuppiNWJets':('NPuppiWtagged_0p55',linspace(0, 6, 7).tolist(),';W tag multiplicity (Puppi SD);'),
	'NTJets':('NJetsTtagged_0p81',linspace(0, 4, 5).tolist(),';t tag multiplicity;'),
	'NH1bJets':('NJetsH1btagged',linspace(0, 4, 5).tolist(),';H1b tag multiplicity (CHS Pruning);'),
	'NH2bJets':('NJetsH2btagged',linspace(0, 4, 5).tolist(),';H2b tag multiplicity (CHS Pruning);'),
	'PuppiNH1bJets':('NPuppiH1btagged',linspace(0, 4, 5).tolist(),';H1b tag multiplicity (Puppi SD);'),
	'PuppiNH2bJets':('NPuppiH2btagged',linspace(0, 4, 5).tolist(),';H2b tag multiplicity (Puppi SD);'),
	'NJetsAK8':('NJetsAK8_JetSubCalc',linspace(0, 8, 9).tolist(),';AK8 Jet multiplicity;'),
	'JetPtAK8':('theJetAK8Pt_JetSubCalc_PtOrdered',linspace(0, 1500, 51).tolist(),';AK8 Jet p_{T} [GeV];'),
	'JetPtBinsAK8':('theJetAK8Pt_JetSubCalc_PtOrdered',bigbins,';AK8 Jet p_{T} [GeV];'),
	'JetEtaAK8':('theJetAK8Eta_JetSubCalc_PtOrdered',linspace(-4, 4, 41).tolist(),';AK8 Jet #eta;'),

	'Tau21'  :('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{2}/#tau_{1};'),
	'Tau21Nm1'  :('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{2}/#tau_{1} (CHS Pruning);'),
	'PuppiTau21'  :('theJetAK8PUPPITau2_JetSubCalc_PtOrdered/theJetAK8PUPPITau1_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet Puppi #tau_{2}/#tau_{1};'),
	'PuppiTau21Nm1'  :('theJetAK8PUPPITau2_JetSubCalc_PtOrdered/theJetAK8PUPPITau1_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet Puppi #tau_{2}/#tau_{1} (Puppi SD);'),
	'Tau32'  :('theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{3}/#tau_{2};'),
	'Tau32Nm1'  :('theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{3}/#tau_{2} (CHS SD);'),

	'Pruned' :('theJetAK8PrunedMassWtagUncerts_JetSubCalc_PtOrdered',linspace(0, 300, 51).tolist(),';AK8 CHS Pruned mass [GeV];'),
	'PrunedWNm1' :('theJetAK8PrunedMassWtagUncerts_JetSubCalc_PtOrdered',linspace(0, 300, 51).tolist(),';AK8 CHS Pruned mass [GeV];'),
	'PrunedHNm1' :('theJetAK8PrunedMassWtagUncerts_JetSubCalc_PtOrdered',linspace(0, 300, 51).tolist(),';AK8 CHS Pruned mass [GeV];'),
	'PrunedNsubBNm1':('theJetAK8SDSubjetNCSVM_PtOrdered',linspace(0, 3, 4).tolist(),';b-tagged subjet multiplicity (CHS Pruning);'),

	'SoftDrop' :('theJetAK8SoftDropMass_JetSubCalc_PtOrdered',linspace(0, 300, 51).tolist(),';AK8 CHS soft drop mass [GeV];'),
	'SoftDropHNm1' :('theJetAK8SoftDropMass_JetSubCalc_PtOrdered',linspace(0, 300, 51).tolist(),';AK8 CHS soft drop mass [GeV];'),
	'SoftDropTNm1' :('theJetAK8SoftDropMass_JetSubCalc_PtOrdered',linspace(0, 300, 51).tolist(),';AK8 CHS soft drop mass [GeV];'),
	'SoftDropNsubBNm1':('theJetAK8SDSubjetNCSVM_PtOrdered',linspace(0, 3, 4).tolist(),';b-tagged subjet multiplicity (CHS SD);'),

	'PuppiSDRaw' :('theJetAK8PUPPISoftDropRaw_JetSubCalc_PtOrdered',linspace(0.2, 300, 51).tolist(),';AK8 Puppi soft drop raw mass [GeV];'),
	'PuppiSDCorr' :('theJetAK8PUPPISoftDropCorr_JetSubCalc_PtOrdered',linspace(0.2, 300, 51).tolist(),';AK8 Puppi soft drop corrected mass [GeV];'),
	'PuppiSD' :('theJetAK8PUPPISoftDrop_PtOrdered',linspace(0.2, 300, 51).tolist(),';AK8 Puppi soft drop mass [GeV];'),
	'PuppiSDWNm1' :('theJetAK8PUPPISoftDrop_PtOrdered',linspace(0.2, 300, 51).tolist(),';AK8 Puppi soft drop mass [GeV];'),
	'PuppiSDRawWNm1' :('theJetAK8PUPPISoftDropRaw_JetSubCalc_PtOrdered',linspace(0.2, 300, 51).tolist(),';AK8 Puppi soft drop raw mass [GeV];'),
	'PuppiSDCorrWNm1' :('theJetAK8PUPPISoftDropCorr_JetSubCalc_PtOrdered',linspace(0.2, 300, 51).tolist(),';AK8 Puppi soft drop corrected mass [GeV];'),
	'PuppiSDHNm1' :('theJetAK8PUPPISoftDrop_PtOrdered',linspace(0.2, 300, 51).tolist(),';AK8 Puppi soft drop mass [GeV];'),
	'PuppiNsubBNm1':('theJetAK8SDSubjetNCSVM_PtOrdered',linspace(0, 3, 4).tolist(),';b-tagged subjet multiplicity (Puppi SD);'),

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
	'Tau3':('theJetAK8NjettinessTau3_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #tau_{3}'),
	'JetPhi':('theJetPhi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK4 Jet #phi'),
	'JetPhiAK8':('theJetAK8Phi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK8 Jet #phi'),
	'Bjet1Pt':('BJetLeadPt',linspace(0,1500,51).tolist(),';1^{st} b jet p_{T} [GeV]'),  ## B TAG
	'Wjet1Pt':('WJetLeadPt',linspace(0,1500,51).tolist(),';1^{st} W jet p_{T} [GeV]'),
	'Tjet1Pt':('TJetLeadPt',linspace(0,1500,51).tolist(),';1^{st} t jet p_{T} [GeV]'),
	'topMass':('topMass',linspace(0,1500,51).tolist(),';reconstructed M(t) [GeV]'),
	'topPt':('topPt',linspace(0,1500,51).tolist(),';reconstructed pT(t) [GeV]'),
	'minMlj':('minMleppJet',linspace(0,1000,51).tolist(),';min[M(l,jet)] [GeV], 0 b tags'),
	'PtRel':('ptRel_lepJet',linspace(0,500,51).tolist(),';p_{T,rel}(l, closest jet) [GeV]'),

	'HT':('AK4HT',linspace(0, 5000, nbins).tolist(),';H_{T} (GeV);'),
	'ST':('AK4HTpMETpLepPt',linspace(0, 5000, nbins).tolist(),';S_{T} (GeV);'),
	'minMlb':('minMleppBjet',linspace(0, xmax, nbins).tolist(),';min[M(l,b)] (GeV);'),
	'minMlbST':('minMleppBjet',linspace(0, xmax, nbins).tolist(),';min[M(l,b)] (GeV);'), #analyze.py will use ST for H tag bins
	}

print "PLOTTING:",iPlot
print "         LJMET Variable:",plotList[iPlot][0]
print "         X-AXIS TITLE  :",plotList[iPlot][2]
print "         BINNING USED  :",plotList[iPlot][1]

catList = list(itertools.product(isEMlist,taglist,algolist))
nCats  = len(catList)
catInd = 1
for cat in catList:
 	catDir = cat[0]+'_'+cat[1]+'_'+cat[2]
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
 	category = {'isEM':cat[0],'tag':cat[1],'algo':cat[2]}
 	for data in dataList: 
 		datahists.update(analyze(tTreeData,data,cutList,False,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
 		if catInd==nCats: del tFileData[data]
 	for bkg in bkgList: 
 		bkghists.update(analyze(tTreeBkg,bkg,cutList,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
 		if catInd==nCats: del tFileBkg[bkg]
 		if doAllSys and catInd==nCats:
 			for syst in shapesFiles:
 				for ud in ['Up','Down']: del tFileBkg[bkg+syst+ud]
 	for sig in sigList: 
 	 	for decay in decays: 
 	 		sighists.update(analyze(tTreeSig,sig+decay,cutList,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized))
 	 		if catInd==nCats: del tFileSig[sig+decay]
 	 		if doAllSys and catInd==nCats:
 	 			for syst in shapesFiles:
 	 				for ud in ['Up','Down']: del tFileSig[sig+decay+syst+ud]

 	#Negative Bin Correction
	for bkg in bkghists.keys(): negBinCorrection(bkghists[bkg])
 	for sig in sighists.keys(): negBinCorrection(sighists[sig])

 	# #OverFlow Correction
 	for data in datahists.keys(): overflow(datahists[data])
 	for bkg in bkghists.keys():   overflow(bkghists[bkg])
 	for sig in sighists.keys():   overflow(sighists[sig])

 	pickle.dump(datahists,open(outDir+'/datahists_'+iPlot+'.p','wb'))
	pickle.dump(bkghists,open(outDir+'/bkghists_'+iPlot+'.p','wb'))
	pickle.dump(sighists,open(outDir+'/sighists_'+iPlot+'.p','wb'))
 	catInd+=1

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))

