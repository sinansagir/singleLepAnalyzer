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

def analyze(tTree,process,cutList,isotrig,doAllSys,discriminantName,discriminantDetails,category):
	print "*****"*20
	print "*****"*20
	print "DISTRIBUTION:", discriminantName
	print "            -name in ljmet trees:", discriminantDetails[0]
	print "            -x-axis label is set to:", discriminantDetails[2]
	print "            -using the binning as:", discriminantDetails[1]
	discriminantLJMETName=discriminantDetails[0]
	xbins=array('d', discriminantDetails[1])
	xAxisLabel=discriminantDetails[2]
	
	wtagvar = 'NJetsWtagged_JMR'
	if 'Data' in process: wtagvar = 'NJetsWtagged'

	print "/////"*5
	print "PROCESSING: ", process
	print "/////"*5
	cut = ''
	cut += '(leptonPt_singleLepCalc > '+str(cutList['lepPtCut'])+')'
	cut += ' && (corr_met_singleLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[0] > '+str(cutList['leadJetPtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[1] > '+str(cutList['subLeadJetPtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[2] > '+str(cutList['thirdJetPtCut'])+')'
	cut += ' && (NJetsHtagged == 0)'
#	cut += ' && ('+wtagvar+' == 0)'
	cut += ' && (deltaR_lepClosestJet > 0.4 || PtRelLepClosestJet > 40)'
	cut += ' && (NJets_JetSubCalc >= '+str(cutList['njetsCut'])+')'
#	cut += ' && (('+wtagvar+' > 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut'])+') || ('+wtagvar+' == 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut']+1)+'))'
	cut += ' && (NJetsCSVwithSF_JetSubCalc >= '+str(cutList['nbjetsCut'])+')'
	cut += ' && (deltaR_lepJets[1] >= '+str(cutList['drCut'])+')'

	if 'PrunedSmearedNm1' in discriminantName: cut += ' && (theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered < 0.6)'

	massvar = 'theJetAK8PrunedMassJMRSmeared_JetSubCalc'
	if 'Data' in process: massvar = 'theJetAK8PrunedMass_JetSubCalc_PtOrdered'

	if 'Tau21Nm1' in discriminantName:  cut += ' && ('+massvar+' > 65 && '+massvar+' < 105)'

	
	doTopRwt = False

	TrigEff = 'TrigEffWeight'
	if isotrig == 1:
		cut += ' && DataPastTrigger == 1 && MCPastTrigger == 1'
	else:
		TrigEff = 'TrigEffAltWeight'
		cut += ' && DataPastTriggerAlt == 1 && MCPastTriggerAlt == 1'
		
	print "Applying Cuts: ", cut
	
	hists = {}
	hists[discriminantName+'_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'_'+lumiStr+'fb_'+category+'_' +process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		hists[discriminantName+'pileupUp_'  +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'pileupUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'pileupDown_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'pileupDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRFcorrdUp_'  +lumiStr+'fb_'+category+'_'+process]=R.TH1D(discriminantName+'muRFcorrdUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRFcorrdDown_'+lumiStr+'fb_'+category+'_'+process]=R.TH1D(discriminantName+'muRFcorrdDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRFenvUp_'  +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muRFenvUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRFenvDown_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muRFenvDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muRUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muRDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muFUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muFUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muFDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'muFDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'pdfUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'pdfUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'pdfDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'pdfDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'topptUp_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'topptUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'topptDown_' +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'topptDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jmrUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmrUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jmrDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmrDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jmsUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmsUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jmsDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jmsDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'tau21Up_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'tau21Up_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'tau21Down_' +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'tau21Down_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jsfUp_'     +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jsfUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jsfDown_'   +lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'jsfDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if tTree[process+'jecUp']:		
			hists[discriminantName+'jecUp_'   +lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'jecUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'jecDown_' +lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'jecDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if tTree[process+'jerUp']:		
			hists[discriminantName+'jerUp_'   +lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'jerUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'jerDown_' +lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'jerDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if tTree[process+'btagUp']:		
			hists[discriminantName+'btagUp_'  +lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'btagUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'btagDown_'+lumiStr+'fb_'+category+'_'+process]  = R.TH1D(discriminantName+'btagDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		for i in range(100): hists[discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process] = R.TH1D(discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()
		
	if 'Data' in process: 
		weightStr           = '1'
		weightPileupUpStr   = '1'
		weightPileupDownStr = '1'
		weightmuRFcorrdUpStr   = '1'
		weightmuRFcorrdDownStr = '1'
		weightmuRFenvUpStr  = '1'
		weightmuRFenvDownStr= '1'
		weightmuRUpStr   = '1'
		weightmuRDownStr = '1'
		weightmuFUpStr   = '1'
		weightmuFDownStr = '1'
		weightPDFUpStr   = '1'
		weightPDFDownStr = '1'
		weighttopptUpStr    = '1'
		weighttopptDownStr  = '1'
		weightjsfUpStr    = '1'
		weightjsfDownStr  = '1'

	elif 'TTJets' in process and doTopRwt:
		weightStr           = 'TrigEffWeight * JetSF * pileupWeight * isoSF * lepIdSF * MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc) * '+str(weight[process])
#		weightStr           = 'topPtWeight * TrigEffWeight * JetSF * pileupWeight * isoSF * lepIdSF * MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc) * '+str(weight[process])
		weightPileupUpStr   = weightStr.replace('pileupWeight','pileupWeightUp')
		weightPileupDownStr = weightStr.replace('pileupWeight','pileupWeightDown')
		weightmuRFcorrdUpStr   = 'renormWeights[5] * '+weightStr
		weightmuRFcorrdDownStr = 'renormWeights[3] * '+weightStr
		weightmuRFenvUpStr  = 'renormUp * '+weightStr
		weightmuRFenvDownStr= 'renormDown * '+weightStr
		weightmuRUpStr      = 'renormWeights[4] * '+weightStr
		weightmuRDownStr    = 'renormWeights[2] * '+weightStr
		weightmuFUpStr      = 'renormWeights[1] * '+weightStr
		weightmuFDownStr    = 'renormWeights[0] * '+weightStr
		weightPDFUpStr      = 'pdfUp * '+weightStr
		weightPDFDownStr    = 'pdfDown * '+weightStr
		weighttopptUpStr    = weightStr
		weighttopptDownStr  = 'topPtWeight * '+weightStr
		weightjsfUpStr      = weightStr.replace('JetSF','JetSFup')
		weightjsfDownStr    = weightStr.replace('JetSF','JetSFdn')
	else: 
#
		weightStr           = TrigEff+' * pileupWeight * JetSF_pTNbwflat * isoSF * lepIdSF * MCWeight_singleLepCalc/abs(MCWeight_singleLepCalc) * '+str(weight[process])
		weightPileupUpStr   = weightStr.replace('pileupWeight','pileupWeightUp')
		weightPileupDownStr = weightStr.replace('pileupWeight','pileupWeightDown')
		weightmuRFcorrdUpStr   = 'renormWeights[5] * '+weightStr
		weightmuRFcorrdDownStr = 'renormWeights[3] * '+weightStr
		weightmuRFenvUpStr  = 'renormUp * '+weightStr
		weightmuRFenvDownStr= 'renormDown * '+weightStr
		weightmuRUpStr      = 'renormWeights[4] * '+weightStr
		weightmuRDownStr    = 'renormWeights[2] * '+weightStr
		weightmuFUpStr      = 'renormWeights[1] * '+weightStr
		weightmuFDownStr    = 'renormWeights[0] * '+weightStr
		weightPDFUpStr      = 'pdfUp * '+weightStr
		weightPDFDownStr    = 'pdfDown * '+weightStr
		weighttopptUpStr    = weightStr
		weighttopptDownStr  = 'topPtWeight * '+weightStr
		weightjsfUpStr      = weightStr.replace('JetSF','JetSFupwide')
		weightjsfDownStr    = weightStr.replace('JetSF','JetSFdnwide')

	if 'Data' in process:
		origname = discriminantLJMETName
		if discriminantName == 'NWJetsSmeared':
			discriminantLJMETName = 'NJetsWtagged_0p6'
		if '0p55' in discriminantName:
			discriminantLJMETName = 'NJetsWtagged_0p55'
		if discriminantName == 'PrunedSmeared':
			discriminantLJMETName = 'theJetAK8PrunedMass_JetSubCalc_PtOrdered'
			#discriminantLJMETName = 'theJetAK8PrunedMass_JetSubCalc_new'
		if origname != discriminantLJMETName:
			print 'NEW LJMET NAME:',discriminantLJMETName

	if 'Bjet1' in discriminantName or 'Mlb' in discriminantName or 'b1' in discriminantName:
		cut += ' && (NJetsCSVwithSF_JetSubCalc > 0)'
	if 'b2' in discriminantName:
		cut += ' && (NJetsCSVwithSF_JetSubCalc > 1)'

	if 'Mlj' in discriminantName: cut += ' && (NJetsCSVwithSF_JetSubCalc == 0)'

	isEMCut=''
	if category=='E': isEMCut+=' && isElectron==1'
	elif category=='M': isEMCut+=' && isMuon==1'

	tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+''+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
	if doAllSys:
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pileupUp_'  +lumiStr+'fb_'+category+'_'+process, weightPileupUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pileupDown_'+lumiStr+'fb_'+category+'_'+process, weightPileupDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRFcorrdUp_'  +lumiStr+'fb_'+category+'_'+process, weightmuRFcorrdUpStr  +'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRFcorrdDown_'+lumiStr+'fb_'+category+'_'+process, weightmuRFcorrdDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRFenvUp_'  +lumiStr+'fb_'+category+'_'+process, weightmuRFenvUpStr  +'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRFenvDown_'+lumiStr+'fb_'+category+'_'+process, weightmuRFenvDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRUp_'     +lumiStr+'fb_'+category+'_'+process, weightmuRUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRDown_'   +lumiStr+'fb_'+category+'_'+process, weightmuRDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muFUp_'     +lumiStr+'fb_'+category+'_'+process, weightmuFUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muFDown_'   +lumiStr+'fb_'+category+'_'+process, weightmuFDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pdfUp_'     +lumiStr+'fb_'+category+'_'+process, weightPDFUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pdfDown_'   +lumiStr+'fb_'+category+'_'+process, weightPDFDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'topptUp_'   +lumiStr+'fb_'+category+'_'+process, weighttopptUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'topptDown_' +lumiStr+'fb_'+category+'_'+process, weighttopptDownStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'jsfUp_'     +lumiStr+'fb_'+category+'_'+process, weightjsfUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'jsfDown_'   +lumiStr+'fb_'+category+'_'+process, weightjsfDownStr+'*('+cut+isEMCut+')', 'GOFF')
		JMRName = discriminantLJMETName
		if discriminantLJMETName == 'theJetAK8PrunedMassJMRSmeared_JetSubCalc': JMRName = 'theJetAK8PrunedMassJMRSmearedUp_JetSubCalc'
		if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[0]'
		if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[0]'
		if 'Wjet' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[0]'
		if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[0]'
		if 'taggedW' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[0]'
		if 'WJetTaggedPt' in discriminantLJMETName: JMRName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtJMRup')
		print 'JMRup LJMET NAME',JMRName
		tTree[process].Draw(JMRName+' >> '+discriminantName+'jmrUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')

		JMRName = discriminantLJMETName
		if discriminantLJMETName == 'theJetAK8PrunedMassJMRSmeared_JetSubCalc': JMRName = 'theJetAK8PrunedMassJMRSmearedDn_JetSubCalc'
		if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[1]'
		if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[1]'
		if 'Wjet' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[1]'
		if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[1]'
		if 'taggedW' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[1]'
		if 'WJetTaggedPt' in discriminantLJMETName: JMRName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtJMRdn')
		print 'JMRdn LJMET NAME',JMRName
		tTree[process].Draw(JMRName+' >> '+discriminantName+'jmrDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')

		JMSName = discriminantLJMETName
		if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[2]'
		if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[2]'
		if 'Wjet' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[2]'
		if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[2]'
		if 'taggedW' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[2]'
		if 'WJetTaggedPt' in discriminantLJMETName: JMSName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtJMSup')
		print 'JMSup LJMET NAME',JMSName
		tTree[process].Draw(JMSName+' >> '+discriminantName+'jmsUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')

		JMSName = discriminantLJMETName
		if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[3]'
		if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[3]'
		if 'Wjet' in discriminantLJMETName: JMSName = discriminantLJMETName+'_shifts[3]'
		if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[3]'
		if 'taggedW' in discriminantLJMETName: JMSName = discriminantLJMETName+'_shifts[3]'
		if 'WJetTaggedPt' in discriminantLJMETName: JMSName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtJMSdn')
		print 'JMSdn LJMET NAME',JMSName
		tTree[process].Draw(JMSName+' >> '+discriminantName+'jmsDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')

		TAUName = discriminantLJMETName
		if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[4]'
		if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[4]'
		if 'Wjet' in discriminantLJMETName: TAUName = discriminantLJMETName+'_shifts[4]'
		if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[4]'
		if 'taggedW' in discriminantLJMETName: TAUName = discriminantLJMETName+'_shifts[4]'
		if 'WJetTaggedPt' in discriminantLJMETName: TAUName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtTAUup')
		print 'TAUup LJMET NAME',TAUName
		tTree[process].Draw(TAUName+' >> '+discriminantName+'tau21Up'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')

		TAUName = discriminantLJMETName
		if discriminantLJMETName == 'NJetsWtagged_JMR': JMRName = 'NJetsWtagged_shifts[5]'
		if 'NJetsWtagged_0p' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[5]'
		if 'Wjet' in discriminantLJMETName: TAUName = discriminantLJMETName+'_shifts[5]'
		if 'WJetLeadPt' in discriminantLJMETName: JMRName = discriminantLJMETName+'_shifts[5]'
		if 'taggedW' in discriminantLJMETName: TAUName = discriminantLJMETName+'_shifts[5]'
		if 'WJetTaggedPt' in discriminantLJMETName: TAUName = discriminantLJMETName.replace('WJetTaggedPt','WJetTaggedPtTAUdn')
		print 'TAUdn LJMET NAME',TAUName
		tTree[process].Draw(TAUName+' >> '+discriminantName+'tau21Down'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')		
		if tTree[process+'jecUp']:
			tTree[process+'jecUp'].Draw(discriminantLJMETName   +' >> '+discriminantName+'jecUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
			tTree[process+'jecDown'].Draw(discriminantLJMETName +' >> '+discriminantName+'jecDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		if tTree[process+'jerUp']:
			tTree[process+'jerUp'].Draw(discriminantLJMETName   +' >> '+discriminantName+'jerUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
			tTree[process+'jerDown'].Draw(discriminantLJMETName +' >> '+discriminantName+'jerDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		if tTree[process+'btagUp']:
			tTree[process+'btagUp'].Draw(discriminantLJMETName  +' >> '+discriminantName+'btagUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
			tTree[process+'btagDown'].Draw(discriminantLJMETName+' >> '+discriminantName+'btagDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		for i in range(100): tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+cut+isEMCut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists

