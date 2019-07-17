import os,sys
from operator import itemgetter,attrgetter

input = 'FILE'

rFileName = input.split('/')[-1][:-5]+'_DeepAK8'
                                                                          
def get_model():
    model = build_model_from_rootfile(input,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('Best')==0))

    #
    model.fill_histogram_zerobins()
    model.set_signal_processes('sig')
    ##model.scale_predictions((41298.+35867.)/36814.)
    
    procs = model.processes
    obsvs = model.observables.keys()

    for obs in obsvs:
        if 'isE' in obs:
            try: model.add_lognormal_uncertainty('elIdSys', math.log(1.02), '*', obs) #(uncert name, magnitude, which process to apply to, which channel/observable)
            except: pass
            try: model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), '*', obs) #iso + reco
            except: pass
            try: model.add_lognormal_uncertainty('elTrigSys', math.log(1.05), '*', obs) #iso + reco
            except: pass
            try: model.add_lognormal_uncertainty('elRecoSys', math.log(1.01), '*', obs) #iso + reco
            except: pass
        elif 'isM' in obs:
            try: model.add_lognormal_uncertainty('muIdSys', math.log(1.02), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('muIsoSys', math.log(1.01), '*', obs) #iso + tracking
            except: pass
            try: model.add_lognormal_uncertainty('muTrigSys', math.log(1.05), '*', obs) #iso + tracking
            except: pass
            try: model.add_lognormal_uncertainty('muRecoSys', math.log(1.01), '*', obs) #iso + tracking
            except: pass

    try: model.add_lognormal_uncertainty('lumiSys', math.log(1.023), '*', '*')
    except: pass

    # flat values for tests
    #try: model.add_lognormal_uncertainty('QCDscale', math.log(1.25),'qcd','*')
    #except RuntimeError: pass
    #try: model.add_lognormal_uncertainty('TTbarscale', math.log(1.30),'top','*')
    #except RuntimeError: pass
    #try: model.add_lognormal_uncertainty('EWKscale', math.log(1.25),'ewk','*')
    #except RuntimeError: pass
    # try: model.add_lognormal_uncertainty('jsf', math.log(1.038), 'WJets', '*')
    # except: pass
    # try: model.add_lognormal_uncertainty('muRFcorrdNewDYJets', math.log(1.15), 'DYJets', '*')
    # except: pass
    # try: model.add_lognormal_uncertainty('muRFcorrdNewEwk', math.log(1.15), 'ewk', '*')
    # except: pass
    # try: model.add_lognormal_uncertainty('muRFcorrdNewSingleTop', math.log(1.16), 'SingleTop', '*')
    # except: pass

    return model

model = get_model()

##################################################################################################################

model_summary(model)

plot_exp, plot_obs = bayesian_limits(model,'all', n_toy = 3000, n_data = 300)

plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
##plot_obs.write_txt('limits_'+rFileName+'_observed.txt')

report.write_html('htmlout_'+rFileName)

# sigmass = rFileName.split('_')[2]
# xsec = {}
# xsec['TTM800']  = 0.196 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM900']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM1000']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM1100']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM1300']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM1500']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM1700']  = 0.000666 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# xsec['TTM1800'] = 0.000391 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
# if '800' in sigmass or '900' in sigmass or '1000' in sigmass or '1100' in sigmass or '1200' in sigmass:
#     xs=xsec[rFileName.split('_')[2]]
#     print "xsec =",xs

#     signal_process_groups = {'sig': ['sig']}
#     import json
#     f = open(rFileName+'.json', 'w')
#     disc = discovery(model,use_data = False,input_expected='toys:%f' % xs,spid='sig',Z_error_max=0.1,ts_method=derll)
# #disc = discovery(model, spid = 'sig', use_data = False, input_expected = 'toys:%f' % xs, maxit = 2, n = 1000000)
#     print disc
#     json.dump(disc, f)
