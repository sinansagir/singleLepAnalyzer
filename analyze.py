#!/usr/bin/python

from ROOT import TH1D,TH2D,TTree,TFile
from array import array
from weights import *
from utils import *

"""
--This function will make kinematic plots for a given distribution for electron, muon channels and their combination
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

def analyze(tTree,tTreePkey,process,cutList,doAllSys,doJetRwt,iPlot,plotDetails,category,region,isCategorized):
	print "*****"*20
	print "*****"*20
	plotTreeName=plotDetails[0]
	xbins=array('d', plotDetails[1])
	xAxisLabel=plotDetails[2]
	isPlot2D = False
	if len(plotDetails)==4: 
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
	
	if iPlot.endswith('pBDT') and isSR(njets,nbtag):# if the category is an SR, set the template to BDT:
		plotTreeName=plotDetails[3]
		xbins=array('d', plotDetails[4])
		xAxisLabel=plotDetails[5]
	print "DISTRIBUTION:", iPlot
	print "            -name in ljmet trees:", plotTreeName
	print "            -x-axis label is set to:", xAxisLabel
	print "            -using the binning as:", xbins
	
	ljmetCalc = 'singleLepCalc' #JetSubCalc/singleLepCalc switch

	# Define general cuts
	#cut  = '(leptonPt_singleLepCalc > '+str(cutList['lepPtCut'])+')'
	cut  = '((leptonPt_singleLepCalc > 35 && isElectron) || (leptonPt_singleLepCalc > 30 && isMuon))'
	cut += ' && (corr_met_singleLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (AK4JetPt_'+ljmetCalc+'_PtOrdered[0] > '+str(cutList['jet1PtCut'])+')'
	cut += ' && (AK4JetPt_'+ljmetCalc+'_PtOrdered[1] > '+str(cutList['jet2PtCut'])+')'
	#cut += ' && (minDR_lepJet > 0.4 || ptRel_lepJet > 40)'#2D Cut
	cut += ' && (minDR_lepJet > 0.4)'
	cut += ' && (isTau_singleLepCalc == 0)'
	if isEM=='E' and isCR(njets,nbtag): cut += ' && (min_deltaPhi_METjets>0.05)'
	cut += ' && DataPastTriggerLepTight == 1 && MCPastTriggerLepTight == 1'
	# Define weights
	TrigEff = 'TrigEffWeight'

	jetSFstr = '1'
	#if doJetRwt and ('WJetsMG' in process or 'QCD' in process) and 'JSF' in process: jetSFstr= 'JetSF_80X'

	weightStr = '1'

	#Update here depending on the training type!!!!!!
	trainingSamples=[]#'Tt','Tbt','Ts','TtW','TbtW','TTWl','TTWq','TTZl','TTZq']
	if ('BDT' in plotTreeName) and (process in trainingSamples or process.startswith('Hptb')):
		cut += ' && (isTraining == 0)'
		weightStr = '2'

	HTweightStr = '1'
	HTweightStrUp = '1'
	HTweightStrDn = '1'
	if 'WJetsHT' in process:
		#HTweightStr = str(genHTweight[process])
		HTweightStr   = 'HTSF_Pol'
		HTweightStrUp = 'HTSF_PolUp'
		HTweightStrDn = 'HTSF_PolDn'
		#HTweightStr   = 'HTSF_Exp'
		#HTweightStrUp = 'HTSF_ExpUp'
		#HTweightStrDn = 'HTSF_ExpDn'
	
	topPt13TeVstr = '1'
	if 'TTJets' in process: topPt13TeVstr = 'topPtWeight13TeV'
# 	topPt13TeVstr = '1'
# 	HTweightStr   = '1'
# 	HTweightStrUp = '1'
# 	HTweightStrDn = '1'
	if 'Data' not in process:
		weightStr          += ' * '+topPt13TeVstr+' * '+HTweightStr+' * '+jetSFstr+' * '+TrigEff+' * pileupWeight * isoSF * lepIdSF * EGammaGsfSF * MuTrkSF * (MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc)) * '+str(weight[process])
		weightTrigEffUpStr  = weightStr.replace(TrigEff,'('+TrigEff+'+'+TrigEff+'Uncert)')
		weightTrigEffDownStr= weightStr.replace(TrigEff,'('+TrigEff+'-'+TrigEff+'Uncert)')
		weightPileupUpStr   = weightStr.replace('pileupWeight','pileupWeightUp')
		weightPileupDownStr = weightStr.replace('pileupWeight','pileupWeightDown')
		weightmuRFcorrdUpStr   = 'renormWeights[5] * '+weightStr
		weightmuRFcorrdDownStr = 'renormWeights[3] * '+weightStr
		weightmuRUpStr      = 'renormWeights[4] * '+weightStr
		weightmuRDownStr    = 'renormWeights[2] * '+weightStr
		weightmuFUpStr      = 'renormWeights[1] * '+weightStr
		weightmuFDownStr    = 'renormWeights[0] * '+weightStr
		weighttopptUpStr    = weightStr.replace(topPt13TeVstr,'1')
		weighttopptDownStr  = weightStr
		weighthtUpStr       = weightStr.replace(HTweightStr,HTweightStrUp)
		weighthtDownStr     = weightStr.replace(HTweightStr,HTweightStrDn)
		#weightjsfUpStr      = weightStr.replace(jetSFstr,'1')
		#weightjsfDownStr    = weightStr.replace(jetSFstr,'('jetSFstr+'*'+jetSFstr+')')
	#weightStr = '1'
	#cut += ' && MCWeight_singleLepCalc < 0'

	# Design the tagging cuts for categories
	isEMCut=''
	if isEM=='E': isEMCut+=' && isElectron==1'
	elif isEM=='M': isEMCut+=' && isMuon==1'

	nbtagLJMETname = 'NJetsCSVwithSF_'+ljmetCalc
	njetsLJMETname = 'NJets_'+ljmetCalc
	nttagCut = ''
	nWtagCut = ''
	
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

	njetsCut = ''
	if 'p' in njets: njetsCut+=' && '+njetsLJMETname+'>='+njets[:-1]
	else: njetsCut+=' && '+njetsLJMETname+'=='+njets
	if njets=='0p': njetsCut=''
	
	nbjCut += nbtagCut+njetsCut
	
	fullcut = cut+isEMCut+nttagCut+nWtagCut+nbjCut
	if 'TTJets' in process:
		if process.endswith('_tt2b'): fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==4'
		elif process.endswith('_ttbb'): fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==3'
		elif process.endswith('_ttb'): fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==2'
		elif process.endswith('_ttcc'): fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==1'
		elif process.endswith('_ttlf'): fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==0'

	# replace cuts for shifts
	cut_btagUp = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[0]')
	cut_btagDn = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[1]')
	cut_mistagUp = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[2]')
	cut_mistagDn = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[3]')

	print 'plotTreeName: '+plotTreeName
	print 'Flavour: '+isEM+' #ttags: '+nttag+' #Wtags: '+nWtag+' #btags: '+nbtag+' #jets: '+njets
	print "Weights:",weightStr
	print "Cuts:",fullcut


	# Declare histograms
	hists = {}
	if isPlot2D: hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH2D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
	else: hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		systList = ['trigeff','pileup','muRFcorrd','muR','muF','toppt','btag','mistag','jec','jer','ht']
		for syst in systList:
			for ud in ['Up','Down']:
				if isPlot2D: hists[iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH2D(iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
				else: hists[iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
# 		for i in range(100): 
# 			if isPlot2D: hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH2D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
# 			else: hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+''+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
	if doAllSys:
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process, weightTrigEffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process, weightPileupUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process, weightPileupDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdUpStr  +'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process, weightmuRFcorrdDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuRUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuRDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process, weightmuFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightmuFDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process, weighttopptUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process, weighttopptDownStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'htUp_'         +lumiStr+'fb_'+catStr+'_'+process, weighthtUpStr+'*('+fullcut+')', 'GOFF')
		tTree[tTreePkey].Draw(plotTreeName+' >> '+iPlot+'htDown_'       +lumiStr+'fb_'+catStr+'_'+process, weighthtDownStr+'*('+fullcut+')', 'GOFF')

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
		tTree[tTreePkey].Draw(BTAGupName+' >> '+iPlot+'btagUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_btagUp+')', 'GOFF')
		tTree[tTreePkey].Draw(BTAGdnName+' >> '+iPlot+'btagDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_btagDn+')', 'GOFF')
		tTree[tTreePkey].Draw(MISTAGupName+' >> '+iPlot+'mistagUp_'  +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_mistagUp+')', 'GOFF')
		tTree[tTreePkey].Draw(MISTAGdnName+' >> '+iPlot+'mistagDown_'+lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_mistagDn+')', 'GOFF')

		if tTree[tTreePkey+'jecUp']:
			tTree[tTreePkey+'jecUp'].Draw(plotTreeName   +' >> '+iPlot+'jecUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[tTreePkey+'jecDown'].Draw(plotTreeName +' >> '+iPlot+'jecDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		if tTree[tTreePkey+'jerUp']:
			tTree[tTreePkey+'jerUp'].Draw(plotTreeName   +' >> '+iPlot+'jerUp_'  +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[tTreePkey+'jerDown'].Draw(plotTreeName +' >> '+iPlot+'jerDown_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		#for i in range(100): tTree[process].Draw(plotTreeName+' >> '+iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+fullcut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
