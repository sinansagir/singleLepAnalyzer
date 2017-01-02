import os,sys,pickle
from operator import itemgetter,attrgetter

input0H = '/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/makeTemplates/TTWJ_bkg_mle.root'

rFileName = input0H.split('/')[-1][:-5]
                                                                                                                                          
def get0H_model():
    model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sig')==0))
    
    model.fill_histogram_zerobins()
    model.set_signal_process_groups({'':[]})
    
    procs = model.processes
    obsvs = model.observables.keys()
    
    for obs in obsvs:
        if 'isE' in obs:
            try: model.add_lognormal_uncertainty('sfel_trg', math.log(1.05), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_id', math.log(1.02), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_iso', math.log(1.02), '*', obs)
            except RuntimeError: pass
        elif 'isM' in obs:
            try: model.add_lognormal_uncertainty('sfmu_trg', math.log(1.05), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_id', math.log(1.02), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_iso', math.log(1.02), '*', obs)
            except RuntimeError: pass
    try: model.add_lognormal_uncertainty('luminosity', math.log(1.062), '*', '*')
    except RuntimeError: pass

    flatpars = {'mean': 0.0, 
                'range': [float('-inf'), float('inf')], 
                'typ': 'gauss', 
                'width': float('inf')}

    try: model.add_lognormal_uncertainty('top_rate', math.log(1.50), 'top','*')
    except RuntimeError: pass
    try: model.add_lognormal_uncertainty('ewk_rate', math.log(1.50), 'ewk','*')
    except RuntimeError: pass

    model.distribution.distributions.update({
            'top_rate': flatpars,
            'ewk_rate': flatpars})

    '''
    try: 
        model.add_lognormal_uncertainty('ewk_rate', math.log(1.0), 'ewk','*')
        model.distribution.set_distribution('ewk_rate', 'gauss', mean = 0.0, width = float("inf"), range = [-float("inf"), float("inf")])
    except RuntimeError: pass


    for proc in procs:
        if proc != 'TTbar': continue # and proc != 'SingleTop': continue
        for obs in obsvs:
            if 'nW0_nB0' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.111), proc, obs) # from ttbar CR
                except: pass
            if 'nW0_nB1' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.051), proc, obs) # from ttbar CR
                except: pass
            if 'nW0_nB2' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.055), proc, obs) # from ttbar CR
                except: pass
            if 'nW0_nB3p' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.055), proc, obs) # from ttbar CR
                except: pass
            if 'nW1p_nB0' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.111), proc, obs) # from ttbar CR
                except: pass
            if 'nW1p_nB1' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.051), proc, obs) # from ttbar CR
                except: pass
            if 'nW1p_nB2' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.055), proc, obs) # from ttbar CR
                except: pass
            if 'nW1p_nB3p' in obs:
                try: model.add_lognormal_uncertainty('TTbar_rate',math.log(1.055), proc, obs) # from ttbar CR
                except: pass

    for proc in procs:
        if proc != 'WJets': continue #proc != 'DYJets' and 
        for obs in obsvs:
            if 'nW0_nB0' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.182), proc, obs) # from Wjets CR
                except: pass
            if 'nW0_nB1' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.182), proc, obs) # from Wjets CR
                except: pass
            if 'nW0_nB2' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.182), proc, obs) # from Wjets CR
                except: pass
            if 'nW0_nB3p' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.182), proc, obs) # from Wjets CR
                except: pass
            if 'nW1p_nB0' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.046), proc, obs) # from Wjets CR
                except: pass
            if 'nW1p_nB1' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.046), proc, obs) # from Wjets CR
                except: pass
            if 'nW1p_nB2' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.046), proc, obs) # from Wjets CR
                except: pass
            if 'nW1p_nB3p' in obs:
                try: model.add_lognormal_uncertainty('WJets_rate',math.log(1.046), proc, obs) # from Wjets CR
                except: pass
    '''    
    return model


##################################################################################################################

Model0H = get0H_model()

#Model1H = get1H_model()
#Model0H.combine(Model1H)

options = Options()
options.set('minimizer', 'strategy', 'robust')
options.set('minimizer', 'minuit_tolerance_factor', '100')


parVals = mle(Model0H, input='data', n=1, options = options)#, with_covariance=True)

print parVals

for syst in parVals[''].keys():
	if syst=='__cov' or syst=='__nll': continue
	print syst,"=",parVals[''][syst][0][0],"+/-",parVals[''][syst][0][1]

pickle.dump(parVals,open(rFileName+'.p','wb'))

