from ROOT import *
from array import array
from math import *

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

debug = True
yLog = False
lumi = 35.9
doSys = True
doJustStatUnc = False
doJustSysUnc = True
doAllUnc = False

def formatDataPlot(histo):
	histo.SetMarkerStyle(20)
	histo.SetMarkerSize(1.2)
	histo.SetLineWidth(2)

def formatTOPPlot(hTOP):
	hTOP.SetLineColor(kAzure-6)
	hTOP.SetFillColor(kAzure-6)
	hTOP.SetLineWidth(2)

def formatEWKPlot(hEWK):
	hEWK.SetLineColor(kMagenta-2)
	hEWK.SetFillColor(kMagenta-2)
	hEWK.SetLineWidth(2)

def formatDDBKGPlot(hDDBKG):
	hDDBKG.SetLineColor(15)
	hDDBKG.SetFillColor(15)
	hDDBKG.SetLineWidth(2)

def formatUpperHist(histogram):
	histogram.GetXaxis().SetLabelSize(0)
	histogram.GetYaxis().SetLabelSize(0.07)
	histogram.GetYaxis().SetTitleSize(0.08)
	histogram.GetYaxis().SetTitleOffset(.71)

	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.0001)
# 	histogram.SetMinimum(0.001)
	histogram.SetMinimum(0.25)
	if yLog:
		uPad.SetLogy()
		histogram.SetMinimum(0.1)
		
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
#	histogram.GetYaxis().SetRangeUser(0,1.99)
	histogram.GetYaxis().SetRangeUser(0,2.99)
	histogram.GetYaxis().CenterTitle()


#open files

# dataFile = "/user_data/rsyarif/optimization_reMiniAOD_PRv9_FRv30CR2_newRunH_correctedMuTrkSF_AllSys_2017_4_14/lep1Pt0_jetPt0_MET20_NJets3_NBJets1_HT0_ST0_mllOS20/Shape_accurateLHESys_FRsysMar28_newSigSF/templates_STrebinnedv2_TTM1000_bW0p5_tZ0p25_tH0p25_35p867fb.root"
dataFile = "/user_data/rsyarif/optimization_reMiniAOD_PRv9_FRv30CR2_newRunH_correctedMuTrkSF_AllSys_2017_4_14/lep1Pt0_jetPt0_MET20_NJets3_NBJets1_HT0_ST0_mllOS20/Shape_accurateLHESys_FRsysMar28_newSigSF_AsymmFRsys/templates_STrebinnedv2_TTM1000_bW0p5_tZ0p25_tH0p25_35p867fb.root"
# dataFile = "/user_data/rsyarif/optimization_reMiniAOD_PRv10_FRv42CR2_newRunH_correctedMuTrkSF_AllSys_2017_7_4/lep1Pt0_jetPt0_MET20_NJets3_NBJets1_HT0_ST0_mllOS20/Shape_accurateLHESys_FRsysMar28_newSigSF_AsymmFRsys/templates_STrebinnedv2_TTM1000_bW0p5_tZ0p25_tH0p25_35p867fb.root"
mleFile = "histos-mle_templates_STrebinnedv2_TTM1000_bW0p5_tZ0p25_tH0p25_35p867fb_bkgonly"

rFile = ROOT.TFile(dataFile)
rFile_mle = ROOT.TFile(mleFile+".root")

category = ['EEE','EEM','EMM','MMM']

#set data histo

hdata={}
for cat in category:
	hdata[cat] = rFile.Get("triLep"+cat+"__DATA")
	formatDataPlot(hdata[cat])
		
	#get original binning (for some reason the bins centers are shifted)

	bins_array = hdata[cat].GetXaxis().GetXbins()
	bins=[]
	for ibin in xrange(bins_array.GetSize()):
		bins.append(bins_array.At(ibin))

#define dictionaries

htop = {}
hewk = {}
hddbkg = {}

htop_tmp = {}
hewk_tmp = {}
hddbkg_tmp = {}

hs = {}
htotbkg = {}
htotbkgErr = {}

leg = {}

pull = {}
pullUncBandTot = {}

#define dictionaries for doSys
if doSys:
	sysList = [
				'pdfNew',
	# 			'muRFcorrdNewSig',
				'muRFcorrdNewEwk',
				'muRFcorrdNewTop',
				'btag',
				'mistag',
				'jer',
				'jec',
				'pileup',
# 				'mumumuTrigSys',
# 				'elmumuTrigSys',
# 				'elelmuTrigSys',
# 				'elelelTrigSys',
				'mmmTrigSys',
				'emmTrigSys',
				'eemTrigSys',
				'eeeTrigSys',
				'muIsoSys',
				'elIsoSys',
				'muIdSys',
				'elIdSys',
# 				'FRsys', #closure in ttbar
				'muFReta',
				'muFR',
				'elFR',
				'muPRsys', #varying to 1.0
				'elPRsys', #varying to 1.0
# 				'muPR',
# 				'elPR',
				'lumiSys',
				]
	mleFileSys = {}
	rFile_mle_sys = {}

	print "opening uncertainty files:" 
	for sys in sysList:
		print "	",sys,
		for PM in ['plus','minus']:
			mleFileSys[sys+PM] = "histos-mle_"+sys+"_"+PM+"_templates_STrebinnedv2_TTM1000_bW0p5_tZ0p25_tH0p25_35p867fb_bkgonly"
			rFile_mle_sys[sys+PM] = ROOT.TFile(mleFileSys[sys+PM]+".root")	
		print " done ..."


	#initilize dictionaries
	htopSys = {}
	hewkSys = {}
	hddbkgSys = {}

	htop_tmpSys = {}
	hewk_tmpSys = {}
	hddbkg_tmpSys = {}
	
	htotbkgSys = {}

for cat in category:

	#set bkg histo
	htop[cat] = ROOT.TH1D("h"+cat+"__top","h"+cat+"__top",bins_array.GetSize()-1,array('d',bins))
	hewk[cat] = ROOT.TH1D("h"+cat+"__ewk","h"+cat+"__ewk",bins_array.GetSize()-1,array('d',bins))
	hddbkg[cat] = ROOT.TH1D("h"+cat+"__ddbkg","h"+cat+"__ddbkg",bins_array.GetSize()-1,array('d',bins))

	htop_tmp[cat] = rFile_mle.Get("triLep"+cat+"__top")
	hewk_tmp[cat] = rFile_mle.Get("triLep"+cat+"__ewk")
	hddbkg_tmp[cat] = rFile_mle.Get("triLep"+cat+"__ddbkg")

	for ibin in xrange(bins_array.GetSize()+2):
		htop[cat].SetBinContent(ibin,htop_tmp[cat].GetBinContent(ibin))
		hewk[cat].SetBinContent(ibin,hewk_tmp[cat].GetBinContent(ibin))
		hddbkg[cat].SetBinContent(ibin,hddbkg_tmp[cat].GetBinContent(ibin))

		htop[cat].SetBinError(ibin,htop_tmp[cat].GetBinError(ibin))
		hewk[cat].SetBinError(ibin,hewk_tmp[cat].GetBinError(ibin))
		hddbkg[cat].SetBinError(ibin,hddbkg_tmp[cat].GetBinError(ibin))
	
	#set color
	formatTOPPlot(htop[cat])
	formatEWKPlot(hewk[cat])
	formatDDBKGPlot(hddbkg[cat])
	
	#Arrange stacks and htotbkg
	print 'Creating THStacks and htotbkg for',cat
	hs[cat] = THStack("hs"+cat+"","hs"+cat+"")
	htotbkg[cat] = ROOT.TH1D("h"+cat+"__totbkg","h"+cat+"__totbkg",bins_array.GetSize()-1,array('d',bins))
# 	try: 
	hs[cat].Add(htop[cat])
	hs[cat].Add(hewk[cat])
	hs[cat].Add(hddbkg[cat])

	htotbkg[cat].Add(htop[cat])
	htotbkg[cat].Add(hewk[cat])
	htotbkg[cat].Add(hddbkg[cat])
# 	except: pass

	#check	
# 	for ibin in xrange(bins_array.GetSize()+2):
# 		print '			bin:',bin,' content:',htotbkg[cat].GetBinContent(ibin)

	#setup histo for uncertainties:
	if doSys:
		
		print 'Setting up histo for uncertainties for ',cat,' ...'
		
		htopSys[cat] = {}
		hewkSys[cat] = {}
		hddbkgSys[cat] = {}

		htop_tmpSys[cat] = {}
		hewk_tmpSys[cat] = {}
		hddbkg_tmpSys[cat] = {}

		htotbkgSys[cat] = {}

		for sys in sysList:
			for PM in ['plus','minus']:
				htopSys[cat][sys+PM] = ROOT.TH1D("h"+cat+"__top__"+sys+PM,"h"+cat+"__top__"+sys+PM,bins_array.GetSize()-1,array('d',bins))
				hewkSys[cat][sys+PM] = ROOT.TH1D("h"+cat+"__ewk__"+sys+PM,"h"+cat+"__ewk__"+sys+PM,bins_array.GetSize()-1,array('d',bins))
				hddbkgSys[cat][sys+PM] = ROOT.TH1D("h"+cat+"__ddbkg__"+sys+PM,"h"+cat+"__ddbkg__"+sys+PM,bins_array.GetSize()-1,array('d',bins))

				htop_tmpSys[cat][sys+PM] = rFile_mle_sys[sys+PM].Get("triLep"+cat+"__top")
				hewk_tmpSys[cat][sys+PM] = rFile_mle_sys[sys+PM].Get("triLep"+cat+"__ewk")
				hddbkg_tmpSys[cat][sys+PM] = rFile_mle_sys[sys+PM].Get("triLep"+cat+"__ddbkg")

				for ibin in xrange(bins_array.GetSize()+2):
					htopSys[cat][sys+PM].SetBinContent(ibin,htop_tmpSys[cat][sys+PM].GetBinContent(ibin))
					hewkSys[cat][sys+PM].SetBinContent(ibin,hewk_tmpSys[cat][sys+PM].GetBinContent(ibin))
					hddbkgSys[cat][sys+PM].SetBinContent(ibin,hddbkg_tmpSys[cat][sys+PM].GetBinContent(ibin))

					htopSys[cat][sys+PM].SetBinError(ibin,htop_tmpSys[cat][sys+PM].GetBinError(ibin))
					hewkSys[cat][sys+PM].SetBinError(ibin,hewk_tmpSys[cat][sys+PM].GetBinError(ibin))
					hddbkgSys[cat][sys+PM].SetBinError(ibin,hddbkg_tmpSys[cat][sys+PM].GetBinError(ibin))

				print '		creating totBkg',sys,PM,'histo ...'
				htotbkgSys[cat][sys+PM] = ROOT.TH1D("h"+cat+"__totbkg__"+sys+PM,"h"+cat+"__totbkg__"+sys+PM,bins_array.GetSize()-1,array('d',bins))
# 				try: 
				htotbkgSys[cat][sys+PM].Add(htopSys[cat][sys+PM])
				htotbkgSys[cat][sys+PM].Add(hewkSys[cat][sys+PM])
				htotbkgSys[cat][sys+PM].Add(hddbkgSys[cat][sys+PM])
# 				except: pass

				#check
# 				for ibin in xrange(bins_array.GetSize()+2):
					#print '			bin:',bin,' content:',htotbkgSys[cat][sys+PM].GetBinContent(ibin)
		

#Set up yield uncertainties
print 'Set up yield uncertainties'
sysSqErr = {}
totBkgSqErr = {}
if doSys:
	for cat in category:
		
		#initialize
		print '	Initialize sysSqErr'
		sysSqErr[cat] = {}			
		for sys in sysList:
			for PM in ['plus','minus']:
				sysSqErr[cat][sys+PM] = {}			
				for ibin in xrange(bins_array.GetSize()+2):
					i = str(ibin)
					sysSqErr[cat][sys+PM][i] = 0 
					#print '		sysSqErr[',cat,'][',sys+PM,'][',i,'] = ', sysSqErr[cat][sys+PM][i] 
		#initialize
		print '	Initialize totBkgSqErr'
		totBkgSqErr[cat] = {}
		for PM in ['plus','minus']:
			totBkgSqErr[cat][PM] = {}			
			for ibin in xrange(bins_array.GetSize()+2):
				i = str(ibin)
				totBkgSqErr[cat][PM][i] = 0 

		
		#fill
		print '	Fill'
		for sys in sysList:

			for PM in ['plus','minus']:
				for ibin in xrange(bins_array.GetSize()+2):
					i = str(ibin)
					diffErr = htotbkgSys[cat][sys+PM].GetBinContent(ibin)-htotbkg[cat].GetBinContent(ibin)
					if diffErr > 0:
						sysSqErr[cat][sys+'plus'][i] += diffErr*diffErr
						print '		sysSqErr[',cat,'][',sys,'plus][',i,'] = ', sysSqErr[cat][sys+'plus'][i] 
					if diffErr < 0:
						sysSqErr[cat][sys+'minus'][i] += diffErr*diffErr
						print '		sysSqErr[',cat,'][',sys,'minus][',i,'] = ', sysSqErr[cat][sys+'minus'][i] 

			for PM in ['plus','minus']:
				for ibin in xrange(bins_array.GetSize()+2):
					i = str(ibin)				
					totBkgSqErr[cat][PM][i] += sysSqErr[cat][sys+PM][i]
					print '		totBkgSqErr[',cat,'][',PM,'][',i,'] = ', totBkgSqErr[cat][PM][i] 

canvas = ROOT.TCanvas("canvas","canvas",800,800)
canvas.Divide(2,2)

for icat in xrange(len(category)):
	print 'Drawing ', category[icat]
	canvas.cd(icat+1)

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
	hdata[category[icat]].SetMinimum(0.015)
	hdata[category[icat]].SetTitle("")
	hdata[category[icat]].GetYaxis().SetTitle("Events")
	formatUpperHist(hdata[category[icat]])

	uPad.cd()

	hdata[category[icat]].Draw("E1 X0")
	hs[category[icat]].Draw("SAME HIST")
	hdata[category[icat]].Draw("SAME E1 X0")

	uPad.RedrawAxis()

	leg[category[icat]] = TLegend(0.65,0.53,0.95,0.90)
	leg[category[icat]].SetShadowColor(0)
	leg[category[icat]].SetFillColor(0)
	leg[category[icat]].SetFillStyle(0)
	leg[category[icat]].SetLineColor(0)
	leg[category[icat]].SetLineStyle(0)
	leg[category[icat]].SetBorderSize(0) 
	leg[category[icat]].SetTextFont(42)
	leg[category[icat]].AddEntry(hdata[category[icat]],"DATA")
	
	try: leg[category[icat]].AddEntry(hewk[category[icat]],"VV & VVV","f")
	except: pass
	try: leg[category[icat]].AddEntry(htop[category[icat]],"TTV","f")
	except: pass
	try: leg[category[icat]].AddEntry(hddbkg[category[icat]],"DD BKG","f")
	except: pass
	#leg.AddEntry(bkgHTgerr,"Bkg uncert. (stat. #oplus syst.)","f")
	leg[category[icat]].Draw("SAME")

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
	if category[icat]=='EEE': chString+='eee'
	if category[icat]=='EEM': chString+='ee#mu'
	if category[icat]=='EMM': chString+='e#mu#mu'
	if category[icat]=='MMM': chString+='#mu#mu#mu'
	chLatex.DrawLatex(0.16, 0.82, chString)

	lPad.cd() #LOWER PAD
	
	#Setup data/mc ratio plot 
	pull[category[icat]]=hdata[category[icat]].Clone("pull")
# 	try: 
	pull[category[icat]].Divide(htotbkg[category[icat]])
# 	except: pass	
	
# 	try:
	if debug: print 'bin ','			hdata','				hbkg','			ratio','			','statErr','		','errPlus','		','errPlus'
	for ibin in range(0,hdata[category[icat]].GetNbinsX()+2):
		if debug: print ibin,'			',hdata[category[icat]].GetBinContent(ibin),'+-',round(hdata[category[icat]].GetBinError(ibin),2),'			',round(htotbkg[category[icat]].GetBinContent(ibin),2),

		#set up error bar on ratio plot (data uncertainty)
		dataStatErr= 0.
		if (htotbkg[category[icat]].GetBinContent(ibin))!=0:
			if debug: print '			',round(hdata[category[icat]].GetBinContent(ibin)/htotbkg[category[icat]].GetBinContent(ibin),2),
			dataStatErr = hdata[category[icat]].GetBinError(ibin)/(htotbkg[category[icat]].GetBinContent(ibin)) #is this right?
		else: 
			if debug: print '			',0.0,
		pull[category[icat]].SetBinError(ibin,dataStatErr) #is this right?

		### setup MC uncertainties	FOR PRINT only
		statErr = htotbkg[category[icat]].GetBinError(ibin)
		statErrLow = htotbkg[category[icat]].GetBinErrorLow(ibin)
		statErrUp = htotbkg[category[icat]].GetBinErrorUp(ibin)
		sysSqErrPlus = totBkgSqErr[category[icat]]['plus'][str(ibin)]
		sysSqErrMinus = totBkgSqErr[category[icat]]['minus'][str(ibin)]
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
	
	pull[category[icat]].SetMaximum(3)
	pull[category[icat]].SetMinimum(0)
	pull[category[icat]].SetFillColor(1)
	pull[category[icat]].SetMarkerStyle(7)
	pull[category[icat]].SetLineColor(1)
	formatLowerHist(pull[category[icat]])

	pull[category[icat]].Draw("SAME E0")

	### setup MC uncertainties for histogram

	BkgOverBkg = pull[category[icat]].Clone("bkgOverbkg")
# 	try: 
	BkgOverBkg.Divide(htotbkg[category[icat]], htotbkg[category[icat]])
# 	except: pass
	pullUncBandTot[category[icat]] = TGraphAsymmErrors(BkgOverBkg.Clone("pulluncTot"))
	htotbkgErr[category[icat]] = TGraphAsymmErrors(htotbkg[category[icat]].Clone("htotbkgErr"))

# 	try:
	for ibin in range(0,hdata[category[icat]].GetNbinsX()+2):
		statErr = htotbkg[category[icat]].GetBinError(ibin)
		statErrLow = htotbkg[category[icat]].GetBinErrorLow(ibin)
		statErrUp = htotbkg[category[icat]].GetBinErrorUp(ibin)

		sysSqErrPlus = totBkgSqErr[category[icat]]['plus'][str(ibin)]
		sysSqErrMinus = totBkgSqErr[category[icat]]['minus'][str(ibin)]
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

		htotbkgErr[category[icat]].SetPointEYhigh(ibin-1,totErrPlus)
		htotbkgErr[category[icat]].SetPointEYlow(ibin-1,totErrMinus)			
		if htotbkg[category[icat]].GetBinContent(ibin)!=0:
			pullUncBandTot[category[icat]].SetPointEYhigh(ibin-1,totErrPlus/htotbkg[category[icat]].GetBinContent(ibin))
			pullUncBandTot[category[icat]].SetPointEYlow(ibin-1,totErrMinus/htotbkg[category[icat]].GetBinContent(ibin))
		else:			
			pullUncBandTot[category[icat]].SetPointEYhigh(ibin-1,0.)
			pullUncBandTot[category[icat]].SetPointEYlow(ibin-1,0.)
# 	except: pass

	pullUncBandTot[category[icat]].SetFillStyle(3344)
	pullUncBandTot[category[icat]].SetFillColor(1)
	pullUncBandTot[category[icat]].SetLineColor(1)
	pullUncBandTot[category[icat]].SetMarkerSize(0)
	gStyle.SetHatchesLineWidth(1)
	pullUncBandTot[category[icat]].Draw("SAME E2")

	lPad.RedrawAxis()

	uPad.cd()
	htotbkgErr[category[icat]].SetFillStyle(3004)
	htotbkgErr[category[icat]].SetFillColor(kBlack)
	htotbkgErr[category[icat]].Draw("SAME E2")
	uPad.RedrawAxis()

if doJustStatUnc:
	canvas.SaveAs(mleFile+"_onlyStatUnc.png")
	canvas.SaveAs(mleFile+"_onlyStatUnc.pdf")

if doJustSysUnc:
	canvas.SaveAs(mleFile+"_onlySysUnc.png")
	canvas.SaveAs(mleFile+"_onlySysUnc.pdf")

if doAllUnc:
	canvas.SaveAs(mleFile+".png")
	canvas.SaveAs(mleFile+".pdf")

