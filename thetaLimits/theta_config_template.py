import os,sys
from operator import itemgetter,attrgetter

input = 'FILE'

rFileName = input.split('/')[-1][:-5]
                                                                          
def get_model():
    model = build_model_from_rootfile(input,include_mc_uncertainties=True)
    model.fill_histogram_zerobins()
    model.set_signal_processes('sig')
    
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

model = get_model()

##################################################################################################################

model_summary(model)

plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 5000, n_data = 500)

plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
plot_obs.write_txt('limits_'+rFileName+'_observed.txt')

report.write_html('htmlout_'+rFileName)
