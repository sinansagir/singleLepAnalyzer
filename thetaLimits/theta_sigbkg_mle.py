import os,sys,pickle
from operator import itemgetter,attrgetter

input = '/user_data/ssagir/CMSSW_7_4_7/src/singleLepAnalyzer/x53x53_2016/makeTemplates/templates_M17WtSF_2017_3_31_SRpCR/templates_minMlb_X53X53M900left_35p867fb_rebinned_stat0p3.root'
rFileName = input.split('/')[-1][:-5]

category = str(sys.argv[2])
print 'File:',rFileName,', category:',category

def get_model():
    if category == 'All': model = build_model_from_rootfile(input,include_mc_uncertainties=True,histogram_filter = (lambda s:  s.count('__pdf__')==0 and s.count('__muR__')==0 and s.count('__muF__')==0 and s.count('__muRFcorrd__')==0 and s.count('__muRFcorrdNew__')==0 and s.count('__trigeff__')==0))
    
    model.fill_histogram_zerobins()
    model.set_signal_processes('sig')
    
    procs = model.processes
    obsvs = model.observables.keys()

    for obs in obsvs:
		if 'isE' in obs:
			#model.add_lognormal_uncertainty('elTrigSys', math.log(1.01), '*', obs)
			model.add_lognormal_uncertainty('elIdSys', math.log(1.02), '*', obs)
			model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), '*', obs)
		elif 'isM' in obs:
			#model.add_lognormal_uncertainty('muTrigSys', math.log(1.01), '*', obs)
			model.add_lognormal_uncertainty('muIdSys', math.log(1.03), '*', obs)
			model.add_lognormal_uncertainty('muIsoSys', math.log(1.01), '*', obs)
    model.add_lognormal_uncertainty('lumiSys', math.log(1.026), '*', '*')
    #try: model.add_lognormal_uncertainty('qcdScale', math.log(1.50), 'qcd', '*')
    #except: pass
    
    #additional uncertainties for missing systs: btag,mistag, and trigEff
#     try: model.add_lognormal_uncertainty('topSys', math.log(1.30), 'top', '*')
#     except: pass
#     try: model.add_lognormal_uncertainty('ewkSys', math.log(1.30), 'ewk', '*')
#     except: pass
#     try: model.add_lognormal_uncertainty('qcdSys', math.log(1.30), 'qcd', '*')
#     except: pass
#     try: model.add_lognormal_uncertainty('sigSys', math.log(1.10), 'sig', '*')
#     except: pass
    			
    return model

##################################################################################################################

model = get_model()
model_summary(model)

options = Options()
options.set('minimizer', 'strategy', 'robust')
options.set('minimizer', 'minuit_tolerance_factor', '100')

parVals = mle(model, input='data', n=1, with_error=True, chi2=True, ks=True, with_covariance=True, options=options)

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
    
    for p in model.get_parameters([]):
        if p == 'beta_signal': continue
        parameter_values_prior[p] = 0.0
        parameter_values_post[p] = parVals['sig'][p][0][0]
        parameter_values_plus[p] = parVals['sig'][p][0][0] + parVals['sig'][p][0][1]
        parameter_values_minus[p] = parVals['sig'][p][0][0] - parVals['sig'][p][0][1]
    	
    for p in model.get_parameters([]):
        if p == 'beta_signal': continue
        parameter_values_syst_plus[p] = parameter_values_post.copy()
        parameter_values_syst_minus[p] = parameter_values_post.copy()
    
    for p in model.get_parameters([]):
        if p == 'beta_signal': continue
        parameter_values_syst_plus[p][p] = parameter_values_plus[p]
        parameter_values_syst_minus[p][p] = parameter_values_minus[p]
    
    # create root file with pre-fit templates
    histos_prior = evaluate_prediction(model, parameter_values_prior, include_signal = False)
    write_histograms_to_rootfile(histos_prior, 'histos-mle_prior_'+rFileName+'_sigbkg.root')
    
    # create root file with post-fit templates (background-only)
    histos_post = evaluate_prediction(model, parameter_values_post, include_signal = False)
    write_histograms_to_rootfile(histos_post, 'histos-mle-post_'+rFileName+'_sigbkg.root')
    
    # create root files, where for each nuisance parameter, we move only that nuisance parameter by +1/-1 sigma
    histos_syst_plus = {}
    histos_syst_minus = {}
    
    for p in model.get_parameters([]):
        if p == 'beta_signal': continue
        histos_syst_plus[p] = evaluate_prediction(model, parameter_values_syst_plus[p],include_signal = False)
        write_histograms_to_rootfile(histos_syst_plus[p], 'histos-mle_'+p+'_plus_'+category+'_sigbkg.root')
        histos_syst_minus[p] = evaluate_prediction(model, parameter_values_syst_minus[p], include_signal = False)
        write_histograms_to_rootfile(histos_syst_minus[p], 'histos-mle_'+p+'_minus_'+category+'_sigbkg.root')
    
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


