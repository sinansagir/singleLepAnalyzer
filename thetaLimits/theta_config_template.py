
input = 'dummy.root'

rFileName = input.split('/')[-1][:-5]
                                                                                                                                          
def get_model():
    model = build_model_from_rootfile(input,include_mc_uncertainties=True)#,histogram_filter = (lambda s: s.count('jec')==0 and s.count('jer')==0)

    model.fill_histogram_zerobins()
    model.set_signal_processes('sig')
    
    procs = model.processes
    obsvs = model.observables.keys()

#     for obs in obsvs:
# 		if 'isE' in obs:
# 			model.add_lognormal_uncertainty('elIdSys', math.log(1.02), '*', obs)
# 			model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), '*', obs)
# 		elif 'isM' in obs:
# 			model.add_lognormal_uncertainty('muIdSys', math.log(1.03), '*', obs)
# 			model.add_lognormal_uncertainty('muIsoSys', math.log(1.01), '*', obs)
#     model.add_lognormal_uncertainty('lumiSys', math.log(1.026), '*', '*')
    model.add_lognormal_uncertainty('topSys', math.log(1.30), 'top', '*')
    model.add_lognormal_uncertainty('ewkSys', math.log(1.30), 'ewk', '*')
    model.add_lognormal_uncertainty('qcdSys', math.log(1.30), 'qcd', '*')
    model.add_lognormal_uncertainty('sigSys', math.log(1.10), 'sig', '*')
   			
    return model

model = get_model()

##################################################################################################################

model_summary(model)

#plot_exp, plot_obs = bayesian_limits(model,'all')#, n_toy = 5000, n_data = 500)
#plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 100000, n_data = 1000)
plot_exp, plot_obs = bayesian_limits(model,'expected')
plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
#plot_obs.write_txt('limits_'+rFileName+'_observed.txt')

report.write_html('htmlout_'+rFileName)


