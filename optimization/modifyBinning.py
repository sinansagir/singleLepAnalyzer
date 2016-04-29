#!/usr/bin/python

import os,sys,time,math,fnmatch
from array import array
from ROOT import *

cutString = 'lep40_MET75_1jet300_2jet150_NJets3_NBJets0_3jet100_4jet0_5jet0_DR1_1Wjet0_1bjet0_HT0_ST0_minMlb0'
templateDir = os.getcwd()+'/templates_minMlb_tau21LT0p6_tptp_2016_3_4/'

rebinHists = True
xbinsList = {}
xbinsList['isE_nT0p_nW0_nB0']  = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 640.0, 672.0, 688.0, 720.0, 736.0, 752.0, 784.0, 800.0]
xbinsList['isE_nT0p_nW0_nB1']  = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
xbinsList['isE_nT0p_nW0_nB2']  = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 800.0]
xbinsList['isE_nT0p_nW0_nB2p'] = xbinsList['isE_nT0p_nW0_nB2']
xbinsList['isE_nT0p_nW0_nB3p'] = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 208.0, 256.0, 400.0, 800.0]
xbinsList['isE_nT0p_nW1p_nB0'] = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 608.0, 656.0, 704.0, 752.0, 800.0]
xbinsList['isE_nT0p_nW1p_nB1'] = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0]
xbinsList['isE_nT0p_nW1p_nB2'] = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 496.0, 800.0]
xbinsList['isE_nT0p_nW1p_nB2p']= xbinsList['isE_nT0p_nW1p_nB2']
xbinsList['isE_nT0p_nW1p_nB3p']= [0.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 208.0, 272.0, 304.0, 800.0]
xbinsList['isM_nT0p_nW0_nB0']  = xbinsList['isE_nT0p_nW0_nB0']
xbinsList['isM_nT0p_nW0_nB1']  = xbinsList['isE_nT0p_nW0_nB1']
xbinsList['isM_nT0p_nW0_nB2']  = xbinsList['isE_nT0p_nW0_nB2']
xbinsList['isM_nT0p_nW0_nB2p'] = xbinsList['isE_nT0p_nW0_nB2p']
xbinsList['isM_nT0p_nW0_nB3p'] = xbinsList['isE_nT0p_nW0_nB3p']
xbinsList['isM_nT0p_nW1p_nB0'] = xbinsList['isE_nT0p_nW1p_nB0']
xbinsList['isM_nT0p_nW1p_nB1'] = xbinsList['isE_nT0p_nW1p_nB1']
xbinsList['isM_nT0p_nW1p_nB2'] = xbinsList['isE_nT0p_nW1p_nB2']
xbinsList['isM_nT0p_nW1p_nB2p']= xbinsList['isE_nT0p_nW1p_nB2p'] 
xbinsList['isM_nT0p_nW1p_nB3p']= xbinsList['isE_nT0p_nW1p_nB3p']

normalizeRENORM = True
normalizePDF    = True
removalKeys = {} # True == keep, False == remove
removalKeys['muR__']       = True
removalKeys['muF__']       = True
removalKeys['muRFcorrd__'] = True
removalKeys['muRFenv__']   = True
removalKeys['toppt__']     = True
removalKeys['jmr__']       = True
removalKeys['jms__']       = True
removalKeys['tau21__']     = True
removalKeys['jsf__']       = True

xbins = {}
for key in xbinsList.keys(): xbins[key] = array('d', xbinsList[key])

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)
            
rfiles = [file for file in findfiles(templateDir+cutString, '*.root') if '00_2p318fb.root' in file]

tfile = {}
outputRfile = {}
iRfile=0
for file in rfiles: 
	print file
	tfile[iRfile] = TFile(file)	
	rebinnedHists = {}
	if rebinHists: outputRfile[iRfile] = TFile(file.replace('.root','_rebinned.root'),'RECREATE')
	else: outputRfile[iRfile] = TFile(file.replace('.root','_modified.root'),'RECREATE')
	for k in tfile[iRfile].GetListOfKeys():
		histName = k.GetName()
		if any([item in histName and not removalKeys[item] for item in removalKeys.keys()]): continue
		channel = histName[histName.find('is'):histName.find('__')]
		if rebinHists: rebinnedHists[histName]=tfile[iRfile].Get(histName).Rebin(len(xbins[channel])-1,histName,xbins[channel])
		else: rebinnedHists[histName]=tfile[iRfile].Get(histName).Clone()
		if 'sig__mu' in histName and normalizeRENORM: #normalize the renorm/fact shapes to nominal
			renormNomHist = tfile[iRfile].Get(histName[:histName.find('__mu')]).Clone()
			renormSysHist = tfile[iRfile].Get(histName).Clone()
			rebinnedHists[histName].Scale(renormNomHist.Integral()/renormSysHist.Integral())
		if 'sig__pdf' in histName and normalizePDF: #normalize the pdf shapes to nominal
			renormNomHist = tfile[iRfile].Get(histName[:histName.find('__pdf')]).Clone()
			renormSysHist = tfile[iRfile].Get(histName).Clone()
			rebinnedHists[histName].Scale(renormNomHist.Integral()/renormSysHist.Integral())
		if '__pdf' in histName:
			if '__pdf__' not in histName and '__pdfNew__' not in histName: continue
		rebinnedHists[histName].Write()
		
	muRUphists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'muR__plus' in k.GetName()]
	for hist in muRUphists:
		newMuRFName = 'muRFcorrdNew'
# 		if 'ewk' in hist: newMuRFName = 'muRFcorrdNewEWK'
# 		if 'top' in hist: newMuRFName = 'muRFcorrdNewTOP'
# 		if 'qcd' in hist: newMuRFName = 'muRFcorrdNewQCD'
# 		if 'sig' in hist: newMuRFName = 'muRFcorrdNewSIG'
		muRFcorrdNewUpHist = rebinnedHists[hist].Clone(hist.replace('muR__plus',newMuRFName+'__plus'))
		muRFcorrdNewDnHist = rebinnedHists[hist].Clone(hist.replace('muR__plus',newMuRFName+'__minus'))
		muRFdecorrdNewUpHist = rebinnedHists[hist].Clone(hist.replace('muR__plus','muRFdecorrdNew__plus'))
		muRFdecorrdNewDnHist = rebinnedHists[hist].Clone(hist.replace('muR__plus','muRFdecorrdNew__minus'))
		histList = [
			rebinnedHists[hist[:hist.find('__mu')]], #nominal
			rebinnedHists[hist], #renormWeights[4]
			rebinnedHists[hist.replace('muR__plus','muR__minus')], #renormWeights[2]
			rebinnedHists[hist.replace('muR__plus','muF__plus')], #renormWeights[1]
			rebinnedHists[hist.replace('muR__plus','muF__minus')], #renormWeights[0]
			rebinnedHists[hist.replace('muR__plus','muRFcorrd__plus')], #renormWeights[5]
			rebinnedHists[hist.replace('muR__plus','muRFcorrd__minus')] #renormWeights[3]
			]
		for ibin in range(1,histList[0].GetNbinsX()+1):
			weightList = [histList[ind].GetBinContent(ibin) for ind in range(len(histList))]		
			indCorrdUp = weightList.index(max(weightList))
			indCorrdDn = weightList.index(min(weightList))
			indDeCorrdUp = weightList.index(max(weightList[:-2]))
			indDeCorrdDn = weightList.index(min(weightList[:-2]))
			
			muRFcorrdNewUpHist.SetBinContent(ibin,histList[indCorrdUp].GetBinContent(ibin))
			muRFcorrdNewDnHist.SetBinContent(ibin,histList[indCorrdDn].GetBinContent(ibin))
			muRFdecorrdNewUpHist.SetBinContent(ibin,histList[indDeCorrdUp].GetBinContent(ibin))
			muRFdecorrdNewDnHist.SetBinContent(ibin,histList[indDeCorrdDn].GetBinContent(ibin))
			
			muRFcorrdNewUpHist.SetBinError(ibin,histList[indCorrdUp].GetBinError(ibin))
			muRFcorrdNewDnHist.SetBinError(ibin,histList[indCorrdDn].GetBinError(ibin))
			muRFdecorrdNewUpHist.SetBinError(ibin,histList[indDeCorrdUp].GetBinError(ibin))
			muRFdecorrdNewDnHist.SetBinError(ibin,histList[indDeCorrdDn].GetBinError(ibin))
		if 'sig__mu' in hist and normalizeRENORM: #normalize the renorm/fact shapes to nominal
			renormNomHist = tfile[iRfile].Get(hist[:hist.find('__mu')]).Clone()
			muRFcorrdNewUpHist.Scale(renormNomHist.Integral()/muRFcorrdNewUpHist.Integral())
			muRFcorrdNewDnHist.Scale(renormNomHist.Integral()/muRFcorrdNewDnHist.Integral())
			muRFdecorrdNewUpHist.Scale(renormNomHist.Integral()/muRFdecorrdNewUpHist.Integral())
			muRFdecorrdNewDnHist.Scale(renormNomHist.Integral()/muRFdecorrdNewDnHist.Integral())
		muRFcorrdNewUpHist.Write()
		muRFcorrdNewDnHist.Write()
		muRFdecorrdNewUpHist.Write()
		muRFdecorrdNewDnHist.Write()
		
	pdfUphists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'pdf__plus' in k.GetName()]
	for hist in pdfUphists:
		newPDFName = 'pdfNew'
# 		if 'ewk' in hist: newPDFName = 'pdfNewEWK'
# 		if 'top' in hist: newPDFName = 'pdfNewTOP'
# 		if 'qcd' in hist: newPDFName = 'pdfNewQCD'
# 		if 'sig' in hist: newPDFName = 'pdfNewSIG'
		pdfNewUpHist = rebinnedHists[hist].Clone(hist.replace('pdf__plus',newPDFName+'__plus'))
		pdfNewDnHist = rebinnedHists[hist].Clone(hist.replace('pdf__plus',newPDFName+'__minus'))
		for ibin in range(1,pdfNewUpHist.GetNbinsX()+1):
			weightList = [rebinnedHists[hist.replace('pdf__plus','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(100)]
			indPDFUp = sorted(range(len(weightList)), key=lambda k: weightList[k])[83]
			indPDFDn = sorted(range(len(weightList)), key=lambda k: weightList[k])[15]
			pdfNewUpHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf__plus','pdf'+str(indPDFUp))].GetBinContent(ibin))
			pdfNewDnHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf__plus','pdf'+str(indPDFDn))].GetBinContent(ibin))
			pdfNewUpHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf__plus','pdf'+str(indPDFUp))].GetBinError(ibin))
			pdfNewDnHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf__plus','pdf'+str(indPDFDn))].GetBinError(ibin))
		if 'sig__pdf' in hist and normalizePDF: #normalize the renorm/fact shapes to nominal
			renormNomHist = tfile[iRfile].Get(hist[:hist.find('__pdf')]).Clone()
			pdfNewUpHist.Scale(renormNomHist.Integral()/pdfNewUpHist.Integral())
			pdfNewDnHist.Scale(renormNomHist.Integral()/pdfNewDnHist.Integral())
		pdfNewUpHist.Write()
		pdfNewDnHist.Write()
		
	outputRfile[iRfile].Close()
	tfile[iRfile].Close()
 	iRfile+=1
 	
print "Total root files modified:", iRfile 




