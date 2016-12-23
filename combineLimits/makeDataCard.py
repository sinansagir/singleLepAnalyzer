#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
from ROOT import TFile
import os,sys


def add_processes_and_observations(cb, prefix="HTB"):
    print '>> Creating processes and observations...'
    for chn in chns:
    	cats_chn = cats[chn]
    	cb.AddObservations(  ['*'],  [prefix], [era], [chn],                 cats_chn      )
    	cb.AddProcesses(     ['*'],  [prefix], [era], [chn], bkg_procs[chn], cats_chn, False  )
    	cb.AddProcesses(     masses, [prefix], [era], [chn], sig_procs,      cats_chn, True   )

def add_shapes(cb):
    print '>> Extracting histograms from input root files...'
    for chn in chns:
        file = os.getcwd() + "/master.root"
        bkg_pattern = "BDT_36p4fb_%s_nT0p_nW0p_$BIN__$PROCESS" % chn
        cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(
            file, bkg_pattern, bkg_pattern + "__$SYSTEMATIC")
        sig_pattern = "BDT_36p4fb_%s_nT0p_nW0p_$BIN__$PROCESS$MASS" % chn
        cb.cp().channel([chn]).era([era]).signals().ExtractShapes(
			file, sig_pattern, sig_pattern + "__$SYSTEMATIC")


def add_bbb(cb):
    print '>> Merging bin errors and generating bbb uncertainties...'
    bbb = ch.BinByBinFactory()
    bbb.SetAddThreshold(0.1).SetMergeThreshold(0.5).SetFixNorm(False)

    for chn in chns:
    	cb_chn = cb.cp().channel([chn])
    	bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(bkg_procs[chn]), cb)
    	bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3]).process(sig_procs), cb)			

def rename_and_write(cb):
    print '>> Setting standardised bin names...'
    ch.SetStandardBinNames(cb)

    writer = ch.CardWriter('LIMITS'+limConf+'/$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                           'LIMITS'+limConf+'/$TAG/common/$ANALYSIS_$CHANNEL.input.root')

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
    bkgs = ['ewk', 'top', 'qcd', 'ttbar', 'wjets']

    cb.cp().process(signal + bkgs).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "lumi", "lnN", ch.SystMap()(1.062))
    cb.cp().process(signal + bkgs).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "elTrigSys", "lnN", ch.SystMap()(1.03))
    cb.cp().process(signal + bkgs).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "muTrigSys", "lnN", ch.SystMap()(1.011))
    cb.cp().process(signal + bkgs).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "elIdSys", "lnN", ch.SystMap()(1.01))
    cb.cp().process(signal + bkgs).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "muIdSys", "lnN", ch.SystMap()(1.011))
    cb.cp().process(signal + bkgs).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "elIsoSys", "lnN", ch.SystMap()(1.01))
    cb.cp().process(signal + bkgs).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "muIsoSys", "lnN", ch.SystMap()(1.03))
    #cb.cp().process(signal + bkgs).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "TrigEff", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkgs).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "pileup", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkgs).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "jec", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkgs).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "jer", "shape", ch.SystMap()(1.0))
    #cb.cp().process(signal + bkgs).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "btag", "shape", ch.SystMap()(1.0))
    #cb.cp().process(signal + bkgs).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "mistag", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ttbar']).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "toppt", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ttbar']).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "q2", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkgs).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "muRFcorrdNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkgs).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "pdfNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ttbar']).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "DDnorm_ttbar", "lnN", ch.SystMap()(1.0546))
    cb.cp().process(['wjets']).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "DDnorm_wjets", "lnN", ch.SystMap()(1.1324))
    cb.cp().process(['ttbar']).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "ttbar_SF_el", "lnU", ch.SystMap()(lnU))
    cb.cp().process(['ttbar']).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "ttbar_SF_mu", "lnU", ch.SystMap()(lnU))
    cb.cp().process(['wjets']).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "wjets_SF_el", "lnU", ch.SystMap()(lnU))
    cb.cp().process(['wjets']).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "wjets_SF_mu", "lnU", ch.SystMap()(lnU))
    if bbbType==1:
		tfile = TFile(os.getcwd() + "/master.root")
		allhists = [k.GetName() for k in tfile.GetListOfKeys()]
		datahists = [k.GetName() for k in tfile.GetListOfKeys() if '__data_obs' in k.GetName()]
		mySignal = sig_procs[0][:-1]
		for chn in chns:
			for cat in cats[chn]:
				histName = [item for item in datahists if chn in item and cat[1] in item][0]
				hist = tfile.Get(histName).Clone()
				for ibin in range(1, hist.GetNbinsX()+1):
					for proc in bkgs:
						if histName.replace('data_obs',proc)+'__CMS_'+mySignal+'_'+chn+'_nT0p_nW0p_'+cat[1]+'_'+era+'_'+proc+'_bin_%iUp' % ibin in allhists:
							cb.cp().process([proc]).channel([chn]).bin_id([cat[0]]).AddSyst(cb, 'CMS_'+mySignal+'_'+chn+'_nT0p_nW0p_'+cat[1]+'_'+era+'_'+proc+'_bin_%i' % ibin, "shape", ch.SystMap()(1.0))
					for mss in masses:
						proc=mySignal+'M'+mss
						if histName.replace('data_obs',proc)+'__CMS_'+mySignal+'_'+chn+'_nT0p_nW0p_'+cat[1]+'_'+era+'_'+mySignal+'_bin_%iUp' % ibin in allhists:
							cb.cp().process(signal).mass([mss]).channel([chn]).bin_id([cat[0]]).AddSyst(cb, 'CMS_'+mySignal+'_'+chn+'_nT0p_nW0p_'+cat[1]+'_'+era+'_'+mySignal+'_bin_%i' % ibin, "shape", ch.SystMap()(1.0))

def go(cb):
    add_processes_and_observations(cb)
    add_systematics(cb)
    add_shapes(cb)
    if bbbType==0: add_bbb(cb)
    rename_and_write(cb)
    # print_cb(cb)


if __name__ == "__main__":
    cb = ch.CombineHarvester()
    # cb.SetVerbosity(20)

    era = '13TeV'
    bbbType = 0 #-1==no BBB, 0==harvester BBB, 1==modifyBinning.py BBB
    lnU = 10.0
    if len(sys.argv)>1: lnU=float(sys.argv[1])
    limConf = '_lnU'+str(lnU).replace('.','p')
    if bbbType==-1: limConf+='_noBBB'
    if bbbType== 1: limConf+='_customBBB'
    #limConf+='_onlyLumi'

    bkg_procs = {'isSR_isE' : ['ewk', 'top', 'qcd','ttbar','wjets'],
                 'isSR_isM' : ['ewk', 'top', 'qcd','ttbar','wjets'],
                 'isCR_isE' : ['ewk', 'top', 'qcd','ttbar','wjets'],
                 'isCR_isM' : ['ewk', 'top', 'qcd','ttbar','wjets'],
                 }
    chns = sorted(bkg_procs.keys())

    sig_procs = ['HTBM']

    cats = {'isSR_isE' :[(0, 'nB2_nJ5'),
						 (1, 'nB2_nJ6p'),
						 (2, 'nB3p_nJ4'),
						 (3, 'nB3_nJ5'),
						 (4, 'nB3_nJ6p'),
						 (5, 'nB4p_nJ5'),
						 (6, 'nB4p_nJ6p'),
						 ],
			'isSR_isM' :[(0, 'nB2_nJ5'),
						 (1, 'nB2_nJ6p'),
						 (2, 'nB3p_nJ4'),
						 (3, 'nB3_nJ5'),
						 (4, 'nB3_nJ6p'),
						 (5, 'nB4p_nJ5'),
						 (6, 'nB4p_nJ6p'),
						 ],
            'isCR_isE' :[(0, 'nB1_nJ3'),
						 (1, 'nB1_nJ4'),
						 (2, 'nB1_nJ5'),
						 (3, 'nB1_nJ6p'),
						 (4, 'nB2p_nJ3'),
						 (5, 'nB2_nJ4'),
						 ],
			'isCR_isM' :[(0, 'nB1_nJ3'),
						 (1, 'nB1_nJ4'),
						 (2, 'nB1_nJ5'),
						 (3, 'nB1_nJ6p'),
						 (4, 'nB2p_nJ3'),
						 (5, 'nB2_nJ4'),
						],
            }

    masses = ch.ValsFromRange('180,200:500|50,750,800,1000,2000,3000')
    go(cb)

