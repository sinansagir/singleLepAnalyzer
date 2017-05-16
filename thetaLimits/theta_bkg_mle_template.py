import os,sys,pickle
from operator import itemgetter,attrgetter

input = '/user_data/ssagir/CMSSW_7_4_7/src/singleLepAnalyzer/x53x53_2016/makeTemplates/templates_M17WtSF_2017_3_31_SRpCR/templates_minMlb_X53X53M900left_35p867fb_rebinned_stat0p3.root'
rFileName = input.split('/')[-1][:-5]

sigproc = 'sig'
isBkgOnly = False
if isBkgOnly: sigproc = ''
                                                                                                                                          
def get_model():
    model = build_model_from_rootfile(input,include_mc_uncertainties=True,histogram_filter = (lambda s:  s.count('__pdf__')==0 and s.count('__muR__')==0 and s.count('__muF__')==0 and s.count('__muRFcorrd__')==0 and s.count('__muRFcorrdNew__')==0 and s.count('__trigeff__')==0))
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

def get_bkgonly_model():
    model = build_model_from_rootfile(input,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0 and s.count('__pdf__')==0 and s.count('__muR__')==0 and s.count('__muF__')==0 and s.count('__muRFcorrd__')==0 and s.count('__muRFcorrdNew__')==0 and s.count('__trigeff__')==0))
    model.fill_histogram_zerobins()
    #model.set_signal_processes(sigproc)
    model.set_signal_process_groups({'':[]})
    
    procs = model.processes
    obsvs = model.observables.keys()

    for obs in obsvs:
		if 'isE' in obs:
			#model.add_lognormal_uncertainty('elTrigSys', math.log(1.05), '*', obs)
			model.add_lognormal_uncertainty('elIdSys', math.log(1.02), '*', obs)
			model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), '*', obs)
		elif 'isM' in obs:
			#model.add_lognormal_uncertainty('muTrigSys', math.log(1.05), '*', obs)
			model.add_lognormal_uncertainty('muIdSys', math.log(1.03), '*', obs)
			model.add_lognormal_uncertainty('muIsoSys', math.log(1.01), '*', obs)
    model.add_lognormal_uncertainty('lumiSys', math.log(1.026), '*', '*')
#     try: model.add_lognormal_uncertainty('qcdmuRFcorrdNew', math.log(1.35), 'qcd', '*')
#     except: pass
    
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

parVals = mle(model, input='data', n=1, with_error=True, with_covariance=True,options = options)

parameter_values = {}
for syst in parVals[sigproc].keys():
    if syst=='__nll' or syst=='__cov': continue
    else:
        print syst,"=",parVals[sigproc][syst][0][0],"+/-",parVals[sigproc][syst][0][1]
        parameter_values[syst] = parVals[sigproc][syst][0][0]

if isBkgOnly: pickle.dump(parVals,open(rFileName+'_bkgonly.p','wb'))
else: pickle.dump(parVals,open(rFileName+'.p','wb'))

histos = evaluate_prediction(model, parameter_values, include_signal=False)
if isBkgOnly: write_histograms_to_rootfile(histos, 'histos-mle_'+rFileName+'_bkgonly.root')
else: write_histograms_to_rootfile(histos, 'histos-mle_'+rFileName+'.root')

from numpy import linalg
import numpy as np

theta_res = parVals[sigproc]
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
