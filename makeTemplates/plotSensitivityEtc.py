#!/usr/bin/python

import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from ROOT import *
from weights import *
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

lumi=36 #for plots
lumiInTemplates= str(targetlumi/1000).replace('.','p') # 1/fb

region='SR' #SR,PS
isCategorized=True
iPlot='YLD'
if len(sys.argv)>1: iPlot=str(sys.argv[1])
cutString='lep50_MET30_DR0_1jet50_2jet40'
pfix='templates'
if not isCategorized: pfix='kinematics_'+region
#templateDir=os.getcwd()+'/'+pfix+'_negSignals_2016_12_1/'+cutString+'/' #for negative signal fraction
templateDir=os.getcwd()+'/'+pfix+'_noWeight_2016_11_28/'+cutString+'/' #for signal efficiency
#templateDir=os.getcwd()+'/'+pfix+'_bkgSplit_wRwt_cats_2016_12_10/'+cutString+'/' #for background yields and fraction
plotLimits = False
limitFile = '/user_data/ssagir/HTB_limits_2016/templates_2016_11_26/nB1_nJ3/limits_templates_HT_HTBM200_36p0fb_rebinned_stat0p3_expected.txt'
massList = range(180,200+1,20)+range(250,500+1,50)
massList = [str(mss) for mss in massList]

useHTbinned = True
splitWJets = False
splitTTbar = False
isRebinned=''#'_rebinned_stat0p3' #post for ROOT file names
if not useHTbinned: isRebinned+='_incWjets'
if splitWJets: isRebinned+='_WJsplit'
if splitTTbar: isRebinned+='_TTsplit'
isRebinned+=''#'_rebinned_stat0p3'
saveKey = '' # tag for plot names

mass = '450'
sig1='HTBM'+mass # choose the 1st signal to plot
sig1leg='H^{#pm} ('+mass+' GeV)'
tempsig='templates_'+iPlot+'_'+sig1+'_'+lumiInTemplates+'fb'+isRebinned+'.root'

if splitWJets and not splitTTbar: bkgProcList = ['ttbar','wjetsb','wjetsc','wjetsl','top','ewk','qcd']
elif not splitWJets and splitTTbar: bkgProcList = ['ttbb','ttll','wjets','top','ewk','qcd']
elif splitWJets and splitTTbar: bkgProcList = ['ttbb','ttll','wjetsb','wjetsc','wjetsl','top','ewk','qcd']
else: bkgProcList = ['ttbar','wjets','top','ewk','qcd']

if '53' in sig1: bkgHistColors = {'top':kRed-9,'ewk':kBlue-7,'qcd':kOrange-5} #X53X53
elif 'HTB' in sig1: bkgHistColors = {'ttbar':kGreen-3,'wjets':kPink-4,'ttbb':kGreen-3,'ttll':kGreen+3,'wjetsb':kRed-9,'wjetsc':kPink-4,'wjetsl':kBlue-7,'top':kAzure+8,'ewk':kMagenta-2,'qcd':kOrange+5} #HTB
else: bkgHistColors = {'top':kAzure+8,'ewk':kMagenta-2,'qcd':kOrange+5} #TT

yLog  = False
plotProc = 'sig'#sig,totBkg,sigOverBkg,'ttbar','wjets','top','ewk','qcd'
doBkgFraction = False #set plotProc to "totBkg"
doNegSigFrac = False
doEfficiency = True
scaleXsec = False

isEMlist =['E','M']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['2','3','3p','4p']
njetslist = ['4','5','6p']
if not isCategorized: 
	nbtaglist = ['2p']
	njetslist = ['2p']
if iPlot=='YLD':
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0p']
	njetslist = ['0p']
tagList = list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))

def formatUpperHist(histogram):
	histogram.GetXaxis().SetLabelSize(0)

	histogram.GetXaxis().SetLabelSize(0.045)
	histogram.GetXaxis().SetTitleSize(0.055)
	histogram.GetYaxis().SetLabelSize(0.045)
	histogram.GetYaxis().SetTitleSize(0.055)
	histogram.GetYaxis().SetTitleOffset(1.25)
	histogram.GetXaxis().SetNdivisions(506)
	histogram.GetYaxis().CenterTitle()
	if yLog: 
		uPad.SetLogy()
		#histogram.SetMinimum(0.101)

RFiles={}
for mss in massList: RFiles[mss] = TFile(templateDir+tempsig.replace(mass,mss))
RFiles2={}
for mss in massList: RFiles2[mss] = TFile(templateDir.replace('_negSignals_','_totSignals_')+tempsig.replace(mass,mss))
bkghists = {}
bkghistsmerged = {}
sighists = {}
sighistsmerged = {}
sighists2 = {}
sighists2merged = {}
hsigObkg = {}
hsigNegFrac = {}
hsigObkgmerged = {}
hsigNegFracmerged = {}
for tag in tagList:
	tagStr='nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]
	#if skip(tag[3],tag[2]): continue #DO YOU WANT TO HAVE THIS??
	modTag = tagStr[tagStr.find('nT'):tagStr.find('nJ')-3]
	for isEM in isEMlist:
		histPrefix=iPlot+'_'+lumiInTemplates+'fb_'
		catStr='is'+isEM+'_'+tagStr
		histPrefix+=catStr
		print histPrefix
		for proc in bkgProcList: 
			try: bkghists[proc+catStr] = RFiles[mass].Get(histPrefix+'__'+proc).Clone()
			except:
				print "There is no "+proc+"!!!!!!!!"
				print "Skipping "+proc+"....."
				pass
		hData = RFiles[mass].Get(histPrefix+'__DATA').Clone()
		for mss in massList: 
			sighists[mss] = RFiles[mss].Get(histPrefix+'__sig').Clone(histPrefix+'__'+mss)
			if scaleXsec: sighists[mss].Scale(xsec['HTBM'+mss])
			if doEfficiency: sighists[mss].Scale(1./nRun['HTBM'+mss])
			if doNegSigFrac: 
				sighists2[mss] = RFiles2[mss].Get(histPrefix+'__sig').Clone(histPrefix+'__2'+mss)
				if scaleXsec: sighists2[mss].Scale(xsec['HTBM'+mss])
				if doEfficiency: sighists2[mss].Scale(1./nRun['HTBM'+mss])

		bkgHT = bkghists[bkgProcList[0]+catStr].Clone()
		for proc in bkgProcList:
			if proc==bkgProcList[0]: continue
			try: bkgHT.Add(bkghists[proc+catStr])
			except: pass

		stackbkgHT = THStack("stackbkgHT","")
		for proc in bkgProcList:
			try: stackbkgHT.Add(bkghists[proc+catStr])
			except: pass

		gStyle.SetOptStat(0)
		c1 = TCanvas("c1","c1",1200,1000)
		gStyle.SetErrorX(0.5)
		yDiv=0.0
		uMargin = 0.12
		rMargin=.04
		uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
		uPad.SetTopMargin(0.10)
		uPad.SetBottomMargin(uMargin)
		uPad.SetRightMargin(rMargin)
		uPad.SetLeftMargin(.15)
		uPad.Draw()
	
		uPad.cd()
		uPad.SetGrid()

		#sighists[mass].Divide(bkgHT)
		for mss in massList: 
			hsigObkg[mss] = sighists[mss].Clone('hsigObkg'+mss)
			if doNegSigFrac: hsigNegFrac[mss] = sighists[mss].Clone('hsigNegFrac'+mss)
			for binNo in range(1,hsigObkg[mss].GetNbinsX()+1):
				hsigObkg[mss].SetBinContent(binNo,sighists[mss].GetBinContent(binNo)/math.sqrt(sighists[mss].GetBinContent(binNo)+bkgHT.GetBinContent(binNo)))
				if doNegSigFrac: hsigNegFrac[mss].SetBinContent(binNo,sighists[mss].GetBinContent(binNo)/sighists2[mss].GetBinContent(binNo))
		if plotProc=='sig':
			formatUpperHist(sighists[mass])
			if doEfficiency: sighists[mass].GetYaxis().SetTitle("N_{passed}/N_{gen}")
			else: sighists[mass].GetYaxis().SetTitle("N_{sig}")
			sighists[mass].SetLineColor(2)
			sighists[mass].SetFillColor(2)
			sighists[mass].SetLineWidth(2)
			sighists[mass].Draw("HIST")
		elif plotProc=='totBkg':
			if doBkgFraction: 
				stackbkgHTfrac = THStack("stackbkgHTfrac","")
				for proc in bkgProcList:
					bkghists[proc+catStr].Divide(bkgHT)
					try: stackbkgHTfrac.Add(bkghists[proc+catStr])
					except: pass

				bkgHT.GetYaxis().SetTitle("N_{process}/N_{tot Bkg}")
				for proc in bkgProcList:
					try: 
						bkghists[proc+catStr].SetLineColor(bkgHistColors[proc])
						bkghists[proc+catStr].SetFillColor(bkgHistColors[proc])
						bkghists[proc+catStr].SetLineWidth(2)
					except: pass
				stackbkgHTfrac.Draw("HIST")
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
			if doBkgFraction: bkghists[plotProc+catStr].Divide(bkgHT)
			bkghists[plotProc+catStr].Draw("HIST")
		else:
			if doNegSigFrac: 
				formatUpperHist(hsigNegFrac[mass])
				hsigNegFrac[mass].GetYaxis().SetTitle("N_{neg}/N_{total}")
				hsigNegFrac[mass].SetLineColor(2)
				hsigNegFrac[mass].SetFillColor(0)
				hsigNegFrac[mass].SetLineWidth(4)
				hsigNegFrac[mass].SetMinimum(0)
				hsigNegFrac[mass].SetMaximum(1)
				hsigNegFrac[mass].Draw("HIST")
			else:
				formatUpperHist(hsigObkg[mass])
				hsigObkg[mass].GetYaxis().SetTitle("N_{sig}/#sqrt{N_{sig}+N_{bkg}}")
				hsigObkg[mass].SetLineColor(2)
				hsigObkg[mass].SetFillColor(0)
				hsigObkg[mass].SetLineWidth(4)
				hsigObkg[mass].Draw("HIST")
		
		chLatex = TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.04)
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

		prelimTex=TLatex()
		prelimTex.SetNDC()
		prelimTex.SetTextAlign(31) # align right
		prelimTex.SetTextFont(42)
		prelimTex.SetTextSize(0.05)
		prelimTex.SetLineWidth(2)
		prelimTex.DrawLatex(0.95,0.92,str(lumi)+" fb^{-1} (13 TeV)")

		prelimTex2=TLatex()
		prelimTex2.SetNDC()
		prelimTex2.SetTextFont(61)
		prelimTex2.SetLineWidth(2)
		prelimTex2.SetTextSize(0.08)
		prelimTex2.DrawLatex(0.12,0.92,"CMS")

		prelimTex3=TLatex()
		prelimTex3.SetNDC()
		prelimTex3.SetTextAlign(13)
		prelimTex3.SetTextFont(52)
		prelimTex3.SetTextSize(0.055)
		prelimTex3.SetLineWidth(2)
		prelimTex3.DrawLatex(0.26,0.96,"Preliminary")

		#c1.Write()
		savePrefix = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
		if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix+isRebinned.replace('_rebinned_stat1p1','')+saveKey
		if nttaglist[0]=='0p': savePrefix=savePrefix.replace('nT0p_','')
		if nWtaglist[0]=='0p': savePrefix=savePrefix.replace('nW0p_','')
		if nbtaglist[0]=='0p': savePrefix=savePrefix.replace('nB0p_','')
		if njetslist[0]=='0p': savePrefix=savePrefix.replace('nJ0p_','')
		if yLog: savePrefix+='_logy'

		if plotProc=='sig':
			savePrefix+='_'+sig1
		elif plotProc=='totBkg':
			savePrefix+='_totBkg'
			if doBkgFraction: savePrefix+='frac'
		elif plotProc in bkgProcList:
			savePrefix+='_'+plotProc
		else:
			if plotLimits: savePrefix+='_'+sig1+'_lim'
			elif doNegSigFrac: savePrefix+='_'+sig1+'_negSigFrac'
			else: savePrefix+='_'+sig1+'_sigOverBkg'

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
	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+'isL'+tagStr] = RFiles[mass].Get(histPrefixE+'__'+proc).Clone()
			bkghistsmerged[proc+'isL'+tagStr].Add(RFiles[mass].Get(histPrefixM+'__'+proc))
		except:pass
	hDatamerged = RFiles[mass].Get(histPrefixE+'__DATA').Clone()
	hDatamerged.Add(RFiles[mass].Get(histPrefixM+'__DATA').Clone())
	for mss in massList: 
		sighistsmerged[mss] = RFiles[mss].Get(histPrefixE+'__sig').Clone(histPrefixE+'__'+mss+'merged')
		sighistsmerged[mss].Add(RFiles[mss].Get(histPrefixM+'__sig').Clone())
		if scaleXsec: sighistsmerged[mss].Scale(xsec['HTBM'+mss])
		if doEfficiency: sighistsmerged[mss].Scale(1./nRun['HTBM'+mss])
		if doNegSigFrac: 
			sighists2merged[mss] = RFiles2[mss].Get(histPrefixE+'__sig').Clone(histPrefixE+'__'+mss+'merged')
			sighists2merged[mss].Add(RFiles2[mss].Get(histPrefixM+'__sig').Clone())
			if scaleXsec: sighists2merged[mss].Scale(xsec['HTBM'+mss])
			if doEfficiency: sighists2merged[mss].Scale(1./nRun['HTBM'+mss])

	bkgHTmerged = bkghistsmerged[bkgProcList[0]+'isL'+tagStr].Clone()
	for proc in bkgProcList:
		if proc==bkgProcList[0]: continue
		try: bkgHTmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
		except: pass

	gStyle.SetOptStat(0)
	c1merged = TCanvas("c1merged","c1merged",1200,1000)
	gStyle.SetErrorX(0.5)
	yDiv=0.0
	uMargin = 0.12
	rMargin=.04
	uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
	uPad.SetTopMargin(0.10)
	uPad.SetBottomMargin(uMargin)
	uPad.SetRightMargin(rMargin)
	uPad.SetLeftMargin(.15)
	uPad.Draw()
	
	uPad.cd()
	uPad.SetGrid()

	#sighistsmerged[mass].Divide(bkgHTmerged)
	for mss in massList: 
		hsigObkgmerged[mss] = sighistsmerged[mss].Clone('hsigObkgmerged'+mss)
		if doNegSigFrac: hsigNegFracmerged[mss] = sighists[mss].Clone('hsigNegFracmerged'+mss)
		for binNo in range(1,hsigObkgmerged[mss].GetNbinsX()+1):
			binLabelB = hsigObkgmerged[mss].GetXaxis().GetBinLabel(binNo).split('/')[0][:-1]
			binLabelJ = hsigObkgmerged[mss].GetXaxis().GetBinLabel(binNo).split('/')[1][:-1]
			catStr = 'nB'+binLabelB.replace('#geq','')
			if '#geq' in binLabelB: catStr+='p'
			catStr+='_nJ'+binLabelJ.replace('#geq','')
			if '#geq' in binLabelJ: catStr+='p'
			if plotLimits:
				fexp = open(limitFile.replace('/nB1_nJ3/','/'+catStr+'/').replace('_HTBM200_','_HTBM'+mss+'_'), 'rU')
				linesExp = fexp.readlines()
				fexp.close()
				exp = float(linesExp[1].strip().split()[1])
				hsigObkgmerged[mss].SetBinContent(binNo,exp)
			else: 
				hsigObkgmerged[mss].SetBinContent(binNo,sighistsmerged[mss].GetBinContent(binNo)/math.sqrt(sighistsmerged[mss].GetBinContent(binNo)+bkgHTmerged.GetBinContent(binNo)))
				if doNegSigFrac: hsigNegFracmerged[mss].SetBinContent(binNo,sighistsmerged[mss].GetBinContent(binNo)/sighists2merged[mss].GetBinContent(binNo))

	if plotProc=='sig':
		formatUpperHist(sighistsmerged[mass])
		if doEfficiency: sighistsmerged[mass].GetYaxis().SetTitle("N_{passed}/N_{gen}")
		else: sighistsmerged[mass].GetYaxis().SetTitle("N_{sig}")
		sighistsmerged[mass].SetLineColor(2)
		sighistsmerged[mass].SetFillColor(2)
		sighistsmerged[mass].SetLineWidth(2)
		sighistsmerged[mass].SetMaximum(0.07)
		sighistsmerged[mass].Draw("HIST")
	elif plotProc=='totBkg':
		if doBkgFraction: 
			stackbkgHTfracmerged = THStack("stackbkgHTfracmerged","")
			for proc in bkgProcList:
				bkghistsmerged[proc+'isL'+tagStr].Divide(bkgHTmerged)
				try: stackbkgHTfracmerged.Add(bkghistsmerged[proc+'isL'+tagStr])
				except: pass

			bkgHTmerged.GetYaxis().SetTitle("N_{process}/N_{tot Bkg}")
			stackbkgHTfracmerged.SetMaximum(1.5)
			for proc in bkgProcList:
				try: 
					bkghistsmerged[proc+'isL'+tagStr].SetLineColor(bkgHistColors[proc])
					bkghistsmerged[proc+'isL'+tagStr].SetFillColor(bkgHistColors[proc])
					bkghistsmerged[proc+'isL'+tagStr].SetLineWidth(2)
				except: pass
			stackbkgHTfracmerged.Draw("HIST")
			
			leg = TLegend(0.35,0.67,0.95,0.87)
			leg.SetShadowColor(0)
			leg.SetFillColor(0)
			leg.SetFillStyle(0)
			leg.SetLineColor(0)
			leg.SetLineStyle(0)
			leg.SetBorderSize(0) 
			leg.SetNColumns(3)
			leg.SetTextFont(62)#42)
			leg.AddEntry(bkghistsmerged['qcd'+'isL'+tagStr],"QCD","f")
			try: leg.AddEntry(bkghistsmerged['ewk'+'isL'+tagStr],"Other EWK","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['top'+'isL'+tagStr],"Other Top","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['wjets'+'isL'+tagStr],"W+jets","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['wjetsb'+'isL'+tagStr],"W+b","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['wjetsc'+'isL'+tagStr],"W+c","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['wjetsl'+'isL'+tagStr],"W+udsg","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['ttbar'+'isL'+tagStr],"t#bar{t}","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['ttbb'+'isL'+tagStr],"t#bar{t}bb","f")
			except: pass
			try: leg.AddEntry(bkghistsmerged['ttll'+'isL'+tagStr],"t#bar{t}ll","f")
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
		if doBkgFraction: bkghistsmerged[plotProc+'isL'+tagStr].Divide(bkgHTmerged)
		bkghistsmerged[plotProc+'isL'+tagStr].Draw("HIST")
	else:
		if doNegSigFrac: 
			formatUpperHist(hsigNegFracmerged[mass])
			hsigNegFracmerged[mass].GetYaxis().SetTitle("N_{neg}/N_{total}")
			hsigNegFracmerged[mass].SetLineColor(2)
			hsigNegFracmerged[mass].SetFillColor(0)
			hsigNegFracmerged[mass].SetLineWidth(4)
			hsigNegFracmerged[mass].SetMinimum(0.29)
			hsigNegFracmerged[mass].SetMaximum(0.45)
			hsigNegFracmerged[mass].Draw("HIST")
			ind_=0
			for mss in massList: 
				ind_+=1
				hsigNegFracmerged[mss].SetLineColor(ind_)
				hsigNegFracmerged[mss].SetFillColor(0)
				hsigNegFracmerged[mss].SetLineWidth(4)
				hsigNegFracmerged[mss].Draw("SAME HIST")
				
			leg = TLegend(0.45,0.75,0.99,0.90)
			leg.SetShadowColor(0)
			leg.SetFillColor(0)
			leg.SetFillStyle(0)
			leg.SetLineColor(0)
			leg.SetLineStyle(0)
			leg.SetBorderSize(0) 
			leg.SetNColumns(4)
			leg.SetTextFont(62)#42)
			for mss in massList: leg.AddEntry(hsigNegFracmerged[mss],mss,"f")
			leg.Draw("same")

		else:
			formatUpperHist(hsigObkgmerged[mass])
			if plotLimits: hsigObkgmerged[mass].GetYaxis().SetTitle("Upper limit")
			else: hsigObkgmerged[mass].GetYaxis().SetTitle("N_{sig}/#sqrt{N_{sig}+N_{bkg}}")
			hsigObkgmerged[mass].SetLineColor(2)
			hsigObkgmerged[mass].SetFillColor(0)
			hsigObkgmerged[mass].SetLineWidth(4)
			hsigObkgmerged[mass].Draw("HIST")
			
# 			ind_=0
# 			for mss in massList: 
# 				ind_+=1
# 				hsigObkgmerged[mss].SetLineColor(ind_)
# 				hsigObkgmerged[mss].SetFillColor(0)
# 				hsigObkgmerged[mss].SetLineWidth(4)
# 				hsigObkgmerged[mss].Draw("SAME HIST")
				
			leg = TLegend(0.45,0.75,0.99,0.90)
			leg.SetShadowColor(0)
			leg.SetFillColor(0)
			leg.SetFillStyle(0)
			leg.SetLineColor(0)
			leg.SetLineStyle(0)
			leg.SetBorderSize(0) 
			leg.SetNColumns(4)
			leg.SetTextFont(62)#42)
			leg.AddEntry(hsigObkgmerged[mass],mass,"f")
			#for mss in massList: leg.AddEntry(hsigObkgmerged[mss],mss,"f")
			leg.Draw("same")
	
	#uPad.RedrawAxis()
	chLatexmerged = TLatex()
	chLatexmerged.SetNDC()
	chLatexmerged.SetTextSize(0.04)
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

	prelimTex=TLatex()
	prelimTex.SetNDC()
	prelimTex.SetTextAlign(31) # align right
	prelimTex.SetTextFont(42)
	prelimTex.SetTextSize(0.05)
	prelimTex.SetLineWidth(2)
	prelimTex.DrawLatex(0.95,0.92,str(lumi)+" fb^{-1} (13 TeV)")
	
	prelimTex2=TLatex()
	prelimTex2.SetNDC()
	prelimTex2.SetTextFont(61)
	prelimTex2.SetLineWidth(2)
	prelimTex2.SetTextSize(0.08)
	prelimTex2.DrawLatex(0.12,0.92,"CMS")
	
	prelimTex3=TLatex()
	prelimTex3.SetNDC()
	prelimTex3.SetTextAlign(13)
	prelimTex3.SetTextFont(52)
	prelimTex3.SetTextSize(0.055)
	prelimTex3.SetLineWidth(2)
	prelimTex3.DrawLatex(0.26,0.96,"Preliminary")
	
	#c1merged.Write()
	savePrefixmerged = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('isE','isL')+isRebinned.replace('_rebinned_stat1p1','')+saveKey
	if nttaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nT0p_','')
	if nWtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nW0p_','')
	if nbtaglist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nB0p_','')
	if njetslist[0]=='0p': savePrefixmerged=savePrefixmerged.replace('nJ0p_','')
	if yLog: savePrefixmerged+='_logy'
	
	if plotProc=='sig':
		savePrefixmerged+='_'+sig1
	elif plotProc=='totBkg':
		savePrefixmerged+='_totBkg'
		if doBkgFraction: savePrefixmerged+='frac'
	elif plotProc in bkgProcList:
		savePrefixmerged+='_'+plotProc
	else:
		if plotLimits: savePrefixmerged+='_'+sig1+'_lim'
		else: savePrefixmerged+='_'+sig1+'_sigOverBkg'

	c1merged.SaveAs(savePrefixmerged+".pdf")
	c1merged.SaveAs(savePrefixmerged+".png")
	c1merged.SaveAs(savePrefixmerged+".eps")
	#c1merged.SaveAs(savePrefixmerged+".root")
	#c1merged.SaveAs(savePrefixmerged+".C")
	for proc in bkgProcList:
		try: del bkghistsmerged[proc+'isL'+tagStr]
		except: pass
			
for mss in massList: RFiles[mss].Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


