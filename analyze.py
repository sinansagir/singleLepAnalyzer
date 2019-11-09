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

def analyze(tTree,process,flv,cutList,doAllSys,doJetRwt,iPlot,plotDetails,category,region,isCategorized):
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
	print "PROCESSING: ", process+flv
	print "/////"*5

	# Define categories
	isEM  = category['isEM']
	nhott = category['nhott']
	nttag = category['nttag']
	nWtag = category['nWtag']
	nbtag = category['nbtag']
	njets = category['njets']
	catStr = 'is'+isEM+'_nHOT'+nhott+'_nT'+nttag+'_nW'+nWtag+'_nB'+nbtag+'_nJ'+njets

	# Define general cuts
	cut  = '((leptonPt_MultiLepCalc > '+str(cutList['elPtCut'])+' && isElectron==1) || (leptonPt_MultiLepCalc > '+str(cutList['muPtCut'])+' && isMuon==1))'
	cut += ' && (corr_met_MultiLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (MT_lepMet > '+str(cutList['mtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[0] > '+str(cutList['jet1PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[1] > '+str(cutList['jet2PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[2] > '+str(cutList['jet3PtCut'])+')'
	cut += ' && (minDR_lepJet > 0.4)'# || ptRel_lepJet > 40)'
	cut += ' && (AK4HT  > '+str(cutList['AK4HTCut'])+')'
	
	if process.startswith('TTJetsSemiLepNjet0'): cut += ' && (isHTgt500Njetge9 == 0)'
	if process.startswith('TTJetsSemiLepNjet9'): cut += ' && (isHTgt500Njetge9 == 1)'

	# Define weights
	TrigEffUp = '1'
	TrigEffDn = '1'
	TrigEff = 'triggerSF'
	cut += ' && DataPastTrigger == 1 && MCPastTrigger == 1'

	jetSFstr='1'
	jetSFstrUp = '1'
	jetSFstrDn = '1'
# 	if (process!='WJetsMG' and 'WJetsMG' in process):
# 		jetSFstr = 'HTSF_Pol'
# 		jetSFstrUp = 'HTSF_PolUp'
# 		jetSFstrDn = 'HTSF_PolDn'
# 		#jetSFstr = str(genHTweight[process])

	weightStr = '1'
	#Update here as needed!!!!!!
	if ('BDT' in plotTreeName) and (process.startswith('4TM') or process.startswith('TTJets')):
		cut += ' && (isTraining == 3)'
		weightStr = '3'
		
	topPt13TeVstr = '1'
	if 'TTJets' in process: topPt13TeVstr = 'topPtWeight13TeV'
	if 'Data' not in process:
		weightStr          += ' * '+jetSFstr+' * '+TrigEff+' * pileupWeight * lepIdSF * EGammaGsfSF * isoSF * L1NonPrefiringProb_CommonCalc * (MCWeight_MultiLepCalc/abs(MCWeight_MultiLepCalc)) * '+str(weight[process])
# 		weightTrigEffUpStr  = weightStr.replace(TrigEff,'('+TrigEff+'+'+TrigEff+'Uncert)')
# 		weightTrigEffDownStr= weightStr.replace(TrigEff,'('+TrigEff+'-'+TrigEff+'Uncert)')
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
		weightIsrUpStr      = 'renormPSWeights[0] * '+weightStr
		weightIsrDownStr    = 'renormPSWeights[2] * '+weightStr
		weightFsrUpStr      = 'renormPSWeights[1] * '+weightStr
		weightFsrDownStr    = 'renormPSWeights[3] * '+weightStr
		weighttopptUpStr    = '('+topPt13TeVstr+') * '+weightStr
		weighttopptDownStr  = '(1/'+topPt13TeVstr+') * '+weightStr
		weightjsfUpStr      = weightStr.replace(jetSFstr,jetSFstrUp)
		weightjsfDownStr    = weightStr.replace(jetSFstr,jetSFstrDn)

	# For N-1 tagging cuts
	sdmassvar='theJetAK8SoftDropCorr_JetSubCalc_PtOrdered'
	tau21var = 'theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered'
	tau32var = 'theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered'
	if 'SoftDropMassNm1W' in iPlot: cut += ' && ('+tau21var+' < 0.45)'
	if 'SoftDropMassNm1t' in iPlot: cut += ' && ('+tau32var+' < 0.80)'
	if 'Tau21Nm1' in iPlot:  cut += ' && ('+sdmassvar+' > 65 && '+sdmassvar+' < 105)'
	if 'Tau32Nm1' in iPlot:  cut += ' && ('+sdmassvar+' > 105 && '+sdmassvar+' < 220)'

	# Design the tagging cuts for categories
	isEMCut=''
	if isEM=='E': isEMCut+=' && isElectron==1'
	elif isEM=='M': isEMCut+=' && isMuon==1'

	nhottLJMETname = 'NresolvedTops1pFake'
	nttagLJMETname = 'NJetsTtagged'
	nWtagLJMETname = 'NJetsWtagged'
	nbtagLJMETname = 'NJetsCSVwithSF_JetSubCalc'
	njetsLJMETname = 'NJets_JetSubCalc'

	nhottCut = ''
	if 'p' in nhott: nhottCut+=' && '+nhottLJMETname+'>='+nhott[:-1]
	else: nhottCut+=' && '+nhottLJMETname+'=='+nhott
	if nhott=='0p': nhottCut=''

	nttagCut = ''
	if 'p' in nttag: nttagCut+=' && '+nttagLJMETname+'>='+nttag[:-1]
	else: nttagCut+=' && '+nttagLJMETname+'=='+nttag
	if nttag=='0p': nttagCut=''

	nWtagCut = ''
	if 'p' in nWtag: nWtagCut+=' && '+nWtagLJMETname+'>='+nWtag[:-1]
	else: nWtagCut+=' && '+nWtagLJMETname+'=='+nWtag
	if nWtag=='0p': nWtagCut=''
			
	nbtagCut = ''
	if 'p' in nbtag: nbtagCut+=' && '+nbtagLJMETname+'>='+nbtag[:-1]
	else: nbtagCut+=' && '+nbtagLJMETname+'=='+nbtag
	
	if nbtag=='0' and 'minMlb' in iPlot: 
		originalLJMETName=plotTreeName
		plotTreeName='minMleppJet'

	njetsCut = ''
	if 'p' in njets: njetsCut+=' && '+njetsLJMETname+'>='+njets[:-1]
	else: njetsCut+=' && '+njetsLJMETname+'=='+njets
	if njets=='0p': njetsCut=''

	fullcut = cut+isEMCut+nhottCut+nttagCut+nWtagCut+nbtagCut+njetsCut
	if 'TTJets' in process and flv!='':
		if flv=='_ttlf': fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==0'
		elif flv=='_ttcc': fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==1'
		elif flv=='_ttbb': fullcut+=' && (genTtbarIdCategory_TTbarMassCalc[0]==2 || genTtbarIdCategory_TTbarMassCalc[0]==3 || genTtbarIdCategory_TTbarMassCalc[0]==4)'
# 		elif flv=='_ttb': fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==2'
# 		elif flv=='_ttbb': fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==3'
# 		elif flv=='_tt2b': fullcut+=' && genTtbarIdCategory_TTbarMassCalc[0]==4'
		
	# replace cuts for shifts
	cut_btagUp = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_bSFup')
	cut_btagDn = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_bSFdn')
	cut_mistagUp = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_lSFup')
	cut_mistagDn = fullcut.replace(nbtagLJMETname,nbtagLJMETname+'_lSFdn')
	
	cut_tau21Up = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[0]')
	cut_tau21Dn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[1]')
	cut_jmsWUp = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[2]')
	cut_jmsWDn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[3]')
	cut_jmrWUp = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[4]')
	cut_jmrWDn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[5]')
	cut_tau21ptUp = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[6]')
	cut_tau21ptDn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[7]')
	
	cut_tau32Up = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[0]')
	cut_tau32Dn = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[1]')
	cut_jmstUp = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[2]')
	cut_jmstDn = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[3]')
	cut_jmrtUp = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[4]')
	cut_jmrtDn = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[5]')

	print 'plotTreeName: '+plotTreeName
	print 'Flavour: '+isEM+' #hott: '+nhott+' #ttags: '+nttag+' #Wtags: '+nWtag+' #btags: '+nbtag+' #jets: '+njets
	print "Weights:",weightStr
	print 'Cuts: '+fullcut

	# Declare histograms
	hists = {}
	if isPlot2D: hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process+flv]  = TH2D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process+flv,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
	else: hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process+flv]  = TH1D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process+flv,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		systList = ['pileup','prefire','muRFcorrd','muR','muF','isr','fsr','toppt','tau32','jmst','jmrt','tau21','jmsW','jmrW','tau21pt','btag','mistag','jec','jer']
		for syst in systList:
			for ud in ['Up','Down']:
				if isPlot2D: hists[iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process+flv] = TH2D(iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process+flv,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
				else: hists[iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process+flv] = TH1D(iPlot+syst+ud+'_'+lumiStr+'fb_'+catStr+'_'+process+flv,xAxisLabel,len(xbins)-1,xbins)
		for i in range(100): 
			if isPlot2D: hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process+flv] = TH2D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process+flv,yAxisLabel+xAxisLabel,len(ybins)-1,ybins,len(xbins)-1,xbins)
			else: hists[iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process+flv] = TH1D(iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process+flv,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	tTree[process].Draw(plotTreeName+' >> '+iPlot+''+'_'+lumiStr+'fb_'+catStr+'_' +process+flv, weightStr+'*('+fullcut+')', 'GOFF')
	if doAllSys:
# 		tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process+flv, weightTrigEffUpStr+'*('+fullcut+')', 'GOFF')
# 		tTree[process].Draw(plotTreeName+' >> '+iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process+flv, weightTrigEffDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupUp_'     +lumiStr+'fb_'+catStr+'_'+process+flv, weightPileupUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'pileupDown_'   +lumiStr+'fb_'+catStr+'_'+process+flv, weightPileupDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'prefireUp_'     +lumiStr+'fb_'+catStr+'_'+process+flv, weightPileupUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'prefireDown_'   +lumiStr+'fb_'+catStr+'_'+process+flv, weightPileupDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdUp_'  +lumiStr+'fb_'+catStr+'_'+process+flv, weightmuRFcorrdUpStr  +'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRFcorrdDown_'+lumiStr+'fb_'+catStr+'_'+process+flv, weightmuRFcorrdDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRUp_'        +lumiStr+'fb_'+catStr+'_'+process+flv, weightmuRUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muRDown_'      +lumiStr+'fb_'+catStr+'_'+process+flv, weightmuRDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFUp_'        +lumiStr+'fb_'+catStr+'_'+process+flv, weightmuFUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'muFDown_'      +lumiStr+'fb_'+catStr+'_'+process+flv, weightmuFDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'isrUp_'      +lumiStr+'fb_'+catStr+'_'+process, weightIsrUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'isrDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightIsrDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'fsrUp_'      +lumiStr+'fb_'+catStr+'_'+process, weightFsrUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'fsrDown_'      +lumiStr+'fb_'+catStr+'_'+process, weightFsrDownStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptUp_'      +lumiStr+'fb_'+catStr+'_'+process+flv, weighttopptUpStr+'*('+fullcut+')', 'GOFF')
		tTree[process].Draw(plotTreeName+' >> '+iPlot+'topptDown_'    +lumiStr+'fb_'+catStr+'_'+process+flv, weighttopptDownStr+'*('+fullcut+')', 'GOFF')
# 		tTree[process].Draw(plotTreeName+' >> '+iPlot+'htUp_'         +lumiStr+'fb_'+catStr+'_'+process+flv, weighthtUpStr+'*('+fullcut+')', 'GOFF')
# 		tTree[process].Draw(plotTreeName+' >> '+iPlot+'htDown_'       +lumiStr+'fb_'+catStr+'_'+process+flv, weighthtDownStr+'*('+fullcut+')', 'GOFF')


		# Change the plot name itself for shifts if needed
		# t-tagging:
		TAU32upName = plotTreeName
		TAU32dnName = plotTreeName
		JMSTupName  = plotTreeName
		JMSTdnName  = plotTreeName
		JMRTupName  = plotTreeName
		JMRTdnName  = plotTreeName
		if 'Ttagged' in TAU32upName or 'Tjet' in TAU32upName or 'TJet' in TAU32upName: 
			TAU32upName = TAU32upName+'_shifts[0]'
			TAU32dnName = TAU32dnName+'_shifts[1]'
			JMSTupName  = JMSTupName+'_shifts[2]'
			JMSTdnName  = JMSTdnName+'_shifts[3]'
			JMRTupName  = JMRTupName+'_shifts[4]'
			JMRTdnName  = JMRTdnName+'_shifts[5]'
		print 'TTAG SHIFT LJMET NAMES:',TAU32upName,TAU32dnName,JMSTupName,JMSTdnName,JMRTupName,JMRTdnName
		tTree[process].Draw(TAU32upName+' >> '+iPlot+'tau32Up_'  +lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_tau32Up+')', 'GOFF')
		tTree[process].Draw(TAU32dnName+' >> '+iPlot+'tau32Down_'+lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_tau32Dn+')', 'GOFF')		
		tTree[process].Draw(JMSTupName+' >> '+iPlot+'jmstUp_'  +lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_jmstUp+')', 'GOFF')
		tTree[process].Draw(JMSTdnName+' >> '+iPlot+'jmstDown_'+lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_jmstDn+')', 'GOFF')		
		tTree[process].Draw(JMRTupName+' >> '+iPlot+'jmrtUp_'  +lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_jmrtUp+')', 'GOFF')
		tTree[process].Draw(JMRTdnName+' >> '+iPlot+'jmrtDown_'+lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_jmrtDn+')', 'GOFF')		

		# W-tagging:
		TAU21upName = plotTreeName
		TAU21dnName = plotTreeName
		JMSWupName  = plotTreeName
		JMSWdnName  = plotTreeName
		JMRWupName  = plotTreeName
		JMRWdnName  = plotTreeName
		TAU21PTupName = plotTreeName
		TAU21PTdnName = plotTreeName
		if 'Wtagged' in TAU21upName or 'Wjet' in TAU21upName or 'WJet' in TAU21upName: 
			TAU21upName = TAU21upName+'_shifts[0]'
			TAU21dnName = TAU21dnName+'_shifts[1]'
			JMSWupName  = JMSWupName+'_shifts[2]'
			JMSWdnName  = JMSWdnName+'_shifts[3]'
			JMRWupName  = JMRWupName+'_shifts[4]'
			JMRWdnName  = JMRWdnName+'_shifts[5]'
			TAU21PTupName = TAU21PTupName+'_shifts[6]'
			TAU21PTdnName = TAU21PTdnName+'_shifts[7]'
		print 'WTAG SHIFT LJMET NAMES:',TAU21upName,TAU21dnName,JMSWupName,JMSWdnName,JMRWupName,JMRWdnName,TAU21PTupName,TAU21PTdnName
		tTree[process].Draw(TAU21upName+' >> '+iPlot+'tau21Up_'  +lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_tau21Up+')', 'GOFF')
		tTree[process].Draw(TAU21dnName+' >> '+iPlot+'tau21Down_'+lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_tau21Dn+')', 'GOFF')		
		tTree[process].Draw(JMSWupName+' >> '+iPlot+'jmsWUp_'  +lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_jmsWUp+')', 'GOFF')
		tTree[process].Draw(JMSWdnName+' >> '+iPlot+'jmsWDown_'+lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_jmsWDn+')', 'GOFF')		
		tTree[process].Draw(JMRWupName+' >> '+iPlot+'jmrWUp_'  +lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_jmrWUp+')', 'GOFF')
		tTree[process].Draw(JMRWdnName+' >> '+iPlot+'jmrWDown_'+lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_jmrWDn+')', 'GOFF')		
		tTree[process].Draw(TAU21upName+' >> '+iPlot+'tau21ptUp_'  +lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_tau21ptUp+')', 'GOFF')
		tTree[process].Draw(TAU21dnName+' >> '+iPlot+'tau21ptDown_'+lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_tau21ptDn+')', 'GOFF')		

		# b-tagging:
		BTAGupName = plotTreeName#.replace('_lepBJets','_bSFup_lepBJets')
		BTAGdnName = plotTreeName#.replace('_lepBJets','_bSFdn_lepBJets')
		MISTAGupName = plotTreeName#.replace('_lepBJets','_lSFup_lepBJets')
		MISTAGdnName = plotTreeName#.replace('_lepBJets','_lSFdn_lepBJets')
		if 'CSVwithSF' in BTAGupName or 'Htag' in BTAGupName or 'MleppB' in BTAGupName or 'BJetLead' in BTAGupName or 'minMlb' in BTAGupName: 
			BTAGupName = BTAGupName+'_bSFup'
			BTAGdnName = BTAGdnName+'_bSFdn'
			MISTAGupName = MISTAGupName+'_lSFup'
			MISTAGdnName = MISTAGdnName+'_lSFdn'
		print 'BTAG SHIFT LJMET NAMES:',BTAGupName,BTAGdnName,MISTAGupName,MISTAGdnName
		tTree[process].Draw(BTAGupName+' >> '+iPlot+'btagUp_'  +lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_btagUp+')', 'GOFF')
		tTree[process].Draw(BTAGdnName+' >> '+iPlot+'btagDown_'+lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_btagDn+')', 'GOFF')
		tTree[process].Draw(MISTAGupName+' >> '+iPlot+'mistagUp_'  +lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_mistagUp+')', 'GOFF')
		tTree[process].Draw(MISTAGdnName+' >> '+iPlot+'mistagDown_'+lumiStr+'fb_'+catStr+'_'+process+flv, weightStr+'*('+cut_mistagDn+')', 'GOFF')

		if tTree[process+'jecUp']:
			print 'Processing JEC ...'
			tTree[process+'jecUp'].Draw(plotTreeName   +' >> '+iPlot+'jecUp_'  +lumiStr+'fb_'+catStr+'_' +process+flv, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jecDown'].Draw(plotTreeName +' >> '+iPlot+'jecDown_'+lumiStr+'fb_'+catStr+'_' +process+flv, weightStr+'*('+fullcut+')', 'GOFF')
		if tTree[process+'jerUp']:
			print 'Processing JER ...'
			tTree[process+'jerUp'].Draw(plotTreeName   +' >> '+iPlot+'jerUp_'  +lumiStr+'fb_'+catStr+'_' +process+flv, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jerDown'].Draw(plotTreeName +' >> '+iPlot+'jerDown_'+lumiStr+'fb_'+catStr+'_' +process+flv, weightStr+'*('+fullcut+')', 'GOFF')
		for i in range(100): 
			print 'Processing PDF',i+1,'/ 100 ...'
			tTree[process].Draw(plotTreeName+' >> '+iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process+flv, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+fullcut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
