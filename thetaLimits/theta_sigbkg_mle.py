import os,sys,pickle
from operator import itemgetter,attrgetter

input1L = '/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/makeTemplates/templates4CRhtSR_NewEl/splitLess/templates_minMlbST_TTM1000_bW0p5_tZ0p25_tH0p25_36p814fb_BKGNORM_rebinned_stat0p3.root'
input3L = '/user_data/rsyarif/optimization_reMiniAOD_PRv9_FRv45FRSRHT400low_newRunH_correctedMuTrkSF_fixedMlllBUnc_AllSys_2017_8_14/lep1Pt0_jetPt0_MET20_NJets3_NBJets1_HT400_ST0_mllOS20/Shape_accurateLHESys_FRsysMar28_newSigSF_AsymmFRsys/templates_minMlllBv4_TTM1000_bW0p5_tZ0p25_tH0p25_35p867fb.root'

rFileName = input1L.split('/')[-1][:-5]

category = str(sys.argv[2])
print 'File:',rFileName,', category:',category
                                                                                                                                   
def get_model1L():
    if category == 'All' or category == 'comb': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0))
    if category == 'AllNoB0': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('_nH1p_nW0p_nB0_isCR_')==0 and s.count('_nB0_isSR_')==0))
    if category == 'AllNoCRHB0': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('_nH1p_nW0p_nB0_isCR_')==0))


    if category == 'Higgs': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('nH0')==0))
    if category == 'Higgs1b': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('nH0')==0 and s.count('nH2b')==0))
    if category == 'Higgs2b': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('nH0')==0 and s.count('nH1b')==0))
    if category == 'Wtag1': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nW0_')==0))
    if category == 'Wtag0': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nW1p_')==0))
    if category == 'Btag0': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB1')==0 and s.count('nB2_')==0 and s.count('nB3p_')==0))
    if category == 'Btag1': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB0_')==0 and s.count('nB2_')==0 and s.count('nB3p_')==0))
    if category == 'Btag2': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB0_')==0 and s.count('nB1_')==0 and s.count('nB3p_')==0))
    if category == 'Btag3': model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('toppt')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB0_')==0 and s.count('nB1_')==0 and s.count('nB2_')==0))

    model.fill_histogram_zerobins()
    model.set_signal_processes('sig')
    
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
    try: model.add_lognormal_uncertainty('TTbarscale', math.log(1.30),'TTbar','*')
    except RuntimeError: pass
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

def get_model3L():
    model = build_model_from_rootfile(input3L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('muR__')==0 and s.count('muF__')==0 and s.count('muRFcorrd__')==0 and s.count('elelelTrigSys')==0 and s.count('elelmuTrigSys')==0 and s.count('elmumuTrigSys')==0 and s.count('mumumuTrigSys')==0 and s.count('elIsoSys')==0 and s.count('elIdSys')==0 and s.count('muIsoSys')==0 and s.count('muIdSys')==0 and s.count('PR__')==0))

    #
    model.fill_histogram_zerobins()
    model.set_signal_processes('sig')
    
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
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.36),proc,'triLepMMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.18),proc,'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.29),proc,'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.38),proc,'triLepEEE')
            except RuntimeError: pass


    return model

##################################################################################################################

model1L = get_model1L()

if category == 'comb':
    model3L = get_model3L()
    model1L.combine(model3L)

model_summary(model1L)

options = Options()
options.set('minimizer', 'strategy', 'robust')
options.set('minimizer', 'minuit_tolerance_factor', '100')

parVals = mle(model1L, input='data', n=1, with_error=True, chi2=True, ks=True, with_covariance=True, options=options)

parameter_values = {}
for syst in parVals['sig'].keys():
    if syst=='__nll' or syst=='__cov': continue
    if 'chi2' in syst: print 'Found chi2:',syst,', values:',parVals['sig'][syst][0],', length=',len(parVals['sig'][syst])
    elif 'ks' in syst: print 'Found K-S:',syst,', values:',parVals['sig'][syst][0],', length=',len(parVals['sig'][syst])
    else:
        print syst,"=",parVals['sig'][syst][0][0],"+/-",parVals['sig'][syst][0][1]
        parameter_values[syst] = parVals['sig'][syst][0][0]

pickle.dump(parVals,open(rFileName+'_'+category+'.p','wb'))

histos = evaluate_prediction(model1L, parameter_values, include_signal=False)
write_histograms_to_rootfile(histos, 'histos-mle_'+category+'.root')

if 'All' in category:
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
        parameter_values_post[p] = parVals['sig'][p][0][0]
        parameter_values_plus[p] = parVals['sig'][p][0][0] + parVals['sig'][p][0][1]
        parameter_values_minus[p] = parVals['sig'][p][0][0] - parVals['sig'][p][0][1]
    	
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
    write_histograms_to_rootfile(histos_prior, 'histos-mle_prior_'+rFileName+'_sigbkgNoB0.root')
    
    # create root file with post-fit templates (background-only)
    histos_post = evaluate_prediction(model1L, parameter_values_post, include_signal = False)
    write_histograms_to_rootfile(histos_post, 'histos-mle-post_'+rFileName+'_sigbkgNoB0.root')
    
    # create root files, where for each nuisance parameter, we move only that nuisance parameter by +1/-1 sigma
    histos_syst_plus = {}
    histos_syst_minus = {}
    
    for p in model1L.get_parameters([]):
        if p == 'beta_signal': continue
        histos_syst_plus[p] = evaluate_prediction(model1L, parameter_values_syst_plus[p],include_signal = False)
        write_histograms_to_rootfile(histos_syst_plus[p], 'histos-mle_'+p+'_plus_'+category+'_sigbkgNoB0.root')
        histos_syst_minus[p] = evaluate_prediction(model1L, parameter_values_syst_minus[p], include_signal = False)
        write_histograms_to_rootfile(histos_syst_minus[p], 'histos-mle_'+p+'_minus_'+category+'_sigbkgNoB0.root')
    
from numpy import linalg
import numpy as np

theta_res = parVals['sig']
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


