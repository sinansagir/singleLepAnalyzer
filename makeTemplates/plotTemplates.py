#!/usr/bin/python

import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from ROOT import *
from weights import *
from modSyst import *
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

lumi=35.9 #for plots
lumiInTemplates= str(targetlumi/1000).replace('.','p') # 1/fb

region='SR' #SR,PS
isCategorized=True
iPlot='HTpBDT'
if len(sys.argv)>1: iPlot=str(sys.argv[1])
cutString=''#'lep50_MET30_DR0_1jet50_2jet40'
pfix='templates'
if not isCategorized: pfix='kinematics_'+region
templateDir=os.getcwd()+'/'+pfix+'_JetKin_2017_4_24/'+cutString+'/'

splitTTbar = True
isRebinned=''#'_rebinned_stat0p3' #post for ROOT file names
saveKey = '' # tag for plot names

sig1='Hptb200' # choose the 1st signal to plot
sig1leg='H^{#pm} (0.2 TeV)'
sig2='Hptb300'
sig2leg='H^{#pm} (0.3 TeV)'
plotCombine = True
scaleSignals = True
scaleFact1 = 100
tempsig='templates_'+iPlot+'_'+sig1+'_'+lumiInTemplates+'fb'+isRebinned+'.root'
if plotCombine: tempsig='templates_'+iPlot+'_'+lumiInTemplates+'fb'+isRebinned+'.root'

if splitTTbar: bkgProcList = ['tt2b','ttbb','ttb','ttcc','ttlf','top','ewk','qcd']
else: bkgProcList = ['ttbar','top','ewk','qcd']

if '53' in sig1: bkgHistColors = {'top':kRed-9,'ewk':kBlue-7,'qcd':kOrange-5} #X53X53
elif 'Hptb' in sig1: bkgHistColors = {'ttbar':kGreen-3,'wjets':kPink-4,'tt2b':kGreen+9,'ttbb':kGreen-7,'ttb':kGreen-5,'ttcc':kGreen-3,'ttlf':kGreen+3,'top':kRed-9,'ewk':kMagenta-2,'qcd':kOrange+5} #HTB
else: bkgHistColors = {'top':kAzure+8,'ewk':kMagenta-2,'qcd':kOrange+5} #TT

systematicList = ['pileup','jec','jer','toppt','btag','mistag','scale','trigeff','ht']#,'pdfNew',]
doAllSys = True
doQ2sys  = False
if not doAllSys: doQ2sys = False
addCRsys = False
doNormByBinWidth=False
doOneBand = False
if not doAllSys: doOneBand = True # Don't change this!
blind = True
blindYLD = True
yLog  = False
doRealPull = False
if doRealPull: doOneBand=False
drawYields = False
plotBkgShapes = True #not yet implemented

isEMlist =['E','M']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['1','2','2p','3p']
njetslist = ['3','4','5','6p']
if not isCategorized: 
	nbtaglist = ['1p']
	njetslist = ['3p']
if iPlot=='YLD':
	isCategorized=0
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0p']
	njetslist = ['0p']
tagList = list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))

lumiSys = 0.025 # lumi uncertainty
trigSys = 0.#05 # trigger uncertainty
lepIdSys = 0.03 # lepton id uncertainty
lepIsoSys = 0.01 # lepton isolation uncertainty
corrdSys = math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2) #cheating while total e/m values are close

for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	modelingSys['data_'+modTag] = 0.
	if not addCRsys: #else CR uncertainties are defined in modSyst.py module
		for proc in bkgProcList:
			modelingSys[proc+'_'+modTag] = 0.

def getNormUnc(hist,ibin,modelingUnc):
	contentsquared = hist.GetBinContent(ibin)**2
	error = corrdSys*corrdSys*contentsquared  #correlated uncertainties
	error += modelingUnc*modelingUnc*contentsquared #background modeling uncertainty from CRs
	return error

def formatUpperHist(histogram):
	histogram.GetXaxis().SetLabelSize(0)

	if blind == True:
		histogram.GetXaxis().SetLabelSize(0.045)
		histogram.GetXaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetLabelSize(0.045)
		histogram.GetYaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetTitleOffset(1.15)
		histogram.GetXaxis().SetNdivisions(506)
	else:
		histogram.GetYaxis().SetLabelSize(0.07)
		histogram.GetYaxis().SetTitleSize(0.08)
		histogram.GetYaxis().SetTitleOffset(.71)

	if 'nB0' in histogram.GetName() and 'minMlb' in histogram.GetName(): histogram.GetXaxis().SetTitle("min[M(l,jets)] (GeV)")
	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.000101)
	#if not doNormByBinWidth: histogram.SetMaximum(1.5*histogram.GetMaximum())
	if not yLog: 
		histogram.SetMinimum(0.25)
	if yLog:
		uPad.SetLogy()
		if not doNormByBinWidth: histogram.SetMaximum(200*histogram.GetMaximum())
		else: histogram.SetMaximum(200*histogram.GetMaximum())
		
def formatLowerHist(histogram):
	histogram.GetXaxis().SetLabelSize(.12)
	histogram.GetXaxis().SetTitleSize(0.15)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetXaxis().SetNdivisions(506)

	histogram.GetYaxis().SetLabelSize(0.12)
	histogram.GetYaxis().SetTitleSize(0.14)
	histogram.GetYaxis().SetTitleOffset(.37)
	histogram.GetYaxis().SetTitle('Data/Bkg')
	histogram.GetYaxis().SetNdivisions(5)
	if doRealPull: histogram.GetYaxis().SetRangeUser(min(-2.99,0.8*histogram.GetBinContent(histogram.GetMaximumBin())),max(2.99,1.2*histogram.GetBinContent(histogram.GetMaximumBin())))
	else: 
		if iPlot=='YLD': histogram.GetYaxis().SetRangeUser(0.5,1.5)
		else: histogram.GetYaxis().SetRangeUser(0,2.99)
	histogram.GetYaxis().CenterTitle()

legx1 = 0.65
legx2 = legx1+0.30
legy1 = 0.39
legy2 = legy1+0.50

RFile1 = TFile(templateDir+tempsig.replace(sig1,sig1))
RFile2 = TFile(templateDir+tempsig.replace(sig1,sig2))
print RFile1
bkghists = {}
bkghistsmerged = {}
systHists = {}
totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}
if plotCombine:
	dataName = 'data_obs'
	upTag = 'Up'
	downTag = 'Down'
else: #theta
	dataName = 'DATA'
	upTag = '__plus'
	downTag = '__minus'
blindGlob = blind
for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]
	if isCR(tag[3],tag[2]): 
		postTag = 'isCR_'
		blind = False
	else: 
		postTag = 'isSR_'
		blind = blindGlob
	if not isCategorized: blind = blindGlob
	if not plotCombine: postTag=''
	if skip(tag[3],tag[2]) and isCategorized: continue
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	for isEM in isEMlist:
		histPrefix=iPlot+'_'+lumiInTemplates+'fb_'
		catStr=postTag+'is'+isEM+'_'+tagStr
		histPrefix+=catStr
		print histPrefix
		for proc in bkgProcList: 
			try: bkghists[proc+catStr] = RFile1.Get(histPrefix+'__'+proc).Clone()
			except:
				print "There is no "+proc+"!!!!!!!!"
				print "Skipping "+proc+"....."
				pass
		if blindYLD and iPlot=='YLD': hData = RFile1.Get(histPrefix+'__'+dataName+'_blind').Clone()
		else: hData = RFile1.Get(histPrefix+'__'+dataName).Clone()
		if plotCombine:
			hsig1 = RFile1.Get(histPrefix+'__'+sig1).Clone(histPrefix+'__sig1')
			hsig2 = RFile2.Get(histPrefix+'__'+sig2).Clone(histPrefix+'__sig2')
		else:
			hsig1 = RFile1.Get(histPrefix+'__sig').Clone(histPrefix+'__sig1')
			hsig2 = RFile2.Get(histPrefix+'__sig').Clone(histPrefix+'__sig2')
		hsig1.Scale(xsec[sig1])
		hsig2.Scale(xsec[sig2])
		if doNormByBinWidth:
			for proc in bkgProcList:
				try: normByBinWidth(bkghists[proc+catStr])
				except: pass
			normByBinWidth(hsig1)
			normByBinWidth(hsig2)
			normByBinWidth(hData)

		if doAllSys:
			q2list = []
			if doQ2sys: q2list=['q2']
			print systematicList
			for syst in systematicList+q2list:
				print syst
				for ud in [upTag,downTag]:
					for proc in bkgProcList:
						try: 
							systHists[proc+catStr+syst+ud] = RFile1.Get(histPrefix+'__'+proc+'__'+syst+ud).Clone()
							if doNormByBinWidth: normByBinWidth(systHists[proc+catStr+syst+ud])
						except: pass

		bkgHT = bkghists[bkgProcList[0]+catStr].Clone()
		for proc in bkgProcList:
			if proc==bkgProcList[0]: continue
			try: bkgHT.Add(bkghists[proc+catStr])
			except: pass

		totBkgTemp1[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
		totBkgTemp2[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
		totBkgTemp3[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))
		
		for ibin in range(1,bkghists[bkgProcList[0]+catStr].GetNbinsX()+1):
			errorUp = 0.
			errorDn = 0.
			errorStatOnly = bkgHT.GetBinError(ibin)**2
			errorNorm = 0.
			for proc in bkgProcList:
				try: errorNorm += getNormUnc(bkghists[proc+catStr],ibin,modelingSys[proc+'_'+modTag])
				except: pass

			if doAllSys:
				q2list=[]
				if doQ2sys: q2list=['q2']
				for syst in systematicList+q2list:
					for proc in bkgProcList:
						try:
							errorPlus = systHists[proc+catStr+syst+upTag].GetBinContent(ibin)-bkghists[proc+catStr].GetBinContent(ibin)
							errorMinus = bkghists[proc+catStr].GetBinContent(ibin)-systHists[proc+catStr+syst+downTag].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass

			totBkgTemp1[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
			totBkgTemp1[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
			totBkgTemp2[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
			totBkgTemp2[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
			totBkgTemp3[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
			totBkgTemp3[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
		
		bkgHTgerr = totBkgTemp3[catStr].Clone()

		scaleFact1 = int(bkgHT.GetMaximum()/hsig1.GetMaximum()) - int(bkgHT.GetMaximum()/hsig1.GetMaximum()) % 10
		scaleFact2 = int(bkgHT.GetMaximum()/hsig2.GetMaximum()) - int(bkgHT.GetMaximum()/hsig2.GetMaximum()) % 10
		if scaleFact1==0: scaleFact1=int(bkgHT.GetMaximum()/hsig1.GetMaximum())
		if scaleFact2==0: scaleFact2=int(bkgHT.GetMaximum()/hsig2.GetMaximum())
		if scaleFact1==0: scaleFact1=1
		if scaleFact2==0: scaleFact2=1
		if not scaleSignals:
			scaleFact1=1
			scaleFact2=1
		hsig1.Scale(scaleFact1)
		hsig2.Scale(scaleFact2)

                ############################################################
		############## Making Plots of e+jets, mu+jets and e/mu+jets 
                ############################################################
		
		drawQCD = False
		try: drawQCD = bkghists['qcd'+catStr].Integral()/bkgHT.Integral()>.005 #don't plot QCD if it is less than 0.5%
		except: pass

		stackbkgHT = THStack("stackbkgHT","")
		for proc in bkgProcList:
			try: 
				if drawQCD or proc!='qcd': stackbkgHT.Add(bkghists[proc+catStr])
			except: pass

		sig1Color= kBlack
		sig2Color= kRed
		if '53' in sig1:
			sig1Color= kBlack
			sig2Color= kBlack
			
		for proc in bkgProcList:
			try: 
				bkghists[proc+catStr].SetLineColor(bkgHistColors[proc])
				bkghists[proc+catStr].SetFillColor(bkgHistColors[proc])
				bkghists[proc+catStr].SetLineWidth(2)
			except: pass
			
		if drawYields: 
			bkgHT.SetMarkerSize(4)
			bkgHT.SetMarkerColor(rt.kRed)

		hsig1.SetLineColor(sig1Color)
		hsig1.SetFillStyle(0)
		hsig1.SetLineWidth(3)
		hsig2.SetLineColor(sig2Color)
		hsig2.SetLineStyle(7)#5)
		hsig2.SetFillStyle(0)
		hsig2.SetLineWidth(3)
		
		if not drawYields: hData.SetMarkerStyle(20)
		hData.SetMarkerStyle(20)
		hData.SetMarkerSize(1.2)
		hData.SetLineWidth(2)
		if drawYields: hData.SetMarkerSize(4)

		bkgHTgerr.SetFillStyle(3004)
		bkgHTgerr.SetFillColor(kBlack)

		gStyle.SetOptStat(0)
		c1 = TCanvas("c1","c1",1200,1000)
		gStyle.SetErrorX(0.5)
		yDiv=0.35
		if blind == True: yDiv=0.0
		uMargin = 0
		if blind == True: uMargin = 0.12
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
		else: hData.GetYaxis().SetTitle("Events / bin")
		formatUpperHist(hData)
		uPad.cd()
		hData.SetTitle("")
		if not blind: hData.Draw("E1 X0")
		if blind: 
			hsig1.SetMinimum(0.015)
			if doNormByBinWidth: hsig1.GetYaxis().SetTitle("Events / 1 GeV")
			else: hsig1.GetYaxis().SetTitle("Events / bin")
			formatUpperHist(hsig1)
			hsig1.SetMaximum(hData.GetMaximum())
			hsig1.Draw("HIST")
		stackbkgHT.Draw("SAME HIST")
		if drawYields: 
			rt.gStyle.SetPaintTextFormat("1.0f")
			bkgHT.Draw("SAME TEXT90")
		hsig1.Draw("SAME HIST")
		hsig2.Draw("SAME HIST")
		if not blind: 
			hData.Draw("SAME E1 X0") #redraw data so its not hidden
			if drawYields: hData.Draw("SAME TEXT00") 
		uPad.RedrawAxis()
		bkgHTgerr.Draw("SAME E2")
		
		chLatex = TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.06)
		if blind: chLatex.SetTextSize(0.04)
		chLatex.SetTextAlign(21) # align center
		flvString = ''
		tagString = ''
		if isEM=='E': flvString+='e+jets'
		if isEM=='M': flvString+='#mu+jets'
		if tag[0]!='0p': 
			if 'p' in tag[0]: tagString+='#geq'+tag[0][:-1]+' t, '
			else: tagString+=tag[0]+' t, '
		if tag[1]!='0p': 
			if 'p' in tag[1]: tagString+='#geq'+tag[1][:-1]+' W, '
			else: tagString+=tag[1]+' W, '
		if tag[2]!='0p': 
			if 'p' in tag[2]: tagString+='#geq'+tag[2][:-1]+' b, '
			else: tagString+=tag[2]+' b, '
		if tag[3]!='0p': 
			if 'p' in tag[3]: tagString+='#geq'+tag[3][:-1]+' j'
			else: tagString+=tag[3]+' j'
		if tagString.endswith(', '): tagString = tagString[:-2]
		chLatex.DrawLatex(0.26, 0.84, flvString)
		chLatex.DrawLatex(0.26, 0.78, tagString)

		if drawQCD: leg = TLegend(0.65,0.22,0.95,0.87)
		if not drawQCD or blind: leg = TLegend(0.65,0.24,0.95,0.89)
		leg = TLegend(legx1,legy1,legx2,legy2)
		leg.SetShadowColor(0)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetLineColor(0)
		leg.SetLineStyle(0)
		leg.SetBorderSize(0) 
		leg.SetNColumns(1)
		leg.SetTextFont(62)#42)
		scaleFact1Str = ' x'+str(scaleFact1)
		scaleFact2Str = ' x'+str(scaleFact2)
		if not scaleSignals:
			scaleFact1Str = ''
			scaleFact2Str = ''
		if drawQCD:
			leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
			leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
			leg.AddEntry(bkghists['qcd'+catStr],"QCD","f")
			try: leg.AddEntry(bkghists['ewk'+catStr],"EWK","f")
			except: pass
			if not blind: 
				try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
				except: pass
				try: leg.AddEntry(bkghists['wjets'+catStr],"W+jets","f")
				except: pass
				try: leg.AddEntry(bkghists['wjetsb'+catStr],"W+b","f")
				except: pass
				try: leg.AddEntry(bkghists['wjetsc'+catStr],"W+c","f")
				except: pass
				try: leg.AddEntry(bkghists['wjetsl'+catStr],"W+udsg","f")
				except: pass
				leg.AddEntry(bkgHTgerr,"Bkg uncert.","f")
				try: 
					leg.AddEntry(bkghists['ttbar'+catStr],"t#bar{t}","f")
					leg.AddEntry(0, "", "")
				except: pass
				try: leg.AddEntry(bkghists['tt2b'+catStr],"t#bar{t}+2b","f")
				except: pass
				try: leg.AddEntry(bkghists['ttbb'+catStr],"t#bar{t}+bb","f")
				except: pass
				try: leg.AddEntry(bkghists['ttb'+catStr],"t#bar{t}+b","f")
				except: pass
				try: leg.AddEntry(bkghists['ttcc'+catStr],"t#bar{t}+c","f")
				except: pass
				try: leg.AddEntry(bkghists['ttlf'+catStr],"t#bar{t}+lf","f")
				except: pass
				leg.AddEntry(hData,"DATA")
			else:
				try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
				except: pass
				try: leg.AddEntry(bkghists['wjets'+catStr],"W+jets","f")
				except: pass
				leg.AddEntry(bkgHTgerr,"Bkg uncert.","f")
				try: leg.AddEntry(bkghists['ttbar'+catStr],"t#bar{t}","f")
				except: pass
				
		if not drawQCD:
			leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
			leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
			try: leg.AddEntry(bkghists['ewk'+catStr],"EWK","f")
			except: pass
			try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
			except: pass
			try: leg.AddEntry(bkghists['wjets'+catStr],"W+jets","f")
			except: pass
			try: leg.AddEntry(bkghists['ttbar'+catStr],"t#bar{t}","f")
			except: pass
			leg.AddEntry(bkgHTgerr,"Bkg uncert.","f")
			if not blind: leg.AddEntry(hData,"DATA")
		leg.Draw("same")

		prelimTex=TLatex()
		prelimTex.SetNDC()
		prelimTex.SetTextAlign(31) # align right
		prelimTex.SetTextFont(42)
		prelimTex.SetTextSize(0.07)
		if blind: prelimTex.SetTextSize(0.05)
		prelimTex.SetLineWidth(2)
		prelimTex.DrawLatex(0.95,0.92,str(lumi)+" fb^{-1} (13 TeV)")

		prelimTex2=TLatex()
		prelimTex2.SetNDC()
		prelimTex2.SetTextFont(61)
		prelimTex2.SetLineWidth(2)
		prelimTex2.SetTextSize(0.10)
		if blind: prelimTex2.SetTextSize(0.08)
		prelimTex2.DrawLatex(0.22,0.92,"CMS")

		prelimTex3=TLatex()
		prelimTex3.SetNDC()
		prelimTex3.SetTextAlign(13)
		prelimTex3.SetTextFont(52)
		prelimTex3.SetTextSize(0.075)
		if blind: prelimTex3.SetTextSize(0.055)
		prelimTex3.SetLineWidth(2)
		if not blind: prelimTex3.DrawLatex(0.34,0.975,"Preliminary")
		if blind: prelimTex3.DrawLatex(0.36,0.96,"Preliminary")

		if blind == False and not doRealPull:
			lPad.cd()
			pull=hData.Clone("pull")
			pull.Divide(hData, bkgHT)
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pull.SetBinError(binNo,hData.GetBinError(binNo)/bkgHT.GetBinContent(binNo))
			if iPlot=='YLD':
				pull.SetMaximum(1.5)
				pull.SetMinimum(0.5)
			else: 
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
					pullUncBandTot.SetPointEYhigh(binNo-1,totBkgTemp3[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandTot.SetPointEYlow(binNo-1,totBkgTemp3[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
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
					pullUncBandNorm.SetPointEYhigh(binNo-1,totBkgTemp2[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandNorm.SetPointEYlow(binNo-1,totBkgTemp2[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandNorm.SetFillStyle(3001)
			pullUncBandNorm.SetFillColor(2)
			pullUncBandNorm.SetLineColor(2)
			pullUncBandNorm.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandNorm.Draw("SAME E2")
			
			pullUncBandStat=TGraphAsymmErrors(BkgOverBkg.Clone("pulluncStat"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandStat.SetPointEYhigh(binNo-1,totBkgTemp1[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandStat.SetPointEYlow(binNo-1,totBkgTemp1[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandStat.SetFillStyle(3001)
			pullUncBandStat.SetFillColor(3)
			pullUncBandStat.SetLineColor(3)
			pullUncBandStat.SetMarkerSize(0)
			gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandStat.Draw("SAME E2")

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
			if not doOneBand: 
				pullLegend.AddEntry(pullUncBandStat , "Bkg uncert. (shape syst.)" , "f")
				pullLegend.AddEntry(pullUncBandNorm , "Bkg uncert. (shape #oplus norm. syst.)" , "f")
				pullLegend.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus all syst.)" , "f")
			elif not doAllSys: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus norm.)" , "f")
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
					MCerror = 0.5*(totBkgTemp3[catStr].GetErrorYhigh(binNo-1)+totBkgTemp3[catStr].GetErrorYlow(binNo-1))
					pull.SetBinContent(binNo,(hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(MCerror**2+hData.GetBinError(binNo)**2))
				else: pull.SetBinContent(binNo,0.)
			pull.SetMaximum(3)
			pull.SetMinimum(-3)
			if '53' in sig1:
				pull.SetFillColor(2)
				pull.SetLineColor(2)
			else:
				pull.SetFillColor(kGray+2)
				pull.SetLineColor(kGray+2)
			formatLowerHist(pull)
			pull.GetYaxis().SetTitle('Pull')
			pull.Draw("HIST")

		#c1.Write()
		savePrefix = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
		if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix+isRebinned.replace('_rebinned_stat1p1','')+saveKey
		if nttaglist[0]=='0p': savePrefix=savePrefix.replace('nT0p_','')
		if nWtaglist[0]=='0p': savePrefix=savePrefix.replace('nW0p_','')
		if nbtaglist[0]=='0p': savePrefix=savePrefix.replace('nB0p_','')
		if njetslist[0]=='0p': savePrefix=savePrefix.replace('nJ0p_','')
		if doRealPull: savePrefix+='_pull'
		if doNormByBinWidth: savePrefix+='_NBBW'
		if yLog: savePrefix+='_logy'
		if blind or blindYLD: savePrefix+='_blind'

		if doOneBand:
			c1.SaveAs(savePrefix+"totBand.pdf")
			c1.SaveAs(savePrefix+"totBand.png")
			c1.SaveAs(savePrefix+"totBand.eps")
			#c1.SaveAs(savePrefix+"totBand.root")
			#c1.SaveAs(savePrefix+"totBand.C")
		else:
			c1.SaveAs(savePrefix+".pdf")
			c1.SaveAs(savePrefix+".png")
			c1.SaveAs(savePrefix+".eps")
			#c1.SaveAs(savePrefix+".root")
			#c1.SaveAs(savePrefix+".C")
		for proc in bkgProcList:
			try: del bkghists[proc+catStr]
			except: pass
					
	# Making plots for e+jets/mu+jets combined #
	histPrefixE = iPlot+'_'+lumiInTemplates+'fb_'+postTag+'isE_'+tagStr
	histPrefixM = iPlot+'_'+lumiInTemplates+'fb_'+postTag+'isM_'+tagStr
	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr] = RFile1.Get(histPrefixE+'__'+proc).Clone()
			bkghistsmerged[proc+'isL'+tagStr].Add(RFile1.Get(histPrefixM+'__'+proc))
		except:pass
	if blindYLD and iPlot=='YLD': hDatamerged = RFile1.Get(histPrefixE+'__'+dataName+'_blind').Clone()
	else: hDatamerged = RFile1.Get(histPrefixE+'__'+dataName).Clone()
	if blindYLD and iPlot=='YLD': hDatamerged.Add(RFile1.Get(histPrefixM+'__DATA_blind').Clone())
	else: hDatamerged.Add(RFile1.Get(histPrefixM+'__'+dataName).Clone())
	if plotCombine: 
		hsig1merged = RFile1.Get(histPrefixE+'__'+sig1).Clone(histPrefixE+'__sig1merged')
		hsig2merged = RFile2.Get(histPrefixE+'__'+sig2).Clone(histPrefixE+'__sig2merged')
		hsig1merged.Add(RFile1.Get(histPrefixM+'__'+sig1).Clone())
		hsig2merged.Add(RFile2.Get(histPrefixM+'__'+sig2).Clone())
	else:
		hsig1merged = RFile1.Get(histPrefixE+'__sig').Clone(histPrefixE+'__sig1merged')
		hsig2merged = RFile2.Get(histPrefixE+'__sig').Clone(histPrefixE+'__sig2merged')
		hsig1merged.Add(RFile1.Get(histPrefixM+'__sig').Clone())
		hsig2merged.Add(RFile2.Get(histPrefixM+'__sig').Clone())
	hsig1merged.Scale(xsec[sig1])
	hsig2merged.Scale(xsec[sig2])
	if doNormByBinWidth:
		for proc in bkgProcList:
			try: normByBinWidth(bkghistsmerged[proc+'isL'+tagStr])
			except: pass
		normByBinWidth(hsig1merged)
		normByBinWidth(hsig2merged)
		normByBinWidth(hDatamerged)

	if doAllSys:
		q2list=[]
		if doQ2sys: q2list=['q2']
		for syst in systematicList+q2list:
			for ud in [upTag,downTag]:
				for proc in bkgProcList:
					try: 
						systHists[proc+'isL'+tagStr+syst+ud] = systHists[proc+postTag+'isE_'+tagStr+syst+ud].Clone()
						systHists[proc+'isL'+tagStr+syst+ud].Add(systHists[proc+postTag+'isM_'+tagStr+syst+ud])
					except: pass

	bkgHTmerged = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone()
	for proc in bkgProcList:
		if proc==bkgProcList[0]: continue
		try: bkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass

	totBkgTemp1['isL'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapeOnly'))
	totBkgTemp2['isL'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapePlusNorm'))
	totBkgTemp3['isL'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'All'))
	
	for ibin in range(1,bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetNbinsX()+1):
		errorUp = 0.
		errorDn = 0.
		errorStatOnly = bkgHTmerged.GetBinError(ibin)**2
		errorNorm = 0.
		for proc in bkgProcList:
			try: errorNorm += getNormUnc(bkghistsmerged[proc+'isL'+tagStr],ibin,modelingSys[proc+'_'+modTag])
			except: pass

		if doAllSys:
			q2list=[]
			if doQ2sys: q2list=['q2']
			for syst in systematicList+q2list:
				for proc in bkgProcList:
					try:
						errorPlus = systHists[proc+'isL'+tagStr+syst+upTag].GetBinContent(ibin)-bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)
						errorMinus = bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)-systHists[proc+'isL'+tagStr+syst+downTag].GetBinContent(ibin)
						if errorPlus > 0: errorUp += errorPlus**2
						else: errorDn += errorPlus**2
						if errorMinus > 0: errorDn += errorMinus**2
						else: errorUp += errorMinus**2
					except: pass

		totBkgTemp1['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
		totBkgTemp1['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
		totBkgTemp2['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
		totBkgTemp2['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
		totBkgTemp3['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatOnly))
		totBkgTemp3['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatOnly))
	
	bkgHTgerrmerged = totBkgTemp3['isL'+tagStr].Clone()

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
	
	drawQCDmerged = False
	try: drawQCDmerged = bkghistsmerged['qcdisL'+tagStr].Integral()/bkgHTmerged.Integral()>.005
	except: pass

	stackbkgHTmerged = THStack("stackbkgHTmerged","")
	for proc in bkgProcList:
		try: 
			if drawQCDmerged or proc!='qcd': stackbkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass

	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr].SetLineColor(bkgHistColors[proc])
			bkghistsmerged[proc+'isL'+tagStr].SetFillColor(bkgHistColors[proc])
			bkghistsmerged[proc+'isL'+tagStr].SetLineWidth(2)
		except: pass
	if drawYields: 
		bkgHTmerged.SetMarkerSize(4)
		bkgHTmerged.SetMarkerColor(rt.kRed)

	hsig1merged.SetLineColor(sig1Color)
	hsig1merged.SetFillStyle(0)
	hsig1merged.SetLineWidth(3)
	hsig2merged.SetLineColor(sig2Color)
	hsig2merged.SetLineStyle(7)#5)
	hsig2merged.SetFillStyle(0)
	hsig2merged.SetLineWidth(3)
	
	if not drawYields: hDatamerged.SetMarkerStyle(20)
	hDatamerged.SetMarkerStyle(20)
	hDatamerged.SetMarkerSize(1.2)
	hDatamerged.SetLineWidth(2)
	if drawYields: hDatamerged.SetMarkerSize(4)

	bkgHTgerrmerged.SetFillStyle(3004)
	bkgHTgerrmerged.SetFillColor(kBlack)

	gStyle.SetOptStat(0)
	c1merged = TCanvas("c1merged","c1merged",1200,1000)
	gStyle.SetErrorX(0.5)
	yDiv=0.35
	if blind == True: yDiv=0.0
	uMargin = 0
	if blind == True: uMargin = 0.12
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
	else: hDatamerged.GetYaxis().SetTitle("Events / bin")
	formatUpperHist(hDatamerged)
	uPad.cd()
	hDatamerged.SetTitle("")
	stackbkgHTmerged.SetTitle("")
	if not blind: hDatamerged.Draw("E1 X0")
	if blind: 
		hsig1merged.SetMinimum(0.015)
		if doNormByBinWidth: hsig1merged.GetYaxis().SetTitle("Events / 1 GeV")
		else: hsig1merged.GetYaxis().SetTitle("Events / bin")
		formatUpperHist(hsig1merged)
		hsig1merged.SetMaximum(hDatamerged.GetMaximum())
		hsig1merged.Draw("HIST")
	stackbkgHTmerged.Draw("SAME HIST")
	if drawYields: 
		rt.gStyle.SetPaintTextFormat("1.0f")
		bkgHTmerged.Draw("SAME TEXT90")
	hsig1merged.Draw("SAME HIST")
	hsig2merged.Draw("SAME HIST")
	if not blind: 
		hDatamerged.Draw("SAME E1 X0") #redraw data so its not hidden
		if drawYields: hDatamerged.Draw("SAME TEXT00") 
	uPad.RedrawAxis()
	bkgHTgerrmerged.Draw("SAME E2")

	chLatexmerged = TLatex()
	chLatexmerged.SetNDC()
	chLatexmerged.SetTextSize(0.06)
	if blind: chLatexmerged.SetTextSize(0.04)
	chLatexmerged.SetTextAlign(21) # align center
	flvString = 'e/#mu+jets'
	tagString = ''
	if tag[0]!='0p':
		if 'p' in tag[0]: tagString+='#geq'+tag[0][:-1]+' t, '
		else: tagString+=tag[0]+' t,  '
	if tag[1]!='0p':
		if 'p' in tag[1]: tagString+='#geq'+tag[1][:-1]+' W, '
		else: tagString+=tag[1]+' W, '
	if tag[2]!='0p':
		if 'p' in tag[2]: tagString+='#geq'+tag[2][:-1]+' b, '
		else: tagString+=tag[2]+' b, '
	if tag[3]!='0p':
		if 'p' in tag[3]: tagString+='#geq'+tag[3][:-1]+' j'
		else: tagString+=tag[3]+' j'
	if tagString.endswith(', '): tagString = tagString[:-2]
	chLatexmerged.DrawLatex(0.26, 0.85, flvString)
	chLatexmerged.DrawLatex(0.26, 0.78, tagString)

	if drawQCDmerged: legmerged = TLegend(0.35,0.55,0.95,0.87)
	if not drawQCDmerged or blind: legmerged = TLegend(0.35,0.55,0.95,0.89)
	legmerged = TLegend(legx1,legy1,legx2,legy2)
	legmerged.SetShadowColor(0)
	legmerged.SetFillColor(0)
	legmerged.SetFillStyle(0)
	legmerged.SetLineColor(0)
	legmerged.SetLineStyle(0)
	legmerged.SetBorderSize(0) 
	legmerged.SetNColumns(1)
	legmerged.SetTextFont(62)#42)
	scaleFact1Str = ' x'+str(scaleFact1)
	scaleFact2Str = ' x'+str(scaleFact2)
	if not scaleSignals:
		scaleFact1Str = ''
		scaleFact2Str = ''
	if drawQCDmerged:
		legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
		legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
		legmerged.AddEntry(bkghistsmerged['qcdisL'+tagStr],"QCD","f")
		try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EWK","f")
		except: pass
		if not blind: 
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['wjetsisL'+tagStr],"W+jets","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['wjetsbisL'+tagStr],"W+b","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['wjetscisL'+tagStr],"W+c","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['wjetslisL'+tagStr],"W+udsg","f")
			except: pass
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncert.","f")
			try: 
				legmerged.AddEntry(bkghistsmerged['ttbarisL'+tagStr],"t#bar{t}","f")
				legmerged.AddEntry(0, "", "")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['tt2bisL'+tagStr],"t#bar{t}+2b","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ttbbisL'+tagStr],"t#bar{t}+bb","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ttbisL'+tagStr],"t#bar{t}+b","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ttccisL'+tagStr],"t#bar{t}+c","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ttlfisL'+tagStr],"t#bar{t}+lf","f")
			except: pass
			legmerged.AddEntry(hDatamerged,"DATA")
		else:
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['wjetsisL'+tagStr],"W+jets","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['wjetsbisL'+tagStr],"W+b","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['wjetscisL'+tagStr],"W+c","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['wjetslisL'+tagStr],"W+udsg","f")
			except: pass
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncert.","f")
			try: legmerged.AddEntry(bkghistsmerged['ttbarisL'+tagStr],"t#bar{t}","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['tt2bisL'+tagStr],"t#bar{t}+2b","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ttbbisL'+tagStr],"t#bar{t}+bb","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ttbisL'+tagStr],"t#bar{t}+b","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ttccisL'+tagStr],"t#bar{t}+c","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ttlfisL'+tagStr],"t#bar{t}+lf","f")
			except: pass
	if not drawQCDmerged:
		legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
		legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
		try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EWK","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['wjetsisL'+tagStr],"W+jets","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['wjetsbisL'+tagStr],"W+b","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['wjetscisL'+tagStr],"W+c","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['wjetslisL'+tagStr],"W+udsg","f")
		except: pass
		legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncert.","f")
		try: legmerged.AddEntry(bkghistsmerged['ttbarisL'+tagStr],"t#bar{t}","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['tt2bisL'+tagStr],"t#bar{t}+2b","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['ttbbisL'+tagStr],"t#bar{t}+bb","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['ttbisL'+tagStr],"t#bar{t}+b","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['ttccisL'+tagStr],"t#bar{t}+c(c)","f")
		except: pass
		try: legmerged.AddEntry(bkghistsmerged['ttlfisL'+tagStr],"t#bar{t}+lf","f")
		except: pass
		if not blind: legmerged.AddEntry(hDatamerged,"DATA")
	legmerged.Draw("same")

	prelimTex=TLatex()
	prelimTex.SetNDC()
	prelimTex.SetTextAlign(31) # align right
	prelimTex.SetTextFont(42)
	prelimTex.SetTextSize(0.07)
	if blind: prelimTex.SetTextSize(0.05)
	prelimTex.SetLineWidth(2)
	prelimTex.DrawLatex(0.95,0.92,str(lumi)+" fb^{-1} (13 TeV)")
	
	prelimTex2=TLatex()
	prelimTex2.SetNDC()
	prelimTex2.SetTextFont(61)
	prelimTex2.SetLineWidth(2)
	prelimTex2.SetTextSize(0.10)
	if blind: prelimTex2.SetTextSize(0.08)
	prelimTex2.DrawLatex(0.22,0.92,"CMS")
	
	prelimTex3=TLatex()
	prelimTex3.SetNDC()
	prelimTex3.SetTextAlign(13)
	prelimTex3.SetTextFont(52)
	prelimTex3.SetTextSize(0.075)
	if blind: prelimTex3.SetTextSize(0.055)
	prelimTex3.SetLineWidth(2)
	if not blind: prelimTex3.DrawLatex(0.34,0.975,"Preliminary")
	if blind: prelimTex3.DrawLatex(0.36,0.96,"Preliminary")
	
	if blind == False and not doRealPull:
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		pullmerged.Divide(hDatamerged, bkgHTmerged)
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pull.SetBinError(binNo,hDatamerged.GetBinError(binNo)/bkgHTmerged.GetBinContent(binNo))
		if iPlot=='YLD':
			pullmerged.SetMaximum(1.5)
			pullmerged.SetMinimum(0.5)
		else:
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
				pullUncBandTotmerged.SetPointEYhigh(binNo-1,totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandTotmerged.SetPointEYlow(binNo-1, totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
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
				pullUncBandNormmerged.SetPointEYhigh(binNo-1,totBkgTemp2['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandNormmerged.SetPointEYlow(binNo-1, totBkgTemp2['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandNormmerged.SetFillStyle(3001)
		pullUncBandNormmerged.SetFillColor(2)
		pullUncBandNormmerged.SetLineColor(2)
		pullUncBandNormmerged.SetMarkerSize(0)
		gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandNormmerged.Draw("SAME E2")
		
		pullUncBandStatmerged=TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncStatmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandStatmerged.SetPointEYhigh(binNo-1,totBkgTemp1['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandStatmerged.SetPointEYlow(binNo-1, totBkgTemp1['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
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
		if not doOneBand: 
			pullLegendmerged.AddEntry(pullUncBandStat , "Bkg uncert. (shape syst.)" , "f")
			pullLegendmerged.AddEntry(pullUncBandNorm , "Bkg uncert. (shape #oplus norm. syst.)" , "f")
			pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus all syst.)" , "f")
		elif not doAllSys: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus norm.)" , "f")
		else: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert. (stat. #oplus syst.)" , "f")
		pullLegendmerged.Draw("SAME")
		pullmerged.Draw("SAME")
		lPad.RedrawAxis()

	if blind == False and doRealPull:
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if hDatamerged.GetBinContent(binNo)!=0:
				MCerror = 0.5*(totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)+totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1))
				pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(MCerror**2+hDatamerged.GetBinError(binNo)**2))
			else: pullmerged.SetBinContent(binNo,0.)
		pullmerged.SetMaximum(3)
		pullmerged.SetMinimum(-3)
		if '53' in sig1:
			pullmerged.SetFillColor(2)
			pullmerged.SetLineColor(2)
		else:
			pullmerged.SetFillColor(kGray+2)
			pullmerged.SetLineColor(kGray+2)
		formatLowerHist(pullmerged)
		pullmerged.GetYaxis().SetTitle('Pull')
		pullmerged.Draw("HIST")

	#c1merged.Write()
	savePrefixmerged = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('isE','isL')+isRebinned.replace('_rebinned_stat1p1','')+saveKey
	if nttaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nT0p_','')
	if nWtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nW0p_','')
	if nbtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nB0p_','')
	if njetslist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nJ0p_','')
	if doRealPull: savePrefixmerged+='_pull'
	if doNormByBinWidth: savePrefixmerged+='_NBBW'
	if yLog: savePrefixmerged+='_logy'
	if blind or blindYLD: savePrefixmerged+='_blind'

	if doOneBand: 
		c1merged.SaveAs(savePrefixmerged+"totBand.pdf")
		c1merged.SaveAs(savePrefixmerged+"totBand.png")
		c1merged.SaveAs(savePrefixmerged+"totBand.eps")
		#c1merged.SaveAs(savePrefixmerged+"totBand.root")
		#c1merged.SaveAs(savePrefixmerged+"totBand.C")
	else: 
		c1merged.SaveAs(savePrefixmerged+".pdf")
		c1merged.SaveAs(savePrefixmerged+".png")
		c1merged.SaveAs(savePrefixmerged+".eps")
		#c1merged.SaveAs(savePrefixmerged+".root")
		#c1merged.SaveAs(savePrefixmerged+".C")
	for proc in bkgProcList:
		try: del bkghistsmerged[proc+'isL'+tagStr]
		except: pass
			
RFile1.Close()
RFile2.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


