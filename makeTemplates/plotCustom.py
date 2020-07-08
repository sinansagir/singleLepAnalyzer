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

year=2018
if year==2017:
	from weights17 import *
	lumi=41.5 #for plots
else:
	from weights18 import *
	lumi=59.97 #for plots
lumiInTemplates= str(targetlumi/1000).replace('.','p') # 1/fb

iPlot='YLD'
cutString=''#'lep50_MET30_DR0_1jet50_2jet40'
pfix='templates'
templateDir=os.getcwd()+'/'+pfix+'_R'+str(year)+'_Xtrig_2020_4_25/'+cutString+'/'
plotLimits = False
limitFile = '/user_data/ssagir/HTB_limits_2016/templates_2016_11_26/nB1_nJ3/limits_templates_HT_HTBM200_36p0fb_rebinned_stat0p3_expected.txt'

isRebinned = ''#'_rebinned_stat0p3'
saveKey = '' # tag for plot names

mass = '690'
sig1 = 'TTTTM690' # choose the 1st signal to plot
sig1leg='t#bar{t}t#bar{t}'
tempsig='templates_'+iPlot+'_'+sig1+'_'+lumiInTemplates+'fb'+isRebinned+'.root'

bkgProcList = ['ttbj','ttbb','ttcc','ttjj','top','ewk','qcd']
bkgHistColors = {'tt2b':rt.kRed+3,'tt1b':rt.kRed-3,'ttbj':rt.kRed+3,'ttbb':rt.kRed,'ttcc':rt.kRed-5,'ttjj':rt.kRed-7,'top':rt.kBlue,'ewk':rt.kMagenta-2,'qcd':rt.kOrange+5,'ttbar':rt.kRed} #4T

yLog = True
plotProc = 'bkg'#sig,bkg,SoB,'ttbar','wjets','top','ewk','qcd'
if len(sys.argv)>1: plotProc=str(sys.argv[1])
doBkgFraction = True #set plotProc to "bkg"
doNegSigFrac = False
doEfficiency = False
scaleXsec = False
if plotProc=='SoB' or doBkgFraction: yLog = False
zero = 1E-12

isEMlist  = ['E','M']
nhottlist = ['0p']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['0p']
njetslist = ['0p']
tagList = list(itertools.product(nhottlist,nttaglist,nWtaglist,nbtaglist,njetslist))

def formatUpperHist(histogram):
	histogram.GetXaxis().SetLabelSize(0)

	histogram.GetXaxis().SetLabelSize(0.045)
	histogram.GetXaxis().SetTitleSize(0.055)
	histogram.GetYaxis().SetLabelSize(0.045)
	histogram.GetYaxis().SetTitleSize(0.055)
	histogram.GetYaxis().SetTitleOffset(0.75)
	histogram.GetXaxis().SetNdivisions(506)
	histogram.GetXaxis().LabelsOption("v")
	histogram.GetYaxis().CenterTitle()
	if yLog: 
		uPad.SetLogy()
		#histogram.SetMinimum(0.101)

RFile = rt.TFile(templateDir+tempsig)
if doNegSigFrac: RFile2 = rt.TFile(templateDir.replace('_negSignals_','_totSignals_')+tempsig)

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= str(lumi)+" fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation Preliminary"
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
B = 0.22*H_ref
L = 0.12*W_ref
R = 0.04*W_ref

tagPosX = 0.76
tagPosY = 0.62

bkghists = {}
bkghistsmerged = {}
for tag in tagList:
	tagStr='nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]
	#if skip(tag[3],tag[2]): continue #DO YOU WANT TO HAVE THIS??
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	for isEM in isEMlist:
		histPrefix=iPlot+'_'+lumiInTemplates+'fb_'
		catStr='is'+isEM+'_'+tagStr
		histPrefix+=catStr
		print histPrefix
		for proc in bkgProcList: 
			try: bkghists[proc+catStr] = RFile.Get(histPrefix+'__'+proc).Clone()
			except:
				print "There is no "+proc+"!!! Skipping it....."
				pass

		hData = RFile.Get(histPrefix+'__DATA').Clone()
		hSig = RFile.Get(histPrefix+'__sig').Clone(histPrefix+'__'+sig1)
		if scaleXsec: hSig.Scale(xsec[sig1])
		if doEfficiency: hSig.Scale(1./nRun[sig1])
		if doNegSigFrac: 
			hSig2 = RFile2.Get(histPrefix+'__sig').Clone(histPrefix+'__2'+sig1)
			if scaleXsec: hSig2.Scale(xsec[sig1])
			if doEfficiency: hSig2.Scale(1./nRun[sig1])

		bkgHT = bkghists[bkgProcList[0]+catStr].Clone(bkgProcList[0]+catStr+'totBkg')
		for proc in bkgProcList[1:]:
			try: bkgHT.Add(bkghists[proc+catStr])
			except: pass

		stackbkgHT = rt.THStack("stackbkgHT","")
		for proc in bkgProcList:
			try: stackbkgHT.Add(bkghists[proc+catStr])
			except: pass

		c1 = rt.TCanvas("c1","c1",50,50,W,H)
		c1.SetFillColor(0)
		c1.SetBorderMode(0)
		c1.SetFrameFillStyle(0)
		c1.SetFrameBorderMode(0)
		#c1.SetTickx(0)
		#c1.SetTicky(0)
	
		yDiv=0.0
		uPad=rt.TPad("uPad","",0,yDiv,1,1) #for actual plots
	
		uPad.SetLeftMargin( L/W )
		uPad.SetRightMargin( R/W )
		uPad.SetTopMargin( T/H )
		uPad.SetBottomMargin( B/H )
		uPad.SetGrid()
	
		uPad.SetFillColor(0)
		uPad.SetBorderMode(0)
		uPad.SetFrameFillStyle(0)
		uPad.SetFrameBorderMode(0)
		#uPad.SetTickx(0)
		#uPad.SetTicky(0)
		uPad.Draw()
		
		uPad.cd()

		#hSig.Divide(bkgHT)
		hsigObkg = hSig.Clone('hsigObkg'+sig1)
		if doNegSigFrac: hsigNegFrac = hSig.Clone('hsigNegFrac'+sig1)
		for binNo in range(1,hsigObkg.GetNbinsX()+1):
			hsigObkg.SetBinContent(binNo,hSig.GetBinContent(binNo)/(math.sqrt(hSig.GetBinContent(binNo)+bkgHT.GetBinContent(binNo))+zero))
			if doNegSigFrac: hsigNegFrac.SetBinContent(binNo,hSig.GetBinContent(binNo)/hSig2.GetBinContent(binNo))
		if plotProc=='sig':
			formatUpperHist(hSig)
			if doEfficiency: hSig.GetYaxis().SetTitle("N_{passed}/N_{gen}")
			else: hSig.GetYaxis().SetTitle("N_{sig}")
			hSig.SetLineColor(2)
			hSig.SetFillColor(2)
			hSig.SetLineWidth(2)
			hSig.Draw("HIST")
		elif plotProc=='bkg':
			if doBkgFraction: 
				stackbkgHTfrac = rt.THStack("stackbkgHTfrac","")
				for proc in bkgProcList:
					bkghists[proc+catStr].SetLineColor(bkgHistColors[proc])
					bkghists[proc+catStr].SetFillColor(bkgHistColors[proc])
					bkghists[proc+catStr].SetLineWidth(2)
					bkghists[proc+catStr].GetXaxis().LabelsOption("v")
					bkghists[proc+catStr].Divide(bkgHT)
					bkghists[proc+catStr].Scale(100)
					try: stackbkgHTfrac.Add(bkghists[proc+catStr])
					except: pass

				bkgHT.GetYaxis().SetTitle("N_{process}/N_{tot Bkg}")
				bkghists[bkgProcList[0]+catStr].SetMaximum(140)
				bkghists[bkgProcList[0]+catStr].Draw("HIST")
				stackbkgHTfrac.Draw("SAMEHIST")
				
				leg = rt.TLegend(0.55,0.72,0.95,0.88)
				leg.SetShadowColor(0)
				leg.SetFillColor(0)
				leg.SetFillStyle(0)
				leg.SetLineColor(0)
				leg.SetLineStyle(0)
				leg.SetBorderSize(0) 
				leg.SetNColumns(3)
				leg.SetTextFont(62)#42)
				try: leg.AddEntry(bkghists['qcd'+catStr],"QCD","f")
				except: pass
				try: leg.AddEntry(bkghists['ewk'+catStr],"EWK","f")
				except: pass
				try: leg.AddEntry(bkghists['top'+catStr],"TOP","f")
				except: pass
				try: leg.AddEntry(bkghists['ttbj'+catStr],"t#bar{t}+b(j)","f")
				except: pass
				try: leg.AddEntry(bkghists['ttbb'+catStr],"t#bar{t}+b(b)","f")
				except: pass
				try: leg.AddEntry(bkghists['ttcc'+catStr],"t#bar{t}+c(c)","f")
				except: pass
				try: leg.AddEntry(bkghists['ttjj'+catStr],"t#bar{t}+j(j)","f")
				except: pass
				leg.Draw("same")
			else:
				formatUpperHist(bkgHT)
				bkgHT.GetYaxis().SetTitle("N_{Tot Bkg}")
				bkgHT.SetLineColor(2)
				bkgHT.SetFillColor(2)
				bkgHT.SetLineWidth(2)
				bkgHT.Draw("HIST")

		elif plotProc in bkgProcList:
			formatUpperHist(bkghists[plotProc+catStr])
			bkghists[plotProc+catStr].GetYaxis().SetTitle("N_{"+plotProc+"}")
			if doBkgFraction: bkghists[plotProc+catStr].GetYaxis().SetTitle("N_{"+plotProc+"}/N_{tot Bkg}")
			bkghists[plotProc+catStr].SetLineColor(2)
			bkghists[plotProc+catStr].SetFillColor(2)
			bkghists[plotProc+catStr].SetLineWidth(2)
			if doBkgFraction: 
				bkghists[plotProc+catStr].Divide(bkgHT)
				bkghists[plotProc+catStr].Scale(100)
			bkghists[plotProc+catStr].Draw("HIST")
		else:
			if doNegSigFrac: 
				formatUpperHist(hsigNegFrac)
				hsigNegFrac.GetYaxis().SetTitle("N_{neg}/N_{total}")
				hsigNegFrac.SetLineColor(2)
				hsigNegFrac.SetFillColor(0)
				hsigNegFrac.SetLineWidth(4)
				hsigNegFrac.SetMinimum(0)
				hsigNegFrac.SetMaximum(1)
				hsigNegFrac.Draw("HIST")
			else:
				formatUpperHist(hsigObkg)
				hsigObkg.GetYaxis().SetTitle("N_{sig}/#sqrt{N_{sig}+N_{bkg}}")
				hsigObkg.SetLineColor(2)
				hsigObkg.SetFillColor(0)
				hsigObkg.SetLineWidth(4)
				hsigObkg.Draw("HIST")

		chLatex = rt.TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.04)
		chLatex.SetTextAlign(21) # align center
		flvString = ''
		tagString = ''
		if isEM=='E': flvString+='e+jets'
		if isEM=='M': flvString+='#mu+jets'
		if tag[0]!='0p': 
			if 'p' in tag[0]: tagString+='#geq'+tag[0][:-1]+'res-t/'
			else: tagString+=tag[0]+'res-t/'
		if tag[1]!='0p': 
			if 'p' in tag[1]: tagString+='#geq'+tag[1][:-1]+'t/'
			else: tagString+=tag[1]+'t/'
		if tag[2]!='0p': 
			if 'p' in tag[2]: tagString+='#geq'+tag[2][:-1]+'W/'
			else: tagString+=tag[2]+'W/'
		if tag[3]!='0p': 
			if 'p' in tag[3]: tagString+='#geq'+tag[3][:-1]+'b/'
			else: tagString+=tag[3]+'b/'
		if tag[4]!='0p': 
			if 'p' in tag[4]: tagString+='#geq'+tag[4][:-1]+'j'
			else: tagString+=tag[4]+'j'
		if tagString.endswith('/'): tagString = tagString[:-1]
		chLatex.DrawLatex(tagPosX, tagPosY, flvString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)

		#draw the lumi text on the canvas
		CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)
	
		uPad.Update()
		uPad.RedrawAxis()
		frame = uPad.GetFrame()
		uPad.Draw()

		#c1.Write()
		savePrefix = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
		if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix.replace('_nHOT0p','').replace('_nT0p','').replace('_nW0p','').replace('_nB0p','').replace('_nJ0p','')
		savePrefix+=isRebinned.replace('_rebinned_stat1p1','')+saveKey
		if yLog: savePrefix+='_logy'

		if plotProc=='sig':
			savePrefix+='_'+sig1
		elif plotProc=='bkg':
			savePrefix+='_bkg'
			if doBkgFraction: savePrefix+='frac'
		elif plotProc in bkgProcList:
			savePrefix+='_'+plotProc
		else:
			if plotLimits: savePrefix+='_'+sig1+'_lim'
			elif doNegSigFrac: savePrefix+='_'+sig1+'_negSigFrac'
			else: savePrefix+='_'+sig1+'_SoB'

		c1.SaveAs(savePrefix+".png")
		#c1.SaveAs(savePrefix+".pdf")
		#c1.SaveAs(savePrefix+".eps")
		for proc in bkgProcList:
			try: del bkghists[proc+catStr]
			except: pass
					
	# Making plots for e+jets/mu+jets combined #
	histPrefixE = iPlot+'_'+lumiInTemplates+'fb_isE_'+tagStr
	histPrefixM = iPlot+'_'+lumiInTemplates+'fb_isM_'+tagStr
	bkghistsmerged = {}
	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr] = RFile.Get(histPrefixE+'__'+proc).Clone()
			bkghistsmerged[proc+'isL'+tagStr].Add(RFile.Get(histPrefixM+'__'+proc))
		except: pass
	hDatamerged = RFile.Get(histPrefixE+'__DATA').Clone()
	hDatamerged.Add(RFile.Get(histPrefixM+'__DATA').Clone())
	hSigmerged = RFile.Get(histPrefixE+'__sig').Clone(histPrefixE+'__'+sig1+'merged')
	hSigmerged.Add(RFile.Get(histPrefixM+'__sig').Clone())
	if scaleXsec: hSigmerged.Scale(xsec[sig1])
	if doEfficiency: hSigmerged.Scale(1./nRun[sig1])
	if doNegSigFrac:
		hSig2merged = RFile2.Get(histPrefixE+'__sig').Clone(histPrefixE+'__'+sig1+'merged')
		hSig2merged.Add(RFile2.Get(histPrefixM+'__sig').Clone())
		if scaleXsec: hSig2merged.Scale(xsec[sig1])
		if doEfficiency: hSig2merged.Scale(1./nRun[sig1])

	bkgHTmerged = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone(bkgProcList[0]+'isL'+tagStr+'totBkg')
	for proc in bkgProcList[1:]:
		try: bkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass

	c1merged = rt.TCanvas("c1merged","c1merged",50,50,W,H)
	c1merged.SetFillColor(0)
	c1merged.SetBorderMode(0)
	c1merged.SetFrameFillStyle(0)
	c1merged.SetFrameBorderMode(0)
	#c1merged.SetTickx(0)
	#c1merged.SetTicky(0)
	
	yDiv=0.0
	uPad=rt.TPad("uPad","",0,yDiv,1,1) #for actual plots
	
	uPad.SetLeftMargin( L/W )
	uPad.SetRightMargin( R/W )
	uPad.SetTopMargin( T/H )
	uPad.SetBottomMargin( B/H )
	
	uPad.SetGrid()
	
	uPad.SetFillColor(0)
	uPad.SetBorderMode(0)
	uPad.SetFrameFillStyle(0)
	uPad.SetFrameBorderMode(0)
	#uPad.SetTickx(0)
	#uPad.SetTicky(0)
	uPad.Draw()
	
	uPad.cd()

	#hSigmerged.Divide(bkgHTmerged)
	hsigObkgmerged = hSigmerged.Clone('hsigObkgmerged'+sig1)
	if doNegSigFrac: hsigNegFracmerged = hSig.Clone('hsigNegFracmerged'+sig1)
	for binNo in range(1,hsigObkgmerged.GetNbinsX()+1):
		if plotLimits:
			binLabelB = hsigObkgmerged.GetXaxis().GetBinLabel(binNo).split('/')[0][:-1]
			binLabelJ = hsigObkgmerged.GetXaxis().GetBinLabel(binNo).split('/')[1][:-1]
			catStr = 'nB'+binLabelB.replace('#geq','')
			if '#geq' in binLabelB: catStr+='p'
			catStr+='_nJ'+binLabelJ.replace('#geq','')
			if '#geq' in binLabelJ: catStr+='p'
			fexp = open(limitFile.replace('/nB1_nJ3/','/'+catStr+'/').replace('_HTBM200_','_HTBM'+sig1+'_'), 'rU')
			linesExp = fexp.readlines()
			fexp.close()
			exp = float(linesExp[1].strip().split()[1])
			hsigObkgmerged.SetBinContent(binNo,exp)
		else: 
			hsigObkgmerged.SetBinContent(binNo,hSigmerged.GetBinContent(binNo)/(math.sqrt(hSigmerged.GetBinContent(binNo)+bkgHTmerged.GetBinContent(binNo))+zero))
			if doNegSigFrac: hsigNegFracmerged.SetBinContent(binNo,hSigmerged.GetBinContent(binNo)/hSig2merged.GetBinContent(binNo))

	if plotProc=='sig':
		formatUpperHist(hSigmerged)
		if doEfficiency: hSigmerged.GetYaxis().SetTitle("N_{passed}/N_{gen}")
		else: hSigmerged.GetYaxis().SetTitle("N_{sig}")
		hSigmerged.SetLineColor(2)
		hSigmerged.SetFillColor(2)
		hSigmerged.SetLineWidth(2)
		#hSigmerged.SetMaximum(0.07)
		hSigmerged.Draw("HIST")
	elif plotProc=='bkg':
		if doBkgFraction: 
			stackbkgHTfracmerged = rt.THStack("stackbkgHTfracmerged","")
			for proc in bkgProcList:
				bkghistsmerged[proc+'isL'+tagStr].SetLineColor(bkgHistColors[proc])
				bkghistsmerged[proc+'isL'+tagStr].SetFillColor(bkgHistColors[proc])
				bkghistsmerged[proc+'isL'+tagStr].SetLineWidth(2)
				bkghistsmerged[proc+'isL'+tagStr].GetXaxis().LabelsOption("v")
				bkghistsmerged[proc+'isL'+tagStr].Divide(bkgHTmerged)
				bkghistsmerged[proc+'isL'+tagStr].Scale(100)
				try: stackbkgHTfracmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
				except: pass
			bkghistsmerged['ttbbisL'+tagStr].SetMaximum(140)
			bkghistsmerged['ttbbisL'+tagStr].Draw("HIST")
			stackbkgHTfracmerged.Draw("SAMEHIST")
			
			leg = rt.TLegend(0.55,0.72,0.95,0.88)
			leg.SetShadowColor(0)
			leg.SetFillColor(0)
			leg.SetFillStyle(0)
			leg.SetLineColor(0)
			leg.SetLineStyle(0)
			leg.SetBorderSize(0) 
			leg.SetNColumns(3)
			leg.SetTextFont(62)#42)
			try: leg.AddEntry(bkghistsmerged['qcd'+'isL'+tagStr],"QCD","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['ewk'+'isL'+tagStr],"EWK","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['top'+'isL'+tagStr],"TOP","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['ttbj'+'isL'+tagStr],"t#bar{t}+b(j)","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['ttbb'+'isL'+tagStr],"t#bar{t}+b(b)","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['ttcc'+'isL'+tagStr],"t#bar{t}+c(c)","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['ttjj'+'isL'+tagStr],"t#bar{t}+j(j)","f")
			except: pass
			leg.Draw("same")
		else:
			formatUpperHist(bkgHTmerged)
			bkgHTmerged.GetYaxis().SetTitle("N_{Tot Bkg}")
			bkgHTmerged.SetLineColor(2)
			bkgHTmerged.SetFillColor(2)
			bkgHTmerged.SetLineWidth(2)
			bkgHTmerged.Draw("HIST")
	elif plotProc in bkgProcList:
		formatUpperHist(bkghistsmerged[plotProc+'isL'+tagStr])
		bkghistsmerged[plotProc+'isL'+tagStr].GetYaxis().SetTitle("N_{"+plotProc+"}")
		if doBkgFraction: bkghistsmerged[plotProc+'isL'+tagStr].GetYaxis().SetTitle("N_{"+plotProc+"}/N_{tot Bkg}")
		bkghistsmerged[plotProc+'isL'+tagStr].SetLineColor(2)
		bkghistsmerged[plotProc+'isL'+tagStr].SetFillColor(2)
		bkghistsmerged[plotProc+'isL'+tagStr].SetLineWidth(2)
		if doBkgFraction: 
			bkghistsmerged[plotProc+'isL'+tagStr].Divide(bkgHTmerged)
			bkghistsmerged[plotProc+'isL'+tagStr].Scale(100)
		bkghistsmerged[plotProc+'isL'+tagStr].Draw("HIST")
	else:
		if doNegSigFrac: 
			formatUpperHist(hsigNegFracmerged)
			hsigNegFracmerged.GetYaxis().SetTitle("N_{neg}/N_{total}")
			hsigNegFracmerged.SetLineColor(2)
			hsigNegFracmerged.SetFillColor(0)
			hsigNegFracmerged.SetLineWidth(4)
			hsigNegFracmerged.SetMinimum(0.29)
			hsigNegFracmerged.SetMaximum(0.45)
			hsigNegFracmerged.Draw("HIST")
			hsigNegFracmerged.SetLineColor(1)
			hsigNegFracmerged.SetFillColor(0)
			hsigNegFracmerged.SetLineWidth(4)
			hsigNegFracmerged.Draw("SAME HIST")
				
			leg = rt.TLegend(0.45,0.75,0.99,0.90)
			leg.SetShadowColor(0)
			leg.SetFillColor(0)
			leg.SetFillStyle(0)
			leg.SetLineColor(0)
			leg.SetLineStyle(0)
			leg.SetBorderSize(0) 
			leg.SetNColumns(4)
			leg.SetTextFont(62)#42)
			leg.AddEntry(hsigNegFracmerged,sig1leg,"f")
			leg.Draw("same")

		else:
			#formatUpperHist(hsigObkgmerged)
			hsigObkgmerged.GetXaxis().LabelsOption("v")
			if plotLimits: hsigObkgmerged.GetYaxis().SetTitle("Upper limit")
			else: hsigObkgmerged.GetYaxis().SetTitle("N_{sig}/#sqrt{N_{sig}+N_{bkg}}")
			hsigObkgmerged.SetLineColor(2)
			hsigObkgmerged.SetFillColor(0)
			hsigObkgmerged.SetLineWidth(4)
			hsigObkgmerged.Draw("HIST")
			
# 			hsigObkgmerged.SetLineColor(1)
# 			hsigObkgmerged.SetFillColor(0)
# 			hsigObkgmerged.SetLineWidth(4)
# 			hsigObkgmerged.Draw("SAME HIST")
				
			leg = rt.TLegend(0.45,0.75,0.99,0.90)
			leg.SetShadowColor(0)
			leg.SetFillColor(0)
			leg.SetFillStyle(0)
			leg.SetLineColor(0)
			leg.SetLineStyle(0)
			leg.SetBorderSize(0) 
			leg.SetNColumns(4)
			leg.SetTextFont(62)#42)
			#leg.AddEntry(hsigObkgmerged,mass,"f")
			leg.Draw("same")
	
	chLatexmerged = rt.TLatex()
	chLatexmerged.SetNDC()
	chLatexmerged.SetTextSize(0.04)
	chLatexmerged.SetTextAlign(21) # align center
	flvString = 'e/#mu+jets'
	chLatexmerged.DrawLatex(tagPosX, tagPosY, flvString)
	chLatexmerged.DrawLatex(tagPosX, tagPosY-0.06, tagString)

	#draw the lumi text on the canvas
	CMS_lumi.CMS_lumi(uPad, iPeriod, iPos)
	
	uPad.Update()
	uPad.RedrawAxis()
	frame = uPad.GetFrame()
	uPad.Draw()
	
	#c1merged.Write()
	savePrefixmerged = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('isE','isL').replace('_nHOT0p','').replace('_nT0p','').replace('_nW0p','').replace('_nB0p','').replace('_nJ0p','')
	savePrefixmerged+=isRebinned.replace('_rebinned_stat1p1','')+saveKey
	if yLog: savePrefixmerged+='_logy'
	
	if plotProc=='sig':
		savePrefixmerged+='_'+sig1
	elif plotProc=='bkg':
		savePrefixmerged+='_bkg'
		if doBkgFraction: savePrefixmerged+='frac'
	elif plotProc in bkgProcList:
		savePrefixmerged+='_'+plotProc
	else:
		if plotLimits: savePrefixmerged+='_'+sig1+'_lim'
		else: savePrefixmerged+='_'+sig1+'_SoB'

	c1merged.SaveAs(savePrefixmerged+".png")
	#c1merged.SaveAs(savePrefixmerged+".pdf")
	#c1merged.SaveAs(savePrefixmerged+".eps")
	for proc in bkgProcList:
		try: del bkghistsmerged[proc+'isL'+tagStr]
		except: pass
			
RFile.Close()
if doNegSigFrac: RFile2.Close()
	
print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


