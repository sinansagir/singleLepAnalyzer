#!/usr/bin/python

import os,sys,time,math,pickle,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import ROOT as rt
#from weights import *
from modSyst import *
from utils import *
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)
start_time = time.time()

year='R18'
if year=='R17':
	from weights17 import *
	lumi=41.5 #for plots
else:
	from weights18 import *
	lumi=59.97 #for plots
lumiInTemplates= str(targetlumi/1000).replace('.','p') # 1/fb

region='SR' #PS,SR,TTCR,WJCR
isCategorized=0
iPlot='HT_vs_HTb'
if len(sys.argv)>1: iPlot=str(sys.argv[1])
cutString=''
if region=='SR': pfix='templates_'+year
elif region=='WJCR': pfix='wjets_'+year
elif region=='TTCR': pfix='ttbar_'+year
if not isCategorized: pfix='kinematics_'+region+'_'+year
templateDir=os.getcwd()+'/'+pfix+'_nonjetsf_2d_2020_9_3/'+cutString+'/'

isRebinned=''#'_rebinned_stat0p3' #post for ROOT file names
saveKey = '' # tag for plot names

sig='tttt' #  choose the 1st signal to plot
sigleg='t#bar{t}t#bar{t}'
scaleSignalsToXsec = False # !!!!!Make sure you know signal x-sec used in input files to this script. If this is True, it will scale signal histograms by x-sec in weights.py!!!!!
scaleSignals = False
sigScaleFact = 10 #put -1 if auto-scaling wanted
useCombineTemplates = True
sigfile='templates_'+iPlot+'_'+sig+'_'+lumiInTemplates+'fb'+isRebinned+'.root'

ttProcList = ['ttnobb','ttbb'] # ['ttjj','ttcc','ttbb','ttbj']
if iPlot=='HTYLD': ttProcList = ['ttbb','ttnobb']
bkgProcList = ttProcList+['top','ewk','qcd']

yLog  = False

isEMlist  = ['E','M']

if useCombineTemplates:
	sigName = sig
	dataName = 'data_obs'
	sigfile = sigfile.replace(sig+'_','')
else: #theta
	sigName = 'sig'
	dataName = 'DATA'
if not os.path.exists(templateDir+sigfile):
	print "ERROR: File does not exits: "+templateDir+sigfile
	os._exit(1)
print "READING: "+templateDir+sigfile
RFile = rt.TFile(templateDir+sigfile)

datahists = [k.GetName() for k in RFile.GetListOfKeys() if '__'+dataName in k.GetName()]
catsElist = [hist[hist.find('fb_')+3:hist.find('__')] for hist in datahists if 'isE_' in hist]

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= str(lumi)+" fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref

iPeriod = 4 #see CMS_lumi.py module for usage!

# references for T, B, L, R
T = 0.10*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.12*W_ref

tagPosX = 0.76
tagPosY = 0.62

bkghists = {}
bkghistsmerged = {}
for catEStr in catsElist:
	for isEM in isEMlist:
		histPrefix=iPlot+'_'+lumiInTemplates+'fb_'
		catStr=catEStr.replace('isE','is'+isEM)
		histPrefix+=catStr
		print histPrefix
		for proc in bkgProcList: 
			try: bkghists[proc+catStr] = RFile.Get(histPrefix+'__'+proc).Clone()
			except:
				print "There is no "+proc+"!!!!!!!!"
				print "Skipping "+proc+"....."
				pass
		hData = RFile.Get(histPrefix+'__'+dataName).Clone()
		hsig = RFile.Get(histPrefix+'__'+sigName).Clone(histPrefix+'__'+sigName)
		if scaleSignalsToXsec: hsig.Scale(xsec[sig])

		totBkg = bkghists[bkgProcList[0]+catStr].Clone()
		for proc in bkgProcList:
			if proc==bkgProcList[0]: continue
			try: totBkg.Add(bkghists[proc+catStr])
			except: pass
			
		hSoB = hsig.Clone('SoB')
		for binx in range(1,hSoB.GetNbinsX()+1):
			for biny in range(1,hSoB.GetNbinsY()+1):
				hSoB.SetBinContent(binx,biny,1,hsig.GetBinContent(binx,biny)/(math.sqrt(totBkg.GetBinContent(binx,biny))+1E-12))
		
		c1 = rt.TCanvas("c1","c1",50,50,W,H)
		c1.SetFillColor(0)
		c1.SetBorderMode(0)
		c1.SetFrameFillStyle(0)
		c1.SetFrameBorderMode(0)
		#c1.SetTickx(0)
		#c1.SetTicky(0)
		c1.SetLeftMargin( L/W )
		c1.SetRightMargin( R/W )
		c1.SetTopMargin( T/H )
		c1.SetBottomMargin( B/H )

		hsig.Draw("COLZ")
	
		chLatex = rt.TLatex()
		chLatex.SetNDC()
		chLatex.SetTextSize(0.04)
		chLatex.SetTextAlign(21) # align center
		tagString = ''
		tagString2 = ''
		flvString='e+jets'
		if isEM=='M': flvString='#mu+jets'
		nJ = catStr.split('_')[-1].replace('nJ','')
		nB = catStr.split('_')[-2].replace('nB','')
		nW = catStr.split('_')[-3].replace('nW','')
		nT = catStr.split('_')[-4].replace('nT','')
		nHOT = catStr.split('_')[-5].replace('nHOT','')
		if nHOT!='0p': 
			if 'p' in nHOT: tagString2+='#geq'+nHOT[:-1]+' resolved t'
			else: tagString2+=nHOT+' resolved t'
		if nT!='0p': 
			if 'p' in nT: tagString+='#geq'+nT[:-1]+' t, '
			else: tagString+=nT+' t, '
		if nW!='0p': 
			if 'p' in nW: tagString+='#geq'+nW[:-1]+' W, '
			else: tagString+=nW+' W, '
		if nB!='0p': 
			if 'p' in nB: tagString+='#geq'+nB[:-1]+' b, '
			else: tagString+=nB+' b, '
		if nJ!='0p': 
			if 'p' in nJ: tagString+='#geq'+nJ[:-1]+' j'
			else: tagString+=nJ+' j'
		if tagString.endswith(', '): tagString = tagString[:-2]
		chLatex.DrawLatex(tagPosX, tagPosY, flvString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)

		#draw the lumi text on the canvas
		CMS_lumi.CMS_lumi(c1, iPeriod, iPos)

		#c1.Write()
		savePrefix = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
		if not os.path.exists(savePrefix): os.system('mkdir '+savePrefix)
		savePrefix+=histPrefix+isRebinned+saveKey
		savePrefix=savePrefix.replace('nHOT0p_','').replace('nT0p_','').replace('nW0p_','').replace('nB0p_','').replace('nJ0p_','').replace('_rebinned_stat1p1','')
		if yLog: savePrefix+='_logy'

		hSoB.Draw("COLZ")
		chLatex.DrawLatex(tagPosX, tagPosY, flvString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)
		CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
		c1.SaveAs(savePrefix+'_SoB.png')
		
		hsig.Draw("COLZ")
		chLatex.DrawLatex(tagPosX, tagPosY, flvString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)
		CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
		c1.SaveAs(savePrefix+'_tttt.png')

		hData.Draw("COLZ")
		chLatex.DrawLatex(tagPosX, tagPosY, flvString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)
		CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
		c1.SaveAs(savePrefix+'_data.png')

		totBkg.Draw("COLZ")
		chLatex.DrawLatex(tagPosX, tagPosY, flvString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
		chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)
		CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
		c1.SaveAs(savePrefix+'_bkg.png')
		for proc in bkgProcList:
			try:
				bkghists[proc+catStr].Draw("COLZ")
				chLatex.DrawLatex(tagPosX, tagPosY, flvString)
				chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
				chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)
				CMS_lumi.CMS_lumi(c1, iPeriod, iPos)
				c1.SaveAs(savePrefix+'_'+proc+'.png')
			except: pass
# 		c1.SaveAs(savePrefix+'.pdf')
# 		c1.SaveAs(savePrefix+'.eps')
# 		c1.SaveAs(savePrefix+'.root')
# 		c1.SaveAs(savePrefix+'.C')

		for proc in bkgProcList:
			try: del bkghists[proc+catStr]
			except: pass
					
	# Making plots for e+jets/mu+jets combined #
	histPrefixE = iPlot+'_'+lumiInTemplates+'fb_'+catEStr
	histPrefixM = iPlot+'_'+lumiInTemplates+'fb_'+catEStr.replace('isE','isM')
	catLStr = catEStr.replace('isE','isL')
	for proc in bkgProcList:
		try: 
			bkghistsmerged[proc+catLStr] = RFile.Get(histPrefixE+'__'+proc).Clone()
			bkghistsmerged[proc+catLStr].Add(RFile.Get(histPrefixM+'__'+proc))
		except:pass
	hDatamerged = RFile.Get(histPrefixE+'__'+dataName).Clone()
	hDatamerged.Add(RFile.Get(histPrefixM+'__'+dataName).Clone())
	hsigmerged = RFile.Get(histPrefixE+'__'+sigName).Clone(histPrefixE+'__'+sigName+'merged')
	hsigmerged.Add(RFile.Get(histPrefixM+'__'+sigName).Clone())

	totBkgmerged = bkghistsmerged[bkgProcList[0]+catLStr].Clone()
	for proc in bkgProcList[1:]:
		try: totBkgmerged.Add(bkghistsmerged[proc+catLStr])
		except: pass

	hSoBmerged = hsigmerged.Clone('SoB')
	for binx in range(1,hSoBmerged.GetNbinsX()+1):
		for biny in range(1,hSoBmerged.GetNbinsY()+1):
			hSoBmerged.SetBinContent(binx,biny,1,hsigmerged.GetBinContent(binx,biny)/(math.sqrt(totBkgmerged.GetBinContent(binx,biny))+1E-12))

	c1merged = rt.TCanvas("c1merged","c1merged",50,50,W,H)
	c1merged.SetFillColor(0)
	c1merged.SetBorderMode(0)
	c1merged.SetFrameFillStyle(0)
	c1merged.SetFrameBorderMode(0)
	#c1merged.SetTickx(0)
	#c1merged.SetTicky(0)
	c1merged.SetLeftMargin( L/W )
	c1merged.SetRightMargin( R/W )
	c1merged.SetTopMargin( T/H )
	c1merged.SetBottomMargin( B/H )

	hsigmerged.Draw("COLZ")

	chLatexmerged = rt.TLatex()
	chLatexmerged.SetNDC()
	chLatexmerged.SetTextSize(0.04)
	chLatexmerged.SetTextAlign(21) # align center
	flvString = 'e/#mu+jets'
	chLatexmerged.DrawLatex(tagPosX, tagPosY, flvString)
	chLatexmerged.DrawLatex(tagPosX, tagPosY-0.06, tagString)
	chLatexmerged.DrawLatex(tagPosX, tagPosY-0.12, tagString2)

	#draw the lumi text on the canvas
	CMS_lumi.CMS_lumi(c1merged, iPeriod, iPos)
	
	#c1merged.Write()
	savePrefixmerged = templateDir.replace(cutString,'')+templateDir.split('/')[-2]+'plots/'
	if not os.path.exists(savePrefixmerged): os.system('mkdir '+savePrefixmerged)
	savePrefixmerged+=histPrefixE.replace('isE','isL')+isRebinned+saveKey
	savePrefixmerged=savePrefixmerged.replace('nHOT0p_','').replace('nT0p_','').replace('nW0p_','').replace('nB0p_','').replace('nJ0p_','').replace('_rebinned_stat1p1','')
	if yLog: savePrefixmerged+='_logy'

	hSoBmerged.Draw("COLZ")
	chLatex.DrawLatex(tagPosX, tagPosY, flvString)
	chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
	chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)
	CMS_lumi.CMS_lumi(c1merged, iPeriod, iPos)
	c1merged.SaveAs(savePrefixmerged+'_SoB.png')

	hsigmerged.Draw("COLZ")
	chLatex.DrawLatex(tagPosX, tagPosY, flvString)
	chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
	chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)
	CMS_lumi.CMS_lumi(c1merged, iPeriod, iPos)
	c1merged.SaveAs(savePrefixmerged+'_tttt.png')

	hDatamerged.Draw("COLZ")
	chLatex.DrawLatex(tagPosX, tagPosY, flvString)
	chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
	chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)
	CMS_lumi.CMS_lumi(c1merged, iPeriod, iPos)
	c1merged.SaveAs(savePrefixmerged+'_data.png')

	totBkgmerged.Draw("COLZ")
	chLatex.DrawLatex(tagPosX, tagPosY, flvString)
	chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
	chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)
	CMS_lumi.CMS_lumi(c1merged, iPeriod, iPos)
	c1merged.SaveAs(savePrefixmerged+'_bkg.png')
	for proc in bkgProcList:
		try:
			bkghistsmerged[proc+catLStr].Draw("COLZ")
			chLatex.DrawLatex(tagPosX, tagPosY, flvString)
			chLatex.DrawLatex(tagPosX, tagPosY-0.06, tagString)
			chLatex.DrawLatex(tagPosX, tagPosY-0.12, tagString2)
			CMS_lumi.CMS_lumi(c1merged, iPeriod, iPos)
			c1merged.SaveAs(savePrefixmerged+'_'+proc+'.png')
		except: pass
# 	c1merged.SaveAs(savePrefixmerged+'.pdf')
# 	c1merged.SaveAs(savePrefixmerged+'.eps')
# 	c1merged.SaveAs(savePrefixmerged+'.root')
# 	c1merged.SaveAs(savePrefixmerged+'.C')
	
	for proc in bkgProcList:
		try: del bkghistsmerged[proc+catLStr]
		except: pass
			
RFile.Close()

print("--- %s minutes ---" % (round(time.time() - start_time, 2)/60))


