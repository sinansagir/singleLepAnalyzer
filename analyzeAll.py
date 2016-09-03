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
	isCategorized = False
	try: isEM = category[0]
	except: isEM = ''
	nttag = ''
	nWtag = ''
	nbtag = ''
	catStr = isEM
	if len(category) > 1:
		isCategorized = True
		isEM  = category['isEM']
		nttag = category['nttag']
		nWtag = category['nWtag']
		nbtag = category['nbtag']
		catStr = 'is'+isEM+'_nT'+nttag+'_nW'+nWtag+'_nB'+nbtag

	# Define general cuts
	cut = ''
	cut += '(leptonPt_singleLepCalc > '+str(cutList['lepPtCut'])+')'
	cut += ' && (corr_met_singleLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[0] > '+str(cutList['jet1PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[1] > '+str(cutList['jet2PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[2] > '+str(cutList['jet3PtCut'])+')'
	cut += ' && (minDR_lepJet > 0.4 || ptRel_lepJet > 40)'
	cut += ' && (NJets_JetSubCalc >= '+str(cutList['njetsCut'])+')'
	if 'CR' in region:
		cut += ' && (deltaR_lepJets[1] >= 0.4 && deltaR_lepJets[1] < '+str(cutList['drCut'])+')'
		if 'TT' in region: cut += ' && (NJetsCSVwithSF_JetSubCalc >= '+str(cutList['nbjetsCut'])+')'
		elif 'WJ' in region: cut += ' && (NJetsCSVwithSF_JetSubCalc == '+str(cutList['nbjetsCut'])+')'
	else: # 'PS' or 'SR'
		cut += ' && (deltaR_lepJets[1] >= '+str(cutList['drCut'])+')'
		cut += ' && (NJetsCSVwithSF_JetSubCalc >= '+str(cutList['nbjetsCut'])+')'


	# Define weights
	TrigEff = 'TrigEffWeight'
	if isotrig == 1:
		cut += ' && DataPastTrigger == 1' # no MC HLT except signal  && MCPastTrigger == 1'
	else:
		TrigEff = 'TrigEffAltWeight'
		cut += ' && DataPastTriggerAlt == 1' #&& MCPastTriggerAlt == 1'

	jetSFstr='1'
	if doJetRwt and ('WJetsMG' in process or 'QCD' in process):
		jetSFstr= 'JetSF_80X'

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
		weightStr           =  jetSFstr+ ' * ' + TrigEff+' * pileupWeight * isoSF * lepIdSF * EGammaGsfSF * MuTrkSF * (MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc)) * '+str(weight[process])
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

	print "Applying Weights:",weightStr

	# For N-1 tagging cuts
	pruned_massvar = 'theJetAK8PrunedMassWtagUncerts_JetSubCalc_PtOrdered'
	soft_massvar='theJetAK8SoftDropMass_JetSubCalc_PtOrdered'
	wtagvar = 'NJetsWtagged_0p6'
	if 'PrunedNm1' in iPlot: cut += ' && (theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered < 0.6)'
	if 'SoftDropMassNm1' in iPlot: cut+=  ' && (theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered < 0.81)'
	if 'Tau21Nm1' in iPlot:  cut += ' && ('+pruned_massvar+' > 65 && '+pruned_massvar+' < 105)'
	if 'Tau32Nm1' in iPlot:  cut += ' && ('+soft_massvar+' > 105 && '+ soft_massvar+' < 220)'

	#plot with a specific number of b tags
	if not isCategorized:
		if 'Bjet1' in iPlot or 'Mlb' in iPlot or 'b1' in iPlot:
			cut += ' && (NJetsCSVwithSF_JetSubCalc > 0)'
		if 'b2' in iPlot: cut += ' && (NJetsCSVwithSF_JetSubCalc > 1)'
		if 'Mlj' in iPlot: cut += ' && (NJetsCSVwithSF_JetSubCalc == 0)'

	# Design the tagging cuts for categories
	isEMCut=''
	if isEM=='E': isEMCut+=' && isElectron==1'
	elif isEM=='M': isEMCut+=' && isMuon==1'

	nttagLJMETname = 'NJetsTtagged_0p81'
	nWtagLJMETname = 'NJetsWtagged_0p6'
	nbtagLJMETname = 'NJetsCSVwithSF_JetSubCalc'
	nttagCut = ''
	nWtagCut = ''
	nbtagCut = ''
	if isCategorized:
		nttagCut=''
		if 'p' in nttag: nttagCut+=' && '+nttagLJMETname+'>='+nttag[:-1]
		else: nttagCut+=' && '+nttagLJMETname+'=='+nttag
		if nttag=='0p': nttagCut=''
	
		nWtagCut=''
		if '0p' in nWtag: nWtagCut += ' && (('+nWtagLJMETname+' > 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut'])+') || ('+nWtagLJMETname+' == 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut']+1)+'))'
		elif 'p' in nWtag: nWtagCut+=' && '+nWtagLJMETname+'>='+nWtag[:-1]
		else: nWtagCut+=' && '+nWtagLJMETname+'=='+nWtag +' && NJets_JetSubCalc >=' +str(cutList['njetsCut']+1)
		
		nbtagCut=''
		if 'p' in nbtag: nbtagCut+=' && NJetsCSVwithSF_JetSubCalc>='+nbtag[:-1]
		else: nbtagCut+=' && NJetsCSVwithSF_JetSubCalc=='+nbtag
		
		if nbtag=='0' and iPlot=='minMlb': 
			originalLJMETName=plotTreeName
			plotTreeName='minMleppJet'
# 	else:
# 		if 'SR' in region: cut += ' && (('+nWtagLJMETname+' > 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut'])+') || ('+nWtagLJMETname+' == 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut']+1)+'))'

	fullcut = cut+isEMCut+nttagCut+nWtagCut+nbtagCut

	# replace cuts for shifts
        cut_btagUp = fullcut.replace('NJetsHtagged','NJetsHtagged_shifts[0]')
        cut_btagDn = fullcut.replace('NJetsHtagged','NJetsHtagged_shifts[1]')
        cut_mistagUp = fullcut.replace('NJetsHtagged','NJetsHtagged_shifts[2]')
        cut_mistagDn = fullcut.replace('NJetsHtagged','NJetsHtagged_shifts[3]')

        cut_btagUp = cut_btagUp.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[0]')
        cut_btagDn = cut_btagDn.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[1]')
        cut_mistagUp = cut_mistagUp.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[2]')
        cut_mistagDn = cut_mistagDn.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[3]')

        cut_tauUp = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[0]')
        cut_tauDn = fullcut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[1]')

        cut_topsfUp = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[0]')
        cut_topsfDn = fullcut.replace(nttagLJMETname,nttagLJMETname+'_shifts[1]')

	print 'Flavour: '+isEM+' #ttags: '+nttag+' #Wtags: '+nWtag+' #btags: '+nbtag
	print 'plotTreeName: '+plotTreeName
	print 'Cuts: '+fullcut

	# Declare histograms
	hists = {}
	hists[iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process]  = TH1D(iPlot+'_'+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		hists[iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffUp_'    +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'trigeffDown_'  +lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
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
		for i in range(100): hists[iPlot+'pdf'+str(i)+lumiStr+'fb_'+catStr+'_'+process] = TH1D(iPlot+'pdf'+str(i)+lumiStr+'fb_'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()

	# DRAW histograms
	tTree[process].Draw(plotTreeName+' >> '+iPlot+''+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
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
		BTAGName = plotTreeName
		if 'CSVwithSF' in BTAGName or 'Htag' in BTAGName or 'MleppB' in BTAGName or 'BJetLead' in BTAGName or 'MinMlb' in BTAGName: BTAGName = BTAGName+'_shifts[0]'
		if '_lepBJets' in BTAGName: BTAGName = BTAGName.replace('_lepBJets','_bSFup_lepBJets')
                print 'BTAGup LJMET NAME',BTAGName
                tTree[process].Draw(BTAGName+    ' >> '+iPlot+'btagUp_'       +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_btagUp+')', 'GOFF')
                BTAGName = BTAGName.replace('_shifts[0]','_shifts[1]')
		BTAGName = BTAGName.replace('_bSFup','_bSFdn')
                print 'BTAGdown LJMET NAME',BTAGName
                tTree[process].Draw(BTAGName+    ' >> '+iPlot+'btagDown_'     +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+cut_btagDn+')', 'GOFF')
                BTAGName = BTAGName.replace('_shifts[1]','_shifts[2]')
		BTAGName = BTAGName.replace('_bSFdn','_lSFup')
                print 'MISTAGup LJMET NAME',BTAGName
                tTree[process].Draw(BTAGName+    ' >> '+iPlot+'mistagUp_'     +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+cut_mistagUp+')', 'GOFF')
                BTAGName = BTAGName.replace('_shifts[2]','_shifts[3]')
		BTAGName = BTAGName.replace('_lSFup','_lSFdn')
                print 'MISTAGdown LJMET NAME',BTAGName
		tTree[process].Draw(BTAGName+    ' >> '+iPlot+'mistagDown_'   +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+cut_mistagDn+')', 'GOFF')

		TTAGName= plotTreeName
		if 'Ttagged' in TTAGName or 'Tjet' in TTAGName or 'TJet' in TTAGName: TTAGName = TTAGName+'_shifts[0]'
		tTree[process].Draw(TTAGName+    ' >> '+iPlot+'topsfUp_'      +lumiStr+'fb_'+catStr+'_'+process, weightStr  +'*('+cut_topsfUp+')', 'GOFF')
                print 'TTAGup LJMET NAME',TTAGName
		TTAGName = TTAGName.replace('shifts[0]','shifts[1]')
		tTree[process].Draw(TTAGName+    ' >> '+iPlot+'topsfDown_'    +lumiStr+'fb_'+catStr+'_'+process, weightStr+'*('+cut_topsfDn+')', 'GOFF')
                print 'TTAGdown LJMET NAME',TTAGName

		TAUName = plotTreeName
		if 'Wtagged' in TAUName or 'Wjet' in TAUName or 'WJet' in TAUName: TAUName = TAUName+'_shifts[0]'
		print 'TAUup LJMET NAME',TAUName
		tTree[process].Draw(TAUName+     ' >> '+iPlot+'tau21Up_'      +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+cut_tauUp+')', 'GOFF')
		TAUName = TAUName.replace('shifts[0]','shifts[1]')
		print 'TAUdn LJMET NAME',TAUName
		tTree[process].Draw(TAUName+     ' >> '+iPlot+'tau21Down_'    +lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+cut_tauDn+')', 'GOFF')		

		if tTree[process+'jecUp']:
			tTree[process+'jecUp'].Draw(plotTreeName   +' >> '+iPlot+'jecUp'+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jecDown'].Draw(plotTreeName +' >> '+iPlot+'jecDown'+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		if tTree[process+'jerUp']:
			tTree[process+'jerUp'].Draw(plotTreeName   +' >> '+iPlot+'jerUp'+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
			tTree[process+'jerDown'].Draw(plotTreeName +' >> '+iPlot+'jerDown'+'_'+lumiStr+'fb_'+catStr+'_' +process, weightStr+'*('+fullcut+')', 'GOFF')
		for i in range(100): tTree[process].Draw(plotTreeName+' >> '+iPlot+'pdf'+str(i)+'_'+lumiStr+'fb_'+catStr+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+fullcut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
