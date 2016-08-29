#!/usr/bin/python

#import ROOT as R
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

def analyze(tTree,process,cutList,isotrig,doAllSys,doJetRwt,discriminantName,discriminantDetails,category,region):
	print "*****"*20
	print "*****"*20
	print "DISTRIBUTION:", discriminantName
	print "            -name in ljmet trees:", discriminantDetails[0]
	print "            -x-axis label is set to:", discriminantDetails[2]
	print "            -using the binning as:", discriminantDetails[1]
	discriminantLJMETName=discriminantDetails[0]
	xbins=array('d', discriminantDetails[1])
	xAxisLabel=discriminantDetails[2]
	
	print "/////"*5
	print "PROCESSING: ", process
	print "/////"*5
	cut = ''
	cut += '(leptonPt_singleLepCalc > '+str(cutList['lepPtCut'])+')'
	cut += ' && (corr_met_singleLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[0] > '+str(cutList['jet1PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[1] > '+str(cutList['jet2PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[2] > '+str(cutList['jet3PtCut'])+')'
	cut += ' && (NJetsHtagged == 0)'
	cut += ' && (minDR_lepJet > 0.4 || ptRel_lepJet > 40)'
	cut += ' && (NJets_JetSubCalc >= '+str(cutList['njetsCut'])+')'
	if 'CR' in region:
		cut += ' && (deltaR_lepJets[1] >= 0.4 && deltaR_lepJets[1] < '+str(cutList['drCut'])+')'
		if 'TT' in region: cut += ' && (NJetsCSVwithSF_JetSubCalc >= 2)'
		elif 'WJ' in region: cut += ' && (NJetsCSVwithSF_JetSubCalc == 0)'
	
	else:
		cut += ' && (deltaR_lepJets[1] >= '+str(cutList['drCut'])+')'
		cut += ' && (NJetsCSVwithSF_JetSubCalc >= '+str(cutList['nbjetsCut'])+')'

	wtagvar = 'NJetsWtagged_0p6'
	if region == 'Final':
		cut += ' && (('+wtagvar+' > 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut'])+') || ('+wtagvar+' == 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut']+1)+'))'

	# For N-1 W tagging cuts
	if 'PrunedNm1' in discriminantName: cut += ' && (theJetAK8NjettinessTau2_JetSubCalc_PtOrdered/theJetAK8NjettinessTau1_JetSubCalc_PtOrdered < 0.6)'
	if 'SoftDropMassNm1' in discriminantName: cut+=  ' && (theJetAK8NjettinessTau3_JetSubCalc_PtOrdered/theJetAK8NjettinessTau2_JetSubCalc_PtOrdered < 0.81)'

	pruned_massvar = 'theJetAK8PrunedMassWtagUncerts_JetSubCalc_PtOrdered'
	soft_massvar='theJetAK8SoftDropMass_JetSubCalc_PtOrdered'
	if 'Tau21Nm1' in discriminantName:  cut += ' && ('+pruned_massvar+' > 65 && '+pruned_massvar+' < 105)'
	if 'Tau32Nm1' in discriminantName:  cut += ' && ('+soft_massvar+' > 105 && '+ soft_massvar+' < 220)'


	# Choose between triggers
	TrigEff = 'TrigEffWeight'
	if isotrig == 1:
		cut += ' && DataPastTrigger == 1' # no MC HLT except signal  && MCPastTrigger == 1'
	else:
		TrigEff = 'TrigEffAltWeight'
		cut += ' && DataPastTriggerAlt == 1 && MCPastTriggerAlt == 1'
		
	print "Applying Cuts: ", cut

	# replacing R.TH1D with TH1D!
	hists = {}
	hists[discriminantName+'_'+lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'_'+lumiStr+'fb_'+category+'_' +process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		hists[discriminantName+'trigeffUp_'  +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'trigeffUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'trigeffDown_'+lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'trigeffDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'pileupUp_'  +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'pileupUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'pileupDown_'+lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'pileupDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRFcorrdUp_'  +lumiStr+'fb_'+category+'_'+process]=TH1D(discriminantName+'muRFcorrdUp_'  +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRFcorrdDown_'+lumiStr+'fb_'+category+'_'+process]=TH1D(discriminantName+'muRFcorrdDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRUp_'     +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'muRUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRDown_'   +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'muRDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muFUp_'     +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'muFUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muFDown_'   +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'muFDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'topptUp_'   +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'topptUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'topptDown_' +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'topptDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'btagUp_'+lumiStr+'fb_'+category+'_'+process]  = TH1D(discriminantName+'btagUp_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                hists[discriminantName+'btagDown_'+lumiStr+'fb_'+category+'_'+process]  = TH1D(discriminantName+'btagDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                hists[discriminantName+'mistagUp_'+lumiStr+'fb_'+category+'_'+process]  = TH1D(discriminantName+'mistagUp_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                hists[discriminantName+'mistagDown_'+lumiStr+'fb_'+category+'_'+process]  = TH1D(discriminantName+'mistagDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'tau21Up_'   +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'tau21Up_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'tau21Down_' +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'tau21Down_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jsfUp_'     +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'jsfUp_'     +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jsfDown_'   +lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'jsfDown_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                hists[discriminantName+'topsfUp_'+lumiStr+'fb_'+category+'_'+process]  = TH1D(discriminantName+'topsfUp_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                hists[discriminantName+'topsfDown_'+lumiStr+'fb_'+category+'_'+process]  = TH1D(discriminantName+'topsfDown_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if tTree[process+'jecUp']:		
			hists[discriminantName+'jecUp_'   +lumiStr+'fb_'+category+'_'+process]  = TH1D(discriminantName+'jecUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'jecDown_' +lumiStr+'fb_'+category+'_'+process]  = TH1D(discriminantName+'jecDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if tTree[process+'jerUp']:		
			hists[discriminantName+'jerUp_'   +lumiStr+'fb_'+category+'_'+process]  = TH1D(discriminantName+'jerUp_'   +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'jerDown_' +lumiStr+'fb_'+category+'_'+process]  = TH1D(discriminantName+'jerDown_' +lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		for i in range(100): hists[discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process] = TH1D(discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	for key in hists.keys(): hists[key].Sumw2()
		

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
		weightStr           =  jetSFstr+ ' * ' + TrigEff+' * pileupWeight * isoSF * lepIdSF * MCWeight_singleLepCalc * EGammaGsfSF * MuTrkSF/abs(MCWeight_singleLepCalc) * '+str(weight[process])
		weightTrigEffUpStr   = weightStr.replace(TrigEff,'TrigEffWeightUncert')
		weightTrigEffDownStr = weightStr
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

 
	#special data names
	#if 'Data' in process:

	#plot with a specific number of b tags
	if 'Bjet1' in discriminantName or 'Mlb' in discriminantName or 'b1' in discriminantName:
		cut += ' && (NJetsCSVwithSF_JetSubCalc > 0)'
	if 'b2' in discriminantName: cut += ' && (NJetsCSVwithSF_JetSubCalc > 1)'
	if 'Mlj' in discriminantName: cut += ' && (NJetsCSVwithSF_JetSubCalc == 0)'
	
	# replace cuts for shifts
        cut_btagUp = cut.replace('NJetsHtagged','NJetsHtagged_shifts[0]')
        cut_btagDn = cut.replace('NJetsHtagged','NJetsHtagged_shifts[1]')
        cut_mistagUp = cut.replace('NJetsHtagged','NJetsHtagged_shifts[2]')
        cut_mistagDn = cut.replace('NJetsHtagged','NJetsHtagged_shifts[3]')

        cut_btagUp = cut_btagUp.replace('NJetsCSVwithSF_JetSubCalc','NJetsCSVwithSF_JetSubCalc_shifts[0]')
        cut_btagDn = cut_btagDn.replace('NJetsCSVwithSF_JetSubCalc','NJetsCSVwithSF_JetSubCalc_shifts[1]')
        cut_mistagUp = cut_mistagUp.replace('NJetsCSVwithSF_JetSubCalc','NJetsCSVwithSF_JetSubCalc_shifts[2]')
        cut_mistagDn = cut_mistagDn.replace('NJetsCSVwithSF_JetSubCalc','NJetsCSVwithSF_JetSubCalc_shifts[3]')

        cut_tauUp = cut.replace(wtagvar,wtagvar+'_shifts[0]')
        cut_tauDn = cut.replace(wtagvar,wtagvar+'_shifts[1]')
 
	isEMCut=''
	if category=='E': isEMCut+=' && isElectron==1'
	elif category=='M': isEMCut+=' && isMuon==1'

	tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+''+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
	if doAllSys:
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'trigeffUp_'  +lumiStr+'fb_'+category+'_'+process, weightTrigEffUpStr+'*('+cut+isEMCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'trigeffDown_'+lumiStr+'fb_'+category+'_'+process, weightTrigEffDownStr+'*('+cut+isEMCut+')', 'GOFF')
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


		BTAGName = discriminantLJMETName
                if BTAGName == 'NJetsCSVwithSF_JetSubCalc' or BTAGName == 'NJetsHtagged' or BTAGName == 'minMleppBjet' or BTAGName == 'BJetLeadPt' or BTAGName == 'deltaRlepbJetInMinMlb' or BTAGName == 'deltaPhilepbJetInMinMlb':
                        BTAGName = BTAGName+'_shifts[0]'
		if '_lepBJets' in BTAGName: BTAGName = BTAGName.replace('_lepBJets','_bSFup_lepBJets')
                print 'BTAGup LJMET NAME',BTAGName
                tTree[process].Draw(BTAGName+' >> '+discriminantName+'btagUp_'+lumiStr+'fb_'+category+'_'+process, weightStr+'*('+cut_btagUp+isEMCut+')', 'GOFF')
                BTAGName = BTAGName.replace('_shifts[0]','_shifts[1]')
		BTAGName = BTAGName.replace('_bSFup','_bSFdn')
                print 'BTAGdown LJMET NAME',BTAGName
                tTree[process].Draw(BTAGName+' >> '+discriminantName+'btagDown_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut_btagDn+isEMCut+')', 'GOFF')
                BTAGName = BTAGName.replace('_shifts[1]','_shifts[2]')
		BTAGName = BTAGName.replace('_bSFdn','_lSFup')
                print 'MISTAGup LJMET NAME',BTAGName
                tTree[process].Draw(BTAGName+' >> '+discriminantName+'mistagUp_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut_mistagUp+isEMCut+')', 'GOFF')
                BTAGName = BTAGName.replace('_shifts[2]','_shifts[3]')
		BTAGName = BTAGName.replace('_lSFup','_lSFdn')
                print 'MISTAGdown LJMET NAME',BTAGName
		tTree[process].Draw(BTAGName+' >> '+discriminantName+'mistagDown_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut_mistagDn+isEMCut+')', 'GOFF')


		TTAGName= discriminantLJMETName
		if 'Ttagged' in TTAGName or 'Tjet' in TTAGName or 'TJet' in TTAGName: TTAGName = TTAGName+'_shifts[0]'
		tTree[process].Draw(TTAGName+' >> '+discriminantName+'topsfUp_'+lumiStr+'fb_'+category+'_'+process, weightStr  +'*('+cut+isEMCut+')', 'GOFF')
                print 'TTAGup LJMET NAME',TTAGName

		TTAGName = TTAGName.replace('shifts[0]','shifts[1]')
		tTree[process].Draw(TTAGName+' >> '+discriminantName+'topsfDown_'+lumiStr+'fb_'+category+'_'+process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
                print 'TTAGdown LJMET NAME',TTAGName

		TAUName = discriminantLJMETName
		if 'Wtagged' in TAUName or 'Wjet' in TAUName or 'WJet' in TAUName: 
			TAUName = TAUName+'_shifts[0]'
		print 'TAUup LJMET NAME',TAUName
		tTree[process].Draw(TAUName+' >> '+discriminantName+'tau21Up'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut_tauUp+isEMCut+')', 'GOFF')

		TAUName = TAUName.replace('shifts[0]','shifts[1]')
		print 'TAUdn LJMET NAME',TAUName
		tTree[process].Draw(TAUName+' >> '+discriminantName+'tau21Down'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut_tauDn+isEMCut+')', 'GOFF')		

		if tTree[process+'jecUp']:
			tTree[process+'jecUp'].Draw(discriminantLJMETName   +' >> '+discriminantName+'jecUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
			tTree[process+'jecDown'].Draw(discriminantLJMETName +' >> '+discriminantName+'jecDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		if tTree[process+'jerUp']:
			tTree[process+'jerUp'].Draw(discriminantLJMETName   +' >> '+discriminantName+'jerUp'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
			tTree[process+'jerDown'].Draw(discriminantLJMETName +' >> '+discriminantName+'jerDown'+'_'+lumiStr+'fb_'+category+'_' +process, weightStr+'*('+cut+isEMCut+')', 'GOFF')
		for i in range(100): tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_'+category+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+cut+isEMCut+')', 'GOFF')
	
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists
