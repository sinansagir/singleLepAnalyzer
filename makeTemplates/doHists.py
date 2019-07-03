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
step1Dir = 'root://cmseos.fnal.gov//store/user/jmanagan/LJMet94X_1lepTTdnn_042219_step2hadds/nominal'

iPlot = 'HT' #minMlb' #choose a discriminant from plotList below!
if len(sys.argv)>2: iPlot=sys.argv[2]
region = 'TTCR'
if len(sys.argv)>3: region=sys.argv[3]
isCategorized = True
if len(sys.argv)>4: isCategorized=int(sys.argv[4])
doJetRwt= 1
doTopRwt= 0
doAllSys= False
cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='templatesTest'+region
if not isCategorized: pfix='kinematicsTEST'+region
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
	'DYMG','WJetsMG400','WJetsMG600','WJetsMG800','WJetsMG1200','WJetsMG2500',
	'TTJetsHad0','TTJetsHad700','TTJetsHad1000','TTJetsSemiLep0','TTJetsSemiLep700','TTJetsSemiLep1000','TTJets2L2nu0','TTJets2L2nu700','TTJets2L2nu1000',
	'TTJetsPH700mtt','TTJetsPH1000mtt','Ts','Tbs','Tt','Tbt','TtW','TbtW','TTW','TTZ','TTH',
	'WW','WZ','ZZ',
	'QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000'
	]

dataList = [
	'DataERRBCDEF',
	'DataMRRBCDEF',
	#'Data18EG',
	#'Data18MU',
	]

whichSignal = 'TT' #HTB, TT, BB, or X53X53
massList = range(1000,1800+1,100)
sigList = [whichSignal+'M'+str(mass) for mass in massList]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in massList for chiral in ['left','right']]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': 
	decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
	sigList.remove('BBM1700')
if whichSignal=='X53X53': decays = [''] #decays to tWtW 100% of the time
if whichSignal=='HTB': decays = ['']

cutList = {'lepPtCut':55,'metCut':50,'nAK8Cut':3,'dnnCut':0.50,'HTCut':510} ## also requires mass reco worked
if 'CR' in region :cutList = {'lepPtCut':55,'metCut':50,'nAK8Cut':3,'dnnCut':0.50,'HTCut':510} 
if 'PS' in region :cutList = {'lepPtCut':55,'metCut':50,'nAK8Cut':0,'dnnCut':0.0,'HTCut':510} ## most basic
if 'NoDR' in region: cutList = {'lepPtCut':55,'metCut':50,'nAK8Cut':2,'dnnCut':0.0,'HTCut':510} ## not used anymore

cutString  = ''
		
if len(sys.argv)>5: isEMlist=[str(sys.argv[5])]
else: isEMlist = ['E','M']
if len(sys.argv)>6: taglist=[str(sys.argv[6])]
else: 
	taglist = ['all']
	if isCategorized: taglist=['taggedbWbW','taggedtHbW','taggedtHtH','taggedtZbW','taggedtZtH','taggedtZtZ','taggedtZHtZH','notV']
if len(sys.argv)>7: algolist=[str(sys.argv[7])]
else: 
	algolist = ['all']
	if isCategorized or 'algos' in region: algolist = ['DeepAK8']

def readTree(file):
#	if not EOSpathExists(file[23:]): 
#		print "Error: File does not exist! Aborting ...",file[23:]
#		os._exit(1)
	tFile = TFile.Open(file,'READ')
	tTree = tFile.Get('ljmet')
	return tFile, tTree 

print "READING TREES"
shapesFiles = ['jec','btag']
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
	print step1Dir+'/'+samples[bkg]+'_hadd.root'
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
        'tmass':('t_mass',linspace(0,500,51).tolist(),';M(t) [GeV]'),
        'Wmass':('W_mass',linspace(0,250,51).tolist(),';M(W) [GeV]'),
        'tpt':('t_pt',linspace(0,1000,51).tolist(),';M(t) [GeV]'),
        'Wpt':('W_pt',linspace(0,1000,51).tolist(),';M(W) [GeV]'),
        'Wdrlep':('W_dRLep',linspace(0,5,51).tolist(),';leptonic W, #DeltaR(W,lepton)'),
        'tdrWb':('t_dRWb',linspace(0,5,51).tolist(),';leptonic t, #DeltaR(W,b)'),
	'isLepW':('isLeptonic_W',linspace(0,2,3).tolist(),';lepton from W'),
        'Tp1Mass':('Tprime1_DeepAK8_Mass',linspace(0,4000,51).tolist(),';M(T) [GeV]'), ## replace with ALGO if needed
        'Tp2Mass':('Tprime2_DeepAK8_Mass',linspace(0,4000,nbins).tolist(),';M(T) [GeV]'),
        'Tp2MDnn':('Tprime2_DeepAK8_Mass',linspace(0,4000,nbins).tolist(),';M(T) [GeV]'), #analyze.py makes notV DnnTprime
        'Tp2MST':('Tprime2_DeepAK8_Mass',linspace(0,4000,nbins).tolist(),';M(T) [GeV]'), #analyze.py makes notV ST
        'Tp1Pt':('Tprime1_DeepAK8_Pt',linspace(0,3000,51).tolist(),';T quark p_{T} [GeV]'),
        'Tp2Pt':('Tprime2_DeepAK8_Pt',linspace(0,3000,51).tolist(),';T quark p_{T} [GeV]'),
        'Tp1Eta':('Tprime1_DeepAK8_Eta',linspace(-5,5,51).tolist(),';T quark #eta'),
        'Tp2Eta':('Tprime2_DeepAK8_Eta',linspace(-5,5,51).tolist(),';T quark #eta'),
        'Tp1Phi':('Tprime1_DeepAK8_Phi',linspace(-3.14,3.14).tolist(),';T quark #phi'),
        'Tp2Phi':('Tprime2_DeepAK8_Phi',linspace(-3.14,3.14,51).tolist(),';T quark #phi'),
        'Tp1deltaR':('Tprime1_DeepAK8_deltaR',linspace(0,5,51).tolist(),';#DeltaR(T quark product jets)'),
        'Tp2deltaR':('Tprime2_DeepAK8_deltaR',linspace(0,5,51).tolist(),';#DeltaR(T quark product jets)'),
	'DnnTprime':('dnn_Tprime',linspace(0,1,nbins).tolist(),';DNN VLQ score'),
	'DnnTTbar':('dnn_ttbar',linspace(0,1,51).tolist(),';DNN t#bar{t} score'),
	'DnnWJets':('dnn_WJets',linspace(0,1,51).tolist(),';DNN W+jets score'),
        'probSumDecay':('probSum_DeepAK8_decay',linspace(0,20,21).tolist(),';weighted sum of decay product probabilities'), ## replace with ALGO if needed
        'probSumFour':('probSum_DeepAK8_four',linspace(0,5,6).tolist(),';sum of W/Z/H/t probabilities'),
        'probb':('dnn_B_DeepAK8Calc_PtOrdered',linspace(0,1,51).tolist(),';B score'),  ## replace with AlgoCalc if needed
        'probh':('dnn_H_DeepAK8Calc_PtOrdered',linspace(0,1,51).tolist(),';H score'),  ## change back for BEST
        'probj':('dnn_J_DeepAK8Calc_PtOrdered',linspace(0,1,51).tolist(),';J score'),
        'probt':('dnn_T_DeepAK8Calc_PtOrdered',linspace(0,1,51).tolist(),';t score'),
        'probw':('dnn_W_DeepAK8Calc_PtOrdered',linspace(0,1,51).tolist(),';W score'),
        'probz':('dnn_Z_DeepAK8Calc_PtOrdered',linspace(0,1,51).tolist(),';Z score'),
	'dnnLargest':('dnn_largest_DeepAK8Calc_PtOrdered',linspace(0,10,11).tolist(),';dnn largest score'),
	'nB':('nB_DeepAK8',linspace(0,5,6).tolist(),';number of B quarks'),  ## replace with ALGO if needed
	'nH':('nH_DeepAK8',linspace(0,5,6).tolist(),';number of H bosons'),
	'nT':('nT_DeepAK8',linspace(0,5,6).tolist(),';number of T quarks'),
	'nW':('nW_DeepAK8',linspace(0,5,6).tolist(),';number of W bosons'),
	'nZ':('nZ_DeepAK8',linspace(0,5,6).tolist(),';number of Z bosons'),

	'deltaRAK8':('minDR_leadAK8otherAK8',linspace(0,5,51).tolist(),';min #DeltaR(1^{st} AK8 jet, other AK8 jet)'),
	'minDRlepAK8':('minDR_lepAK8',linspace(0,5,51).tolist(),';min #DeltaR(l, AK8 jet)'),
	'minDPhiMetJet':('minDPhi_MetJet',linspace(-3.2,3.2,33).tolist(),':min #Delta#phi(MET, AK4 jet)'),
	'MTlmet':('MT_lepMet',linspace(0,250,51).tolist(),';M_{T}(l,#slash{E}_{T}) [GeV]'),
	'MTlmetmod':('MT_lepMetmod',linspace(0,250,51).tolist(),';M_{T}(l,mod #slash{E}_{T}) [GeV]'),
	'NPV'   :('nPV_singleLepCalc',linspace(0, 100, 101).tolist(),';PV multiplicity;'),
	'NTrue'   :('nTrueInteractions_singleLepCalc',linspace(0, 100, 101).tolist(),';MC pileup multiplicity;'),
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
	'MET'   :('corr_met_singleLepCalc',linspace(0, 1500, 51).tolist(),';#slash{E}_{T} [GeV];'),
	'METmod'   :('corr_metmod_singleLepCalc',linspace(0, 1500, 51).tolist(),';modified #slash{E}_{T} [GeV];'),
	'NJets' :('NJets_JetSubCalc',linspace(0, 15, 16).tolist(),';jet multiplicity;'),
	'NBJets':('NJetsCSVwithSF_JetSubCalc',linspace(0, 10, 11).tolist(),';b tag multiplicity;'),
	'NBJetsNoSF':('NJetsCSV_JetSubCalc',linspace(0, 10, 11).tolist(),';b tag multiplicity;'),
	'NJetsAK8':('NJetsAK8_JetSubCalc',linspace(0, 8, 9).tolist(),';AK8 Jet multiplicity;'),
	'JetPtAK8':('theJetAK8Pt_JetSubCalc_PtOrdered',linspace(0, 1500, 51).tolist(),';AK8 Jet p_{T} [GeV];'),
	'JetPtBinsAK8':('theJetAK8Pt_JetSubCalc_PtOrdered',bigbins,';AK8 Jet p_{T} [GeV];'),
	'JetEtaAK8':('theJetAK8Eta_JetSubCalc_PtOrdered',linspace(-4, 4, 41).tolist(),';AK8 Jet #eta;'),

	'Tau21'  :('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{2}/#tau_{1};'),
	'Tau21Nm1'  :('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{2}/#tau_{1};'),
	'Tau32'  :('theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{3}/#tau_{2};'),
	'Tau32Nm1'  :('theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0, 1, 51).tolist(),';AK8 Jet #tau_{3}/#tau_{2};'),

	'SoftDrop' :('theJetAK8SoftDropCorr_JetSubCalc_PtOrdered',linspace(0, 500, 51).tolist(),';AK8 CHS soft drop mass [GeV];'),
	'SoftDropWZNm1' :('theJetAK8SoftDropCorr_JetSubCalc_PtOrdered',linspace(0, 300, 51).tolist(),';AK8 CHS soft drop mass [GeV];'),
	'SoftDropHNm1' :('theJetAK8SoftDropCorr_JetSubCalc_PtOrdered',linspace(0, 300, 51).tolist(),';AK8 CHS soft drop mass [GeV];'),
	'SoftDropTNm1' :('theJetAK8SoftDropCorr_JetSubCalc_PtOrdered',linspace(0, 300, 51).tolist(),';AK8 CHS soft drop mass [GeV];'),
	'SoftDropNsubBNm1':('theJetAK8SDSubjetNDeepCSVMSF_PtOrdered',linspace(0, 3, 4).tolist(),';b-tagged subjet multiplicity (CHS SD);'),
	'DoubleBNm1':('theJetAK8DoubleB_JetSubCalc_PtOrdered',linspace(-1,1,51).tolist(),';DoubleB discriminator;'),

	'mindeltaR':('minDR_lepJet',linspace(0, 5, 51).tolist(),';min #DeltaR(l, jet);'),
	'mindeltaRAK8':('minDR_lepAK8',linspace(0, 5, 51).tolist(),';min #DeltaR(l, AK8 jet);'),
	'deltaRjet1':('deltaR_lepJets[0]',linspace(0, 5, 51).tolist(),';#DeltaR(l, 1^{st} jet);'),
	'deltaRjet2':('deltaR_lepJets[1]',linspace(0, 5, 51).tolist(),';#DeltaR(l, 2^{nd} jet);'),
	'deltaRjet3':('deltaR_lepJets[2]',linspace(0, 5, 51).tolist(),';#DeltaR(l, 3^{rd} jet);'),
	'nLepGen':('NLeptonDecays_TpTpCalc',linspace(0,10,11).tolist(),';N lepton decays from TT'),
	'METphi':('corr_met_phi_singleLepCalc',linspace(-3.2,3.2,65).tolist(),';#phi(#slash{E}_{T})'),
	'lepPhi':('leptonPhi_singleLepCalc',linspace(-3.2,3.2,65).tolist(),';#phi(l)'),
	'lepIso':('leptonMiniIso_singleLepCalc',linspace(0,0.2,51).tolist(),';lepton mini isolation'),
	'Tau1':('theJetAK8NjettinessTau1_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #tau_{1}'),
	'Tau2':('theJetAK8NjettinessTau2_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #tau_{2}'),
	'Tau3':('theJetAK8NjettinessTau3_JetSubCalc_PtOrdered',linspace(0,1,51).tolist(),';AK8 Jet #tau_{3}'),
	'JetPhi':('theJetPhi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK4 Jet #phi'),
	'JetPhiAK8':('theJetAK8Phi_JetSubCalc_PtOrdered',linspace(-3.2,3.2,65).tolist(),';AK8 Jet #phi'),
	'topMass':('topMass',linspace(0,1500,51).tolist(),';reconstructed M(t) [GeV]'),
	'topPt':('topPt',linspace(0,1500,51).tolist(),';reconstructed pT(t) [GeV]'),
	'minMlj':('minMleppJet',linspace(0,1000,51).tolist(),';min[M(l,jet)] [GeV], 0 b tags'),
	'PtRel':('ptRel_lepJet',linspace(0,500,51).tolist(),';p_{T,rel}(l, closest jet) [GeV]'),
	'PtRelAK8':('ptRel_lepAK8',linspace(0,500,51).tolist(),';p_{T,rel}(l, closest AK8 jet) [GeV]'),

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
print 'Cat list:',catList
nCats  = len(catList)
catInd = 1
for cat in catList:
	print 'Category:',cat
 	catDir = cat[0]+'_'+cat[1]+'_'+cat[2]
 	datahists = {}
 	bkghists  = {}
 	sighists  = {}
 	if len(sys.argv)>1:
		outDir=sys.argv[1]
		sys.path.append(outDir)
 	else: 
		outDir = os.getcwd()
		outDir+='/'+pfix
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		outDir+='/'+catDir
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
 	category = {'isEM':cat[0],'tag':cat[1],'algo':cat[2]}
	print 'Running analyze'
 	for data in dataList: 
 		datahists.update(analyze(tTreeData,data,cutList,False,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized,whichSignal))
 		if catInd==nCats: del tFileData[data]
 	for bkg in bkgList: 
		#print bkg,bkghists
 		bkghists.update(analyze(tTreeBkg,bkg,cutList,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized,whichSignal))
 		if catInd==nCats: del tFileBkg[bkg]
 		if doAllSys and catInd==nCats:
 			for syst in shapesFiles:
 				for ud in ['Up','Down']: del tFileBkg[bkg+syst+ud]
 	for sig in sigList: 
 	 	for decay in decays: 
 	 		sighists.update(analyze(tTreeSig,sig+decay,cutList,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region,isCategorized,whichSignal))
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
