import ROOT as R
import os,sys,math
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from utils import *
from array import array

from tdrStyle import *
setTDRStyle()
R.gROOT.SetBatch(1)

year = str(sys.argv[1])

discriminant = 'DnnTprime'
rfilePostFix = '_Combine_rebinned_stat0p3'
#rfilePostFix = '_rebinned_stat0p3'
BRStr = '_bW0p5_tZ0p25_tH0p25'

lumi = 41.5
lumiStr = '_41p53fb'
outDir = os.getcwd()+'/templatesSRCR_June2020TT_0p3smoothedLOWESS/'
#templateFile = '/uscms_data/d3/jmanagan/CMSSW_10_2_10/src/tptp_2017/makeTemplates/templatesSRCR_June2020TT/templates_'+discriminant+'_TTM1400'+BRStr+lumiStr+rfilePostFix+'_smoothedLOWESS.root'
templateFile = '/uscms_data/d3/jmanagan/CMSSW_10_2_10/src/tptp_2017/makeTemplates/templatesSRCR_June2020TT/templates_'+discriminant+BRStr+lumiStr.replace('fb','')+rfilePostFix+'_smoothedLOWESS.root'
if year == '2018':
	lumi = 59.7
	lumiStr = '_59p69fb'
	rfilePostFix = '_BKGNORM_rebinned_stat0p3'
	outDir = os.getcwd()+'/templatesCRhtntagSR_Feb2020_2018/'
	templateFile = '../makeTemplates/templatesCRhtntagSR_MVAfixBB/templates_'+discriminant+'_BBM1400'+BRStr+lumiStr+rfilePostFix+'.root'

if not os.path.exists(outDir): os.system('mkdir '+outDir)
if not os.path.exists(outDir+'/bkgs'): os.system('mkdir '+outDir+'/bkgs')
if not os.path.exists(outDir+'/sigs'): os.system('mkdir '+outDir+'/sigs')

saveKey = ''#
channels = ['isE','isM']
tags = ['taggedbWbW','taggedtZbW','taggedtHbW','taggedtZHtZH','notVbW','notVtH','notVtZ','notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W','dnnLargeT','dnnLargeH','dnnLargeZ','dnnLargeW','dnnLargeB','dnnLargeJwjet','dnnLargeJttbar']
if 'BB' in templateFile: tags = ['taggedtWtW','taggedbZtW','taggedbHtW','notVtW','notVbH','notVbZ','notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W','dnnLargeT','dnnLargeH','dnnLargeZ','dnnLargeW','dnnLargeB','dnnLargeJwjet','dnnLargeJttbar']

yearpdf = year
if year != '2016': yearpdf = '20172018'
systematics = ['jec'+year,'jer'+year,'pdfNew'+yearpdf,'muRFcorrdNewTop','muRFcorrdNewEwk','pileup','jsf','elTrig'+year,'muTrig'+year,'Teff','Tmis'+year,'Heff','Hmis'+year,'Zeff','Zmis'+year,'Weff','Wmis'+year,'Beff','Bmis'+year]
if year != '2018': systematics.append('prefire')

systnames = {'jec'+year:'JEC','jer'+year:'JER','pdfNew'+yearpdf:'PDF','pileup':'Pileup','prefire':'Prefiring','jsf':'HT weight','muRFcorrdNewSig':'Ren./Fact. Sig','muRFcorrdNewTop':'Ren./Fact. Top','muRFcorrdNewEwk':'Ren./Fact. Ewk','muRFcorrdNewQCD':'Ren./Fact. QCD','elTrig'+year:'El trigger','muTrig'+year:'Mu trigger','Teff':'DeepAK8 T','Tmis'+year:'DeepAK8 T mistag','Heff':'DeepAK8 H','Hmis'+year:'DeepAK8 H mistag','Zeff':'DeepAK8 Z','Zmis'+year:'DeepAK8 Z mistag','Weff':'DeepAK8 W','Wmis'+year:'DeepAK8 W mistag','Beff':'DeepAK8 B','Bmis'+year:'DeepAK8 B mistag'}
		
RFile = R.TFile(templateFile)

for syst in systematics:
	if 'Ewk' in syst: 
		bkgList = ['ewk','top','qcd']
	elif 'QCD' in syst:
		bkgList = ['qcd','top','ewk']
	else:
		bkgList = ['top','ewk','qcd']
	for ch in channels:
		for tag in tags:
			print '-----------------------------'+syst+', '+ch+', '+tag+'--------------------------------'
			histname = discriminant
                        SRCR = '_isSR'
			if 'prime' in discriminant and ('dnnLarge' in tag): 
                                histname = 'HTNtag'
                                SRCR = '_isCR'

			Prefix = histname+lumiStr+SRCR+'_'+channels[0]+'_'+tag+'_DeepAK8__'+bkgList[0]
			try: 
				if ch != 'isL': hNm = RFile.Get(Prefix.replace(channels[0],ch)).Clone()
				else: 
					hNm = RFile.Get(Prefix).Clone()
					hNm = RFile.Get(Prefix.replace(channels[0],channels[1]))
			except:
				print 'No histogram for ',bkgList[0],' in this channel!'
				continue

			if ch != 'isL':
				hNm = RFile.Get(Prefix.replace(channels[0],ch)).Clone()
				hUp = RFile.Get(Prefix.replace(channels[0],ch)+'__'+syst+'Up').Clone()
				hDn = RFile.Get(Prefix.replace(channels[0],ch)+'__'+syst+'Down').Clone()
			else:
				hNm = RFile.Get(Prefix).Clone()
				hUp = RFile.Get(Prefix+'__'+syst+'Up').Clone()
				hDn = RFile.Get(Prefix+'__'+syst+'Down').Clone()
				hNm.Add(RFile.Get(Prefix.replace(channels[0],channels[1])))
				hUp.Add(RFile.Get(Prefix.replace(channels[0],channels[1])+'__'+syst+'Up'))
				hDn.Add(RFile.Get(Prefix.replace(channels[0],channels[1])+'__'+syst+'Down'))
				
			for bkg in bkgList:
				if ch==channels[0] and bkg==bkgList[0]: 
					print Prefix
					continue
				
				if ch != 'isL':
					try: 
						print Prefix.replace(channels[0],ch).replace(bkgList[0],bkg)
						htemp = RFile.Get(Prefix.replace(channels[0],ch).replace(bkgList[0],bkg)).Clone()
						hNm.Add(htemp)
					except: pass
					try:
						if (syst=='muRFcorrdNewTop' and bkg!='top') or (syst=='muRFcorrdNewEwk' and bkg!='ewk') or (syst=='muRFcorrdNewQCD' and bkg!='qcd'):
							htempUp = RFile.Get(Prefix.replace(channels[0],ch).replace(bkgList[0],bkg)).Clone()
							hUp.Add(htempUp)
						else:
							htempUp = RFile.Get(Prefix.replace(channels[0],ch).replace(bkgList[0],bkg)+'__'+syst+'Up').Clone()
							hUp.Add(htempUp)
					except:pass
					try: 
						if (syst=='muRFcorrdNewTop' and bkg!='top') or (syst=='muRFcorrdNewEwk' and bkg!='ewk') or (syst=='muRFcorrdNewQCD' and bkg!='qcd'):
							htempDown = RFile.Get(Prefix.replace(channels[0],ch).replace(bkgList[0],bkg)).Clone()
							hDn.Add(htempDown)
						else:
							htempDown = RFile.Get(Prefix.replace(channels[0],ch).replace(bkgList[0],bkg)+'__'+syst+'Down').Clone()
							hDn.Add(htempDown)
					except:pass
				else:
					try: 
						print Prefix.replace(bkgList[0],bkg)
						htemp = RFile.Get(Prefix.replace(bkgList[0],bkg)).Clone()
						hNm.Add(htemp)
						print Prefix.replace(channels[0],channels[1]).replace(bkgList[0],bkg)
						htemp = RFile.Get(Prefix.replace(channels[0],channels[1]).replace(bkgList[0],bkg)).Clone()
						hNm.Add(htemp)
					except: pass
					try:
						if (syst=='muRFcorrdNewTop' and bkg!='top') or (syst=='muRFcorrdNewEwk' and bkg!='ewk') or (syst=='muRFcorrdNewQCD' and bkg!='qcd'):
							htempUp = RFile.Get(Prefix.replace(bkgList[0],bkg)).Clone()
							hUp.Add(htempUp)
							htempUp = RFile.Get(Prefix.replace(channels[0],channels[1]).replace(bkgList[0],bkg)).Clone()
							hUp.Add(htempUp)
						else:
							htempUp = RFile.Get(Prefix.replace(bkgList[0],bkg)+'__'+syst+'Up').Clone()
							hUp.Add(htempUp)
							htempUp = RFile.Get(Prefix.replace(channels[0],channels[1]).replace(bkgList[0],bkg)+'__'+syst+'Up').Clone()
							hUp.Add(htempUp)
					except:pass
					try: 
						if (syst=='muRFcorrdNewTop' and bkg!='top') or (syst=='muRFcorrdNewEwk' and bkg!='ewk') or (syst=='muRFcorrdNewQCD' and bkg!='qcd'):
							htempDown = RFile.Get(Prefix.replace(bkgList[0],bkg)).Clone()
							hDn.Add(htempDown)
							htempDown = RFile.Get(Prefix.replace(channels[0],channels[1]).replace(bkgList[0],bkg)).Clone()
							hDn.Add(htempDown)
						else:
							htempDown = RFile.Get(Prefix.replace(bkgList[0],bkg)+'__'+syst+'Down').Clone()
							hDn.Add(htempDown)
							htempDown = RFile.Get(Prefix.replace(channels[0],channels[1]).replace(bkgList[0],bkg)+'__'+syst+'Down').Clone()
							hDn.Add(htempDown)
					except:pass

			if histname != 'HTNtag' or 'dnnLargeJ' in tag:
				normByBinWidth(hNm,0.01)
				normByBinWidth(hUp,0.01)
				normByBinWidth(hDn,0.01)

			#hNm.Rebin(2);
			#hUp.Rebin(2);
			#hDn.Rebin(2);
			#hNm.Draw()
			#hUp.Draw()
			#hDn.Draw()

			canv = R.TCanvas(Prefix+'__'+syst,Prefix+'__'+syst,1000,700)
			yDiv = 0.35
			uPad=R.TPad('uPad','',0,yDiv,1,1)
			uPad.SetTopMargin(0.07)
			uPad.SetBottomMargin(0)
			uPad.SetRightMargin(.05)
			uPad.SetLeftMargin(.18)
			#uPad.SetLogy()
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

			#canv.SetLogy()
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

			if histname == 'HTNtag':
				if 'dnnLargeJ' in tag: hUp.GetYaxis().SetTitle("< Events / 1 GeV >")
				elif 'dnnLarge' in tag: hUp.GetYaxis().SetTitle("Events")
			else: hUp.GetYaxis().SetTitle("< Events / 0.1 >")

			hUp.GetYaxis().SetLabelSize(0.10)
			hUp.GetYaxis().SetTitleSize(0.1)
			hUp.GetYaxis().SetTitleOffset(.6)

			#hUp.SetMaximum(1.1*max(hUp.GetMaximum(),hNm.GetMaximum(),hDn.GetMaximum()))
			hUp.GetYaxis().SetRangeUser(0.0001,1.4*max(hUp.GetMaximum(),hNm.GetMaximum(),hDn.GetMaximum()))

			hUp.Draw('hist')
			hNm.Draw('same hist')
			hDn.Draw('same hist')
			#uPad.RedrawAxis()

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
			pullDown.SetFillColor(4)
			pullDown.SetLineColor(4)

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
			if 'muRF' in syst:
				pullUp.SetMinimum(-0.5)
				pullUp.SetMaximum(0.5)
			else:
				pullUp.SetMinimum(-0.20)
				pullUp.SetMaximum(0.20)
			pullUp.Draw("hist")
			pullDown.Draw('same hist')
			lPad.RedrawAxis()

			uPad.cd()

			legend = R.TLegend(0.4,0.65,0.7,0.90)
			legend.SetShadowColor(0);
			legend.SetFillColor(0);
			legend.SetLineColor(0);
			legend.AddEntry(hNm,'Nominal','l')
			legend.AddEntry(hUp,systnames[syst]+' Up','l')
			legend.AddEntry(hDn,systnames[syst]+' Down','l')
			legend.Draw('same')

			prelimTex=R.TLatex()
			prelimTex.SetNDC()
			prelimTex.SetTextAlign(31) # align right
			prelimTex.SetTextFont(42)
			prelimTex.SetTextSize(0.05)
			prelimTex.SetLineWidth(2)
			#lumi=round(lumi,2)
			prelimTex.DrawLatex(0.90,0.943,str(lumi)+" fb^{-1} (13 TeV)")
			#prelimTex.DrawLatex(0.88, 0.95, "CMS Preliminary, "+str(lumi)+" fb^{-1} at #sqrt{s} = 8 TeV");

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
			#if blind: prelimTex3.DrawLatex(0.29175,0.9664,"Preliminary")

			Tex1=R.TLatex()
			Tex1.SetNDC()
			Tex1.SetTextSize(0.05)
			Tex1.SetTextAlign(31) # align right
			#if i == 0: textx = 0.89
			#else: textx = 0.85
			textx = 0.3
			#Tex1.DrawLatex(textx, 0.86, 'test')

			Tex2 = R.TLatex()
			Tex2.SetNDC()
			Tex2.SetTextSize(0.05)
			Tex2.SetTextAlign(21)
			if ch=='isE': channelTxt = 'e+jets'
			if ch=='isM': channelTxt = '#mu+jets'
			tagTxt = tag
			sigbkgTxt = 'Total Bkg'
			Tex2.DrawLatex(textx, 0.85, channelTxt)
			Tex2.DrawLatex(textx, 0.80, tagTxt)
			Tex2.DrawLatex(textx, 0.75, sigbkgTxt)
			#Tex2.DrawLatex(textx, 0.70, ttagTxt)

			canv.SaveAs(outDir+'/bkgs/'+syst+'_'+ch+'_'+tag+'.pdf')
			canv.SaveAs(outDir+'/bkgs/'+syst+'_'+ch+'_'+tag+'.png')
			canv.SaveAs(outDir+'/bkgs/'+syst+'_'+ch+'_'+tag+'.root')

			print '-----------------------------'+syst+', '+ch+', '+tag+' SIGNAL --------------------------------'
			if syst=='muRFcorrdNewTop': systtemp = 'muRFcorrdNewSig'
			elif syst=='muRFcorrdNewEwk': continue
			else: systtemp = syst

			hNm.Reset()
			hUp.Reset()
			hDn.Reset()

			Prefix = histname+lumiStr+SRCR+'_'+channels[0]+'_'+tag+'_DeepAK8__TTM1400'
			try: 
				if ch != 'isL': hNm = RFile.Get(Prefix.replace(channels[0],ch)).Clone()
				else: 
					hNm = RFile.Get(Prefix).Clone()
					hNm = RFile.Get(Prefix.replace(channels[0],channels[1]))
			except:
				print 'No histogram for sig in this channel!'
				continue

			if ch != 'isL':
				hNm = RFile.Get(Prefix.replace(channels[0],ch)).Clone()
				hUp = RFile.Get(Prefix.replace(channels[0],ch)+'__'+systtemp+'Up').Clone()
				hDn = RFile.Get(Prefix.replace(channels[0],ch)+'__'+systtemp+'Down').Clone()
			else:
				hNm = RFile.Get(Prefix).Clone()
				hUp = RFile.Get(Prefix+'__'+systtemp+'Up').Clone()
				hDn = RFile.Get(Prefix+'__'+systtemp+'Down').Clone()
				hNm.Add(RFile.Get(Prefix.replace(channels[0],channels[1])))
				hUp.Add(RFile.Get(Prefix.replace(channels[0],channels[1])+'__'+systtemp+'Up'))
				hDn.Add(RFile.Get(Prefix.replace(channels[0],channels[1])+'__'+systtemp+'Down'))
				

			#hNm.Rebin(2);
			#hUp.Rebin(2);
			#hDn.Rebin(2);
			#hNm.Draw()
			#hUp.Draw()
			#hDn.Draw()
			if histname != 'HTNtag' or 'dnnLargeJ' in tag:
				normByBinWidth(hNm,0.01)
				normByBinWidth(hUp,0.01)
				normByBinWidth(hDn,0.01)

			canv = R.TCanvas(Prefix+'__'+systtemp,Prefix+'__'+systtemp,1000,700)
			yDiv = 0.35
			uPad=R.TPad('uPad','',0,yDiv,1,1)
			uPad.SetTopMargin(0.07)
			uPad.SetBottomMargin(0)
			uPad.SetRightMargin(.05)
			uPad.SetLeftMargin(.18)
			#uPad.SetLogy()
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

			#canv.SetLogy()
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

			if histname == 'HTNtag':
				if 'dnnLargeJ' in tag: hUp.GetYaxis().SetTitle("< Events / 1 GeV >")
				elif 'dnnLarge' in tag: hUp.GetYaxis().SetTitle("Events")
			else: hUp.GetYaxis().SetTitle("< Events / 0.1 >")
			hUp.GetYaxis().SetLabelSize(0.10)
			hUp.GetYaxis().SetTitleSize(0.1)
			hUp.GetYaxis().SetTitleOffset(.6)

			#hUp.SetMaximum(1.1*max(hUp.GetMaximum(),hNm.GetMaximum(),hDn.GetMaximum()))
			hUp.GetYaxis().SetRangeUser(0.0001,1.2*max(hUp.GetMaximum(),hNm.GetMaximum(),hDn.GetMaximum()))

			hUp.Draw()
			hNm.Draw('same')
			hDn.Draw('same')
			#uPad.RedrawAxis()

			pullUp.Reset()
			pullDown.Reset()

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
			pullDown.SetFillColor(4)
			pullDown.SetLineColor(4)

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
			if 'muRF' in systtemp or 'jec' in systtemp:
				pullUp.SetMinimum(-0.5)#min(pullDown.GetMinimum(),pullUp.GetMinimum()))
				pullUp.SetMaximum(0.5)#max(pullDown.GetMaximum(),pullUp.GetMaximum()))
			else:
				pullUp.SetMinimum(-0.20)
				pullUp.SetMaximum(0.20)
			pullUp.Draw('hist')
			pullDown.Draw('same hist')
			lPad.RedrawAxis()

			uPad.cd()

			legendS = R.TLegend(0.4,0.65,0.7,0.90)
			legendS.SetShadowColor(0);
			legendS.SetFillColor(0);
			legendS.SetLineColor(0);
			legendS.AddEntry(hNm,'Nominal','l')
			legendS.AddEntry(hUp,systnames[systtemp]+' Up','l')
			legendS.AddEntry(hDn,systnames[systtemp]+' Down','l')
			legendS.Draw('same')

			#prelimTex=R.TLatex()
			prelimTex.SetNDC()
			prelimTex.SetTextAlign(31) # align right
			prelimTex.SetTextFont(42)
			prelimTex.SetTextSize(0.05)
			prelimTex.SetLineWidth(2)
			#lumi=round(lumi,2)
			prelimTex.DrawLatex(0.90,0.943,str(lumi)+" fb^{-1} (13 TeV)")
			#prelimTex.DrawLatex(0.88, 0.95, "CMS Preliminary, "+str(lumi)+" fb^{-1} at #sqrt{s} = 8 TeV");

			#prelimTex2=R.TLatex()
			prelimTex2.SetNDC()
			prelimTex2.SetTextFont(61)
			prelimTex2.SetLineWidth(2)
			prelimTex2.SetTextSize(0.07)
			prelimTex2.DrawLatex(0.18,0.9364,"CMS")

			#prelimTex3=R.TLatex()
			prelimTex3.SetNDC()
			prelimTex3.SetTextAlign(13)
			prelimTex3.SetTextFont(52)
			prelimTex3.SetTextSize(0.040)
			prelimTex3.SetLineWidth(2)
			prelimTex3.DrawLatex(0.25175,0.9664,"Preliminary")
			#if blind: prelimTex3.DrawLatex(0.29175,0.9664,"Preliminary")

			#Tex1=R.TLatex()
			Tex1.SetNDC()
			Tex1.SetTextSize(0.05)
			Tex1.SetTextAlign(31) # align right
			#if i == 0: textx = 0.89
			#else: textx = 0.85
			textx = 0.3
			#Tex1.DrawLatex(textx, 0.86, 'test')

			#Tex2 = R.TLatex()
			Tex2.SetNDC()
			Tex2.SetTextSize(0.05)
			Tex2.SetTextAlign(21)
			if ch=='isE': channelTxt = 'e+jets'
			if ch=='isM': channelTxt = '#mu+jets'
			tagTxt = tag
			sigbkgTxt = 'BB 1.4 TeV (50/25/25)'
			Tex2.DrawLatex(textx, 0.85, channelTxt)
			Tex2.DrawLatex(textx, 0.80, tagTxt)
			Tex2.DrawLatex(textx, 0.75, sigbkgTxt)
			#Tex2.DrawLatex(textx, 0.70, ttagTxt)

			canv.SaveAs(outDir+'/sigs/'+systtemp+'_'+ch+'_'+tag+'.pdf')
			canv.SaveAs(outDir+'/sigs/'+systtemp+'_'+ch+'_'+tag+'.png')
			canv.SaveAs(outDir+'/sigs/'+systtemp+'_'+ch+'_'+tag+'.root')

RFile.Close()

