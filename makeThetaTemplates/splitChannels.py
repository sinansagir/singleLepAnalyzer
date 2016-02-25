#!/usr/bin/python

import os,sys,time,math,fnmatch
from array import array
from ROOT import *

cutString = 'lep40_MET75_1jet300_2jet150_NJets3_NBJets0_3jet100_4jet0_5jet0_DR1_1Wjet0_1bjet0_HT0_ST0_minMlb0'
templateDir = os.getcwd()+'/templates_minMlb_withShapes_2016_1_27_19_9_47/'

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)
            
rfiles = [file for file in findfiles(templateDir+cutString, '*.root') if '_rebinned.root' in file]# and '_minMlb300' in file]

normalizeRENORM = True
normalizePDF    = True
removalKeys = {} # True == keep, False == remove
removalKeys['muR__']       = False
removalKeys['muF__']       = False
removalKeys['muRFcorrd__'] = False
removalKeys['muRFenv__']   = False
removalKeys['muRFcorrdNew__'] = True
removalKeys['muRFdecorrdNew__'] = False
removalKeys['pdf__']       = False
removalKeys['pdfNew__']    = True
removalKeys['toppt__']     = True
removalKeys['jmr__']       = True
removalKeys['jms__']       = True
removalKeys['tau21__']     = True
removalKeys['jsf__']       = True
key1  = 'muR__'
key2  = 'muF__'
key3  = 'muRFcorrd__'
key4  = 'toppt__'
key5  = 'jmr__'
key6  = 'jms__'
key7  = 'tau21__'
keyJSF= 'jsf__'
keyE  = '_isE_'
keyM  = '_isM_'
keyW0 = '_nW0_'
keyW1p= '_nW1p_'
keyb0 = '_nB0_'
keyb1 = '_nB1_'
keyb2 = '_nB2_'
keyb3p= '_nB3p_'

tfile = {}
outputRfile = {}
iRfile=0
for file in rfiles:
	iRfile+=1
	tfile[iRfile] = TFile(file)
	if iRfile%100==0: print "FINISHED", iRfile, "out of", len(rfiles)
	#if os.path.exists(file.replace('.root','_modified.root')): continue
	#hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'sig__mu' not in k.GetName() and 'sig__pdf' not in k.GetName() and key1 not in k.GetName() and key2 not in k.GetName()] #correlated renorm/fact and removes uncertainties on signals
	#hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if 'sig__mu' not in k.GetName() and 'sig__pdf' not in k.GetName() and key3 not in k.GetName()] #uncorrelated renorm/fact and removes uncertainties on signals
	#hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if key1 not in k.GetName() and key2 not in k.GetName()] #correlated renorm/fact and keep uncertainties on signals
	#hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if key3 not in k.GetName()] #uncorrelated renorm/fact and keep uncertainties on signals
	
	hists = {}
	hists['newPDFandRF'] = [k.GetName() for k in tfile[iRfile].GetListOfKeys()]
# 	hists['noB0'] = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if keyb0 not in k.GetName()]
# 	hists['noJSF']= [k.GetName() for k in tfile[iRfile].GetListOfKeys() if keyJSF not in k.GetName()]
# 	hists['isE']  = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if keyE in k.GetName()]
# 	hists['isM']  = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if keyM in k.GetName()]
# 	hists['nB0']  = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if keyb0 in k.GetName()]
# 	hists['nB1']  = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if keyb1 in k.GetName()]
# 	hists['nB2']  = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if keyb2 in k.GetName()]
# 	hists['nB3p'] = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if keyb3p in k.GetName()]
# 	hists['nW0']  = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if keyW0 in k.GetName()]
# 	hists['nW1p'] = [k.GetName() for k in tfile[iRfile].GetListOfKeys() if keyW1p in k.GetName()]
	
	for key in hists.keys():
		outputRfile[str(iRfile)+key] = TFile(file.replace('.root','_'+key+'.root'),'RECREATE') #use someting more informative for "modified" here
		for hist in hists[key]:
			if '__pdf' in hist:
				if '__pdf__' not in hist and '__pdfNew__' not in hist: continue
			if any([item in hist and not removalKeys[item] for item in removalKeys.keys()]): continue
			if 'sig__mu' in hist: #normalize the renorm/fact shapes to nominal
				if normalizeRENORM:
					renormNomHist = tfile[iRfile].Get(hist[:hist.find('__mu')]).Clone()
					renormSysHist = tfile[iRfile].Get(hist).Clone()
					renormSysHist.Scale(renormNomHist.Integral()/renormSysHist.Integral())
					renormSysHist.Write()
				else: tfile[iRfile].Get(hist).Write()
			elif 'sig__pdf' in hist: #normalize the pdf shapes to nominal
				if normalizePDF:
					renormNomHist = tfile[iRfile].Get(hist[:hist.find('__pdf')]).Clone()
					renormSysHist = tfile[iRfile].Get(hist).Clone()
					renormSysHist.Scale(renormNomHist.Integral()/renormSysHist.Integral())
					renormSysHist.Write()
				else: tfile[iRfile].Get(hist).Write()
			else: tfile[iRfile].Get(hist).Write()
		outputRfile[str(iRfile)+key].Close()
	tfile[iRfile].Close()
	outputRfile.clear()
	tfile.clear()
 	
print "Total root files modified:", iRfile 




