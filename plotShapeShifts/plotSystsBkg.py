import ROOT as R
import os,sys,math
from array import array

from tdrStyle import *
setTDRStyle()
R.gROOT.SetBatch(1)
outDir = os.getcwd()+'/'

lumi = 2.3
discriminant = 'minMlb'
rfilePostFix = '_modified'
tempVersion = 'templates_minMlb_ObjRev/'
cutString = 'SelectionFile'
templateFile = '../makeThetaTemplates/'+tempVersion+cutString+'/templates_'+discriminant+'_TTM900_12p892fb'+rfilePostFix+'.root'
if not os.path.exists(outDir+tempVersion): os.system('mkdir '+outDir+tempVersion)
if not os.path.exists(outDir+tempVersion+'/bkgs'): os.system('mkdir '+outDir+tempVersion+'/bkgs')

saveKey = ''
bkgList = ['top','ewk','qcd'] #some uncertainties will be skipped depending on the bkgList[0] process!!!!
channels = ['isE','isM']
ttags = ['nT0p']#,'nT1p']
wtags = ['nW0','nW1p']
btags = ['nB0','nB1','nB2','nB3p']
systematics = ['pileup','jec','jer','btag','mistag','tau21','q2','jsf','muRFcorrdNew','pdfNew','trigeff']
		
RFile = R.TFile(templateFile)

for syst in systematics:
	Prefix = discriminant+'_12p892fb_'+channels[0]+'_'+ttags[0]+'_'+wtags[0]+'_'+btags[0]+'__'+bkgList[0]
	if (syst=='q2' or syst=='toppt') and bkgList[0]!='top': continue
	if (syst=='pdNewf' or syst=='muRFcorrdNew') and bkgList[0]=='qcd': continue
	print Prefix
	hNm = RFile.Get(Prefix).Clone()
	hUp = RFile.Get(Prefix+'__'+syst+'__plus').Clone()
	hDn = RFile.Get(Prefix+'__'+syst+'__minus').Clone()
	for ch in channels:
		for ttag in ttags:
			for wtag in wtags:
				for btag in btags:
					for bkg in bkgList:
						if ch==channels[0] and btag==btags[0] and ttag==ttags[0] and wtag==wtags[0] and bkg==bkgList[0]: continue
						try: 
							print Prefix.replace(channels[0],ch).replace(ttags[0],ttag).replace(wtags[0],wtag).replace(btags[0],btag).replace(bkgList[0],bkg)
							htemp = RFile.Get(Prefix.replace('isE',ch).replace(ttags[0],ttag).replace(wtags[0],wtag).replace(btags[0],btag).replace(bkgList[0],bkg)).Clone()
							hNm.Add(htemp)
						except: pass
						try:
							if (syst=='q2' or syst=='toppt') and bkg!='top':
								htempUp = RFile.Get(Prefix.replace(channels[0],ch).replace(ttags[0],ttag).replace(wtags[0],wtag).replace(btags[0],btag).replace(bkgList[0],bkg)).Clone()
								hUp.Add(htempUp)
							else:
								htempUp = RFile.Get(Prefix.replace(channels[0],ch).replace(ttags[0],ttag).replace(wtags[0],wtag).replace(btags[0],btag).replace(bkgList[0],bkg)+'__'+syst+'__plus').Clone()
								scaleHist = 1.

								htempUp.Scale(scaleHist)
								hUp.Add(htempUp)
						except:pass
						try: 
							if (syst=='q2' or syst=='toppt') and bkg!='top':
								htempDown = RFile.Get(Prefix.replace(channels[0],ch).replace(ttags[0],ttag).replace(wtags[0],wtag).replace(btags[0],btag).replace(bkgList[0],bkg)).Clone()
								hDn.Add(htempDown)
							else:
								htempDown = RFile.Get(Prefix.replace(channels[0],ch).replace(ttags[0],ttag).replace(wtags[0],wtag).replace(btags[0],btag).replace(bkgList[0],bkg)+'__'+syst+'__minus').Clone()
								scaleHist = 1.

								htempDown.Scale(scaleHist)
								hDn.Add(htempDown)
						except:pass
	hNm.Draw()
	hUp.Draw()
	hDn.Draw()
	print syst, ((hUp.Integral()/hNm.Integral()-1.)+(1.-hDn.Integral()/hNm.Integral()))/2

	canv = R.TCanvas(syst,syst,1000,700)
	yDiv = 0.35
	uPad=R.TPad('uPad','',0,yDiv,1,1)
	uPad.SetTopMargin(0.07)
	uPad.SetBottomMargin(0)
	uPad.SetRightMargin(.05)
	uPad.SetLeftMargin(.18)
	uPad.Draw()

	lPad=R.TPad("lPad","",0,0,1,yDiv) #for sigma runner
	lPad.SetTopMargin(0)
	lPad.SetBottomMargin(.4)
	lPad.SetRightMargin(.05)
	lPad.SetLeftMargin(.18)
	lPad.SetGridy()
	lPad.Draw()

	uPad.cd()

	R.gStyle.SetOptTitle(0)

	hNm.SetFillColor(R.kWhite)
	hUp.SetFillColor(R.kWhite)
	hDn.SetFillColor(R.kWhite)
	hNm.SetMarkerColor(R.kBlack)
	hUp.SetMarkerColor(R.kRed)
	hDn.SetMarkerColor(R.kBlue)
	hNm.SetLineColor(R.kBlack)
	hUp.SetLineColor(R.kRed)
	hDn.SetLineColor(R.kBlue)
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
	R.gStyle.SetOptTitle(0)
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

	legend = R.TLegend(0.6,0.65,0.9,0.90)
	legend.SetShadowColor(0);
	legend.SetFillColor(0);
	legend.SetLineColor(0);
	legend.AddEntry(hNm,'Nominal','l')
	legend.AddEntry(hUp,syst.replace('topsf','t tag').replace('muRFcorrdNew','muRF').replace('muRFdecorrdNew','muRF').replace('muRFcorrd','muRF').replace('muRFenv','muRF').replace('pdfNew','PDF').replace('toppt','Top Pt').replace('jsf','JSF').replace('jec','JEC').replace('q2','Q^{2}').replace('miniiso','miniIso').replace('pileup','Pileup').replace('jer','JER').replace('btag','b tag').replace('pdf','PDF').replace('jmr','JMR').replace('jms','JMS').replace('tau21','#tau_{2}/#tau_{1}')+' Up','l')
	legend.AddEntry(hDn,syst.replace('topsf','t tag').replace('muRFcorrdNew','muRF').replace('muRFdecorrdNew','muRF').replace('muRFcorrd','muRF').replace('muRFenv','muRF').replace('pdfNew','PDF').replace('toppt','Top Pt').replace('jsf','JSF').replace('jec','JEC').replace('q2','Q^{2}').replace('miniiso','miniIso').replace('pileup','Pileup').replace('jer','JER').replace('btag','b tag').replace('pdf','PDF').replace('jmr','JMR').replace('jms','JMS').replace('tau21','#tau_{2}/#tau_{1}')+' Down','l')
	legend.Draw('same')
	
	prelimTex=R.TLatex()
	prelimTex.SetNDC()
	prelimTex.SetTextAlign(31) # align right
	prelimTex.SetTextFont(42)
	prelimTex.SetTextSize(0.05)
	prelimTex.SetLineWidth(2)
	prelimTex.DrawLatex(0.90,0.943,str(lumi)+" fb^{-1} (13 TeV)")

	prelimTex2=R.TLatex()
	prelimTex2.SetNDC()
	prelimTex2.SetTextFont(61)
	prelimTex2.SetLineWidth(2)
	prelimTex2.SetTextSize(0.07)
	prelimTex2.DrawLatex(0.18,0.9364,"CMS")

	prelimTex3=R.TLatex()
	prelimTex3.SetNDC()
	prelimTex3.SetTextAlign(13)
	prelimTex3.SetTextFont(52)
	prelimTex3.SetTextSize(0.040)
	prelimTex3.SetLineWidth(2)
	prelimTex3.DrawLatex(0.25175,0.9664,"Preliminary")

	Tex1=R.TLatex()
	Tex1.SetNDC()
	Tex1.SetTextSize(0.05)
	Tex1.SetTextAlign(31) # align right
	textx = 0.4
	
	Tex2 = R.TLatex()
	Tex2.SetNDC()
	Tex2.SetTextSize(0.05)
	Tex2.SetTextAlign(31)

	canv.SaveAs(tempVersion+'/bkgs/'+syst+saveKey+'.pdf')
	canv.SaveAs(tempVersion+'/bkgs/'+syst+saveKey+'.png')
	canv.SaveAs(tempVersion+'/bkgs/'+syst+saveKey+'.root')

RFile.Close()

