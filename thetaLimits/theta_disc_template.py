#!/usr/bin/python

import json

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

## tttt x-sec values:
## 8.213 fb found on DAS: https://cms-gen-dev.cern.ch/xsdb/?searchQuery=DAS=TTTT_TuneCP5_13TeV-amcatnlo-pythia8
## 9.2 fb found on TOP-17-019 CMS paper
## 11.12 fb for LO_QCD + NLO_QCD and 11.97 fb for LO + NLO found on https://arxiv.org/pdf/1711.02116.pdf [Table 6]
xs=0.0092 
print "xsec =",xs

signal_process_groups = {'sig': ['sig']}
fjson = open(rFileName+'.json', 'w')
#defaults: theta_auto.discovery(model, spid=None, use_data=True, Z_error_max=0.05, maxit=100, n=10000, input_expected='toys:1.0', n_expected=1000, nuisance_constraint=None, nuisance_prior_toys_bkg=None, options=None, verbose=True, ts_method=<function deltanll at 0x46355f0>)
disc = discovery(model,use_data = False,input_expected='toys:%f' % xs,spid='sig',Z_error_max=0.1,ts_method=derll)
#disc = discovery(model,use_data = False,n=250000,input_expected='toys:%f' % xs,spid='sig',ts_method=derll)#,maxit=2, n=1000000)
json.dump(disc, fjson)
print disc
