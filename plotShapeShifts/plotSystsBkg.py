#!/usr/bin/python

import os,sys,math,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
from array import array
from utils import *
import CMS_lumi, tdrstyle

#set the tdr style
tdrstyle.setTDRStyle()
rt.gROOT.SetBatch(1)

outDir = os.getcwd()+'/'
iPlot = 'HT'
year='R17'
if year=='R17':
	lumiStr = '41p53fb'
	lumi=41.5 #for plots
else:
	lumiStr = '59p97fb'
	lumi=59.97 #for plots
sig1 = 'tttt' #  choose the 1st signal to plot
isRebinned = '_rebinned_stat0p3'
useCombine = True
tempVersion = 'templates_'+year+'_Xtrig_2020_7_29/'
cutString = ''
if useCombine: templateFile = '../makeTemplates/'+tempVersion+'/'+cutString+'/templates_'+iPlot+'_'+lumiStr+isRebinned+'.root'
else: templateFile = '../makeTemplates/'+tempVersion+'/'+cutString+'/templates_'+iPlot+'_'+sig1+'_'+lumiStr+isRebinned+'.root'
if not os.path.exists(outDir+tempVersion): os.system('mkdir '+outDir+tempVersion)
if not os.path.exists(outDir+tempVersion+'/bkgs'): os.system('mkdir '+outDir+tempVersion+'/bkgs')

saveKey = ''
bkgTTBarList = ['ttnobb','ttbb'] #['ttjj','ttcc','ttbb','ttbj']
bkgList = bkgTTBarList+['top','ewk','qcd'] #some uncertainties will be skipped depending on the bkgList[0] process!!!!
isEMlist  = ['E','M']
nhottlist = ['0','1p']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['2','3','4p']
njetslist = ['5','6','7','8','9','10p']
# nbtaglist = ['2p']
# njetslist = ['6p']
systematics = ['pileup','prefire','btag','mistag','jec','jer','hotstat','hotcspur','hotclosure','PSwgt','muRF','pdf','hdamp','ue']#,'ht','trigeff','toppt','tau32','jmst','jmrt','tau21','jmsW','jmrW','tau21pt'] #

catList = ['is'+item[0]+'_nHOT'+item[1]+'_nT'+item[2]+'_nW'+item[3]+'_nB'+item[4]+'_nJ'+item[5] for item in list(itertools.product(isEMlist,nhottlist,nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip_75cats(item)]
RFile = rt.TFile(templateFile)
if useCombine:
	upTag = 'Up'
	downTag = 'Down'
else: #theta
	upTag = '__plus'
	downTag = '__minus'
	
for syst in systematics:
	Prefix = iPlot+'_'+lumiStr+'_'+catList[0]+'__'+bkgList[0]
	print Prefix+'__'+syst
	hNm = RFile.Get(Prefix).Clone()
	try:
		hUp = RFile.Get(Prefix+'__'+syst+upTag).Clone()
		hDn = RFile.Get(Prefix+'__'+syst+downTag).Clone()
	except:
		print "No shape for",bkgList[0],cat,syst
		hUp = RFile.Get(Prefix).Clone()
		hDn = RFile.Get(Prefix).Clone()
	for cat in catList:
		for bkg in bkgList:
			if bkg==bkgList[0] and cat==catList[0]: continue
			try: 
				htemp = RFile.Get(Prefix.replace(bkgList[0],bkg).replace(catList[0],cat)).Clone()
				hNm.Add(htemp)
			except: 
				print "No nominal for",bkg,cat,syst
				pass
				
			try:
				htempUp = RFile.Get(Prefix.replace(bkgList[0],bkg).replace(catList[0],cat)+'__'+syst+upTag).Clone()
				hUp.Add(htempUp)
			except:
				print "No shape for",bkg,cat,syst
				try:
					htempUp = RFile.Get(Prefix.replace(bkgList[0],bkg).replace(catList[0],cat)).Clone()
					hUp.Add(htempUp)
				except: 
					print "No nominal for",bkg,cat,syst
					pass
		
			try:
				htempDown = RFile.Get(Prefix.replace(bkgList[0],bkg).replace(catList[0],cat)+'__'+syst+downTag).Clone()
				hDn.Add(htempDown)
			except:
				print "No shape for",bkg,cat,syst
				try:
					htempDown = RFile.Get(Prefix.replace(bkgList[0],bkg).replace(catList[0],cat)).Clone()
					hDn.Add(htempDown)
				except: 
					print "No nominal for",bkg,cat,syst
					pass
	hNm.Draw()
	hUp.Draw()
	hDn.Draw()

	canv = rt.TCanvas(syst,syst,1000,700)
	yDiv = 0.35
	uPad=rt.TPad('uPad','',0,yDiv,1,1)
	uPad.SetTopMargin(0.07)
	uPad.SetBottomMargin(0)
	uPad.SetRightMargin(.05)
	uPad.SetLeftMargin(.18)
	uPad.Draw()

	lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner
	lPad.SetTopMargin(0)
	lPad.SetBottomMargin(.4)
	lPad.SetRightMargin(.05)
	lPad.SetLeftMargin(.18)
	lPad.SetGridy()
	lPad.Draw()

	uPad.cd()

	rt.gStyle.SetOptTitle(0)

	hNm.SetFillColor(rt.kWhite)
	hUp.SetFillColor(rt.kWhite)
	hDn.SetFillColor(rt.kWhite)
	hNm.SetMarkerColor(rt.kBlack)
	hUp.SetMarkerColor(rt.kRed)
	hDn.SetMarkerColor(rt.kBlue)
	hNm.SetLineColor(rt.kBlack)
	hUp.SetLineColor(rt.kRed)
	hDn.SetLineColor(rt.kBlue)
	hNm.SetLineWidth(2)
	hNm.SetLineStyle(1)
	hUp.SetLineWidth(2)
	hUp.SetLineStyle(1)
	hDn.SetLineWidth(2)
	hDn.SetLineStyle(1)
	hNm.SetMarkerSize(.05)
	hUp.SetMarkerSize(.05)
	hDn.SetMarkerSize(.05)

	hUp.GetYaxis().SetTitle('Events')
	hUp.GetYaxis().SetLabelSize(0.10)
	hUp.GetYaxis().SetTitleSize(0.1)
	hUp.GetYaxis().SetTitleOffset(.6)

	hUp.GetYaxis().SetRangeUser(0.0001,1.1*max(hUp.GetMaximum(),hNm.GetMaximum(),hDn.GetMaximum()))
	
	hUp.Draw()
	hNm.Draw('same')
	hDn.Draw('same')

	lPad.cd()
	rt.gStyle.SetOptTitle(0)
	pullUp = hUp.Clone()
	for iBin in range(0,pullUp.GetXaxis().GetNbins()+2):
		pullUp.SetBinContent(iBin,pullUp.GetBinContent(iBin)-hNm.GetBinContent(iBin))
		pullUp.SetBinError(iBin,math.sqrt(pullUp.GetBinError(iBin)**2+hNm.GetBinError(iBin)**2))
	pullUp.Divide(hNm)
	pullUp.SetTitle('')
	pullUp.SetFillColor(2)
	pullUp.SetLineColor(2)

	pullUp.GetXaxis().SetLabelSize(.15)
	pullUp.GetXaxis().SetTitleSize(0.18)
	pullUp.GetXaxis().SetTitleOffset(0.95)

	pullUp.GetYaxis().SetTitle('#frac{Up/Down-Nom}{Nom}')#'Python-C++'
	pullUp.GetYaxis().CenterTitle(1)
	pullUp.GetYaxis().SetLabelSize(0.125)
	pullUp.GetYaxis().SetTitleSize(0.1)
	pullUp.GetYaxis().SetTitleOffset(.55)
	pullUp.GetYaxis().SetNdivisions(506)

	pullDown = hDn.Clone()
	for iBin in range(0,pullDown.GetXaxis().GetNbins()+2):
		pullDown.SetBinContent(iBin,pullDown.GetBinContent(iBin)-hNm.GetBinContent(iBin))
		pullDown.SetBinError(iBin,math.sqrt(pullDown.GetBinError(iBin)**2+hNm.GetBinError(iBin)**2))
	pullDown.Divide(hNm)
	pullDown.SetTitle('')
	pullDown.SetFillColor(4)
	pullDown.SetLineColor(4)

	pullDown.GetXaxis().SetLabelSize(.15)
	pullDown.GetXaxis().SetTitleSize(0.18)
	pullDown.GetXaxis().SetTitleOffset(0.95)

	pullDown.GetYaxis().SetTitle('#frac{Up/Down-Nom}{Nom}')#'Python-C++'
	pullDown.GetYaxis().CenterTitle(1)
	pullDown.GetYaxis().SetLabelSize(0.125)
	pullDown.GetYaxis().SetTitleSize(0.1)
	pullDown.GetYaxis().SetTitleOffset(.55)
	pullDown.GetYaxis().SetNdivisions(506)
	pullUp.SetMinimum(-0.5)#-1.4)#min(pullDown.GetMinimum(),pullUp.GetMinimum()))
	pullUp.SetMaximum(0.5)#1.4)#max(pullDown.GetMaximum(),pullUp.GetMaximum()))
	pullUp.Draw()
	pullDown.Draw('same')
	lPad.RedrawAxis()

	uPad.cd()

	legend = rt.TLegend(0.6,0.65,0.9,0.90)
	legend.SetShadowColor(0);
	legend.SetFillColor(0);
	legend.SetLineColor(0);
	legend.AddEntry(hNm,'Nominal','l')
	legend.AddEntry(hUp,syst.replace('topsf','t tag').replace('muRFcorrdNew','muRF').replace('muRFdecorrdNew','muRF').replace('muRFcorrd','muRF').replace('muRFenv','muRF').replace('pdfNew','PDF').replace('toppt','Top Pt').replace('jsf','JSF').replace('jec','JEC').replace('q2','Q^{2}').replace('miniiso','miniIso').replace('pileup','Pileup').replace('jer','JER').replace('btag','b tag').replace('pdf','PDF').replace('jmr','JMR').replace('jms','JMS').replace('tau21','#tau_{2}/#tau_{1}')+' Up','l')
	legend.AddEntry(hDn,syst.replace('topsf','t tag').replace('muRFcorrdNew','muRF').replace('muRFdecorrdNew','muRF').replace('muRFcorrd','muRF').replace('muRFenv','muRF').replace('pdfNew','PDF').replace('toppt','Top Pt').replace('jsf','JSF').replace('jec','JEC').replace('q2','Q^{2}').replace('miniiso','miniIso').replace('pileup','Pileup').replace('jer','JER').replace('btag','b tag').replace('pdf','PDF').replace('jmr','JMR').replace('jms','JMS').replace('tau21','#tau_{2}/#tau_{1}')+' Down','l')
	legend.Draw('same')
	
	prelimTex=rt.TLatex()
	prelimTex.SetNDC()
	prelimTex.SetTextAlign(31) # align right
	prelimTex.SetTextFont(42)
	prelimTex.SetTextSize(0.05)
	prelimTex.SetLineWidth(2)
	prelimTex.DrawLatex(0.90,0.943,str(lumi)+" fb^{-1} (13 TeV)")

	prelimTex2=rt.TLatex()
	prelimTex2.SetNDC()
	prelimTex2.SetTextFont(61)
	prelimTex2.SetLineWidth(2)
	prelimTex2.SetTextSize(0.07)
	prelimTex2.DrawLatex(0.18,0.9364,"CMS")

	prelimTex3=rt.TLatex()
	prelimTex3.SetNDC()
	prelimTex3.SetTextAlign(13)
	prelimTex3.SetTextFont(52)
	prelimTex3.SetTextSize(0.040)
	prelimTex3.SetLineWidth(2)
	prelimTex3.DrawLatex(0.25175,0.9664,"Preliminary")

	canv.SaveAs(tempVersion+'/bkgs/'+syst+saveKey+'.pdf')
	canv.SaveAs(tempVersion+'/bkgs/'+syst+saveKey+'.png')
	#canv.SaveAs(tempVersion+'/bkgs/'+syst+saveKey+'.eps')
RFile.Close()
