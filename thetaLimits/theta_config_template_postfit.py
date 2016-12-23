import os,sys,pickle
from operator import itemgetter,attrgetter

input = 'dummy.root'

rFileName = input.split('/')[-1][:-5]
                                                                                                                                          
def get_model():
    model = build_model_from_rootfile(input,include_mc_uncertainties=True)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)

    model.fill_histogram_zerobins()
    model.set_signal_processes('sig')
    
    procs = model.processes
    obsvs = model.observables.keys()

    for obs in obsvs:
		if 'isE' in obs:
			model.add_lognormal_uncertainty('elTrigSys', math.log(1.03), '*', obs)
			model.add_lognormal_uncertainty('elIdSys', math.log(1.01), '*', obs)
			model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), '*', obs)
		elif 'isM' in obs:
			model.add_lognormal_uncertainty('muTrigSys', math.log(1.011), '*', obs)
			model.add_lognormal_uncertainty('muIdSys', math.log(1.011), '*', obs)
			model.add_lognormal_uncertainty('muIsoSys', math.log(1.03), '*', obs)
    model.add_lognormal_uncertainty('lumiSys', math.log(1.062), '*', '*')
    
    try: model.add_lognormal_uncertainty('topSys', math.log(1.50), 'top', '*')
    except: pass
    try: model.add_lognormal_uncertainty('ewkSys', math.log(1.50), 'ewk', '*')
    except: pass
    try: model.add_lognormal_uncertainty('qcdSys', math.log(1.50), 'qcd', '*')
    except: pass
    try: model.add_lognormal_uncertainty('ttbarSys', math.log(1.50), 'ttbar', '*')
    except: pass
    try: model.add_lognormal_uncertainty('wjetsSys', math.log(1.50), 'wjets', '*')
    except: pass
    try: model.add_lognormal_uncertainty('sigSys', math.log(1.10), 'sig', '*')
    except: pass
    			
    return model

model = get_model()

##################################################################################################################

# model_summary(model)
# 
# plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 5000, n_data = 500)
# #plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 100000, n_data = 1000)
# #plot_exp, plot_obs = bayesian_limits(model,'expected')
# plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
# plot_obs.write_txt('limits_'+rFileName+'_observed.txt')
# 
# report.write_html('htmlout_'+rFileName)

options = Options()
options.set('minimizer', 'strategy', 'robust')
options.set('minimizer', 'minuit_tolerance_factor', '1000')


parVals = mle(model, input='data', n=1, options = options)#, with_covariance=True)

#print parVals['sig']
for syst in parVals['sig'].keys():
	if syst=='__cov' or syst=='__nll': continue
	print syst,"=",parVals['sig'][syst][0][0],"+/-",parVals['sig'][syst][0][1]

pickle.dump(parVals,open(rFileName+'.p','wb'))

# signal_process_groups = {'': []}
# parameter_values = {}
# for p in model.get_parameters([]):
#     parameter_values[p] = parVals['sig'][p][0][0]
# histos = evaluate_prediction(model, parameter_values, include_signal = False)
# write_histograms_to_rootfile(histos, 'histos-mle.root')
# #print parVals
# 
# bayesian_posterior_model_prediction(model, input='data', n=1)
# 
# model_summary(model, True, True, True)

# model_summary(model)
# 
# #plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 5000, n_data = 500)
# plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 100000, n_data = 1000)
# #plot_exp, plot_obs = bayesian_limits(model,'expected')
# plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
# plot_obs.write_txt('limits_'+rFileName+'_observed.txt')
# 
# report.write_html('htmlout_'+rFileName)

