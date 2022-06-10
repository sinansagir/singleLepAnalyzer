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
iPlot = sys.argv[1]#'HT'
year = sys.argv[2]#'R16'

addStat=True

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
useCombine = True
tempVersion = 'templates_'+year+'_40vars_6j_NJetsCSV_053121lim2'
isRebinned = '_rebinned_stat0p3'
if 'kinematics' in tempVersion: isRebinned = '_rebinned_stat1p1'
cutString = ''
saveKey = ''#'_tshape'
if useCombine: templateFile = '../makeTemplates/'+tempVersion+'/'+cutString+'/templates_'+iPlot+'_'+lumiStr+isRebinned+'.root'
else: templateFile = '../makeTemplates/'+tempVersion+'/'+cutString+'/templates_'+iPlot+'_'+sig1+'_'+lumiStr+isRebinned+'.root'
if not os.path.exists(outDir+tempVersion): os.system('mkdir '+outDir+tempVersion)

bkgTTBarList = ['ttnobb','ttbb'] #['ttjj','ttcc','ttbb','ttbj']
bkgList = bkgTTBarList+['top','ewk','qcd'] #some uncertainties will be skipped depending on the bkgList[0] process!!!!
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
systematics = ['hotclosure']#['pileup','hotstat','hotcspur','hotclosure','isr','fsr','PSwgt','muRF','pdf','hdamp','ue','CSVshapelf','CSVshapehf','CSVshapehfstats1','CSVshapehfstats2','CSVshapecferr1','CSVshapecferr2','CSVshapelfstats1','CSVshapelfstats2']#,'njet','njetsf','ht','trigeff','toppt','tau32','jmst','jmrt','tau21','jmsW','jmrW','tau21pt']
#,'btag','btagcorr','btaguncorr','mistag'
if year!='R18': systematics += ['prefire']
# if year=='R18': systematics += ['hem']
systematics+= ['JEC','JER']#,
systematics = ['bdt']
# 'JEC_Total','JEC_FlavorQCD',
# 'JEC_RelativeBal','JEC_RelativeSample_'+year.replace('R','20'),
# 'JEC_Absolute','JEC_Absolute_'+year.replace('R','20'),
# 'JEC_HF','JEC_HF_'+year.replace('R','20'),
# 'JEC_EC2','JEC_EC2_'+year.replace('R','20'),
# 'JEC_BBEC1','JEC_BBEC1_'+year.replace('R','20')]
systematics = ['hdamp','ue']
#systematics = ['lowess'+syst for syst in systematics]

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
	Prefix = iPlot+'_'+lumiStr+'_'+cat+'__'+bkgList[0]
	print Prefix
	nBinsBkg += RFile.Get(Prefix).GetNbinsX()

distr=rt.TH1F('err',';relative statistical error;N of bins',100,0,2)

max_stat=-1.0
comboHists = {}	
comboSigHists = {}			
signal='tttt'
for em in isEMlist:
	comboHists['bkg'+em]=rt.TH1F('bkg'+em,'Bin #',nBinsBkg,0,nBinsBkg)
	comboSigHists[signal+em]=rt.TH1F(signal+em,'Bin #',nBinsBkg,0,nBinsBkg)
	for syst in systematics:
		comboHists['bkg'+em+syst+'Up']=rt.TH1F('bkg'+em+syst+'Up','Bin #',nBinsBkg,0,nBinsBkg)
		comboHists['bkg'+em+syst+'Dn']=rt.TH1F('bkg'+em+syst+'Dn','Bin #',nBinsBkg,0,nBinsBkg)
		comboSigHists[signal+em+syst+'Up']=rt.TH1F(signal+em+syst+'Up','Bin #',nBinsBkg,0,nBinsBkg)
		comboSigHists[signal+em+syst+'Dn']=rt.TH1F(signal+em+syst+'Dn','Bin #',nBinsBkg,0,nBinsBkg)
		ibin = 0
		for cat in catList:
			if 'is'+em not in cat: continue
			Prefix = iPlot+'_'+lumiStr+'_'+cat+'__'+bkgList[0]
			print Prefix+'__'+syst
			try: hNm = RFile.Get(Prefix).Clone()
			except: 
				print bkgList[0]+" NOT FOUND for category "+cat
				continue
			try:
				hUp = RFile.Get(Prefix+'__'+syst+upTag).Clone()
				hDn = RFile.Get(Prefix+'__'+syst+downTag).Clone()
			except:
				print "No shape for",bkgList[0],cat,syst
				hUp = RFile.Get(Prefix).Clone()
				hDn = RFile.Get(Prefix).Clone()

			if useCombine: PrefixSig = iPlot+'_'+lumiStr+'_'+cat+'__'+signal
			else: PrefixSig = iPlot+'_'+lumiStr+'_'+cat+'__sig'
			hNmSig = RFile.Get(PrefixSig).Clone()
			hUpSig = RFile.Get(PrefixSig+'__'+syst+upTag).Clone()
			hDnSig = RFile.Get(PrefixSig+'__'+syst+downTag).Clone()
			for bkg in bkgList:
				if bkg==bkgList[0]: continue
				try: 
					htemp = RFile.Get(Prefix.replace(bkgList[0],bkg)).Clone()
					hNm.Add(htemp)
				except: 
					print "No nominal for",bkg,cat,syst
					pass
				try:
					htempUp = RFile.Get(Prefix.replace(bkgList[0],bkg)+'__'+syst+upTag).Clone()
					hUp.Add(htempUp)
				except:
					print "No shape for",bkg,cat,syst
					try:
						htempUp = RFile.Get(Prefix.replace(bkgList[0],bkg)).Clone()
						hUp.Add(htempUp)
					except: 
						print "No nominal for",bkg,cat,syst
						pass
			
				try:
					htempDown = RFile.Get(Prefix.replace(bkgList[0],bkg)+'__'+syst+downTag).Clone()
					hDn.Add(htempDown)
				except:
					print "No shape for",bkg,cat,syst
					try:
						htempDown = RFile.Get(Prefix.replace(bkgList[0],bkg)).Clone()
						hDn.Add(htempDown)
					except: 
						print "No nominal for",bkg,cat,syst
						pass

			for jbin in range(1,hNm.GetNbinsX()+1):
				comboHists['bkg'+em].SetBinContent(ibin+jbin,hNm.GetBinContent(jbin))
				comboHists['bkg'+em+syst+'Up'].SetBinContent(ibin+jbin,hUp.GetBinContent(jbin))
				comboHists['bkg'+em+syst+'Dn'].SetBinContent(ibin+jbin,hDn.GetBinContent(jbin))
				if addStat:
					# if hNm.GetBinContent(jbin)>0.0000001:
					# 	distr.Fill(hNm.GetBinError(jbin)/hNm.GetBinContent(jbin))
					if hUp.GetBinContent(jbin)>0.0000001:
						distr.Fill(hUp.GetBinError(jbin)/hUp.GetBinContent(jbin))
						if hUp.GetBinError(jbin)/hUp.GetBinContent(jbin)>max_stat:
							max_stat=hUp.GetBinError(jbin)/hUp.GetBinContent(jbin)
					if hDn.GetBinContent(jbin)>0.0000001:	
						distr.Fill(hDn.GetBinError(jbin)/hDn.GetBinContent(jbin))	
						if hDn.GetBinError(jbin)/hDn.GetBinContent(jbin)>max_stat:
							max_stat=hDn.GetBinError(jbin)/hDn.GetBinContent(jbin)
					comboHists['bkg'+em].SetBinError(ibin+jbin,hNm.GetBinError(jbin))
					comboHists['bkg'+em+syst+'Up'].SetBinError(ibin+jbin,hUp.GetBinError(jbin))
					comboHists['bkg'+em+syst+'Dn'].SetBinError(ibin+jbin,hDn.GetBinError(jbin))
					#s/sqrt(b)
					s_over_sqrt_b=hNmSig.GetBinContent(jbin)/math.sqrt(hNm.GetBinContent(jbin))
					comboSigHists[signal+em].SetBinContent(ibin+jbin,s_over_sqrt_b)
# 				comboHists['bkg'+em].GetXaxis().SetBinLabel(ibin+jbin,str(ibin+jbin))
# 				comboHists['bkg'+em+syst+'Up'].GetXaxis().SetBinLabel(ibin+jbin,str(ibin+jbin))
# 				comboHists['bkg'+em+syst+'Dn'].GetXaxis().SetBinLabel(ibin+jbin,str(ibin+jbin))
			if len(catList)==2:
				comboHists['bkg'+em] = hNm.Clone('bkg'+em)
				comboHists['bkg'+em+syst+'Up'] = hUp.Clone('bkg'+em+syst+'Up')
				comboHists['bkg'+em+syst+'Dn'] = hDn.Clone('bkg'+em+syst+'Dn')
			ibin += hNm.GetNbinsX()

		canv = rt.TCanvas('bkg'+em,'bkg'+em,1000,700)
		yDiv = 0.35
		uPad=rt.TPad('uPad','',0,yDiv,1,1)
		uPad.SetTopMargin(0.07)
		uPad.SetBottomMargin(0)
		uPad.SetRightMargin(.02)
		uPad.SetLeftMargin(.12)
		uPad.SetLogy()
		uPad.Draw()

		lPad=rt.TPad("lPad","",0,0,1,yDiv) #for sigma runner
		lPad.SetTopMargin(0)
		lPad.SetBottomMargin(.4)
		lPad.SetRightMargin(.02)
		lPad.SetLeftMargin(.12)
		lPad.SetGridy()
		lPad.Draw()

		uPad.cd()

		rt.gStyle.SetOptTitle(0)

		comboHists['bkg'+em].SetFillColor(rt.kWhite)
		comboHists['bkg'+em+syst+'Up'].SetFillColor(rt.kWhite)
		comboHists['bkg'+em+syst+'Dn'].SetFillColor(rt.kWhite)
		comboHists['bkg'+em].SetMarkerColor(rt.kBlack)
		comboHists['bkg'+em+syst+'Up'].SetMarkerColor(rt.kRed)
		comboHists['bkg'+em+syst+'Dn'].SetMarkerColor(rt.kBlue)
		comboHists['bkg'+em].SetLineColor(rt.kBlack)
		comboHists['bkg'+em+syst+'Up'].SetLineColor(rt.kRed)
		comboHists['bkg'+em+syst+'Dn'].SetLineColor(rt.kBlue)
		comboHists['bkg'+em].SetLineWidth(2)
		comboHists['bkg'+em].SetLineStyle(1)
		comboHists['bkg'+em+syst+'Up'].SetLineWidth(2)
		comboHists['bkg'+em+syst+'Up'].SetLineStyle(1)
		comboHists['bkg'+em+syst+'Dn'].SetLineWidth(2)
		comboHists['bkg'+em+syst+'Dn'].SetLineStyle(1)
		comboHists['bkg'+em].SetMarkerSize(.05)
		comboHists['bkg'+em+syst+'Up'].SetMarkerSize(.05)
		comboHists['bkg'+em+syst+'Dn'].SetMarkerSize(.05)

		comboHists['bkg'+em+syst+'Up'].GetYaxis().SetTitle('Events')
		comboHists['bkg'+em+syst+'Up'].GetYaxis().SetLabelSize(0.10)
		comboHists['bkg'+em+syst+'Up'].GetYaxis().SetTitleSize(0.1)
		comboHists['bkg'+em+syst+'Up'].GetYaxis().SetTitleOffset(.65)
		if len(catList)!=2: comboHists['bkg'+em+syst+'Up'].GetXaxis().SetTitle('Bin #')
		comboHists['bkg'+em+syst+'Up'].GetXaxis().SetLabelSize(0.10)
		comboHists['bkg'+em+syst+'Up'].GetXaxis().SetTitleSize(0.1)
		#comboHists['bkg'+em+syst+'Up'].GetXaxis().SetTitleOffset(.65)

		#comboHists['bkg'+em+syst+'Up'].SetMaximum(1.1*max(comboHists['bkg'+em+syst+'Up'].GetMaximum(),comboHists['bkg'+em].GetMaximum(),comboHists['bkg'+em+syst+'Dn'].GetMaximum()))
		comboHists['bkg'+em+syst+'Up'].GetYaxis().SetRangeUser(0.05,1.1*max(comboHists['bkg'+em+syst+'Up'].GetMaximum(),comboHists['bkg'+em].GetMaximum(),comboHists['bkg'+em+syst+'Dn'].GetMaximum()))


		if addStat:
				comboHistsUp2=comboHists['bkg'+em+syst+'Up'].Clone()
				comboHists2=comboHists['bkg'+em].Clone()
				comboHistsDn2=comboHists['bkg'+em+syst+'Dn'].Clone()
				comboHists['bkg'+em+syst+'Up'].SetLineWidth(1)
				comboHists['bkg'+em].SetLineWidth(1)
				comboHists['bkg'+em+syst+'Dn'].SetLineWidth(1)
				comboHistsUp2.SetFillColorAlpha(rt.kRed,0.3)
				comboHists2.SetFillColorAlpha(rt.kBlack,0.3)
				comboHistsDn2.SetFillColorAlpha(rt.kBlue,0.3)

				comboSigHists[signal+em].SetFillColor(rt.kWhite)
				comboSigHists[signal+em].SetMarkerColor(rt.kBlack)
				comboSigHists[signal+em].SetLineColor(rt.kBlack)
				comboSigHists[signal+em].SetLineWidth(2)
				comboSigHists[signal+em].SetLineStyle(1)
				comboSigHists[signal+em].SetMarkerSize(.05)
				comboSigHists[signal+em].GetYaxis().SetRangeUser(0.00005,50*comboSigHists[signal+em].GetMaximum())


				# comboHists['bkg'+em+syst+'Up'].Draw('hist')
				# comboHists['bkg'+em].Draw('samehist')
				# comboHists['bkg'+em+syst+'Dn'].Draw('samehist')
				# comboHistsUp2.Draw('same e2')
				# comboHists2.Draw('same e2')
				# comboHistsDn2.Draw('same e2')
				comboSigHists[signal+em].Draw('hist')
				# comboHists['bkg'+em].Draw('samehist')
				# comboHists['bkg'+em+syst+'Dn'].Draw('samehist')

		else:
				comboHists['bkg'+em+syst+'Up'].Draw('hist')
				comboHists['bkg'+em].Draw('samehist')
				comboHists['bkg'+em+syst+'Dn'].Draw('samehist')

# 		comboHists['bkg'+em+syst+'Up'].Draw()
# 		comboHists['bkg'+em].Draw('same')
# 		comboHists['bkg'+em+syst+'Dn'].Draw('same')

		# comboHists['bkg'+em+syst+'Up'].Draw('hist')
		# comboHists['bkg'+em].Draw('samehist')
		# comboHists['bkg'+em+syst+'Dn'].Draw('samehist')

		#uPad.RedrawAxis()

		lPad.cd()
		rt.gStyle.SetOptTitle(0)
		pullUp = comboHists['bkg'+em+syst+'Up'].Clone()


		pullUp_original=pullUp.Clone()
		for iBin in range(0,pullUp.GetXaxis().GetNbins()+2):

				if abs(pullUp_original.GetBinContent(iBin))<0.0000000001:
					pullUp_original.SetBinContent(iBin,pullUp_original.GetBinContent(iBin)+0.0000000001)
				if abs(comboHists['bkg'+em].GetBinContent(iBin))<0.0000000001:
					comboHists['bkg'+em].SetBinContent(iBin,comboHists['bkg'+em].GetBinContent(iBin)+0.0000000001)
				pullUp.SetBinContent(iBin,pullUp_original.GetBinContent(iBin)/comboHists['bkg'+em].GetBinContent(iBin)-1)
				
				pullUp.SetBinError(iBin,
					(pullUp.GetBinContent(iBin)+1)*math.sqrt(\
						(pullUp_original.GetBinError(iBin)/pullUp_original.GetBinContent(iBin))**2+\
						(comboHists['bkg'+em].GetBinError(iBin)/comboHists['bkg'+em].GetBinContent(iBin))**2\
						-2*(pullUp_original.GetBinError(iBin)/pullUp_original.GetBinContent(iBin))*(comboHists['bkg'+em].GetBinError(iBin)/comboHists['bkg'+em].GetBinContent(iBin))\
						))



		# for iBin in range(0,pullUp.GetXaxis().GetNbins()+2):
		# 	pullUp.SetBinContent(iBin,pullUp.GetBinContent(iBin)-comboHists['bkg'+em].GetBinContent(iBin))
		# 	pullUp.SetBinError(iBin,math.sqrt(pullUp.GetBinError(iBin)**2+comboHists['bkg'+em].GetBinError(iBin)**2))

		pullUp.Divide(comboHists['bkg'+em])
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

		pullDown = comboHists['bkg'+em+syst+'Dn'].Clone()

		pullDown_original=pullDown.Clone()
		for iBin in range(0,pullDown.GetXaxis().GetNbins()+2):

				if abs(pullDown_original.GetBinContent(iBin))<0.0000000001:
					pullDown_original.SetBinContent(iBin,pullDown_original.GetBinContent(iBin)+0.0000000001)
				if abs(comboHists['bkg'+em].GetBinContent(iBin))<0.0000000001:
					comboHists['bkg'+em].SetBinContent(iBin,comboHists['bkg'+em].GetBinContent(iBin)+0.0000000001)
				pullDown.SetBinContent(iBin,pullDown_original.GetBinContent(iBin)/comboHists['bkg'+em].GetBinContent(iBin)-1)
				
				pullDown.SetBinError(iBin,
					(pullDown.GetBinContent(iBin)+1)*math.sqrt(\
						(pullDown_original.GetBinError(iBin)/pullDown_original.GetBinContent(iBin))**2+\
						(comboHists['bkg'+em].GetBinError(iBin)/comboHists['bkg'+em].GetBinContent(iBin))**2\
						-2*(pullDown_original.GetBinError(iBin)/pullDown_original.GetBinContent(iBin))*(comboHists['bkg'+em].GetBinError(iBin)/comboHists['bkg'+em].GetBinContent(iBin))\
						))

		# for iBin in range(0,pullDown.GetXaxis().GetNbins()+2):
		# 	pullDown.SetBinContent(iBin,pullDown.GetBinContent(iBin)-comboHists['bkg'+em].GetBinContent(iBin))
		# 	pullDown.SetBinError(iBin,math.sqrt(pullDown.GetBinError(iBin)**2+comboHists['bkg'+em].GetBinError(iBin)**2))

		pullDown.Divide(comboHists['bkg'+em])
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

		if addStat:
				pullUp2=pullUp.Clone()
				pullDown2=pullDown.Clone()
				pullUp.SetLineWidth(1)
				pullDown.SetLineWidth(1)
				pullUp2.SetFillColorAlpha(rt.kRed,0.3)
				pullDown2.SetFillColorAlpha(rt.kBlue,0.3)
				
				pullUp.Draw('hist')
				pullDown.Draw('same hist')
				pullUp2.Draw('same e2')
				pullDown2.Draw('same e2')
		else:	
				pullUp.Draw('hist')
				pullDown.Draw('samehist')
		# pullUp.Draw('hist')
		# pullDown.Draw('samehist')


		lPad.RedrawAxis()

		uPad.cd()

		legend = rt.TLegend(0.7,0.65,0.9,0.90)
		legend.SetShadowColor(0);
		legend.SetFillColor(0);
		legend.SetLineColor(0);
		legend.SetTextSize(0.05);
		legend.AddEntry(comboHists['bkg'+em],'S/#sqrt{B}','l')
		legend.AddEntry(comboHists['bkg'+em+syst+'Up'],syst.replace('lowess','').replace('hem','HEM15/16').replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('isr','ISR').replace('fsr','FSR').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Up','l')
		legend.AddEntry(comboHists['bkg'+em+syst+'Dn'],syst.replace('lowess','').replace('hem','HEM15/16').replace('pileup','PU').replace('prefire','Prefire').replace('btag','b tag').replace('mistag','udsg mistag').replace('jec','JEC').replace('jer','JER').replace('hotstat','res-t stat').replace('hotcspur','res-t CSpurity').replace('hotclosure','res-t closure').replace('PSwgt','PS weight').replace('isr','ISR').replace('fsr','FSR').replace('pdf','PDF').replace('hdamp','hDamp').replace('ue','UE').replace('njet','Njet').replace('tau21','#tau_{2}/#tau_{1}').replace('toppt','top p_{T}').replace('q2','Q^{2}').replace('jmr','JMR').replace('jms','JMS').replace('tau21pt','#tau_{2}/#tau_{1} p_{T}').replace('tau21','#tau_{2}/#tau_{1}').replace('tau32','#tau_{3}/#tau_{2}')+' Down','l')

		legend.Draw('same')

		prelimTex=rt.TLatex()
		prelimTex.SetNDC()
		prelimTex.SetTextAlign(31) # align right
		prelimTex.SetTextFont(42)
		prelimTex.SetTextSize(0.07)
		prelimTex.SetLineWidth(2)
		prelimTex.DrawLatex(0.97,0.94,str(lumi)+" fb^{-1} (13 TeV)")

		prelimTex2=rt.TLatex()
		prelimTex2.SetNDC()
		prelimTex2.SetTextFont(61)
		prelimTex2.SetLineWidth(2)
		prelimTex2.SetTextSize(0.09)
		prelimTex2.DrawLatex(0.18,0.8364,"CMS")

		prelimTex3=rt.TLatex()
		prelimTex3.SetNDC()
		prelimTex3.SetTextAlign(13)
		prelimTex3.SetTextFont(52)
		prelimTex3.SetTextSize(0.050)
		prelimTex3.SetLineWidth(2)
		prelimTex3.DrawLatex(0.26275,0.87,"Preliminary")

		chLatex = rt.TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.07)
		chLatex.SetTextAlign(21)
		flv = cat.split('_')[0]
		if em=='E': flvString='e+jets'
		if em=='M': flvString='#mu+jets'
		chLatex.DrawLatex(0.45, 0.84, flvString)

		canv.SaveAs(tempVersion+'/'+syst+'_'+iPlot+'_'+lumiStr+'_is'+em+saveKey+'_bkg.pdf')
		# canv.SaveAs(tempVersion+'/'+syst+'_'+iPlot+'_'+lumiStr+'_is'+em+saveKey+'_bkg.png')
		#canv.SaveAs(tempVersion+'/'+saveDir+'/'+syst+'_'+iPlot+'_'+lumiStr+'_is'+em+'_bkg.eps')

cc=rt.TCanvas()
distr.Draw()
cc.SaveAs(year+'3Bkg.pdf')

RFile.Close()
print max_stat
