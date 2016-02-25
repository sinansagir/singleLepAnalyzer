#!/usr/bin/python

import os,sys,time,math,fnmatch
from ROOT import *

cutString = 'lep80_MET100_leadJet200_subLeadJet90_leadbJet0_ST0_HT0_NJets4_NBJets1_3rdJet0_4thJet0_5thJet0_WJet0'
templateDir = '/home/ssagir/CMSSW_7_3_0/src/approval/optimization_x53x53/templates_minMlb_2015_12_10_23_33_35/'

refLumi = 2 # "." will be replaced with "p" in the filename
normdLumi = 2.11 # "." will be replaced with "p" in the filename

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)
            
rfiles = [file for file in findfiles(templateDir+cutString, '*WJet0rebinned_uncorrdRFandRFnormalized.root')]

tfile = {}
outputRfile = {}
hists3fb = {}
iRfile=0
for file in rfiles: 
	if '_'+str(refLumi).replace('.','p')+'fb_' not in file: continue
	print file
	tfile[iRfile] = TFile(file)
	hists = [k.GetName() for k in tfile[iRfile].GetListOfKeys()]
	print file.replace(str(refLumi).replace('.','p')+'fb',str(normdLumi).replace('.','p')+'fb')
	outputRfile[iRfile] = TFile(file.replace('_'+str(refLumi).replace('.','p')+'fb_','_'+str(normdLumi).replace('.','p')+'fb_'),'RECREATE')
	ihists=0
	for hist in hists:
		print hist
		print hist.replace(str(refLumi).replace('.','p')+'fb',str(normdLumi).replace('.','p'))+'fb'
		hists3fb[hist]=tfile[iRfile].Get(hist).Clone(hist.replace(str(refLumi).replace('.','p')+'fb_',str(normdLumi).replace('.','p')+'fb_'))
		if '__DATA' not in hist: hists3fb[hist].Scale(float(normdLumi)/2.21)
		hists3fb[hist].Write()
		ihists+=1
	print "Total Histograms modified: ",ihists
	outputRfile[iRfile].Close()
 	iRfile+=1
 	#if i>0:break
print "Total root files modified:", iRfile 




