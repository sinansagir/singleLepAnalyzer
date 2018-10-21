#!/usr/bin/python

import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
from weights import *
from modSyst import *
from utils import *
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)
start_time = time.time()

lumi=35.9 #for plots
lumiInTemplates= str(targetlumi/1000).replace('.','p') # 1/fb

region='PS' #PS,SR,TTCR,WJCR
isCategorized=0
if region!='PS': isCategorized=1
iPlot='deltaRjet2'
if len(sys.argv)>1: iPlot=str(sys.argv[1])
cutString=''
if region=='SR': pfix='templates_'
elif region=='WJCR': pfix='wjets_'
elif region=='TTCR': pfix='ttbar_'
if not isCategorized: pfix='kinematics_'+region+'_'
templateDir=os.getcwd()+'/'+pfix+'M17WtSF_2017_3_31/'+cutString+'/'
postFitFile=os.getcwd()+'/../thetaLimits/chi2test_2017_2_12/histos-mle.root'
plotPostFit = False #this is not working yet!!

isRebinned='_rebinned_stat1p1' #post for ROOT file names
saveKey = '_poisson'#'_noQ2' # tag for plot names

sig1='X53X53M900left' #  choose the 1st signal to plot
sig1leg='X_{5/3}#bar{X}_{5/3} LH (0.9 TeV)'
sig2='X53X53M1200right' #  choose the 2nd signal to plot
sig2leg='X_{5/3}#bar{X}_{5/3} RH (1.2 TeV)'
scaleSignals = True
sigScaleFact = 70 #put -1 if auto-scaling wanted
tempsig='templates_'+iPlot+'_'+sig1+'_'+lumiInTemplates+'fb'+isRebinned+'.root'

bkgProcList = ['top','ewk','qcd']
#bkgProcList = ['TTJets','T','WJets','ZJets','VV','qcd']
if '53' in sig1: bkgHistColors = {'top':rt.kRed-9,'ewk':rt.kBlue-7,'qcd':rt.kOrange-5,'TTJets':rt.kRed-9,'T':rt.kRed-5,'WJets':rt.kBlue-7,'ZJets':rt.kBlue-1,'VV':rt.kBlue+5,'qcd':rt.kOrange-5} #X53X53
elif 'HTB' in sig1: bkgHistColors = {'ttbar':rt.kGreen-3,'wjets':rt.kPink-4,'top':rt.kAzure+8,'ewk':rt.kMagenta-2,'qcd':rt.kOrange+5} #HTB
else: bkgHistColors = {'top':rt.kAzure+8,'ewk':rt.kMagenta-2,'qcd':rt.kOrange+5} #TT

systematicList = ['pileup','jec','jer','jms','jmr','tau21','taupt','topsf','trigeff','ht',
				  'btag','mistag','pdfNew','muRFcorrdNew','toppt']

doAllSys = True
doQ2sys  = False
addCRsys = False
doNormByBinWidth=False
doOneBand = False
blind = False
yLog  = False
doRealPull = True
compareShapes = False
drawYields = False
if not doAllSys: doQ2sys = False
if not doAllSys: doOneBand = True # Don't change this!
if yLog: scaleSignals = False
if doRealPull: doOneBand=False
if compareShapes: blind,yLog,scaleSignals,sigScaleFact=True,False,False,-1

isEMlist =['E','M']
if region=='SR': nttaglist=['0','1p']
else: nttaglist = ['0p']
if region=='TTCR': nWtaglist = ['0p']
else: nWtaglist=['0','1p']
if region=='WJCR': nbtaglist = ['0']
elif region=='TTCR': nbtaglist=['1','2p']#,'2','3p']
else: nbtaglist=['1','2p']
if not isCategorized: 	
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['1p']#['0','1p','2p']
	if region=='CR': nbtaglist = ['0','0p','1p']
njetslist = ['4p']
if region=='PS': njetslist = ['3p']
if 'YLD' in iPlot:
	doNormByBinWidth = False
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0p']
	njetslist = ['0p']
tagList = list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))

lumiSys = 0.025 # lumi uncertainty
trigSys = 0.0 # trigger uncertainty
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
	if 'NTJets' in histogram.GetName(): histogram.GetXaxis().SetNdivisions(5)
	elif 'NWJets' in histogram.GetName(): histogram.GetXaxis().SetNdivisions(5)
	elif 'NBJets' in histogram.GetName(): histogram.GetXaxis().SetNdivisions(6,rt.kFALSE)
	else: histogram.GetXaxis().SetNdivisions(506)

	if blind == True:
		histogram.GetXaxis().SetLabelSize(0.045)
		histogram.GetXaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetLabelSize(0.045)
		histogram.GetYaxis().SetTitleSize(0.055)
		histogram.GetYaxis().SetTitleOffset(1.15)
	else:
		histogram.GetYaxis().SetLabelSize(0.07)
		histogram.GetYaxis().SetTitleSize(0.08)
		histogram.GetYaxis().SetTitleOffset(.95)
		if 'NTJets' in histogram.GetName() or 'NWJets' in histogram.GetName() or 'NBJets' in histogram.GetName(): histogram.GetYaxis().SetTitleOffset(0.81)
	if 'YLD' in iPlot: histogram.GetXaxis().LabelsOption("u")

	if 'nB0' in histogram.GetName() and 'minMlb' in histogram.GetName() and 'YLD' not in iPlot: histogram.GetXaxis().SetTitle("min[M(l,j)], j#neqb [GeV]")
	if 'JetPt' in histogram.GetName() or 'JetEta' in histogram.GetName() or 'JetPhi' in histogram.GetName() or 'Pruned' in histogram.GetName() or 'Tau' in histogram.GetName() or 'SoftDropMass' in histogram.GetName(): histogram.GetYaxis().SetTitle(histogram.GetYaxis().GetTitle().replace("Events","Jets"))
	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.000101)
	if region=='WJCR': histogram.SetMinimum(0.0000101)
	if region=='PS': histogram.SetMinimum(0.0101)
	if not yLog: 
		histogram.SetMinimum(0.25)
	if yLog:
		if 'nB1' in histogram.GetName(): histogram.SetMaximum(1e4*rt.TMath.MaxElement(histogram.GetN(),histogram.GetY()))
		else: histogram.SetMaximum(2e2*rt.TMath.MaxElement(histogram.GetN(),histogram.GetY()))
		uPad.SetLogy()
	else: 
		if 'YLD' in iPlot: histogram.SetMaximum(1.3*histogram.GetMaximum())
		else: histogram.SetMaximum(1.3*histogram.GetMaximum())
		
def formatLowerHist(histogram,disc):
	histogram.GetXaxis().SetLabelSize(.12)
	histogram.GetXaxis().SetTitleSize(0.15)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetXaxis().SetNdivisions(506)

	if 'NTJets' in disc: histogram.GetXaxis().SetNdivisions(5)
	elif 'NWJets' in disc: histogram.GetXaxis().SetNdivisions(5)
	elif 'NBJets' in disc: histogram.GetXaxis().SetNdivisions(6,rt.kFALSE)
	else: histogram.GetXaxis().SetNdivisions(506)
	if 'NTJets' in disc or 'NWJets' in disc or 'NBJets' in disc or 'NJets' in disc: histogram.GetXaxis().SetLabelSize(0.15)

	histogram.GetYaxis().SetLabelSize(0.12)
	histogram.GetYaxis().SetTitleSize(0.14)
	histogram.GetYaxis().SetTitleOffset(.43)
	histogram.GetYaxis().SetTitle('Data/Bkg')
	histogram.GetYaxis().SetNdivisions(5,2,0)
	if doRealPull: histogram.GetYaxis().SetRangeUser(min(-2.99,0.8*histogram.GetBinContent(histogram.GetMaximumBin())),max(2.99,1.2*histogram.GetBinContent(histogram.GetMaximumBin())))
	#else: histogram.GetYaxis().SetRangeUser(0.45,1.55)#0,2.99)
	else: histogram.GetYaxis().SetRangeUser(0.01,1.99)#0,2.99)
	histogram.GetYaxis().CenterTitle()

if not os.path.exists(templateDir+tempsig.replace(sig1,sig1)):
	print "ERROR: File does not exits: "+templateDir+tempsig.replace(sig1,sig1)
	os._exit(1)
print "READING: "+templateDir+tempsig.replace(sig1,sig1)
RFile1 = rt.TFile(templateDir+tempsig.replace(sig1,sig1))
RFile2 = rt.TFile(templateDir+tempsig.replace(sig1,sig2))
if plotPostFit: RPostFile = rt.TFile(postFitFile)

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= "35.9 fb^{-1}"
CMS_lumi.writeExtraText = 0
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 800; 
W_ref = 800; 
W = W_ref
H = H_ref

iPeriod = 4 #see CMS_lumi.py module for usage!

# references for T, B, L, R
T = 0.10*H_ref
B = 0.35*H_ref 
if blind == True: B = 0.12*H_ref
L = 0.15*W_ref
R = 0.05*W_ref

tagPosX = 0.34
tagPosY = 0.84
if 'Tau32' in iPlot: tagPosX = 0.58
if not blind: tagPosY-=0.1

table = []
table.append(['break'])
table.append(['Categories','prob_KS','prob_KS_X','prob_chi2','chi2','ndof'])
table.append(['break'])
bkghists = {}
bkghistsmerged = {}
systHists = {}
totBkgTemp1 = {}
totBkgTemp2 = {}
totBkgTemp3 = {}
for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	for isEM in isEMlist:
		histPrefix=iPlot+'_'+lumiInTemplates+'fb_'
		catStr='is'+isEM+'_'+tagStr
		histPrefix+=catStr
		print histPrefix
		totBkg = 0.
		for proc in bkgProcList: 
			try:
				bkghists[proc+catStr] = RFile1.Get(histPrefix+'__'+proc).Clone()
				if plotPostFit: 
					postFitHist = RPostFile.Get(histPrefix+'__'+proc).Clone()
					for ibin in range(1,bkghists[proc+catStr].GetNbinsX()+1):
						bkghists[proc+catStr].SetBinContent(ibin,postFitHist.GetBinContent(ibin))
						bkghists[proc+catStr].SetBinError(ibin,postFitHist.GetBinError(ibin))
				totBkg += bkghists[proc+catStr].Integral()
			except:
				print "There is no "+proc+"!!! Skipping it....."
				pass
		hData = RFile1.Get(histPrefix+'__DATA').Clone()
		gaeData = rt.TGraphAsymmErrors(hData.Clone(hData.GetName().replace("DATA","gaeData")))
		hData_test = RFile1.Get(histPrefix+'__DATA').Clone()
		bkgHT_test = bkghists[bkgProcList[0]+catStr].Clone()
		for proc in bkgProcList:
			if proc==bkgProcList[0]: continue
			try: bkgHT_test.Add(bkghists[proc+catStr])
			except: pass
		print hData_test.Integral(),bkgHT_test.Integral()
		hsig1 = RFile1.Get(histPrefix+'__sig').Clone(histPrefix+'__sig1')
		hsig2 = RFile2.Get(histPrefix+'__sig').Clone(histPrefix+'__sig2')
		hsig1.Scale(xsec[sig1])
		hsig2.Scale(xsec[sig2])

		bkgHT = bkghists[bkgProcList[0]+catStr].Clone()
		for proc in bkgProcList:
			if proc==bkgProcList[0]: continue
			try: bkgHT.Add(bkghists[proc+catStr])
			except: pass
		gaeBkgHT = rt.TGraphAsymmErrors(bkgHT.Clone("gaeBkgHT"))

		if doNormByBinWidth: poissonNormByBinWidth(gaeBkgHT,bkgHT)
		else: poissonErrors(gaeBkgHT)

		if doNormByBinWidth:
			for proc in bkgProcList:
				try: normByBinWidth(bkghists[proc+catStr])
				except: pass
			normByBinWidth(bkgHT)
			normByBinWidth(hsig1)
			normByBinWidth(hsig2)
			poissonNormByBinWidth(gaeData,hData)
			normByBinWidth(hData)
		else: poissonErrors(gaeData)
		# Yes, there are easier ways using the TH1's but
		# it would be rough to swap objects lower down

		if doAllSys:
			q2list = []
			if doQ2sys: q2list=['q2']
			print systematicList
			for syst in systematicList+q2list:
				print syst
				for ud in ['minus','plus']:
					for proc in bkgProcList:
						try: 
							systHists[proc+catStr+syst+ud] = RFile1.Get(histPrefix+'__'+proc+'__'+syst+'__'+ud).Clone()
							if doNormByBinWidth: normByBinWidth(systHists[proc+catStr+syst+ud])
						except: pass

		# we only use the bin contents from this cloning
		# if stat uncert is going to come from the cloning, clone the gaeBkgHT I think
		totBkgTemp1[catStr] = gaeBkgHT.Clone(bkgHT.GetName()+'shapeOnly')
		totBkgTemp2[catStr] = gaeBkgHT.Clone(bkgHT.GetName()+'shapePlusNorm')
		totBkgTemp3[catStr] = gaeBkgHT.Clone(bkgHT.GetName()+'All')
		
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

			totBkgTemp1[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorStatUp))
			totBkgTemp1[catStr].SetPointEYlow(ibin-1, math.sqrt(errorStatDn))
			totBkgTemp2[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorStatUp+errorNorm))
			totBkgTemp2[catStr].SetPointEYlow(ibin-1, math.sqrt(errorStatDn+errorNorm))
			totBkgTemp3[catStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatUp))
			totBkgTemp3[catStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatDn))
			
		for ibin in range(1, bkgHT_test.GetNbinsX()+1):
			bkgHT_test.SetBinError(ibin,(totBkgTemp3[catStr].GetErrorYlow(ibin-1) + totBkgTemp3[catStr].GetErrorYhigh(ibin-1))/2 )

		prob_KS = bkgHT_test.KolmogorovTest(hData_test)
		prob_KS_X = bkgHT_test.KolmogorovTest(hData_test,"X")
		prob_chi2 = hData_test.Chi2Test(bkgHT_test,"UW")
		chi2 = hData_test.Chi2Test(bkgHT_test,"UW CHI2")
		if hData_test.Chi2Test(bkgHT_test,"UW CHI2/NDF")!=0: ndof = int(hData_test.Chi2Test(bkgHT_test,"UW CHI2")/hData_test.Chi2Test(bkgHT_test,"UW CHI2/NDF"))
		else: ndof = 0
		print '/'*80,'\n','*'*80
		print histPrefix+'_KS =',prob_KS
		print 'WARNING: KS test works on unbinned distributions. For binned histograms, see NOTE3 at https://root.cern.ch/doc/master/classTH1.html#a2747cabe9ebe61c2fdfd74ff307cef3a'
		print '*'*80,'\n','/'*80,'\n','*'*80
		print histPrefix+'_Chi2Test:'
		print "p-value =",prob_chi2,"CHI2/NDF",chi2,"/",ndof
		print '*'*80,'\n','/'*80
		table.append([catStr,prob_KS,prob_KS_X,prob_chi2,chi2,ndof])
		
		bkgHTgerr = totBkgTemp3[catStr].Clone()

		scaleFact1 = int(bkgHT.GetMaximum()/hsig1.GetMaximum()) - int(bkgHT.GetMaximum()/hsig1.GetMaximum()) % 10
		scaleFact2 = int(bkgHT.GetMaximum()/hsig2.GetMaximum()) - int(bkgHT.GetMaximum()/hsig2.GetMaximum()) % 10
		if scaleFact1==0: scaleFact1=int(bkgHT.GetMaximum()/hsig1.GetMaximum())
		if scaleFact2==0: scaleFact2=int(bkgHT.GetMaximum()/hsig2.GetMaximum())
		if scaleFact1==0: scaleFact1=1
		if scaleFact2==0: scaleFact2=1
		if sigScaleFact>0:
			scaleFact1=sigScaleFact
			scaleFact2=sigScaleFact
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

		stackbkgHT = rt.THStack("stackbkgHT","")
		bkgProcListNew = bkgProcList[:]
		if region=='WJCR':
			bkgProcListNew[bkgProcList.index("top")],bkgProcListNew[bkgProcList.index("ewk")]=bkgProcList[bkgProcList.index("ewk")],bkgProcList[bkgProcList.index("top")]
		for proc in bkgProcListNew:
			if drawQCD or proc!='qcd': 
				try: stackbkgHT.Add(bkghists[proc+catStr])
				except: pass

		sig1Color= rt.kBlack
		sig2Color= rt.kRed
		if '53' in sig1:
			sig1Color= rt.kBlack
			sig2Color= rt.kBlack
			
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
		
		if not drawYields: gaeData.SetMarkerStyle(20)
		gaeData.SetMarkerSize(1.2)
		gaeData.SetLineWidth(2)
		gaeData.SetMarkerColor(rt.kBlack)
		gaeData.SetLineColor(rt.kBlack)
		if drawYields: gaeData.SetMarkerSize(4)

		bkgHTgerr.SetFillStyle(3004)
		bkgHTgerr.SetFillColor(rt.kBlack)
		bkgHTgerr.SetLineColor(rt.kBlack)

		c1 = rt.TCanvas("c1","c1",50,50,W,H)
		c1.SetFillColor(0)
		c1.SetBorderMode(0)
		c1.SetFrameFillStyle(0)
		c1.SetFrameBorderMode(0)
		#c1.SetTickx(0)
		#c1.SetTicky(0)
	
		yDiv=0.35
		if blind == True: yDiv=0.0
		# overlap the pads a little to hide the error bar gap:
		uPad=rt.TPad("uPad","",0,yDiv-0.009,1,1) #for actual plots
	
		uPad.SetLeftMargin( L/W )
		uPad.SetRightMargin( R/W )
		uPad.SetTopMargin( T/H )
		uPad.SetBottomMargin( 0.01 )
		if blind == True: uPad.SetBottomMargin( B/H )
	
		uPad.SetFillColor(0)
		uPad.SetBorderMode(0)
		uPad.SetFrameFillStyle(0)
		uPad.SetFrameBorderMode(0)
		#uPad.SetTickx(0)
		#uPad.SetTicky(0)
		uPad.Draw()
		if blind == False:
			lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner

			lPad.SetLeftMargin( L/W )
			lPad.SetRightMargin( R/W )
			lPad.SetTopMargin( 0.01 )
			lPad.SetBottomMargin( B/H )

			#lPad.SetGridy()
			lPad.SetFillColor(0)
			lPad.SetBorderMode(0)
			lPad.SetFrameFillStyle(0)
			lPad.SetFrameBorderMode(0)
			#lPad.SetTickx(0)
			#lPad.SetTicky(0)
			lPad.Draw()
		# this is super important now!! gaeData has badly defined (negative) maximum
		if not doNormByBinWidth: gaeData.SetMaximum(1.2*max(gaeData.GetMaximum(),bkgHT.GetMaximum()))
		#gaeData.SetMinimum(0.015)
		gaeData.SetTitle("")
		if doNormByBinWidth: gaeData.GetYaxis().SetTitle("< Events / GeV >")
		elif iPlot=='minMlb': gaeData.GetYaxis().SetTitle("Events / 20 GeV")
		else: gaeData.GetYaxis().SetTitle("Events / bin")
		formatUpperHist(gaeData)
		gaeData.GetXaxis().SetRangeUser(hData.GetBinLowEdge(1),hData.GetBinLowEdge(gaeData.GetN()+1))
		uPad.cd()
		gaeData.SetTitle("")
		if compareShapes: 
			hsig1.Scale(totBkg/hsig1.Integral())
			hsig2.Scale(totBkg/hsig2.Integral())
		if not blind: 
			if 'rebinned_stat0p' in isRebinned: gaeData.Draw("apz1")
			else: gaeData.Draw("apz0")
		if blind: 
			#hsig1.SetMinimum(0.015)
			if doNormByBinWidth: hsig1.GetYaxis().SetTitle("< Events / GeV >")
			else: hsig1.GetYaxis().SetTitle("Events / bin")
			formatUpperHist(hsig1)
			hsig1.SetMaximum(gaeData.GetMaximum())
			hsig1.Draw("HIST")
		stackbkgHT.Draw("SAME HIST")
		if drawYields: 
			rt.gStyle.SetPaintTextFormat("1.0f")
			bkgHT.Draw("SAME TEXT90")
		hsig1.Draw("SAME HIST")
		hsig2.Draw("SAME HIST")
		if not blind: 
			if 'rebinned_stat0p' in isRebinned: gaeData.Draw("pz1")
			else: gaeData.Draw("pz0") #redraw data so its not hidden
			if drawYields: gaeData.Draw("SAME TEXT00") 
		uPad.RedrawAxis()
		bkgHTgerr.Draw("SAME E2")
		
		chLatex = rt.TLatex()
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
		chLatex.DrawLatex(tagPosX, tagPosY, flvString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)

		if drawQCD: leg = rt.TLegend(0.40,0.52,0.92,0.87)
		if not drawQCD or blind: leg = rt.TLegend(0.40,0.62,0.92,0.87)
		rt.SetOwnership( leg, 0 )   # 0 = release (not keep), 1 = keep
		leg.SetShadowColor(0)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetLineColor(0)
		leg.SetLineStyle(0)
		leg.SetBorderSize(0) 
		leg.SetNColumns(2)
		leg.SetTextFont(62)#42)
		leg.SetColumnSeparation(0.05)
		scaleFact1Str = 'x'+str(scaleFact1)
		scaleFact2Str = 'x'+str(scaleFact2)
		if not scaleSignals:
			scaleFact1Str = ''
			scaleFact2Str = ''
		if drawQCD:
			if not blind: 
				leg.AddEntry(gaeData,"Data","ep")
				leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
				leg.AddEntry(bkghists['qcd'+catStr],"QCD","f")
				leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
				try: leg.AddEntry(bkghists['ewk'+catStr],"EWK","f")
				except: pass
				try: leg.AddEntry(bkghists['WJets'+catStr],"W+jets","f")
				except: pass
				try: leg.AddEntry(bkghists['ZJets'+catStr],"Z+jets","f")
				except: pass
				try: leg.AddEntry(bkghists['VV'+catStr],"VV","f")
				except: pass
				leg.AddEntry(bkgHTgerr,"Bkg uncertainty","f")
				try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
				except: pass
				try: leg.AddEntry(bkghists['TTJets'+catStr],"t#bar{t}","f")
				except: pass
				try: leg.AddEntry(bkghists['T'+catStr],"Single t","f")
				except: pass
			else: 
				leg.AddEntry(bkghists['qcd'+catStr],"QCD","f")
				leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
				try: leg.AddEntry(bkghists['ewk'+catStr],"EWK","f")
				except: pass
				try: leg.AddEntry(bkghists['WJets'+catStr],"W+jets","f")
				except: pass
				try: leg.AddEntry(bkghists['ZJets'+catStr],"Z+jets","f")
				except: pass
				try: leg.AddEntry(bkghists['VV'+catStr],"VV","f")
				except: pass
				leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
				try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
				except: pass
				try: leg.AddEntry(bkghists['TTJets'+catStr],"t#bar{t}","f")
				except: pass
				try: leg.AddEntry(bkghists['T'+catStr],"Single t","f")
				except: pass
				leg.AddEntry(bkgHTgerr,"Bkg uncertainty","f")
		if not drawQCD:
			if not blind: 
				leg.AddEntry(gaeData,"Data","ep")
				leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
				try: leg.AddEntry(bkghists['ewk'+catStr],"EWK","f")
				except: pass
				try: leg.AddEntry(bkghists['WJets'+catStr],"W+jets","f")
				except: pass
				try: leg.AddEntry(bkghists['ZJets'+catStr],"Z+jets","f")
				except: pass
				try: leg.AddEntry(bkghists['VV'+catStr],"VV","f")
				except: pass
				leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
				try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
				except: pass
				try: leg.AddEntry(bkghists['TTJets'+catStr],"t#bar{t}","f")
				except: pass
				try: leg.AddEntry(bkghists['T'+catStr],"Single t","f")
				except: pass
				leg.AddEntry(bkgHTgerr,"Bkg uncertainty","f")
			else:
				try: leg.AddEntry(bkghists['ewk'+catStr],"EWK","f")
				except: pass
				try: leg.AddEntry(bkghists['WJets'+catStr],"W+jets","f")
				except: pass
				try: leg.AddEntry(bkghists['ZJets'+catStr],"Z+jets","f")
				except: pass
				try: leg.AddEntry(bkghists['VV'+catStr],"VV","f")
				except: pass
				leg.AddEntry(hsig1,sig1leg+scaleFact1Str,"l")
				try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
				except: pass
				try: leg.AddEntry(bkghists['TTJets'+catStr],"t#bar{t}","f")
				except: pass
				try: leg.AddEntry(bkghists['T'+catStr],"Single t","f")
				except: pass
				leg.AddEntry(hsig2,sig2leg+scaleFact2Str,"l")
				leg.AddEntry(0, "", "")
				leg.AddEntry(bkgHTgerr,"Bkg uncertainty","f")
		leg.Draw("same")

		#draw the lumi text on the canvas
		CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)
	
		uPad.Update()
		uPad.RedrawAxis()
		frame = uPad.GetFrame()
		uPad.Draw()

		if blind == False and not doRealPull:
			lPad.cd()
			pull=hData.Clone("pull")
			pull.Divide(hData, bkgHT)
			pullData=rt.TGraphAsymmErrors(pull.Clone("pullData"))
			for binNo in range(1,hData.GetNbinsX()+1):
				binLbl = binNo-1
				if 'NJets' in iPlot: 
					#if binNo == 1 or binNo == 5 or binNo == 10 or binNo == 15: pull.GetXaxis().SetBinLabel(binNo,str(binNo))
					if binLbl%2 == 0: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
					else: pull.GetXaxis().SetBinLabel(binNo,'')
				if 'NTJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if 'NWJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if 'NBJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if bkgHT.GetBinContent(binNo)!=0:
					pullData.SetPointEYhigh(binNo-1,gaeData.GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullData.SetPointEYlow(binNo-1,gaeData.GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))
			pull.SetMaximum(3)
			pull.SetMinimum(0)
			pull.SetFillColor(1)
			pull.SetLineColor(1)
			formatLowerHist(pull,iPlot)
			pull.Draw("E0")#"E1")
			
			BkgOverBkg = pull.Clone("bkgOverbkg")
			BkgOverBkg.Divide(bkgHT, bkgHT)
			pullUncBandTot=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandTot.SetPointEYhigh(binNo-1,totBkgTemp3[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandTot.SetPointEYlow(binNo-1,totBkgTemp3[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandTot.SetFillStyle(3001)
			pullUncBandTot.SetFillColor(1)
			pullUncBandTot.SetLineColor(1)
			pullUncBandTot.SetMarkerSize(0)
			rt.gStyle.SetHatchesLineWidth(1)
			pullUncBandTot.Draw("SAME E2")
			
			pullUncBandNorm=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncNorm"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandNorm.SetPointEYhigh(binNo-1,totBkgTemp2[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandNorm.SetPointEYlow(binNo-1,totBkgTemp2[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandNorm.SetFillStyle(3001)
			pullUncBandNorm.SetFillColor(2)
			pullUncBandNorm.SetLineColor(2)
			pullUncBandNorm.SetMarkerSize(0)
			rt.gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandNorm.Draw("SAME E2")
			
			pullUncBandStat=rt.TGraphAsymmErrors(BkgOverBkg.Clone("pulluncStat"))
			for binNo in range(0,hData.GetNbinsX()+2):
				if bkgHT.GetBinContent(binNo)!=0:
					pullUncBandStat.SetPointEYhigh(binNo-1,totBkgTemp1[catStr].GetErrorYhigh(binNo-1)/bkgHT.GetBinContent(binNo))
					pullUncBandStat.SetPointEYlow(binNo-1,totBkgTemp1[catStr].GetErrorYlow(binNo-1)/bkgHT.GetBinContent(binNo))			
			pullUncBandStat.SetFillStyle(3001)
			pullUncBandStat.SetFillColor(3)
			pullUncBandStat.SetLineColor(3)
			pullUncBandStat.SetMarkerSize(0)
			rt.gStyle.SetHatchesLineWidth(1)
			if not doOneBand: pullUncBandStat.Draw("SAME E2")

			pullLegend=rt.TLegend(0.14,0.87,0.85,0.96)
			rt.SetOwnership( pullLegend, 0 )   # 0 = release (not keep), 1 = keep
			pullLegend.SetShadowColor(0)
			pullLegend.SetNColumns(3)
			pullLegend.SetFillColor(0)
			pullLegend.SetFillStyle(0)
			pullLegend.SetLineColor(0)
			pullLegend.SetLineStyle(0)
			pullLegend.SetBorderSize(0)
			pullLegend.SetTextFont(42)
			if not doOneBand: 
				pullLegend.AddEntry(pullUncBandStat , "Bkg uncert (stat)" , "f")
				pullLegend.AddEntry(pullUncBandNorm , "Bkg uncert (stat #oplus norm syst)" , "f")
				pullLegend.AddEntry(pullUncBandTot , "Bkg uncert (stat #oplus all syst)" , "f")
			else: 
				if doAllSys: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert (stat #oplus syst)" , "f")
				else: pullLegend.AddEntry(pullUncBandTot , "Bkg uncert (stat)" , "f")
			#pullLegend.AddEntry(pullQ2up , "Q^{2} Up" , "l")
			#pullLegend.AddEntry(pullQ2dn , "Q^{2} Down" , "l")
			pullLegend.Draw("SAME")
			pull.Draw("SAME")
			lPad.RedrawAxis()

		if blind == False and doRealPull:
			lPad.cd()
			pull=hData.Clone("pull")
			for binNo in range(1,hData.GetNbinsX()+1):
				binLbl = binNo-1
				if 'NJets' in iPlot: 
					#if binNo == 1 or binNo == 5 or binNo == 10 or binNo == 15: pull.GetXaxis().SetBinLabel(binNo,str(binNo))
					if binLbl%2 == 0: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
					else: pull.GetXaxis().SetBinLabel(binNo,'')
				if 'NTJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if 'NWJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if 'NBJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
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
			formatLowerHist(pull,iPlot)
			pull.GetYaxis().SetTitle('#frac{(obs-bkg)}{uncertainty}')
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
		if blind: savePrefix+='_blind'
		if compareShapes: savePrefix+='_shp'
		if plotPostFit: savePrefix+='_postfit'

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
	totBkgMerged = 0.
	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr] = RFile1.Get(histPrefixE+'__'+proc).Clone()
			bkghistsmerged[proc+'isL'+tagStr].Add(RFile1.Get(histPrefixM+'__'+proc))
			if plotPostFit: 
				postFitHist = RPostFile.Get(histPrefixE+'__'+proc).Clone()
				postFitHist.Add(RPostFile.Get(histPrefixM+'__'+proc))
				for ibin in range(1,bkghistsmerged[proc+'isL'+tagStr].GetNbinsX()+1):
					bkghistsmerged[proc+'isL'+tagStr].SetBinContent(ibin,postFitHist.GetBinContent(ibin))
					bkghistsmerged[proc+'isL'+tagStr].SetBinError(ibin,postFitHist.GetBinError(ibin))
			totBkgMerged += bkghistsmerged[proc+'isL'+tagStr].Integral()
		except:pass
	hDatamerged = RFile1.Get(histPrefixE+'__DATA').Clone()
	hDatamerged.Add(RFile1.Get(histPrefixM+'__DATA').Clone())
	gaeDatamerged = rt.TGraphAsymmErrors(hDatamerged.Clone(hDatamerged.GetName().replace("DATA","gaeData")))
	hDatamerged_test = RFile1.Get(histPrefixE+'__DATA').Clone()
	hDatamerged_test.Add(RFile1.Get(histPrefixM+'__DATA').Clone())
	bkgHTmerged_test = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone()
	for proc in bkgProcList:
		if proc==bkgProcList[0]: continue
		try: bkgHTmerged_test.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass
	hsig1merged = RFile1.Get(histPrefixE+'__sig').Clone(histPrefixE+'__sig1merged')
	hsig2merged = RFile2.Get(histPrefixE+'__sig').Clone(histPrefixE+'__sig2merged')
	hsig1merged.Add(RFile1.Get(histPrefixM+'__sig').Clone())
	hsig2merged.Add(RFile2.Get(histPrefixM+'__sig').Clone())
	hsig1merged.Scale(xsec[sig1])
	hsig2merged.Scale(xsec[sig2])

	bkgHTmerged = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone()
	for proc in bkgProcList:
		if proc==bkgProcList[0]: continue
		try: bkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass
	gaeBkgHTmerged = rt.TGraphAsymmErrors(bkgHTmerged.Clone("gaeBkgHTmerged"))

	if doNormByBinWidth:
		for proc in bkgProcList:
			try: normByBinWidth(bkghistsmerged[proc+'isL'+tagStr])
			except: pass
		normByBinWidth(bkgHTmerged)
		normByBinWidth(hsig1merged)
		normByBinWidth(hsig2merged)
		poissonNormByBinWidth(gaeBkgHTmerged,bkgHTmerged)
		poissonNormByBinWidth(gaeDatamerged,hDatamerged)
		normByBinWidth(hDatamerged)
	else: 
		poissonErrors(gaeBkgHTmerged)
		poissonErrors(gaeDatamerged)
	# Yes, there are easier ways using the TH1's but
	# it would be rough to swap objects lower down	

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

	totBkgTemp1['isL'+tagStr] = gaeBkgHTmerged.Clone(bkgHTmerged.GetName()+'shapeOnly')
	totBkgTemp2['isL'+tagStr] = gaeBkgHTmerged.Clone(bkgHTmerged.GetName()+'shapePlusNorm')
	totBkgTemp3['isL'+tagStr] = gaeBkgHTmerged.Clone(bkgHTmerged.GetName()+'All')
	
	for ibin in range(1,bkghistsmerged[bkgProcList[0]+'isL'+tagStr].GetNbinsX()+1):
		errorUp = 0.
		errorDn = 0.
		errorStatUp = gaeBkgHTmerged.GetErrorYhigh(ibin-1)**2
		errorStatDn = gaeBkgHTmerged.GetErrorYlow(ibin-1)**2
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

		totBkgTemp1['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorStatUp))
		totBkgTemp1['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorStatDn))
		totBkgTemp2['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorStatUp+errorNorm))
		totBkgTemp2['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorStatDn+errorNorm))
		totBkgTemp3['isL'+tagStr].SetPointEYhigh(ibin-1,math.sqrt(errorUp+errorNorm+errorStatUp))
		totBkgTemp3['isL'+tagStr].SetPointEYlow(ibin-1, math.sqrt(errorDn+errorNorm+errorStatDn))

	for ibin in range(1, bkgHTmerged_test.GetNbinsX()+1):
		bkgHTmerged_test.SetBinError(ibin,(totBkgTemp3['isL'+tagStr].GetErrorYlow(ibin-1) + totBkgTemp3['isL'+tagStr].GetErrorYhigh(ibin-1))/2 )
	
	prob_KS = bkgHTmerged_test.KolmogorovTest(hDatamerged_test)
	prob_KS_X = bkgHTmerged_test.KolmogorovTest(hDatamerged_test,"X")
	prob_chi2 = hDatamerged_test.Chi2Test(bkgHTmerged_test,"UW")
	chi2 = hDatamerged_test.Chi2Test(bkgHTmerged_test,"UW CHI2")
	if hDatamerged_test.Chi2Test(bkgHTmerged_test,"UW CHI2/NDF")!=0: ndof = int(hDatamerged_test.Chi2Test(bkgHTmerged_test,"UW CHI2")/hDatamerged_test.Chi2Test(bkgHTmerged_test,"UW CHI2/NDF"))
	else: ndof = 0
	print '/'*80,'\n','*'*80
	print histPrefixE.replace('isE','isL')+'_KS =',prob_KS
	print 'WARNING: KS test works on unbinned distributions. For binned histograms, see NOTE3 at https://root.cern.ch/doc/master/classTH1.html#a2747cabe9ebe61c2fdfd74ff307cef3a'
	print '*'*80,'\n','/'*80,'\n','*'*80
	print histPrefixE.replace('isE','isL')+'_Chi2Test:'
	print "p-value =",prob_chi2,"CHI2/NDF",chi2,"/",ndof
	print '*'*80,'\n','/'*80
	table.append(['isL_'+tagStr,prob_KS,prob_KS_X,prob_chi2,chi2,ndof])

	bkgHTgerrmerged = totBkgTemp3['isL'+tagStr].Clone()

	scaleFact1merged = int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum()) - int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum()) % 10
	scaleFact2merged = int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum()) - int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum()) % 10
	if scaleFact1merged==0: scaleFact1merged=int(bkgHTmerged.GetMaximum()/hsig1merged.GetMaximum())
	if scaleFact2merged==0: scaleFact2merged=int(bkgHTmerged.GetMaximum()/hsig2merged.GetMaximum())
	if scaleFact1merged==0: scaleFact1merged=1
	if scaleFact2merged==0: scaleFact2merged=1
	if sigScaleFact>0:
		scaleFact1merged=sigScaleFact
		scaleFact2merged=sigScaleFact
	if not scaleSignals:
		scaleFact1merged=1
		scaleFact2merged=1
	hsig1merged.Scale(scaleFact1merged)
	hsig2merged.Scale(scaleFact2merged)
	
	drawQCDmerged = False
	try: drawQCDmerged = bkghistsmerged['qcdisL'+tagStr].Integral()/bkgHTmerged.Integral()>.005
	except: pass

	stackbkgHTmerged = rt.THStack("stackbkgHTmerged","")
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
	
	if not drawYields: gaeDatamerged.SetMarkerStyle(20)
	gaeDatamerged.SetMarkerSize(1.2)
	gaeDatamerged.SetLineWidth(2)
	gaeDatamerged.SetMarkerColor(rt.kBlack)
	gaeDatamerged.SetLineColor(rt.kBlack)
	if drawYields: gaeDatamerged.SetMarkerSize(4)

	bkgHTgerrmerged.SetFillStyle(3004)
	bkgHTgerrmerged.SetFillColor(rt.kBlack)
	bkgHTgerrmerged.SetLineColor(rt.kBlack)

	c1merged = rt.TCanvas("c1merged","c1merged",50,50,W,H)
	c1merged.SetFillColor(0)
	c1merged.SetBorderMode(0)
	c1merged.SetFrameFillStyle(0)
	c1merged.SetFrameBorderMode(0)
	#c1merged.SetTickx(0)
	#c1merged.SetTicky(0)
	
	yDiv=0.35
	if blind == True: yDiv=0.0
	# overlap the pads a little to hide the error bar gap:
	uPad=rt.TPad("uPad","",0,yDiv,1,1) #for actual plots
	
	uPad.SetLeftMargin( L/W )
	uPad.SetRightMargin( R/W )
	uPad.SetTopMargin( T/H )
	uPad.SetBottomMargin( 0.01 )
	if blind == True: uPad.SetBottomMargin( B/H )
	
	uPad.SetFillColor(0)
	uPad.SetBorderMode(0)
	uPad.SetFrameFillStyle(0)
	uPad.SetFrameBorderMode(0)
	#uPad.SetTickx(0)
	#uPad.SetTicky(0)
	uPad.Draw()
	if blind == False:
		lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner

		lPad.SetLeftMargin( L/W )
		lPad.SetRightMargin( R/W )
		lPad.SetTopMargin( 0.05 )
		lPad.SetBottomMargin( B/H )

		#lPad.SetGridy()
		lPad.SetFillColor(0)
		lPad.SetBorderMode(0)
		lPad.SetFrameFillStyle(0)
		lPad.SetFrameBorderMode(0)
		#lPad.SetTickx(0)
		#lPad.SetTicky(0)
		lPad.Draw()
	if not doNormByBinWidth: gaeDatamerged.SetMaximum(1.2*max(gaeDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
	#gaeDatamerged.SetMinimum(0.015)
	gaeDatamerged.SetTitle("")
	if doNormByBinWidth: gaeDatamerged.GetYaxis().SetTitle("< Events / GeV >")
	#elif isRebinned!='': gaeDatamerged.GetYaxis().SetTitle("Events / bin")
	elif iPlot=='minMlb': gaeDatamerged.GetYaxis().SetTitle("Events / 20 GeV")
	else: gaeDatamerged.GetYaxis().SetTitle("Events / bin")
	formatUpperHist(gaeDatamerged)
	gaeDatamerged.GetXaxis().SetRangeUser(hDatamerged.GetBinLowEdge(1),hDatamerged.GetBinLowEdge(gaeDatamerged.GetN()+1))
	uPad.cd()
	gaeDatamerged.SetTitle("")
	stackbkgHTmerged.SetTitle("")
	if compareShapes: 
		hsig1merged.Scale(totBkgMerged/hsig1merged.Integral())
		hsig2merged.Scale(totBkgMerged/hsig2merged.Integral())
	if not blind: 
		if 'rebinned_stat0p' in isRebinned: gaeDatamerged.Draw("apz1")
		else: gaeDatamerged.Draw("apz0")
	if blind: 
		#hsig1merged.SetMinimum(0.015)
		if doNormByBinWidth: hsig1merged.GetYaxis().SetTitle("< Events / GeV >")
		elif isRebinned!='': hsig1merged.GetYaxis().SetTitle("Events / bin")
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
		if 'rebinned_stat0p' in isRebinned: gaeDatamerged.Draw("pz1")
		else: gaeDatamerged.Draw("pz0") #redraw data so its not hidden
		if drawYields: hDatamerged.Draw("SAME TEXT00") 
	uPad.RedrawAxis()
	bkgHTgerrmerged.Draw("SAME E2")

	chLatexmerged = rt.TLatex()
	chLatexmerged.SetNDC()
	chLatexmerged.SetTextSize(0.06)
	if blind: chLatexmerged.SetTextSize(0.04)
	chLatexmerged.SetTextAlign(21) # align center
	flvString = 'e/#mu+jets'
	tagString = ''
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
	chLatexmerged.DrawLatex(tagPosX, tagPosY, flvString)
	chLatexmerged.DrawLatex(tagPosX, tagPosY-0.06, tagString)

	if drawQCDmerged: legmerged = rt.TLegend(0.43,0.52,0.92,0.87)
	if not drawQCDmerged or blind: legmerged = rt.TLegend(0.40,0.62,0.92,0.87)
	#legmerged = rt.TLegend(0.50,0.35,0.9,0.87)
	#if 'Tau32' in iPlot: legmerged = rt.TLegend(0.3,0.52,0.8,0.87)
	rt.SetOwnership( legmerged, 0 )   # 0 = release (not keep), 1 = keep
	legmerged.SetShadowColor(0)
	legmerged.SetFillColor(0)
	legmerged.SetFillStyle(0)
	legmerged.SetLineColor(0)
	legmerged.SetLineStyle(0)
	legmerged.SetBorderSize(0) 
	legmerged.SetNColumns(2)
	legmerged.SetTextFont(62)#42)
	legmerged.SetColumnSeparation(0.05)
	scaleFact1Str = 'x'+str(scaleFact1)
	scaleFact2Str = 'x'+str(scaleFact2)
	if not scaleSignals:
		scaleFact1Str = ''
		scaleFact2Str = ''
	if drawQCDmerged:
		if not blind:
			legmerged.AddEntry(gaeDatamerged,"Data","ep")
			legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
			legmerged.AddEntry(bkghistsmerged['qcdisL'+tagStr],"QCD","f")
			legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
			try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EWK","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['WJetsisL'+tagStr],"W+jets","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ZJetsisL'+tagStr],"Z+jets","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['VVisL'+tagStr],"VV","f")
			except: pass 
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncertainty","f")
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['TTJetsisL'+tagStr],"t#bar{t}","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['TisL'+tagStr],"Single t","f")
			except: pass
		else:
			legmerged.AddEntry(bkghistsmerged['qcdisL'+tagStr],"QCD","f")
			legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
			try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EWK","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['WJetsisL'+tagStr],"W+jets","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ZJetsisL'+tagStr],"Z+jets","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['VVisL'+tagStr],"VV","f")
			except: pass 
			legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['TTJetsisL'+tagStr],"t#bar{t}","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['TisL'+tagStr],"Single t","f")
			except: pass
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncertainty","f")
	if not drawQCDmerged:
		if not blind: 
			legmerged.AddEntry(gaeDatamerged,"Data","ep")
			legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
			try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EWK","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['WJetsisL'+tagStr],"W+jets","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ZJetsisL'+tagStr],"Z+jets","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['VVisL'+tagStr],"VV","f")
			except: pass
			legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['TTJetsisL'+tagStr],"t#bar{t}","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['TisL'+tagStr],"Single t","f")
			except: pass
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncertainty","f")
		else:
			try: legmerged.AddEntry(bkghistsmerged['ewkisL'+tagStr],"EWK","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['WJetsisL'+tagStr],"W+jets","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['ZJetsisL'+tagStr],"Z+jets","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['VVisL'+tagStr],"VV","f")
			except: pass
			legmerged.AddEntry(hsig1merged,sig1leg+scaleFact1Str,"l")
			try: legmerged.AddEntry(bkghistsmerged['topisL'+tagStr],"TOP","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['TTJetsisL'+tagStr],"t#bar{t}","f")
			except: pass
			try: legmerged.AddEntry(bkghistsmerged['TisL'+tagStr],"Single t","f")
			except: pass
			legmerged.AddEntry(hsig2merged,sig2leg+scaleFact2Str,"l")
			legmerged.AddEntry(0, "", "")
			legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncertainty","f")
	legmerged.Draw("same")

	#draw the lumi text on the canvas
	CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)
	
	uPad.Update()
	uPad.RedrawAxis()
	frame = uPad.GetFrame()
	uPad.Draw()
	
	if blind == False and not doRealPull:
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		pullmerged.Divide(hDatamerged, bkgHTmerged)
		pullmergedData=TGraphAsymmErrors(pullmerged.Clone("pullmergedData"))
		for binNo in range(1,hDatamerged.GetNbinsX()+1):
			binLbl = binNo-1
			if 'NJets' in iPlot: 
				#if binNo == 1 or binNo == 5 or binNo == 10 or binNo == 15: pullmerged.GetXaxis().SetBinLabel(binNo,str(binNo))
				if binLbl%2 == 0: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
				else: pullmerged.GetXaxis().SetBinLabel(binNo,'')
			if 'NTJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if 'NWJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if 'NBJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullmergedData.SetPointEYhigh(binNo-1,gaeDatamerged.GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullmergedData.SetPointEYlow(binNo-1,gaeDatamerged.GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))
		pullmerged.SetMaximum(3)
		pullmerged.SetMinimum(0)
		pullmerged.SetFillColor(1)
		pullmerged.SetLineColor(1)
		formatLowerHist(pullmerged,iPlot)
		pullmerged.Draw("E0")#"E1")
		
		BkgOverBkgmerged = pullmerged.Clone("bkgOverbkgmerged")
		BkgOverBkgmerged.Divide(bkgHTmerged, bkgHTmerged)
		pullUncBandTotmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncTotmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandTotmerged.SetPointEYhigh(binNo-1,totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandTotmerged.SetPointEYlow(binNo-1, totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandTotmerged.SetFillStyle(3001)
		pullUncBandTotmerged.SetFillColor(1)
		pullUncBandTotmerged.SetLineColor(1)
		pullUncBandTotmerged.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		pullUncBandTotmerged.Draw("SAME E2")
		
		pullUncBandNormmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncNormmerged"))
		for binNo in range(0,hData.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandNormmerged.SetPointEYhigh(binNo-1,totBkgTemp2['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandNormmerged.SetPointEYlow(binNo-1, totBkgTemp2['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandNormmerged.SetFillStyle(3001)
		pullUncBandNormmerged.SetFillColor(2)
		pullUncBandNormmerged.SetLineColor(2)
		pullUncBandNormmerged.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandNormmerged.Draw("SAME E2")
		
		pullUncBandStatmerged=rt.TGraphAsymmErrors(BkgOverBkgmerged.Clone("pulluncStatmerged"))
		for binNo in range(0,hDatamerged.GetNbinsX()+2):
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pullUncBandStatmerged.SetPointEYhigh(binNo-1,totBkgTemp1['isL'+tagStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandStatmerged.SetPointEYlow(binNo-1, totBkgTemp1['isL'+tagStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandStatmerged.SetFillStyle(3001)
		pullUncBandStatmerged.SetFillColor(3)
		pullUncBandStatmerged.SetLineColor(3)
		pullUncBandStatmerged.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		if not doOneBand: pullUncBandStatmerged.Draw("SAME E2")

		pullLegendmerged=rt.TLegend(0.14,0.87,0.85,0.96)
		rt.SetOwnership( pullLegendmerged, 0 )   # 0 = release (not keep), 1 = keep
		pullLegendmerged.SetShadowColor(0)
		pullLegendmerged.SetNColumns(3)
		pullLegendmerged.SetFillColor(0)
		pullLegendmerged.SetFillStyle(0)
		pullLegendmerged.SetLineColor(0)
		pullLegendmerged.SetLineStyle(0)
		pullLegendmerged.SetBorderSize(0)
		pullLegendmerged.SetTextFont(42)
		if not doOneBand: 
			pullLegendmerged.AddEntry(pullUncBandStat , "Bkg uncert (stat)" , "f")
			pullLegendmerged.AddEntry(pullUncBandNorm , "Bkg uncert (stat #oplus norm. syst)" , "f")
			pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert (stat #oplus all syst)" , "f")
		else: 
			if doAllSys: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert (stat #oplus syst)" , "f")
			else: pullLegendmerged.AddEntry(pullUncBandTot , "Bkg uncert (stat)" , "f")
		pullLegendmerged.Draw("SAME")
		pullmerged.Draw("SAME")
		lPad.RedrawAxis()

	if blind == False and doRealPull:
		lPad.cd()
		pullmerged=hDatamerged.Clone("pullmerged")
		for binNo in range(1,hDatamerged.GetNbinsX()+1):
			binLbl = binNo-1
			if 'NJets' in iPlot: 
				#if binNo == 1 or binNo == 5 or binNo == 10 or binNo == 15: pullmerged.GetXaxis().SetBinLabel(binNo,str(binNo))
				if binLbl%2 == 0: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
				else: pullmerged.GetXaxis().SetBinLabel(binNo,'')
			if 'NTJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if 'NWJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if 'NBJets' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if hDatamerged.GetBinContent(binNo)!=0:
				MCerror = 0.5*(totBkgTemp3['isL'+tagStr].GetErrorYhigh(binNo-1)+totBkgTemp3['isL'+tagStr].GetErrorYlow(binNo-1))
				pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(MCerror**2+hDatamerged.GetBinError(binNo)**2))
			else: pullmerged.SetBinContent(binNo,0.)
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
		formatLowerHist(pullmerged,iPlot)
		pullmerged.GetYaxis().SetTitle('#frac{(obs-bkg)}{uncertainty}')
		pullmerged.Draw("HIST")
		
		minX = hDatamerged.GetBinLowEdge(1)
		maxX = hDatamerged.GetBinLowEdge(hDatamerged.GetNbinsX()+1)
		line = rt.TLine(minX,0,maxX,0)
		line.SetLineStyle(2)
		line.SetLineColor(rt.kBlack)
		line.Draw()

		lPad.Update()
		lPad.RedrawAxis()
		frame = lPad.GetFrame()
		lPad.Draw()

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
	if blind: savePrefixmerged+='_blind'
	if compareShapes: savePrefixmerged+='_shp'
	if plotPostFit: savePrefixmerged+='_postfit'

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

if not doNormByBinWidth: 
	out=open(templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'+tempsig.replace('templates','GOFtests').replace('.root','').replace(sig1+'_','')+saveKey+'.txt','w')
	printTable(table,out)
			
RFile1.Close()
RFile2.Close()
if plotPostFit: RPostFile.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


