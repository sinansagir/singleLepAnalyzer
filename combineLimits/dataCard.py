#!/usr/bin/env python

import os,sys,time,math,datetime,itertools
from ROOT import gROOT,TFile,TH1F

if 'CMSSW_10_2_10' in os.environ['CMSSW_BASE']:
        print "Go CMSENV inside CMSSW_10_2_13!"
        exit(1)

parent = os.path.dirname(os.getcwd())
thisdir= os.path.dirname(os.getcwd()+'/')
sys.path.append(parent)
from utils import *
import CombineHarvester.CombineTools.ch as ch

gROOT.SetBatch(1)

BRconfStr=str(sys.argv[1])

whichsignal = 'TT'
if 'tW' in BRconfStr: whichsignal = 'BB'
year = '2017'

fileDir = '/uscms_data/d3/jmanagan/CMSSW_10_2_10/src/tptp_2017/makeTemplates/'
template = 'templates'+sys.argv[2]+'_' ##Change template to template directory. e.g.: templatesSR_......

tag = 'Feb2021' ##Tag and saveKey are used for output directory names
saveKey = tag+'_'+str(sys.argv[3])
CRdiscrim = sys.argv[4]

print'Tag = ',tag,', BR string = ',BRconfStr, ', whichsignal = ',whichsignal

def add_processes_and_observations(cb, prefix=whichsignal):
        print '------------------------------------------------------------------------'
	print '>> Creating processes and observations...prefix:',prefix
	for chn in chns:
                print '>>>> \t Creating proc/obs for channel:',chn
		cats_chn = cats[chn]
		cb.AddObservations(  ['*'],  [prefix], [era], [chn],                 cats_chn      )
		cb.AddProcesses(     ['*'],  [prefix], [era], [chn], bkg_procs[chn], cats_chn, False  )
		cb.AddProcesses(     masses, [prefix], [era], [chn], sig_procs,      cats_chn, True   )


def add_shapes(cb, prefix=whichsignal):
        print '------------------------------------------------------------------------'
	print '>> Extracting histograms from input root files...prefix:',prefix
	for chn in chns:
                print '>>>> \t Extracting histos for channel:',chn
		CRbkg_pattern = CRdiscrim+'_'+lumiStr+'_%s$BIN__$PROCESS' % chn
		SRbkg_pattern = 'DnnTprime_'+lumiStr+'_%s$BIN__$PROCESS' % chn
		CRsig_pattern = CRdiscrim+'_'+lumiStr+'_%s$BIN__$PROCESS$MASS' % chn
		SRsig_pattern = 'DnnTprime_'+lumiStr+'_%s$BIN__$PROCESS$MASS' % chn
		if prefix=='BB': 
                        SRbkg_pattern = SRbkg_pattern.replace('Tprime','Bprime')
                        SRsig_pattern = SRsig_pattern.replace('TTM','BBM').replace('Tprime','Bprime')
                        print 'Changing names!',SRbkg_pattern,SRsig_pattern

		if 'isCR' in chn: 
			cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(rfile, CRbkg_pattern, CRbkg_pattern + '__$SYSTEMATIC')
			cb.cp().channel([chn]).era([era]).signals().ExtractShapes(rfile, CRsig_pattern, CRsig_pattern + '__$SYSTEMATIC')
		else:
			cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(rfile, SRbkg_pattern, SRbkg_pattern + '__$SYSTEMATIC')
			cb.cp().channel([chn]).era([era]).signals().ExtractShapes(rfile, SRsig_pattern, SRsig_pattern + '__$SYSTEMATIC')
		        

def add_bbb(cb):
        ## This function is not used! autoMCstats in the card instead
	print '>> Merging bin errors and generating bbb uncertainties...'
	bbb = ch.BinByBinFactory()
	bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(False)
	
	for chn in chns:
		cb_chn = cb.cp().channel([chn])
		if 'CR' in chn:
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(bkg_procs[chn]), cb)
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(sig_procs), cb)
		else:
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0]).process(bkg_procs[chn]), cb)
			bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0]).process(sig_procs), cb)


def rename_and_write(cb):
        print '------------------------------------------------------------------------'
	print '>> Setting standardised bin names...'
	ch.SetStandardBinNames(cb)
	
	writer = ch.CardWriter('limits_'+template+saveKey+'/'+BRconfStr+'/$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
						   'limits_'+template+saveKey+'/'+BRconfStr+'/$TAG/common/$ANALYSIS_$CHANNEL.input.root')
	writer.SetVerbosity(1)
	writer.WriteCards('cmb', cb)
	for chn in chns:
                print '>>>> \t WriteCards for channel:',chn
		writer.WriteCards(chn, cb.cp().channel([chn]))
	print '>> Done writing cards!'


def print_cb(cb):
	for s in ['Obs', 'Procs', 'Systs', 'Params']:
		print '* %s *' % s
		getattr(cb, 'Print%s' % s)()
		print


def add_systematics(cb):
        print '------------------------------------------------------------------------'
	print '>> Adding systematic uncertainties...'
	
	signal = cb.cp().signals().process_set()
	
        ## https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM#CurRec
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumi$ERA', 'lnN', ch.SystMap('era')(['2016'], 1.022)(['2017'], 1.020)(['2018'], 1.015)) 
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumiXY', 'lnN', ch.SystMap('era')(['2016'], 1.009)(['2017'], 1.008)(['2018'], 1.020)) 
        if era != '2018':
                cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumiBBD', 'lnN', ch.SystMap('era')(['2016'], 1.004)(['2017'], 1.004)) 
                cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumiDB', 'lnN', ch.SystMap('era')(['2016'], 1.005)(['2017'], 1.005)) 
                cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumiGS', 'lnN', ch.SystMap('era')(['2016'], 1.004)(['2017'], 1.001)) 
        if era != '2016':
                cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumiLS', 'lnN', ch.SystMap('era')(['2017'], 1.003)(['2018'], 1.002)) 
                cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'lumiBCC', 'lnN', ch.SystMap('era')(['2017'], 1.003)(['2018'], 1.002)) 

        ## Taking lepton SFs as uncorrelated, new calculations each year
	cb.cp().process(signal + allbkgs).channel(chnsE).AddSyst(cb, 'elIdSys$ERA', 'lnN', ch.SystMap()(1.027)) 
	cb.cp().process(signal + allbkgs).channel(chnsM).AddSyst(cb, 'muIdSys$ERA', 'lnN', ch.SystMap()(1.027))
	cb.cp().process(signal + allbkgs).channel(chnsE).AddSyst(cb, 'elTrig$ERA', 'shape', ch.SystMap()(1.0))
	cb.cp().process(signal + allbkgs).channel(chnsM).AddSyst(cb, 'muTrig$ERA', 'shape', ch.SystMap()(1.0))

        ## To be used when "FullMu" was turned off in modifyBinning 
        #cb.cp().process([allbkgs[2]]).channel(chns).AddSyst(cb, 'QCDscale', 'lnN', ch.SystMap()(1.25))
        #cb.cp().process([allbkgs[0]]).channel(chns).AddSyst(cb, 'TTbarscale', 'lnN', ch.SystMap()(1.30))
        #cb.cp().process([allbkgs[1]]).channel(chns).AddSyst(cb, 'EWKscale', 'lnN', ch.SystMap()(1.25))

        ## Taking uncorrelated -- example of B2G-19-001. Jec uncorrelated is more conservative than the various 0/50/100 scenarios that require source splitting
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jer$ERA', 'shape', ch.SystMap()(1.0))
	cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'jec$ERA', 'shape', ch.SystMap()(1.0))

        ## Correlated in 2016 and 2017, doesn't exist in 2018
        if era != '2018':
                cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'prefire', 'shape', ch.SystMap()(1.0))

        ## Taking these as correlated since the training was unchanged
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Teff', 'shape', ch.SystMap()(1.0)) 
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Heff', 'shape', ch.SystMap()(1.0))
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Zeff', 'shape', ch.SystMap()(1.0))
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Weff', 'shape', ch.SystMap()(1.0))
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Beff', 'shape', ch.SystMap()(1.0))
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Tmis$ERA', 'shape', ch.SystMap()(1.0)) #
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Hmis$ERA', 'shape', ch.SystMap()(1.0)) #
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Zmis$ERA', 'shape', ch.SystMap()(1.0)) #
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Wmis$ERA', 'shape', ch.SystMap()(1.0)) #
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Bmis$ERA', 'shape', ch.SystMap()(1.0)) #

        ## PDF was separate in 16 from 17/18
        if era == '2016':
                cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'pdfNew$ERA', 'shape', ch.SystMap()(1.0))
        else:
                cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'pdfNew20172018', 'shape', ch.SystMap()(1.0))

        ## Correlated: https://hypernews.cern.ch/HyperNews/CMS/get/b2g/1381.html
        cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'pileup', 'shape', ch.SystMap()(1.0)) 

        ## HT weighting only on EWK background, same in all years
        cb.cp().process([allbkgs[1]]).channel(chns).AddSyst(cb, 'jsf', 'shape', ch.SystMap()(1.0))

        ## HTCorr on top background only, same in all years
        cb.cp().process([allbkgs[0]]).channel(chns).AddSyst(cb, 'toppt', 'shape', ch.SystMap()(1.0))

        ## DeepAK8 J-score shape correction, independent in 2017 and 2018
        if era != '2016':
                cb.cp().process(signal + allbkgs).channel(chns).AddSyst(cb, 'Jshape$ERA', 'shape', ch.SystMap()(1.0)) 

	## Taking as correlated across years, but not processes -- no changes to this setting in MC
	cb.cp().process([allbkgs[0]]).channel(chns).AddSyst(cb, 'muRFcorrdNewTop', 'shape', ch.SystMap()(1.0))
	cb.cp().process([allbkgs[1]]).channel(chns).AddSyst(cb, 'muRFcorrdNewEwk', 'shape', ch.SystMap()(1.0))
	cb.cp().process([allbkgs[2]]).channel(chns).AddSyst(cb, 'muRFcorrdNewQCD', 'shape', ch.SystMap()(1.0))
	cb.cp().process(signal).channel(chns).AddSyst(cb, 'muRFcorrdNewSig', 'shape', ch.SystMap()(1.0))



def add_autoMCstat(cb):
        print '------------------------------------------------------------------------'
	print '>> Adding autoMCstats...'
	
	thisDir = os.getcwd()
	mass=0
	massList = range(900,1800+1,100)

	for chn in chns+['cmb']:
                print '>>>> \t Adding autoMCstats for channel:',chn
		for mass in massList:
			chnDir = os.getcwd()+'/limits_'+template+saveKey+'/'+BRconfStr+'/'+chn+'/'+str(mass)+'/'
			print 'chnDir: ',chnDir
			os.chdir(chnDir)
			files = [x for x in os.listdir(chnDir) if '.txt' in x]
			for ifile in files:
				with open(chnDir+ifile, 'a') as chnfile: chnfile.write('* autoMCStats 1.')
			os.chdir(thisDir)

def create_workspace(cb):
        print '------------------------------------------------------------------------'
	print '>> Creating workspace...'

	#for chn in ['cmb']+chns:  ## do I really need individual workspaces? Not sure...
	for chn in ['cmb']:
                print '>>>> \t Creating workspace for channel:',chn
		chnDir = os.getcwd()+'/limits_'+template+saveKey+'/'+BRconfStr+'/'+chn+'/*'
		cmd = 'combineTool.py -M T2W -i '+chnDir+' -o workspace.root --parallel 4 --channel-masks'
		os.system(cmd)


def go(cb):
	add_processes_and_observations(cb)
	add_systematics(cb)
	add_shapes(cb)
	rename_and_write(cb)
	add_autoMCstat(cb)
	create_workspace(cb)


if __name__ == '__main__':
	cb = ch.CombineHarvester()
	
	era = year
	lumiStrDir = '35p867'
	if year=='2018': lumiStrDir = '59p69'
	if year=='2017': lumiStrDir = '41p53'
        lumiStr = lumiStrDir+'fb'

        if not os.path.exists('./limits_'+template+saveKey+'/'+BRconfStr): os.system('mkdir -p ./limits_'+template+saveKey+'/'+BRconfStr+'/')

        discrim = 'DnnTprime'
        if whichsignal == 'BB': discrim = 'DnnBprime'
	if 'SRCR' in template:
		rfile = fileDir+template+tag+whichsignal+'/templates_'+discrim+'_'+BRconfStr+'_'+lumiStrDir+'_Combine_rebinned_stat0p3_smoothedLOWESS.root'
		os.system('cp '+rfile+' ./limits_'+template+saveKey+'/'+BRconfStr+'/')
        elif 'CR' in template:
		rfile = fileDir+template+tag+whichsignal+'/templates_'+CRdiscrim+'_'+BRconfStr+'_'+lumiStrDir+'_Combine_chi2_rebinned_stat0p3.root'
		os.system('cp '+rfile+' ./limits_'+template+saveKey+'/'+BRconfStr+'/')

	print'File: ',rfile
	allbkgs = ['top','ewk','qcd']

	dataName = 'data_obs'
	tfile = TFile(rfile)
	allHistNames = [k.GetName() for k in tfile.GetListOfKeys() if not (k.GetName().endswith('Up') or k.GetName().endswith('Down'))]
	tfile.Close()
	chns = [hist[hist.find('fb_')+3:hist.find('__')] for hist in allHistNames if '__'+dataName in hist]

	chnsE = [chn for chn in chns if '_isE_' in chn]
	chnsM = [chn for chn in chns if '_isM_' in chn]
	bkg_procs = {chn:[hist.split('__')[-1] for hist in allHistNames if '_'+chn+'_' in hist and not (hist.endswith('Up') or hist.endswith('Down') or hist.endswith(dataName) or 'TTM' in hist or 'BBM' in hist)] for chn in chns}
	for cat in sorted(bkg_procs.keys()):
		print cat,bkg_procs[cat]
	if 'qcd' in bkg_procs[cat]:
		print '		Removing qcd ...'
		bkg_procs[cat]=bkg_procs[cat][:-1]
	
	if whichsignal=='TT': sig_procs = ['TTM']
	elif whichsignal=='BB': sig_procs = ['BBM'] 	

	cats = {}
	for chn in chns: cats[chn] = [(0, '')]
	
	masses = ch.ValsFromRange('900:1800|100')	
	print 'Found this mass list: ',masses

	go(cb)

