#!/usr/bin/python

import os,sys,time,math,pickle
from ROOT import *
from weights import *

gROOT.SetBatch(1)
start_time = time.time()

lumi=2.3 #for plots

templateDir=os.getcwd()+'/kinematics_substructure'
lumiInTemplates='2p263'

sig='ttm800' # choose the 1st signal to plot
sigleg='TT(0.8 TeV)'
scaleSignals = True

scaleFact1 = 400
if 'Final' in templateDir: scaleFact1 = 40

systematicList = ['pileup','jec','jer','jsf','jmr','jms','btag','tau21','pdfNew','muRFcorrdNew','toppt']
doAllSys = True
doQ2sys = True
if not doAllSys: doQ2sys = False # I assume you don't want Q^2 as well if you are not doing the other shape systematics! (this is just to change one bool)

isRebinned=''#post fix for file names if the name changed b/c of rebinning or some other process
doNormByBinWidth=False # not tested, may not work out of the box
doOneBand = False
if not doAllSys: doOneBand = True # Don't change this!
blind = False
yLog = True

doRealPull = False
if doRealPull: doOneBand=False

totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}

def formatUpperHist(histogram):
	histogram.GetXaxis().SetLabelSize(0)
	if blind == True:
		histogram.GetXaxis().SetLabelSize(0.08)
		histogram.GetXaxis().SetTitleSize(0.08)
		#histogram.GetXaxis().SetTitle(xTitle)
		histogram.GetYaxis().SetLabelSize(0.08)
		histogram.GetYaxis().SetTitleSize(0.08)
		histogram.GetYaxis().SetTitleOffset(1.2)
		histogram.GetXaxis().SetNdivisions(506)
	else:
		histogram.GetYaxis().SetLabelSize(0.07)
		histogram.GetYaxis().SetTitleSize(0.08)
		histogram.GetYaxis().SetTitleOffset(.71)

	if 'JetPt' in histogram.GetName() or 'JetEta' in histogram.GetName() or 'JetPhi' in histogram.GetName() or 'Pruned' in histogram.GetName() or 'Tau' in histogram.GetName(): histogram.GetYaxis().SetTitle("Jets")
	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.001)
	if not yLog: 
		histogram.SetMinimum(0.25)
	if yLog:
		uPad.SetLogy()
		histogram.SetMinimum(0.1)
		if not doNormByBinWidth: histogram.SetMaximum(100*histogram.GetMaximum())
		
def formatLowerHist(histogram):
	histogram.GetXaxis().SetLabelSize(.12)
	histogram.GetXaxis().SetTitleSize(0.15)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetXaxis().SetNdivisions(506)
	#histogram.GetXaxis().SetTitle("S_{T} (GeV)")

	histogram.GetYaxis().SetLabelSize(0.12)
	histogram.GetYaxis().SetTitleSize(0.14)
	histogram.GetYaxis().SetTitleOffset(.37)
	histogram.GetYaxis().SetTitle('Data/Bkg')
	histogram.GetYaxis().SetNdivisions(5)
	if doRealPull: histogram.GetYaxis().SetRangeUser(min(-2.99,0.8*histogram.GetBinContent(histogram.GetMaximumBin())),max(2.99,1.2*histogram.GetBinContent(histogram.GetMaximumBin())))
#	else: histogram.GetYaxis().SetRangeUser(0,1.99)
	else: histogram.GetYaxis().SetRangeUser(0,2.99)
	histogram.GetYaxis().CenterTitle()

def normByBinWidth(result):
	result.SetBinContent(0,0)
	result.SetBinContent(result.GetNbinsX()+1,0)
	result.SetBinError(0,0)
	result.SetBinError(result.GetNbinsX()+1,0)
	
	for bin in range(1,result.GetNbinsX()+1):
		width=result.GetBinWidth(bin)
		content=result.GetBinContent(bin)
		error=result.GetBinError(bin)
		
		result.SetBinContent(bin, content/width)
		result.SetBinError(bin, error/width)

lumiSys = 0.046 #4.6% lumi uncertainty
trigSys = 0.03 #3% trigger uncertainty
lepIdSys = 0.01 #1% lepton id uncertainty
lepIsoSys = 0.01 #1% lepton isolation uncertainty
topXsecSys = 0.0 #55 #5.5% top x-sec uncertainty
ewkXsecSys = 0.0 #5 #5% ewk x-sec uncertainty
qcdXsecSys = 0.0 #50 #50% qcd x-sec uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2)

def addSystematicUncertainties(hist,modelingUnc):
	for ibin in range(1,hist.GetNbinsX()+1):
		contentsquared = hist.GetBinContent(ibin)**2
		error = hist.GetBinError(ibin)**2 #statistical uncertainty
		error += corrdSys*corrdSys*contentsquared  #correlated uncertainties
		error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
		if 'top' in hist.GetName(): error += topXsecSys*topXsecSys*contentsquared # cross section
		if 'ewk' in hist.GetName(): error += ewkXsecSys*ewkXsecSys*contentsquared # cross section
		if 'qcd' in hist.GetName(): error += qcdXsecSys*qcdXsecSys*contentsquared # cross section

def getNormUnc(hist,ibin,modelingUnc):
	contentsquared = hist.GetBinContent(ibin)**2
	error = corrdSys*corrdSys*contentsquared  #correlated uncertainties
	error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
	if 'top' in hist.GetName(): error += topXsecSys*topXsecSys*contentsquared # cross section
	if 'ewk' in hist.GetName(): error += ewkXsecSys*ewkXsecSys*contentsquared # cross section
	if 'qcd' in hist.GetName(): error += qcdXsecSys*qcdXsecSys*contentsquared # cross section
	return error	
		
CRuncert = {# for finalselection with no DR or minMlb cut
	'topE':0.112, #212, #0.12,#0.129, #
	'topM':0.087, #0.133, #0.077,#0.163,#
	'topAll':0.098, #0.168, #0.096,#0.14,#
	'ewkE':0.260, #0.43, #0.25,#0.207,#
	'ewkM':0.104, #0.026, #0.045,#0.257,#
	'ewkAll':0.172, #0.202, #0.13,#0.24,#
	}

plotList = [#distribution name as defined in "doHists.py"
#	'deltaRb1Nonb',
#	'deltaRb2Nonb',
#	'deltaRWNonb',
#	'deltaEtab1Nonb',
#	'deltaEtab2Nonb',
#	'deltaEtaWNonb',
#	'deltaPhib1Nonb',
#	'deltaPhib2Nonb',
#	'deltaPhiWNonb',
#	'TTbarPtBalance',

#	'JetPtBins',
#	'deltaRAK8',
#	'NPV',
#	'lepPt',
#	'lepEta',
#	'JetEta',
#	'JetPt' ,
#	'Jet1Pt',
#	'Jet2Pt',
#	'Jet3Pt',
#	'Jet4Pt',
#	'HT',
#	'ST',
#	'MET',
#	'METwJetSF',
#	'METwJetSFraw',
#	'NJets' ,
#	'NBJets',
	'NWJetsSmeared',
	'NWJetsSmeared0p55SF',
	'NWJetsSmeared0p55noSF',
#	'NJetsAK8',
#	'JetPtAK8',
#	'JetEtaAK8',
	'Tau21',
	'Tau21Nm1',
	'PrunedSmeared',
#	'mindeltaR',
#	'deltaRjet1',
#	'deltaRjet2',
#	'deltaRjet3',
#	'minMlb',
#	'METphi',
#	'lepPhi',
#	'lepDxy',
#	'lepDz',
#	'lepCharge',
#	'lepIso',
#	'Tau1',
#	'Tau2',
#	'JetPhi',
#	'JetPhiAK8',
#	'Bjet1Pt',
#	'Wjet1Pt',
#	'topMass',
#	'topPt',
#	'minMlj',
#	'minMljDR',
#	'minMlbDR',
#	'minMljDPhi',
#	'minMlbDPhi',
#	'nonMinMlbDR',
#	'MWb1',
#	'MWb2',
#	'HT4jets',
#	'deltaRlb1',
#	'deltaRlb2',
#	'deltaRtW',
#	'deltaRlW',
#	'deltaRWb1',
#	'deltaRWb2',
#	'deltaPhilb1',
#	'deltaPhilb2',
#	'deltaPhitW',
#	'deltaPhilW',
#	'deltaPhiWb1',
#	'deltaPhiWb2',
#	'WjetPt',
	'PtRel',

#	'JetPt',
#	'JetPtCSF',
#	'JetPtNSF',
#	'Jet1Pt',
#	'Jet2Pt',
#	'Jet2Pt',
#	'Jet3Pt',
#	'Jet4Pt',
#	'Jet5Pt',
#	'Jet6Pt',
#	'Jet1PtCSF',
#	'Jet2PtCSF',
#	'Jet3PtCSF',
#	'Jet4PtCSF',
#	'Jet5PtCSF',
#	'Jet6PtCSF',
#	'Jet1PtNSF',
#	'Jet2PtNSF',
#	'Jet3PtNSF',
#	'Jet4PtNSF',
#	'Jet5PtNSF',
#	'Jet6PtNSF',
#	'HT',
#	'HTCSF',
#	'HTNSF',
#	'ST',
#	'STCSF',
#	'STNSF',
#	'NJets',
#	'NJetsCSF',
#	'NJetsNSF',
#	'NBJets',
#	'NBJetsCSF',
#	'NBJetsNSF',
#	'NJetsAK8',
#	'NJetsAK8CSF',
#	'JetPtAK8',
#	'JetPtAK8CSF',
	]

fit  = False
fit2 = False
fit3 = False
fit4 = False
isEMlist=['E','M','All']
for discriminant in plotList:	
	fileTemp='templates_'+discriminant+'_'+lumiInTemplates+'fb'+isRebinned+'.root'
	print templateDir+'/'+fileTemp
	if not os.path.exists(templateDir+'/'+fileTemp): 
		print 'not found, skipping'
		continue
	RFile = TFile(templateDir+'/'+fileTemp)

	systHists={}
	for isEM in isEMlist:
		histPrefix=discriminant+'_'+lumiInTemplates+'fb_'+isEM
		
		hTOP = RFile.Get(histPrefix+'__top').Clone()
		try: hEWK = RFile.Get(histPrefix+'__ewk').Clone()
		except: 
			print "There is no EWK!!!!!!!!"
			print "Skipping EWK....."
			pass
		try: hQCD = RFile.Get(histPrefix+'__qcd').Clone()
		except: 
			print "There is no QCD!!!!!!!!"
			print "Skipping QCD....."
			pass
		
		print discriminant,isEM, "TOP", hTOP.Integral()
		print discriminant,isEM, "EWK", hEWK.Integral()
		try: print discriminant,isEM, "QCD", hQCD.Integral()
		except: pass
		
		hData = RFile.Get(histPrefix+'__DATA').Clone()
		hsig1 = RFile.Get(histPrefix+'__'+sig+'bwbw').Clone()
		hsig2 = RFile.Get(histPrefix+'__'+sig+'tztz').Clone()
		hsig3 = RFile.Get(histPrefix+'__'+sig+'thth').Clone()

		hsig = RFile.Get(histPrefix+'__'+sig+'bwbw').Clone(histPrefix+'__'+sig+'nominal')
		decays = ['tztz','thth','tzbw','thbw','tzth']
		for decay in decays:
			htemp = RFile.Get(histPrefix+'__'+sig+decay).Clone()
			hsig.Add(htemp)

		# original scale = lumi * xsec * BR(50/25/25) / N(33/33/33)
		hsig1.Scale(1.0/BR['TTBWBW'])
		hsig2.Scale(1.0/BR['TTTZTZ'])
		hsig3.Scale(1.0/BR['TTTHTH'])
		if doNormByBinWidth:
			normByBinWidth(hTOP)
			normByBinWidth(hEWK)
			normByBinWidth(hQCD)
			normByBinWidth(hsig1)
			normByBinWidth(hsig2)
			normByBinWidth(hData)
		
		if doAllSys:
			for sys in systematicList:
				for ud in ['minus','plus']:
					systHists['top'+sys+ud] = RFile.Get(histPrefix+'__top__'+sys+'__'+ud).Clone()
					try: systHists['ewk'+sys+ud] = RFile.Get(histPrefix+'__ewk__'+sys+'__'+ud).Clone()
					except: pass
					try: systHists['qcd'+sys+ud] = RFile.Get(histPrefix+'__qcd__'+sys+'__'+ud).Clone()
					except: pass
		if doQ2sys:
			for ud in ['minus','plus']:
				systHists['topq2'+ud] = RFile.Get(histPrefix+'__top__q2__'+ud).Clone()
				systHists['q2'+ud] = systHists['topq2'+ud].Clone()
				systHists['ewkq2'+ud] = RFile.Get(histPrefix+'__ewk').Clone()
				systHists['q2'+ud].Add(systHists['ewkq2'+ud])
				try:
					systHists['qcdq2'+ud] = RFile.Get(histPrefix+'__qcd').Clone()
					systHists['q2'+ud].Add(systHists['qcdq2'+ud])
				except: pass

		hTOPstatOnly = hTOP.Clone(hTOP.GetName()+'statOnly')
		try: hEWKstatOnly= hEWK.Clone(hEWK.GetName()+'statOnly')
		except: pass
		try: hQCDstatOnly = hQCD.Clone(hQCD.GetName()+'statOnly')
		except: pass

		bkgHT = hTOP.Clone()
		try: bkgHT.Add(hEWK)
		except: pass
		try: bkgHT.Add(hQCD)
		except: pass

		totBkgTemp1[isEM] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
		totBkgTemp2[isEM] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
		totBkgTemp3[isEM] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))
			
		for ibin in range(1,hTOP.GetNbinsX()+1):
			errorUp = 0.
			errorDn = 0.
			errorSym = 0.

			errorStatOnly = bkgHT.GetBinError(ibin)**2
			errorCheck = hTOP.GetBinError(ibin)**2 + hEWK.GetBinError(ibin)**2
			try: errorCheck += hQCD.GetBinError(ibin)**2
			except: pass

			errorStatCheck = hTOPstatOnly.GetBinError(ibin)**2 + hEWKstatOnly.GetBinError(ibin)**2
			try: errorStatCheck += hQCDstatOnly.GetBinError(ibin)**2
			except: pass

			errorNorm = getNormUnc(hTOPstatOnly,ibin,CRuncert['top'+isEM])
			try: errorNorm += getNormUnc(hEWKstatOnly,ibin,CRuncert['ewk'+isEM])
			except: pass
			try: errorNorm += getNormUnc(hQCDstatOnly,ibin,0.0)
			except: pass

			for sys in systematicList:
				if doAllSys:	
					errorSym += (0.5*abs(systHists['top'+sys+'plus'].GetBinContent(ibin)-systHists['top'+sys+'minus'].GetBinContent(ibin)))**2				
					errorPlus = systHists['top'+sys+'plus'].GetBinContent(ibin)-hTOP.GetBinContent(ibin)
					errorMinus = hTOP.GetBinContent(ibin)-systHists['top'+sys+'minus'].GetBinContent(ibin)
					if errorPlus > 0: errorUp += errorPlus**2
					else: errorDn += errorPlus**2
					if errorMinus > 0: errorDn += errorMinus**2
					else: errorUp += errorMinus**2
					if sys!='toppt':
						try:
							errorSym += (0.5*abs(systHists['ewk'+sys+'plus'].GetBinContent(ibin)-systHists['ewk'+sys+'minus'].GetBinContent(ibin)))**2				
							errorPlus = systHists['ewk'+sys+'plus'].GetBinContent(ibin)-hEWK.GetBinContent(ibin)
							errorMinus = hEWK.GetBinContent(ibin)-systHists['ewk'+sys+'minus'].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass
						try:
							errorSym += (0.5*abs(systHists['qcd'+sys+'plus'].GetBinContent(ibin)-systHists['qcd'+sys+'minus'].GetBinContent(ibin)))**2				
							errorPlus = systHists['qcd'+sys+'plus'].GetBinContent(ibin)-hQCD.GetBinContent(ibin)
							errorMinus = hQCD.GetBinContent(ibin)-systHists['qcd'+sys+'minus'].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass													
			if doQ2sys: 
				errorSym += (0.5*abs(systHists['topq2plus'].GetBinContent(ibin)-systHists['topq2minus'].GetBinContent(ibin)))**2				
				errorPlus = systHists['topq2plus'].GetBinContent(ibin)-hTOP.GetBinContent(ibin)
				errorMinus = hTOP.GetBinContent(ibin)-systHists['topq2minus'].GetBinContent(ibin)
				if errorPlus > 0: errorUp += errorPlus**2
				else: errorDn += errorPlus**2
				if errorMinus > 0: errorDn += errorMinus**2
				else: errorUp += errorMinus**2

			totBkgTemp1[isEM].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
			totBkgTemp1[isEM].SetPointEYlow(ibin-1,math.sqrt(errorDn))
			totBkgTemp2[isEM].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
			totBkgTemp2[isEM].SetPointEYlow(ibin-1,math.sqrt(errorDn+errorNorm))
			totBkgTemp3[isEM].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
			totBkgTemp3[isEM].SetPointEYlow(ibin-1,math.sqrt(errorDn+errorNorm+errorStatOnly))
			
		bkgHTgerr = totBkgTemp3[isEM].Clone()

		'''
		scaleFact1 = int(bkgHT.GetMaximum()/hsig1.GetMaximum()) - int(bkgHT.GetMaximum()/hsig1.GetMaximum()) % 10
		scaleFact1 *= 0.60
		if scaleFact1==0: scaleFact1=int(bkgHT.GetMaximum()/hsig1.GetMaximum())
		if scaleFact1==0: scaleFact1=1
		if not scaleSignals:
			scaleFact1=1
 		#else:
 		#	scaleFact1=25
                '''
		hsig1.Scale(scaleFact1)
		hsig2.Scale(scaleFact1)
		hsig3.Scale(scaleFact1)
		hsig.Scale(scaleFact1)
		
		stackbkgHT = THStack("stackbkgHT","")
		try: stackbkgHT.Add(hTOP)
		except: pass
		try: stackbkgHT.Add(hEWK)
		except: pass
		try: 
			if hQCD.Integral()/bkgHT.Integral()>.005: stackbkgHT.Add(hQCD) #don't plot QCD if it is less than 0.5%
		except: pass

		hTOP.SetLineColor(kAzure-6)
		hTOP.SetFillColor(kAzure-6)
		hTOP.SetLineWidth(2)
		try: 
			hEWK.SetLineColor(kMagenta-2)
			hEWK.SetFillColor(kMagenta-2)
			hEWK.SetLineWidth(2)
		except: pass
		try:
			hQCD.SetLineColor(kOrange+5)
			hQCD.SetFillColor(kOrange+5)
			hQCD.SetLineWidth(2)
		except: pass
		
		hsig.SetLineColor(kBlack)
		hsig.SetLineWidth(3)
		hsig1.SetLineColor(kRed)
		hsig1.SetLineStyle(2)
		hsig1.SetLineWidth(3)
		hsig2.SetLineColor(kOrange-2)
		hsig2.SetLineStyle(5)
		hsig2.SetLineWidth(3)
		hsig3.SetLineColor(kGreen+1)
		hsig3.SetLineStyle(7)
		hsig3.SetLineWidth(3)
		
		hData.SetMarkerStyle(20)
		hData.SetMarkerSize(1.2)
		hData.SetLineWidth(2)

		bkgHTgerr.SetFillStyle(3004)
		bkgHTgerr.SetFillColor(kBlack)

		gStyle.SetOptStat(0)
		c1 = TCanvas("c1","c1",1200,1000)
		gStyle.SetErrorX(0.5)
		yDiv=0.35
		if blind == True: yDiv=0.1
		uMargin = 0
		if blind == True: uMargin = 0.15
		rMargin=.04
		uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
		uPad.SetTopMargin(0.10)
		uPad.SetBottomMargin(uMargin)
		uPad.SetRightMargin(rMargin)
		uPad.SetLeftMargin(.12)
		uPad.Draw()
		if blind == False:
			lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
			lPad.SetTopMargin(0)
			lPad.SetBottomMargin(.4)
			lPad.SetRightMargin(rMargin)
			lPad.SetLeftMargin(.12)
			lPad.SetGridy()
			lPad.Draw()
		if not doNormByBinWidth: hData.SetMaximum(1.2*max(hData.GetMaximum(),bkgHT.GetMaximum()))
		hData.SetMinimum(0.015)
		hData.SetTitle("")
		if doNormByBinWidth: hData.GetYaxis().SetTitle("Events / 1 GeV")
		else: hData.GetYaxis().SetTitle("Events")
		formatUpperHist(hData)
		uPad.cd()
		hData.SetTitle("")
		if not blind: hData.Draw("E1 X0")
		if blind: 

			hsig1.SetMinimum(0.015)
			if doNormByBinWidth: hsig1.GetYaxis().SetTitle("Events / 1 GeV")
			else: hsig1.GetYaxis().SetTitle("Events")
			formatUpperHist(hsig1)
			hsig1.SetMaximum(hData.GetMaximum())
			hsig1.Draw("HIST")

		stackbkgHT.Draw("SAME HIST")
		hsig.Draw("SAME HIST")
		hsig1.Draw("SAME HIST")
		hsig2.Draw("SAME HIST")
		hsig3.Draw("SAME HIST")
		if not blind: hData.Draw("SAME E1 X0") #redraw data so its not hidden
		uPad.RedrawAxis()
		bkgHTgerr.Draw("SAME E2")

		leg = {}
		if 'Tau21' in discriminant:
			leg = TLegend(0.15,0.53,0.45,0.90)
		elif 'Eta' in discriminant or 'deltaRjet2' in discriminant:
			leg = TLegend(0.72,0.43,0.95,0.90)
		else:
			leg = TLegend(0.65,0.53,0.95,0.90)
		leg.SetShadowColor(0)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetLineColor(0)
		leg.SetLineStyle(0)
		leg.SetBorderSize(0) 
		leg.SetTextFont(42)
		if not blind: leg.AddEntry(hData,"DATA")
		
		scaleFact1Str = ' x'+str(scaleFact1)
		if not scaleSignals:
			scaleFact1Str = ''
		
		leg.AddEntry(hsig,sigleg+' nominal BRs'+scaleFact1Str,"l")
		leg.AddEntry(hsig1,sigleg+' #rightarrow bWbW'+scaleFact1Str,"l")
		leg.AddEntry(hsig2,sigleg+' #rightarrow tZtZ'+scaleFact1Str,"l")
		leg.AddEntry(hsig3,sigleg+' #rightarrow tHtH'+scaleFact1Str,"l")
		try: 
			if hQCD.Integral()/bkgHT.Integral()>.005: leg.AddEntry(hQCD,"QCD","f") #don't plot QCD if it is less than 0.5%
		except: pass
		try: leg.AddEntry(hEWK,"EWK","f")
		except: pass
		try: leg.AddEntry(hTOP,"TOP","f")
		except: pass
		leg.AddEntry(bkgHTgerr,"Bkg uncert. (stat. #oplus syst.)","f")
		leg.Draw("same")

		prelimTex=TLatex()
		prelimTex.SetNDC()
		prelimTex.SetTextAlign(31) # align right
		prelimTex.SetTextFont(42)
		prelimTex.SetTextSize(0.07)
		prelimTex.SetLineWidth(2)
		prelimTex.DrawLatex(0.95,0.92,str(lumi)+" fb^{-1} (13 TeV)")

		prelimTex2=TLatex()
		prelimTex2.SetNDC()
		prelimTex2.SetTextFont(61)
		prelimTex2.SetLineWidth(2)
		prelimTex2.SetTextSize(0.10)
		prelimTex2.DrawLatex(0.12,0.92,"CMS")

		prelimTex3=TLatex()
		prelimTex3.SetNDC()
		prelimTex3.SetTextAlign(13)
		prelimTex3.SetTextFont(52)
		prelimTex3.SetTextSize(0.075)
		prelimTex3.SetLineWidth(2)
		if not blind: prelimTex3.DrawLatex(0.24,0.975,"Preliminary")
		if blind: prelimTex3.DrawLatex(0.29175,0.9364,"Preliminary")

		flat = TF1("flat","pol1",30,250);

		line = TF1("line","pol1",250,1500);
		line2 = TF1("line2","pol1",30,1500);
		line3 = TF1("line3","pol1",30,1500);
		line4 = TF1("line4","pol1",30,1500);

		line.SetLineWidth(2);

		para = TF1("para","pol2",30,1500); para.SetLineColor(kBlue);
		para2 = TF1("para2","pol2",30,1500); para2.SetLineColor(kBlue);
		para3 = TF1("para3","pol2",30,1500); para3.SetLineColor(kBlue);

		cube = TF1("cube","pol3",30,1500); cube.SetLineColor(kGreen);
		cube2 = TF1("cube2","pol3",30,1500); cube2.SetLineColor(kGreen);
		cube3 = TF1("cube3","pol3",30,1500); cube3.SetLineColor(kGreen);

		if blind == False and not doRealPull:
			lPad.cd()
			pull=hData.Clone("pull")
#			pull.Scale(1.0/pull.Integral())
#			pullDenom = bkgHT.Clone("pullDenom")
#			pullDenom.Scale(1.0/pullDenom.Integral())
#			pull.Divide(pullDenom)
			pull.Divide(hData, bkgHT)

			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pull.SetBinError(binNo,hData.GetBinError(binNo)/bkgHT.GetBinContent(binNo))
			pull.SetMaximum(3)
			pull.SetMinimum(0)
			pull.SetFillColor(1)
			pull.SetLineColor(1)
			formatLowerHist(pull)
			if fit:
#				pull.Fit("flat","R")
#				fitresult = pull.Fit("line","RS")
#				cov = fitresult.GetCovarianceMatrix()
#				p0p0cov = cov(0,0)
#				p0p1cov = cov(0,1)
#				p1p1cov = cov(1,1)
#				print 'covariance p0-p0 =',p0p0cov
#				print 'covariance p0-p1 =',p0p1cov
#				print 'covariance p1-p1 =',p1p1cov
				'''
				****************************************
				Minimizer is Linear
				Chi2                      =      9.97134
				NDf                       =            9
				p0                        =      1.09771   +/-   0.0384644   
				p1                        = -0.000517529   +/-   9.94895e-05 
				covariance p0-p0 = 0.0014795109823
				covariance p0-p1 = -3.6104869696e-06
				covariance p1-p1 = 9.89815635815e-09
				******************************
				'''				
				jsf = TF1("jsf","1.09771 - 0.000517529*x",200,1500)
				jsfup = TF1("jsfup","1.09771 - 0.000517529*x + sqrt(0.0014795109823 + x*x*9.89815635815e-09 - 2*x*3.6104869696e-06)",200,1500)
				jsfdn = TF1("jsfdn","1.09771 - 0.000517529*x - sqrt(0.0014795109823 + x*x*9.89815635815e-09 - 2*x*3.6104869696e-06)",200,1500)

				print 'JSFup at 250:',jsfup.Eval(250)
				
				jsf.SetLineColor(kRed)
				jsf.SetLineWidth(2)
				jsfup.SetLineColor(kBlue)
				jsfdn.SetLineColor(kBlue)
				jsfup.SetLineWidth(2)
				jsfdn.SetLineWidth(2)
#				pull.Fit("para","R+")
#				pull.Fit("cube","R+")
#				pull.Draw("E1 same")
				pull.Draw("E1 same")
				jsf.Draw("same")
				jsfup.Draw("same")
				jsfdn.Draw("same")
			elif fit2:
				pull.Fit("line2","R")
#				pull.Fit("para2","R+")
#				pull.Fit("cube2","R+")
				pull.Draw("E1 same")
			elif fit3:
				pull.Fit("line3","R")
#				pull.Fit("para3","R+")
#				pull.Fit("cube3","R+")
				pull.Draw("E1 same")
			elif fit4:
				pull.Fit("line4","R")
				pull.Draw("E1 same")
			else:
				pull.Draw("E1")

			if 'Bins' in discriminant:
				print '******************************'
				print 'Data/MC for',discriminant
				for binNo in range(0,pull.GetNbinsX()+2):
					print 'Bin',binNo,': content =',pull.GetBinContent(binNo),'; error =',pull.GetBinError(binNo),';'
		
			BkgOverBkg = pull.Clone("bkgOverbkg")
			BkgOverBkg.Divide(bkgHT, bkgHT)
			pullUncBandTot=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandTot.SetPointEYhigh(binNo-1,totBkgTemp3[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandTot.SetPointEYlow(binNo-1,totBkgTemp3[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			if not doOneBand: pullUncBandTot.SetFillStyle(3001)
			else: pullUncBandTot.SetFillStyle(3344)
			pullUncBandTot.SetFillColor(1)
			pullUncBandTot.SetLineColor(1)
			pullUncBandTot.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			pullUncBandTot.Draw("SAME E2")
				
			pullUncBandNorm=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncNorm"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandNorm.SetPointEYhigh(binNo-1,totBkgTemp2[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandNorm.SetPointEYlow(binNo-1,totBkgTemp2[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandNorm.SetFillStyle(3001)
			pullUncBandNorm.SetFillColor(2)
			pullUncBandNorm.SetLineColor(2)
			pullUncBandNorm.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandNorm.Draw("SAME E2")
			
			pullUncBandStat=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncStat"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandStat.SetPointEYhigh(binNo-1,totBkgTemp1[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandStat.SetPointEYlow(binNo-1,totBkgTemp1[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandStat.SetFillStyle(3001)
			pullUncBandStat.SetFillColor(3)
			pullUncBandStat.SetLineColor(3)
			pullUncBandStat.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandStat.Draw("SAME E2")
		
			if doQ2sys:
				pullQ2up=systHists['q2plus'].Clone("pullQ2Up")
				pullQ2up.Divide(systHists['q2plus'], bkgHT)
				pullQ2up.SetFillColor(0)
				pullQ2up.SetLineColor(6)#kGreen+1)
				pullQ2up.SetLineWidth(3)
				#pullQ2up.Draw("SAME HIST")
		
				pullQ2dn=systHists['q2minus'].Clone("pullQ2Dn")
				pullQ2dn.Divide(systHists['q2minus'], bkgHT)
				pullQ2dn.SetFillColor(0)
				pullQ2dn.SetLineColor(6)#kGreen+1)
				pullQ2dn.SetLineWidth(3)
				pullQ2dn.SetLineStyle(5)
				#pullQ2dn.Draw("SAME HIST")

			pullLegend=TLegend(0.14,0.87,0.85,0.96)
			SetOwnership( pullLegend, 0 )   # 0 = release (not keep), 1 = keep
			pullLegend.SetShadowColor(0)
			pullLegend.SetNColumns(3)
			pullLegend.SetFillColor(0)
			pullLegend.SetFillStyle(0)
			pullLegend.SetLineColor(0)
			pullLegend.SetLineStyle(0)
			pullLegend.SetBorderSize(0)
			pullLegend.SetTextFont(42)
			if not doOneBand: pullLegend.AddEntry(pullUncBandStat , "Bkg shape syst." , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandNorm , "Bkg shape #oplus norm. syst." , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandTot , "Bkg stat. #oplus all syst." , "f")
#			else: pullLegend.AddEntry(pullUncBandTot , "Bkg stat. #oplus syst." , "f")
			else: 
				pullLegend.AddEntry(pullUncBandTot , "Bkg stat." , "f")
			#	pullLegend.AddEntry(jsf, "Fit","l")
			#	pullLegend.AddEntry(jsfup, "#pm 1#sigma","l")
			#pullLegend.AddEntry(pullQ2up , "Q^{2} Up" , "l")
			#pullLegend.AddEntry(pullQ2dn , "Q^{2} Down" , "l")
			pullLegend.Draw("SAME")
			pull.Draw("SAME")
			lPad.RedrawAxis()

		if blind == False and doRealPull:
			lPad.cd()
			pull=hData.Clone("pull")
			for binNo in range(0,hData.GetNbinsX()+2):
				if hData.GetBinContent(binNo)!=0:
					MCerror = 0.5*(totBkgTemp3[isEM].GetErrorYhigh(binNo-1)+totBkgTemp3[isEM].GetErrorYlow(binNo-1))
					pull.SetBinContent(binNo,(hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(MCerror**2+hData.GetBinError(binNo)**2))
					#pull.SetBinContent(binNo,(hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(bkgHT.GetBinError(binNo)**2+hData.GetBinError(binNo)**2))
				else: pull.SetBinContent(binNo,0.)
			pull.SetMaximum(3)
			pull.SetMinimum(-3)
			pull.SetFillColor(2)
			pull.SetLineColor(2)
			formatLowerHist(pull)
			pull.GetYaxis().SetTitle('Pull')
			pull.Draw("HIST")

		#c1.Write()
		savePrefix = templateDir.split('/')[-1]+'/plots/'
		if not os.path.exists(os.getcwd()+'/'+savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix+isRebinned
		if doRealPull: savePrefix+='_pull'
		if yLog: savePrefix+='_logy'

		if doOneBand:
			c1.SaveAs(savePrefix+"_totBand.pdf")
			c1.SaveAs(savePrefix+"_totBand.png")
			c1.SaveAs(savePrefix+"_totBand.root")
			#c1.SaveAs(savePrefix+"totBand.C")
		else:
			c1.SaveAs(savePrefix+".pdf")
			c1.SaveAs(savePrefix+".png")
			c1.SaveAs(savePrefix+".root")
			#c1.SaveAs(savePrefix+".C")
			
	RFile.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


