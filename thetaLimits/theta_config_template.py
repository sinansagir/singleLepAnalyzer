
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
			model.add_lognormal_uncertainty('elTrigSys', math.log(1.01), '*', obs)
			model.add_lognormal_uncertainty('elIdSys', math.log(1.01), '*', obs)
			model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), '*', obs)
		elif 'isM' in obs:
			model.add_lognormal_uncertainty('muTrigSys', math.log(1.0112), '*', obs)
			model.add_lognormal_uncertainty('muIdSys', math.log(1.0112), '*', obs)
			model.add_lognormal_uncertainty('muIsoSys', math.log(1.03), '*', obs)
    model.add_lognormal_uncertainty('lumiSys', math.log(1.062), '*', '*')

    #modeling uncertainties: Inclusive WJets sample, NOT REWEIGHTED, 8SEP16--SS
    for obs in obsvs:
		if 'nT0_nW0_nB1' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top0T0W1BSys',  math.log(1.11), 'top', obs) #1 b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk0T0W1BSys',  math.log(1.12), 'ewk', obs) #0 W-tag
		if 'nT0_nW0_nB2p' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top0T0W2pBSys', math.log(1.15), 'top', obs) #2+ b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk0T0W2pBSys', math.log(1.12), 'ewk', obs) #0 W-tag
		if 'nT0_nW1p_nB1' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top0T1pW1BSys', math.log(1.11), 'top', obs) #1 b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk0T1pW1BSys', math.log(1.12), 'ewk', obs) #1+ W-tag
		if 'nT0_nW1p_nB2p' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top0T1pW2pBSys',math.log(1.15), 'top', obs) #2+ b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk0T1pW2pBSys',math.log(1.12), 'ewk', obs) #1+ W-tag
		if 'nT1p_nW0_nB1' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top1pT0W1BSys', math.log(1.11), 'top', obs) #1 b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk1pT0W1BSys', math.log(1.12), 'ewk', obs) #0 W-tag
		if 'nT1p_nW0_nB2p' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top1pT0W2pBSys',math.log(1.15), 'top', obs) #2+ b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk1pT0W2pBSys',math.log(1.12), 'ewk', obs) #0 W-tag
		if 'nT1p_nW1p_nB1' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top1pT1pW1BSys',math.log(1.11), 'top', obs) #1 b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk1pT1pW1BSys',math.log(1.12), 'ewk', obs) #1+ W-tag
		if 'nT1p_nW1p_nB2p' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top1pT1pW2pBSys',math.log(1.15),'top', obs) #2+ b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk1pT1pW2pBSys',math.log(1.12),'ewk', obs) #1+ W-tag
		#for no top tag categories
		if 'nT0p_nW0_nB1' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top0W1BSys',  math.log(1.11), 'top', obs) #1 b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk0W1BSys',  math.log(1.12), 'ewk', obs) #0 W-tag
		if 'nT0p_nW0_nB2p' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top0W2pBSys', math.log(1.15), 'top', obs) #2+ b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk0W2pBSys', math.log(1.12), 'ewk', obs) #0 W-tag
		if 'nT0p_nW1p_nB1' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top1pW1BSys', math.log(1.11), 'top', obs) #1 b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk1pW1BSys', math.log(1.12), 'ewk', obs) #1+ W-tag
		if 'nT0p_nW1p_nB2p' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top1pW2pBSys',math.log(1.15), 'top', obs) #2+ b-tag
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk1pW2pBSys',math.log(1.12), 'ewk', obs) #1+ W-tag
			
    return model

model = get_model()

##################################################################################################################

model_summary(model)

plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 5000, n_data = 500)
#plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 100000, n_data = 1000)
#plot_exp, plot_obs = bayesian_limits(model,'expected')
plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
plot_obs.write_txt('limits_'+rFileName+'_observed.txt')

report.write_html('htmlout_'+rFileName)
