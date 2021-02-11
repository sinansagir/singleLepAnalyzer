#!/usr/bin/env python

import os,sys,time,math,datetime,itertools
from ROOT import gROOT,TFile,TH1F
#import CombineHarvester.CombineTools.ch as ch
parent = os.path.dirname(os.getcwd())
thisdir= os.path.dirname(os.getcwd()+'/')
sys.path.append(parent)
from utils import *
gROOT.SetBatch(1)

whichsignal = 'TT'

year = '2016'
era = '13TeV_R'+year
lumiStr = '41p53fb'
if year=='2018': lumiStr = '59p97fb'
if year=='2017': lumiStr = '41p53fb'
if year=='2016': lumiStr = '35p867fb'

tag = '_ttHFupLFdown' ##Tag and saveKey are used for output directory names
saveKey = '_ttHF'+tag
BRconfStr=''
BRs={}
if whichsignal=='TT':
        BRs['BW']=[0.0,0.50,1.0,0.0,0.0]#,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
        BRs['TH']=[0.5,0.25,0.0,1.0,0.0]#,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]
        BRs['TZ']=[0.5,0.25,0.0,0.0,1.0]#,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
        nBRconf=len(BRs['BW'])
elif whichsignal=='BB':
        BRs['TW']=[0.0,0.50,1.0,0.0,0.0]#,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
        BRs['BH']=[0.5,0.25,0.0,1.0,0.0]#,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]  # May or may not want to keep these lines, have to ask
        BRs['BZ']=[0.5,0.25,0.0,0.0,1.0]#,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
        nBRconf=len(BRs['TW'])

for BRind in range(nBRconf):
	if whichsignal=='TT': BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
     	if whichsignal=='BB': BRconfStr='_tW'+str(BRs['TW'][BRind]).replace('.','p')+'_bZ'+str(BRs['BZ'][BRind]).replace('.','p')+'_bH'+str(BRs['BH'][BRind]).replace('.','p')

	fileDir = '/uscms_data/d3/cholz/CMSSW_10_2_10/src/tptp_2016/makeTemplates/'
	template = 'templatesSR_June2020TT' ##Change template to template directory. e.g.: templatesSR_......
	#if not os.path.exists('./limits_'+template+saveKey): os.system('mkdir ./limits_'+template+saveKey)

mass = 0
massList = range(1000,1800+1,100)

for mass in massList:
	for BRind in range(nBRconf):
        	if whichsignal=='TT': BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
        	if whichsignal=='BB': BRconfStr='_tW'+str(BRs['TW'][BRind]).replace('.','p')+'_bZ'+str(BRs['BZ'][BRind]).replace('.','p')+'_bH'+str(BRs['BH'][BRind]).replace('.','p')
		if whichsignal=='TT' and 'SR' in template:
			rfile = './'+template+'/templates_DnnTprime'+str(mass)+'_'+BRconfStr+'_'+lumiStr+'_rebinned_stat0p3.root'
		if whichsignal=='TT' and 'CR' in template:
			rfile = './'+template+'/templates_HTNtag'+str(mass)+'_'+BRconfStr+'_'+lumiStr+'_rebinned_stat0p3.root'
		if whichsignal=='BB' and 'SR' in template:
			rfile = './'+template+'/templates_DnnBprime'+str(mass)+'_'+BRconfStr+'_'+lumiStr+'_rebinned_stat0p3.root'
		if whichsignal=='BB' and 'CR' in template:
	        	rfile = './'+template+'/templates_HTNtag'+str(mass)+'_'+BRconfStr+'_'+lumiStr+'_rebinned_stat0p3.root'
		print'File name:', rfile
