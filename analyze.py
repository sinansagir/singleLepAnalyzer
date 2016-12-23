#!/usr/bin/python

from ROOT import TH1D,TH2D,TTree,TFile
from array import array
from weights import *

"""
--This function will make kinematic plots for a given distribution for electron, muon channels and their combination
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

def analyze(tTree,process,cutList,isotrig,doAllSys,doJetRwt,iPlot,plotDetails,category,region,isCategorized):
	print "*****"*20
	print "*****"*20
	print "DISTRIBUTION:", iPlot
	print "            -name in ljmet trees:", plotDetails[0]
	print "            -x-axis label is set to:", plotDetails[2]
	print "            -using the binning as:", plotDetails[1]
	plotTreeName=plotDetails[0]
	xbins=array('d', plotDetails[1])
	xAxisLabel=plotDetails[2]
	isPlot2D = False
	if len(plotDetails)>3: 
		isPlot2D = True
		ybins=array('d', plotDetails[3])
		yAxisLabel=plotDetails[4]
	
	print "/////"*5
	print "PROCESSING: ", process
	print "/////"*5

	# Define categories
	isEM  = category['isEM']
	nttag = category['nttag']
	nWtag = category['nWtag']
	nbtag = category['nbtag']
	njets = category['njets']
	catStr = 'is'+isEM+'_nT'+nttag+'_nW'+nWtag+'_nB'+nbtag+'_nJ'+njets

	# Define general cuts
	cut  = '(leptonPt_singleLepCalc > '+str(cutList['lepPtCut'])+')'
	cut += ' && (corr_met_singleLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[0] > '+str(cutList['jet1PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[1] > '+str(cutList['jet2PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[2] > '+str(cutList['jet3PtCut'])+')'
	cut += ' && (minDR_lepJet > 0.4 || ptRel_lepJet > 40)'

	# Define weights
	TrigEff = 'TrigEffWeight'
	if isotrig == 1:
		cut += ' && DataPastTrigger == 1'# && MCPastTrigger == 1' # no MC HLT except signal
	else:
		#TrigEff = 'TrigEffAltWeight'
		cut += ' && DataPastTriggerAlt == 1'# && MCPastTriggerAlt == 1'

	jetSFstr='1'
	if doJetRwt and ('WJetsMG' in process or 'QCD' in process): jetSFstr= 'JetSF_80X'

	weightStr = '1'
	if doJetRwt and 'TTJets' in process: weightStr += ' * topPtWeight13TeV'
	if 'Data' not in process: 
		weightStr          += ' * '+jetSFstr+' * '+TrigEff+' * pileupWeight * isoSF * lepIdSF * EGammaGsfSF * MuTrkSF * (MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc)) * '+str(weight[process])
		weightTrigEffUpStr  = weightStr.replace(TrigEff,'TrigEffWeightUncert')
		weightTrigEffDownStr= weightStr
		weightPileupUpStr   = weightStr.replace('pileupWeight','pileupWeightUp')
		weightPileupDownStr = weightStr.replace('pileupWeight','pileupWeightDown')
		weightmuRFcorrdUpStr   = 'renormWeights[5] * '+weightStr
		weightmuRFcorrdDownStr = 'renormWeights[3] * '+weightStr
		weightmuRUpStr      = 'renormWeights[4] * '+weightStr
		weightmuRDownStr    = 'renormWeights[2] * '+weightStr
		weightmuFUpStr      = 'renormWeights[1] * '+weightStr
		weightmuFDownStr    = 'renormWeights[0] * '+weightStr
		weighttopptUpStr    = weightStr 
		weighttopptDownStr  = 'topPtWeight * '+weightStr 
		weightjsfUpStr      = weightStr.replace('JetSF_80X','1')
		weightjsfDownStr    = weightStr.replace('JetSF_80X','JetSF_80X*JetSF_80X')
	#weightStr = '1'
	#cut += ' && MCWeight_singleLepCalc < 0'

	# For N-1 tagging cuts
	pruned_massvar = 'theJetAK8PrunedMassWtagUncerts_JetSubCalc_PtOrdered'
	soft_massvar='theJetAK8SoftDropMass_JetSubCalc_PtOrdered'
	tau21var = 'theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered'
	tau32var = 'theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered'
	if 'PrunedNm1' in iPlot: cut += ' && ('+tau21var+' < 0.6)'
	if 'SoftDropMassNm1' in iPlot: cut+=  ' && ('+tau32var+' < 0.69)'
	if 'Tau21Nm1' in iPlot:  cut += ' && ('+pruned_massvar+' > 65 && '+pruned_massvar+' < 105)'
	if 'Tau32Nm1' in iPlot:  cut += ' && ('+soft_massvar+' > 105 && '+ soft_massvar+' < 220)'

	#plot with a specific number of b tags
	if not isCategorized:
		if 'Bjet1' in iPlot or 'Mlb' in iPlot or 'b1' in iPlot: nbtag='1p'
		if 'b2' in iPlot: nbtag='2p'
		if 'Mlj' in iPlot: nbtag='0'

	# Design the tagging cuts for categories
	isEMCut=''
	if isEM=='E': isEMCut+=' && isElectron==1'
	elif isEM=='M': isEMCut+=' && isMuon==1'

	nttagLJMETname = 'NJetsTtagged_0p81'
	nWtagLJMETname = 'NJetsWtagged_0p6'
	nbtagLJMETname = 'NJetsCSV_JetSubCalc'#'NJetsCSVwithSF_JetSubCalc'
	njetsLJMETname = 'NJets_JetSubCalc'
	nttagCut = ''
	if 'p' in nttag: nttagCut+=' && '+nttagLJMETname+'>='+nttag[:-1]
	else: nttagCut+=' && '+nttagLJMETname+'=='+nttag
	if nttag=='0p': nttagCut=''

	nWtagCut = ''
	if 'p' in nWtag: nWtagCut+=' && '+nWtagLJMETname+'>='+nWtag[:-1]
	else: nWtagCut+=' && '+nWtagLJMETname+'=='+nWtag
	if nWtag=='0p': nWtagCut=''
	
# 	nbjCut = ''	
# 	if isCategorized:
# 		nbtagCut = ''
# 		if 'p' in nbtag: nbtagCut+=' && '+nbtagLJMETname+'>='+nbtag[:-1]
# 		else: nbtagCut+=' && '+nbtagLJMETname+'=='+nbtag
# 	
# 		if nbtag=='0' and iPlot=='minMlb': 
# 			originalLJMETName=plotTreeName
# 			plotTreeName='minMleppJet'
# 
# 		njetsCut = ''
# 		if 'p' in njets: njetsCut+=' && '+njetsLJMETname+'>='+njets[:-1]
# 		else: njetsCut+=' && '+njetsLJMETname+'=='+njets
# 		if njets=='0p': njetsCut=''
# 		
# 		nbjCut += nbtagCut+njetsCut
# 		
# 	else:
# 		if 'CR' in region:
# 			nbjCut+=' && ( ('+nbtagLJMETname+'==1 && '+njetsLJMETname+'>=3)'
# 			nbjCut+=  ' || ('+nbtagLJMETname+'>=2 && '+njetsLJMETname+'==3)'
# 			nbjCut+=  ' || ('+nbtagLJMETname+'==2 && '+njetsLJMETname+'==4))'
# 		if 'SR' in region:
# 			nbjCut+=' && ( ('+nbtagLJMETname+'==2 && '+njetsLJMETname+'>=5)'
# 			nbjCut+=  ' || ('+nbtagLJMETname+'==3 && '+njetsLJMETname+'>=5)'
# 			nbjCut+=  ' || ('+nbtagLJMETname+'>=4 && '+njetsLJMETname+'>=5)'
# 			nbjCut+=  ' || ('+nbtagLJMETname+'>=3 && '+njetsLJMETname+'==4))'
	nbjCut = ''	
	nbtagCut = ''
	if 'p' in nbtag: nbtagCut+=' && '+nbtagLJMETname+'>='+nbtag[:-1]
	else: nbtagCut+=' && '+nbtagLJMETname+'=='+nbtag

	if nbtag=='0' and iPlot=='minMlb': 
		originalLJMETName=plotTreeName
		plotTreeName='minMleppJet'

	njetsCut = ''
	if 'p' in njets: njetsCut+=' && '+njetsLJMETname+'>='+njets[:-1]
	else: njetsCut+=' && '+njetsLJMETname+'=='+njets
	if njets=='0p': njetsCut=''
	
	nbjCut += nbtagCut+njetsCut
	
	fullcut = cut+isEMCut+nttagCut+nWtagCut+nbjCut
	if 'WJets' in process: 
		if process.endswith('_bflv'): fullcut+=' && NbHFlav>0'
		elif process.endswith('_cflv'): fullcut+=' && NbHFlav==0 && NcHFlav>0'
		elif process.endswith('_lflv'): fullcut+=' && NbHFlav==0 && NcHFlav==0'
	elif 'TTJets' in process: 
		if process.endswith('_bbflv'): fullcut+=' && NbHFlav>=3'
		elif process.endswith('_llflv'): fullcut+=' && NbHFlav<3'

	# replace cuts for shifts
	cut_btagUp = fullcut#.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[0]')
	cut_btagDn = fullcut#.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[1]')
	cut_mistagUp = fullcut#.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[2]')
	cut_mistagDn = fullcut#.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[3]')
	
	cut_tauUp = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[0]')
	cut_tauDn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[1]')
	
	cut_topsfUp = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[0]')
	cut_topsfDn = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[1]')

	print 'plotTreeName: '+plotTreeName
	print 'Flavour: '+isEM+' #ttags: '+nttag+' #Wtags: '+nWtag+' #btags: '+nbtag+' #jets: '+njets
	print "Weights:",weightStr
	print 'Cuts: '+fullcut

	# Declare histograms
	hists = {}
	if isPlot2D: hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH2D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
	else: hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		systList = ['trigeff','pileup','muRFcorrd','muR','muF','toppt','btag','mistag','jsf','jer','jec']
		for syst in systList:
			for ud in ['Up','Down']:
				if isPlot2D: hists[iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH2D(iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
				else: hists[iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		for i in range(100): 
			if isPlot2D: hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH2D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
			else: hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	fullcutShape = fullcut
	if iPlot=='BDT' and 'Data' not in process and 'Q2' not in process: fullcut+=' && isTraining==1'
	tTree[process].Draw(plotTreeName+' >> '+iPlot+''+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
# 	if 'TTJets' in process: 
# 		if process.endswith('_bbflv'): hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process].Scale(1.71)
# 		elif process.endswith('_llflv'): hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process].Scale((1.-1.71*hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process].Integral())/(1.-hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process].Integral()))
	if doAllSys:
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process, weightPileupUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process, weightPileupDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdUpStr  +'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuRUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuRDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuFDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process, weighttopptUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process, weighttopptDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightjsfUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightjsfDownStr+'*('+fullcut+')', 'GOFF')

		# Change the plot name itself for shifts if needed
		BTAGupName = plotTreeName.replace('_lepBJets','_bSFup_lepBJets')
		BTAGdnName = plotTreeName.replace('_lepBJets','_bSFdn_lepBJets')
		MISTAGupName = plotTreeName.replace('_lepBJets','_lSFup_lepBJets')
		MISTAGdnName = plotTreeName.replace('_lepBJets','_lSFdn_lepBJets')
		if 'CSVwithSF' in BTAGupName or 'Htag' in BTAGupName or 'MleppB' in BTAGupName or 'BJetLead' in BTAGupName or 'minMlb' in BTAGupName: 
			BTAGupName = BTAGupName+'_shifts[0]'
			BTAGdnName = BTAGdnName+'_shifts[1]'
			MISTAGupName = MISTAGupName+'_shifts[2]'
			MISTAGdnName = MISTAGdnName+'_shifts[3]'
		print 'BTAG SHIFT LJMET NAMES',BTAGupName,BTAGdnName,MISTAGupName,MISTAGdnName
		tTree[process].Draw(BTAGupName+' >> '+iPlot+'btagUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_btagUp+')', 'GOFF')
		tTree[process].Draw(BTAGdnName+' >> '+iPlot+'btagDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_btagDn+')', 'GOFF')
		tTree[process].Draw(MISTAGupName+' >> '+iPlot+'mistagUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_mistagUp+')', 'GOFF')
		tTree[process].Draw(MISTAGdnName+' >> '+iPlot+'mistagDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_mistagDn+')', 'GOFF')

		print 'Cuts (JECR shape): '+fullcutShape
		if tTree[process+'jecUp']:
			tTree[process+'jecUp'].Draw(plotTreeName   +' >> '+iPlot+'jecUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcutShape+')', 'GOFF')
			tTree[process+'jecDown'].Draw(plotTreeName +' >> '+iPlot+'jecDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcutShape+')', 'GOFF')
		if tTree[process+'jerUp']:
			tTree[process+'jerUp'].Draw(plotTreeName   +' >> '+iPlot+'jerUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcutShape+')', 'GOFF')
			tTree[process+'jerDown'].Draw(plotTreeName +' >> '+iPlot+'jerDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcutShape+')', 'GOFF')
		for i in range(100): tTree[process].Draw(plotTreeName+' >> '+iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+fullcut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
