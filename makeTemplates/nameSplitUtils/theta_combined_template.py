import os,sys
from operator import itemgetter,attrgetter

outDir = os.environ['CMSSW_BASE']

input0H = ''

#
input1H = ''

rFileName = input0H.split('/')[-1][:-5]
                                                                                                        
def get0H_model():
    print 'getting 0H model from',input0H
    model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('q2')==0))
    
    model.fill_histogram_zerobins()
    model.set_signal_processes('TpTp_M-*')
    
    procs = model.processes
    obsvs = model.observables.keys()

    # Luminosity
    try: model.add_lognormal_uncertainty('luminosity', math.log(1.027), '*', '*')
    except RuntimeError: pass
    
    # ID, trigger, iso scale factor uncertainties
    for obs in obsvs:
        print obs
        if 'isE' in obs:
            try: model.add_lognormal_uncertainty('sfel_trg', math.log(1.05), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_id', math.log(1.01), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_iso', math.log(1.01), '*', obs)
            except RuntimeError: pass
        elif 'isM' in obs:
            try: model.add_lognormal_uncertainty('sfmu_trg', math.log(1.05), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_id', math.log(1.01), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_iso', math.log(1.01), '*', obs)
            except RuntimeError: pass

    # Rate uncertainties
    try: model.add_lognormal_uncertainty('SingleTop_rate',  math.log(1.16), 'SingleTop', '*') # from ttbar CR
    except RuntimeError: pass
    try: model.add_lognormal_uncertainty('Diboson_rate',  math.log(1.15), 'Diboson', '*') # from ttbar CR
    except RuntimeError: pass
    #try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.109), 'TTbar', '*') # from ttbar CR
    #except: pass
    #try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.183), 'WJets', '*') # from Wjets CR
    #except: pass
    
    for obs in obsvs:
        if 'nW0_nB0' in obs:
            try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.109), 'TTbar', obs) # from ttbar CR
            except: pass
        if 'nW0_nB1' in obs:
            try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.026), 'TTbar', obs) # from ttbar CR
            except: pass
        if 'nW0_nB2' in obs:
            try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.070), 'TTbar', obs) # from ttbar CR
            except: pass
        if 'nW0_nB3p' in obs:
            try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.070), 'TTbar', obs) # from ttbar CR
            except: pass
        if 'nW1p_nB0' in obs:
            try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.109), 'TTbar', obs) # from ttbar CR
            except: pass
        if 'nW1p_nB1' in obs:
            try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.026), 'TTbar', obs) # from ttbar CR
            except: pass
        if 'nW1p_nB2' in obs:
            try: model.add_lognormal_uncertainty('TTbar_rate', math.log(1.070), 'TTbar', obs) # from ttbar CR
            except: pass
        if 'nW1p_nB3p' in obs:
            try: model.add_lognormal_uncertainty('TTbar_rate',math.log(1.070), 'TTbar', obs) # from ttbar CR
            except: pass

    for obs in obsvs:
        if 'nW0_nB0' in obs:
            try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.183), 'WJets', obs) # from Wjets CR
            except: pass
        if 'nW0_nB1' in obs:
            try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.183), 'WJets', obs) # from Wjets CR
            except: pass
        if 'nW0_nB2' in obs:
            try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.183), 'WJets', obs) # from Wjets CR
            except: pass
        if 'nW0_nB3p' in obs:
            try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.183), 'WJets', obs) # from Wjets CR
            except: pass
        if 'nW1p_nB0' in obs:
            try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.036), 'WJets', obs) # from Wjets CR
            except: pass
        if 'nW1p_nB1' in obs:
            try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.036), 'WJets', obs) # from Wjets CR
            except: pass
        if 'nW1p_nB2' in obs:
            try: model.add_lognormal_uncertainty('WJets_rate', math.log(1.036), 'WJets', obs) # from Wjets CR
            except: pass
        if 'nW1p_nB3p' in obs:
            try: model.add_lognormal_uncertainty('WJets_rate',math.log(1.036), 'WJets', obs) # from Wjets CR
            except: pass

    # Higgs tag eff difference between 74X and 76X, anti-correlated to b efficiency scale factor
    try: model.add_lognormal_uncertainty("btag_bc",math.log(0.97), '*', '*')
    except RuntimeError: pass

    return model

def get1H_model():
    print 'getting 1H model from',input1H
    model = build_model_from_rootfile(input1H,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('sfmu')==0 and s.count('sfel')==0))
    
    model.fill_histogram_zerobins()
    model.set_signal_processes('TpTp_M*')
    
    procs = model.processes
    obsvs = model.observables.keys()

    # Luminosity
    try: model.add_lognormal_uncertainty('luminosity', math.log(1.027), '*', '*')
    except RuntimeError: pass

    # ID, trigger scale factor uncertainties
    for obs in obsvs:
        print obs
        if 'El45' in obs:
            try: model.add_lognormal_uncertainty('sfel_trg', math.log(1.02), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfel_id', math.log(1.02), '*', obs)
            except RuntimeError: pass
        if 'Mu45' in obs:
            try: model.add_lognormal_uncertainty('sfmu_trg', math.log(1.01), '*', obs)
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('sfmu_id', math.log(1.02), '*', obs)
            except RuntimeError: pass            

    # Rate uncertainties
    try: model.add_lognormal_uncertainty('TTbar_rate',  math.log(1.087), 'TTbar', '*')
    except RuntimeError: pass
    try: model.add_lognormal_uncertainty('WJets_rate',  math.log(1.06), 'WJets', '*')
    except RuntimeError: pass
    try: model.add_lognormal_uncertainty('QCD_rate',  math.log(2.00), 'QCD', '*')
    except RuntimeError: pass
    try: model.add_lognormal_uncertainty('SingleTop_rate',  math.log(1.16), 'SingleTop', '*')
    except RuntimeError: pass
    try: model.add_lognormal_uncertainty('Diboson_rate',  math.log(1.15), 'Diboson', '*')
    except RuntimeError: pass

    # Higgs tag eff difference between 74X and 76X, correlated to b efficiency scale factor
    try: model.add_lognormal_uncertainty("btag_bc", math.log(1.03), '*', '*')
    except RuntimeError: pass

    # Higgs tag eff difference between pythia8 and herwig
    try: model.add_lognormal_uncertainty("higgs_py2hw", math.log(1.05), '*', '*')
    except RuntimeError: pass

    return model

##################################################################################################################

Model0H = get0H_model()

#Model1H = get1H_model()
#Model0H.combine(Model1H)

model_summary(Model0H)

#Bayesian Limits
plot_exp, plot_obs = bayesian_limits(Model0H,'all', n_toy = 5000, n_data = 500)
plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
plot_obs.write_txt('limits_'+rFileName+'_observed.txt')

report.write_html('htmlout_'+rFileName)
