import os,sys,pickle
from operator import itemgetter,attrgetter

input0H = '/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/makeTemplates/templates4CRhtSR_ARC/splitLess/templates_minMlbST_TTM1000_bW0p5_tZ0p25_tH0p25_36p814fb_rebinned_stat0p3.root'

rFileName = input0H.split('/')[-1][:-5]

category = str(sys.argv[2])
print 'File:',rFileName,', category:',category

                                                                                                                                          
def get0H_model():
    if category == 'All': model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('DATA')==0))
    if category == 'Higgs': model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('DATA')==0 and s.count('nH0')==0))
    if category == 'Higgs1b': model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('DATA')==0 and s.count('nH0')==0 and s.count('nH2b')==0))
    if category == 'Higgs2b': model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('DATA')==0 and s.count('nH0')==0 and s.count('nH1b')==0))
    if category == 'Wtag1': model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('DATA')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nW0_')==0))
    if category == 'Wtag0': model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('DATA')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nW1p_')==0))
    if category == 'Btag0': model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('DATA')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB1')==0 and s.count('nB2_')==0 and s.count('nB3p_')==0))
    if category == 'Btag1': model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('DATA')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB0_')==0 and s.count('nB2_')==0 and s.count('nB3p_')==0))
    if category == 'Btag2': model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('DATA')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB0_')==0 and s.count('nB1_')==0 and s.count('nB3p_')==0))
    if category == 'Btag3': model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('DATA')==0 and s.count('nH1')==0 and s.count('nH2b')==0 and s.count('nB0_')==0 and s.count('nB1_')==0 and s.count('nB2_')==0))
    
    model.fill_histogram_zerobins()
    model.set_signal_process_groups({'':[]})
    
    procs = model.processes
    obsvs = model.observables.keys()
    
    for obs in obsvs:
        if 'isE' in obs:
            try: model.add_lognormal_uncertainty('sfel_id', math.log(1.02), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_iso', math.log(1.01), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_gsf', math.log(1.01), '*', obs)
            except RuntimeError: pass
        elif 'isM' in obs:
            try: model.add_lognormal_uncertainty('sfmu_id', math.log(1.03), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_iso', math.log(1.01), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_trk', math.log(1.01), '*', obs)
            except RuntimeError: pass
        if 'H1b' in obs or 'H2b' in obs:
            try: model.add_lognormal_uncertainty('higgs_prop',math.log(1.05), '*', obs)
            except:pass
        else:
            try: model.add_lognormal_uncertainty('higgs_prop',math.log(0.95), '*', obs)
            except:pass
            

    try: model.add_lognormal_uncertainty('luminosity', math.log(1.025), '*', '*')
    except RuntimeError: pass

    flatpars = {'mean': 0.0, 
                'range': [float('-inf'), float('inf')], 
                'typ': 'gauss', 
                'width': float('inf')}
    
    #try: model.add_lognormal_uncertainty('top_rate', math.log(1.10), 'top','*')
    #except RuntimeError: pass
    #model.distribution.distributions.update({'top_rate': flatpars})

    #try: model.add_lognormal_uncertainty('ewk_rate', math.log(1.10), 'ewk','*')
    #except RuntimeError: pass
    #model.distribution.distributions.update({'ewk_rate': flatpars})


    return model


##################################################################################################################

model = get0H_model()

model_summary(model)

options = Options()
options.set('minimizer', 'strategy', 'robust')
options.set('minimizer', 'minuit_tolerance_factor', '100')

parVals = mle(model, input='toys-asimov:0', n=1, with_error=True, chi2=True, ks=True, with_covariance=True, options=options)

parameter_values = {}
for syst in parVals[''].keys():
    if syst=='__nll' or syst=='__cov': continue
    if 'chi2' in syst: print 'Found chi2:',syst,', values:',parVals[''][syst][0],', length=',len(parVals[''][syst])
    elif 'ks' in syst: print 'Found K-S:',syst,', values:',parVals[''][syst][0],', length=',len(parVals[''][syst])
    else:
        print syst,"=",parVals[''][syst][0][0],"+/-",parVals[''][syst][0][1]
        parameter_values[syst] = parVals[''][syst][0][0]

pickle.dump(parVals,open(rFileName+'_'+category+'.p','wb'))

histos = evaluate_prediction(model, parameter_values, include_signal=False)
write_histograms_to_rootfile(histos, 'histos-mle_'+category+'.root')

from numpy import linalg
import numpy as np

theta_res = parVals['']
param_list = []
for k, res in theta_res.iteritems():
    #print k,',',res
    if any(k == i for i in ['__nll','__cov','__chi2','__ks']): continue
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


