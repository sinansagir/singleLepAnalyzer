#!/usr/bin/python

from array import array
from weights import *
#import ROOT as R
from ROOT import TH1D,TFile,TTree

"""
--This function will make theta templates for a given distribution and a category
--Check the cuts below to make sure those are the desired full set of cuts!
--The applied weights are defined in "weights.py". Also, the additional weights (SFs, 
negative MC weights, ets) applied below should be checked!
"""

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb

def analyze(tTree,process,cutList,doAllSys,discriminantName,discriminantDetails,category):
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
	cut  = '(leptonPt_singleLepCalc > '+str(cutList['lepPtCut'])+')'
	cut += ' && (corr_met_singleLepCalc > '+str(cutList['metCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[0] > '+str(cutList['jet1PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[1] > '+str(cutList['jet2PtCut'])+')'
	cut += ' && (theJetPt_JetSubCalc_PtOrdered[2] > '+str(cutList['jet3PtCut'])+')'
	cut += ' && (minDR_lepJet > 0.4 || ptRel_lepJet > 40)' # 2D cut
	cut += ' && (deltaR_lepJets[1] >= '+str(cutList['drCut'])+')'
	cut += ' && (NJets_JetSubCalc >= '+str(cutList['njetsCut'])+')'
	cut += ' && DataPastTrigger == 1' # MC has no HLT (could test requiring signal to pass) && MCPastTrigger == 1' #standard triggers
	cut += ' && NJetsHtagged == 0'
	 	# replace cuts for shifts
	cut_btagUp = cut.replace('NJetsHtagged','NJetsHtagged_shifts[0]');
	cut_btagDn = cut.replace('NJetsHtagged','NJetsHtagged_shifts[1]');
	cut_mistagUp = cut.replace('NJetsHtagged','NJetsHtagged_shifts[2]');
	cut_mistagDn = cut.replace('NJetsHtagged','NJetsHtagged_shifts[3]');

	print "Applying Cuts: ", cut
	
	isEM  = category['isEM']
	nttag = category['nttag']
	nWtag = category['nWtag']
	nbtag = category['nbtag']
	catStr = isEM+'_nT'+nttag+'_nW'+nWtag+'_nB'+nbtag
	
	hists = {}
	hists[discriminantName+'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
	if doAllSys:
		hists[discriminantName+'trigeffUp_'  +lumiStr+'fb_is'+catStr+'_'+process] = TH1D(discriminantName+'trigeffUp_'  +lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'trigeffDown_'+lumiStr+'fb_is'+catStr+'_'+process] = TH1D(discriminantName+'trigeffDown_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'pileupUp'  +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'pileupUp'  +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'pileupDown'+'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'pileupDown'+'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRFcorrdUp'  +'_'+lumiStr+'fb_is'+catStr+'_'+process]=TH1D(discriminantName+'muRFcorrdUp'  +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRFcorrdDown'+'_'+lumiStr+'fb_is'+catStr+'_'+process]=TH1D(discriminantName+'muRFcorrdDown'+'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'muRUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muRDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'muRDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muFUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'muFUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'muFDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'muFDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'topptUp'   +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'topptUp'   +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'topptDown' +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'topptDown' +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
                hists[discriminantName+'btagUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'btagUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'btagDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'btagDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'mistagUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'mistagUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'mistagDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'mistagDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'tau21Up'   +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'tau21Up'   +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'tau21Down' +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'tau21Down' +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jsfUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'jsfUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'jsfDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'jsfDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)				    
		hists[discriminantName+'topsfUp'  +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'topsfUp'  +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		hists[discriminantName+'topsfDown'  +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'topsfDown'  +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)   
		if tTree[process+'jerUp']: 
			hists[discriminantName+'jerUp'   +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'jerUp'   +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'jerDown' +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'jerDown' +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		if tTree[process+'jecUp']:
			hists[discriminantName+'jecUp'   +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'jecUp'   +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
			hists[discriminantName+'jecDown' +'_'+lumiStr+'fb_is'+catStr+'_'+process]  = TH1D(discriminantName+'jecDown' +'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)
		for i in range(100): hists[discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_is'+catStr+'_'+process] = TH1D(discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_is'+catStr+'_'+process,xAxisLabel,len(xbins)-1,xbins)				
	for key in hists.keys(): hists[key].Sumw2()
	
	
        jetSFstr ='1'
	if 'WJetsMG'in process or 'QCD' in process:	
		jetSFstr   = 'JetSF_80X'
	
	if 'Data' in process: 
		weightStr           = '1'
		weightPileupUpStr   = '1'
		weightPileupDownStr = '1'
		weightmuRFcorrdUpStr   = '1'
		weightmuRFcorrdDownStr = '1'
		weightmuRUpStr      = '1'
		weightmuRDownStr    = '1'
		weightmuFUpStr      = '1'
		weightmuFDownStr    = '1'
		weighttopptUpStr    = '1'
		weighttopptDownStr  = '1'
		weightjsfUpStr      = '1'
		weightjsfDownStr    = '1'       
	else: 
		weightStr           =  jetSFstr+ ' * TrigEffWeight * pileupWeight * isoSF * lepIdSF * MCWeight_singleLepCalc * EGammaGsfSF * MuTrkSF/abs(MCWeight_singleLepCalc) * '+str(weight[process])
		weightTrigEffUpStr   = weightStr.replace('TrigEffWeight','TrigEffWeightUncert')
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
		
	isEMCut= ''
	if isEM=='E': isEMCut+=' && isElectron==1'
	elif isEM=='M': isEMCut+=' && isMuon==1'
	
	nttagLJMETname = 'NJetsTtagged_0p81'
	nttagCut=''
	if 'p' in nttag: nttagCut+=' && '+nttagLJMETname+'>='+nttag[:-1]
	else: nttagCut+=' && '+nttagLJMETname+'=='+nttag
	if nttag=='0p': nttagCut=''
	
	nWtagLJMETname = 'NJetsWtagged_0p6'
        nWtagCut=''
	if '0p' in nWtag: nWtagCut += ' && (('+nWtagLJMETname+' > 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut'])+') || ('+nWtagLJMETname+' == 0 && NJets_JetSubCalc >= '+str(cutList['njetsCut']+1)+'))'
	elif 'p' in nWtag: nWtagCut+=' && '+nWtagLJMETname+'>='+nWtag[:-1]+' && NJets_JetSubCalc >='+ str(cutList['njetsCut'])
	else: nWtagCut+=' && '+nWtagLJMETname+'=='+nWtag +' && NJets_JetSubCalc >=' +str(cutList['njetsCut']+1)
	
	nbtagLJMETname = 'NJetsCSVwithSF_JetSubCalc'
	nbtagCut=''
	if 'p' in nbtag: nbtagCut+=' && '+nbtagLJMETname+'>='+nbtag[:-1]
	else: nbtagCut+=' && '+nbtagLJMETname+'=='+nbtag
	
	if nbtag=='0' and discriminantName=='minMlb': 
		originalLJMETName=discriminantLJMETName
		discriminantLJMETName='minMleppJet'
	
	print 'Flavour: '+isEM+' #ttags: '+nttag+' #Wtags: '+nWtag+' #btags: '+nbtag
	print 'discriminantLJMETName: '+discriminantLJMETName
	print 'Cuts: '+cut+isEMCut+nttagCut+nWtagCut+nbtagCut
	
	tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
	if doAllSys:
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'trigeffUp_'  +lumiStr+'fb_is'+catStr+'_'+process, weightTrigEffUpStr+'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'trigeffDown_'+lumiStr+'fb_is'+catStr+'_'+process, weightTrigEffDownStr+'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pileupUp'  +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightPileupUpStr  +'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pileupDown'+'_'+lumiStr+'fb_is'+catStr+'_'+process, weightPileupDownStr+'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRFcorrdUp'  +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightmuRFcorrdUpStr  +'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRFcorrdDown'+'_'+lumiStr+'fb_is'+catStr+'_'+process, weightmuRFcorrdDownStr+'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
      		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightmuRUpStr     +'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muRDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightmuRDownStr   +'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muFUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightmuFUpStr     +'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'muFDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightmuFDownStr   +'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'topptUp'   +'_'+lumiStr+'fb_is'+catStr+'_'+process, weighttopptUpStr   +'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'topptDown' +'_'+lumiStr+'fb_is'+catStr+'_'+process, weighttopptDownStr +'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'jsfUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightjsfUpStr     +'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'jsfDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightjsfDownStr   +'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		if discriminantLJMETName == 'minMleppBjet': discriminantLJMETName = discriminantLJMETName+'_shifts[0]'
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'btagUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut_btagUp+isEMCut+nttagCut+nWtagCut+nbtagCut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[0]')+')', 'GOFF')
		discriminantLJMETName = discriminantLJMETName.replace('_shifts[0]','_shifts[1]')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'btagDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut_btagDn+isEMCut+nttagCut+nWtagCut+nbtagCut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[1]')+')', 'GOFF')
		discriminantLJMETName = discriminantLJMETName.replace('_shifts[1]','_shifts[2]')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'mistagUp'     +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut_mistagUp+isEMCut+nttagCut+nWtagCut+nbtagCut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[2]')+')', 'GOFF')
		discriminantLJMETName = discriminantLJMETName.replace('_shifts[2]','_shifts[3]')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'mistagDown'   +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut_mistagDn+isEMCut+nttagCut+nWtagCut+nbtagCut.replace(nbtagLJMETname,nbtagLJMETname+'_shifts[3]')+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'tau21Up'   +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut+isEMCut+nttagCut+nWtagCut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[0]')+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'tau21Down' +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut+isEMCut+nttagCut+nWtagCut.replace(nWtagLJMETname,nWtagLJMETname+'_shifts[1]')+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'topsfUp'  +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr  +'*('+cut+isEMCut+nttagCut.replace(nttagLJMETname,nttagLJMETname+'_shifts[0]')+nWtagCut+nbtagCut+')', 'GOFF')
		tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'topsfDown'+'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut+isEMCut+nttagCut.replace(nttagLJMETname,nttagLJMETname+'_shifts[1]')+nWtagCut+nbtagCut+')', 'GOFF')
		if tTree[process+'jerUp']:
			tTree[process+'jerUp'].Draw(discriminantLJMETName   +' >> '+discriminantName+'jerUp'   +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
			tTree[process+'jerDown'].Draw(discriminantLJMETName +' >> '+discriminantName+'jerDown' +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		if tTree[process+'jecUp']:
			tTree[process+'jecUp'].Draw(discriminantLJMETName   +' >> '+discriminantName+'jecUp'   +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
			tTree[process+'jecDown'].Draw(discriminantLJMETName +' >> '+discriminantName+'jecDown' +'_'+lumiStr+'fb_is'+catStr+'_'+process, weightStr+'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
		for i in range(100): tTree[process].Draw(discriminantLJMETName+' >> '+discriminantName+'pdf'+str(i)+'_'+lumiStr+'fb_is'+catStr+'_'+process, 'pdfWeights['+str(i)+'] * '+weightStr+'*('+cut+isEMCut+nttagCut+nWtagCut+nbtagCut+')', 'GOFF')
	for key in hists.keys(): hists[key].SetDirectory(0)	
	return hists

