#!/usr/bin/env python

import os,sys,time,math,datetime,itertools
from ROOT import gROOT,TFile,TH1F
import CombineHarvester.CombineTools.ch as ch
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from utils import *

gROOT.SetBatch(1)

fileDir = "/user_data/ssagir/CMSSW_10_2_10/src/singleLepAnalyzer/fourtops/makeTemplates/"
template = "noHOTtW_OR_onlyHOTtW_2019_10_24"
saveKey = ""

def add_processes_and_observations(cb, prefix="TTTT"):
    print '>> Creating processes and observations...'
    for chn in chns:
        cats_chn = cats[chn]
        if 'isCR' not in chn: 
			cb.AddObservations(  ['*'],  [prefix], [era], [chn],                 cats_chn      )
			cb.AddProcesses(     ['*'],  [prefix], [era], [chn], bkg_procs[chn], cats_chn, False  )
			cb.AddProcesses(     masses, [prefix], [era], [chn], sig_procs,      cats_chn, True   )
        else: 
			cb.AddObservations(  ['all'],  [prefix], [era], [chn],                 cats_chn      )
			cb.AddProcesses(     ['all'],  [prefix], [era], [chn], bkg_procs[chn], cats_chn, False  )


def add_shapes(cb):
    print '>> Extracting histograms from input root files...'
    for chn in chns:
        #file = os.environ['CMSSW_BASE'] + "/src/x53x53/master.root"
        file = fileDir+"templates_"+template+"/templates_HT_41p53fb_rebinned_stat0p3.root"
        bkg_pattern = "HT_41p53fb_%s$BIN__$PROCESS" % chn
        cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(
            file, bkg_pattern, bkg_pattern + "__$SYSTEMATIC")

        sig_pattern = "HT_41p53fb_%s$BIN__$PROCESS$MASS" % chn
        if 'isCR' not in chn:
			cb.cp().channel([chn]).era([era]).signals().ExtractShapes(
				file, sig_pattern, sig_pattern + "__$SYSTEMATIC")


def add_bbb(cb):
    print '>> Merging bin errors and generating bbb uncertainties...'
    bbb = ch.BinByBinFactory()
    bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(False)

    for chn in chns:
        cb_chn = cb.cp().channel([chn])
        if 'isCR' in chn:
        	bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(bkg_procs[chn]), cb)
        	bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(sig_procs), cb)
        else:
        	bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0]).process(bkg_procs[chn]), cb)
        	bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0]).process(sig_procs), cb)			

def rename_and_write(cb):
    print '>> Setting standardised bin names...'
    ch.SetStandardBinNames(cb)

    writer = ch.CardWriter('limits_'+template+saveKey+'/$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                           'limits_'+template+saveKey+'/$TAG/common/$ANALYSIS_$CHANNEL.input.root')

    writer.SetVerbosity(1)
    writer.WriteCards('cmb', cb)
    for chn in chns:
        print chn
        writer.WriteCards(chn, cb.cp().channel([chn]))
    print '>> Done!'


def print_cb(cb):
    for s in ["Obs", "Procs", "Systs", "Params"]:
        print "* %s *" % s
        getattr(cb, "Print%s" % s)()
        print


def add_systematics(cb):
    print '>> Adding systematic uncertainties...'

    signal = cb.cp().signals().process_set()
    bkg = ['ttbb', 'ttcc', 'ttjj', 'top', 'ewk', 'qcd']
    bkgNoQCD = ['ttbb', 'ttcc', 'ttjj', 'top', 'ewk']

#     cb.cp().process(signal + bkg).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "lumi", "lnN", ch.SystMap()(1.027))
#     cb.cp().process(signal + bkg).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "elTrigSys", "lnN", ch.SystMap()(1.05))
#     cb.cp().process(signal + bkg).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "muTrigSys", "lnN", ch.SystMap()(1.05))
#     cb.cp().process(signal + bkg).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "elIdSys", "lnN", ch.SystMap()(1.01))
#     cb.cp().process(signal + bkg).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "muIdSys", "lnN", ch.SystMap()(1.01))
#     cb.cp().process(signal + bkg).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "elIsoSys", "lnN", ch.SystMap()(1.01))
#     cb.cp().process(signal + bkg).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "muIsoSys", "lnN", ch.SystMap()(1.01))
    cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "lumi", "lnN", ch.SystMap()(1.023))
    cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "jec", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "jer", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "prefire", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "pileup", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ttbb']).channel(chns).AddSyst(cb, "ttbbmuRFcorrdNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ttcc']).channel(chns).AddSyst(cb, "ttccmuRFcorrdNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ttjj']).channel(chns).AddSyst(cb, "ttjjmuRFcorrdNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['top']).channel(chns).AddSyst(cb, "topmuRFcorrdNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ewk']).channel(chns).AddSyst(cb, "ewkmuRFcorrdNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['qcd']).channel(chns).AddSyst(cb, "qcdmuRFcorrdNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal).channel(chns).AddSyst(cb, "TTTTM690muRFcorrdNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ttbb']).channel(chns).AddSyst(cb, "ttbbPSwgtNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ttcc']).channel(chns).AddSyst(cb, "ttccPSwgtNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ttjj']).channel(chns).AddSyst(cb, "ttjjPSwgtNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['top']).channel(chns).AddSyst(cb, "topPSwgtNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ewk']).channel(chns).AddSyst(cb, "ewkPSwgtNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['qcd']).channel(chns).AddSyst(cb, "qcdPSwgtNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal).channel(chns).AddSyst(cb, "TTTTM690PSwgtNew", "shape", ch.SystMap()(1.0))
#     cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "pdfNew", "shape", ch.SystMap()(1.0))
#     cb.cp().process(['ttbb', 'ttcc', 'ttjj']).channel(chns).AddSyst(cb, "toppt", "shape", ch.SystMap()(1.0))
#     cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "tau32", "shape", ch.SystMap()(1.0))
#     cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "jmst", "shape", ch.SystMap()(1.0))
#     cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "jmrt", "shape", ch.SystMap()(1.0))
#     cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "tau21", "shape", ch.SystMap()(1.0))
#     cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "jmsW", "shape", ch.SystMap()(1.0))
#     cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "jmrW", "shape", ch.SystMap()(1.0))
#     cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "tau21pt", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "btag", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkg).channel(chns).AddSyst(cb, "mistag", "shape", ch.SystMap()(1.0))

def add_autoMCstat(cb):
    print '>> Adding autoMCstats...'

    thisDir = os.getcwd()
    for chn in chns+['cmb']:
    	chnDir = os.getcwd()+'/limits_'+template+saveKey+'/'+chn+'/690/'
    	files = [x for x in os.listdir(chnDir) if '.txt' in x]
    	os.chdir(chnDir)
    	for thefile in files:
    		with open(chnDir+thefile, "a") as chnfile: chnfile.write("* autoMCStats 1.")
    		print "*"*20
    		print "Making workspace from", chnDir+thefile
    		cmd = "text2workspace.py "+chnDir+thefile+" -v 1 -m 690 --no-b-only"
    		os.system(cmd)
    	os.chdir(thisDir)
    
def go(cb):
    add_processes_and_observations(cb)
    add_systematics(cb)
    add_shapes(cb)
    #add_bbb(cb)
    rename_and_write(cb)
    add_autoMCstat(cb)
    # print_cb(cb)


if __name__ == "__main__":
    cb = ch.CombineHarvester()
    # cb.SetVerbosity(20)

    era = '13TeV'
    
    tfile = TFile(fileDir+"templates_"+template+"/templates_HT_41p53fb_rebinned_stat0p3.root")
    allHistNames = [k.GetName() for k in tfile.GetListOfKeys() if not (k.GetName().endswith('Up') or k.GetName().endswith('Down'))]
    tfile.Close()
    dataName = 'data_obs'
    chns = [hist[hist.find('fb_')+3:hist.find('__')] for hist in allHistNames if '__'+dataName in hist]
    bkg_procs = {chn:[hist.split('__')[-1] for hist in allHistNames if chn in hist and not (hist.endswith('Up') or hist.endswith('Down') or hist.endswith(dataName) or hist.endswith('TTTTM690'))] for chn in chns}
    print bkg_procs

    sig_procs = ['TTTTM']
    
    cats = {}
    for chn in chns: cats[chn] = [(0, '')]

    masses = ch.ValsFromRange('690')
    go(cb)

