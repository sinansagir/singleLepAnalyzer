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
year = 'R16'
if year=='R16':
	lumiStr = '35p867fb'
	lumi=35.9 #for plots
elif year=='R17':
	lumiStr = '41p53fb'
	lumi=41.5 #for plots
elif year=='R18':
	lumiStr = '59p97fb'
	lumi=59.97 #for plots
sig1 = 'tttt' #  choose the 1st signal to plot
smoothingAlgo = 'lowess' #lowess, super, or kern
symmetrizeSmoothing = True #Symmetrize up/down shifts around nominal before smoothing
useCombine = True
tempVersion = 'templates_'+year+'_2021_4_6'
isRebinned = '_2b250GeV3b150GeV4b50GeVbins_rebinned_stat0p3'
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
procList = ['ttbb']
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
systematics = ['JEC']
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

for syst in systematics:
	if not os.path.exists(outDir+tempVersion+'/'+saveDir+'/'+syst): os.system('mkdir '+outDir+tempVersion+'/'+saveDir+'/'+syst)
	for bkg in procList:
		for cat in catList:
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
			hUp.Divide(hNm)
			hDn.Divide(hNm)
			for ibin in range(1,hNm.GetNbinsX()+1):
				p = ibin-1
				x = (hUp.GetBinLowEdge(ibin)+hUp.GetBinLowEdge(ibin+1))/2
				yup = hUp.GetBinContent(ibin)
				ydn = hDn.GetBinContent(ibin)
				if symmetrizeSmoothing:
					grinUp.SetPoint(p, x, 1+(yup-ydn)/2)
					grinDn.SetPoint(p, x, 1-(yup-ydn)/2)
				else:
					grinUp.SetPoint(p, x, yup)
					grinDn.SetPoint(p, x, ydn)
			if smoothingAlgo=='super':
				groutUp = gsUp.SmoothSuper(grinUp,"",9,0)
				groutDn = gsDn.SmoothSuper(grinDn,"",9,0)
			elif smoothingAlgo=='kern':
				groutUp = gsUp.SmoothKern(grinUp,"normal",5.0)
				groutDn = gsDn.SmoothKern(grinDn,"normal",5.0)
			else:
				groutUp = gsUp.SmoothLowess(grinUp,"",1.0)
				groutDn = gsDn.SmoothLowess(grinDn,"",1.0)

			grinUp.SetLineColor(2)                            
			grinDn.SetLineColor(4)                            
			grinUp.SetMarkerColor(2)                            
			grinDn.SetMarkerColor(4)                            
			grinUp.SetMarkerSize(1.)                            
			grinDn.SetMarkerSize(1.)                            
			grinUp.SetMarkerStyle(8)                            
			grinDn.SetMarkerStyle(8)                            
			grinUp.SetLineStyle(5)                            
			grinDn.SetLineStyle(5)                            
			grinUp.SetLineWidth(2)                            
			grinDn.SetLineWidth(2)
			                            
			groutUp.SetLineColor(2)
			groutDn.SetLineColor(4)
			groutUp.SetLineWidth(4)
			groutDn.SetLineWidth(4)
			groutUp.SetMarkerStyle(1)
			groutDn.SetMarkerStyle(1)
			
			canv = rt.TCanvas(Prefix+'__'+syst,Prefix+'__'+syst,1000,700)
			rt.gStyle.SetOptTitle(0)
			canv.SetTopMargin(0.08)
			canv.SetBottomMargin(0.12)
			canv.SetRightMargin(.035)
			canv.SetLeftMargin(.12)
			
			mg = rt.TMultiGraph()
			mg.Add(grinUp)
			mg.Add(grinDn)
			mg.Add(groutUp)
			mg.Add(groutDn)

			mg.Draw("ALXP")

			legend = rt.TLegend(0.15,0.65,0.45,0.90)
			legend.SetShadowColor(0);
			legend.SetFillStyle(0);
			legend.SetFillColor(0);
			legend.SetLineColor(0);
			legend.SetTextSize(0.04);
			legend.AddEntry(grinUp,bkg+'_'+syst.replace('hem','HEM15/16').replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Up','l')
			legend.AddEntry(grinDn,bkg+'_'+syst.replace('hem','HEM15/16').replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Down','l')
			legend.AddEntry(groutUp,bkg+'_'+syst.replace('hem','HEM15/16').replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Up (Lowess)','l')
			legend.AddEntry(groutDn,bkg+'_'+syst.replace('hem','HEM15/16').replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Down (Lowess)','l')

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
			flv = cat.split('_')[0]
			hottag = cat.split('_')[1].replace('nHOT','')
			ttag = cat.split('_')[2].replace('nT','')
			wtag = cat.split('_')[3].replace('nW','')
			btag = cat.split('_')[4].replace('nB','')
			njet = cat.split('_')[5].replace('nJ','')
			flvString = ''
			tagString = ''
			tagString2 = ''
			if flv=='isE': flvString+='e+jets'
			if flv=='isM': flvString+='#mu+jets'
			if hottag!='0p': 
				if 'p' in hottag: tagString2+='#geq'+hottag[:-1]+' resolved t'
				else: tagString2+=hottag+' resolved t'
			if ttag!='0p': 
				if 'p' in ttag: tagString+='#geq'+ttag[:-1]+' t, '
				else: tagString+=ttag+' t, '
			if wtag!='0p': 
				if 'p' in wtag: tagString+='#geq'+wtag[:-1]+' W, '
				else: tagString+=wtag+' W, '
			if btag!='0p': 
				if 'p' in btag: tagString+='#geq'+btag[:-1]+' b, '
				else: tagString+=btag+' b, '
			if njet!='0p': 
				if 'p' in njet: tagString+='#geq'+njet[:-1]+' j'
				else: tagString+=njet+' j'
			if tagString.endswith(', '): tagString = tagString[:-2]
			chLatex.DrawLatex(0.3, 0.34, flvString)
			chLatex.DrawLatex(0.3, 0.28, tagString)
			chLatex.DrawLatex(0.3, 0.22, tagString2)
			
			#mg.GetXaxis().SetRange(-2,2)
			mg.SetMinimum(max([0.,mg.GetHistogram().GetMinimum()]))
			mg.SetMaximum(min([2.,mg.GetHistogram().GetMaximum()]))
			mg.GetXaxis().SetTitle("H_{T} [GeV]")
			mg.GetYaxis().SetTitleOffset(1.)
			mg.GetYaxis().SetTitle("Ratio to nominal")
			
			canv.Modified();
			canv.Update();

			pfix = ''
			if symmetrizeSmoothing: pfix+='_symmetrized'
			canv.SaveAs(tempVersion+'/'+saveDir+'/'+syst+'/'+syst+'_'+cat+'_'+bkg+'_'+smoothingAlgo+pfix+'.png')

RFile.Close()
