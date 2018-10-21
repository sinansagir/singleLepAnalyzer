
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
    model.add_lognormal_uncertainty('topSys', math.log(1.50), 'top', '*')
    model.add_lognormal_uncertainty('ewkSys', math.log(1.50), 'ewk', '*')
    model.add_lognormal_uncertainty('qcdSys', math.log(1.50), 'qcd', '*')
    model.add_lognormal_uncertainty('sigSys', math.log(1.10), 'sig', '*')

    return model

model = get_model()

##################################################################################################################

xsec = {}
xsec['X53X53M700left']   = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M700right']  = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M800left']   = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M800right']  = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M900left']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M900right']  = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1000left']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1000right'] = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1100left']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1100right'] = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1200left']  = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1200right'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1300left']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1300right'] = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1400left']  = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1400right'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1500left']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1500right'] = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1600left']  = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53X53M1600right'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xs=xsec[rFileName.split('_')[2]]
print "xsec =",xs

signal_process_groups = {'sig': ['sig']}
import json
f = open(rFileName+'.json', 'w')
disc = discovery(model,use_data = False,input_expected='toys:%f' % xs,spid='sig',Z_error_max=0.1,ts_method=derll)
#disc = discovery(model, spid = 'sig', use_data = False, input_expected = 'toys:%f' % xs, maxit = 2, n = 1000000)
print disc
json.dump(disc, f)
