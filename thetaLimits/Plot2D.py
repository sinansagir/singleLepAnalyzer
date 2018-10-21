#!/usr/bin/python

import os,sys
from ROOT import *
from pal import *

gROOT.SetBatch(1)

saveKey = 'test'
isBkgOnly = False

lumiPlot = '35.9'
lumiStr = '35p867'
spin='left'#'right'
discriminant='minMlb'
saveKey+=discriminant
histPrefix=discriminant+'_'+str(lumiStr)+'fb'+spin
stat='0p3'
cat=str(sys.argv[1])#'_isE_nT0p_nW0p_nB2p'
saveKey=cat
isRebinned='_rebinned_stat'+str(stat).replace('.','p')
if isBkgOnly: isRebinned+='_bkgonly'
tempKey='postfit_test/noMnT1pnW1pnB2p'
limitDir='templates_M17WtSF_2017_3_31_SRpCRplots/'+tempKey+'/'
LH700file='/mle_covcorr_templates_'+discriminant+'_X53X53M900'+spin+'_'+str(lumiStr)+'fb'+isRebinned+cat+'.root'

nuisNamPlot = {
		   'pdfNew':'PDF',
		   'topmuRFcorrdNew':'muRF(TOP)',
		   'ewkmuRFcorrdNew':'muRF(EWK)',
		   'qcdmuRFcorrdNew':'muRF(QCD)',
		   'qcdScale':'muRF(QCD)',
		   'sigmuRFcorrdNew':'muRF(LH-900GeV)',
		   'muRFcorrdNew':'muRF',
		   'toppt':'top p_{T}',
		   'tau21':'#tau_{2}/#tau_{1}',
		   'jms':'JMS',
		   'jmr':'JMR',
		   'taupt':'#tau_{2}/#tau_{1} p_{T}',
		   'topsf':'t-tag',
		   'btag':'b/c-tag',
		   'mistag':'udsg-mistag',
		   'jer':'JER',
		   'jec':'JEC',
		   'pileup':'pileup',
		   'eltrigeff':'elTrig',
		   'mutrigeff':'muTrig',
		   'ht':'HT',
		   'muIsoSys':'muIso',
		   'elIsoSys':'elIso',
		   'muIdSys':'muId',
		   'elIdSys':'elId',
		   'lumiSys':'lumi',
		   'beta_signal':'beta_signal',
		   }
		   
RFile = TFile(limitDir+LH700file)
hist = RFile.Get('correlation_matrix').Clone()
# hist.GetXaxis().SetRangeUser(0, 2.5)
# for ybin in range(1,8): 
# 	hist.SetBinContent(3,ybin,1,-1)
# 	hist.SetBinContent(8,ybin,1,-1)

for ibin in range(1,hist.GetXaxis().GetNbins()+1): 
	label = hist.GetXaxis().GetBinLabel(ibin)
	hist.GetXaxis().SetBinLabel(ibin,nuisNamPlot[label])
	hist.GetYaxis().SetBinLabel(ibin,nuisNamPlot[label])

gStyle.SetOptStat(0)
gStyle.SetPaintTextFormat("1.2f");
canv = TCanvas("canv","canv",1200,800)
#canv.SetLogy()
#canv.SetTopMargin(0.10)
canv.SetBottomMargin(0.12)
canv.SetRightMargin(0.12)
canv.SetLeftMargin(.16)

#gStyle.SetPalette(57)
set_palette(name="kBird")
hist.Draw("COLZ TEXT")
canv.SaveAs(limitDir.replace(tempKey,'')+'/correlation_matrix'+isRebinned+saveKey+'.png')
canv.SaveAs(limitDir.replace(tempKey,'')+'/correlation_matrix'+isRebinned+saveKey+'.pdf')
canv.SaveAs(limitDir.replace(tempKey,'')+'/correlation_matrix'+isRebinned+saveKey+'.eps')
RFile.Close()

