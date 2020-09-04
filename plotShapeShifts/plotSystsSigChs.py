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
tempVersion = 'templates_'+year+'_njet_2020_8_17/'
cutString = ''
if useCombine: templateFile = '../makeTemplates/'+tempVersion+'/'+cutString+'/templates_'+iPlot+'_'+lumiStr+isRebinned+'.root'
else: templateFile = '../makeTemplates/'+tempVersion+'/'+cutString+'/templates_'+iPlot+'_'+sig1+'_'+lumiStr+isRebinned+'.root'
if not os.path.exists(outDir+tempVersion): os.system('mkdir '+outDir+tempVersion)
if not os.path.exists(outDir+tempVersion+'/signalIndChannels'): os.system('mkdir '+outDir+tempVersion+'/signalIndChannels')

isEMlist  = ['E','M']
nhottlist = ['0','1p']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['2','3','4p']
njetslist = ['6','7','8','9','10p']
# nbtaglist = ['2p']
# njetslist = ['6p']
systematics = ['pileup','prefire','btag','mistag','jec','jer','hotstat','hotcspur','hotclosure','PSwgt','muRF','pdf']#,'hdamp','ue','ht','trigeff','toppt','tau32','jmst','jmrt','tau21','jmsW','jmrW','tau21pt'] #

signameList = ['tttt']

catList = ['is'+item[0]+'_nHOT'+item[1]+'_nT'+item[2]+'_nW'+item[3]+'_nB'+item[4]+'_nJ'+item[5] for item in list(itertools.product(isEMlist,nhottlist,nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip(item)]
if useCombine:
	upTag = 'Up'
	downTag = 'Down'
else: #theta
	upTag = '__plus'
	downTag = '__minus'
	
for signal in signameList:
	RFile = rt.TFile(templateFile.replace(signameList[0],signal))
	for syst in systematics:
		if not os.path.exists(outDir+tempVersion+'/signalIndChannels/'+syst): os.system('mkdir '+outDir+tempVersion+'/signalIndChannels/'+syst)
		for cat in catList:
			if (syst=='q2' or syst=='toppt'):
				print "Do you expect to have "+syst+" for your signal? FIX ME IF SO! I'll skip this systematic"
				continue
			if useCombine: Prefix = iPlot+'_'+lumiStr+'_'+cat+'__'+signal
			else: Prefix = iPlot+'_'+lumiStr+'_'+cat+'__sig'
			print Prefix+'__'+syst
			hNm = RFile.Get(Prefix).Clone()
			hUp = RFile.Get(Prefix+'__'+syst+upTag).Clone()
			hDn = RFile.Get(Prefix+'__'+syst+downTag).Clone()
			hNm.Draw()
			hUp.Draw()
			hDn.Draw()

			canv = rt.TCanvas(Prefix+'__'+syst,Prefix+'__'+syst,1000,700)
			yDiv = 0.35
			uPad=rt.TPad('uPad','',0,yDiv,1,1)
			uPad.SetTopMargin(0.07)
			uPad.SetBottomMargin(0)
			uPad.SetRightMargin(.05)
			uPad.SetLeftMargin(.18)
			#uPad.SetLogy()
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

			#canv.SetLogy()
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

			#hUp.SetMaximum(1.1*max(hUp.GetMaximum(),hNm.GetMaximum(),hDn.GetMaximum()))
			hUp.GetYaxis().SetRangeUser(0.0001,1.1*max(hUp.GetMaximum(),hNm.GetMaximum(),hDn.GetMaximum()))

# 			hUp.Draw()
# 			hNm.Draw('same')
# 			hDn.Draw('same')
			hUp.Draw('hist')
			hNm.Draw('samehist')
			hDn.Draw('samehist')
			#uPad.RedrawAxis()

			lPad.cd()
			rt.gStyle.SetOptTitle(0)
			pullUp = hUp.Clone()
			for iBin in range(0,pullUp.GetXaxis().GetNbins()+2):
				pullUp.SetBinContent(iBin,pullUp.GetBinContent(iBin)-hNm.GetBinContent(iBin))
				pullUp.SetBinError(iBin,math.sqrt(pullUp.GetBinError(iBin)**2+hNm.GetBinError(iBin)**2))
			pullUp.Divide(hNm)
			pullUp.SetTitle('')
			pullUp.SetFillColor(rt.kWhite)
			pullUp.SetLineColor(rt.kRed)

			#pullUp.GetXaxis().SetTitle(histName)
			pullUp.GetXaxis().SetLabelSize(.15)
			pullUp.GetXaxis().SetTitleSize(0.18)
			pullUp.GetXaxis().SetTitleOffset(0.95)

			pullUp.GetYaxis().SetTitle('#frac{Up/Down-Nom}{Nom}')#'Python-C++'
			pullUp.GetYaxis().CenterTitle(1)
			pullUp.GetYaxis().SetLabelSize(0.125)
			pullUp.GetYaxis().SetTitleSize(0.1)
			pullUp.GetYaxis().SetTitleOffset(.55)
			pullUp.GetYaxis().SetNdivisions(506)
			#pullUp.SetMinimum(pullDown.GetMinimum())
			#pullUp.SetMaximum(pullUp.GetMaximum())

			pullDown = hDn.Clone()
			for iBin in range(0,pullDown.GetXaxis().GetNbins()+2):
				pullDown.SetBinContent(iBin,pullDown.GetBinContent(iBin)-hNm.GetBinContent(iBin))
				pullDown.SetBinError(iBin,math.sqrt(pullDown.GetBinError(iBin)**2+hNm.GetBinError(iBin)**2))
			pullDown.Divide(hNm)
			pullDown.SetTitle('')
			pullDown.SetFillColor(rt.kWhite)
			pullDown.SetLineColor(rt.kBlue)

			#pullDown.GetXaxis().SetTitle(histName)
			pullDown.GetXaxis().SetLabelSize(.15)
			pullDown.GetXaxis().SetTitleSize(0.18)
			pullDown.GetXaxis().SetTitleOffset(0.95)

			pullDown.GetYaxis().SetTitle('#frac{Up/Down-Nom}{Nom}')#'Python-C++'
			pullDown.GetYaxis().CenterTitle(1)
			pullDown.GetYaxis().SetLabelSize(0.125)
			pullDown.GetYaxis().SetTitleSize(0.1)
			pullDown.GetYaxis().SetTitleOffset(.55)
			pullDown.GetYaxis().SetNdivisions(506)
			pullUp.SetMinimum(-1.4)#min(pullDown.GetMinimum(),pullUp.GetMinimum()))
			pullUp.SetMaximum(1.4)#max(pullDown.GetMaximum(),pullUp.GetMaximum()))
			#pullDown.SetMinimum(pullDown.GetMinimum())
			#pullDown.SetMaximum(pullDown.GetMaximum())
# 			pullUp.Draw()
# 			pullDown.Draw('same')
			pullUp.Draw('hist')
			pullDown.Draw('samehist')
			lPad.RedrawAxis()

			uPad.cd()

			legend = rt.TLegend(0.7,0.65,0.9,0.90)
			legend.SetShadowColor(0);
			legend.SetFillColor(0);
			legend.SetLineColor(0);
			legend.AddEntry(hNm,signal,'l')
			legend.AddEntry(hUp,syst.replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Up','l')
			legend.AddEntry(hDn,syst.replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Down','l')

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

			chLatex = rt.TLatex()
			chLatex.SetNDC()
			chLatex.SetTextSize(0.05)
			chLatex.SetTextAlign(21)
			flv = cat.split('_')[0]
			hottag = cat.split('_')[1]
			ttag = cat.split('_')[2]
			wtag = cat.split('_')[3]
			btag = cat.split('_')[4]
			njet = cat.split('_')[5]
			flvString = ''
			tagString = ''
			tagString2 = ''
			if flv=='isE': flvString+='e+jets'
			if flv=='isM': flvString+='#mu+jets'
			if hottag!='0p': 
				if 'p' in hottag: tagString2+='#geq'+hottag[4:-1]+' resolved t'
				else: tagString2+=hottag[4:]+' resolved t'
			if ttag!='0p': 
				if 'p' in ttag: tagString+='#geq'+ttag[2:-1]+' t, '
				else: tagString+=ttag[2:]+' t, '
			if wtag!='0p': 
				if 'p' in wtag: tagString+='#geq'+wtag[2:-1]+' W, '
				else: tagString+=wtag[2:]+' W, '
			if btag!='0p': 
				if 'p' in btag: tagString+='#geq'+btag[2:-1]+' b, '
				else: tagString+=btag[2:]+' b, '
			if njet!='0p': 
				if 'p' in njet: tagString+='#geq'+njet[2:-1]+' j'
				else: tagString+=njet[2:]+' j'
			if tagString.endswith(', '): tagString = tagString[:-2]
			chLatex.DrawLatex(0.45, 0.84, flvString)
			chLatex.DrawLatex(0.45, 0.78, tagString)
			chLatex.DrawLatex(0.45, 0.72, tagString2)
		
			canv.SaveAs(tempVersion+'/signalIndChannels/'+syst+'/'+syst+'_'+signal+'_'+cat+'.pdf')
			canv.SaveAs(tempVersion+'/signalIndChannels/'+syst+'/'+syst+'_'+signal+'_'+cat+'.png')
			#canv.SaveAs(tempVersion+'/signalIndChannels/'+syst+'/'+syst+'_'+signal+'_'+cat+'.eps')
	RFile.Close()
