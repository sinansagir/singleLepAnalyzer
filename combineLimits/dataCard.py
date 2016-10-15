#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import os


def add_processes_and_observations(cb, prefix="x53x53right"):
    print '>> Creating processes and observations...'
    if chiral=='LH': prefix="x53x53left"
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
        file = os.environ['CMSSW_BASE'] + "/src/x53x53/master.root"
        bkg_pattern = "minMlb_2p318fb_%s_$BIN__$PROCESS" % chn
        cb.cp().channel([chn]).era([era]).backgrounds().ExtractShapes(
            file, bkg_pattern, bkg_pattern + "__$SYSTEMATIC")

        sig_pattern = "minMlb_2p318fb_%s_$BIN__$PROCESS$MASS" % chn
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
        	bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3,4,5,6,7]).process(bkg_procs[chn]), cb)
        	bbb.MergeAndAdd(cb_chn.cp().era([era]).bin_id([0,1,2,3,4,5,6,7]).process(sig_procs), cb)			

def rename_and_write(cb):
    print '>> Setting standardised bin names...'
    ch.SetStandardBinNames(cb)

    writer = ch.CardWriter('LIMITS_'+chiral+'/$TAG/$MASS/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                           'LIMITS_'+chiral+'/$TAG/common/$ANALYSIS_$CHANNEL.input.root')

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
    bkg = ['ewk', 'top', 'qcd']
    bkgNoQCD = ['ewk', 'top']

    cb.cp().process(signal + bkg).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "lumi", "lnN", ch.SystMap()(1.027))
    cb.cp().process(signal + bkg).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "elTrigSys", "lnN", ch.SystMap()(1.05))
    cb.cp().process(signal + bkg).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "muTrigSys", "lnN", ch.SystMap()(1.05))
    cb.cp().process(signal + bkg).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "elIdSys", "lnN", ch.SystMap()(1.01))
    cb.cp().process(signal + bkg).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "muIdSys", "lnN", ch.SystMap()(1.01))
    cb.cp().process(signal + bkg).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "elIsoSys", "lnN", ch.SystMap()(1.01))
    cb.cp().process(signal + bkg).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "muIsoSys", "lnN", ch.SystMap()(1.01))
    cb.cp().process(signal + bkg).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "pileup", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkg).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "jec", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkg).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "jer", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkg).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "btag", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkg).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "mistag", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkgNoQCD).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "jmr", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkgNoQCD).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "jms", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkgNoQCD).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "tau21", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkgNoQCD).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "topsf", "shape", ch.SystMap()(1.0))
    cb.cp().process(['top']).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "toppt", "shape", ch.SystMap()(1.0))
    cb.cp().process(['top']).channel(['isSR_isE','isSR_isM']).AddSyst(cb, "q2", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkg).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "muRFcorrdNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(signal + bkg).channel(['isSR_isE','isSR_isM','isCR_isE','isCR_isM']).AddSyst(cb, "pdfNew", "shape", ch.SystMap()(1.0))
    cb.cp().process(['ewk']).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "ewk_SF_el", "lnU", ch.SystMap()(100.0))
    cb.cp().process(['ewk']).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "ewk_SF_mu", "lnU", ch.SystMap()(100.0))
    cb.cp().process(['top']).channel(['isSR_isE','isCR_isE']).AddSyst(cb, "top_SF_el", "lnU", ch.SystMap()(100.0))
    cb.cp().process(['top']).channel(['isSR_isM','isCR_isM']).AddSyst(cb, "top_SF_mu", "lnU", ch.SystMap()(100.0))


def go(cb):
    add_processes_and_observations(cb)
    add_systematics(cb)
    add_shapes(cb)
    add_bbb(cb)
    rename_and_write(cb)
    # print_cb(cb)


if __name__ == "__main__":
    cb = ch.CombineHarvester()
    # cb.SetVerbosity(20)

    era = '13TeV'
    chiral = 'RH'

    bkg_procs = {'isSR_isE' : ['ewk', 'top', 'qcd'],
                 'isSR_isM' : ['ewk', 'top', 'qcd'],
                 'isCR_isE' : ['ewk', 'top', 'qcd'],
                 'isCR_isM' : ['ewk', 'top', 'qcd'],
                 }
    chns = sorted(bkg_procs.keys())

    if chiral=='RH': sig_procs = ['X53X53rightM']
    if chiral=='LH': sig_procs = ['X53X53leftM']

    cats = {'isSR_isE' :[(0, 'nT0_nW0_nB1'),
						 (1, 'nT0_nW0_nB2p'),
						 (2, 'nT0_nW1p_nB1'),
						 (3, 'nT0_nW1p_nB2p'),
						 (4, 'nT1p_nW0_nB1'),
						 (5, 'nT1p_nW0_nB2p'),
						 (6, 'nT1p_nW1p_nB1'),
						 (7, 'nT1p_nW1p_nB2p'),
						 ],
			'isSR_isM' :[(0, 'nT0_nW0_nB1'),
						 (1, 'nT0_nW0_nB2p'),
						 (2, 'nT0_nW1p_nB1'),
						 (3, 'nT0_nW1p_nB2p'),
						 (4, 'nT1p_nW0_nB1'),
						 (5, 'nT1p_nW0_nB2p'),
						 (6, 'nT1p_nW1p_nB1'),
						 (7, 'nT1p_nW1p_nB2p'),
						 ],
            'isCR_isE' :[(0, 'nT0p_nW0p_nB1'),
						 (1, 'nT0p_nW0p_nB2p'),
						 (2, 'nT0p_nW0_nB0'),
						 (3, 'nT0p_nW1p_nB0'),
						 ],
			'isCR_isM' :[(0, 'nT0p_nW0p_nB1'),
						 (1, 'nT0p_nW0p_nB2p'),
						 (2, 'nT0p_nW0_nB0'),
						 (3, 'nT0p_nW1p_nB0'),
						],
            }

    masses = ch.ValsFromRange('700:1600|100')
    go(cb)

