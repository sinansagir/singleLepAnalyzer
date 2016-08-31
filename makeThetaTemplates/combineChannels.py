#!/usr/bin/python

import os,sys,time,math,fnmatch
from array import array
from ROOT import *

cutString = 'Selectionfile'
templateDir = os.getcwd()+'/ttags_'+sys.argv[1]+'_2016_6_13/'

rebinHists = True
xbinsList = {}
xbinsList['isE_nT0_nW0_nB0']    = [0.0, 32.0, 48.0, 64.0, 80.0, 96.0, 112.0, 128.0, 144.0, 160.0, 176.0, 192.0, 208.0, 224.0, 240.0, 256.0, 272.0, 288.0, 304.0, 320.0, 336.0, 352.0, 368.0, 384.0, 400.0, 416.0, 432.0, 448.0, 464.0, 480.0, 496.0, 512.0, 528.0, 544.0, 560.0, 576.0, 592.0, 608.0, 624.0, 640.0, 656.0, 672.0, 688.0, 704.0, 720.0, 736.0, 752.0, 768.0, 784.0, 800.0] 
xbinsList['isE_nT0_nW0_nB1']   = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT0_nW0_nB2']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT0_nW0_nB3p']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT0_nW1p_nB0']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT0_nW1p_nB1']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT0_nW1p_nB2'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT0_nW1p_nB3p'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT1p_nW0_nB0']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT1p_nW0_nB1']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT1p_nW0_nB2'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT1p_nW0_nB3p'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT1p_nW1p_nB0'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT1p_nW1p_nB1'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT1p_nW1p_nB2']= xbinsList['isE_nT0_nW0_nB0']
xbinsList['isE_nT1p_nW1p_nB3p']= xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT0_nW0_nB0']   = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT0_nW0_nB1']   = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT0_nW0_nB2']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT0_nW0_nB3p']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT0_nW1p_nB0']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT0_nW1p_nB1']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT0_nW1p_nB2'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT0_nW1p_nB3p'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT1p_nW0_nB0']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT1p_nW0_nB1']  = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT1p_nW0_nB2'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT1p_nW0_nB3p'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT1p_nW1p_nB0'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT1p_nW1p_nB1'] = xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT1p_nW1p_nB2']= xbinsList['isE_nT0_nW0_nB0']
xbinsList['isM_nT1p_nW1p_nB3p']= xbinsList['isE_nT0_nW0_nB0']

normalizeRENORM = True
normalizePDF    = True
removalKeys = {} # True == keep, False == remove
removalKeys['muR__']       = False
removalKeys['muF__']       = False
removalKeys['muRFcorrd__'] = False
removalKeys['muRFenv__']   = False
removalKeys['toppt__']     = True
removalKeys['tau21__']     = True
removalKeys['jsf__']       = True

xbins = {}
for key in xbinsList.keys(): xbins[key] = array('d', xbinsList[key])

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)
            
rfiles = [file for file in findfiles(templateDir+cutString, '*.root') if '_rebinned' not in file]

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
                if 'nT1p_nW0_' in histName or 'nT1p_nW1p_' in histName: continue
                rebinnedHists[histName].Write()

        ET1W0B0hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isE_nT1p_nW0_nB0' in k.GetName()]
        ET1W0B1hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isE_nT1p_nW0_nB1' in k.GetName()]
        ET1W0B2hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isE_nT1p_nW0_nB2' in k.GetName()]
        ET1W0B3hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isE_nT1p_nW0_nB3p' in k.GetName()]
        ET1W1B0hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isE_nT1p_nW1p_nB0' in k.GetName()]
        ET1W1B1hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isE_nT1p_nW1p_nB1' in k.GetName()]
        ET1W1B2hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isE_nT1p_nW1p_nB2' in k.GetName()]
        ET1W1B3hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isE_nT1p_nW1p_nB3p' in k.GetName()]
        MT1W0B0hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isM_nT1p_nW0_nB0' in k.GetName()]
        MT1W0B1hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isM_nT1p_nW0_nB1' in k.GetName()]
        MT1W0B2hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isM_nT1p_nW0_nB2' in k.GetName()]
        MT1W0B3hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isM_nT1p_nW0_nB3p' in k.GetName()]
        MT1W1B0hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isM_nT1p_nW1p_nB0' in k.GetName()]
        MT1W1B1hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isM_nT1p_nW1p_nB1' in k.GetName()]
        MT1W1B2hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isM_nT1p_nW1p_nB2' in k.GetName()]
        MT1W1B3hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'isM_nT1p_nW1p_nB3p' in k.GetName()]

        if len(ET1W1B0hists) > len(ET1W0B0hists): print 'E: W1 B0 > W0 B0'
        if len(ET1W1B1hists) > len(ET1W0B1hists): print 'E: W1 B1 > W0 B1'
        if len(ET1W1B2hists) > len(ET1W0B2hists): print 'E: W1 B2 > W0 B2'
        if len(ET1W0B3hists) > len(ET1W0B2hists): print 'E: W0 B3 > W0 B2'
        if len(ET1W1B3hists) > len(ET1W0B2hists): print 'E: W1 B3 > W0 B2'
        if len(MT1W1B0hists) > len(MT1W0B0hists): print 'M: W1 B0 > W0 B0'
        if len(MT1W1B1hists) > len(MT1W0B1hists): print 'M: W1 B1 > W0 B1'
        if len(MT1W1B2hists) > len(MT1W0B2hists): print 'M: W1 B2 > W0 B2'
        if len(MT1W0B3hists) > len(MT1W0B2hists): print 'M: W0 B3 > W0 B2'
        if len(MT1W1B3hists) > len(MT1W0B2hists): print 'M: W1 B3 > W0 B2'

        for ihist in range(0, len(ET1W0B0hists)):
            #print '--------------------------------------------'
            oldHist1 = ET1W0B0hists[ihist]
            #print oldHist1
            oldHist2 = oldHist1.replace('nW0','nW1p')
            #print oldHist2
            newT1name = oldHist1.replace('isE_nT1p_nW0_nB0','isE_nT1p_nW0p_nB0')
            rebinnedHists[newT1name] = rebinnedHists[oldHist1].Clone(newT1name)
            try: rebinnedHists[newT1name].Add(rebinnedHists[oldHist2])
            except: pass
            if '__pdf' in newT1name and ('__pdf__' not in newT1name and '__pdfNew__' not in newT1name): continue
            rebinnedHists[newT1name].Write()

        for ihist in range(0, len(ET1W0B1hists)):
            #print '--------------------------------------------'
            oldHist1 = ET1W0B1hists[ihist]
            #print oldHist1
            oldHist2 = oldHist1.replace('nW0','nW1p')
            #print oldHist2
            newT1name = oldHist1.replace('isE_nT1p_nW0_nB1','isE_nT1p_nW0p_nB1')
            rebinnedHists[newT1name] = rebinnedHists[oldHist1].Clone(newT1name)
            try: rebinnedHists[newT1name].Add(rebinnedHists[oldHist2])
            except: pass
            if '__pdf' in newT1name and ('__pdf__' not in newT1name and '__pdfNew__' not in newT1name): continue
            rebinnedHists[newT1name].Write()
        
        for ihist in range(0, len(ET1W0B2hists)):
            oldHist1 = ET1W0B2hists[ihist]
            oldHist2 = oldHist1.replace('nW0','nW1p')
            oldHist3 = oldHist1.replace('nW0_nB2','nW0_nB3p')
            oldHist4 = oldHist1.replace('nW0_nB2','nW1p_nB3p')
            newT1name = oldHist1.replace('isE_nT1p_nW0_nB2','isE_nT1p_nW0p_nB2p')
            rebinnedHists[newT1name] = rebinnedHists[oldHist1].Clone(newT1name)
            try: rebinnedHists[newT1name].Add(rebinnedHists[oldHist2])
            except: pass
            try: rebinnedHists[newT1name].Add(rebinnedHists[oldHist3])
            except: pass
            try: rebinnedHists[newT1name].Add(rebinnedHists[oldHist4])
            except: pass
            if '__pdf' in newT1name and ('__pdf__' not in newT1name and '__pdfNew__' not in newT1name): continue
            rebinnedHists[newT1name].Write()

        for ihist in range(0, len(MT1W0B0hists)):
            #print '--------------------------------------------'
            oldHist1 = MT1W0B0hists[ihist]
            #print oldHist1
            oldHist2 = oldHist1.replace('nW0','nW1p')
            #print oldHist2
            newT1name = oldHist1.replace('isM_nT1p_nW0_nB0','isM_nT1p_nW0p_nB0')
            rebinnedHists[newT1name] = rebinnedHists[oldHist1].Clone(newT1name)
            try: rebinnedHists[newT1name].Add(rebinnedHists[oldHist2])
            except: pass
            if '__pdf' in newT1name and ('__pdf__' not in newT1name and '__pdfNew__' not in newT1name): continue
            rebinnedHists[newT1name].Write()

        for ihist in range(0, len(MT1W0B1hists)):
            #print '--------------------------------------------'
            oldHist1 = MT1W0B1hists[ihist]
            #print oldHist1
            oldHist2 = oldHist1.replace('nW0','nW1p')
            #print oldHist2
            newT1name = oldHist1.replace('isM_nT1p_nW0_nB1','isM_nT1p_nW0p_nB1')
            rebinnedHists[newT1name] = rebinnedHists[oldHist1].Clone(newT1name)
            try: rebinnedHists[newT1name].Add(rebinnedHists[oldHist2])
            except: pass
            if '__pdf' in newT1name and ('__pdf__' not in newT1name and '__pdfNew__' not in newT1name): continue
            rebinnedHists[newT1name].Write()
        
        for ihist in range(0, len(MT1W0B2hists)):
            oldHist1 = MT1W0B2hists[ihist]
            oldHist2 = oldHist1.replace('nW0','nW1p')
            oldHist3 = oldHist1.replace('nW0_nB2','nW0_nB3p')
            oldHist4 = oldHist1.replace('nW0_nB2','nW1p_nB3p')
            newT1name = oldHist1.replace('isM_nT1p_nW0_nB2','isM_nT1p_nW0p_nB2p')
            rebinnedHists[newT1name] = rebinnedHists[oldHist1].Clone(newT1name)
            try: rebinnedHists[newT1name].Add(rebinnedHists[oldHist2])
            except: pass
            try: rebinnedHists[newT1name].Add(rebinnedHists[oldHist3])
            except: pass
            try: rebinnedHists[newT1name].Add(rebinnedHists[oldHist4])
            except: pass
            if '__pdf' in newT1name and ('__pdf__' not in newT1name and '__pdfNew__' not in newT1name): continue
            rebinnedHists[newT1name].Write()

            
	muRUphists = [hist for hist in rebinnedHists if 'muR__plus' in hist]
	for hist in muRUphists:
		newMuRFName = 'muRFcorrdNew'
		muRFcorrdNewUpHist = rebinnedHists[hist].Clone(hist.replace('muR__plus',newMuRFName+'__plus'))
		muRFcorrdNewDnHist = rebinnedHists[hist].Clone(hist.replace('muR__plus',newMuRFName+'__minus'))

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
			
			muRFcorrdNewUpHist.SetBinContent(ibin,histList[indCorrdUp].GetBinContent(ibin))
			muRFcorrdNewDnHist.SetBinContent(ibin,histList[indCorrdDn].GetBinContent(ibin))
			
			muRFcorrdNewUpHist.SetBinError(ibin,histList[indCorrdUp].GetBinError(ibin))
			muRFcorrdNewDnHist.SetBinError(ibin,histList[indCorrdDn].GetBinError(ibin))
		if 'sig__mu' in hist and normalizeRENORM: #normalize the renorm/fact shapes to nominal
			renormNomHist = rebinnedHists[hist[:hist.find('__mu')]].Clone()
			muRFcorrdNewUpHist.Scale(renormNomHist.Integral()/muRFcorrdNewUpHist.Integral())
			muRFcorrdNewDnHist.Scale(renormNomHist.Integral()/muRFcorrdNewDnHist.Integral())
                if 'nT1p_nW0_' in hist or 'nT1p_nW1p_' in hist: continue
		muRFcorrdNewUpHist.Write()
		muRFcorrdNewDnHist.Write()
		
	pdfUphists = [hist for hist in rebinnedHists if 'pdf0' in hist]
	for hist in pdfUphists:
		newPDFName = 'pdfNew'
		pdfNewUpHist = rebinnedHists[hist].Clone(hist.replace('pdf0',newPDFName+'__plus'))
		pdfNewDnHist = rebinnedHists[hist].Clone(hist.replace('pdf0',newPDFName+'__minus'))
		for ibin in range(1,pdfNewUpHist.GetNbinsX()+1):
			weightList = [rebinnedHists[hist.replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(100)]
			indPDFUp = sorted(range(len(weightList)), key=lambda k: weightList[k])[83]
			indPDFDn = sorted(range(len(weightList)), key=lambda k: weightList[k])[15]
			pdfNewUpHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinContent(ibin))
			pdfNewDnHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinContent(ibin))
			pdfNewUpHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinError(ibin))
			pdfNewDnHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinError(ibin))
		if 'sig__pdf' in hist and normalizePDF: #normalize the renorm/fact shapes to nominal
			renormNomHist = rebinnedHists[hist[:hist.find('__pdf')]].Clone()
			pdfNewUpHist.Scale(renormNomHist.Integral()/pdfNewUpHist.Integral())
			pdfNewDnHist.Scale(renormNomHist.Integral()/pdfNewDnHist.Integral())
                if 'nT1p_nW0_' in hist or 'nT1p_nW1p_' in hist: continue
		pdfNewUpHist.Write()
		pdfNewDnHist.Write()
		
	outputRfile[iRfile].Close()
	tfile[iRfile].Close()
 	iRfile+=1
 	
print "Total root files modified:", iRfile 




