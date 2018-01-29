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

region='CR' #SR,TTCR,WJCR
isCategorized=True
isNoB0 = True
isNoCRHB0 = False
iPlot='HT'#minMlbST'
if len(sys.argv)>1: iPlot=str(sys.argv[1])
cutString='splitLess'#lep40_MET60_DR0_1jet200_2jet100'
if region=='SR': pfix='templates4CRhtSR_'#+iPlot
elif region=='WJCR': pfix='wjets_'#+iPlot
elif region=='TTCR': pfix='ttbar_'#+iPlot
elif region=='HCR': pfix='higgs_'#+iPlot
elif region=='CR': pfix='templates4CRhtSR_'
elif region=='CRall': pfix='control_'
if not isCategorized: pfix='kinematics_'+region+'_'
pfix+='NewEl'
if len(sys.argv)>2: region=str(sys.argv[2])
if len(sys.argv)>3: pfix=str(sys.argv[3])
templateDir=os.getcwd()+'/../makeTemplates/'+pfix+'/'+cutString+'/'
#limitDir=os.getcwd()+'/limitsAug17/'+pfix.replace('NewEl','bkgonly_postfit/')
limitDir=os.getcwd()+'/limitsAug17/'+pfix.replace('NewEl','postfit/')

isRebinned='_BKGNORM_rebinned_stat0p3' #post for ROOT file names
saveKey = '' # tag for plot names

sig1='TTM1000_bW0p5_tZ0p25_tH0p25' #  choose the 1st signal to plot
sig1leg='T#bar{T} (1.0 TeV)'
sig2='TTM1200_bW0p5_tZ0p25_tH0p25' #  choose the 2nd signal to plot
sig2leg='T#bar{T} (1.2 TeV)'
drawNormalized = False # STACKS CAN'T DO THIS...bummer
scaleSignals = False
if not isCategorized and 'CR' not in region: scaleSignals = True
sigScaleFact = 100
if 'SR' in region: sigScaleFact = 50
if 'Nm1' in iPlot: sigScaleFact = sigScaleFact/5
print 'Scaling signals?',scaleSignals
print 'Scale factor = ',sigScaleFact
tempsig='templates_minMlbST_'+sig1+'_'+lumiInTemplates+'fb'+isRebinned+'.root'

bkgProcList = ['TTbar','SingleTop','EWK','QCD']
if '53' in sig1: bkgHistColors = {'top':kRed-9,'ewk':kBlue-7,'qcd':kOrange-5} #X53X53
elif 'HTB' in sig1: bkgHistColors = {'ttbar':kGreen-3,'wjets':kPink-4,'top':kAzure+8,'ewk':kMagenta-2,'qcd':kOrange+5} #HTB
else: bkgHistColors = {'TTbar':kAzure+6,'SingleTop':kAzure+6,'EWK':kMagenta-3,'QCD':kOrange+7} #TT

systematicList = ['tau21','jmr','jms','pileup','jec','jer','muRFcorrdNewTTbar','TTbarscale','muRFcorrdNewSingleTop','SingleTopscale','muRFcorrdNewEwk1L','EWKscale','muRFcorrdNewQCD','QCDscale','pdfNew','btag','mistag','trigeffEl','trigeffMu','taupt','elIdSys','elIsoSys','elRecoSys','muIdSys','muIsoSys','muRecoSys','lumiSys','htag_prop']
if 'WJCRnoJSF' in pfix or 'WJCRwSFs' in pfix or 'TTCRwNewWgt' in pfix: systematicList = ['tau21','pileup','jec','jer','muRFcorrdNew','pdfNew','toppt']
if 'WJCRwJSF' in pfix: systematicList = ['tau21','pileup','jec','jer','muRFcorrdNew','pdfNew','toppt','jsf']
if 'TTCRnoJSF' in pfix: systematicList = ['tau21','pileup','jec','jer','muRFcorrdNew','pdfNew']

doAllSys = True
doQ2sys  = False
if not doAllSys: doQ2sys = False
addCRsys = False
doNormByBinWidth=True
doOneBand = False
if not doAllSys: doOneBand = True # Don't change this!
blind = False
yLog  = True
if yLog: scaleSignals = False
doRealPull = True
if doRealPull: doOneBand=False
compareShapes = False
if compareShapes: blind,yLog=True,False
histrange = {}

isEMlist =['E','M']
#isEMlist =['M']
if region=='SR': nHtaglist=['0','1b','2b']
elif 'CR' in region:
	if region=='HCR': nHtaglist=['1b','2b']
	elif region=='CR': nHtaglist=['0','1p']
	elif region=='CRall': nHtaglist=['0','1b','2b']
	else: nHtaglist=['0']
else: nHtaglist = ['0p']

if region=='TTCR' or region=='HCR' or region=='CR': nWtaglist = ['0p']
else: nWtaglist=['0','0p','1p']

if region=='WJCR': nbtaglist = ['0']
elif region=='HCR' or region=='CR': nbtaglist = ['0','1p']
else: nbtaglist=['0','1','1p','2','3p']
if not isCategorized: 	
	nHtaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0p']
	if region=='WJCR': nbtaglist = ['0']
	if region=='TTCR': nbtaglist = ['1p']
	if region=='HCR': 
		nHtaglist = ['1b','2b']
		nbtaglist = ['1p']
njetslist = ['3p']
if region=='PS': njetslist = ['3p']
if iPlot=='YLD':
	doNormByBinWidth = False
	nHtaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0p']
	njetslist = ['0p']

tagList = []
if isCategorized and iPlot != 'YLD':
	for item in list(itertools.product(nHtaglist,nWtaglist,nbtaglist,njetslist)):
		if 'b' in item[0]:
			if isNoB0 and item[2] == '0': continue
			if item[1] != '0p': continue
			if region == 'CRall':
				if item[2] != '0' and item[2] != '1p': continue
			else:
				if item[2] != '1p' and region != 'WJCR' and region != 'HCR' and region != 'CR': continue
		elif 'b' not in item[0]:
			
			if region == 'CRall':
				if item[1] == '0' and item[2] != '0': continue
				elif item[1] == '1p' and item[2] != '0': continue
				elif item[1] == '0p' and (item[2] == '0' or item[2] == '1p'): continue
			else:				
				if item[1] == '0p' and region != 'TTCR' and region != 'HCR' and region != 'CR': continue
				if item[2] == '1p' and region != 'CR': continue
				if (isNoB0 or isNoCRHB0) and item[0] == '1p' and item[2] == '0': continue
				if isNoB0 and item[0] == '0' and item[2] == '0' and region != 'CR': continue
		tag = [item[0],item[1],item[2],item[3]]
		tagList.append(tag)
else: tagList = list(itertools.product(nHtaglist,nWtaglist,nbtaglist,njetslist))

lumiSys = 0 #math.sqrt(0.025**2 + 0.05**2) # lumi uncertainty plus higgs prop
trigSys = 0.00 # trigger uncertainty, now really reco uncertainty
lepIdSys = 0.00 # lepton id uncertainty
lepIsoSys = 0.00 # lepton isolation uncertainty
corrdSys = 0 #math.sqrt(lumiSys**2+trigSys**2+lepIdSys**2+lepIsoSys**2) #cheating while total e/m values are close

for tag in tagList:
	tagStr='nH'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]  #+'_nJ'+tag[3]
	modTag = tagStr[tagStr.find('nH'):tagStr.find('nJ')-3]	
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
	histogram.GetXaxis().SetRangeUser(histrange[0],histrange[1])
	if blind == True:
		histogram.GetXaxis().SetLabelSize(0.045)
		histogram.GetXaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetLabelSize(0.04)
		histogram.GetYaxis().SetTitleSize(0.05)
		histogram.GetYaxis().SetTitleOffset(1.1)
		histogram.GetXaxis().SetNdivisions(506)
		if 'YLD' in iPlot: histogram.GetXaxis().LabelsOption("u")
	else:
		histogram.GetYaxis().SetLabelSize(0.05)
		histogram.GetYaxis().SetTitleSize(0.06)
		histogram.GetYaxis().SetTitleOffset(.78)

	print 'Formatting upper histogram:',histogram.GetName()
	if 'nB0_' in histogram.GetName() and 'minMlb' in histogram.GetName(): 
		print 'Found b0, changing title'
		histogram.GetXaxis().SetTitle("min[M(l,j)], j#neqb [GeV]")
	#histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.00101)
	if 'H1b' in histogram.GetName(): histogram.SetMinimum(0.000101)
	if 'H2b' in histogram.GetName(): histogram.SetMinimum(0.0000101)
	if not yLog: 
		histogram.SetMinimum(0.25)
	if yLog:
		uPad.SetLogy()
		if not doNormByBinWidth: histogram.SetMaximum(200*histogram.GetMaximum())
		else: 
			histogram.SetMaximum(200*histogram.GetMaximum())
		if iPlot=='YLD': 
			histogram.SetMaximum(200*histogram.GetMaximum())
			histogram.SetMinimum(0.1)

		
def formatLowerHist(histogram):
	histogram.GetXaxis().SetLabelSize(.15)
	histogram.GetXaxis().SetTitleSize(0.18)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetXaxis().SetNdivisions(506)
	#histogram.GetXaxis().SetTitle("S_{T} (GeV)")
	if 'YLD' in iPlot: histogram.GetXaxis().LabelsOption("u")

	histogram.GetYaxis().SetLabelSize(0.15)
	histogram.GetYaxis().SetTitleSize(0.145)
	histogram.GetYaxis().SetTitleOffset(.3)
	if not doRealPull: histogram.GetYaxis().SetTitle('Data/Bkg')
	else: histogram.GetYaxis().SetTitle('#frac{(data-bkg)}{std. dev.}')
	histogram.GetYaxis().SetNdivisions(7)
	if doRealPull: histogram.GetYaxis().SetRangeUser(-2.99,2.99)
	elif yLog and doNormByBinWidth: histogram.GetYaxis().SetRangeUser(0.1,1.9)
	else: histogram.GetYaxis().SetRangeUser(0.4,1.6)
	histogram.GetYaxis().CenterTitle()

RFile1 = TFile(templateDir+tempsig.replace(sig1,sig1))
RFile2 = TFile(templateDir+tempsig.replace(sig1,sig2))
#RFilePost = TFile(limitDir+'/histos-mle_All.root')
RFilePost = TFile(limitDir+'/histos-mle_AllNoB0.root')
print RFile1
bkghists = {}
bkghistsmerged = {}
systHists = {}
totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}
for tag in tagList:
	tagStr='nH'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]  #+'_nJ'+tag[3]
	modTag = tagStr[tagStr.find('nH'):tagStr.find('nJ')-3]
	#tagStr = tagStr.replace('nH','nT')
	#modTag = modTag.replace('nH','nT')
	for isEM in isEMlist:
		histPrefix=iPlot+'_'+lumiInTemplates+'fb_'
		catStr='is'+isEM+'_'+tagStr
		histPrefix+=catStr
		if region=='SR': histPrefix+='_isSR'
		else: histPrefix+='_isCR'
		print histPrefix

		# Backgrounds taken from input file for stat uncerts, from postfit file for yields
		totBkg = 0.
		#testbkght = RFile1.Get(histPrefix+'__'+bkgProcList[0]).Clone('testbkght') 
		for proc in bkgProcList: 
			try: 				
				binshist = RFile1.Get(histPrefix+'__'+proc).Clone()  #Get the rebinned histogram
				#if proc != bkgProcList[0]: testbkght.Add(binshist)
				bkghists[proc+catStr] = binshist.Clone(binshist.GetName()+'_post') # Clone and rename into the container
				temphist = RFilePost.Get(histPrefix+'__'+proc) #Get the postfit histogram
				for ibin in range(1,binshist.GetNbinsX()+1):					
					bkghists[proc+catStr].SetBinContent(ibin,temphist.GetBinContent(ibin)) # Change bin content in the container
					if binshist.GetBinContent(ibin)==0: percentstaterr = 0
					else: 
						percentstaterr = binshist.GetBinError(ibin)/binshist.GetBinContent(ibin) #get the % stat error
						#if proc == 'TTbar': print 'percent stat err =',percentstaterr
					bkghists[proc+catStr].SetBinError(ibin,temphist.GetBinContent(ibin)*percentstaterr) # Change bin error in the container
				totBkg += bkghists[proc+catStr].Integral()
			except:
				print "Something failed for "+proc
				print "tried to open "+histPrefix+'__'+proc
				pass

		# Data and signals opened from the input file
		hData = RFile1.Get(histPrefix+'__DATA').Clone()
		histrange = [hData.GetBinLowEdge(1),hData.GetBinLowEdge(hData.GetNbinsX()+1)]
		gaeData = TGraphAsymmErrors(hData.Clone(hData.GetName().replace('DATA','gaeDATA')))
		hsig1 = RFile1.Get(histPrefix+'__sig').Clone(histPrefix+'__sig1')
		hsig2 = RFile2.Get(histPrefix+'__sig').Clone(histPrefix+'__sig2')
		hsig1.Scale(xsec[sig1[:7]])
		hsig2.Scale(xsec[sig2[:7]])

		bkgHT = bkghists[bkgProcList[0]+catStr].Clone()
		for proc in bkgProcList:
			if proc==bkgProcList[0]: continue
			try: bkgHT.Add(bkghists[proc+catStr])
			except: pass
		gaeBkgHT = TGraphAsymmErrors(bkgHT.Clone("gaeBkgHT"))		

		#for ibin in range(1,10):
		#	print 'New:',bkgHT.GetBinContent(ibin)
		#	print 'Old:',testbkght.GetBinContent(ibin)
		#testbkght.Reset()

		if doNormByBinWidth:
			poissonNormByBinWidth(gaeData,hData)
			for proc in bkgProcList:
				try: normByBinWidth(bkghists[proc+catStr])
				except: pass
			normByBinWidth(hsig1)
			normByBinWidth(hsig2)
			normByBinWidth(hData)
		else: poissonErrors(gaeData)
		# Yes, there are easier ways using the TH1's but
		# it would be rough to swap objects lower down

		if doNormByBinWidth: 
			normByBinWidth(bkgHT)
			poissonNormByBinWidth(gaeBkgHT,bkgHT)
		else: poissonErrors(gaeBkgHT)

		# print 'bkgHT bin 1 yield:',bkgHT.GetBinContent(1)
		# yvals = gaeBkgHT.GetY()
		# yvalsup = gaeBkgHT.GetEYhigh()
		# yvalsdn = gaeBkgHT.GetEYlow()
		# print 'gaeBkgHT point 0 yval:',yvals[0],'+',yvalsup[0],'-',yvalsdn[0]


		if doAllSys:
			q2list = []
			if doQ2sys: q2list=['q2']
			#print systematicList
			for syst in systematicList+q2list:
				#print syst
				for ud in ['minus','plus']:
					for proc in bkgProcList:
						#RFileName = 'histos-mle_'+syst+'_'+ud+'_All_bkgonly.root'
						#RFileName = 'histos-mle_'+syst+'_'+ud+'_All_sigbkg.root'
						RFileName = 'histos-mle_'+syst+'_'+ud+'_AllNoB0_sigbkgNoB0.root'
						RFileSyst = TFile(limitDir+RFileName)
						try: 							
							temphist = RFileSyst.Get(histPrefix+'__'+proc) # Get the postfit for this syst+ud
							binshist = RFile1.Get(histPrefix+'__'+proc).Clone()  #Get the rebinned histogram
							systHists[proc+catStr+syst+ud] = binshist.Clone(temphist.GetName()+'_'+syst+'_'+ud) #Clone and rename in container
							systHists[proc+catStr+syst+ud].SetDirectory(0)
							for ibin in range(1,binshist.GetNbinsX()+1):					
								systHists[proc+catStr+syst+ud].SetBinContent(ibin,temphist.GetBinContent(ibin)) # Change bin content in the container
								systHists[proc+catStr+syst+ud].SetBinError(ibin,temphist.GetBinError(ibin)) # Change bin error in the container
							if doNormByBinWidth: normByBinWidth(systHists[proc+catStr+syst+ud])							
						except: pass
						RFileSyst.Close()

		totBkgTemp1[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapeOnly'))
		totBkgTemp2[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'shapePlusNorm'))
		totBkgTemp3[catStr] = TGraphAsymmErrors(bkgHT.Clone(bkgHT.GetName()+'All'))

		#yvals = totBkgTemp3[catStr].GetY()
		#print 'totBkgTemp3 point 0 yval:', yvals[0]

		for ibin in range(1,bkghists[bkgProcList[0]+catStr].GetNbinsX()+1):
			errorUp = 0.
			errorDn = 0.
			errorStatUp = gaeBkgHT.GetErrorYhigh(ibin-1)**2
			errorStatDn = gaeBkgHT.GetErrorYlow(ibin-1)**2
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
							errorPlus = systHists[proc+catStr+syst+'plus'].GetBinContent(ibin)-bkghists[proc+catStr].GetBinContent(ibin)
							errorMinus = bkghists[proc+catStr].GetBinContent(ibin)-systHists[proc+catStr+syst+'minus'].GetBinContent(ibin)
							if errorPlus > 0: errorUp += errorPlus**2
							else: errorDn += errorPlus**2
							if errorMinus > 0: errorDn += errorMinus**2
							else: errorUp += errorMinus**2
						except: pass

			totBkgTemp1[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
			totBkgTemp1[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
			totBkgTemp2[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
			totBkgTemp2[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
			totBkgTemp3[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatUp))
			totBkgTemp3[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatDn))
		
		bkgHTgerr = totBkgTemp3[catStr].Clone()

		scaleFact1 = int(bkgHT.GetMaximum()/hsig1.GetMaximum()) - int(bkgHT.GetMaximum()/hsig1.GetMaximum()) % 10
		scaleFact2 = int(bkgHT.GetMaximum()/hsig2.GetMaximum()) - int(bkgHT.GetMaximum()/hsig2.GetMaximum()) % 10
		if scaleFact1==0: scaleFact1=int(bkgHT.GetMaximum()/hsig1.GetMaximum())
		if scaleFact2==0: scaleFact2=int(bkgHT.GetMaximum()/hsig2.GetMaximum())
		if scaleFact1==0: scaleFact1=1
		if scaleFact2==0: scaleFact2=1
		if sigScaleFact>0:
			scaleFact1=sigScaleFact
			scaleFact2=sigScaleFact*2
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
		bkgProcListNew = bkgProcList[:]
		if region=='WJCR':
			bkgProcListNew[bkgProcList.index("top")],bkgProcListNew[bkgProcList.index("ewk")]=bkgProcList[bkgProcList.index("ewk")],bkgProcList[bkgProcList.index("top")]
		for proc in bkgProcListNew:
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
		hsig1.SetLineColor(sig1Color)
		hsig1.SetFillStyle(0)
		hsig1.SetLineWidth(3)
		hsig2.SetLineColor(sig2Color)
		hsig2.SetLineStyle(7)#5)
		hsig2.SetFillStyle(0)
		hsig2.SetLineWidth(3)
		
		gaeData.SetMarkerStyle(20)
		gaeData.SetMarkerSize(1.2)
		gaeData.SetLineWidth(2)
		gaeData.SetMarkerColor(kBlack)
		gaeData.SetLineColor(kBlack)

		bkgHTgerr.SetFillStyle(3004)
		bkgHTgerr.SetFillColor(kBlack)

		gStyle.SetOptStat(0)
		c1 = TCanvas("c1","c1",1200,1000)
		gStyle.SetErrorX(0.5)
		yDiv=0.25
		if blind == True: yDiv=0.01
		# for some reason the markers at 0 don't show with this setting:
		uMargin = 0.00001
		if blind == True: uMargin = 0.12
		rMargin=.04
		# overlap the pads a little to hide the error bar gap:
		uPad={}
		if yLog and not blind: uPad=TPad("uPad","",0,yDiv-0.009,1,1) #for actual plots
		else: uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
		uPad.SetTopMargin(0.08)
		uPad.SetBottomMargin(uMargin)
		uPad.SetRightMargin(rMargin)
		uPad.SetLeftMargin(.105)
		uPad.Draw()
		if blind == False:
			lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
			lPad.SetTopMargin(0)
			lPad.SetBottomMargin(.4)
			lPad.SetRightMargin(rMargin)
			lPad.SetLeftMargin(.105)
			lPad.SetGridy()
			lPad.Draw()
		if not doNormByBinWidth: hData.SetMaximum(1.4*max(hData.GetMaximum(),bkgHT.GetMaximum()))
		hData.SetMinimum(0.015)
		hData.SetTitle("")
		# this is super important now!! gaeData has badly defined (negative) maximum
		gaeData.SetMaximum(1.25*max(gaeData.GetMaximum(),bkgHT.GetMaximum()))
		gaeData.SetMinimum(0.015)
		gaeData.SetTitle("")
		if doNormByBinWidth: gaeData.GetYaxis().SetTitle("< Events / 1 GeV >")
		else: gaeData.GetYaxis().SetTitle("Events / bin")
		formatUpperHist(gaeData)
		uPad.cd()
		gaeData.SetTitle("")
		if compareShapes: 
			hsig1.Scale(totBkg/hsig1.Integral())
			hsig2.Scale(totBkg/hsig2.Integral())
		if not blind: gaeData.Draw("apz")
		if blind: 
			hsig1.SetMinimum(0.015)
			if doNormByBinWidth: hsig1.GetYaxis().SetTitle("< Events / 1 GeV >")
			else: hsig1.GetYaxis().SetTitle("Events / bin")
			hsig1.SetMaximum(1.5*hData.GetMaximum())
			if iPlot=='Tau21Nm1': hsig1.SetMaximum(1.5*hData.GetMaximum())
			formatUpperHist(hsig1)
			hsig1.Draw("HIST")
		if doNormByBinWidth: hData.GetYaxis().SetTitle("< Events / 1 GeV >")
		else: hData.GetYaxis().SetTitle("Events / bin")
		
		stackbkgHT.Draw("SAME HIST")
		hsig1.Draw("SAME HIST")
		hsig2.Draw("SAME HIST")
		if not blind: gaeData.Draw("PZ") #redraw data so its not hidden
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
			if '1b' in tag[0]: tagString+='1b H, '
			elif '2b' in tag[0]: tagString+='2b H, '
			elif 'p' in tag[0]: tagString+='#geq'+tag[0][:-1]+' H, '
			else: tagString+=tag[0]+' H, '
		if tag[1]!='0p': 
			if 'p' in tag[1]: tagString+='#geq'+tag[1][:-1]+' W, '
			else: tagString+=tag[1]+' W, '
		if tag[2]!='0p': 
			if 'p' in tag[2]: tagString+='#geq'+tag[2][:-1]+' b, '
			else: tagString+=tag[2]+' b, '
		if tag[3]!='3p': 
			if 'p' in tag[3]: tagString+='#geq'+tag[3][:-1]+' j'
			else: tagString+=tag[3]+' j'
		if tagString.endswith(', '): tagString = tagString[:-2]		
		if iPlot != 'deltaRAK8': chLatex.DrawLatex(0.28, 0.84, flvString)
		else: chLatex.DrawLatex(0.75,0.84,flvString)
		if iPlot != 'YLD': chLatex.DrawLatex(0.28, 0.78, tagString)

		if drawQCD: 
			leg = TLegend(0.45,0.52,0.95,0.87)
			if iPlot == 'deltaRAK8': leg = TLegend(0.15,0.52,0.55,0.82)
		if not drawQCD or blind: 
			leg = TLegend(0.45,0.64,0.95,0.89)
			if iPlot == 'deltaRAK8': leg = TLegend(0.12,0.65,0.62,0.89)
		leg.SetShadowColor(0)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetLineColor(0)
		leg.SetLineStyle(0)
		leg.SetBorderSize(0) 
		leg.SetNColumns(2)
		leg.SetTextFont(62)#42)
		scaleFact1Str = ' x'+str(scaleFact1)
		scaleFact2Str = ' x'+str(scaleFact2)
		if not scaleSignals:
			scaleFact1Str = ''
			scaleFact2Str = ''
		if drawQCD:
			leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
			leg.AddEntry(bkghists['QCD'+catStr],"QCD","f")
			leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
			try: leg.AddEntry(bkghists['EWK'+catStr],"EW","f")
			except: pass
			leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f")
			try: leg.AddEntry(bkghists['TTbar'+catStr],"TOP","f")
			except: pass
			if not blind: 
				leg.AddEntry(0, "", "")
				leg.AddEntry(gaeData,"Data","pel")
				
		if not drawQCD:
			leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
			try: leg.AddEntry(bkghists['EWK'+catStr],"EW","f")
			except: pass
			leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
			try: leg.AddEntry(bkghists['TTbar'+catStr],"TOP","f")
			except: pass
			leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f")
			if not blind: leg.AddEntry(gaeData,"Data","pel")
		leg.Draw("same")

		prelimTex=TLatex()
		prelimTex.SetNDC()
		prelimTex.SetTextAlign(31) # align right
		prelimTex.SetTextFont(42)
		prelimTex.SetTextSize(0.05)
		if blind: prelimTex.SetTextSize(0.05)
		prelimTex.SetLineWidth(2)
		prelimTex.DrawLatex(0.95,0.94,str(lumi)+" fb^{-1} (13 TeV)")

		prelimTex2=TLatex()
		prelimTex2.SetNDC()
		prelimTex2.SetTextFont(61)
		prelimTex2.SetLineWidth(2)
		prelimTex2.SetTextSize(0.08)
		if blind: prelimTex2.SetTextSize(0.08)
		prelimTex2.DrawLatex(0.12,0.93,"CMS")

		prelimTex3=TLatex()
		prelimTex3.SetNDC()
		prelimTex3.SetTextAlign(12)
		prelimTex3.SetTextFont(52)
		prelimTex3.SetTextSize(0.055)
		if blind: prelimTex3.SetTextSize(0.055)
		prelimTex3.SetLineWidth(2)
		if not blind: prelimTex3.DrawLatex(0.23,0.945,"Preliminary")
		if blind: prelimTex3.DrawLatex(0.26,0.945,"Preliminary")

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
			pull.Draw("E0")
			
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
			if not doOneBand: pullLegend.AddEntry(pullUncBandStat , "Bkg. uncert. (shape syst.)" , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandNorm , "Bkg. uncert. (shape #oplus norm. syst.)" , "f")
			if not doOneBand: pullLegend.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus all syst.)" , "f")
			else: 
				if doAllSys: pullLegend.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus syst.)" , "f")
				else: pullLegend.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus lumi)" , "f")
			#pullLegend.AddEntry(pullQ2up , "Q^{2} Up" , "l")
			#pullLegend.AddEntry(pullQ2dn , "Q^{2} Down" , "l")
			pullLegend.Draw("SAME")
			pull.Draw("SAME E0")
			lPad.RedrawAxis()

		if blind == False and doRealPull:
			formatUpperHist(hData)
			lPad.cd()
			pull=hData.Clone("pull")
			for binNo in range(1,hData.GetNbinsX()+1):
				# case for data < MC:
				dataerror = gaeData.GetErrorYhigh(binNo-1)
				MCerror = totBkgTemp3[catStr].GetErrorYlow(binNo-1)
				# case for data > MC: 
				if(hData.GetBinContent(binNo) > bkgHT.GetBinContent(binNo)):
					dataerror = gaeData.GetErrorYlow(binNo-1)
					MCerror = totBkgTemp3[catStr].GetErrorYhigh(binNo-1)
				pull.SetBinContent(binNo,(hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(MCerror**2+dataerror**2))
			pull.SetMaximum(3)
			pull.SetMinimum(-3)
			if '53' in sig1:
				pull.SetFillColor(2)
				pull.SetLineColor(2)
			else:
				pull.SetFillColor(kGray+2)
				pull.SetLineColor(kGray+2)
			formatLowerHist(pull)
			pull.Draw("HIST")

		#c1.Write()
		savePrefix = limitDir+'plots/'
		if isNoB0: savePrefix += 'noB0/'
		if isNoCRHB0: savePrefix += 'noCRHB0/'
		if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix+isRebinned.replace('_rebinned_stat1p1','')+saveKey
		if nHtaglist[0]=='0p': savePrefix=savePrefix.replace('nH0p_','')
		if nWtaglist[0]=='0p': savePrefix=savePrefix.replace('nW0p_','')
		if nbtaglist[0]=='0p': savePrefix=savePrefix.replace('nB0p_','')
		if njetslist[0]=='0p': savePrefix=savePrefix.replace('nJ0p_','')
		if doRealPull: savePrefix+='_pull'
		if doNormByBinWidth: savePrefix+='_NBBW'
		if drawNormalized: savePrefix+='_norm'
		if yLog: savePrefix+='_logy'
		if blind: savePrefix+='_blind'
		if compareShapes: savePrefix+='_shp'

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
	histPrefixE = iPlot+'_'+lumiInTemplates+'fb_isE_'+tagStr
	histPrefixM = iPlot+'_'+lumiInTemplates+'fb_isM_'+tagStr
	if region=='SR': 
		histPrefixE+='_isSR'
		histPrefixM+='_isSR'
		#tagStr += '_isSR'
	else: 
		histPrefixE+='_isCR'
		histPrefixM+='_isCR'
		#tagStr += '_isCR'
	totBkgMerged = 0.
	for proc in bkgProcList:
		try: 
			binshistmerged = RFile1.Get(histPrefixE+'__'+proc).Clone()  #Get the rebinned histogram
			binshistmerged.Add(RFile1.Get(histPrefixM+'__'+proc))
			bkghistsmerged[proc+'isL'+tagStr] = binshistmerged.Clone(binshistmerged.GetName()+'_post') # Clone and rename into the container
			temphistmerged = RFilePost.Get(histPrefixE+'__'+proc).Clone() #Get the postfit histogram
			temphistmerged.Add(RFilePost.Get(histPrefixM+'__'+proc))
			for ibin in range(1,binshistmerged.GetNbinsX()+1):
				bkghistsmerged[proc+'isL'+tagStr].SetBinContent(ibin,temphistmerged.GetBinContent(ibin)) # Change bin content in the container
				if binshistmerged.GetBinContent(ibin)==0: percentstaterr = 0
				else: percentstaterr = binshistmerged.GetBinError(ibin)/binshistmerged.GetBinContent(ibin) #get the % stat error
				bkghistsmerged[proc+'isL'+tagStr].SetBinError(ibin,temphistmerged.GetBinContent(ibin)*percentstaterr) # Change bin error in the container
			totBkgMerged += bkghistsmerged[proc+'isL'+tagStr].Integral()
		except:	pass

	#print 'Bkghistmerged:'
	#for key in bkghistsmerged:
	#	print key

	hDatamerged = RFile1.Get(histPrefixE+'__DATA').Clone()
	hsig1merged = RFile1.Get(histPrefixE+'__sig').Clone(histPrefixE+'__sig1merged')
	hsig2merged = RFile2.Get(histPrefixE+'__sig').Clone(histPrefixE+'__sig2merged')
	hDatamerged.Add(RFile1.Get(histPrefixM+'__DATA').Clone())
	hsig1merged.Add(RFile1.Get(histPrefixM+'__sig').Clone())
	hsig2merged.Add(RFile2.Get(histPrefixM+'__sig').Clone())
	hsig1merged.Scale(xsec[sig1[:7]])
	hsig2merged.Scale(xsec[sig2[:7]])
        histrange = [hDatamerged.GetBinLowEdge(1),hDatamerged.GetBinLowEdge(hDatamerged.GetNbinsX()+1)]
	gaeDatamerged = TGraphAsymmErrors(hDatamerged.Clone(hDatamerged.GetName().replace("DATA","gaeDATA")))

	bkgHTmerged = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone()
	for proc in bkgProcList:
		if proc==bkgProcList[0]: continue
		try: bkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass
	gaeBkgHTmerged = TGraphAsymmErrors(bkgHTmerged.Clone("gaeBkgHTmerged"))

	if doNormByBinWidth:
		poissonNormByBinWidth(gaeDatamerged,hDatamerged)
		for proc in bkgProcList:
			try: normByBinWidth(bkghistsmerged[proc+'isL'+tagStr])
			except: pass
		normByBinWidth(hsig1merged)
		normByBinWidth(hsig2merged)
		normByBinWidth(hDatamerged)
	else: poissonErrors(gaeDatamerged)
	# Yes, there are easier ways using the TH1's but
	# it would be rough to swap objects lower down	

	if doNormByBinWidth: 
		normByBinWidth(bkgHTmerged)
		poissonNormByBinWidth(gaeBkgHTmerged,bkgHTmerged)
	else: poissonErrors(gaeBkgHTmerged)

	if doAllSys:
		q2list=[]
		if doQ2sys: q2list=['q2']
		for syst in systematicList+q2list:
			for ud in ['minus','plus']:
				for proc in bkgProcList:
					try: 
						systHists[proc+'isL'+tagStr+syst+ud] = systHists[proc+'isE_'+tagStr+syst+ud].Clone()
						systHists[proc+'isL'+tagStr+syst+ud].Add(systHists[proc+'isM_'+tagStr+syst+ud])
					except: pass

	totBkgTemp1['isL'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapeOnly'))
	totBkgTemp2['isL'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'shapePlusNorm'))
	totBkgTemp3['isL'+tagStr] = TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'All'))

	yvals = gaeBkgHTmerged.GetY()	
	for ibin in range(1,bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetNbinsX()+1):
		errorUp = 0.
		errorDn = 0.
		errorStatUp = gaeBkgHTmerged.GetErrorYhigh(ibin-1)**2
		errorStatDn = gaeBkgHTmerged.GetErrorYlow(ibin-1)**2

		if ibin < 3:
			print 'gaeBkgHTmerged = ',yvals[ibin-1],'+',math.sqrt(errorStatUp),'-',math.sqrt(errorStatDn)

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
						errorPlus = systHists[proc+'isL'+tagStr+syst+'plus'].GetBinContent(ibin)-bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)
						errorMinus = bkghistsmerged[proc+'isL'+tagStr].GetBinContent(ibin)-systHists[proc+'isL'+tagStr+syst+'minus'].GetBinContent(ibin)
						if errorPlus > 0: errorUp += errorPlus**2
						else: errorDn += errorPlus**2
						if errorMinus > 0: errorDn += errorMinus**2
						else: errorUp += errorMinus**2
					except: pass

		totBkgTemp1['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp))
		totBkgTemp1['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn))
		totBkgTemp2['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm))
		totBkgTemp2['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm))
		totBkgTemp3['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatUp))
		totBkgTemp3['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatDn))
	
	bkgHTgerrmerged = totBkgTemp3['isL'+tagStr].Clone()

	scaleFact1merged = int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum()) - int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum()) % 10
	scaleFact2merged = int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum()) - int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum()) % 10
	if scaleFact1merged==0: scaleFact1merged=int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum())
	if scaleFact2merged==0: scaleFact2merged=int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum())
	if scaleFact1merged==0: scaleFact1merged=1
	if scaleFact2merged==0: scaleFact2merged=1
	if sigScaleFact>0:
		scaleFact1merged=sigScaleFact
		scaleFact2merged=sigScaleFact*2
	if not scaleSignals:
		scaleFact1merged=1
		scaleFact2merged=1
	hsig1merged.Scale(scaleFact1merged)
	hsig2merged.Scale(scaleFact2merged)
	
	drawQCDmerged = False
	try: drawQCDmerged = bkghistsmerged['qcdisL'+tagStr].Integral()/bkgHTmerged.Integral()>.005
	except: pass

	stackbkgHTmerged = THStack("stackbkgHTmerged","")
	bkgProcListNew = bkgProcList[:]
	if region=='WJCR':
		bkgProcListNew[bkgProcList.index("top")],bkgProcListNew[bkgProcList.index("ewk")]=bkgProcList[bkgProcList.index("ewk")],bkgProcList[bkgProcList.index("top")]
	for proc in bkgProcListNew:
		try: 
			if drawQCDmerged or proc!='qcd': stackbkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass

	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr].SetLineColor(bkgHistColors[proc])
			bkghistsmerged[proc+'isL'+tagStr].SetFillColor(bkgHistColors[proc])
			bkghistsmerged[proc+'isL'+tagStr].SetLineWidth(2)
		except: pass
	hsig1merged.SetLineColor(sig1Color)
	hsig1merged.SetFillStyle(0)
	hsig1merged.SetLineWidth(3)
	hsig2merged.SetLineColor(sig2Color)
	hsig2merged.SetLineStyle(7)#5)
	hsig2merged.SetFillStyle(0)
	hsig2merged.SetLineWidth(3)
	
	gaeDatamerged.SetMarkerStyle(20)
	gaeDatamerged.SetMarkerSize(1.2)
	gaeDatamerged.SetLineWidth(2)
	gaeDatamerged.SetMarkerColor(kBlack)
	gaeDatamerged.SetLineColor(kBlack)

	bkgHTgerrmerged.SetFillStyle(3004)
	bkgHTgerrmerged.SetFillColor(kBlack)

	gStyle.SetOptStat(0)
	c1merged = TCanvas("c1merged","c1merged",1200,1000)
	gStyle.SetErrorX(0.5)
	yDiv=0.25
	if blind == True: yDiv=0.01
	uMargin = 0.00001
	if blind == True: uMargin = 0.12
	rMargin=.04
	uPad={}
	if yLog and not blind: uPad=TPad("uPad","",0,yDiv-0.009,1,1) #for actual plots
	else: uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
	uPad.SetTopMargin(0.08)
	uPad.SetBottomMargin(uMargin)
	uPad.SetRightMargin(rMargin)
	uPad.SetLeftMargin(.105)
	uPad.Draw()
	if blind == False:
		lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
		lPad.SetTopMargin(0)
		lPad.SetBottomMargin(.4)
		lPad.SetRightMargin(rMargin)
		lPad.SetLeftMargin(.105)
		lPad.SetGridy()
		lPad.Draw()
	gaeDatamerged.SetMaximum(1.25*max(gaeDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
	gaeDatamerged.SetMinimum(0.015)
	if doNormByBinWidth: gaeDatamerged.GetYaxis().SetTitle("< Events / 1 GeV >")
	else: gaeDatamerged.GetYaxis().SetTitle("Events / bin")
	formatUpperHist(gaeDatamerged)
	uPad.cd()
	gaeDatamerged.SetTitle("")
	stackbkgHTmerged.SetTitle("")
	if compareShapes: 
		hsig1merged.Scale(totBkgMerged/hsig1merged.Integral())
		hsig2merged.Scale(totBkgMerged/hsig2merged.Integral())
	if not blind: gaeDatamerged.Draw("apz")
	if blind: 
		hsig1merged.SetMinimum(0.015)
		if doNormByBinWidth: hsig1merged.GetYaxis().SetTitle("< Events / 1 GeV >")
		else: hsig1merged.GetYaxis().SetTitle("Events / bin")
		hsig1merged.SetMaximum(1.5*hDatamerged.GetMaximum())
		if iPlot=='Tau21Nm1': hsig1merged.SetMaximum(1.5*hDatamerged.GetMaximum())
		formatUpperHist(hsig1merged)
		hsig1merged.Draw("HIST")
	stackbkgHTmerged.Draw("SAME HIST")
	hsig1merged.Draw("SAME HIST")
	hsig2merged.Draw("SAME HIST")
	if not blind: gaeDatamerged.Draw("PZ") #redraw data so its not hidden
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
		if '1b' in tag[0]: tagString+='1b H, '
		elif '2b' in tag[0]: tagString+='2b H, '
		elif 'p' in tag[0]: tagString+='#geq'+tag[0][:-1]+' H, '
		else: tagString+=tag[0]+' H,  '
	if tag[1]!='0p':
		if 'p' in tag[1]: tagString+='#geq'+tag[1][:-1]+' W, '
		else: tagString+=tag[1]+' W, '
	if tag[2]!='0p':
		if 'p' in tag[2]: tagString+='#geq'+tag[2][:-1]+' b, '
		else: tagString+=tag[2]+' b, '
	if tag[3]!='3p':
		if 'p' in tag[3]: tagString+='#geq'+tag[3][:-1]+' j'
		else: tagString+=tag[3]+' j'
	if tagString.endswith(', '): tagString = tagString[:-2]
	if iPlot != 'deltaRAK8': chLatexmerged.DrawLatex(0.28, 0.85, flvString)
	else: chLatexmerged.DrawLatex(0.75,0.85,flvString)
	if iPlot != 'YLD':chLatexmerged.DrawLatex(0.28, 0.78, tagString)

	if drawQCDmerged: 
		legmerged = TLegend(0.45,0.52,0.95,0.87)
		if iPlot == 'deltaRAK8': legmerged = TLegend(0.15,0.52,0.55,0.82)
	if not drawQCDmerged or blind: 
		legmerged = TLegend(0.45,0.64,0.95,0.89)
		if iPlot == 'deltaRAK8': legmerged = TLegend(0.12,0.65,0.62,0.90)
	legmerged.SetShadowColor(0)
	legmerged.SetFillColor(0)
	legmerged.SetFillStyle(0)
	legmerged.SetLineColor(0)
	legmerged.SetLineStyle(0)
	legmerged.SetBorderSize(0) 
	legmerged.SetNColumns(2)
	legmerged.SetTextFont(62)#42)
	scaleFact1Str = ' x'+str(scaleFact1)
	scaleFact2Str = ' x'+str(scaleFact2)
	if not scaleSignals:
		scaleFact1Str = ''
		scaleFact2Str = ''
	if drawQCDmerged:
		legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
		legmerged.AddEntry(bkghistsmerged['QCDisL'+tagStr],"QCD","f")
		legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
		legmerged.AddEntry(bkghistsmerged['EWKisL'+tagStr],"EW","f")
		#except: pass
		if not blind: 
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f")
			legmerged.AddEntry(bkghistsmerged['TTbarisL'+tagStr],"TOP","f")
			#except: pass
			legmerged.AddEntry(0, "", "")
			legmerged.AddEntry(gaeDatamerged,"Data","pel")
		else:
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f")
			legmerged.AddEntry(bkghistsmerged['TTbarisL'+tagStr],"TOP","f")
			#except: pass
	if not drawQCDmerged:
		legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
		legmerged.AddEntry(bkghistsmerged['EWKisL'+tagStr],"EW","f")
		#except: pass
		legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
		legmerged.AddEntry(bkghistsmerged['TTbarisL'+tagStr],"TOP","f")
		#except: pass
		legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f")
		if not blind: legmerged.AddEntry(gaeDatamerged,"Data","pel")
	legmerged.Draw("same")

	prelimTex=TLatex()
	prelimTex.SetNDC()
	prelimTex.SetTextAlign(31) # align right
	prelimTex.SetTextFont(42)
	prelimTex.SetTextSize(0.05)
	if blind: prelimTex.SetTextSize(0.05)
	prelimTex.SetLineWidth(2)
	prelimTex.DrawLatex(0.95,0.94,str(lumi)+" fb^{-1} (13 TeV)")
	
	prelimTex2=TLatex()
	prelimTex2.SetNDC()
	prelimTex2.SetTextFont(61)
	prelimTex2.SetLineWidth(2)
	prelimTex2.SetTextSize(0.08)
	if blind: prelimTex2.SetTextSize(0.08)
	prelimTex2.DrawLatex(0.12,0.93,"CMS")
	
	prelimTex3=TLatex()
	prelimTex3.SetNDC()
	prelimTex3.SetTextAlign(12)
	prelimTex3.SetTextFont(52)
	prelimTex3.SetTextSize(0.055)
	if blind: prelimTex3.SetTextSize(0.055)
	prelimTex3.SetLineWidth(2)
	if not blind: prelimTex3.DrawLatex(0.23,0.945,"Preliminary")
	if blind: prelimTex3.DrawLatex(0.26,0.945,"Preliminary")
	
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
		pullmerged.Draw("E0")
		
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
		if not doOneBand: pullLegendmerged.AddEntry(pullUncBandStat , "Bkg. uncert. (shape syst.)" , "f")
		if not doOneBand: pullLegendmerged.AddEntry(pullUncBandNorm , "Bkg. uncert. (shape #oplus norm. syst.)" , "f")
		if not doOneBand: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus all syst.)" , "f")
		else: 
			if doAllSys: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus syst.)" , "f")
			else: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg. uncert. (stat. #oplus lumi)" , "f")
		pullLegendmerged.Draw("SAME")
		pullmerged.Draw("SAME E0")
		lPad.RedrawAxis()

	if blind == False and doRealPull:
		formatUpperHist(hDatamerged)
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		for binNo in range(1,hDatamerged.GetNbinsX()+1):
			# case for data < MC:
			dataerror = gaeDatamerged.GetErrorYhigh(binNo-1)
			MCerror = totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1)
			# case for data > MC:
			if(hDatamerged.GetBinContent(binNo) > bkgHTmerged.GetBinContent(binNo)):
				dataerror = gaeDatamerged.GetErrorYlow(binNo-1)
				MCerror = totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)
			pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(MCerror**2+dataerror**2))
		pullmerged.SetMaximum(3)
		pullmerged.SetMinimum(-3)
		if '53' in sig1:
			pullmerged.SetFillColor(2)
			pullmerged.SetLineColor(2)
		else:
			pullmerged.SetFillColor(kGray+2)
			pullmerged.SetLineColor(kGray+2)
		formatLowerHist(pullmerged)
		pullmerged.Draw("HIST")

	#c1merged.Write()
	savePrefixmerged = limitDir+'plots/'
	if isNoB0: savePrefixmerged += 'noB0/'
	if isNoCRHB0: savePrefixmerged += 'noCRHB0/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('isE','isL')+isRebinned.replace('_rebinned_stat1p1','')+saveKey
	if nHtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nH0p_','')
	if nWtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nW0p_','')
	if nbtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nB0p_','')
	if njetslist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nJ0p_','')
	if doRealPull: savePrefixmerged+='_pull'
	if doNormByBinWidth: savePrefixmerged+='_NBBW'
	if drawNormalized: savePrefix+='_norm'
	if yLog: savePrefixmerged+='_logy'
	if blind: savePrefixmerged+='_blind'
	if compareShapes: savePrefixmerged+='_shp'

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
RFilePost.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


