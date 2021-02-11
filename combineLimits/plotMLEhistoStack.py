from ROOT import TFile, TH1D, THStack, TPad, TLegend, TLatex, TGraphAsymmErrors, gROOT, RooPlot
from array import array
from math import *
import os,sys

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

debug = True
yLog = False
blind = True
lumi = 35.9
lumiStr = '_35p867fb'
discrim ='DnnTprime'
mleType = sys.argv[1]

doSys = False
doJustStatUnc = True
doJustSysUnc = False
doAllUnc = False

#open files

dataFile = "/uscms_data/d3/jmanagan/CMSSW_10_2_10/src/tptp_2016/makeTemplates/templatesSRCR_June2020TT/templates_"+discrim+"_TTM1400_bW0p5_tZ0p25_tH0p25"+lumiStr+"_BKGNORM_rebinned_stat0p3.root"

mleFile = "fitDiagnostics.root"
outdir = 'fitDiag_fullMuSmoothed_'+mleType+'/'
if not os.path.exists(outdir): os.system('mkdir -p '+outdir)

isEM = ['isE','isM']
category = ['dnnLargeT','dnnLargeH','dnnLargeW','dnnLargeZ','dnnLargeB','dnnLargeJwjet','dnnLargeJttbar']
if not blind and 'All' in mleType: category = category + ['taggedbWbW','taggedtZbW','taggedtHbW','taggedtZHtZH','notVbW','notVtZ','notVtH',
							  'notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W']
Prefix = discrim+lumiStr+'_'+isEM[0]+'_'+category[0]+'_DeepAK8'
CombPrefix = 'TT_isCR_'+category[0]+'_DeepAK8'

#set data histo
rFile = TFile.Open(dataFile)
rFile_mle = TFile.Open(mleFile+".root")

hdata={}
bins={}
bins_array={}
for em in isEM:
	for cat in category:
		if 'dnnLarge' in cat: Prefix = Prefix.replace(discrim,'HTNtag')
		print "Getting DATA: ",Prefix.replace(isEM[0],em).replace(category[0],cat)
		hdata[em+cat] = (rFile.Get(Prefix.replace(isEM[0],em).replace(category[0],cat)+"__DATA")).Clone()
		hdata[em+cat].SetDirectory(0)

		formatDataPlot(hdata[em+cat])

		if em==isEM[0]:
			bins_array[cat] = hdata[em+cat].GetXaxis().GetXbins()
			binstemp = []
			for ibin in xrange(bins_array[cat].GetSize()):
				binstemp.append(bins_array[cat].At(ibin))
			bins[cat] = binstemp

#define dictionaries

htop = {}
hewk = {}
hqcd = {}

htop_tmp = {}
hewk_tmp = {}
hqcd_tmp = {}

hs = {}
htotbkg = {}
htotbkgErr = {}

leg = {}

pull = {}
pullUncBandTot = {}

#define dictionaries for doSys
if doSys:
	sysList = [
		'elIdSys',
		'muIdSys',
		#'elIsoSys',
		#'muIsoSys',
		#'elRecoSys',
		#'muRecoSys',
		'trigeffEl',
		'trigeffMu',
		'lumiSys',
		'pileup',
		'jec',
		'jer',
		'jsf',
		'ltag',
		'btag',
		'muRFcorrdNewTop',
		'muRFcorrdNewEwk',
		'muRFcorrdNewQCD',
		'TOPrate',
		'EWKrate',
		'QCDrate',
		'Teff',
		'Tmis',
		'Heff',
		'Hmis',
		'Zeff',
		'Zmis',
		'Weff',
		'Wmis',
		'Beff',
		'Bmis',
		#'Jeff',
		#'Jmis',
		]

	mleFileSys = {}
	rFile_mle_sys = {}

	print "opening uncertainty files:" 
	for sys in sysList:
		print "	",sys,
		for PM in ['plus','minus']:
			mleFileSys[sys+PM] = "histos-mle_"+mleType+"_"+sys+"_"+PM
			rFile_mle_sys[sys+PM] = ROOT.TFile(mleFileSys[sys+PM]+".root")	
		print " done ..."


	#initilize dictionaries
	htopSys = {}
	hewkSys = {}
	hqcdSys = {}

	htop_tmpSys = {}
	hewk_tmpSys = {}
	hqcd_tmpSys = {}
	
	htotbkgSys = {}

for em in isEM:
	for cat in category:

	        #set bkg histo
		htop[em+cat] = ROOT.TH1D("h"+em+cat+"__top","h"+em+cat+"__top",bins_array[cat].GetSize()-1,array('d',bins[cat]))
		hewk[em+cat] = ROOT.TH1D("h"+em+cat+"__ewk","h"+em+cat+"__ewk",bins_array[cat].GetSize()-1,array('d',bins[cat]))
		hqcd[em+cat] = ROOT.TH1D("h"+em+cat+"__qcd","h"+em+cat+"__qcd",bins_array[cat].GetSize()-1,array('d',bins[cat]))
		#print 'htop nbins = ',htop[em+cat].GetNbinsX()

		htop_tmp[em+cat] = (rFile_mle.Get(Prefix.replace(isEM[0],em).replace(category[0],cat)+"__top")).Clone()
		hewk_tmp[em+cat] = (rFile_mle.Get(Prefix.replace(isEM[0],em).replace(category[0],cat)+"__ewk")).Clone()
		hqcd_tmp[em+cat] = (rFile_mle.Get(Prefix.replace(isEM[0],em).replace(category[0],cat)+"__qcd")).Clone()
	
		for ibin in xrange(bins_array[cat].GetSize()):
			#print 'ibin = ',ibin, 'Low edge =',bins_array[cat][ibin],"top content = ",htop_tmp[em+cat].GetBinContent(ibin+1)
			htop[em+cat].SetBinContent(ibin+1,htop_tmp[em+cat].GetBinContent(ibin+1))
			hewk[em+cat].SetBinContent(ibin+1,hewk_tmp[em+cat].GetBinContent(ibin+1))
			hqcd[em+cat].SetBinContent(ibin+1,hqcd_tmp[em+cat].GetBinContent(ibin+1))
	
			htop[em+cat].SetBinError(ibin+1,htop_tmp[em+cat].GetBinError(ibin+1))
			hewk[em+cat].SetBinError(ibin+1,hewk_tmp[em+cat].GetBinError(ibin+1))
			hqcd[em+cat].SetBinError(ibin+1,hqcd_tmp[em+cat].GetBinError(ibin+1))
	
	        #set color
		formatTOPPlot(htop[em+cat])
		formatEWKPlot(hewk[em+cat])
		formatQCDPlot(hqcd[em+cat])
	
	        #Arrange stacks and htotbkg
		print 'Creating THStacks and htotbkg for',cat
		hs[em+cat] = THStack("hs"+em+cat+"","hs"+em+cat+"")
		htotbkg[em+cat] = ROOT.TH1D("h"+em+cat+"__totbkg","h"+em+cat+"__totbkg",bins_array[cat].GetSize()-1,array('d',bins[cat]))
	        #try: 
		hs[em+cat].Add(hewk[em+cat])
		hs[em+cat].Add(htop[em+cat])
		hs[em+cat].Add(hqcd[em+cat])
	
		htotbkg[em+cat].Add(hewk[em+cat])
		htotbkg[em+cat].Add(htop[em+cat])
		htotbkg[em+cat].Add(hqcd[em+cat])
		#except: pass
	
	        #check	
		#for ibin in xrange(bins_array[cat].GetSize()+2):
		#	print '			bin:',bin,' content:',htotbkg[em+cat].GetBinContent(ibin)
	
	        #setup histo for uncertainties:
		if doSys:
			
			print 'Setting up histo for uncertainties for ',cat,' ...'
			
			htopSys[em+cat] = {}
			hewkSys[em+cat] = {}
			hqcdSys[em+cat] = {}
	
			htop_tmpSys[em+cat] = {}
			hewk_tmpSys[em+cat] = {}
			hqcd_tmpSys[em+cat] = {}
	
			htotbkgSys[em+cat] = {}
	
			for sys in sysList:
				for PM in ['plus','minus']:
					htopSys[em+cat][sys+PM] = ROOT.TH1D("h"+em+cat+"__top__"+sys+PM,"h"+em+cat+"__top__"+sys+PM,bins_array[cat].GetSize()-1,array('d',bins[cat]))
					hewkSys[em+cat][sys+PM] = ROOT.TH1D("h"+em+cat+"__ewk__"+sys+PM,"h"+em+cat+"__ewk__"+sys+PM,bins_array[cat].GetSize()-1,array('d',bins[cat]))
					hqcdSys[em+cat][sys+PM] = ROOT.TH1D("h"+em+cat+"__qcd__"+sys+PM,"h"+em+cat+"__qcd__"+sys+PM,bins_array[cat].GetSize()-1,array('d',bins[cat]))
	
					htop_tmpSys[em+cat][sys+PM] = (rFile_mle_sys[sys+PM].Get(Prefix.replace(isEM[0],em).replace(category[0],cat)+"__top")).Clone()
					hewk_tmpSys[em+cat][sys+PM] = (rFile_mle_sys[sys+PM].Get(Prefix.replace(isEM[0],em).replace(category[0],cat)+"__ewk")).Clone()
					hqcd_tmpSys[em+cat][sys+PM] = (rFile_mle_sys[sys+PM].Get(Prefix.replace(isEM[0],em).replace(category[0],cat)+"__qcd")).Clone()
	
					for ibin in xrange(bins_array[cat].GetSize()+2):
						htopSys[em+cat][sys+PM].SetBinContent(ibin,htop_tmpSys[em+cat][sys+PM].GetBinContent(ibin))
						hewkSys[em+cat][sys+PM].SetBinContent(ibin,hewk_tmpSys[em+cat][sys+PM].GetBinContent(ibin))
						hqcdSys[em+cat][sys+PM].SetBinContent(ibin,hqcd_tmpSys[em+cat][sys+PM].GetBinContent(ibin))
	
						htopSys[em+cat][sys+PM].SetBinError(ibin,htop_tmpSys[em+cat][sys+PM].GetBinError(ibin))
						hewkSys[em+cat][sys+PM].SetBinError(ibin,hewk_tmpSys[em+cat][sys+PM].GetBinError(ibin))
						hqcdSys[em+cat][sys+PM].SetBinError(ibin,hqcd_tmpSys[em+cat][sys+PM].GetBinError(ibin))
	
					print '		creating totBkg',sys,PM,'histo ...'
					htotbkgSys[em+cat][sys+PM] = ROOT.TH1D("h"+em+cat+"__totbkg__"+sys+PM,"h"+em+cat+"__totbkg__"+sys+PM,bins_array[cat].GetSize()-1,array('d',bins[cat]))
					#try: 
					htotbkgSys[em+cat][sys+PM].Add(htopSys[em+cat][sys+PM])
					htotbkgSys[em+cat][sys+PM].Add(hewkSys[em+cat][sys+PM])
					htotbkgSys[em+cat][sys+PM].Add(hqcdSys[em+cat][sys+PM])
					#except: pass
	
					#check
					#for ibin in xrange(bins_array[cat].GetSize()+2):
					#	print '			bin:',bin,' content:',htotbkgSys[em+cat][sys+PM].GetBinContent(ibin)
		

#Set up yield uncertainties
print 'Set up yield uncertainties'
sysSqErr = {}
totBkgSqErr = {}
if doSys:
	for em in isEM:
		for cat in category:
		
			#initialize
			print '	Initialize sysSqErr'
			sysSqErr[em+cat] = {}			
			for sys in sysList:
				for PM in ['plus','minus']:
					sysSqErr[em+cat][sys+PM] = {}			
					for ibin in xrange(bins_array[cat].GetSize()+2):
						i = str(ibin)
						sysSqErr[em+cat][sys+PM][i] = 0 
						#print '		sysSqErr[',cat,'][',sys+PM,'][',i,'] = ', sysSqErr[em+cat][sys+PM][i] 
			#initialize
			print '	Initialize totBkgSqErr'
			totBkgSqErr[em+cat] = {}
			for PM in ['plus','minus']:
				totBkgSqErr[em+cat][PM] = {}			
				for ibin in xrange(bins_array[cat].GetSize()+2):
					i = str(ibin)
					totBkgSqErr[em+cat][PM][i] = 0 
	
			
			#fill
			print '	Fill'
			for sys in sysList:
	
				for PM in ['plus','minus']:
					for ibin in xrange(bins_array[cat].GetSize()+2):
						i = str(ibin)
						diffErr = htotbkgSys[em+cat][sys+PM].GetBinContent(ibin)-htotbkg[em+cat].GetBinContent(ibin)
						if diffErr > 0:
							sysSqErr[em+cat][sys+'plus'][i] += diffErr*diffErr
							print '		sysSqErr[',em+cat,'][',sys,'plus][',i,'] = ', sysSqErr[em+cat][sys+'plus'][i] 
						if diffErr < 0:
							sysSqErr[em+cat][sys+'minus'][i] += diffErr*diffErr
							print '		sysSqErr[',em+cat,'][',sys,'minus][',i,'] = ', sysSqErr[em+cat][sys+'minus'][i] 
	
				for PM in ['plus','minus']:
					for ibin in xrange(bins_array[cat].GetSize()+2):
						i = str(ibin)				
						totBkgSqErr[em+cat][PM][i] += sysSqErr[em+cat][sys+PM][i]
						print '		totBkgSqErr[',em+cat,'][',PM,'][',i,'] = ', totBkgSqErr[em+cat][PM][i] 
	
for em in isEM:
	for cat in category:
		print 'Drawing ', em, cat

		canvas = ROOT.TCanvas("canvas","canvas",800,800)
	
		gStyle.SetOptStat(0)
		gStyle.SetErrorX(0.5)
		yDiv=0.35
		uMargin = 0
		rMargin=.04
		uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
		uPad.SetTopMargin(0.10)
		uPad.SetBottomMargin(uMargin)
		uPad.SetRightMargin(rMargin)
		uPad.SetLeftMargin(.12)
		uPad.Draw()
		lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
		lPad.SetTopMargin(0)
		lPad.SetBottomMargin(.4)
		lPad.SetRightMargin(rMargin)
		lPad.SetLeftMargin(.12)
		lPad.SetGridy()
		lPad.Draw()
		hdata[em+cat].SetMinimum(0.015)
		hdata[em+cat].SetTitle("")
		hdata[em+cat].GetYaxis().SetTitle("Events")
		formatUpperHist(hdata[em+cat])
	
		uPad.cd()
	
		hdata[em+cat].Draw("E1 X0")
		hs[em+cat].Draw("SAME HIST")
		hdata[em+cat].Draw("SAME E1 X0")
	
		uPad.RedrawAxis()
	
		leg[em+cat] = TLegend(0.65,0.53,0.95,0.90)
		leg[em+cat].SetShadowColor(0)
		leg[em+cat].SetFillColor(0)
		leg[em+cat].SetFillStyle(0)
		leg[em+cat].SetLineColor(0)
		leg[em+cat].SetLineStyle(0)
		leg[em+cat].SetBorderSize(0) 
		leg[em+cat].SetTextFont(42)
		leg[em+cat].AddEntry(hdata[em+cat],"DATA")
		
		try: leg[em+cat].AddEntry(hqcd[em+cat],"QCD","f")
		except: pass
		try: leg[em+cat].AddEntry(htop[em+cat],"TOP","f")
		except: pass
		try: leg[em+cat].AddEntry(hewk[em+cat],"EWK","f")
		except: pass
		#leg.AddEntry(bkgHTgerr,"Bkg uncert. (stat. #oplus syst.)","f")
		leg[em+cat].Draw("SAME")
	
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
		prelimTex3.DrawLatex(0.24,0.975,"Preliminary")
	
		chLatex = TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.06)
		chLatex.SetTextAlign(11) # align right                                                                                                                                                                                         
		chString = ''
		if em=='isE': chString+='e+jets'
		if em=='isM': chString+='#mu+jets'
		chLatex.DrawLatex(0.16, 0.82, chString)
		chLatex.DrawLatex(0.16, 0.75, cat)
	
		lPad.cd() #LOWER PAD
		
		#Setup data/mc ratio plot 
		pull[em+cat]=hdata[em+cat].Clone("pull")
	# 	try: 
		print 'Dividing pull: data bins = ',hdata[em+cat].GetNbinsX(),' totbkg bins = ',htotbkg[em+cat].GetNbinsX()
		pull[em+cat].Divide(htotbkg[em+cat])
	# 	except: pass	
		
	# 	try:
		if debug: print 'bin ','			hdata','				hbkg','			ratio','			','statErr','		','errPlus','		','errPlus'
		for ibin in range(0,hdata[em+cat].GetNbinsX()+2):
			if debug: print ibin,'			',hdata[em+cat].GetBinContent(ibin),'+-',round(hdata[em+cat].GetBinError(ibin),2),'			',round(htotbkg[em+cat].GetBinContent(ibin),2),
	
			#set up error bar on ratio plot (data uncertainty)
			dataStatErr= 0.
			if (htotbkg[em+cat].GetBinContent(ibin))!=0:
				if debug: print '			',round(hdata[em+cat].GetBinContent(ibin)/htotbkg[em+cat].GetBinContent(ibin),2),
				dataStatErr = hdata[em+cat].GetBinError(ibin)/(htotbkg[em+cat].GetBinContent(ibin)) #is this right?
			else: 
				if debug: print '			',0.0,
			pull[em+cat].SetBinError(ibin,dataStatErr) #is this right?
	
			### setup MC uncertainties	FOR PRINT only
			statErr = htotbkg[em+cat].GetBinError(ibin)
			statErrLow = htotbkg[em+cat].GetBinErrorLow(ibin)
			statErrUp = htotbkg[em+cat].GetBinErrorUp(ibin)
			sysSqErrPlus = 0.0
			sysSqErrMinus = 0.0
			if doSys:
				sysSqErrPlus = totBkgSqErr[em+cat]['plus'][str(ibin)]
				sysSqErrMinus = totBkgSqErr[em+cat]['minus'][str(ibin)]
			totErrPlus = 0.0
			totErrMinus = 0.0
			if(doJustStatUnc):
				totErrPlus = sqrt(statErr*statErr) #is this right??
				totErrMinus = sqrt(statErr*statErr)
			elif(doJustSysUnc):
				totErrPlus = sqrt(sysSqErrPlus) #is this right??
				totErrMinus = sqrt(sysSqErrMinus)
			elif(doAllUnc):
				totErrPlus = sqrt(statErr*statErr + sysSqErrPlus) #is this right??
				totErrMinus = sqrt(statErr*statErr + sysSqErrMinus)
			if debug: print '			',round(statErr,2),#round(statErrUp,2),round(statErrLow,2),
			if debug: print '			',round(totErrPlus,2),
			if debug: print '			',round(totErrMinus,2)		
	# 	except: pass
		
		pull[em+cat].SetMaximum(3)
		pull[em+cat].SetMinimum(0)
		pull[em+cat].SetFillColor(1)
		pull[em+cat].SetMarkerStyle(20)
		pull[em+cat].SetLineColor(1)
		formatLowerHist(pull[em+cat])
	
		pull[em+cat].Draw("SAME E0")
	
		### setup MC uncertainties for histogram
	
		BkgOverBkg = pull[em+cat].Clone("bkgOverbkg")
	# 	try: 
		BkgOverBkg.Divide(htotbkg[em+cat], htotbkg[em+cat])
	# 	except: pass
		pullUncBandTot[em+cat] = TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
		htotbkgErr[em+cat] = TGraphAsymmErrors(htotbkg[em+cat].Clone("htotbkgErr"))
	
	# 	try:
		for ibin in range(0,hdata[em+cat].GetNbinsX()+2):
			statErr = htotbkg[em+cat].GetBinError(ibin)
			statErrLow = htotbkg[em+cat].GetBinErrorLow(ibin)
			statErrUp = htotbkg[em+cat].GetBinErrorUp(ibin)
	
			sysSqErrPlus = 0.0
			sysSqErrMinus = 0.0
			if doSys:
				sysSqErrPlus = totBkgSqErr[em+cat]['plus'][str(ibin)]
				sysSqErrMinus = totBkgSqErr[em+cat]['minus'][str(ibin)]
			totErrPlus = 0.0
			totErrMinus = 0.0
			if(doJustStatUnc):
				totErrPlus = sqrt(statErr*statErr) #is this right??
				totErrMinus = sqrt(statErr*statErr)
			elif(doJustSysUnc):
				totErrPlus = sqrt(sysSqErrPlus) #is this right??
				totErrMinus = sqrt(sysSqErrMinus)
			elif(doAllUnc):
				totErrPlus = sqrt(statErr*statErr + sysSqErrPlus) #is this right??
				totErrMinus = sqrt(statErr*statErr + sysSqErrMinus)
	
			htotbkgErr[em+cat].SetPointEYhigh(ibin-1,totErrPlus)
			htotbkgErr[em+cat].SetPointEYlow(ibin-1,totErrMinus)			
			if htotbkg[em+cat].GetBinContent(ibin)!=0:
				pullUncBandTot[em+cat].SetPointEYhigh(ibin-1,totErrPlus/htotbkg[em+cat].GetBinContent(ibin))
				pullUncBandTot[em+cat].SetPointEYlow(ibin-1,totErrMinus/htotbkg[em+cat].GetBinContent(ibin))
			else:			
				pullUncBandTot[em+cat].SetPointEYhigh(ibin-1,0.)
				pullUncBandTot[em+cat].SetPointEYlow(ibin-1,0.)
	# 	except: pass
	
		pullUncBandTot[em+cat].SetFillStyle(3344)
		pullUncBandTot[em+cat].SetFillColor(1)
		pullUncBandTot[em+cat].SetLineColor(1)
		pullUncBandTot[em+cat].SetMarkerSize(0)
		gStyle.SetHatchesLineWidth(1)
		pullUncBandTot[em+cat].Draw("SAME E2")
	
		lPad.RedrawAxis()
	
		uPad.cd()
		if doSys:
			htotbkgErr[em+cat].SetFillStyle(3004)
			htotbkgErr[em+cat].SetFillColor(kBlack)
			htotbkgErr[em+cat].Draw("SAME E2")
		uPad.RedrawAxis()
	
		if doJustStatUnc:
			canvas.SaveAs(outdir+"/"+em+"_"+cat+"_onlyStatUnc.png")
			canvas.SaveAs(outdir+"/"+em+"_"+cat+"_onlyStatUnc.pdf")
	
		if doJustSysUnc:
			canvas.SaveAs(outdir+"/"+em+"_"+cat+"_onlySysUnc.png")
			canvas.SaveAs(outdir+"/"+em+"_"+cat+"_onlySysUnc.pdf")
	
		if doAllUnc:
			canvas.SaveAs(outdir+"/"+em+"_"+cat+".png")
			canvas.SaveAs(outdir+"/"+em+"_"+cat+".pdf")
	
	
	
	
	
