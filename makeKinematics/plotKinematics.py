#!/usr/bin/python

import os,sys,time,math,pickle
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as R
from weights import *
from utils import *

R.gROOT.SetBatch(1)
#R.TGaxis.SetMaxDigits(3)
start_time = time.time()

lumi=2.3 #for plots

pfix='kinematics_preSel_noJSF_2016_10_9'
templateDir=os.getcwd()+'/'+pfix
lumiInTemplates='2p318'

sig1='X53X53M800' # choose the 1st signal to plot
sig1leg='X_{5/3}#bar{X}_{5/3} (LH-0.8 TeV)'
sig2='X53X53M1100' # choose the 2nd signal to plot
sig2leg='X_{5/3}#bar{X}_{5/3} (RH-1.1 TeV)'
scaleSignals = True

systematicList = ['pileup','toppt','jmr','jms','tau21','btag','mistag','jer','jec','q2','pdfNew','muRFcorrdNew','topsf']
if 'withJSF' in pfix:
	systematicList+= ['jsf']
doAllSys = True
doQ2sys  = True
if not doAllSys: doQ2sys = False # I assume you don't want Q^2 as well if you are not doing the other shape systematics! (this is just to change one bool)

isRebinned=''#post fix for file names if the name changed b/c of rebinning or some other process
doNormByBinWidth=False # not tested, may not work out of the box
doOneBand = False
if not doAllSys: doOneBand = True # Don't change this!
blind = False
yLog  = False

doRealPull = True
if doRealPull: doOneBand=False

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
		if stackbkgHT.GetMaximum()>1e4: histogram.GetYaxis().SetTitleOffset(.95)
		elif stackbkgHT.GetMaximum()>1e3: histogram.GetYaxis().SetTitleOffset(.81)
		else: histogram.GetYaxis().SetTitleOffset(.71)

	if 'JetPt' in histogram.GetName() or 'JetEta' in histogram.GetName() or 'JetPhi' in histogram.GetName() or 'Pruned' in histogram.GetName() or 'Tau' in histogram.GetName(): histogram.GetYaxis().SetTitle(histogram.GetYaxis().GetTitle().replace("Events","Jets"))
	if 'minMlb' in histogram.GetName(): histogram.GetXaxis().SetTitle("min[M(l,b)] (GeV)")
	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.00101)
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
	if stackbkgHT.GetMaximum()>1e4: 
		if doRealPull: histogram.GetYaxis().SetTitleOffset(.37)
		else: histogram.GetYaxis().SetTitleOffset(.52)

	elif stackbkgHT.GetMaximum()>1e3: 
		if doRealPull: histogram.GetYaxis().SetTitleOffset(.40)
		else: histogram.GetYaxis().SetTitleOffset(.45)

	else: 
		if doRealPull: histogram.GetYaxis().SetTitleOffset(.32)
		else: histogram.GetYaxis().SetTitleOffset(.37)
	histogram.GetYaxis().SetTitle('Data/Bkg')
	histogram.GetYaxis().SetNdivisions(5)
	if doRealPull: histogram.GetYaxis().SetRangeUser(min(-2.99,0.8*histogram.GetBinContent(histogram.GetMaximumBin())),max(2.99,1.2*histogram.GetBinContent(histogram.GetMaximumBin())))
#	else: histogram.GetYaxis().SetRangeUser(0,1.99)
	else: histogram.GetYaxis().SetRangeUser(0,2.99)
	histogram.GetYaxis().CenterTitle()

lumiSys = 0.027 # lumi uncertainty
trigSys = 0.05 # trigger uncertainty
lepIdSys = 0.01 # lepton id uncertainty
lepIsoSys = 0.01 # lepton isolation uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2)

modelingSys={#Inclusive WJets sample, NOT REWEIGHTED, 8OCT16--SS
			'topE':0.12,
			'topM':0.13,
			'topL':0.13,
			'ewkE':0.14,
			'ewkM':0.09,
			'ewkL':0.11,
			}

def getNormUnc(hist,ibin,modelingUnc):
	contentsquared = hist.GetBinContent(ibin)**2
	error = corrdSys*corrdSys*contentsquared  #correlated uncertainties
	error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
	return error	

plotList = [#distribution name as defined in "doHists.py"
		'NPV',
		'lepPt',
		'lepEta',
		'JetEta',
		'JetPt' ,
		'Jet1Pt',
		'Jet2Pt',
		'Jet3Pt',
		'Jet4Pt',
		'Jet5Pt',
		'Jet6Pt',
		'HT',
		'ST',
		'MET',
		'NJets' ,
		'NBJets',
		'NWJets',
		'NJetsAK8',
		'JetPtAK8',
		'JetEtaAK8',
		'Tau21',
		'Tau32',
		'mindeltaR',
		'deltaRjet1',
		'deltaRjet2',
		'deltaRjet3',
		'PtRel',
		'PrunedSmeared',
		'SDMass',
		'NTJets',
		'NTJetsSF',
		'minMlb',
		'minMlbDR',
		]

totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}
isEMlist=['E','M','L']
for discriminant in plotList:	
	fileTemp='kinematics_'+discriminant+'_'+lumiInTemplates+'fb'+isRebinned+'.root'
	print templateDir+'/'+fileTemp
	if not os.path.exists(templateDir+'/'+fileTemp): 
		print 'not found, skipping'
		continue
	RFile = R.TFile(templateDir+'/'+fileTemp)

	systHists={}
	
	for isEM in isEMlist:
		histPrefix=discriminant+'_'+lumiInTemplates+'fb_is'+isEM
		
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
		hsig1 = RFile.Get(histPrefix+'__'+sig1+'left').Clone()
		hsig2 = RFile.Get(histPrefix+'__'+sig2+'right').Clone()

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

		totBkgTemp1[isEM] = R.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
		totBkgTemp2[isEM] = R.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
		totBkgTemp3[isEM] = R.TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))
			
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

			errorNorm = getNormUnc(hTOPstatOnly,ibin,modelingSys['top'+isEM])
			try: errorNorm += getNormUnc(hEWKstatOnly,ibin,modelingSys['ewk'+isEM])
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

		scaleFact1 = int(bkgHT.GetMaximum()/hsig1.GetMaximum()) - int(bkgHT.GetMaximum()/hsig1.GetMaximum()) % 10
		scaleFact2 = int(bkgHT.GetMaximum()/hsig2.GetMaximum()) - int(bkgHT.GetMaximum()/hsig2.GetMaximum()) % 10
		if scaleFact1==0: scaleFact1=int(bkgHT.GetMaximum()/hsig1.GetMaximum())
		if scaleFact2==0: scaleFact2=int(bkgHT.GetMaximum()/hsig2.GetMaximum())
		if scaleFact1==0: scaleFact1=1
		if scaleFact2==0: scaleFact2=1
		if not scaleSignals:
			scaleFact1=1
 		#else:
 		#	scaleFact1=25

		hsig1.Scale(scaleFact1)
		hsig2.Scale(scaleFact2)
				
		stackbkgHT = R.THStack("stackbkgHT","")
		try: stackbkgHT.Add(hTOP)
		except: pass
		try: stackbkgHT.Add(hEWK)
		except: pass
		try: 
			if hQCD.Integral()/bkgHT.Integral()>.005: stackbkgHT.Add(hQCD) #don't plot QCD if it is less than 0.5%
		except: pass

		topColor = R.kAzure+8
		ewkColor = R.kMagenta-2
		qcdColor = R.kOrange+5
		sig1Color= R.kBlack
		sig2Color= R.kRed
		if '53' in sig1: 
			topColor = R.kRed-9
			ewkColor = R.kBlue-7
			qcdColor = R.kOrange-5
			sig1Color= R.kBlack
			sig2Color= R.kBlack
			
		hTOP.SetLineColor(topColor)
		hTOP.SetFillColor(topColor)
		hTOP.SetLineWidth(2)
		try: 
			hEWK.SetLineColor(ewkColor)
			hEWK.SetFillColor(ewkColor)
			hEWK.SetLineWidth(2)
		except: pass
		try:
			hQCD.SetLineColor(qcdColor)
			hQCD.SetFillColor(qcdColor)
			hQCD.SetLineWidth(2)
		except: pass
					
		hsig1.SetLineColor(sig1Color)
		hsig1.SetLineStyle(2)
		hsig1.SetLineWidth(3)
		hsig2.SetLineColor(sig2Color)
		hsig2.SetLineStyle(5)
		hsig2.SetLineWidth(3)
				
		hData.SetMarkerStyle(20)
		hData.SetMarkerSize(1.2)
		hData.SetLineWidth(2)

		bkgHTgerr.SetFillStyle(3004)
		bkgHTgerr.SetFillColor(R.kBlack)

		R.gStyle.SetOptStat(0)
		c1 = R.TCanvas("c1","c1",1200,1000)
		R.gStyle.SetErrorX(0.5)
		yDiv=0.35
		if blind == True: yDiv=0.1
		uMargin = 0
		if blind == True: uMargin = 0.15
		rMargin=.04
		lMargin=0.12
		if stackbkgHT.GetMaximum()>1e3: lMargin=0.14
		if stackbkgHT.GetMaximum()>1e4: lMargin=0.16
		uPad=R.TPad("uPad","",0,yDiv,1,1) #for actual plots
		uPad.SetTopMargin(0.10)
		uPad.SetBottomMargin(uMargin)
		uPad.SetRightMargin(rMargin)
		uPad.SetLeftMargin(lMargin)
		uPad.Draw()
		if blind == False:
			lPad=R.TPad("lPad","",0,0,1,yDiv) #for sigma runner
			lPad.SetTopMargin(0)
			lPad.SetBottomMargin(.4)
			lPad.SetRightMargin(rMargin)
			lPad.SetLeftMargin(lMargin)
			lPad.SetGridy()
			lPad.Draw()
		if not doNormByBinWidth: hData.SetMaximum(1.2*max(hData.GetMaximum(),bkgHT.GetMaximum()))
		hData.SetMinimum(0.015)
		hData.SetTitle("")
		if doNormByBinWidth: hData.GetYaxis().SetTitle("Events / 1 GeV")
		else: 
			binWidth = hData.GetBinWidth(1)
			hData.GetYaxis().SetTitle("Events / "+str(binWidth))
			if 'GeV' in hData.GetXaxis().GetTitle(): hData.GetYaxis().SetTitle("Events / "+str(binWidth)+" GeV")
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
		
		hsig1.Draw("SAME HIST")
		hsig2.Draw("SAME HIST")
		
		if not blind: hData.Draw("SAME E1 X0") #redraw data so its not hidden
		uPad.RedrawAxis()
		bkgHTgerr.Draw("SAME E2")

		leg = {}
		if 'Tau21' in discriminant or 'Tau32' in discriminant or 'deltaRjet1' in discriminant:
			leg = R.TLegend(0.15,0.53,0.45,0.90)
		elif 'Eta' in discriminant or 'deltaRjet2' in discriminant:
			leg = R.TLegend(0.72,0.43,0.95,0.90)
		else:
			leg = R.TLegend(0.65,0.53,0.95,0.90)
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

		leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
		leg.AddEntry(hsig2,sig2leg+scaleFact1Str,"l")
				
		try: 
			if hQCD.Integral()/bkgHT.Integral()>.005: leg.AddEntry(hQCD,"QCD","f") #don't plot QCD if it is less than 0.5%
		except: pass
		try: leg.AddEntry(hEWK,"EWK","f")
		except: pass
		try: leg.AddEntry(hTOP,"TOP","f")
		except: pass
		leg.AddEntry(bkgHTgerr,"Bkg uncert. (stat. #oplus syst.)","f")
		leg.Draw("same")

		prelimTex=R.TLatex()
		prelimTex.SetNDC()
		prelimTex.SetTextAlign(31) # align right
		prelimTex.SetTextFont(42)
		prelimTex.SetTextSize(0.07)
		prelimTex.SetLineWidth(2)
		prelimTex.DrawLatex(0.95,0.92,str(lumi)+" fb^{-1} (13 TeV)")

		prelimTex2=R.TLatex()
		prelimTex2.SetNDC()
		prelimTex2.SetTextFont(61)
		prelimTex2.SetLineWidth(2)
		prelimTex2.SetTextSize(0.10)
		prelimTex2.DrawLatex(lMargin,0.92,"CMS")

		prelimTex3=R.TLatex()
		prelimTex3.SetNDC()
		prelimTex3.SetTextAlign(13)
		prelimTex3.SetTextFont(52)
		prelimTex3.SetTextSize(0.075)
		prelimTex3.SetLineWidth(2)
		if not blind: prelimTex3.DrawLatex(lMargin+0.12,0.975,"Preliminary")
		if blind: prelimTex3.DrawLatex(0.29175,0.9364,"Preliminary")

		flat = R.TF1("flat","pol1",30,250);

		line = R.TF1("line","pol1",250,1500);
		line2 = R.TF1("line2","pol1",30,1500);
		line3 = R.TF1("line3","pol1",30,1500);
		line4 = R.TF1("line4","pol1",30,1500);

		line.SetLineWidth(2);

		para = R.TF1("para","pol2",30,1500); para.SetLineColor(R.kBlue);
		para2 = R.TF1("para2","pol2",30,1500); para2.SetLineColor(R.kBlue);
		para3 = R.TF1("para3","pol2",30,1500); para3.SetLineColor(R.kBlue);

		cube = R.TF1("cube","pol3",30,1500); cube.SetLineColor(R.kGreen);
		cube2 = R.TF1("cube2","pol3",30,1500); cube2.SetLineColor(R.kGreen);
		cube3 = R.TF1("cube3","pol3",30,1500); cube3.SetLineColor(R.kGreen);

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
			pull.Draw("E1")

			if 'Bins' in discriminant:
				print '******************************'
				print 'Data/MC for',discriminant
				for binNo in range(0,pull.GetNbinsX()+2):
					print 'Bin',binNo,': content =',pull.GetBinContent(binNo),'; error =',pull.GetBinError(binNo),';'
		
			BkgOverBkg = pull.Clone("bkgOverbkg")
			BkgOverBkg.Divide(bkgHT, bkgHT)
			pullUncBandTot=R.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandTot.SetPointEYhigh(binNo-1,totBkgTemp3[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandTot.SetPointEYlow(binNo-1,totBkgTemp3[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			if not doOneBand: pullUncBandTot.SetFillStyle(3001)
			else: pullUncBandTot.SetFillStyle(3344)
			pullUncBandTot.SetFillColor(1)
			pullUncBandTot.SetLineColor(1)
			pullUncBandTot.SetMarkerSize(0)
			R.gStyle.SetHatchesLineWidth(1)
			pullUncBandTot.Draw("SAME E2")
				
			pullUncBandNorm=R.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncNorm"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandNorm.SetPointEYhigh(binNo-1,totBkgTemp2[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandNorm.SetPointEYlow(binNo-1,totBkgTemp2[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandNorm.SetFillStyle(3001)
			pullUncBandNorm.SetFillColor(2)
			pullUncBandNorm.SetLineColor(2)
			pullUncBandNorm.SetMarkerSize(0)
			R.gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandNorm.Draw("SAME E2")
			
			pullUncBandStat=R.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncStat"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandStat.SetPointEYhigh(binNo-1,totBkgTemp1[isEM].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandStat.SetPointEYlow(binNo-1,totBkgTemp1[isEM].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandStat.SetFillStyle(3001)
			pullUncBandStat.SetFillColor(3)
			pullUncBandStat.SetLineColor(3)
			pullUncBandStat.SetMarkerSize(0)
			R.gStyle.SetHatchesLineWidth(1)
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

			if stackbkgHT.GetMaximum()>1e4: pullLegend=R.TLegend(0.18,0.87,0.89,0.96)
			elif stackbkgHT.GetMaximum()>1e3: pullLegend=R.TLegend(0.16,0.87,0.87,0.96)
			else: pullLegend=R.TLegend(0.14,0.87,0.85,0.96)
			R.SetOwnership( pullLegend, 0 )   # 0 = release (not keep), 1 = keep
			pullLegend.SetShadowColor(0)
			pullLegend.SetNColumns(3)
			pullLegend.SetFillColor(0)
			pullLegend.SetFillStyle(0)
			pullLegend.SetLineColor(0)
			pullLegend.SetLineStyle(0)
			pullLegend.SetBorderSize(0)
			pullLegend.SetTextFont(42)
			if not doOneBand: pullLegend.AddEntry(pullUncBandStat , "Bkg uncert. (shape syst.)" , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandNorm , "Bkg uncert. (shape #oplus norm. syst.)" , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus all syst.)" , "f")
			else: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus syst.)" , "f")
			#else: 
			#	pullLegend.AddEntry(pullUncBandTot , "Bkg stat." , "f")
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
			pull.GetYaxis().SetTitle('#frac{(obs-bkg)}{#sigma}')
			pull.Draw("HIST")

		savePrefix = templateDir.split('/')[-1]+'/plots/'
		if not os.path.exists(os.getcwd()+'/'+savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix+isRebinned
		if doRealPull: savePrefix+='_pull'
		if yLog: savePrefix+='_logy'

		if doOneBand:
			c1.SaveAs(savePrefix+"_totBand.pdf")
			c1.SaveAs(savePrefix+"_totBand.png")
			c1.SaveAs(savePrefix+"_totBand.eps")
		else:
			c1.SaveAs(savePrefix+".pdf")
			c1.SaveAs(savePrefix+".png")
			c1.SaveAs(savePrefix+".eps")
			
	RFile.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


