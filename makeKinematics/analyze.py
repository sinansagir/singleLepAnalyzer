#!/usr/bin/python

import ROOT as R
from array import array
from weights import *

"""
--This function will make kinematic plots for a given distribution for electron, muon channels and their combination
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

def analyze(tTree,process,cutList,doAllSys,discriminantName,discriminantDetails,category):
	discriminantLJMETName=discriminantDetails[0]
	xbins=array('d', discriminantDetails[1])
	xAxisLabel=discriminantDetails[2]
	doJetReweighting = False#'WJetsMG' in process or 'QCDht' in process

	print "/////"*5
	print "PROCESSING: ", process
	print "/////"*5
	#Common selections:
	cut  = '(leptonPt_singleLepCalc > '+str(cutList['lepPtCut'])+')'
	cut += ' && (corr_met_singleLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[0] > '+str(cutList['jet1PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[1] > '+str(cutList['jet2PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[2] > '+str(cutList['jet3PtCut'])+')'
	cut += ' && (minDR_lepJet > 0.4 || ptRel_lepJet > 40)' # 2D cut                     
	cut += ' && (deltaR_lepJets[1] > '+str(cutList['drCut'])+')'
	cut += ' && (AK4HT > '+str(cutList['htCut'])+')'
	cut += ' && (AK4HTpMETpLepPt > '+str(cutList['stCut'])+')'
	cut += ' && (NJets_JetSubCalc >= '+str(cutList['njetsCut'])+')'
	cut += ' && (DataPastTrigger == 1 && MCPastTrigger == 1)' #standard triggers, check trigger weight branch name!
	#cut += ' && (DataPastTriggerAlt == 1 && MCPastTriggerAlt == 1)' #alternative triggers, check trigger weight branch name!
	
	#kinematic specific selections:
	if 'Bjet1' in discriminantName: cut += ' && (NJetsCSVwithSF_JetSubCalc > 0)'
	elif 'Mlb' in discriminantName: cut += ' && (NJetsCSVwithSF_JetSubCalc > 0)'
	elif 'b1'  in discriminantName: cut += ' && (NJetsCSVwithSF_JetSubCalc > 0)'
	elif 'b2'  in discriminantName: cut += ' && (NJetsCSVwithSF_JetSubCalc > 1)'
	elif 'Mlj' in discriminantName: cut += ' && (NJetsCSVwithSF_JetSubCalc == 0)'
	cut += ' && (NJetsCSVwithSF_JetSubCalc >= '+str(cutList['nbjetsCut'])+')'

	isEMCut=''
	if category=='E': isEMCut+=' && isElectron==1'
	elif category=='M': isEMCut+=' && isMuon==1'

	TrigEff = 'TrigEffWeight' #standard triggers
	#TrigEff = 'TrigEffAltWeight' #alternative triggers
	
	hists = {}
	hists[discriminantName+'_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'_'+lumiStr+'fb_'+category+'_' +process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		hists[discriminantName+'pileupUp_'  +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'pileupUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'pileupDown_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'pileupDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRFcorrdUp_'  +lumiStr+'fb_'+category+'_'+process]=R.TH1D(discriminantName+'muRFcorrdUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRFcorrdDown_'+lumiStr+'fb_'+category+'_'+process]=R.TH1D(discriminantName+'muRFcorrdDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muRUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muRDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muFUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muFUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muFDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muFDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'topptUp_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'topptUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'topptDown_' +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'topptDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'topsfUp_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'topsfUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'topsfDown_' +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'topsfDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jmrUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmrUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jmrDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmrDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jmsUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmsUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jmsDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmsDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'tau21Up_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'tau21Up_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'tau21Down_' +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'tau21Down_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jsfUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jsfUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jsfDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jsfDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'btagUp_'    +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'btagUp_'    +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'btagDown_'  +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'btagDown_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'mistagUp_'  +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'mistagUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'mistagDown_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'mistagDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if tTree[process+'jecUp']:		
			hists[discriminantName+'jecUp_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jecUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'jecDown_' +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jecDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if tTree[process+'jerUp']:		
			hists[discriminantName+'jerUp_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jerUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'jerDown_' +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jerDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#if tTree[process+'btagCorrUp']:		
		#	hists[discriminantName+'btagCorrUp_'  +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'btagCorrUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		#	hists[discriminantName+'btagCorrDown_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'btagCorrDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		for i in range(100): hists[discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()
		
	if doJetReweighting:
		jetSFstr   = 'JetSF_pTNbwflat'
		jetSFupstr = 'JetSFupwide_pTNbwflat'
		jetSFdnstr = 'JetSFdnwide_pTNbwflat'
	if not doJetReweighting:
		jetSFstr   = '1'
		jetSFupstr = '1'
		jetSFdnstr = '1'

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

	elif 'TTJets' in process and False:
		weightStr           = jetSFstr+' * '+TrigEff+' * pileupWeight * isoSF * lepIdSF * MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc) * '+str(weight[process])
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
	else: 
		weightStr           = jetSFstr+' * '+TrigEff+' * pileupWeight * isoSF * lepIdSF * MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc) * '+str(weight[process])
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

	print "Applying Cuts   : ", cut+isEMCut
	print "Applying Weights: "
	print "                  (printing nominal weights!)"
	print "                  ", weightStr
	
	if 'Data' in process:
		origname = discriminantLJMETName
		if discriminantName == 'NTJetsSF': discriminantLJMETName = 'NJetsToptagged_tau0p69'
		if discriminantName == 'NWJets': discriminantLJMETName = 'NJetsWtagged_0p6'
		if discriminantName == 'PrunedSmeared': discriminantLJMETName = 'theJetAK8PrunedMass_JetSubCalc_PtOrdered'
		if origname != discriminantLJMETName: print 'NEW LJMET NAME:',discriminantLJMETName

	tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+''+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
	if doAllSys:
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pileupUp_'  +lumiStr+'fb_'+category+'_'+process, weightPileupUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pileupDown_'+lumiStr+'fb_'+category+'_'+process, weightPileupDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRFcorrdUp_'  +lumiStr+'fb_'+category+'_'+process, weightmuRFcorrdUpStr  +'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRFcorrdDown_'+lumiStr+'fb_'+category+'_'+process, weightmuRFcorrdDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRUp_'     +lumiStr+'fb_'+category+'_'+process, weightmuRUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRDown_'   +lumiStr+'fb_'+category+'_'+process, weightmuRDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muFUp_'     +lumiStr+'fb_'+category+'_'+process, weightmuFUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muFDown_'   +lumiStr+'fb_'+category+'_'+process, weightmuFDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'topptUp_'   +lumiStr+'fb_'+category+'_'+process, weighttopptUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'topptDown_' +lumiStr+'fb_'+category+'_'+process, weighttopptDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'jsfUp_'     +lumiStr+'fb_'+category+'_'+process, weightjsfUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'jsfDown_'   +lumiStr+'fb_'+category+'_'+process, weightjsfDownStr+'*('+cut+isEMCut+')', 'GOFF')
		
		tTagSFshiftName = discriminantLJMETName
		if 'NJetsToptagged' in discriminantLJMETName and 'SF' in discriminantLJMETName: 
			tTagSFshiftName = discriminantLJMETName+'up'
		print 'topTagShift NAME',tTagSFshiftName.replace('SFup','SFup')
		tTree[process].Draw(tTagSFshiftName.replace('SFup','SFup')+' >> '+discriminantName+'topsfUp_'   +lumiStr+'fb_'+category+'_'+process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		print 'topTagShift NAME',tTagSFshiftName.replace('SFup','SFdn')
		tTree[process].Draw(tTagSFshiftName.replace('SFup','SFdn')+' >> '+discriminantName+'topsfDown_' +lumiStr+'fb_'+category+'_'+process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		
		wTagSFshiftName = discriminantLJMETName
		if discriminantLJMETName == 'theJetAK8PrunedMassJMRSmeared_JetSubCalc': wTagSFshiftName = 'theJetAK8PrunedMassJMRSmearedUp_JetSubCalc'
		if 'NJetsWtagged_' in discriminantLJMETName: wTagSFshiftName = discriminantLJMETName+'_shifts[0]'
		if 'Wjet' in discriminantLJMETName: wTagSFshiftName = discriminantLJMETName+'_shifts[0]'
		if 'WJetLeadPt' in discriminantLJMETName: wTagSFshiftName = discriminantLJMETName+'_shifts[0]'
		if 'taggedW' in discriminantLJMETName: wTagSFshiftName = discriminantLJMETName+'_shifts[0]'
		if 'WJetTaggedPt' in discriminantLJMETName: wTagSFshiftName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtJMRup')
		print 'JMRup LJMET NAME',wTagSFshiftName.replace('SmearedUp','SmearedUp').replace('JMRup','JMRup').replace('_shifts[0]','_shifts[0]')
		tTree[process].Draw(wTagSFshiftName.replace('SmearedUp','SmearedUp').replace('JMRup','JMRup').replace('_shifts[0]','_shifts[0]')+' >> '+discriminantName+'jmrUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		print 'JMRdn LJMET NAME',wTagSFshiftName.replace('SmearedUp','SmearedDn').replace('JMRup','JMRdn').replace('_shifts[0]','_shifts[1]')
		tTree[process].Draw(wTagSFshiftName.replace('SmearedUp','SmearedDn').replace('JMRup','JMRdn').replace('_shifts[0]','_shifts[1]')+' >> '+discriminantName+'jmrDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		print 'JMSup LJMET NAME',wTagSFshiftName.replace('SmearedUp','Smeared').replace('JMRup','JMSup').replace('_shifts[0]','_shifts[2]')
		tTree[process].Draw(wTagSFshiftName.replace('SmearedUp','Smeared').replace('JMRup','JMSup').replace('_shifts[0]','_shifts[2]')+' >> '+discriminantName+'jmsUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		print 'JMSdn LJMET NAME',wTagSFshiftName.replace('SmearedUp','Smeared').replace('JMRup','JMSdn').replace('_shifts[0]','_shifts[3]')
		tTree[process].Draw(wTagSFshiftName.replace('SmearedUp','Smeared').replace('JMRup','JMSdn').replace('_shifts[0]','_shifts[3]')+' >> '+discriminantName+'jmsDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		print 'TAUup LJMET NAME',wTagSFshiftName.replace('SmearedUp','Smeared').replace('JMRup','TAUup').replace('_shifts[0]','_shifts[4]')
		tTree[process].Draw(wTagSFshiftName.replace('SmearedUp','Smeared').replace('JMRup','TAUup').replace('_shifts[0]','_shifts[4]')+' >> '+discriminantName+'tau21Up'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		print 'TAUdn LJMET NAME',wTagSFshiftName.replace('SmearedUp','Smeared').replace('JMRup','TAUdn').replace('_shifts[0]','_shifts[5]')
		tTree[process].Draw(wTagSFshiftName.replace('SmearedUp','Smeared').replace('JMRup','TAUdn').replace('_shifts[0]','_shifts[5]')+' >> '+discriminantName+'tau21Down'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')		
		
		bTagSFshiftName = discriminantLJMETName
		if 'minMlb' in discriminantLJMETName or 'Bjet' in discriminantLJMETName or 'NBJets' in discriminantLJMETName: 
			bTagSFshiftName = discriminantLJMETName+'_shifts[0]'
		print 'BTAGup LJMET NAME',bTagSFshiftName.replace('_shifts[0]','[_shifts0]')
		tTree[process].Draw(bTagSFshiftName.replace('_shifts[0]','_shifts[0]')+' >> '+discriminantName+'btagUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		print 'BTAGdn LJMET NAME',bTagSFshiftName.replace('_shifts[0]','_shifts[1]')
		tTree[process].Draw(bTagSFshiftName.replace('_shifts[0]','_shifts[1]')+' >> '+discriminantName+'btagDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		print 'MISTAGup LJMET NAME',bTagSFshiftName.replace('_shifts[0]','_shifts[2]')
		tTree[process].Draw(bTagSFshiftName.replace('_shifts[0]','_shifts[2]')+' >> '+discriminantName+'mistagUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		print 'MISTAGdn LJMET NAME',bTagSFshiftName.replace('_shifts[0]','_shifts[3]')
		tTree[process].Draw(bTagSFshiftName.replace('_shifts[0]','_shifts[3]')+' >> '+discriminantName+'mistagDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		
		if tTree[process+'jecUp']:
			tTree[process+'jecUp'].Draw(discriminantLJMETName   +' >> '+discriminantName+'jecUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
			tTree[process+'jecDown'].Draw(discriminantLJMETName +' >> '+discriminantName+'jecDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		if tTree[process+'jerUp']:
			tTree[process+'jerUp'].Draw(discriminantLJMETName   +' >> '+discriminantName+'jerUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
			tTree[process+'jerDown'].Draw(discriminantLJMETName +' >> '+discriminantName+'jerDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		#if tTree[process+'btagCorrUp']:
		#	tTree[process+'btagCorrUp'].Draw(discriminantLJMETName  +' >> '+discriminantName+'btagCorrUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		#	tTree[process+'btagCorrDown'].Draw(discriminantLJMETName+' >> '+discriminantName+'btagCorrDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		for i in range(100): tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+cut+isEMCut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists

