import os,sys,pickle
from operator import itemgetter,attrgetter

input = '/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/makeTemplates/templates_Wkshp/templates_minMlb_TTM900_36p0fb_rebinned_stat0p3.root'
rFileName = input.split('/')[-1][:-5]
                                                                          
def get_model():
    model = build_model_from_rootfile(input,include_mc_uncertainties=True)#,histogram_filter = (lambda s: s.count('sig')==0))# and s.count('TTbar__ScaleVar')==0 and s.count('WJets__ScaleVar')==0 and s.count('TTbar__PDF')==0 and s.count('WJets__PDF')==0 ))
    model.fill_histogram_zerobins()
    model.set_signal_processes('sig')
    #model.set_signal_process_groups({'':[]})
    
    procs = model.processes
    obsvs = model.observables.keys()

    for obs in obsvs:
        if 'isE' in obs:
            try: model.add_lognormal_uncertainty('elTrigSys', math.log(1.05), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('elIdSys', math.log(1.02), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('elIsoSys', math.log(1.02), '*', obs)
            except: pass
        elif 'isM' in obs:
            try: model.add_lognormal_uncertainty('muTrigSys', math.log(1.05), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('muIdSys', math.log(1.02), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('muIsoSys', math.log(1.02), '*', obs)
            except: pass

    try: model.add_lognormal_uncertainty('lumiSys', math.log(1.062), '*', '*')
    except: pass

    # flat values for tests
    try: model.add_lognormal_uncertainty('qcdsys', math.log(1.10), 'qcd', '*')
    except: pass
    try: model.add_lognormal_uncertainty('topsys', math.log(1.10), 'top', '*')
    except: pass
    try: model.add_lognormal_uncertainty('ewksys', math.log(1.10), 'ewk', '*')
    except: pass
    try: model.add_lognormal_uncertainty('sigsys', math.log(1.10), 'sig', '*')
    except: pass
    '''
    #modeling uncertainties -- TOP
    for obs in obsvs:
        if 'nW0_nB0' in obs:
            try: model.add_lognormal_uncertainty('top0W0BSys',  math.log(1.157), 'top', obs) # from ttbar CR
            except: pass                                 
        elif 'nW0_nB1' in obs:                           
            try: model.add_lognormal_uncertainty('top0W1BSys',  math.log(1.153), 'top', obs) # from ttbar CR
            except: pass                                 
        elif 'nW0_nB2' in obs:                           
            try: model.add_lognormal_uncertainty('top0W2BSys',  math.log(1.163), 'top', obs) # from ttbar CR
            except: pass                                 
       	elif 'nW0_nB3p' in obs:                          
            try: model.add_lognormal_uncertainty('top0W3pBSys', math.log(1.163), 'top', obs) # from ttbar CR
            except: pass                                 
       	elif 'nW1p_nB0' in obs:                          
            try: model.add_lognormal_uncertainty('top1pW0BSys', math.log(1.157), 'top', obs) # from ttbar CR
            except: pass                                 
        elif 'nW1p_nB1' in obs:                          
            try: model.add_lognormal_uncertainty('top1pW1BSys', math.log(1.153), 'top', obs) # from ttbar CR
            except: pass                                 
       	elif 'nW1p_nB2' in obs:                          
            try: model.add_lognormal_uncertainty('top1pW2BSys', math.log(1.163), 'top', obs) # from ttbar CR
            except: pass                                 
       	elif 'nW1p_nB3p' in obs:                         
            try: model.add_lognormal_uncertainty('top1pW3pBSys',math.log(1.163), 'top', obs) # from ttbar CR
            except: pass
            
    #modeling uncertainties -- EWK
    for obs in obsvs:
        if 'nW0_nB0' in obs:
            try: model.add_lognormal_uncertainty('ewk0W0BSys',  math.log(1.136), 'ewk', obs) # from Wjets CR
            except: pass                                 
        elif 'nW0_nB1' in obs:                           
            try: model.add_lognormal_uncertainty('ewk0W1BSys',  math.log(1.136), 'ewk', obs) # from Wjets CR
            except: pass                                 
        elif 'nW0_nB2' in obs:                           
            try: model.add_lognormal_uncertainty('ewk0W2BSys',  math.log(1.136), 'ewk', obs) # from Wjets CR
            except: pass                                 
        elif 'nW0_nB3p' in obs:                          
            try: model.add_lognormal_uncertainty('ewk0W3pBSys', math.log(1.136), 'ewk', obs) # from Wjets CR
            except: pass                                 
        elif 'nW1p_nB0' in obs:                          
            try: model.add_lognormal_uncertainty('ewk1pW0BSys', math.log(1.133), 'ewk', obs) # from Wjets CR
            except: pass                                 
        elif 'nW1p_nB1' in obs:                          
            try: model.add_lognormal_uncertainty('ewk1pW1BSys', math.log(1.133), 'ewk', obs) # from Wjets CR
            except: pass                                 
        elif 'nW1p_nB2' in obs:                          
            try: model.add_lognormal_uncertainty('ewk1pW2BSys', math.log(1.133), 'ewk', obs) # from Wjets CR
            except: pass                                 
        elif 'nW1p_nB3p' in obs:                         
            try: model.add_lognormal_uncertainty('ewk1pW3pBSys',math.log(1.133), 'ewk', obs) # from Wjets CR
            except: pass
    '''
    return model

##################################################################################################################

model = get_model()
model_summary(model)

options = Options()
#options.set('minimizer', 'strategy', 'robust')
options.set('minimizer', 'minuit_tolerance_factor', '100')

parVals = mle(model, input='data', n=1, with_error=True, with_covariance=True,options = options)#, with_covariance=True)

parameter_values = {}
for syst in parVals['sig'].keys():
    if syst=='__nll' or syst=='__cov': continue
    else:
        print syst,"=",parVals['sig'][syst][0][0],"+/-",parVals['sig'][syst][0][1]
        parameter_values[syst] = parVals['sig'][syst][0][0]

pickle.dump(parVals,open(rFileName+'_withSIG.p','wb'))

histos = evaluate_prediction(model, parameter_values, include_signal=False)
write_histograms_to_rootfile(histos, 'histos-mle_withSIG.root')

from numpy import linalg
import numpy as np

theta_res = parVals['sig']
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

matrices = ROOT.TFile('mle_covcorr_withSIG.root','RECREATE')
cov_hist.Write()
corr_hist.Write()
matrices.Close()
