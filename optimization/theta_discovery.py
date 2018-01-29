import os,sys
from operator import itemgetter,attrgetter

input = 'FILE'

rFileName = input.split('/')[-1][:-5]
                                                                          
def get_model():
    model = build_model_from_rootfile(input,include_mc_uncertainties=True)

    #
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
            try: model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), '*', obs)
            except: pass
        elif 'isM' in obs:
            try: model.add_lognormal_uncertainty('muIdSys', math.log(1.03), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('muTrigSys', math.log(1.05), '*', obs)
            except: pass
            try: model.add_lognormal_uncertainty('muIsoSys', math.log(1.01), '*', obs)
            except: pass

        if 'H1b' in obs or 'H2b' in obs:
            try: model.add_lognormal_uncertainty('htag_prop',math.log(1.05), '*', obs)
            except: pass
        else:
            try: model.add_lognormal_uncertainty('htag_prop',math.log(0.95), '*', obs)
            except: pass


    try: model.add_lognormal_uncertainty('lumiSys', math.log(1.026), '*', '*')
    except: pass

    # flat values for tests
    try: model.add_lognormal_uncertainty('btag', math.log(1.05), '*', '*')
    except: pass
    try: model.add_lognormal_uncertainty('jec', math.log(1.05), '*', '*')
    except: pass
    try: model.add_lognormal_uncertainty('taupt', math.log(1.05), 'sig', '*')
    except: pass

    return model

##################################################################################################################

model = get_model()
model_summary(model)

sigmass = rFileName.split('_')[2]
xsec = {}
xsec['TTM800']  = 0.196 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM900']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1000']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1100']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1300']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1500']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1700']  = 0.000666 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['TTM1800'] = 0.000391 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo

xs=xsec[rFileName.split('_')[2]]
print "xsec =",xs

signal_process_groups = {'sig': ['sig']}
import json
f = open(rFileName+'.json', 'w')
disc = discovery(model,use_data = False,input_expected='toys:%f' % xs,spid='sig',Z_error_max=0.2,ts_method=derll)
#disc = discovery(model, spid = 'sig', use_data = False, input_expected = 'toys:%f' % xs, maxit = 2, n = 1000000)
print disc
json.dump(disc, f)
