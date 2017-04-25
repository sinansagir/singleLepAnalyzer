import ROOT as R
import os,sys,math,itertools
from array import array
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from utils import *
from tdrStyle import *

setTDRStyle()
R.gROOT.SetBatch(1)
outDir = os.getcwd()+'/'

lumi = 35.9
discriminant = 'HTpBDT'
lumiStr = '35p867fb'
rfilePostFix = '_rebinned_stat1p1'
tempVersion = 'templates_BDT_3fold_30vars_wSys_2017_3_26'
cutString = ''
templateFile = '../makeTemplates/'+tempVersion+'/'+cutString+'/templates_'+discriminant+'_HTBM500_'+lumiStr+rfilePostFix+'.root'
if not os.path.exists(outDir+tempVersion): os.system('mkdir '+outDir+tempVersion)
saveDir = 'signals_isCR'
if not os.path.exists(outDir+tempVersion+'/'+saveDir): os.system('mkdir '+outDir+tempVersion+'/'+saveDir)

bkgList = ['ttbb','ttcc','ttlf','top','ewk','qcd']
isEMlist = ['E','M']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['1','2','2p','3p']
njetslist = ['3','4','5','6p']
catList = ['is'+item[0]+'_nT'+item[1]+'_nW'+item[2]+'_nB'+item[3]+'_nJ'+item[4] for item in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist)) if isCR(item[4],item[3])]

systematics = ['pileup','jec','jer','muRFcorrdNew','btag','mistag','trigeff']#,'pdfNew']

signameList = [
#                'HTBM180',
			   'HTBM200',
# 			   'HTBM220',
# 			   'HTBM250',
# 			   'HTBM300',
# 			   'HTBM350',
# 			   'HTBM400',
# 			   'HTBM450',
			   'HTBM500',
# 			   'HTBM800',
# 			   'HTBM1000',
# 			   'HTBM2000',
			   'HTBM3000',
			   ]

for signal in signameList:
	RFile = R.TFile(templateFile.replace('HTBM500',signal))
	for syst in systematics:
		if (syst=='q2' or syst=='toppt'):
			print "Do you expect to have "+syst+" for your signal? FIX ME IF SO! I'll skip this systematic"
			continue
		Prefix = discriminant+'_'+lumiStr+'_'+catList[0]+'__sig'
		print Prefix+'__'+syst
		hNm = RFile.Get(Prefix).Clone()
		hUp = RFile.Get(Prefix+'__'+syst+'__plus').Clone()
		hDn = RFile.Get(Prefix+'__'+syst+'__minus').Clone()
		for cat in catList:
			if cat==catList[0]: continue
			try: 
				htemp = RFile.Get(Prefix.replace(catList[0],cat)).Clone()
				hNm.Add(htemp)
			except: 
				print "No nominal for",signal,cat,syst
				pass
				
			try:
				htempUp = RFile.Get(Prefix.replace(catList[0],cat)+'__'+syst+'__plus').Clone()
				hUp.Add(htempUp)
			except:
				print "No shape for",signal,cat,syst
				try:
					htempUp = RFile.Get(Prefix.replace(catList[0],cat)).Clone()
					hUp.Add(htempUp)
				except: 
					print "No nominal for",signal,cat,syst
					pass
		
			try:
				htempDown = RFile.Get(Prefix.replace(catList[0],cat)+'__'+syst+'__minus').Clone()
				hDn.Add(htempDown)
			except:
				print "No shape for",signal,cat,syst
				try:
					htempDown = RFile.Get(Prefix.replace(catList[0],cat)).Clone()
					hDn.Add(htempDown)
				except: 
					print "No nominal for",signal,cat,syst
					pass
		hNm.Draw()
		hUp.Draw()
		hDn.Draw()

		canv = R.TCanvas(Prefix+'__'+syst,Prefix+'__'+syst,1000,700)
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

		hUp.Draw('hist')
		hNm.Draw('same hist')
		hDn.Draw('same hist')

		lPad.cd()
		R.gStyle.SetOptTitle(0)
		pullUp = hUp.Clone()
		for iBin in range(0,pullUp.GetXaxis().GetNbins()+2):
			pullUp.SetBinContent(iBin,pullUp.GetBinContent(iBin)-hNm.GetBinContent(iBin))
			pullUp.SetBinError(iBin,math.sqrt(pullUp.GetBinError(iBin)**2+hNm.GetBinError(iBin)**2))
		pullUp.Divide(hNm)
		pullUp.SetTitle('')
		#pullUp.SetFillColor(2)
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
		#pullDown.SetFillColor(4)
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
		pullUp.Draw('hist')
		pullDown.Draw('same hist')
		lPad.RedrawAxis()

		uPad.cd()

		legend = R.TLegend(0.7,0.65,0.9,0.90)
		legend.SetShadowColor(0);
		legend.SetFillColor(0);
		legend.SetLineColor(0);
		legend.AddEntry(hNm,signal,'l')
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

		canv.SaveAs(tempVersion+'/'+saveDir+'/'+syst+'_'+signal+'.pdf')
		canv.SaveAs(tempVersion+'/'+saveDir+'/'+syst+'_'+signal+'.png')
		canv.SaveAs(tempVersion+'/'+saveDir+'/'+syst+'_'+signal+'.eps')
	RFile.Close()

