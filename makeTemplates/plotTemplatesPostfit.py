#!/usr/bin/python

import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
#from weights import *
from modSyst import *
from utils import *
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)
start_time = time.time()

year=sys.argv[1]
if year=='R16':
	from weights16 import *
	lumi=35.9 #for plots
elif year=='R17':
	from weights17 import *
	lumi=41.5 #for plots
elif year=='R18':
	from weights18 import *
	lumi=59.97 #for plots
lumiInTemplates= str(targetlumi/1000).replace('.','p') # 1/fb
	
region='SR' #PS,SR,TTCR,WJCR
iPlot=sys.argv[2]
# if len(sys.argv)>1: iPlot=str(sys.argv[1])
cutString=''
if region=='SR': pfix='templates_'+year
templateDir=os.getcwd()+'/'+pfix+'_'+sys.argv[3]+'/'+cutString+'/'

fit = 'postfit'
comboFit = True
isRebinned='_2b300GeV3b150GeV4b50GeVbins_rebinned_stat0p3' #post for ROOT file names
saveKey = '_Run2fit' # tag for plot names

sig='tttt' #  choose the 1st signal to plot
sigleg='t#bar{t}t#bar{t}'
scaleSignalsToXsec = False # !!!!!Make sure you know signal x-sec used in input files to this script. If this is True, it will scale signal histograms by x-sec in weights.py!!!!!
scaleSignals = False
sigScaleFact = 10 #put -1 if auto-scaling wanted
sigfile='../../combineLimits/limits_'+year+'_2021_4_6_2b300GeV3b150GeV4b50GeVbins_HT/postfit/postfit_shapes.root'
sigfile='../../combineLimits/HTcomb/2021_4_6_2b300GeV3b150GeV4b50GeVbins_HT_R16p17p18_postfit/postfit_shapes.root'
 
ttProcList = ['ttnobb','ttbb'] # ['ttjj','ttcc','ttbb','ttbj']
bkgProcList = ttProcList+['ttH','top','ewk','qcd']
if '53' in sig: bkgHistColors = {'tt2b':rt.kRed+3,'tt1b':rt.kRed-3,'ttbj':rt.kRed+3,'ttbb':rt.kRed,'ttcc':rt.kRed-5,'ttjj':rt.kRed-7,'ttnobb':rt.kRed-7,'top':rt.kBlue,'ewk':rt.kMagenta-2,'qcd':rt.kOrange+5,'ttbar':rt.kRed} #4T
elif 'tttt' in sig: 
	#bkgHistColors = {'tt2b':rt.kRed+3,'tt1b':rt.kRed-3,'ttbj':rt.kRed+3,'ttbb':rt.kRed,'ttcc':rt.kRed-5,'ttjj':rt.kRed-7,'ttnobb':rt.kRed-9,'top':rt.kBlue,'ttH':rt.kRed+3,'ewk':rt.kMagenta-2,'qcd':rt.kOrange+5,'ttbar':rt.kRed} #4T
	bkgHistColors = {'ttbb':rt.TColor.GetColor("#d3eeef"),'ttnobb':rt.TColor.GetColor("#cf9ddb"),'ttH':rt.TColor.GetColor("#163d4e"),'top':rt.TColor.GetColor("#54792f"),'ewk':rt.TColor.GetColor("#d07e93"),'qcd':rt.TColor.GetColor("#c1caf3")} #4T
elif 'HTB' in sig: bkgHistColors = {'ttbar':rt.kGreen-3,'wjets':rt.kPink-4,'top':rt.kAzure+8,'ewk':rt.kMagenta-2,'qcd':rt.kOrange+5} #HTB
else: bkgHistColors = {'top':rt.kAzure+8,'ewk':rt.kMagenta-2,'qcd':rt.kOrange+5} #TT

doNormByBinWidth=True
blind = False
yLog  = True
doRealPull = True
compareShapes = False
if compareShapes: blind,yLog,scaleSignals,sigScaleFact=True,False,False,-1
drawYields = False
zero = 1E-12

isEMlist  = ['E','M']
if 'rebinned' not in isRebinned or 'stat1p1' in isRebinned: doNormByBinWidth = False

sigName = sig
dataName = 'data_obs'
upTag = 'Up'
downTag = 'Down'
sigfile = sigfile.replace(sig+'_','')
if not os.path.exists(templateDir+sigfile):
	print "ERROR: File does not exits: "+templateDir+sigfile
	os._exit(1)
print "READING: "+templateDir+sigfile
RFile = rt.TFile(templateDir+sigfile)

datahists = [k.GetName() for k in RFile.GetListOfKeys() if '_'+fit in k.GetName() and '_'+year in k.GetName()]
catsElist = [hist[hist.find(sig+'_')+5:hist.find('_0_')] for hist in datahists if 'isE_' in hist]

def formatUpperHist(histogram,histogramBkg):
	histogram.GetXaxis().SetLabelSize(0)
	histogram.GetXaxis().SetNdivisions(506)

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

	histogram.GetYaxis().CenterTitle()
	histogram.SetMinimum(0.0000101)
	if not yLog: 
		histogram.SetMinimum(0.015)
	if yLog:
		uPad.SetLogy()
		histogram.SetMaximum(2e2*histogramBkg.GetMaximum())
	else: 
		histogram.SetMaximum(1.3*histogramBkg.GetMaximum())
		
def formatLowerHist(histogram,disc):
	histogram.GetXaxis().SetLabelSize(0.12)
	histogram.GetXaxis().SetTitleSize(0.15)
	histogram.GetXaxis().SetTitleOffset(0.95)
	histogram.GetXaxis().SetNdivisions(506)

	histogram.GetXaxis().SetNdivisions(506)

	histogram.GetYaxis().SetLabelSize(0.12)
	histogram.GetYaxis().SetTitleSize(0.14)
	histogram.GetYaxis().SetTitleOffset(.37)
	histogram.GetYaxis().SetTitle('Data/Bkg')
	histogram.GetYaxis().SetNdivisions(506)
	if doRealPull: histogram.GetYaxis().SetRangeUser(min(-2.99,0.8*histogram.GetBinContent(histogram.GetMaximumBin())),max(2.99,1.2*histogram.GetBinContent(histogram.GetMaximumBin())))
	#else: histogram.GetYaxis().SetRangeUser(0.45,1.55)#0,2.99)
	else: histogram.GetYaxis().SetRangeUser(0.01,1.99)#0,2.99)
	histogram.GetYaxis().CenterTitle()

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= str(lumi)+" fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H = H_ref

iPeriod = 4 #see CMS_lumi.py module for usage!

# references for T, B, L, R
T = 0.10*H_ref
B = 0.35*H_ref
L = 0.12*W_ref
R = 0.04*W_ref
if blind == True: B = 0.12*H_ref

tagPosX = 0.76
tagPosY = 0.62
if not blind: tagPosY-=0.13

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
for catEStr in catsElist:
	for isEM in isEMlist:
		histPrefix=sig+'_'
		if comboFit: histPrefix=year+'_'+sig+'_'
		catStr=catEStr.replace('isE','is'+isEM)
		histPrefix+=catStr+'_0_'+year+'_'+fit
		print histPrefix
		totBkg = 0.
		for proc in bkgProcList: 
			try:
				bkghists[proc+catStr] = RFile.Get(histPrefix+'/'+proc).Clone()
				totBkg += bkghists[proc+catStr].Integral()
			except:
				print "There is no "+proc+"!!! Skipping it....."
				pass
		hData = RFile.Get(histPrefix+'/'+dataName).Clone()
		hData_test = RFile.Get(histPrefix+'/'+dataName).Clone()
		bkgHT_test = bkghists[bkgProcList[0]+catStr].Clone()
		for proc in bkgProcList:
			if proc==bkgProcList[0]: continue
			try: bkgHT_test.Add(bkghists[proc+catStr])
			except: pass
		print hData_test.Integral(),bkgHT_test.Integral()
		hsig = RFile.Get(histPrefix+'/'+sigName).Clone(histPrefix+'__'+sigName)
		if scaleSignalsToXsec: hsig.Scale(xsec[sig])
		if doNormByBinWidth:
			for proc in bkgProcList:
				try: normByBinWidth(bkghists[proc+catStr])
				except: pass
			normByBinWidth(hsig)
			normByBinWidth(hData)

		bkgHT = bkghists[bkgProcList[0]+catStr].Clone()
		for proc in bkgProcList:
			if proc==bkgProcList[0]: continue
			try: bkgHT.Add(bkghists[proc+catStr])
			except: pass

		TotalBkg_ = RFile.Get(histPrefix+'/TotalBkg').Clone()
		if doNormByBinWidth: normByBinWidth(TotalBkg_)
		totBkgTemp3[catStr] = rt.TGraphAsymmErrors(TotalBkg_.Clone(histPrefix+'__TotalBkgAll'))
			
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

		if scaleSignals:
			scaleFact = int(bkgHT.GetMaximum()/(hsig.GetMaximum()+zero)) - int(bkgHT.GetMaximum()/(hsig.GetMaximum()+zero)) % 10
			if scaleFact==0: scaleFact=int(bkgHT.GetMaximum()/(hsig.GetMaximum()+zero))
			if scaleFact==0: scaleFact=1
			if sigScaleFact>0: scaleFact=sigScaleFact
		else: scaleFact=1
		hsig.Scale(scaleFact)

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
			try: 
				if drawQCD or proc!='qcd': stackbkgHT.Add(bkghists[proc+catStr])
			except: pass

		sigColor= rt.kBlack
			
		for proc in bkgProcList:
			try: 
				bkghists[proc+catStr].SetLineColor(bkgHistColors[proc])
				bkghists[proc+catStr].SetFillColor(bkgHistColors[proc])
				bkghists[proc+catStr].SetLineWidth(2)
			except: pass
		if drawYields: 
			bkgHT.SetMarkerSize(4)
			bkgHT.SetMarkerColor(rt.kRed)

		hsig.SetLineColor(sigColor)
		hsig.SetLineStyle(7)#5)
		hsig.SetFillStyle(0)
		hsig.SetLineWidth(3)
		
		if not drawYields: hData.SetMarkerStyle(20)
		hData.SetMarkerSize(1.2)
		hData.SetMarkerColor(rt.kBlack)
		hData.SetLineWidth(2)
		hData.SetLineColor(rt.kBlack)
		if drawYields: hData.SetMarkerSize(4)

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
			lPad.SetTopMargin( 0.01 )
			lPad.SetBottomMargin( B/H )

			lPad.SetGridy()
			lPad.SetFillColor(0)
			lPad.SetBorderMode(0)
			lPad.SetFrameFillStyle(0)
			lPad.SetFrameBorderMode(0)
			#lPad.SetTickx(0)
			#lPad.SetTicky(0)
			lPad.Draw()
		if not doNormByBinWidth: hData.SetMaximum(1.2*max(hData.GetMaximum(),bkgHT.GetMaximum()))
		#hData.SetMinimum(0.015)
		hData.SetTitle("")
		if doNormByBinWidth: hData.GetYaxis().SetTitle("< Events / GeV >")
		elif isRebinned!='': hData.GetYaxis().SetTitle("Events / bin")
		else: hData.GetYaxis().SetTitle("Events / bin")
		formatUpperHist(hData,hData)
		uPad.cd()
		hData.SetTitle("")
		if compareShapes: hsig.Scale(totBkg/hsig.Integral())
		if not blind: 
			if 'rebinned_stat0p' in isRebinned: hData.Draw("esamex1")
			else: hData.Draw("esamex0")
		if blind: 
			#hsig.SetMinimum(0.015)
			if doNormByBinWidth: hsig.GetYaxis().SetTitle("< Events / GeV >")
			elif isRebinned!='': hsig.GetYaxis().SetTitle("Events / bin")
			else: hsig.GetYaxis().SetTitle("Events / bin")
			if doNormByBinWidth: normByBinWidth(bkgHT_test)
			formatUpperHist(hsig,bkgHT_test)
			hsig.Draw("HIST")
		stackbkgHT.Draw("SAME HIST")
		if drawYields: 
			rt.gStyle.SetPaintTextFormat("1.0f")
			bkgHT.Draw("SAME TEXT90")
		hsig.Draw("SAME HIST")
		if not blind: 
			if 'rebinned_stat0p' in isRebinned: hData.Draw("esamex1")
			else: hData.Draw("esamex0") #redraw data so its not hidden
			if drawYields: hData.Draw("SAME TEXT00") 
		uPad.RedrawAxis()
		bkgHTgerr.Draw("SAME E2")
		
		chLatex = rt.TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.06)
		if blind: chLatex.SetTextSize(0.04)
		chLatex.SetTextAlign(21) # align center
		tagString = ''
		tagString2 = ''
		flvString='e+jets'
		if isEM=='M': flvString='#mu+jets'
		nJ = catStr.split('_')[-1].replace('nJ','')
		nB = catStr.split('_')[-2].replace('nB','')
		nW = catStr.split('_')[-3].replace('nW','')
		nT = catStr.split('_')[-4].replace('nT','')
		nHOT = catStr.split('_')[-5].replace('nHOT','')
		if nHOT!='0p': 
			if 'p' in nHOT: tagString2+='#geq'+nHOT[:-1]+' resolved t'
			else: tagString2+=nHOT+' resolved t'
		if nT!='0p': 
			if 'p' in nT: tagString+='#geq'+nT[:-1]+' t, '
			else: tagString+=nT+' t, '
		if nW!='0p': 
			if 'p' in nW: tagString+='#geq'+nW[:-1]+' W, '
			else: tagString+=nW+' W, '
		if nB!='0p': 
			if 'p' in nB: tagString+='#geq'+nB[:-1]+' b, '
			else: tagString+=nB+' b, '
		if nJ!='0p': 
			if 'p' in nJ: tagString+='#geq'+nJ[:-1]+' j'
			else: tagString+=nJ+' j'
		if tagString.endswith(', '): tagString = tagString[:-2]
		chLatex.DrawLatex(tagPosX, tagPosY, flvString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)

		leg = rt.TLegend(0.45,0.52,0.95,0.87)
		if blind: leg = rt.TLegend(0.45,0.64,0.95,0.89)
		leg.SetShadowColor(0)
		leg.SetFillColor(0)
		leg.SetFillStyle(0)
		leg.SetLineColor(0)
		leg.SetLineStyle(0)
		leg.SetBorderSize(0) 
		leg.SetNColumns(2)
		leg.SetTextFont(62)#42)
		scaleFactStr = ' x'+str(scaleFact)
		if not scaleSignals: scaleFactStr = ''
		if not blind: leg.AddEntry(hData,"Data","ep")
		if drawQCD: leg.AddEntry(bkghists['qcd'+catStr],"QCD","f")
		try: leg.AddEntry(bkghists['ewk'+catStr],"EWK","f")
		except: pass
		try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
		except: pass
		try: leg.AddEntry(bkghists['ttH'+catStr],"t#bar{t}+H","f")
		except: pass
		try: leg.AddEntry(bkghists['ttnobb'+catStr],"t#bar{t}+!b#bar{b}","f")
		except: pass
		try: leg.AddEntry(bkghists['ttjj'+catStr],"t#bar{t}+j(j)","f")
		except: pass
		try: leg.AddEntry(bkghists['ttcc'+catStr],"t#bar{t}+c(c)","f")
		except: pass
		if 'tt2b' not in bkgProcList and 'ttnobb' not in bkgProcList:
			try: leg.AddEntry(bkghists['ttbb'+catStr],"t#bar{t}+b(b)","f")
			except: pass
		else:
			try: leg.AddEntry(bkghists['ttbb'+catStr],"t#bar{t}+b#bar{b}","f")
			except: pass
		try: leg.AddEntry(bkghists['tt1b'+catStr],"t#bar{t}+b","f")
		except: pass
		try: leg.AddEntry(bkghists['tt2b'+catStr],"t#bar{t}+2B","f")
		except: pass
		leg.AddEntry(hsig,sigleg+scaleFactStr,"l")
		leg.AddEntry(bkgHTgerr,"Bkg uncert","f")
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
			for binNo in range(1,hData.GetNbinsX()+1):
				binLbl = binNo-1
				if 'NJets' in iPlot: 
					#if binNo == 1 or binNo == 5 or binNo == 10 or binNo == 15: pull.GetXaxis().SetBinLabel(binNo,str(binNo))
					if binLbl%2 == 0: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
					else: pull.GetXaxis().SetBinLabel(binNo,'')
				if 'NTJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if 'NWJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if 'NBJets' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if 'NresolvedTops' in iPlot: pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if bkgHT.GetBinContent(binNo)!=0:
					pull.SetBinError(binNo,hData.GetBinError(binNo)/bkgHT.GetBinContent(binNo))
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
			pullUncBandTot.SetFillStyle(3013)
			pullUncBandTot.SetFillColor(1)
			pullUncBandTot.SetLineColor(1)
			pullUncBandTot.SetMarkerSize(0)
			rt.gStyle.SetHatchesLineWidth(1)
			pullUncBandTot.Draw("SAME E2")

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
			pullLegend.AddEntry(pullUncBandTot , "Bkg uncert" , "f")
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
				if 'NDCSVBJets' in iPlot or 'NresolvedTops' in iPlot or 'NBJets' in iPlot or 'NWJets' in iPlot or 'NTJets' in iPlot: 
					pull.GetXaxis().SetBinLabel(binNo,str(binLbl))
				if hData.GetBinContent(binNo)!=0:
					MCerror = 0.5*(totBkgTemp3[catStr].GetErrorYhigh(binNo-1)+totBkgTemp3[catStr].GetErrorYlow(binNo-1))
					pull.SetBinContent(binNo,(hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(MCerror**2+hData.GetBinError(binNo)**2))
				else: pull.SetBinContent(binNo,0.)
			pull.SetMaximum(3)
			pull.SetMinimum(-3)
			if '53' in sig or 'tttt' in sig:
				pull.SetFillColor(2)
				pull.SetLineColor(2)
			else:
				pull.SetFillColor(rt.kGray+2)
				pull.SetLineColor(rt.kGray+2)
			formatLowerHist(pull,iPlot)
			pull.GetYaxis().SetTitle('#frac{(obs-bkg)}{uncertainty}')
			pull.Draw("HIST")

		#c1.Write()
		savePrefix = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
		if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix.replace('tttt_',iPlot+'_'+lumiInTemplates+'fb_').replace('_0_'+year,'')+isRebinned+saveKey
		savePrefix=savePrefix.replace('nHOT0p_','').replace('nT0p_','').replace('nW0p_','').replace('nB0p_','').replace('nJ0p_','').replace('_rebinned_stat1p1','')
		if doRealPull: savePrefix+='_pull'
		if doNormByBinWidth: savePrefix+='_NBBW'
		if yLog: savePrefix+='_logy'
		if blind: savePrefix+='_blind'
		if compareShapes: savePrefix+='_shp'

		c1.SaveAs(savePrefix+'.png')
		c1.SaveAs(savePrefix+'.pdf')
# 		c1.SaveAs(savePrefix+'.eps')
# 		c1.SaveAs(savePrefix+'.root')
# 		c1.SaveAs(savePrefix+'.C')

		for proc in bkgProcList:
			try: del bkghists[proc+catStr]
			except: pass
					
	# Making plots for e+jets/mu+jets combined #
	histPrefixE = sig+'_'+catEStr+'_0_'+year+'_'+fit
	histPrefixM = sig+'_'+catEStr.replace('isE','isM')+'_0_'+year+'_'+fit
	if comboFit: 
		histPrefixE = year+'_'+sig+'_'+catEStr+'_0_'+year+'_'+fit
		histPrefixM = year+'_'+sig+'_'+catEStr.replace('isE','isM')+'_0_'+year+'_'+fit
	catLStr = catEStr.replace('isE','isL')
	totBkgMerged = 0.
	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+catLStr] = RFile.Get(histPrefixE+'/'+proc).Clone()
			bkghistsmerged[proc+catLStr].Add(RFile.Get(histPrefixM+'/'+proc))
			totBkgMerged += bkghistsmerged[proc+catLStr].Integral()
		except:pass
	hDatamerged = RFile.Get(histPrefixE+'/'+dataName).Clone()
	hDatamerged.Add(RFile.Get(histPrefixM+'/'+dataName).Clone())
	hDatamerged_test = RFile.Get(histPrefixE+'/'+dataName).Clone()
	hDatamerged_test.Add(RFile.Get(histPrefixM+'/'+dataName).Clone())
	bkgHTmerged_test = bkghistsmerged[bkgProcList[0]+catLStr].Clone()
	for proc in bkgProcList[1:]:
		try: bkgHTmerged_test.Add(bkghistsmerged[proc+catLStr])
		except: pass
	hsigmerged = RFile.Get(histPrefixE+'/'+sigName).Clone(histPrefixE+'__'+sigName+'merged')
	hsigmerged.Add(RFile.Get(histPrefixM+'/'+sigName).Clone())
	if scaleSignalsToXsec: hsigmerged.Scale(xsec[sig])
	if doNormByBinWidth:
		for proc in bkgProcList:
			try: normByBinWidth(bkghistsmerged[proc+catLStr])
			except: pass
		normByBinWidth(hsigmerged)
		normByBinWidth(hDatamerged)

	bkgHTmerged = bkghistsmerged[bkgProcList[0]+catLStr].Clone()
	for proc in bkgProcList:
		if proc==bkgProcList[0]: continue
		try: bkgHTmerged.Add(bkghistsmerged[proc+catLStr])
		except: pass

	#totBkgTemp3[catLStr] = rt.TGraphAsymmErrors(bkgHTmerged.Clone(bkgHTmerged.GetName()+'All'))
	TotalBkgmerged_ = RFile.Get(histPrefixE+'/TotalBkg').Clone()
	TotalBkgmerged_.Add(RFile.Get(histPrefixM+'/TotalBkg').Clone())
	if doNormByBinWidth: normByBinWidth(TotalBkgmerged_)
	totBkgTemp3[catLStr] = rt.TGraphAsymmErrors(TotalBkgmerged_.Clone(histPrefixE+'__TotalBkgAllmerged'))
	
# 	for ibin in range(1,bkghistsmerged[bkgProcList[0]+catLStr].GetNbinsX()+1):
# 		errorUp = systHists[proc+catLStr+syst+upTag].GetBinContent(ibin)
# 		errorDn = systHists[proc+catLStr+syst+upTag].GetBinContent(ibin)
# 		totBkgTemp3[catLStr].SetPointEYhigh(ibin-1,errorUp)
# 		totBkgTemp3[catLStr].SetPointEYlow(ibin-1, errorDn)

	for ibin in range(1, bkgHTmerged_test.GetNbinsX()+1):
		bkgHTmerged_test.SetBinError(ibin,(totBkgTemp3[catLStr].GetErrorYlow(ibin-1) + totBkgTemp3[catLStr].GetErrorYhigh(ibin-1))/2 )
	
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
	table.append([catLStr,prob_KS,prob_KS_X,prob_chi2,chi2,ndof])

	bkgHTgerrmerged = totBkgTemp3[catLStr].Clone()

	if scaleSignals:
		scaleFactmerged = int(bkgHTmerged.GetMaximum()/hsigmerged.GetMaximum()) - int(bkgHTmerged.GetMaximum()/hsigmerged.GetMaximum()) % 10
		if scaleFactmerged==0: scaleFactmerged=int(bkgHTmerged.GetMaximum()/hsigmerged.GetMaximum())
		if scaleFactmerged==0: scaleFactmerged=1
		if sigScaleFact>0: scaleFactmerged=sigScaleFact
	else: scaleFactmerged=1
	hsigmerged.Scale(scaleFactmerged)
	
	drawQCDmerged = False
	try: drawQCDmerged = bkghistsmerged['qcd'+catLStr].Integral()/bkgHTmerged.Integral()>.005
	except: pass

	stackbkgHTmerged = rt.THStack("stackbkgHTmerged","")
	bkgProcListNew = bkgProcList[:]
	if region=='WJCR':
		bkgProcListNew[bkgProcList.index("top")],bkgProcListNew[bkgProcList.index("ewk")]=bkgProcList[bkgProcList.index("ewk")],bkgProcList[bkgProcList.index("top")]
	for proc in bkgProcListNew:
		try: 
			if drawQCDmerged or proc!='qcd': stackbkgHTmerged.Add(bkghistsmerged[proc+catLStr])
		except: pass

	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+catLStr].SetLineColor(bkgHistColors[proc])
			bkghistsmerged[proc+catLStr].SetFillColor(bkgHistColors[proc])
			bkghistsmerged[proc+catLStr].SetLineWidth(2)
		except: pass
	if drawYields: 
		bkgHTmerged.SetMarkerSize(4)
		bkgHTmerged.SetMarkerColor(rt.kRed)
	
	hsigmerged.SetLineColor(sigColor)
	hsigmerged.SetLineStyle(7)#5)
	hsigmerged.SetFillStyle(0)
	hsigmerged.SetLineWidth(3)
	
	if not drawYields: hDatamerged.SetMarkerStyle(20)
	hDatamerged.SetMarkerSize(1.2)
	hDatamerged.SetMarkerColor(rt.kBlack)
	hDatamerged.SetLineWidth(2)
	hDatamerged.SetLineColor(rt.kBlack)
	if drawYields: hDatamerged.SetMarkerSize(4)

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
		lPad.SetTopMargin( 0.01 )
		lPad.SetBottomMargin( B/H )

		lPad.SetGridy()
		lPad.SetFillColor(0)
		lPad.SetBorderMode(0)
		lPad.SetFrameFillStyle(0)
		lPad.SetFrameBorderMode(0)
		#lPad.SetTickx(0)
		#lPad.SetTicky(0)
		lPad.Draw()
	if not doNormByBinWidth: hDatamerged.SetMaximum(1.2*max(hDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
	#hDatamerged.SetMinimum(0.015)
	if doNormByBinWidth: hDatamerged.GetYaxis().SetTitle("< Events / GeV >")
	elif isRebinned!='': hDatamerged.GetYaxis().SetTitle("Events / bin")
	else: hDatamerged.GetYaxis().SetTitle("Events / bin")
	formatUpperHist(hDatamerged,hDatamerged)
	uPad.cd()
	hDatamerged.SetTitle("")
	stackbkgHTmerged.SetTitle("")
	if compareShapes: hsigmerged.Scale(totBkgMerged/hsigmerged.Integral())
	if not blind: 
		if 'rebinned_stat0p' in isRebinned: hDatamerged.Draw("esamex1")
		else: hDatamerged.Draw("esamex0")
	if blind: 
		#hsigmerged.SetMinimum(0.015)
		if doNormByBinWidth: hsigmerged.GetYaxis().SetTitle("< Events / GeV >")
		elif isRebinned!='': hsigmerged.GetYaxis().SetTitle("Events / bin")
		else: hsigmerged.GetYaxis().SetTitle("Events / bin")
		if doNormByBinWidth: normByBinWidth(bkgHTmerged_test)
		formatUpperHist(hsigmerged,bkgHTmerged_test)
		#hsigmerged.SetMaximum(bkgHTmerged_test.GetMaximum())
		hsigmerged.Draw("HIST")
	stackbkgHTmerged.Draw("SAME HIST")
	if drawYields: 
		rt.gStyle.SetPaintTextFormat("1.0f")
		bkgHTmerged.Draw("SAME TEXT90")
	hsigmerged.Draw("SAME HIST")
	if not blind: 
		if 'rebinned_stat0p' in isRebinned: hDatamerged.Draw("esamex1")
		else: hDatamerged.Draw("esamex0") #redraw data so its not hidden
		if drawYields: hDatamerged.Draw("SAME TEXT00") 
	uPad.RedrawAxis()
	bkgHTgerrmerged.Draw("SAME E2")

	chLatexmerged = rt.TLatex()
	chLatexmerged.SetNDC()
	chLatexmerged.SetTextSize(0.06)
	if blind: chLatexmerged.SetTextSize(0.04)
	chLatexmerged.SetTextAlign(21) # align center
	flvString = 'e/#mu+jets'
	chLatexmerged.DrawLatex(tagPosX, tagPosY, flvString)
	chLatexmerged.DrawLatex(tagPosX, tagPosY-0.06, tagString)
	chLatexmerged.DrawLatex(tagPosX, tagPosY-0.12, tagString2)

	legmerged = rt.TLegend(0.45,0.52,0.95,0.87)
	if blind: legmerged = rt.TLegend(0.45,0.64,0.95,0.89)
	#if 'Tau32' in iPlot: legmerged = rt.TLegend(0.3,0.52,0.8,0.87)
	legmerged.SetShadowColor(0)
	legmerged.SetFillColor(0)
	legmerged.SetFillStyle(0)
	legmerged.SetLineColor(0)
	legmerged.SetLineStyle(0)
	legmerged.SetBorderSize(0) 
	legmerged.SetNColumns(2)
	legmerged.SetTextFont(62)#42)
	scaleFactStr = ' x'+str(scaleFact)
	if not scaleSignals: scaleFactStr = ''
	if not blind: legmerged.AddEntry(hDatamerged,"Data","ep")
	if drawQCDmerged: legmerged.AddEntry(bkghistsmerged['qcd'+catLStr],"QCD","f")
	try: legmerged.AddEntry(bkghistsmerged['ewk'+catLStr],"EWK","f")
	except: pass
	try: legmerged.AddEntry(bkghistsmerged['top'+catLStr],"TOP","f")
	except: pass
	try: legmerged.AddEntry(bkghistsmerged['ttH'+catLStr],"t#bar{t}+H","f")
	except: pass
	try: legmerged.AddEntry(bkghistsmerged['ttnobb'+catLStr],"t#bar{t}+!b#bar{b}","f")
	except: pass
	try: legmerged.AddEntry(bkghistsmerged['ttjj'+catLStr],"t#bar{t}+j(j)","f")
	except: pass
	try: legmerged.AddEntry(bkghistsmerged['ttcc'+catLStr],"t#bar{t}+c(c)","f")
	except: pass
	if 'tt2b' not in bkgProcList and 'ttnobb' not in bkgProcList:
		try: legmerged.AddEntry(bkghistsmerged['ttbb'+catLStr],"t#bar{t}+b(b)","f")
		except: pass
	else:
		try: legmerged.AddEntry(bkghistsmerged['ttbb'+catLStr],"t#bar{t}+b#bar{b}","f")
		except: pass
	try: legmerged.AddEntry(bkghistsmerged['tt1b'+catLStr],"t#bar{t}+b","f")
	except: pass
	try: legmerged.AddEntry(bkghistsmerged['tt2b'+catLStr],"t#bar{t}+2B","f")
	except: pass
	legmerged.AddEntry(hsigmerged,sigleg+scaleFactStr,"l")
	legmerged.AddEntry(bkgHTgerrmerged,"Bkg uncert","f")
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
		for binNo in range(1,hDatamerged.GetNbinsX()+1):
			binLbl = binNo-1
			if 'NJets' in iPlot: 
				#if binNo == 1 or binNo == 5 or binNo == 10 or binNo == 15: pullmerged.GetXaxis().SetBinLabel(binNo,str(binNo))
				if binLbl%2 == 0: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
				else: pullmerged.GetXaxis().SetBinLabel(binNo,'')
			if 'NDCSVBJets' in iPlot or 'NresolvedTops' in iPlot or 'NBJets' in iPlot or 'NWJets' in iPlot or 'NTJets' in iPlot: 
				pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if bkgHTmerged.GetBinContent(binNo)!=0:
				pull.SetBinError(binNo,hDatamerged.GetBinError(binNo)/bkgHTmerged.GetBinContent(binNo))
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
				pullUncBandTotmerged.SetPointEYhigh(binNo-1,totBkgTemp3[catLStr].GetErrorYhigh(binNo-1)/bkgHTmerged.GetBinContent(binNo))
				pullUncBandTotmerged.SetPointEYlow(binNo-1, totBkgTemp3[catLStr].GetErrorYlow(binNo-1)/bkgHTmerged.GetBinContent(binNo))			
		pullUncBandTotmerged.SetFillStyle(3013)
		pullUncBandTotmerged.SetFillColor(1)
		pullUncBandTotmerged.SetLineColor(1)
		pullUncBandTotmerged.SetMarkerSize(0)
		rt.gStyle.SetHatchesLineWidth(1)
		pullUncBandTotmerged.Draw("SAME E2")

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
		pullLegendmerged.AddEntry(pullUncBandTotmerged , "Bkg uncert" , "f")
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
			if 'NresolvedTops' in iPlot: pullmerged.GetXaxis().SetBinLabel(binNo,str(binLbl))
			if hDatamerged.GetBinContent(binNo)!=0:
				MCerror = 0.5*(totBkgTemp3[catLStr].GetErrorYhigh(binNo-1)+totBkgTemp3[catLStr].GetErrorYlow(binNo-1))
				pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(MCerror**2+hDatamerged.GetBinError(binNo)**2))
			else: pullmerged.SetBinContent(binNo,0.)
		pullmerged.SetMaximum(3)
		pullmerged.SetMinimum(-3)
		if '53' in sig or 'tttt' in sig:
			pullmerged.SetFillColor(2)
			pullmerged.SetLineColor(2)
		else:
			pullmerged.SetFillColor(rt.kGray+2)
			pullmerged.SetLineColor(rt.kGray+2)
		formatLowerHist(pullmerged,iPlot)
		pullmerged.GetYaxis().SetTitle('#frac{(obs-bkg)}{uncertainty}')
		pullmerged.Draw("HIST")

		lPad.Update()
		lPad.RedrawAxis()
		frame = lPad.GetFrame()
		lPad.Draw()

	#c1merged.Write()
	savePrefixmerged = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('isE','isL').replace('tttt_',iPlot+'_'+lumiInTemplates+'fb_').replace('_0_'+year,'')+isRebinned+saveKey
	savePrefixmerged=savePrefixmerged.replace('nHOT0p_','').replace('nT0p_','').replace('nW0p_','').replace('nB0p_','').replace('nJ0p_','').replace('_rebinned_stat1p1','')
	if doRealPull: savePrefixmerged+='_pull'
	if doNormByBinWidth: savePrefixmerged+='_NBBW'
	if yLog: savePrefixmerged+='_logy'
	if blind: savePrefixmerged+='_blind'
	if compareShapes: savePrefixmerged+='_shp'

	c1merged.SaveAs(savePrefixmerged+'.png')
	c1merged.SaveAs(savePrefixmerged+'.pdf')
# 	c1merged.SaveAs(savePrefixmerged+'.eps')
# 	c1merged.SaveAs(savePrefixmerged+'.root')
# 	c1merged.SaveAs(savePrefixmerged+'.C')
	
	for proc in bkgProcList:
		try: del bkghistsmerged[proc+catLStr]
		except: pass

if not doNormByBinWidth: 
	out=open(templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'+sigfile.replace('templates','GOFtests').replace('.root','').replace(sig+'_','')+saveKey+'.txt','w')
	printTable(table,out)
			
RFile.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


