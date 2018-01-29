import os,sys,pickle
from operator import itemgetter,attrgetter

input1L = '/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/makeTemplates/templates4CRhtSR_NewEl/splitLess/templates_minMlbST_TTM1000_bW0p5_tZ0p25_tH0p25_36p814fb_BKGNORM_rebinned_stat0p3.root'
input2L = '/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/ssdluncerts/Oct21_2017_HT1200_nConst4_0NonSSLeps/Limits_TTM1000_bW0p5_tZ0p25_tH0p25_All_LL40_SL35_HT1200_nConst4.root'
input3L = '/user_data/rsyarif/optimization_reMiniAOD_PRv9_FRv49sys_elMVAfix_AllSys_2017_9_21/lep1Pt0_jetPt0_MET20_NJets3_NBJets1_HT0_ST0_mllOS20/Shape_accurateLHESys_FRsysSep21_newSigSF_AsymmFRsys/templates_STrebinnedv2_TTM1000_bW0p5_tZ0p25_tH0p25_35p867fb.root'

rFileName = input1L.split('/')[-1][:-5]

category = str(sys.argv[2])
print 'File:',rFileName,', category:',category
                                                                                                                                   
def get_model1L():
    if category == 'All' or category == 'comb': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0))
    if category == 'combNoB0' or category == 'comb123' or category == 'ssdl': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('nH1p_nW0p_nB0_isCR')==0))
    if category == 'noCR': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('_isCR_')==0))
    if category == 'noB0CR': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('_isCR_')==0 and s.count('nB0_isSR')==0))
    if category == 'noB0': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('_nB0_isSR_')==0))
    if category == 'noCRHB0': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('_nH1p_nW0p_nB0_isCR_')==0))
    if category == 'noB0CRHB0': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('_nH1p_nW0p_nB0_isCR_')==0 and s.count('_nB0_isSR_')==0))

    if category == 'Higgs': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nH0')==0))
    if category == 'Higgs1b': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nH0')==0 and s.count('nH2b')==0))
    if category == 'Higgs2b': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nH0')==0 and s.count('nH1b')==0))
    if category == 'Wtag1': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nW0_')==0))
    if category == 'Wtag0': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nW1p_')==0))
    if category == 'Btag0': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB1')==0 and s.count('nB2_')==0 and s.count('nB3p_')==0))
    if category == 'Btag1': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB0_')==0 and s.count('nB2_')==0 and s.count('nB3p_')==0))
    if category == 'Btag2': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB0_')==0 and s.count('nB1_')==0 and s.count('nB3p_')==0))
    if category == 'Btag3': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB0_')==0 and s.count('nB1_')==0 and s.count('nB2_')==0))

    if 'comb123' in category:         
        if 'NoPDF' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('nH1p_nW0p_nB0_isCR')==0 and s.count('pdfNew')==0))
        if 'NoEWK' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('nH1p_nW0p_nB0_isCR')==0 and s.count('muRFcorrdNewEwk1L')==0))
        if 'NoTT' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('nH1p_nW0p_nB0_isCR')==0 and s.count('muRFcorrdNewTTbar')==0))
        if 'H' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('nH1p_nW0p_nB0_isCR')==0 and s.count('nH0_')==0))
        if 'HW0' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('nH1p_nW0p_nB0_isCR')==0 and s.count('nW1p_')==0))
        if 'HW1' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('nH1p_nW0p_nB0_isCR')==0 and s.count('nW0_')==0))
        if 'W1W0' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('nH1p_nW0p_nB0_isCR')==0 and s.count('nH1b_')==0 and s.count('nH2b_')==0 and s.count('nH1p_')==0))
        if 'W0' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('nH1p_nW0p_nB0_isCR')==0 and s.count('nW1p_')==0 and s.count('nH1b_')==0 and s.count('nH2b_')==0 and s.count('nH1p_')==0))
        if 'W1' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('nH1p_nW0p_nB0_isCR')==0 and s.count('nW0_')==0 and s.count('nH1b_')==0 and s.count('nH2b_')==0 and s.count('nH1p_')==0))

        if 'H0W0B1' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('isCR')==0 and s.count('nW1p_')==0 and s.count('nH1b_')==0 and s.count('nH2b_')==0 and s.count('nB2_')==0 and s.count('nB3p_')==0))
        if 'H0W0B2' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('isCR')==0 and s.count('nW1p_')==0 and s.count('nH1b_')==0 and s.count('nH2b_')==0 and s.count('nB1_')==0 and s.count('nB3p_')==0))
        if 'H0W0B3' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('isCR')==0 and s.count('nW1p_')==0 and s.count('nH1b_')==0 and s.count('nH2b_')==0 and s.count('nB1_')==0 and s.count('nB2_')==0))
        if 'H0W1B1' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('isCR')==0 and s.count('nW0_')==0 and s.count('nH1b_')==0 and s.count('nH2b_')==0 and s.count('nB2_')==0 and s.count('nB3p_')==0))
        if 'H0W1B2' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('isCR')==0 and s.count('nW0_')==0 and s.count('nH1b_')==0 and s.count('nH2b_')==0 and s.count('nB1_')==0 and s.count('nB3p_')==0))
        if 'H0W1B3' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('isCR')==0 and s.count('nW0_')==0 and s.count('nH1b_')==0 and s.count('nH2b_')==0 and s.count('nB1_')==0 and s.count('nB2_')==0))
        if 'H1W0B1' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('isCR')==0 and s.count('nH0_')==0 and s.count('nH2b_')==0))
        if 'H2W0B1' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('isCR')==0 and s.count('nH0_')==0 and s.count('nH1b_')==0))
        if 'HCR' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('isSR')==0 and s.count('nH0_')==0))
        if 'WCR' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('isSR')==0 and s.count('nH1p_')==0 and s.count('nB1p_')==0))
        if 'TCR' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('isSR')==0 and s.count('nH1p_')==0 and s.count('nB0_')==0))
        if 'CR' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('isSR')==0))
        if 'W0NoCR' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('isCR')==0 and s.count('nW1p_')==0 and s.count('nH1b_')==0 and s.count('nH2b_')==0))
        if 'W1NoCR' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('isCR')==0 and s.count('nW0_')==0 and s.count('nH1b_')==0 and s.count('nH2b_')==0))
        if 'HNoCR' in category: model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('sig')==0 and s.count('nB0_isSR')==0 and s.count('isCR')==0 and s.count('nH0_')==0))


    model.fill_histogram_zerobins()
    model.set_signal_process_groups({'':[]})
    
    procs = model.processes
    obsvs = model.observables.keys()

    for obs in obsvs:
        if 'isE' in obs:
            try: model.add_lognormal_uncertainty('elIdSys', math.log(1.02), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), '*', obs) #iso + reco
            except: pass
            try: model.add_lognormal_uncertainty('elRecoSys', math.log(1.01), '*', obs) #iso + reco
            except: pass
        elif 'isM' in obs:
            try: model.add_lognormal_uncertainty('muIdSys', math.log(1.03), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('muIsoSys', math.log(1.01), '*', obs) #iso + tracking
            except: pass
            try: model.add_lognormal_uncertainty('muRecoSys', math.log(1.01), '*', obs) #iso + tracking
            except: pass

        if 'H2b' in obs or 'H1b' in obs:
            try: model.add_lognormal_uncertainty('htag_prop', math.log(1.05), '*', obs)
            except: pass
        else:
            try: model.add_lognormal_uncertainty('htag_prop', math.log(0.95), '*', obs)
            except: pass

    try: model.add_lognormal_uncertainty('lumiSys', math.log(1.025), '*', '*')
    except: pass

    # flat values for tests
    try: model.add_lognormal_uncertainty('QCDscale', math.log(1.25),'QCD','*')
    except RuntimeError: pass
    try: model.add_lognormal_uncertainty('SingleTopscale', math.log(1.16),'SingleTop','*')
    except RuntimeError: pass
    if category != 'comb123NoTT':
        try: model.add_lognormal_uncertainty('TTbarscale', math.log(1.30),'TTbar','*')
        except RuntimeError: pass
    if category != 'comb123NoEWK':
        try: model.add_lognormal_uncertainty('EWKscale', math.log(1.25),'EWK','*')
        except RuntimeError: pass
    # try: model.add_lognormal_uncertainty('jsf', math.log(1.038), 'WJets', '*')
    # except: pass
    # try: model.add_lognormal_uncertainty('muRFcorrdNewDYJets', math.log(1.15), 'DYJets', '*')
    # except: pass
    # try: model.add_lognormal_uncertainty('muRFcorrdNewEwk', math.log(1.15), 'ewk', '*')
    # except: pass
    # try: model.add_lognormal_uncertainty('muRFcorrdNewSingleTop', math.log(1.16), 'SingleTop', '*')
    # except: pass

    return model

def get_model2L():
    model = build_model_from_rootfile(input2L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0))

    model.set_signal_process_groups({'':[]})
    
    procs = model.processes
    print procs
    obsvs = model.observables.keys()
    
    for proc in procs:
        
        #data driven
        if(proc=="FakeRate"):             
            #model.add_lognormal_uncertainty("FakeRate",math.log(1.50),proc)
            for obs in obsvs:
                if 'elel' in obs: model.add_lognormal_uncertainty('elFakeRate',math.log(1.50),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('elFakeRate',math.log(1.35),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('muFakeRate',math.log(1.35),proc,obs)
                if 'mumu' in obs: model.add_lognormal_uncertainty('muFakeRate',math.log(1.50),proc,obs)
        elif(proc=="ChargeMisID"): model.add_lognormal_uncertainty("ChargeMisIDUnc",math.log(1.30),proc)

        #MC
        else:
            model.add_lognormal_uncertainty('lumiSys',math.log(1.025),proc)
            model.add_lognormal_uncertainty('eeTrigSysBD',math.log(1.03),proc,'elelBD')
            model.add_lognormal_uncertainty('emTrigSysBD',math.log(1.03),proc,'elmuBD')
            model.add_lognormal_uncertainty('mmTrigSysBD',math.log(1.03),proc,'mumuBD')
            model.add_lognormal_uncertainty('eeTrigSysEH',math.log(1.03),proc,'elelEH')
            model.add_lognormal_uncertainty('emTrigSysEH',math.log(1.03),proc,'elmuEH')
            model.add_lognormal_uncertainty('mmTrigSysEH',math.log(1.03),proc,'mumuEH')
            
            for obs in obsvs:
                if 'elel' in obs: model.add_lognormal_uncertainty('elIdSys',math.log(1.02),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('elIdSys',math.log(1.01),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('muIdSys',math.log(1.03),proc,obs)
                if 'mumu' in obs: model.add_lognormal_uncertainty('muIdSys',math.log(1.06),proc,obs)
                if 'elel' in obs: model.add_lognormal_uncertainty('elIsoSys',math.log(1.02),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('elIsoSys',math.log(1.01),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('muIsoSys',math.log(1.01),proc,obs)
                if 'mumu' in obs: model.add_lognormal_uncertainty('muIsoSys',math.log(1.02),proc,obs)
                if 'elel' in obs: model.add_lognormal_uncertainty('elRecoSys',math.log(1.02),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('elRecoSys',math.log(1.01),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('muRecoSys',math.log(1.01),proc,obs)
                if 'mumu' in obs: model.add_lognormal_uncertainty('muRecoSys',math.log(1.02),proc,obs)

            if(proc != 'sig'):
                if(proc=='TTZ'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(1.045),math.log(1.055),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(1.03),math.log(1.025),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewTop',math.log(1.109),math.log(1.068),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(1.035),math.log(1.02),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(1.01),math.log(1.01),proc)
                elif(proc=='TTW'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(1.01),math.log(1.01),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(1.134),math.log(1.134),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewTop',math.log(1.164),math.log(1.132),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(1.034),math.log(1.025),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(1.01),math.log(1.01),proc)
                elif(proc=='TTH'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(1.01),math.log(1.01),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(1.035),math.log(1.034),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewTop',math.log(1.198),math.log(1.266),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(1.044),math.log(1.032),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(1.01),math.log(1.01),proc)
                elif(proc=='TTTT'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(1.028),math.log(1.028),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(1.35),math.log(1.35),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewTop',math.log(1.243),math.log(1.265),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(1.021),math.log(1.023),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(1.01),math.log(1.01),proc)
                elif(proc=='WZ'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(1.081),math.log(1.1),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(1.068),math.log(1.106),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewEwk',math.log(1.113),math.log(1.148),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(1.09),math.log(1.09),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(1.01),math.log(1.01),proc)
                elif(proc=='ZZ'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(0.932),math.log(0.953),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(1.023),math.log(1.018),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewEwk',math.log(1.085),math.log(1.109),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(1.09),math.log(1.09),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(1.01),math.log(1.01),proc)
                elif(proc=='WpWp'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(1.012),math.log(1.012),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(1.35),math.log(1.35),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewEwk',math.log(1.35),math.log(1.35),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(1.041),math.log(1.09),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(1.01),math.log(1.01),proc)
                elif(proc=='WWZ'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(1.059),math.log(1.062),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(1.016),math.log(1.015),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewEwk',math.log(1.153),math.log(1.195),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(1.194),math.log(1.09),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(1.01),math.log(1.01),proc)
                elif(proc=='WZZ'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(1.003),math.log(1.017),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(1.019),math.log(1.017),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewEwk',math.log(1.164),math.log(1.211),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(1.09),math.log(1.043),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(1.01),math.log(1.01),proc)
                else: print 'UNKNOWN PROC'

            else:     #   signal
                model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(1.014),math.log(1.013),proc)
                model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewSig',math.log(1.002),math.log(1.003),proc)
                model.add_asymmetric_lognormal_uncertainty('jer',math.log(1.011),math.log(1.011),proc) 
                model.add_asymmetric_lognormal_uncertainty('jec',math.log(1.013),math.log(1.008),proc) 
                model.add_lognormal_uncertainty('pileup',math.log(1.01),proc) 
    

    return model

def get_model3L():
    model = build_model_from_rootfile(input3L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('muR__')==0 and s.count('muF__')==0 and s.count('muRFcorrd__')==0 and s.count('elelelTrigSys')==0 and s.count('elelmuTrigSys')==0 and s.count('elmumuTrigSys')==0 and s.count('mumumuTrigSys')==0 and s.count('elIsoSys')==0 and s.count('elIdSys')==0 and s.count('muIsoSys')==0 and s.count('muIdSys')==0 and s.count('PR__')==0 and s.count('sig')==0))

    #
    model.fill_histogram_zerobins()
    model.set_signal_process_groups({'':[]})
    
    procs = model.processes
    obsvs = model.observables.keys()

    for proc in procs:
        if(proc != 'ddbkg'):
            try: model.add_lognormal_uncertainty('elIdSys', math.log(1.06), proc, 'triLepEEE')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elIdSys', math.log(1.04), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elIdSys', math.log(1.02), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elIsoSys', math.log(1.03), proc, 'triLepEEE')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elIsoSys', math.log(1.02), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elRecoSys', math.log(1.03), proc, 'triLepEEE')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elRecoSys', math.log(1.02), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elRecoSys', math.log(1.01), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIdSys', math.log(1.02), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIdSys', math.log(1.04), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIdSys', math.log(1.06), proc, 'triLepMMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIsoSys', math.log(1.01), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIsoSys', math.log(1.02), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIsoSys', math.log(1.03), proc, 'triLepMMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muRecoSys', math.log(1.01), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muRecoSys', math.log(1.02), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muRecoSys', math.log(1.03), proc, 'triLepMMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('eeeTrigSys', math.log(1.03), proc, 'triLepEEE')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('eemTrigSys', math.log(1.03), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('emmTrigSys', math.log(1.03), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('mmmTrigSys', math.log(1.03), proc, 'triLepMMM')
            except RuntimeError: pass

            try: model.add_lognormal_uncertainty('lumiSys', math.log(1.025), proc, '*')
            except RuntimeError: pass

        else:
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.20),proc,'triLepMMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.18),proc,'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.38),proc,'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.45),proc,'triLepEEE')
            except RuntimeError: pass


    return model

##################################################################################################################

model1L = get_model1L()

if 'comb' in category:
    model3L = get_model3L()
    model1L.combine(model3L)

if 'comb123' in category:
    model2L = get_model2L()
    model1L.combine(model2L)

if category == 'ssdl':
    model1L = get_model2L()

model_summary(model1L)

options = Options()
options.set('minimizer', 'strategy', 'robust')
options.set('minimizer', 'minuit_tolerance_factor', '100')

parVals = mle(model1L, input='data', n=1, with_error=True, chi2=True, ks=True, with_covariance=True, options=options)

parameter_values = {}
for syst in parVals[''].keys():
    if syst=='__nll' or syst=='__cov': continue
    if 'chi2' in syst: print 'Found chi2:',syst,', values:',parVals[''][syst][0],', length=',len(parVals[''][syst])
    elif 'ks' in syst: print 'Found K-S:',syst,', values:',parVals[''][syst][0],', length=',len(parVals[''][syst])
    else:
        print syst,"=",parVals[''][syst][0][0],"+/-",parVals[''][syst][0][1]
        parameter_values[syst] = parVals[''][syst][0][0]

pickle.dump(parVals,open(rFileName+'_'+category+'.p','wb'))

histos = evaluate_prediction(model1L, parameter_values, include_signal=False)
write_histograms_to_rootfile(histos, 'histos-mle_'+category+'.root')

if category == 'All':
    #dictionary of values for pre-fit and post-fit nuisance parameters:
    parameter_values_prior = {}
    parameter_values_post = {}

    #dictionary of values for +1 sigma and -1sigma post-fit nuisance parameters:
    parameter_values_plus = {}
    parameter_values_minus = {}
    
    #dictionary of dictionaries, for each nuisance parameter, move only that nuisance parameter to +1 sigma or -1 sigma
    parameter_values_syst_plus = {}
    parameter_values_syst_minus = {}
    
    for p in model1L.get_parameters([]):
        if p == 'beta_signal': continue
        parameter_values_prior[p] = 0.0
        parameter_values_post[p] = parVals[''][p][0][0]
        parameter_values_plus[p] = parVals[''][p][0][0] + parVals[''][p][0][1]
        parameter_values_minus[p] = parVals[''][p][0][0] - parVals[''][p][0][1]
	
    for p in model1L.get_parameters([]):
        if p == 'beta_signal': continue
        parameter_values_syst_plus[p] = parameter_values_post.copy()
        parameter_values_syst_minus[p] = parameter_values_post.copy()

    for p in model1L.get_parameters([]):
        if p == 'beta_signal': continue
        parameter_values_syst_plus[p][p] = parameter_values_plus[p]
        parameter_values_syst_minus[p][p] = parameter_values_minus[p]

    # create root file with pre-fit templates
    histos_prior = evaluate_prediction(model1L, parameter_values_prior, include_signal = False)
    write_histograms_to_rootfile(histos_prior, 'histos-mle_prior_'+rFileName+'_bkgonly.root')

    # create root file with post-fit templates (background-only)
    histos_post = evaluate_prediction(model1L, parameter_values_post, include_signal = False)
    write_histograms_to_rootfile(histos_post, 'histos-mle-post_'+rFileName+'_bkgonly.root')

    # create root files, where for each nuisance parameter, we move only that nuisance parameter by +1/-1 sigma
    histos_syst_plus = {}
    histos_syst_minus = {}

    for p in model1L.get_parameters([]):
        if p == 'beta_signal': continue
        histos_syst_plus[p] = evaluate_prediction(model1L, parameter_values_syst_plus[p],include_signal = False)
        write_histograms_to_rootfile(histos_syst_plus[p], 'histos-mle_'+p+'_plus_'+category+'_bkgonly.root')
        histos_syst_minus[p] = evaluate_prediction(model1L, parameter_values_syst_minus[p], include_signal = False)
        write_histograms_to_rootfile(histos_syst_minus[p], 'histos-mle_'+p+'_minus_'+category+'_bkgonly.root')


from numpy import linalg
import numpy as np

theta_res = parVals['']
param_list = []
for k, res in theta_res.iteritems():
    #print k,',',res
    if any(k == i for i in ['__nll','__cov','__chi2','__ks','beta_signal']): continue
    err_sq = res[0][1]*res[0][1]
    param_list.append((k, err_sq))

cov_matrix = theta_res['__cov'][0]
ind_dict = {}
for i in xrange(cov_matrix.shape[0]):
    for ii in xrange(cov_matrix.shape[1]):
        entry = cov_matrix[i,ii]
        for proc, val in param_list:
            if abs(val-entry) < 1e-6:
                if i != ii:
                    self.message("WARNING row and column index don't match")
                ind_dict[i] = proc
            if i not in ind_dict.keys():
                ind_dict[i] = 'beta_signal'

cov_matrix = np.matrix(cov_matrix)
diag_matrix = np.matrix(np.sqrt(np.diag(np.diag(cov_matrix))))
#try:
inv_matrix = diag_matrix.I
corr_matrix = inv_matrix * cov_matrix * inv_matrix

corr_hist = ROOT.TH2D("correlation_matrix","",len(param_list),0,len(param_list),len(param_list),0,len(param_list))
cov_hist = ROOT.TH2D("covariance_matrix","",len(param_list),0,len(param_list),len(param_list),0,len(param_list))
    
for i in xrange(corr_matrix.shape[0]):
    if i not in ind_dict.keys(): continue
    corr_hist.GetXaxis().SetBinLabel(i+1, ind_dict.get(i,'unknown'))
    corr_hist.GetYaxis().SetBinLabel(i+1, ind_dict.get(i,'unknown'))
    cov_hist.GetXaxis().SetBinLabel(i+1, ind_dict.get(i,'unknown'))
    cov_hist.GetYaxis().SetBinLabel(i+1, ind_dict.get(i,'unknown'))
    corr_hist.SetLabelSize(0.03,'x')
    cov_hist.SetLabelSize(0.03,'x')
    corr_hist.GetZaxis().SetRangeUser(-1,1)
    for ii in xrange(corr_matrix.shape[1]):
        entry_corr = corr_matrix[i,ii]
        entry_cov = cov_matrix[i,ii]
        corr_hist.Fill(i,ii,entry_corr)
        cov_hist.Fill(i,ii,entry_cov)

matrices = ROOT.TFile('mle_covcorr_'+category+'.root','RECREATE')
cov_hist.Write()
corr_hist.Write()
matrices.Close()


