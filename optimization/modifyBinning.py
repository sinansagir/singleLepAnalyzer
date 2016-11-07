#!/usr/bin/python

import os,sys,time,math,fnmatch
from array import array
from ROOT import *
start_time = time.time()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Run as:
# > python modifyBinning.py
# 
# Optional arguments:
# -- statistical uncertainty threshold (default is 30%)
#
# Notes:
# -- Finds certain root files in a given directory and rebins all histograms in each file
# -- A selection of subset of files in the input directory can be done below under "#Setup the selection ..."
# -- A custom binning choice can also be given below and this choice can be activated by giving a stat unc 
#    threshold larger than 100% (>1.) in the argument
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#cutString = 'lep50_MET150_NJets4_NBJets0_DR1_1jet450_2jet150_3jet0'
templateDir = os.getcwd()+'/templates_minMlb_2016_10_27/'#+cutString
combFile = 'templates_minMlb_2p318fb.root'
rebinCombine = False #else rebins theta tempaltes
normalizeRENORM = True #does it only for signals
normalizePDF    = True #does it only for signals
verbosity = 0

stat = 0.3 # 30% statistical uncertainty requirement
if len(sys.argv)>1: stat=float(sys.argv[1])

if rebinCombine:
	dataName = 'data_obs'
	upTag = 'Up'
	downTag = 'Down'
else: #theta
	dataName = 'DATA'
	upTag = '__plus'
	downTag = '__minus'

cutStrings = [x for x in os.walk(templateDir).next()[1]]

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

ind = 0
for cutString in cutStrings:
	if (ind % 500)==0: print "Finished",ind,"out of",len(cutStrings) 
	ind+=1
	#Setup the selection of the files to be rebinned:          
	rfiles = [file for file in findfiles(templateDir+cutString, '*.root') if 'rebinned' not in file and 'plots' not in file and ('_X53X53M700left_' in file or '_X53X53M800left_' in file or '_X53X53M900left_' in file or '_X53X53M1000left_' in file or '_X53X53M1100left_' in file or '_X53X53M1200left_' in file)]
	if rebinCombine: 
		rfiles = [templateDir+cutString+'/'+combFile]
		if ind>0: break

	if not len(rfiles)>0:
		print cutString
		continue
	tfile = TFile(rfiles[0])
	datahists = [k.GetName() for k in tfile.GetListOfKeys() if '__'+dataName in k.GetName()]
	channels = [hist[hist.find('fb_')+3:hist.find('__')] for hist in datahists]
	allhists = {chn:[hist.GetName() for hist in tfile.GetListOfKeys() if chn in hist.GetName()] for chn in channels}

	totBkgHists = {}
	for hist in datahists:
		channel = hist[hist.find('fb_')+3:hist.find('__')]
		totBkgHists[channel]=tfile.Get(hist.replace('__'+dataName,'__top')).Clone()
		try: totBkgHists[channel].Add(tfile.Get(hist.replace('__'+dataName,'__ewk')))
		except: pass
		try: totBkgHists[channel].Add(tfile.Get(hist.replace('__'+dataName,'__qcd')))
		except: pass

	xbinsListTemp = {}
	for chn in totBkgHists.keys():
		if 'isE' not in chn: continue
		xbinsListTemp[chn]=[tfile.Get(datahists[0]).GetXaxis().GetBinUpEdge(tfile.Get(datahists[0]).GetXaxis().GetNbins())]
		Nbins = tfile.Get(datahists[0]).GetNbinsX()
		totTempBinContent_E = 0.
		totTempBinContent_M = 0.
		totTempBinErrSquared_E = 0.
		totTempBinErrSquared_M = 0.
		for iBin in range(1,Nbins+1):
			totTempBinContent_E += totBkgHists[chn].GetBinContent(Nbins+1-iBin)
			totTempBinContent_M += totBkgHists[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
			totTempBinErrSquared_E += totBkgHists[chn].GetBinError(Nbins+1-iBin)**2
			totTempBinErrSquared_M += totBkgHists[chn.replace('isE','isM')].GetBinError(Nbins+1-iBin)**2
			if totTempBinContent_E>0. and totTempBinContent_M>0.:
				if math.sqrt(totTempBinErrSquared_E)/totTempBinContent_E<=stat and math.sqrt(totTempBinErrSquared_M)/totTempBinContent_M<=stat:
					totTempBinContent_E = 0.
					totTempBinContent_M = 0.
					totTempBinErrSquared_E = 0.
					totTempBinErrSquared_M = 0.
					xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))
		if xbinsListTemp[chn][-1]!=0: xbinsListTemp[chn].append(0)
		if totBkgHists[chn].GetBinContent(1)==0. or totBkgHists[chn.replace('isE','isM')].GetBinContent(1)==0.: 
			if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
		elif totBkgHists[chn].GetBinError(1)/totBkgHists[chn].GetBinContent(1)>stat or totBkgHists[chn.replace('isE','isM')].GetBinError(1)/totBkgHists[chn.replace('isE','isM')].GetBinContent(1)>stat: 
			if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
		xbinsListTemp[chn.replace('isE','isM')]=xbinsListTemp[chn]

	if verbosity:
		print "==> Here is the binning I found with",stat*100,"% uncertainty threshold: "
		print "//"*40
	if stat<=1.:
		xbinsList = {}
		for chn in xbinsListTemp.keys():
			xbinsList[chn] = []
			for bin in range(len(xbinsListTemp[chn])): xbinsList[chn].append(xbinsListTemp[chn][len(xbinsListTemp[chn])-1-bin])
			if verbosity: print chn,"=",xbinsList[chn]
	else: stat = 'Custom'
	if verbosity: print "//"*40

	xbins = {}
	for key in xbinsList.keys(): xbins[key] = array('d', xbinsList[key])

	#os._exit(1)

	iRfile=0
	for rfile in rfiles: 
		if verbosity: print "REBINNING FILE:",file
		tfiles = {}
		outputRfiles = {}
		tfiles[iRfile] = TFile(rfile)	
		outputRfiles[iRfile] = TFile(rfile.replace('.root','_rebinned_stat'+str(stat).replace('.','p')+'.root'),'RECREATE')

		if verbosity: print "==> I will use this binning choice to rebin original histograms:"
		if verbosity: print "PROGRESS:"
		for chn in channels:
			if verbosity: print "         ",chn
			rebinnedHists = {}
			#Rebinning histograms
			for hist in allhists[chn]:
				rebinnedHists[hist]=tfiles[iRfile].Get(hist).Rebin(len(xbins[chn])-1,hist,xbins[chn])
				rebinnedHists[hist].SetDirectory(0)
				if 'sig__mu' in hist and normalizeRENORM: #normalize the renorm/fact shapes to nominal
					renormNomHist = tfiles[iRfile].Get(hist[:hist.find('__mu')]).Clone()
					renormSysHist = tfiles[iRfile].Get(hist).Clone()
					rebinnedHists[hist].Scale(renormNomHist.Integral()/renormSysHist.Integral())
				if 'sig__pdf' in hist and normalizePDF: #normalize the pdf shapes to nominal
					renormNomHist = tfiles[iRfile].Get(hist[:hist.find('__pdf')]).Clone()
					renormSysHist = tfiles[iRfile].Get(hist).Clone()
					rebinnedHists[hist].Scale(renormNomHist.Integral()/renormSysHist.Integral())
				if '__pdf' in hist:
					if 'Up' not in hist or 'Down' not in hist: continue
				rebinnedHists[hist].Write()
			
			#Constructing muRF shapes
			muRUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'muR'+upTag in k.GetName() and chn in k.GetName()]
			for hist in muRUphists:
				newMuRFName = 'muRFcorrdNew'
				muRFcorrdNewUpHist = rebinnedHists[hist].Clone(hist.replace('muRUp',newMuRFName+upTag))
				muRFcorrdNewDnHist = rebinnedHists[hist].Clone(hist.replace('muRUp',newMuRFName+downTag))
				histList = [
					rebinnedHists[hist[:hist.find('__mu')]], #nominal
					rebinnedHists[hist], #renormWeights[4]
					rebinnedHists[hist.replace('muR'+upTag,'muR'+downTag)], #renormWeights[2]
					rebinnedHists[hist.replace('muR'+upTag,'muF'+upTag)], #renormWeights[1]
					rebinnedHists[hist.replace('muR'+upTag,'muF'+downTag)], #renormWeights[0]
					rebinnedHists[hist.replace('muR'+upTag,'muRFcorrd'+upTag)], #renormWeights[5]
					rebinnedHists[hist.replace('muR'+upTag,'muRFcorrd'+downTag)] #renormWeights[3]
					]
				for ibin in range(1,histList[0].GetNbinsX()+1):
					weightList = [histList[ind].GetBinContent(ibin) for ind in range(len(histList))]
					indCorrdUp = weightList.index(max(weightList))
					indCorrdDn = weightList.index(min(weightList))

					muRFcorrdNewUpHist.SetBinContent(ibin,histList[indCorrdUp].GetBinContent(ibin))
					muRFcorrdNewDnHist.SetBinContent(ibin,histList[indCorrdDn].GetBinContent(ibin))

					muRFcorrdNewUpHist.SetBinError(ibin,histList[indCorrdUp].GetBinError(ibin))
					muRFcorrdNewDnHist.SetBinError(ibin,histList[indCorrdDn].GetBinError(ibin))
				if 'sig__mu' in hist and normalizeRENORM: #normalize the renorm/fact shapes to nominal
					renormNomHist = tfiles[iRfile].Get(hist[:hist.find('__mu')]).Clone()
					muRFcorrdNewUpHist.Scale(renormNomHist.Integral()/muRFcorrdNewUpHist.Integral())
					muRFcorrdNewDnHist.Scale(renormNomHist.Integral()/muRFcorrdNewDnHist.Integral())
				muRFcorrdNewUpHist.Write()
				muRFcorrdNewDnHist.Write()

			#Constructing PDF shapes
			pdfUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'pdf0' in k.GetName() and chn in k.GetName()]
			for hist in pdfUphists:
				newPDFName = 'pdfNew'
				pdfNewUpHist = rebinnedHists[hist].Clone(hist.replace('pdf0',newPDFName+upTag))
				pdfNewDnHist = rebinnedHists[hist].Clone(hist.replace('pdf0',newPDFName+downTag))
				for ibin in range(1,pdfNewUpHist.GetNbinsX()+1):
					weightList = [rebinnedHists[hist.replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(100)]
					indPDFUp = sorted(range(len(weightList)), key=lambda k: weightList[k])[83]
					indPDFDn = sorted(range(len(weightList)), key=lambda k: weightList[k])[15]
					pdfNewUpHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinContent(ibin))
					pdfNewDnHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinContent(ibin))
					pdfNewUpHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinError(ibin))
					pdfNewDnHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinError(ibin))
				if 'sig__pdf' in hist and normalizePDF: #normalize the renorm/fact shapes to nominal
					renormNomHist = tfiles[iRfile].Get(hist[:hist.find('__pdf')]).Clone()
					pdfNewUpHist.Scale(renormNomHist.Integral()/pdfNewUpHist.Integral())
					pdfNewDnHist.Scale(renormNomHist.Integral()/pdfNewDnHist.Integral())
				pdfNewUpHist.Write()
				pdfNewDnHist.Write()

		tfiles[iRfile].Close()
		outputRfiles[iRfile].Close()
		iRfile+=1
	tfile.Close()
print ">> Done!"

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


