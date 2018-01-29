import os,sys,pickle
from operator import itemgetter,attrgetter

# input = '/user_data/rsyarif/optimization_reMiniAOD_PRv9_FRv30CR2_newRunH_correctedMuTrkSF_AllSys_2017_4_14/lep1Pt0_jetPt0_MET20_NJets3_NBJets1_HT0_ST0_mllOS20/Shape_accurateLHESys_FRsysMar28_newSigSF/templates_STrebinnedv2_TTM1000_bW0p5_tZ0p25_tH0p25_35p867fb.root'
input = '/user_data/rsyarif/optimization_reMiniAOD_PRv9_FRv30CR2_newRunH_correctedMuTrkSF_AllSys_2017_4_14/lep1Pt0_jetPt0_MET20_NJets3_NBJets1_HT0_ST0_mllOS20/Shape_accurateLHESys_FRsysMar28_newSigSF_AsymmFRsys/templates_STrebinnedv2_TTM1000_bW0p5_tZ0p25_tH0p25_35p867fb.root'
# input = '/user_data/rsyarif/optimization_reMiniAOD_PRv10_FRv42CR2_newRunH_correctedMuTrkSF_AllSys_2017_7_4/lep1Pt0_jetPt0_MET20_NJets3_NBJets1_HT0_ST0_mllOS20/Shape_accurateLHESys_FRsysMar28_newSigSF_AsymmFRsys/templates_STrebinnedv2_TTM1000_bW0p5_tZ0p25_tH0p25_35p867fb.root'
rFileName = input.split('/')[-1][:-5]
print 'rFileName:', rFileName
                                                                                                                                          
sigproc = 'sig'
isBkgOnly = True
if isBkgOnly: sigproc = ''

def get_bkgonly_model():
#     model = build_model_from_rootfile(input,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('__pdf__')==0 and s.count('__muR__')==0 and s.count('__muF__')==0 and s.count('__muRFcorrd__')==0 and s.count('__muRFcorrdNew__')==0 and s.count('__trigeff__')==0) )
    model = build_model_from_rootfile(input,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('muR__')==0 and s.count('muF__')==0 and s.count('muRFcorrd__')==0 and s.count('elelelTrigSys')==0 and s.count('elelmuTrigSys')==0 and s.count('elmumuTrigSys')==0 and s.count('mumumuTrigSys')==0 and s.count('elIsoSys')==0 and s.count('elIdSys')==0 and s.count('muIsoSys')==0 and s.count('muIdSys')==0 and s.count('PR__')==0)) #for PRv9
#     model = build_model_from_rootfile(input,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('muR__')==0 and s.count('muF__')==0 and s.count('muRFcorrd__')==0 and s.count('elelelTrigSys')==0 and s.count('elelmuTrigSys')==0 and s.count('elmumuTrigSys')==0 and s.count('mumumuTrigSys')==0 and s.count('elIsoSys')==0 and s.count('elIdSys')==0 and s.count('muIsoSys')==0 and s.count('muIdSys')==0 and s.count('PRsys__')==0)) #for PRv10
    model.fill_histogram_zerobins()
    #model.set_signal_processes(sigproc)
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
            try: model.add_lognormal_uncertainty('eeeTrigSys', math.log(1.03), proc, 'triLepEEE')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('eemTrigSys', math.log(1.03), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('emmTrigSys', math.log(1.03), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('mmmTrigSys', math.log(1.03), proc, 'triLepMMM')
            except RuntimeError: pass

            try: model.add_lognormal_uncertainty('lumiSys', math.log(1.026), proc, '*')
            except RuntimeError: pass

#         else:
#             try: model.add_lognormal_uncertainty('FRsys',math.log(1.20),proc,'triLepMMM')
#             except RuntimeError: pass
#             try: model.add_lognormal_uncertainty('FRsys',math.log(1.12),proc,'triLepEMM')
#             except RuntimeError: pass
#             try: model.add_lognormal_uncertainty('FRsys',math.log(1.26),proc,'triLepEEM')
#             except RuntimeError: pass
#             try: model.add_lognormal_uncertainty('FRsys',math.log(1.24),proc,'triLepEEE')
#             except RuntimeError: pass

#     flatpars = {'mean': 0.0, 
#                 'range': [float('-inf'), float('inf')], 
#                 'typ': 'gauss', 
#                 'width': float('inf')}
#     
#     model.distribution.distributions.update({'elFR': flatpars})
#     model.distribution.distributions.update({'elPR': flatpars})
#     model.distribution.distributions.update({'elPRsys': flatpars})
#     model.distribution.distributions.update({'FRsys': flatpars})
    			
    return model

if isBkgOnly: model = get_bkgonly_model()
else: model = get_model()
model_summary(model)
##################################################################################################################

#plot_exp, plot_obs = bayesian_limits(model,'all')#, n_toy = 5000, n_data = 500)
#plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 100000, n_data = 1000)
#plot_exp, plot_obs = bayesian_limits(model,'expected')
#plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
#plot_obs.write_txt('limits_'+rFileName+'_observed.txt')

#report.write_html('htmlout_'+rFileName)

options = Options()
#options.set('minimizer', 'strategy', 'robust')
options.set('minimizer', 'minuit_tolerance_factor', '100')

fit = mle(model, input='data', n=1, with_error=True, with_covariance=True,options = options)
#print fit

if isBkgOnly: pickle.dump(fit,open(rFileName+'_bkgonly.p','wb'))
else: pickle.dump(fit,open(rFileName+'.p','wb'))

parameter_values = {}
for syst in fit[sigproc].keys():
    if syst=='__nll' or syst=='__cov': continue
    else:
        print syst,"=",fit[sigproc][syst][0][0],"+/-",fit[sigproc][syst][0][1]
        parameter_values[syst] = fit[sigproc][syst][0][0]

histos = evaluate_prediction(model, parameter_values, include_signal=False)
# if isBkgOnly: write_histograms_to_rootfile(histos, 'histos-mle_'+rFileName+'_bkgonly.root')
if isBkgOnly: write_histograms_to_rootfile(histos, 'histos-mle_'+rFileName+'_bkgonly.root')
else: write_histograms_to_rootfile(histos, 'histos-mle_'+rFileName+'.root')

########### From Andrew - start ################

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
	parameter_values_prior[p] = 0.0
	parameter_values_post[p] = fit[sigproc][p][0][0]
	parameter_values_plus[p] = fit[sigproc][p][0][0] + fit[sigproc][p][0][1]
	parameter_values_minus[p] = fit[sigproc][p][0][0] - fit[sigproc][p][0][1]
	
for p in model.get_parameters([]):
	parameter_values_syst_plus[p] = parameter_values_post.copy()
	parameter_values_syst_minus[p] = parameter_values_post.copy()

for p in model.get_parameters([]):
	parameter_values_syst_plus[p][p] = parameter_values_plus[p]
	parameter_values_syst_minus[p][p] = parameter_values_minus[p]

# create root file with pre-fit templates
histos_prior = evaluate_prediction(model, parameter_values_prior, include_signal = False)
write_histograms_to_rootfile(histos_prior, 'histos-mle_prior_'+rFileName+'_bkgonly.root')

# create root file with post-fit templates (background-only)
histos_post = evaluate_prediction(model, parameter_values_post, include_signal = False)
write_histograms_to_rootfile(histos_post, 'histos-mle-post_'+rFileName+'_bkgonly.root')

# create root files, where for each nuisance parameter, we move only that nuisance parameter by +1/-1 sigma
histos_syst_plus = {}
histos_syst_minus = {}

for p in model.get_parameters([]):
	histos_syst_plus[p] = evaluate_prediction(model, parameter_values_syst_plus[p],include_signal = False)
	write_histograms_to_rootfile(histos_syst_plus[p], 'histos-mle_'+p+'_plus_'+rFileName+'_bkgonly.root')
	histos_syst_minus[p] = evaluate_prediction(model, parameter_values_syst_minus[p], include_signal = False)
	write_histograms_to_rootfile(histos_syst_minus[p], 'histos-mle_'+p+'_minus_'+rFileName+'_bkgonly.root')


########### From Andrew - end ################


from numpy import linalg
import numpy as np

theta_res = fit[sigproc]
param_list = []
for k, res in theta_res.iteritems():
    #print k,',',res
    if any(k == i for i in ['__nll','__cov']): continue
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
                    print "process:", proc
                    print "WARNING row and column index don't match"
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

if isBkgOnly: matrices = ROOT.TFile('mle_covcorr_'+rFileName+'_bkgonly.root','RECREATE')
else: matrices = ROOT.TFile('mle_covcorr_'+rFileName+'.root','RECREATE')
cov_hist.Write()
corr_hist.Write()
matrices.Close()

# xsec = {}
# xsec['X53X53M700left']   = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M700right']  = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M800left']   = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M800right']  = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M900left']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M900right']  = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1000left']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1000right'] = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1100left']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1100right'] = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1200left']  = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1200right'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1300left']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1300right'] = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1400left']  = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1400right'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1500left']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1500right'] = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1600left']  = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xsec['X53X53M1600right'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
# xs=xsec[rFileName.split('_')[2]]
# print "xsec =",xs
# 
# signal_process_groups = {sigproc: [sigproc]}
# import json
# f = open(rFileName+'.json', 'w')
# disc = discovery(model,use_data = False,input_expected='toys:%f' % xs,spid=sigproc,Z_error_max=0.1,ts_method=derll)
# #disc = discovery(model, spid = sigproc, use_data = False, input_expected = 'toys:%f' % xs, maxit = 2, n = 1000000)
# print disc
# json.dump(disc, f)
