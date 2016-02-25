#!/usr/bin/python

import os,sys,time,math,pickle
from ROOT import *
from weights import *

gROOT.SetBatch(1)
start_time = time.time()

lumi=2.3 #for plots
lumiInTemplates='2p263'

discriminant = 'minMlb'
cutString='lep40_MET75_1jet300_2jet150_NJets3_NBJets0_3jet100_4jet0_5jet0_DR1_1Wjet0_1bjet0_HT0_ST0_minMlb0'
saveKey = ''#'_topPtSystOnly'

# m1 = '800'
# sig1='X53X53M'+m1+'left' # choose the 1st signal to plot
# sig1leg='X_{5/3}#bar{X}_{5/3} LH (0.8 TeV)'
# m2 = '800'
# sig2='X53X53M'+m1+'right' # choose the 2nd signal to plot
# sig2leg='X_{5/3}#bar{X}_{5/3} RH (0.8 TeV)'
m1 = '800'
sig1='TTM'+m1 # choose the 1st signal to plot
sig1leg='TT (0.8 TeV)'
m2 = '1000'
sig2='TTM'+m2 # choose the 2nd signal to plot
sig2leg='TT (1.0 TeV)'
scaleSignals = False

systematicList = ['pileup','jec','jer','jmr','jms','btag','tau21','pdfNew','muRFcorrdNew','toppt','jsf']
doAllSys = True
doQ2sys  = True
if not doAllSys: doQ2sys = False # I assume you don't want Q^2 as well if you are not doing the other shape systematics! (this is just to change one bool)

isRebinned='_rebinned'#post fix for file names if the name changed b/c of rebinning or some other process
doNormByBinWidth=False # not tested, may not work out of the box
doOneBand = False
if not doAllSys: doOneBand = True # Don't change this!
blind = False
yLog  = True
doRealPull = True
if doRealPull: doOneBand=False

histPrefix=discriminant+'_'+lumiInTemplates+'fb_'

templateDir=os.getcwd()+'/templates_minMlb_tau21LT0p6_tptp_2016_2_23/'+cutString+'/'
tempsig='templates_'+discriminant+'_'+sig1+'_'+lumiInTemplates+'fb'+isRebinned+'.root'	

isEMlist =['E','M']
nWtaglist=['0','1p']
nbtaglist=['0','1','2','3p']

lumiSys = 0.046 #4.6% lumi uncertainty
trigSys = 0.05 #3% trigger uncertainty
lepIdSys = 0.01 #1% lepton id uncertainty
lepIsoSys = 0.01 #1% lepton isolation uncertainty
topXsecSys = 0.#0.055 #5.5% top x-sec uncertainty
ewkXsecSys = 0.#0.05 #5% ewk x-sec uncertainty
qcdXsecSys = 0.#0.50 #50% qcd x-sec uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2)
topModelingSys = { #top modeling uncertainty from ttbar CR (correlated across e/m)
			     'top_0_0' :0.15,
			     'top_0_1' :0.12,
			     'top_0_2' :0.02,
			     'top_0_2p':0.02,
			     'top_0_3p':0.02,
			     'top_1p_0' :0.15,
			     'top_1p_1' :0.12,
			     'top_1p_2' :0.02,
			     'top_1p_2p':0.02,
			     'top_1p_3p':0.02,
			     }
ewkModelingSys = { #ewk modeling uncertainty from wjets CR (correlated across e/m)		
			     'ewk_0_0' :0.22,
			     'ewk_0_1' :0.22,
			     'ewk_0_2' :0.22,
			     'ewk_0_2p':0.22,
			     'ewk_0_3p':0.22,
			     'ewk_1p_0' :0.02,
			     'ewk_1p_1' :0.02,
			     'ewk_1p_2' :0.02,
			     'ewk_1p_2p':0.02,
			     'ewk_1p_3p':0.02,
			     }

def getNormUnc(hist,ibin,modelingUnc):
	contentsquared = hist.GetBinContent(ibin)**2
	error = corrdSys*corrdSys*contentsquared  #correlated uncertainties
	error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
	if 'top' in hist.GetName(): error += topXsecSys*topXsecSys*contentsquared # cross section
	if 'ewk' in hist.GetName(): error += ewkXsecSys*ewkXsecSys*contentsquared # cross section
	if 'qcd' in hist.GetName(): error += qcdXsecSys*qcdXsecSys*contentsquared # cross section
	return error

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

	if 'nB0' in histogram.GetName() and 'minMlb' in histogram.GetName(): histogram.GetXaxis().SetTitle("min[M(l,jets)] (GeV)")
	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.00101)
	if not yLog: 
		histogram.SetMinimum(0.25)
	if yLog:
		uPad.SetLogy()
		if not doNormByBinWidth: histogram.SetMaximum(200*histogram.GetMaximum())
		
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
	else: histogram.GetYaxis().SetRangeUser(0,2.99)
	histogram.GetYaxis().CenterTitle()

def negBinCorrection(hist): #set negative bin contents to zero and adjust the normalization
	norm0=hist.Integral()
	for iBin in range(0,hist.GetNbinsX()+2):
		if hist.GetBinContent(iBin)<0: hist.SetBinContent(iBin,0)
	if hist.Integral()!=0: hist.Scale(norm0/hist.Integral())

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

RFile1 = TFile(templateDir+tempsig.replace(sig1,sig1))
RFile2 = TFile(templateDir+tempsig.replace(sig1,sig2))
systHists = {}
totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}
for nWtag in nWtaglist:
	for nBtag in nbtaglist:
		for isEM in isEMlist:
			print histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__top'
			hTOP = RFile1.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__top').Clone()
			try: hEWK = RFile1.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__ewk').Clone()
			except:
				print "There is no EWK!!!!!!!!"
				print "Skipping EWK....."
				pass
			try: hQCD = RFile1.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__qcd').Clone()
			except:
				print "There is no QCD!!!!!!!!"
				print "Skipping QCD....."
				pass
			hData = RFile1.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__DATA').Clone()
			hsig1 = RFile1.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__sig').Clone(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__sig1')
			hsig2 = RFile2.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__sig').Clone(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__sig2')
			hsig1.Scale(xsec[sig1])
			hsig2.Scale(xsec[sig2])
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
						systHists['top'+isEM+nWtag+nBtag+sys+ud] = RFile1.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__top__'+sys+'__'+ud).Clone()
						systHists['top'+isEM+nWtag+nBtag+sys+ud] = systHists['top'+isEM+nWtag+nBtag+sys+ud].Clone()
						try: 
							systHists['ewk'+isEM+nWtag+nBtag+sys+ud] = RFile1.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__ewk__'+sys+'__'+ud).Clone()
						except: pass
						try: 
							systHists['qcd'+isEM+nWtag+nBtag+sys+ud] = RFile1.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__qcd__'+sys+'__'+ud).Clone()
						except: pass
			if doQ2sys:
				for ud in ['minus','plus']:
					systHists['top'+isEM+nWtag+nBtag+'q2'+ud] = RFile1.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__top__q2__'+ud).Clone()
					systHists['q2'+isEM+nWtag+nBtag+ud] = systHists['top'+isEM+nWtag+nBtag+'q2'+ud].Clone()
					try:
						systHists['ewk'+isEM+nWtag+nBtag+'q2'+ud] = RFile1.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__ewk').Clone()
						systHists['q2'+isEM+nWtag+nBtag+ud].Add(systHists['ewk'+isEM+nWtag+nBtag+'q2'+ud])
					except: pass
					try:
						systHists['qcd'+isEM+nWtag+nBtag+'q2'+ud] = RFile1.Get(histPrefix+'is'+isEM+'_nW'+nWtag+'_nB'+nBtag+'__qcd').Clone()
						systHists['q2'+isEM+nWtag+nBtag+ud].Add(systHists['qcd'+isEM+nWtag+nBtag+'q2'+ud])
					except: pass

			bkgHT = hTOP.Clone()
			try: bkgHT.Add(hEWK)
			except: pass
			try: bkgHT.Add(hQCD)
			except: pass

			totBkgTemp1[isEM+nWtag+nBtag] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
			totBkgTemp2[isEM+nWtag+nBtag] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
			totBkgTemp3[isEM+nWtag+nBtag] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))
			
			for ibin in range(1,hTOP.GetNbinsX()+1):
				errorUp = 0.
				errorDn = 0.
				errorStatOnly = bkgHT.GetBinError(ibin)**2
				errorNorm = getNormUnc(hTOP,ibin,topModelingSys['top_'+nWtag+'_'+nBtag])
				try: errorNorm += getNormUnc(hEWK,ibin,ewkModelingSys['ewk_'+nWtag+'_'+nBtag])
				except: pass
				try: errorNorm += getNormUnc(hQCD,ibin,0.0)
				except: pass

				for sys in systematicList:
					if doAllSys:	
						errorPlus = systHists['top'+isEM+nWtag+nBtag+sys+'plus'].GetBinContent(ibin)-hTOP.GetBinContent(ibin)
						errorMinus = hTOP.GetBinContent(ibin)-systHists['top'+isEM+nWtag+nBtag+sys+'minus'].GetBinContent(ibin)
						if errorPlus > 0: errorUp += errorPlus**2
						else: errorDn += errorPlus**2
						if errorMinus > 0: errorDn += errorMinus**2
						else: errorUp += errorMinus**2
						if sys!='toppt':
							try:
								errorPlus = systHists['ewk'+isEM+nWtag+nBtag+sys+'plus'].GetBinContent(ibin)-hEWK.GetBinContent(ibin)
								errorMinus = hEWK.GetBinContent(ibin)-systHists['ewk'+isEM+nWtag+nBtag+sys+'minus'].GetBinContent(ibin)
								if errorPlus > 0: errorUp += errorPlus**2
								else: errorDn += errorPlus**2
								if errorMinus > 0: errorDn += errorMinus**2
								else: errorUp += errorMinus**2
							except: pass
							try:
								errorPlus = systHists['qcd'+isEM+nWtag+nBtag+sys+'plus'].GetBinContent(ibin)-hQCD.GetBinContent(ibin)
								errorMinus = hQCD.GetBinContent(ibin)-systHists['qcd'+isEM+nWtag+nBtag+sys+'minus'].GetBinContent(ibin)
								if errorPlus > 0: errorUp += errorPlus**2
								else: errorDn += errorPlus**2
								if errorMinus > 0: errorDn += errorMinus**2
								else: errorUp += errorMinus**2
							except: pass													
				if doQ2sys: 
					errorPlus = systHists['top'+isEM+nWtag+nBtag+'q2plus'].GetBinContent(ibin)-hTOP.GetBinContent(ibin)
					errorMinus = hTOP.GetBinContent(ibin)-systHists['top'+isEM+nWtag+nBtag+'q2minus'].GetBinContent(ibin)
					if errorPlus > 0: errorUp += errorPlus**2
					else: errorDn += errorPlus**2
					if errorMinus > 0: errorDn += errorMinus**2
					else: errorUp += errorMinus**2

				totBkgTemp1[isEM+nWtag+nBtag].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
				totBkgTemp1[isEM+nWtag+nBtag].SetPointEYlow(ibin-1, math.sqrt(errorDn))
				totBkgTemp2[isEM+nWtag+nBtag].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
				totBkgTemp2[isEM+nWtag+nBtag].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
				totBkgTemp3[isEM+nWtag+nBtag].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
				totBkgTemp3[isEM+nWtag+nBtag].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
			
			bkgHTgerr = totBkgTemp3[isEM+nWtag+nBtag].Clone()
	
			scaleFact1 = int(bkgHT.GetMaximum()/hsig1.GetMaximum()) - int(bkgHT.GetMaximum()/hsig1.GetMaximum()) % 10
			scaleFact2 = int(bkgHT.GetMaximum()/hsig2.GetMaximum()) - int(bkgHT.GetMaximum()/hsig2.GetMaximum()) % 10
			if scaleFact1==0: scaleFact1=int(bkgHT.GetMaximum()/hsig1.GetMaximum())
			if scaleFact2==0: scaleFact2=int(bkgHT.GetMaximum()/hsig2.GetMaximum())
			if scaleFact1==0: scaleFact1=1
			if scaleFact2==0: scaleFact2=1
			if not scaleSignals:
				scaleFact1=1
				scaleFact2=1
# 			else:
# 				scaleFact1=25
# 				scaleFact2=25
			hsig1.Scale(scaleFact1)
			hsig2.Scale(scaleFact2)

			stackbkgHT = THStack("stackbkgHT","")#"CMS Preliminary, 5 fb^{-1} at #sqrt{s} = 13 TeV;H_{T} (GeV)")
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
			hsig1.SetLineColor(kRed)
			hsig1.SetFillStyle(0)
			hsig1.SetLineWidth(3)
			hsig2.SetLineColor(kOrange-2)
			hsig2.SetLineStyle(5)
			hsig2.SetFillStyle(0)
			hsig2.SetLineWidth(3)
			
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
				formatUpperHist(sighist1RH)
				hsig1.SetMaximum(hData.GetMaximum())
				hsig1.Draw("HIST")
			stackbkgHT.Draw("SAME HIST")
			hsig1.Draw("SAME HIST")
			hsig2.Draw("SAME HIST")
			if not blind: hData.Draw("SAME E1 X0") #redraw data so its not hidden
			uPad.RedrawAxis()
			bkgHTgerr.Draw("SAME E2")

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
			scaleFact2Str = ' x'+str(scaleFact2)
			if not scaleSignals:
				scaleFact1Str = ''
				scaleFact2Str = ''
			leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
			leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
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

			if blind == False and not doRealPull:
				lPad.cd()
				pull=hData.Clone("pull")
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
				
				BkgOverBkg = pull.Clone("bkgOverbkg")
				BkgOverBkg.Divide(bkgHT, bkgHT)
				pullUncBandTot=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
				for binNo in range(0,hData.GetNbinsX()+2):
					if bkgHT.GetBinContent(binNo)!=0:
						pullUncBandTot.SetPointEYhigh(binNo-1,totBkgTemp3[isEM+nWtag+nBtag].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
						pullUncBandTot.SetPointEYlow(binNo-1,totBkgTemp3[isEM+nWtag+nBtag].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
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
						pullUncBandNorm.SetPointEYhigh(binNo-1,totBkgTemp2[isEM+nWtag+nBtag].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
						pullUncBandNorm.SetPointEYlow(binNo-1,totBkgTemp2[isEM+nWtag+nBtag].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
				pullUncBandNorm.SetFillStyle(3001)
				pullUncBandNorm.SetFillColor(2)
				pullUncBandNorm.SetLineColor(2)
				pullUncBandNorm.SetMarkerSize(0)
				gStyle.SetHatchesLineWidth(1)
				if not doOneBand: pullUncBandNorm.Draw("SAME E2")
				
				pullUncBandStat=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncStat"))
				for binNo in range(0,hData.GetNbinsX()+2):
					if bkgHT.GetBinContent(binNo)!=0:
						pullUncBandStat.SetPointEYhigh(binNo-1,totBkgTemp1[isEM+nWtag+nBtag].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
						pullUncBandStat.SetPointEYlow(binNo-1,totBkgTemp1[isEM+nWtag+nBtag].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
				pullUncBandStat.SetFillStyle(3001)
				pullUncBandStat.SetFillColor(3)
				pullUncBandStat.SetLineColor(3)
				pullUncBandStat.SetMarkerSize(0)
				gStyle.SetHatchesLineWidth(1)
				if not doOneBand: pullUncBandStat.Draw("SAME E2")
				
				if doQ2sys:
					pullQ2up=systHists['q2'+isEM+nWtag+nBtag+'plus'].Clone("pullQ2Up")
					pullQ2up.Divide(systHists['q2'+isEM+nWtag+nBtag+'plus'], bkgHT)
					pullQ2up.SetFillColor(0)
					pullQ2up.SetLineColor(6)
					pullQ2up.SetLineWidth(3)
					#pullQ2up.Draw("SAME HIST")
				
					pullQ2dn=systHists['q2'+isEM+nWtag+nBtag+'minus'].Clone("pullQ2Dn")
					pullQ2dn.Divide(systHists['q2'+isEM+nWtag+nBtag+'minus'], bkgHT)
					pullQ2dn.SetFillColor(0)
					pullQ2dn.SetLineColor(6)
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
				if not doOneBand: pullLegend.AddEntry(pullUncBandStat , "Bkg uncert. (shape syst.)" , "f")
				if not doOneBand: pullLegend.AddEntry(pullUncBandNorm , "Bkg uncert. (shape #oplus norm. syst.)" , "f")
				if not doOneBand: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus all syst.)" , "f")
				else: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus syst.)" , "f")
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
						MCerror = 0.5*(totBkgTemp3[isEM+nWtag+nBtag].GetErrorYhigh(binNo-1)+totBkgTemp3[isEM+nWtag+nBtag].GetErrorYlow(binNo-1))
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
			savePrefix = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
			if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
			savePrefix+=histPrefix+isEM+'_nW'+nWtag+'_nB'+nBtag+isRebinned+saveKey
			if doRealPull: savePrefix+='_pull'
			if yLog: savePrefix+='_logy'

			if doOneBand:
				c1.SaveAs(savePrefix+"totBand.pdf")
				c1.SaveAs(savePrefix+"totBand.png")
				c1.SaveAs(savePrefix+"totBand.root")
				c1.SaveAs(savePrefix+"totBand.C")
			else:
				c1.SaveAs(savePrefix+".pdf")
				c1.SaveAs(savePrefix+".png")
				c1.SaveAs(savePrefix+".root")
				c1.SaveAs(savePrefix+".C")
			try: del hTOP
			except: pass
			try: del hEWK
			except: pass
			try: del hQCD
			except: pass
						
		#plot e/m combined
		hTOPmerged = RFile1.Get(histPrefix+'isE'+'_nW'+nWtag+'_nB'+nBtag+'__top').Clone()
		hTOPmerged.Add(RFile1.Get(histPrefix+'isM'+'_nW'+nWtag+'_nB'+nBtag+'__top'))
		try: 
			hEWKmerged = RFile1.Get(histPrefix+'isE'+'_nW'+nWtag+'_nB'+nBtag+'__ewk').Clone()
			hEWKmerged.Add(RFile1.Get(histPrefix+'isM'+'_nW'+nWtag+'_nB'+nBtag+'__ewk'))
		except:pass
		try: 
			hQCDmerged = RFile1.Get(histPrefix+'isE'+'_nW'+nWtag+'_nB'+nBtag+'__qcd').Clone()
			hQCDmerged.Add(RFile1.Get(histPrefix+'isM'+'_nW'+nWtag+'_nB'+nBtag+'__qcd').Clone())
		except:pass
		hDatamerged = RFile1.Get(histPrefix+'isE'+'_nW'+nWtag+'_nB'+nBtag+'__DATA').Clone()
		hsig1merged = RFile1.Get(histPrefix+'isE'+'_nW'+nWtag+'_nB'+nBtag+'__sig').Clone(histPrefix+'isE'+'_nW'+nWtag+'_nB'+nBtag+'__sig1merged')
		hsig2merged = RFile2.Get(histPrefix+'isE'+'_nW'+nWtag+'_nB'+nBtag+'__sig').Clone(histPrefix+'isE'+'_nW'+nWtag+'_nB'+nBtag+'__sig2merged')
		hDatamerged.Add(RFile1.Get(histPrefix+'isM'+'_nW'+nWtag+'_nB'+nBtag+'__DATA').Clone())
		hsig1merged.Add(RFile1.Get(histPrefix+'isM'+'_nW'+nWtag+'_nB'+nBtag+'__sig').Clone())
		hsig2merged.Add(RFile2.Get(histPrefix+'isM'+'_nW'+nWtag+'_nB'+nBtag+'__sig').Clone())
		hsig1merged.Scale(xsec[sig1])
		hsig2merged.Scale(xsec[sig2])
		if doNormByBinWidth:
			normByBinWidth(hTOPmerged)
			normByBinWidth(hEWKmerged)
			normByBinWidth(hQCDmerged)
			normByBinWidth(hsig1merged)
			normByBinWidth(hsig2merged)
			normByBinWidth(hDatamerged)

		if doAllSys:
			for sys in systematicList:
				for ud in ['minus','plus']:
					systHists['toplep'+nWtag+nBtag+sys+ud] = systHists['topE'+nWtag+nBtag+sys+ud].Clone()
					systHists['toplep'+nWtag+nBtag+sys+ud].Add(systHists['topM'+nWtag+nBtag+sys+ud])
					try: 
						systHists['ewklep'+nWtag+nBtag+sys+ud] = systHists['ewkE'+nWtag+nBtag+sys+ud].Clone()
						systHists['ewklep'+nWtag+nBtag+sys+ud].Add(systHists['ewkM'+nWtag+nBtag+sys+ud])
					except: pass
					try: 
						systHists['qcdlep'+nWtag+nBtag+sys+ud] = systHists['qcdE'+nWtag+nBtag+sys+ud].Clone()
						systHists['qcdlep'+nWtag+nBtag+sys+ud].Add(systHists['qcdM'+nWtag+nBtag+sys+ud])
					except: pass
		if doQ2sys:
			for ud in ['minus','plus']:
				systHists['toplep'+nWtag+nBtag+'q2'+ud] = systHists['topE'+nWtag+nBtag+'q2'+ud].Clone()
				systHists['toplep'+nWtag+nBtag+'q2'+ud].Add(systHists['topM'+nWtag+nBtag+'q2'+ud])
				systHists['q2lep'+nWtag+nBtag+'q2'+ud] = systHists['toplep'+nWtag+nBtag+'q2'+ud].Clone()
				try:
					systHists['ewklep'+nWtag+nBtag+'q2'+ud] = systHists['ewkE'+nWtag+nBtag+'q2'+ud].Clone()
					systHists['ewklep'+nWtag+nBtag+'q2'+ud].Add(systHists['ewkM'+nWtag+nBtag+'q2'+ud])
					systHists['q2lep'+nWtag+nBtag+'q2'+ud].Add(systHists['ewklep'+nWtag+nBtag+'q2'+ud])
				except: pass
				try:
					systHists['qcdlep'+nWtag+nBtag+'q2'+ud] = systHists['qcdE'+nWtag+nBtag+'q2'+ud].Clone()
					systHists['qcdlep'+nWtag+nBtag+'q2'+ud].Add(systHists['qcdM'+nWtag+nBtag+'q2'+ud])
					systHists['q2lep'+nWtag+nBtag+'q2'+ud].Add(systHists['qcdlep'+nWtag+nBtag+'q2'+ud])
				except: pass

		bkgHTmerged = hTOPmerged.Clone()
		try: bkgHTmerged.Add(hEWKmerged)
		except: pass
		try: bkgHTmerged.Add(hQCDmerged)
		except: pass

		totBkgTemp1['lep'+nWtag+nBtag] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapeOnly'))
		totBkgTemp2['lep'+nWtag+nBtag] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapePlusNorm'))
		totBkgTemp3['lep'+nWtag+nBtag] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'All'))
		
		for ibin in range(1,hTOPmerged.GetNbinsX()+1):
			errorUp = 0.
			errorDn = 0.
			errorStatOnly = bkgHTmerged.GetBinError(ibin)**2
			errorNorm = getNormUnc(hTOPmerged,ibin,topModelingSys['top_'+nWtag+'_'+nBtag])
			try: errorNorm += getNormUnc(hEWKmerged,ibin,ewkModelingSys['ewk_'+nWtag+'_'+nBtag])
			except: pass
			try: errorNorm += getNormUnc(hQCDmerged,ibin,0.0)
			except: pass

			for sys in systematicList:
				if doAllSys:	
					errorPlus = systHists['toplep'+nWtag+nBtag+sys+'plus'].GetBinContent(ibin)-hTOPmerged.GetBinContent(ibin)
					errorMinus = hTOPmerged.GetBinContent(ibin)-systHists['toplep'+nWtag+nBtag+sys+'minus'].GetBinContent(ibin)
					if errorPlus > 0: errorUp += errorPlus**2
					else: errorDn += errorPlus**2
					if errorMinus > 0: errorDn += errorMinus**2
					else: errorUp += errorMinus**2
					if sys!='toppt':
						try:
							errorPlus = systHists['ewklep'+nWtag+nBtag+sys+'plus'].GetBinContent(ibin)-hEWKmerged.GetBinContent(ibin)
							errorMinus = hEWKmerged.GetBinContent(ibin)-systHists['ewklep'+nWtag+nBtag+sys+'minus'].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass
						try:
							errorPlus = systHists['qcdlep'+nWtag+nBtag+sys+'plus'].GetBinContent(ibin)-hQCDmerged.GetBinContent(ibin)
							errorMinus = hQCDmerged.GetBinContent(ibin)-systHists['qcdlep'+nWtag+nBtag+sys+'minus'].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass													
			if doQ2sys: 
				errorPlus = systHists['toplep'+nWtag+nBtag+'q2plus'].GetBinContent(ibin)-hTOPmerged.GetBinContent(ibin)
				errorMinus = hTOPmerged.GetBinContent(ibin)-systHists['toplep'+nWtag+nBtag+'q2minus'].GetBinContent(ibin)
				if errorPlus > 0: errorUp += errorPlus**2
				else: errorDn += errorPlus**2
				if errorMinus > 0: errorDn += errorMinus**2
				else: errorUp += errorMinus**2

			totBkgTemp1['lep'+nWtag+nBtag].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
			totBkgTemp1['lep'+nWtag+nBtag].SetPointEYlow(ibin-1, math.sqrt(errorDn))
			totBkgTemp2['lep'+nWtag+nBtag].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
			totBkgTemp2['lep'+nWtag+nBtag].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
			totBkgTemp3['lep'+nWtag+nBtag].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
			totBkgTemp3['lep'+nWtag+nBtag].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
		
		bkgHTgerrmerged = totBkgTemp3['lep'+nWtag+nBtag].Clone()

		scaleFact1merged = int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum()) - int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum()) % 10
		scaleFact2merged = int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum()) - int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum()) % 10
		if scaleFact1merged==0: scaleFact1merged=int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum())
		if scaleFact2merged==0: scaleFact2merged=int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum())
		if scaleFact1merged==0: scaleFact1merged=1
		if scaleFact2merged==0: scaleFact2merged=1
		if not scaleSignals:
			scaleFact1merged=1
			scaleFact2merged=1
		hsig1merged.Scale(scaleFact1merged)
		hsig2merged.Scale(scaleFact2merged)

		stackbkgHTmerged = THStack("stackbkgHTmerged","")#"CMS Preliminary, 5 fb^{-1} at #sqrt{s} = 13 TeV;H_{T} (GeV)")
		try: stackbkgHTmerged.Add(hTOPmerged)
		except: pass
		try: stackbkgHTmerged.Add(hEWKmerged)
		except: pass
		try: 
			if hQCDmerged.Integral()/bkgHTmerged.Integral()>.005: stackbkgHTmerged.Add(hQCDmerged)
		except: pass

		hTOPmerged.SetLineColor(kAzure-6)
		hTOPmerged.SetFillColor(kAzure-6)
		hTOPmerged.SetLineWidth(2)
		try: 
			hEWKmerged.SetLineColor(kMagenta-2)
			hEWKmerged.SetFillColor(kMagenta-2)
			hEWKmerged.SetLineWidth(2)
		except: pass
		try:
			hQCDmerged.SetLineColor(kOrange+5)
			hQCDmerged.SetFillColor(kOrange+5)
			hQCDmerged.SetLineWidth(2)
		except: pass
		hsig1merged.SetLineColor(kRed)
		hsig1merged.SetFillStyle(0)
		hsig1merged.SetLineWidth(3)
		hsig2merged.SetLineColor(kOrange-2)
		hsig2merged.SetLineStyle(5)
		hsig2merged.SetFillStyle(0)
		hsig2merged.SetLineWidth(3)
		
		hDatamerged.SetMarkerStyle(20)
		hDatamerged.SetMarkerSize(1.2)
		hDatamerged.SetLineWidth(2)

		bkgHTgerrmerged.SetFillStyle(3004)
		bkgHTgerrmerged.SetFillColor(kBlack)

		gStyle.SetOptStat(0)
		c1merged = TCanvas("c1merged","c1merged",1200,1000)
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
		if not doNormByBinWidth: hDatamerged.SetMaximum(1.2*max(hDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
		hDatamerged.SetMinimum(0.015)
		if doNormByBinWidth: hDatamerged.GetYaxis().SetTitle("Events / 1 GeV")
		else: hDatamerged.GetYaxis().SetTitle("Events")
		formatUpperHist(hDatamerged)
		uPad.cd()
		hDatamerged.SetTitle("")
		stackbkgHTmerged.SetTitle("")
		if not blind: hDatamerged.Draw("E1 X0")
		if blind: 
			sighist1RHmerged.SetMinimum(0.015)
			if doNormByBinWidth: sighist1RHmerged.GetYaxis().SetTitle("Events / 1 GeV")
			else: sighist1RHmerged.GetYaxis().SetTitle("Events")
			formatUpperHist(sighist1RHmerged)
			sighist1RHmerged.SetMaximum(hDatamerged.GetMaximum())
			sighist1RHmerged.Draw("HIST")
		stackbkgHTmerged.Draw("SAME HIST")
		hsig1merged.Draw("SAME HIST")
		hsig2merged.Draw("SAME HIST")
		if not blind: hDatamerged.Draw("SAME E1 X0") #redraw data so its not hidden
		uPad.RedrawAxis()
		bkgHTgerrmerged.Draw("SAME E2")

		legmerged = TLegend(0.65,0.53,0.95,0.90)
		legmerged.SetShadowColor(0)
		legmerged.SetFillColor(0)
		legmerged.SetFillStyle(0)
		legmerged.SetLineColor(0)
		legmerged.SetLineStyle(0)
		legmerged.SetBorderSize(0) 
		legmerged.SetTextFont(42)
		if not blind: legmerged.AddEntry(hDatamerged,"DATA")
		scaleFact1Str = ' x'+str(scaleFact1)
		scaleFact2Str = ' x'+str(scaleFact2)
		if not scaleSignals:
			scaleFact1Str = ''
			scaleFact2Str = ''
		legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
		legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
		try: 
			if hQCDmerged.Integral()/bkgHTmerged.Integral()>.005: legmerged.AddEntry(hQCDmerged,"QCD","f")
		except: pass
		try: legmerged.AddEntry(hEWKmerged,"EWK","f")
		except: pass
		try: legmerged.AddEntry(hTOPmerged,"TOP","f")
		except: pass
		legmerged.AddEntry(bkgHTgerrmerged,"MC uncert. (stat. #oplus syst.)","f")
		legmerged.Draw("same")

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

		if blind == False and not doRealPull:
			lPad.cd()
			pullmerged=hDatamerged.Clone("pullmerged")
			pullmerged.Divide(hDatamerged, bkgHTmerged)
			for binNo in range(0,hDatamerged.GetNbinsX()+2):
				if bkgHTmerged.GetBinContent(binNo)!=0:
					pull.SetBinError(binNo,hDatamerged.GetBinError(binNo)/bkgHTmerged.GetBinContent(binNo))
			pullmerged.SetMaximum(3)
			pullmerged.SetMinimum(0)
			pullmerged.SetFillColor(1)
			pullmerged.SetLineColor(1)
			formatLowerHist(pullmerged)
			pullmerged.Draw("E1")
			
			BkgOverBkgmerged = pullmerged.Clone("bkgOverbkgmerged")
			BkgOverBkgmerged.Divide(bkgHTmerged, bkgHTmerged)
			pullUncBandTotmerged=TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncTotmerged"))
			for binNo in range(0,hDatamerged.GetNbinsX()+2):
				if bkgHTmerged.GetBinContent(binNo)!=0:
					pullUncBandTotmerged.SetPointEYhigh(binNo-1,totBkgTemp3['lep'+nWtag+nBtag].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
					pullUncBandTotmerged.SetPointEYlow(binNo-1, totBkgTemp3['lep'+nWtag+nBtag].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
			if not doOneBand: pullUncBandTotmerged.SetFillStyle(3001)
			else: pullUncBandTotmerged.SetFillStyle(3344)
			pullUncBandTotmerged.SetFillColor(1)
			pullUncBandTotmerged.SetLineColor(1)
			pullUncBandTotmerged.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			pullUncBandTotmerged.Draw("SAME E2")
			
			pullUncBandNormmerged=TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncNormmerged"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHTmerged.GetBinContent(binNo)!=0:
					pullUncBandNormmerged.SetPointEYhigh(binNo-1,totBkgTemp2['lep'+nWtag+nBtag].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
					pullUncBandNormmerged.SetPointEYlow(binNo-1, totBkgTemp2['lep'+nWtag+nBtag].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
			pullUncBandNormmerged.SetFillStyle(3001)
			pullUncBandNormmerged.SetFillColor(2)
			pullUncBandNormmerged.SetLineColor(2)
			pullUncBandNormmerged.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandNormmerged.Draw("SAME E2")
			
			pullUncBandStatmerged=TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncStatmerged"))
			for binNo in range(0,hDatamerged.GetNbinsX()+2):
				if bkgHTmerged.GetBinContent(binNo)!=0:
					pullUncBandStatmerged.SetPointEYhigh(binNo-1,totBkgTemp1['lep'+nWtag+nBtag].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
					pullUncBandStatmerged.SetPointEYlow(binNo-1, totBkgTemp1['lep'+nWtag+nBtag].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
			pullUncBandStatmerged.SetFillStyle(3001)
			pullUncBandStatmerged.SetFillColor(3)
			pullUncBandStatmerged.SetLineColor(3)
			pullUncBandStatmerged.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandStatmerged.Draw("SAME E2")

			pullLegendmerged=TLegend(0.14,0.87,0.85,0.96)
			SetOwnership( pullLegendmerged, 0 )   # 0 = release (not keep), 1 = keep
			pullLegendmerged.SetShadowColor(0)
			pullLegendmerged.SetNColumns(3)
			pullLegendmerged.SetFillColor(0)
			pullLegendmerged.SetFillStyle(0)
			pullLegendmerged.SetLineColor(0)
			pullLegendmerged.SetLineStyle(0)
			pullLegendmerged.SetBorderSize(0)
			pullLegendmerged.SetTextFont(42)
			if not doOneBand: pullLegendmerged.AddEntry(pullUncBandStat , "Bkg uncert. (shape syst.)" , "f")
			if not doOneBand: pullLegendmerged.AddEntry(pullUncBandNorm , "Bkg uncert. (shape #oplus norm. syst.)" , "f")
			if not doOneBand: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus all syst.)" , "f")
			else: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus syst.)" , "f")
			pullLegendmerged.Draw("SAME")
			pullmerged.Draw("SAME")
			lPad.RedrawAxis()

		if blind == False and doRealPull:
			lPad.cd()
			pullmerged=hDatamerged.Clone("pullmerged")
			for binNo in range(0,hDatamerged.GetNbinsX()+2):
				if hDatamerged.GetBinContent(binNo)!=0:
					MCerror = 0.5*(totBkgTemp3['lep'+nWtag+nBtag].GetErrorYhigh(binNo-1)+totBkgTemp3['lep'+nWtag+nBtag].GetErrorYlow(binNo-1))
					pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(MCerror**2+hDatamerged.GetBinError(binNo)**2))
					#pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(bkgHTmerged.GetBinError(binNo)**2+hDatamerged.GetBinError(binNo)**2))
				else: pullmerged.SetBinContent(binNo,0.)
			pullmerged.SetMaximum(3)
			pullmerged.SetMinimum(-3)
			pullmerged.SetFillColor(2)
			pullmerged.SetLineColor(2)
			formatLowerHist(pullmerged)
			pullmerged.GetYaxis().SetTitle('Pull')
			pullmerged.Draw("HIST")

		#c1merged.Write()
		savePrefixmerged = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
		if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
		savePrefixmerged+=histPrefix+'lep_nW'+nWtag+'_nB'+nBtag+isRebinned+saveKey
		if doRealPull: savePrefixmerged+='_pull'
		if yLog: savePrefixmerged+='_logy'

		if doOneBand: 
			c1merged.SaveAs(savePrefixmerged+"totBand.pdf")
			c1merged.SaveAs(savePrefixmerged+"totBand.png")
			c1merged.SaveAs(savePrefixmerged+"totBand.root")
			c1merged.SaveAs(savePrefixmerged+"totBand.C")
		else: 
			c1merged.SaveAs(savePrefixmerged+".pdf")
			c1merged.SaveAs(savePrefixmerged+".png")
			c1merged.SaveAs(savePrefixmerged+".root")
			c1merged.SaveAs(savePrefixmerged+".C")
		try: del hTOPmerged
		except: pass
		try: del hEWKmerged
		except: pass
		try: del hQCDmerged
		except: pass
			
RFile1.Close()
RFile2.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


