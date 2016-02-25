#!/usr/bin/python

import os,sys,time,math,fnmatch
from array import array
from ROOT import *

outDir = os.getcwd()+'/templates_minMlb_HT_mixed/'
if not os.path.exists(outDir): os.system('mkdir '+outDir)
cutString = 'lep40_MET75_1jet300_2jet150_NJets3_NBJets0_3jet100_4jet0_5jet0_DR1_1Wjet0_1bjet0_HT0_ST0_minMlb0'

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

templateDir = {}
templateDir[keyb0] = os.getcwd()+'/templates_HT_2016_1_13_9_49_29/'+cutString
templateDir[keyb1] = os.getcwd()+'/templates_minMlb_2016_1_13_1_2_40/'+cutString
templateDir[keyb2] = os.getcwd()+'/templates_minMlb_2016_1_13_1_2_40/'+cutString
templateDir[keyb3p]= os.getcwd()+'/templates_minMlb_2016_1_13_1_2_40/'+cutString

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

rfiles = {}
for key in templateDir.keys():
	rfiles[key] = [file for file in findfiles(templateDir[key], '*.root') if '_2p215fb.root' in file]# and '_minMlb300' in file]

tfile = {}
outputRfile = {}
iRfile=0
for file in rfiles[rfiles.keys()[0]]:
	iRfile+=1
	for key in rfiles.keys(): 
		#print file.split('/')[-1].split('_')[-2]
		#print [item for item in rfiles[key] if file.split('/')[-1].split('_')[-2] in item][0]
		tfile[key+str(iRfile)] = TFile([item for item in rfiles[key] if file.split('/')[-1].split('_')[-2] in item][0])
	
	hists = {}
	for key in rfiles.keys(): hists[key]  = [k.GetName() for k in tfile[key+str(iRfile)].GetListOfKeys() if key in k.GetName()]
	
	outputRfile[str(iRfile)] = TFile(outDir+file.split('/')[-1].replace(file.split('/')[-1].split('_')[1]+'_',''),'RECREATE')
	for key in hists.keys():
		for hist in hists[key]:
			#print hist
			if '__mu' in hist: #normalize the renorm/fact shapes to nominal
				renormNomHist = tfile[key+str(iRfile)].Get(hist[:hist.find('__mu')]).Clone()
				renormSysHist = tfile[key+str(iRfile)].Get(hist).Clone()
				renormSysHist.Scale(renormNomHist.Integral()/renormSysHist.Integral())
				renormSysHist.Write()
			elif '__pdf' in hist: #normalize the pdf shapes to nominal
				renormNomHist = tfile[key+str(iRfile)].Get(hist[:hist.find('__pdf')]).Clone()
				renormSysHist = tfile[key+str(iRfile)].Get(hist).Clone()
				renormSysHist.Scale(renormNomHist.Integral()/renormSysHist.Integral())
				renormSysHist.Write()
			else: tfile[key+str(iRfile)].Get(hist).Write()
	outputRfile[str(iRfile)].Close()
	for key in rfiles.keys(): 
		print key, tfile[key+str(iRfile)].GetName(), outputRfile[str(iRfile)].GetName()
		tfile[key+str(iRfile)].Close()
	outputRfile.clear()
	tfile.clear()
 	
print "Total root files modified:", iRfile 




