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
year = 'R17'
if year=='R17':
	lumiStr = '41p53fb'
	lumi=41.5 #for plots
else:
	lumiStr = '59p97fb'
	lumi=59.97 #for plots
sig1 = 'tttt' #  choose the 1st signal to plot
useCombine = True
tempVersion = 'templates_'+year+'_redJECs_2020_12_5'
isRebinned = '_smooth_rebinned_stat0p3'
if 'kinematics' in tempVersion: isRebinned = '_rebinned_stat1p1'
cutString = ''
saveDir = ''
if useCombine: templateFile = '../makeTemplates/'+tempVersion+'/'+cutString+'/templates_'+iPlot+'_'+lumiStr+isRebinned+'.root'
else: templateFile = '../makeTemplates/'+tempVersion+'/'+cutString+'/templates_'+iPlot+'_'+sig1+'_'+lumiStr+isRebinned+'.root'
if not os.path.exists(outDir+tempVersion): os.system('mkdir '+outDir+tempVersion)
if not os.path.exists(outDir+tempVersion+'/'+saveDir): os.system('mkdir '+outDir+tempVersion+'/'+saveDir)

bkgTTBarList = ['ttnobb','ttbb'] #['ttjj','ttcc','ttbb','ttbj']
procList = bkgTTBarList+['top','ewk','qcd']
procList+= [sig1]
isEMlist  = ['E','M']
nhottlist = ['0','1p']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['2','3','4p']
njetslist = ['6','7','8','9','10p']
if 'kinematics' in tempVersion:
	nhottlist = ['0p']
	nbtaglist = ['2p']
	njetslist = ['4p']
systematics = ['pileup','btag','mistag','hotstat','hotcspur','hotclosure','isr','fsr','PSwgt','muRF','pdf']#,'hdamp','ue','njet','njetsf','ht','trigeff','toppt','tau32','jmst','jmrt','tau21','jmsW','jmrW','tau21pt']
if year=='R17': systematics += ['prefire']
# if year=='R18': systematics += ['hem']
systematics+= ['JEC','JER']#,
# 'JEC_Total','JEC_FlavorQCD',
# 'JEC_RelativeBal','JEC_RelativeSample_'+year.replace('R','20'),
# 'JEC_Absolute','JEC_Absolute_'+year.replace('R','20'),
# 'JEC_HF','JEC_HF_'+year.replace('R','20'),
# 'JEC_EC2','JEC_EC2_'+year.replace('R','20'),
# 'JEC_BBEC1','JEC_BBEC1_'+year.replace('R','20')]

catList = ['is'+item[0]+'_nHOT'+item[1]+'_nT'+item[2]+'_nW'+item[3]+'_nB'+item[4]+'_nJ'+item[5] for item in list(itertools.product(isEMlist,nhottlist,nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip(item)]
RFile = rt.TFile(templateFile)
if useCombine:
	upTag = 'Up'
	downTag = 'Down'
else: #theta
	upTag = '__plus'
	downTag = '__minus'

nBinsBkg = 0
for cat in catList:
	if 'isE' not in cat: continue
	Prefix = iPlot+'_'+lumiStr+'_'+cat+'__'+procList[0]
	print Prefix
	nBinsBkg += RFile.Get(Prefix).GetNbinsX()

for syst in systematics:
	if not os.path.exists(outDir+tempVersion+'/'+saveDir+'/'+syst): os.system('mkdir '+outDir+tempVersion+'/'+saveDir+'/'+syst)
	for bkg in procList:
		for em in isEMlist:
			grinCombUp = rt.TGraphErrors()
			grinCombDn = rt.TGraphErrors()
			groutCombUp = rt.TGraphErrors()
			groutCombDn = rt.TGraphErrors()
			ipoint = 0
			for cat in catList:
				if 'is'+em not in cat: continue
				Prefix = iPlot+'_'+lumiStr+'_'+cat+'__'+bkg
				print Prefix+'__'+syst
				grinUp = rt.TGraphErrors()
				grinDn = rt.TGraphErrors()
				groutUp = rt.TGraphErrors()
				groutDn = rt.TGraphErrors()
				gsUp = rt.TGraphSmooth(Prefix+'_up_lowess')
				gsDn = rt.TGraphSmooth(Prefix+'_dn_lowess')
				try: hNm = RFile.Get(Prefix).Clone(Prefix+'_nom')
				except: 
					print 'There is no '+Prefix+'. Skipping ...'
					continue
				hUp = RFile.Get(Prefix+'__'+syst+upTag).Clone(Prefix+'_up')
				hDn = RFile.Get(Prefix+'__'+syst+downTag).Clone(Prefix+'_dn')
				hsUp = RFile.Get(Prefix+'__lowess'+syst+upTag).Clone(Prefix+'_up')
				hsDn = RFile.Get(Prefix+'__lowess'+syst+downTag).Clone(Prefix+'_dn')
				hUp.Divide(hNm)
				hDn.Divide(hNm)
				hsUp.Divide(hNm)
				hsDn.Divide(hNm)
				for ibin in range(1,hNm.GetNbinsX()+1):
					p = ibin-1
					x = (hUp.GetBinLowEdge(ibin)+hUp.GetBinLowEdge(ibin+1))/2
					yup = hUp.GetBinContent(ibin)
					ydn = hDn.GetBinContent(ibin)
					grinUp.SetPoint(p, x, 1+(yup-ydn)/2)
					grinDn.SetPoint(p, x, 1-(yup-ydn)/2)
					ysup = hsUp.GetBinContent(ibin)
					ysdn = hsDn.GetBinContent(ibin)
					if ysup!=0: groutUp.SetPoint(p, x, ysup)
					else: groutUp.SetPoint(p, x, 1)
					if ysdn!=0: groutDn.SetPoint(p, x, ysdn)
					else: groutDn.SetPoint(p, x, 1)
				
				for ibin in range(len(grinUp.GetY())):
					grinCombUp.SetPoint(ipoint+ibin, ipoint+ibin, grinUp.GetY()[ibin])
					grinCombDn.SetPoint(ipoint+ibin, ipoint+ibin, grinDn.GetY()[ibin])
					groutCombUp.SetPoint(ipoint+ibin, ipoint+ibin, groutUp.GetY()[ibin])
					groutCombDn.SetPoint(ipoint+ibin, ipoint+ibin, groutDn.GetY()[ibin])
				if len(catList)==2:
					grinCombUp = grinUp
					grinCombDn = grinDn
					groutCombUp = groutUp
					groutCombDn = groutDn
				ipoint += hNm.GetNbinsX()				

			grinCombUp.SetLineColor(2)                            
			grinCombDn.SetLineColor(4)                            
			grinCombUp.SetMarkerColor(2)                            
			grinCombDn.SetMarkerColor(4)                            
			grinCombUp.SetMarkerSize(0.8)                            
			grinCombDn.SetMarkerSize(0.8)                            
			grinCombUp.SetMarkerStyle(8)                            
			grinCombDn.SetMarkerStyle(8)                            
			grinCombUp.SetLineStyle(2)                            
			grinCombDn.SetLineStyle(2)                            
			grinCombUp.SetLineWidth(2)                            
			grinCombDn.SetLineWidth(2)
									
			groutCombUp.SetLineColor(2)
			groutCombDn.SetLineColor(4)
			groutCombUp.SetLineWidth(4)
			groutCombDn.SetLineWidth(4)
			groutCombUp.SetMarkerStyle(1)
			groutCombDn.SetMarkerStyle(1)
		
			canv = rt.TCanvas(Prefix+'__'+syst,Prefix+'__'+syst,1000,700)
			rt.gStyle.SetOptTitle(0)
			canv.SetTopMargin(0.08)
			canv.SetBottomMargin(0.12)
			canv.SetRightMargin(.035)
			canv.SetLeftMargin(.12)

			mg = rt.TMultiGraph()
			mg.Add(grinCombUp)
			mg.Add(grinCombDn)
			mg.Add(groutCombUp)
			mg.Add(groutCombDn)

			mg.Draw("ALXP")

			legend = rt.TLegend(0.15,0.65,0.45,0.90)
			legend.SetShadowColor(0);
			legend.SetFillStyle(0);
			legend.SetFillColor(0);
			legend.SetLineColor(0);
			legend.SetTextSize(0.04);
			legend.AddEntry(grinCombUp,bkg+'_'+syst.replace('hem','HEM15/16').replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Up','l')
			legend.AddEntry(grinCombDn,bkg+'_'+syst.replace('hem','HEM15/16').replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Down','l')
			legend.AddEntry(groutCombUp,bkg+'_'+syst.replace('hem','HEM15/16').replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Up (Lowess)','l')
			legend.AddEntry(groutCombDn,bkg+'_'+syst.replace('hem','HEM15/16').replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Down (Lowess)','l')

			legend.Draw('same')

			prelimTex=rt.TLatex()
			prelimTex.SetNDC()
			prelimTex.SetTextAlign(31) # align right
			prelimTex.SetTextFont(42)
			prelimTex.SetTextSize(0.07)
			prelimTex.SetLineWidth(2)
			prelimTex.DrawLatex(0.97,0.94,str(lumi)+" fb^{-1} (13 TeV)")
		
			chLatex = rt.TLatex()
			chLatex.SetNDC()
			chLatex.SetTextSize(0.04)
			chLatex.SetTextAlign(21)
			if em=='E': flvString='e+jets'
			if em=='M': flvString='#mu+jets'
			chLatex.DrawLatex(0.3, 0.34, flvString)

			#mg.GetXaxis().SetRange(-2,2)
			mg.SetMinimum(max([0.,mg.GetHistogram().GetMinimum()]))
			mg.SetMaximum(min([2.,mg.GetHistogram().GetMaximum()]))
			mg.GetXaxis().SetTitle("Bin #")
			mg.GetYaxis().SetTitleOffset(1.)
			mg.GetYaxis().SetTitle("Ratio to nominal")
			
			canv.Modified();
			canv.Update();
			
			canv.SaveAs(tempVersion+'/'+saveDir+'/'+syst+'/'+syst+'_'+bkg+'_'+em+'.png')
RFile.Close()
