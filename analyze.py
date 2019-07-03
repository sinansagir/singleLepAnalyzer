#!/usr/bin/python
from ROOT import TH1D,TTree,TFile
from array import array
from numpy import linspace
from weights import *

"""
--This function will make kinematic plots for a given distribution for electron, muon channels and their combination
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
def analyze(tTree,process,cutList,doAllSys,doJetRwt,iPlot,plotDetails,category,region,isCategorized,whichSig):
	print "*****"*20
	print "*****"*20
	print "DISTRIBUTION:", iPlot
	print "            -name in ljmet trees:", plotDetails[0]
	print "            -x-axis label is set to:", plotDetails[2]
	print "            -using the binning as:", plotDetails[1]
	plotTreeName=plotDetails[0]
	xbins=array('d', plotDetails[1])
	xAxisLabel=plotDetails[2]
	
	print "/////"*5
	print "PROCESSING: ", process
	print "/////"*5

	# Define categories
	isEM  = category['isEM']
	tag   = category['tag']
	algo  = category['algo']
	catStr = 'is'+isEM+'_'+tag#+'_'+algo
	if algo != '': catStr = catStr+'_'+algo
	if 'ALGO' in plotTreeName: plotTreeName = plotTreeName.replace("ALGO",algo)
	if 'Algo' in plotTreeName: 
		if algo == 'BEST': plotTreeName = plotTreeName.replace('Algo','Best')
		elif algo == 'DeepAK8': 
			plotTreeName = plotTreeName.replace('Algo','DeepAK8')
			plotTreeName = plotTreeName.replace('Top','T')
			plotTreeName = plotTreeName.replace('Higgs','H')
			plotTreeName = plotTreeName.replace('QCD','J')
		elif algo == 'DeepAK8DC':
			plotTreeName = plotTreeName.replace('Algo','DeepAK8')
			plotTreeName = plotTreeName.replace('dnn_','decorr_')
			plotTreeName = plotTreeName.replace('Top','T')
			plotTreeName = plotTreeName.replace('Higgs','H')
			plotTreeName = plotTreeName.replace('QCD','J')

	# Define general cuts (These are the only cuts for 'PS')
	cut  = '(leptonPt_singleLepCalc > '+str(cutList['lepPtCut'])+')'
	cut += ' && (corr_met_singleLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (AK4HT > '+str(cutList['HTCut'])+')'
	cut += ' && (nPV_singleLepCalc > 50)'
	#cut += ' && (minDR_lepJet > 0.4 || ptRel_lepJet > 40)' // done in step1 now by removing jet
	
	if 'CR' in region: # 'CR' or 'CRinc'  certain AK8 jets and low signal node
		cut += ' && (NJetsAK8_JetSubCalc >= '+str(cutList['nAK8Cut'])+') && (dnn_Tprime < '+str(cutList['dnnCut'])+')'
		if 'TT' in region: cut += ' && (dnn_ttbar > dnn_WJets)'
		if 'WJ' in region: cut += ' && (dnn_ttbar <= dnn_WJets)'
	elif 'SR' in region: # 'SR'  certain AK8 jets, mass reco, high signal node
		cut += ' && (NJetsAK8_JetSubCalc >= '+str(cutList['nAK8Cut'])+') && (Tprime2_'+algo+'_Mass > -1) && (dnn_Tprime >= '+str(cutList['dnnCut'])+')'
	elif 'NoDR' in region: # 'noDR'
		cut += ' && (NJetsAK8_JetSubCalc >= '+str(cutList['nAK8Cut'])+') && (minDR_leadAK8otherAK8 < '+str(cutList['drCut'])+')'
	elif 'PS' in region: # 'PS'  
		cut += ' && (NJetsAK8_JetSubCalc >= '+str(cutList['nAK8Cut'])+')'
		if '0b' in region: cut += ' && (NJetsCSVwithSF_JetSubCalc == 0)'
		elif '1b' in region: cut += ' && (NJetsCSVwighSF_JetSubCalc == 1)'
		elif '2b' in region: cut += ' && (NJetsCSVwithSF_JetSubCalc >= 2)'

	# Define weights
	TrigEffUp = '1'
	TrigEffDn = '1'
	TrigEff = '1'
	cut += ' && DataPastTrigger == 1 && MCPastTrigger == 1'

	jetSFstr='1'
	jetSFstrUp = '1'
	jetSFstrDn = '1'
	if (process!='WJetsMG' and 'WJetsMG' in process):
		jetSFstr = 'HTSF_Pol'
		jetSFstrUp = 'HTSF_PolUp'
		jetSFstrDn = 'HTSF_PolDn'
		#jetSFstr = str(genHTweight[process])

	weightStr = '1'
	if 'Data' not in process: 
		# replaced isoSF, MuTrkSF with 1
		weightStr          += ' * '+jetSFstr+' * '+TrigEff+' * pileupWeightUp * lepIdSF * EGammaGsfSF * L1NonPrefiringProb_CommonCalc * '+str(weight[process])
		#if 'TTJets' in process: weightStr = 'topPtWeight13TeV * '+weightStr
		if whichSig not in process: weightStr += ' * (MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc))' ## approx pos PDF in signal with no weight this iteration

		#weightTrigEffUpStr  = weightStr.replace(TrigEff,TrigEffUp)
		#weightTrigEffDownStr= weightStr.replace(TrigEff,TrigEffDn)
		weightPileupUpStr   = weightStr.replace('pileupWeight','pileupWeightUp')
		weightPileupDownStr = weightStr.replace('pileupWeight','pileupWeightDown')
		weightPrefireUpStr   = weightStr.replace('L1NonPrefiringProb_CommonCalc','L1NonPrefiringProbUp_CommonCalc')
		weightPrefireDownStr = weightStr.replace('L1NonPrefiringProb_CommonCalc','L1NonPrefiringProbDown_CommonCalc')
		weightmuRFcorrdUpStr   = 'renormWeights[5] * '+weightStr
		weightmuRFcorrdDownStr = 'renormWeights[3] * '+weightStr
		weightmuRUpStr      = 'renormWeights[4] * '+weightStr
		weightmuRDownStr    = 'renormWeights[2] * '+weightStr
		weightmuFUpStr      = 'renormWeights[1] * '+weightStr
		weightmuFDownStr    = 'renormWeights[0] * '+weightStr
		weighttopptUpStr    = weightStr.replace('topPtWeight13TeV','1')
		weighttopptDownStr  = weightStr #.replace('topPtWeight13TeV','topPtWeight13TeV*topPtWeight13TeV')
		weightjsfUpStr      = weightStr.replace(jetSFstr,jetSFstrUp)
		weightjsfDownStr    = weightStr.replace(jetSFstr,jetSFstrDn)
		weightTeffUpStr     = weightStr + ' * DeepAK8SF_TeffUp'
		weightTeffDownStr   = weightStr + ' * DeepAK8SF_TeffDn'
		weightTmisUpStr     = weightStr + ' * DeepAK8SF_TmisUp'
		weightTmisDownStr   = weightStr + ' * DeepAK8SF_TmisDn'
		weightHeffUpStr     = weightStr + ' * DeepAK8SF_HeffUp'
		weightHeffDownStr   = weightStr + ' * DeepAK8SF_HeffDn'
		weightHmisUpStr     = weightStr + ' * DeepAK8SF_HmisUp'
		weightHmisDownStr   = weightStr + ' * DeepAK8SF_HmisDn'
		weightZeffUpStr     = weightStr + ' * DeepAK8SF_ZeffUp'
		weightZeffDownStr   = weightStr + ' * DeepAK8SF_ZeffDn'
		weightZmisUpStr     = weightStr + ' * DeepAK8SF_ZmisUp'
		weightZmisDownStr   = weightStr + ' * DeepAK8SF_ZmisDn'
		weightWeffUpStr     = weightStr + ' * DeepAK8SF_WeffUp'
		weightWeffDownStr   = weightStr + ' * DeepAK8SF_WeffDn'
		weightWmisUpStr     = weightStr + ' * DeepAK8SF_WmisUp'
		weightWmisDownStr   = weightStr + ' * DeepAK8SF_WmisDn'
		weightBeffUpStr     = weightStr + ' * DeepAK8SF_BeffUp'
		weightBeffDownStr   = weightStr + ' * DeepAK8SF_BeffDn'
		weightBmisUpStr     = weightStr + ' * DeepAK8SF_BmisUp'
		weightBmisDownStr   = weightStr + ' * DeepAK8SF_BmisDn'
		weightJeffUpStr     = weightStr + ' * DeepAK8SF_JeffUp'
		weightJeffDownStr   = weightStr + ' * DeepAK8SF_JeffDn'
		weightJmisUpStr     = weightStr + ' * DeepAK8SF_JmisUp'
		weightJmisDownStr   = weightStr + ' * DeepAK8SF_JmisDn'

	# For N-1 tagging cuts
	pt_var = 'theJetAK8Pt_JetSubCalc_PtOrdered'
	soft_massvar='theJetAK8SoftDropCorr_JetSubCalc_PtOrdered'
	doubleB_var = 'theJetAK8DoubleB_JetSubCalc_PtOrdered'
	tau21var = 'theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered'
	tau32var = 'theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered'
	if 'SoftDropWZNm1' in iPlot: cut+=  ' && ('+tau21var+' < 0.55 && '+pt_var+' > 200)'
	if 'SoftDropHNm1' in iPlot: cut+=  ' && ('+doubleB_var+' > .6 && '+pt_var+' > 300)'
	if 'SoftDropTNm1' in iPlot: cut+=  ' && ('+tau32var+' < 0.65 && '+pt_var+' > 400)'
	if 'Tau21Nm1' in iPlot:  cut += ' && ('+soft_massvar+' > 65 && '+soft_massvar+' < 105 && '+pt_var+' > 200)'
	if 'Tau32Nm1' in iPlot:  cut += ' && ('+soft_massvar+' > 105 && '+soft_massvar+' < 210 && '+pt_var+' > 400)'
	if 'DoubleBNm1' in iPlot: cut += ' && ('+soft_massvar+' > 105 && '+soft_massvar+' < 135 && '+pt_var+' > 300)'

	if iPlot == 'Tp2MDnn' or iPlot == 'DnnTprime':
		if 'notV' in tag: 
			plotTreeName = 'dnn_Tprime'
			xbins = array('d', linspace(float(cutList['dnnCut']),1,51).tolist())
			xaxislabel = ';DNN VLQ score'		
	if iPlot == 'Tp2MST':
		if 'notV' in tag: 
			plotTreeName = 'AK4HTpMETpLepPt'
			xbins = array('d', linspace(0,5000,51).tolist())
			xaxislabel = ';ST [GeV]'

	# Design the EM cuts for categories
	isEMCut=''
	if isEM=='E': isEMCut+=' && isElectron==1'
	elif isEM=='M': isEMCut+=' && isMuon==1'
		
	# Design the tagging cuts for categories
	tagCut = ''
	if isCategorized:
		if tag == 'taggedbWbW': tagCut += ' && taggedBWBW_'+algo+' == 1'
		elif tag == 'taggedtHbW': tagCut += ' && taggedTHBW_'+algo+' == 1'
		elif tag == 'taggedtZbW': tagCut += ' && taggedTZBW_'+algo+' == 1'
		elif tag == 'taggedtHtH': tagCut += ' && taggedTHTH_'+algo+' == 1'
		elif tag == 'taggedtZtH': tagCut += ' && taggedTZTH_'+algo+' == 1'
		elif tag == 'taggedtZtZ': tagCut += ' && taggedTZTZ_'+algo+' == 1'
		elif tag == 'taggedtZHtZH': tagCut += ' && (taggedTZTZ_'+algo+' == 1 || taggedTZTH_'+algo+' == 1 || taggedTHTH_'+algo+' == 1)'
		elif tag == 'taggedtWtW': tagCut += ' && taggedTWTW_'+algo+' == 1'
		elif tag == 'taggedbZtW': tagCut += ' && taggedBZTW_'+algo+' == 1'
		elif tag == 'taggedbHtW': tagCut += ' && taggedBHTW_'+algo+' == 1'

		if 'notV' in tag:
			tagCut += ' && isValid'+whichSig+'DecayMode_'+algo+' == 0'
			
			# signal categories for only hadronic VLQ valid
			if 'tH' in tag: tagCut += ' && (hadronicTprimeJetIDs_'+algo+'[0] == 1 && hadronicTprimeJetIDs_'+algo+'[1] == 2)'
			elif 'tZ' in tag: tagCut += ' && (hadronicTprimeJetIDs_'+algo+'[0] == 1 && hadronicTprimeJetIDs_'+algo+'[1] == 3)'
			elif 'bW' in tag: tagCut += ' && (hadronicTprimeJetIDs_'+algo+'[0] == 4 && hadronicTprimeJetIDs_'+algo+'[1] == 5)'
			elif 'tW' in tag: tagCut += ' && (hadronicBprimeJetIDs_'+algo+'[0] == 1 && hadronicBprimeJetIDs_'+algo+'[1] == 4)'
			elif 'bZ' in tag: tagCut += ' && (hadronicBprimeJetIDs_'+algo+'[0] == 3 && hadronicBprimeJetIDs_'+algo+'[1] == 5)'
			elif 'bH' in tag: tagCut += ' && (hadronicBprimeJetIDs_'+algo+'[0] == 2 && hadronicBprimeJetIDs_'+algo+'[1] == 5)'

			if whichSig == 'TT' and 'tH' not in tag and 'tZ' not in tag and 'bW' not in tag: 
				tagCut += ' && !(hadronicTprimeJetIDs_'+algo+'[0] == 1 && hadronicTprimeJetIDs_'+algo+'[1] == 2)'
				tagCut += ' && !(hadronicTprimeJetIDs_'+algo+'[0] == 1 && hadronicTprimeJetIDs_'+algo+'[1] == 3)'
				tagCut += ' && !(hadronicTprimeJetIDs_'+algo+'[0] == 4 && hadronicTprimeJetIDs_'+algo+'[1] == 5)'

			if whichSig == 'BB' and 'bH' not in tag and 'bZ' not in tag and 'tW' not in tag: 
				tagCut += ' && !(hadronicBprimeJetIDs_'+algo+'[0] == 1 && hadronicBprimeJetIDs_'+algo+'[1] == 4)'
				tagCut += ' && !(hadronicBprimeJetIDs_'+algo+'[0] == 2 && hadronicBprimeJetIDs_'+algo+'[1] == 5)'
				tagCut += ' && !(hadronicBprimeJetIDs_'+algo+'[0] == 3 && hadronicBprimeJetIDs_'+algo+'[1] == 5)'

			# signal categories for basic tag counts
			if '3W' in tag: tagCut += ' && nW_'+algo+' == 3'
			elif '3pW' in tag: tagCut += ' && nW_'+algo+' >= 3'
			elif '2pW' in tag: tagCut += ' && nW_'+algo+' >= 2'
			elif '2W' in tag: tagCut += ' && nW_'+algo+' == 2'
			elif '1pW' in tag: tagCut += ' && nW_'+algo+' >= 1'
			elif '1W' in tag: tagCut += ' && nW_'+algo+' == 1'
			elif '01W' in tag: tagCut += ' && nW_'+algo+' <= 1'
			elif '0W' in tag: tagCut += ' && nW_'+algo+' == 0'
			
			if '0Z' in tag: tagCut += ' && nZ_'+algo+' == 0'
			elif '01Z' in tag: tagCut += ' && nZ_'+algo+' <= 1'
			elif '1Z' in tag: tagCut += ' && nZ_'+algo+' == 1'
			elif '1pZ' in tag: tagCut += ' && nZ_'+algo+' >= 1'
			elif '2pZ' in tag: tagCut += ' && nZ_'+algo+' >= 2'

			if '0H' in tag: tagCut += ' && nH_'+algo+' == 0'
			elif '01H' in tag: tagCut += ' && nH_'+algo+' <= 1'
			elif '1H' in tag: tagCut += ' && nH_'+algo+' == 1'
			elif '1pH' in tag: tagCut += ' && nH_'+algo+' >= 1'
			elif '2pH' in tag: tagCut += ' && nH_'+algo+' >= 2'

			if '0T' in tag: tagCut += ' && nT_'+algo+' == 0'
			elif '01T' in tag: tagCut += ' && nT_'+algo+' <= 1'
			elif '1T' in tag: tagCut += ' && nT_'+algo+' == 1'
			elif '1pT' in tag: tagCut += ' && nT_'+algo+' >= 1'
			elif '2pT' in tag: tagCut += ' && nT_'+algo+' >= 2'
			
			

	fullcut = cut+isEMCut+tagCut

	print 'plotTreeName: '+plotTreeName
	print 'Flavour: '+isEM+' #tag: '+tag+' #algo: '+algo
	print "Weights:",weightStr
	print 'Cuts: '+fullcut

	# Declare histograms
	hists = {}
	hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		#hists[iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#hists[iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'prefireUp_'     +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'prefireUp_'     +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'prefireDown_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'prefireDown_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#hists[iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#hists[iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'TeffUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'TeffUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'TeffDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'TeffDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'TmisUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'TmisUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'TmisDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'TmisDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'HeffUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'HeffUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'HeffDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'HeffDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'HmisUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'HmisUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'HmisDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'HmisDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'ZeffUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'ZeffUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'ZeffDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'ZeffDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'ZmisUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'ZmisUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'ZmisDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'ZmisDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'WeffUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'WeffUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'WeffDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'WeffDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'WmisUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'WmisUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'WmisDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'WmisDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'BeffUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'BeffUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'BeffDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'BeffDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'BmisUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'BmisUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'BmisDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'BmisDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'JeffUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'JeffUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'JeffDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'JeffDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'JmisUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'JmisUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'JmisDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'JmisDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			
		if process+'jerUp' in tTree: 
			hists[iPlot+'jerUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jerUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'jerDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jerDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if process+'jecUp' in tTree:
			hists[iPlot+'jecUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jecUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'jecDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jecDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if process+'btagUp' in tTree: 
			hists[iPlot+'btagUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'btagUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'btagDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'btagDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if process+'mistagUp' in tTree:
			hists[iPlot+'mistagUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'mistagUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'mistagDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'mistagDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)

		if isCategorized:
			hists[iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			#for i in range(100): hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	tTree[process].Draw(plotTreeName+' >> '+iPlot+''+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
	if doAllSys:
		#tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffUpStr+'*('+fullcut+')', 'GOFF')
		#tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process, weightPileupUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process, weightPileupDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'prefireUp_'     +lumiStr+'fb_'+catStr+'_'+process, weightPrefireUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'prefireDown_'   +lumiStr+'fb_'+catStr+'_'+process, weightPrefireDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdUpStr  +'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdDownStr+'*('+fullcut+')', 'GOFF')
		#tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process, weighttopptUpStr+'*('+fullcut+')', 'GOFF')
		#tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process, weighttopptDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightjsfUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightjsfDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'TeffUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightTeffUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'TeffDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightTeffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'TmisUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightTmisUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'TmisDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightTmisDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'HeffUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightHeffUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'HeffDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightHeffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'HmisUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightHmisUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'HmisDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightHmisDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'ZeffUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightZeffUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'ZeffDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightZeffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'ZmisUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightZmisUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'ZmisDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightZmisDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'WeffUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightWeffUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'WeffDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightWeffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'WmisUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightWmisUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'WmisDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightWmisDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'BeffUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightBeffUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'BeffDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightBeffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'BmisUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightBmisUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'BmisDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightBmisDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'JeffUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightJeffUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'JeffDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightJeffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'JmisUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightJmisUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'JmisDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightJmisDownStr+'*('+fullcut+')', 'GOFF')

		if process+'jecUp' in tTree:
			tTree[process+'jecUp'].Draw(plotTreeName   +' >> '+iPlot+'jecUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jecDown'].Draw(plotTreeName +' >> '+iPlot+'jecDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		if process+'jerUp' in tTree:
			tTree[process+'jerUp'].Draw(plotTreeName   +' >> '+iPlot+'jerUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jerDown'].Draw(plotTreeName +' >> '+iPlot+'jerDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		if process+'btagUp' in tTree:
			tTree[process+'btagUp'].Draw(plotTreeName   +' >> '+iPlot+'btagUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'btagDown'].Draw(plotTreeName +' >> '+iPlot+'btagDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		if process+'mistagUp' in tTree:
			tTree[process+'mistagUp'].Draw(plotTreeName   +' >> '+iPlot+'mistagUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'mistagDown'].Draw(plotTreeName +' >> '+iPlot+'mistagDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')

		if isCategorized:
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuRUpStr+'*('+fullcut+')', 'GOFF')
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuRDownStr+'*('+fullcut+')', 'GOFF')
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuFUpStr+'*('+fullcut+')', 'GOFF')
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuFDownStr+'*('+fullcut+')', 'GOFF')
			#for i in range(100): tTree[process].Draw(plotTreeName+' >> '+iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+fullcut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
