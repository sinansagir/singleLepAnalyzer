#!/usr/bin/python

from ROOT import TH1D,TTree,TFile
from array import array
from weights import *

"""
--This function will make kinematic plots for a given distribution for electron, muon channels and their combination
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

def analyze(tTree,process,cutList,isotrig,doAllSys,doJetRwt,iPlot,plotDetails,category,region):
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
	isCategorized = not (category['nttag']=='0p' and category['nWtag']=='0p' and category['nbtag']=='0p')
	isEM  = category['isEM']
	nttag = category['nttag']
	nWtag = category['nWtag']
	nbtag = category['nbtag']
	catStr = 'is'+isEM
	if isCategorized: catStr += '_nT'+nttag+'_nW'+nWtag+'_nB'+nbtag

	# Define general cuts
	cut  = '(leptonPt_singleLepCalc > '+str(cutList['lepPtCut'])+')'
	cut += ' && (corr_met_singleLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[0] > '+str(cutList['jet1PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[1] > '+str(cutList['jet2PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[2] > '+str(cutList['jet3PtCut'])+')'
	cut += ' && (minDR_lepJet > 0.4 || ptRel_lepJet > 40)'
	cut += ' && (NJets_JetSubCalc >= '+str(cutList['njetsCut'])+')'
	cut += ' && (DataPastTrigger == 1 && MCPastTrigger == 1)' #standard triggers, check trigger weight branch name!
	if 'CR' in region:
		#cut += ' && (deltaR_lepJets[1] >= 0.4 && deltaR_lepJets[1] <= '+str(cutList['drCut'])+')'
		cut += ' && (deltaR_lepJets[1] <= '+str(cutList['drCut'])+')'
		if 'TT' in region: cut += ' && (NJetsCSVwithSF_JetSubCalc >= '+str(cutList['nbjetsCut'])+')'
		elif 'WJ' in region: cut += ' && (NJetsCSVwithSF_JetSubCalc == '+str(cutList['nbjetsCut'])+')'
	else: # 'PS' or 'SR'
		cut += ' && (deltaR_lepJets[1] > '+str(cutList['drCut'])+')'
		cut += ' && (NJetsCSVwithSF_JetSubCalc >= '+str(cutList['nbjetsCut'])+')'

	# Define weights
	jetSFstr   = '1'
	jetSFupstr = '1'
	jetSFdnstr = '1'
	if doJetRwt and ('WJetsMG' in process or 'QCD' in process):
		jetSFstr   = 'JetSF_pTNbwflat'
		jetSFupstr = 'JetSFupwide_pTNbwflat'
		jetSFdnstr = 'JetSFdnwide_pTNbwflat'

	if 'Data' in process: 
		weightStr           = '1'
		weightPileupUpStr   = '1'
		weightPileupDownStr = '1'
		weightmuRFcorrdUpStr   = '1'
		weightmuRFcorrdDownStr = '1'
		weightmuRUpStr   = '1'
		weightmuRDownStr = '1'
		weightmuFUpStr   = '1'
		weightmuFDownStr = '1'
		weighttopptUpStr    = '1'
		weighttopptDownStr  = '1'
		weightjsfUpStr    = '1'
		weightjsfDownStr  = '1'
	else: 
		weightStr           = jetSFstr+' * TrigEffWeight * pileupWeight * isoSF * lepIdSF * (MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc)) * '+str(weight[process])
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
		weightjsfUpStr      = weightStr.replace(jetSFstr,jetSFupstr)
		weightjsfDownStr    = weightStr.replace(jetSFstr,jetSFdnstr)

	print "Applying Weights:",weightStr

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
		if 'Bjet1' in iPlot or 'Mlb' in iPlot or 'b1' in iPlot: cut += ' && (NJetsCSVwithSF_JetSubCalc > 0)'
		if 'b2' in iPlot: cut += ' && (NJetsCSVwithSF_JetSubCalc > 1)'
		if 'Mlj' in iPlot: cut += ' && (NJetsCSVwithSF_JetSubCalc == 0)'
		origname = plotTreeName
		if 'Data' in process and iPlot=='PrunedSmeared': plotTreeName = 'theJetAK8PrunedMass_JetSubCalc_PtOrdered'
		if origname != plotTreeName: print 'NEW LJMET NAME:',plotTreeName
		
	# Design the tagging cuts for categories
	isEMCut=''
	if isEM=='E': isEMCut+=' && isElectron==1'
	elif isEM=='M': isEMCut+=' && isMuon==1'

	nttagLJMETname = 'NJetsToptagged_tau0p69_SF' #shifts will be: nttagLJMETname+'up/dn'
	nWtagLJMETname = 'NJetsWtagged_0p6' #shifts will be: nWtagLJMETname+'_shifts[0/1/2/3/4/5]'
	nbtagLJMETname = 'NJetsCSVwithSF_JetSubCalc' #shifts will be: nbtagLJMETname+'_shifts[0/1/2/3]'
	nttagCut = ''
	nWtagCut = ''
	nbtagCut = ''
	if isCategorized:
		nttagCut=''
		if 'p' in nttag: nttagCut+=' && '+nttagLJMETname+'>='+nttag[:-1]
		else: nttagCut+=' && '+nttagLJMETname+'=='+nttag
		if nttag=='0p': nttagCut=''
	
		nWtagCut=''
		if 'p' in nWtag: nWtagCut+=' && '+nWtagLJMETname+'>='+nWtag[:-1]
		else: nWtagCut+=' && '+nWtagLJMETname+'=='+nWtag
		if nWtag=='0p': nWtagCut=''
		
		nbtagCut=''
		if 'p' in nbtag: nbtagCut+=' && '+nbtagLJMETname+'>='+nbtag[:-1]
		else: nbtagCut+=' && '+nbtagLJMETname+'=='+nbtag
		
		if nbtag=='0' and iPlot=='minMlb': 
			origname = plotTreeName
			plotTreeName='minMleppJet'
			if origname != plotTreeName: print 'NEW LJMET NAME:',plotTreeName
	
	fullcut = cut+isEMCut+nttagCut+nWtagCut+nbtagCut

	# replace cuts for shifts
	cut_btagUp = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[0]')
	cut_btagDn = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[1]')
	cut_mistagUp = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[2]')
	cut_mistagDn = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[3]')
	
	cut_jmrUp = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[0]')
	cut_jmrDn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[1]')
	cut_jmsUp = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[2]')
	cut_jmsDn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[3]')
	cut_tauUp = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[4]')
	cut_tauDn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[5]')
	
	cut_topsfUp = fullcut.replace(nttagLJMETname,nttagLJMETname+'up')
	cut_topsfDn = fullcut.replace(nttagLJMETname,nttagLJMETname+'dn')

	print 'Flavour: '+isEM+' #ttags: '+nttag+' #Wtags: '+nWtag+' #btags: '+nbtag
	print 'plotTreeName: '+plotTreeName
	print 'Cuts: '+fullcut

	# Declare histograms
	hists = {}
	hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		hists[iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'btagUp_'       +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagUp_'       +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'btagDown_'     +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'btagDown_'     +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'mistagUp_'     +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'mistagUp_'     +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'mistagDown_'   +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'mistagDown_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jmrUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jmrUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jmrDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jmrDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jmsUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jmsUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jmsDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jmsDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'tau21Up_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'tau21Up_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'tau21Down_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'tau21Down_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jsfUp_'        +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'jsfDown_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'topsfUp_'      +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topsfUp_'      +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'topsfDown_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'topsfDown_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			
		if tTree[process+'jerUp']: 
			hists[iPlot+'jerUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jerUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'jerDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jerDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if tTree[process+'jecUp']:
			hists[iPlot+'jecUp_'   +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jecUp_'   +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[iPlot+'jecDown_' +lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'jecDown_' +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		for i in range(100): hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	tTree[process].Draw(plotTreeName+' >> '+iPlot+''+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
	if doAllSys:
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
		TTAGupName= plotTreeName
		TTAGdnName= plotTreeName
		if 'Ttagged' in TTAGupName or 'Tjet' in TTAGupName or 'TJet' in TTAGupName: 
			TTAGupName = TTAGupName+'_shifts[0]'
			TTAGdnName = TTAGdnName+'_shifts[1]'
		print 'TTAG SHIFT LJMET NAMES',TTAGupName,TTAGdnName
		tTree[process].Draw(TTAGupName+' >> '+iPlot+'topsfUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_topsfUp+')', 'GOFF')
		tTree[process].Draw(TTAGdnName+' >> '+iPlot+'topsfDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_topsfDn+')', 'GOFF')

		JMRupName = plotTreeName
		JMRdnName = plotTreeName
		JMSupName = plotTreeName
		JMSdnName = plotTreeName
		TAUupName = plotTreeName
		TAUdnName = plotTreeName
		if 'Wtagged' in JMRupName or 'Wjet' in JMRupName or 'WJet' in JMRupName: 
			JMRupName = JMRupName+'_shifts[0]'
			JMRdnName = JMRdnName+'_shifts[1]'
			JMSupName = JMSupName+'_shifts[2]'
			JMSdnName = JMSdnName+'_shifts[3]'
			TAUupName = TAUupName+'_shifts[4]'
			TAUdnName = TAUdnName+'_shifts[5]'
		print 'WTAG SHIFT LJMET NAMES',JMRupName,JMRdnName,JMSupName,JMSdnName,TAUupName,TAUdnName
		tTree[process].Draw(JMRupName+' >> '+iPlot+'jmrUp_'    +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_jmrUp+')', 'GOFF')
		tTree[process].Draw(JMRdnName+' >> '+iPlot+'jmrDown_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_jmrDn+')', 'GOFF')
		tTree[process].Draw(JMSupName+' >> '+iPlot+'jmsUp_'    +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_jmsUp+')', 'GOFF')
		tTree[process].Draw(JMSdnName+' >> '+iPlot+'jmsDown_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_jmsDn+')', 'GOFF')
		tTree[process].Draw(TAUupName+' >> '+iPlot+'tau21Up_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_tauUp+')', 'GOFF')
		tTree[process].Draw(TAUdnName+' >> '+iPlot+'tau21Down_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_tauDn+')', 'GOFF')		

		BTAGupName = plotTreeName.replace('_lepBJets','_bSFup_lepBJets')
		BTAGdnName = plotTreeName.replace('_lepBJets','_bSFdn_lepBJets')
		MISTAGupName = plotTreeName.replace('_lepBJets','_lSFup_lepBJets')
		MISTAGdnName = plotTreeName.replace('_lepBJets','_lSFdn_lepBJets')
		if 'CSVwithSF' in plotTreeName or 'Htag' in plotTreeName or 'MleppB' in plotTreeName or 'BJetLead' in plotTreeName or 'minMlb' in plotTreeName: 
			BTAGupName = BTAGupName+'_shifts[0]'
			BTAGdnName = BTAGdnName+'_shifts[1]'
			MISTAGupName = MISTAGupName+'_shifts[2]'
			MISTAGdnName = MISTAGdnName+'_shifts[3]'
		print 'BTAG SHIFT LJMET NAMES',BTAGupName,BTAGdnName,MISTAGupName,MISTAGdnName
		tTree[process].Draw(BTAGupName+' >> '+iPlot+'btagUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_btagUp+')', 'GOFF')
		tTree[process].Draw(BTAGdnName+' >> '+iPlot+'btagDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_btagDn+')', 'GOFF')
		tTree[process].Draw(MISTAGupName+' >> '+iPlot+'mistagUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_mistagUp+')', 'GOFF')
		tTree[process].Draw(MISTAGdnName+' >> '+iPlot+'mistagDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_mistagDn+')', 'GOFF')

		if tTree[process+'jecUp']:
			tTree[process+'jecUp'].Draw(plotTreeName   +' >> '+iPlot+'jecUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jecDown'].Draw(plotTreeName +' >> '+iPlot+'jecDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		if tTree[process+'jerUp']:
			tTree[process+'jerUp'].Draw(plotTreeName   +' >> '+iPlot+'jerUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jerDown'].Draw(plotTreeName +' >> '+iPlot+'jerDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		for i in range(100): tTree[process].Draw(plotTreeName+' >> '+iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+fullcut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
