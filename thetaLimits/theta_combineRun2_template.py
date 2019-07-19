import os,sys
from operator import itemgetter,attrgetter

input1L2016 = 'FILE'

input1L2017 = 'FILE'

input1L2018 = 'FILE'

input2L2016 = 'FILE'

input2L2017 = 'FILE'

input2L2018 = 'FILE'

input3L2016 = 'FILE'

input3L2017 = 'FILE'

input3L2018 = 'FILE'

#
rFileName = input1L2017.split('/')[-1][:-5]
                                                                          
def get_model1L2017():
    model = build_model_from_rootfile(input1L2017,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('Best')==0))

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

    return model

def get_model1L2018():
    model = build_model_from_rootfile(input1L2018,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('Best')==0))

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

    return model

def get_model3L():
    model = build_model_from_rootfile(input3L,include_mc_uncertainties=True,histogram_filter = (lambda s: s.count('muR__')==0 and s.count('muF__')==0 and s.count('muRFcorrd__')==0 and s.count('elelelTrigSys')==0 and s.count('elelmuTrigSys')==0 and s.count('elmumuTrigSys')==0 and s.count('mumumuTrigSys')==0 and s.count('elIsoSys')==0 and s.count('elIdSys')==0 and s.count('muIsoSys')==0 and s.count('muIdSys')==0 and s.count('PR__')==0))

    #
    model.fill_histogram_zerobins()
    model.set_signal_processes('sig')
    
    procs = model.processes
    obsvs = model.observables.keys()

    for proc in procs:
        if(proc != 'ddbkg'):
            try: model.add_lognormal_uncertainty('elIdSys', math.log(1.06), proc, 'triLepEEE')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elIdSys', math.log(1.04), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elIdSys', math.log(1.02), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elIsoSys', math.log(1.03), proc, 'triLepEEE')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elIsoSys', math.log(1.02), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elRecoSys', math.log(1.03), proc, 'triLepEEE')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elRecoSys', math.log(1.02), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('elRecoSys', math.log(1.01), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIdSys', math.log(1.02), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIdSys', math.log(1.04), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIdSys', math.log(1.06), proc, 'triLepMMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIsoSys', math.log(1.01), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIsoSys', math.log(1.02), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muIsoSys', math.log(1.03), proc, 'triLepMMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muRecoSys', math.log(1.01), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muRecoSys', math.log(1.02), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('muRecoSys', math.log(1.03), proc, 'triLepMMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('eeeTrigSys', math.log(1.03), proc, 'triLepEEE')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('eemTrigSys', math.log(1.03), proc, 'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('emmTrigSys', math.log(1.03), proc, 'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('mmmTrigSys', math.log(1.03), proc, 'triLepMMM')
            except RuntimeError: pass

            try: model.add_lognormal_uncertainty('lumiSys', math.log(1.025), proc, '*')
            except RuntimeError: pass

        else:
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.20),proc,'triLepMMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.18),proc,'triLepEMM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.38),proc,'triLepEEM')
            except RuntimeError: pass
            try: model.add_lognormal_uncertainty('FRsys',math.log(1.45),proc,'triLepEEE')
            except RuntimeError: pass

    #model.scale_predictions(120./35.9)
    return model

def get_model2L():
    model = build_model_from_rootfile(input2L,include_mc_uncertainties=True)

    model.set_signal_processes('sig')
    
    procs = model.processes
    print procs
    obsvs = model.observables.keys()
    
    for proc in procs:
        
        #data driven
        if(proc=="FakeRate"): model.add_lognormal_uncertainty("FakeRate",math.log(1.50),proc)
        elif(proc=="ChargeMisID"): model.add_lognormal_uncertainty("ChargeMisIDUnc",math.log(1.30),proc)

        #MC
        else:
            model.add_lognormal_uncertainty('lumiSys',math.log(1.025),proc)
            model.add_lognormal_uncertainty('eeTrigSysBD',math.log(1.03),proc,'elelBD')
            model.add_lognormal_uncertainty('emTrigSysBD',math.log(1.03),proc,'elmuBD')
            model.add_lognormal_uncertainty('mmTrigSysBD',math.log(1.03),proc,'mumuBD')
            model.add_lognormal_uncertainty('eeTrigSysEH',math.log(1.03),proc,'elelEH')
            model.add_lognormal_uncertainty('emTrigSysEH',math.log(1.03),proc,'elmuEH')
            model.add_lognormal_uncertainty('mmTrigSysEH',math.log(1.03),proc,'mumuEH')
            
            for obs in obsvs:
                if 'elel' in obs: model.add_lognormal_uncertainty('elIdSys',math.log(1.02),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('elIdSys',math.log(1.01),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('muIdSys',math.log(1.03),proc,obs)
                if 'mumu' in obs: model.add_lognormal_uncertainty('muIdSys',math.log(1.06),proc,obs)
                if 'elel' in obs: model.add_lognormal_uncertainty('elIsoSys',math.log(1.02),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('elIsoSys',math.log(1.01),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('muIsoSys',math.log(1.01),proc,obs)
                if 'mumu' in obs: model.add_lognormal_uncertainty('muIsoSys',math.log(1.02),proc,obs)
                if 'elel' in obs: model.add_lognormal_uncertainty('elRecoSys',math.log(1.02),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('elRecoSys',math.log(1.01),proc,obs)
                if 'elmu' in obs: model.add_lognormal_uncertainty('muRecoSys',math.log(1.01),proc,obs)
                if 'mumu' in obs: model.add_lognormal_uncertainty('muRecoSys',math.log(1.02),proc,obs)

            if(proc != 'sig'):
                if(proc=='TTZ'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(TTZPUDOWN),math.log(TTZPUUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(TTZPDFDOWN),math.log(TTZPDFUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewTop',math.log(TTZSCALEDOWN),math.log(TTZSCALEUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(TTZJECDOWN),math.log(TTZJECUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(TTZJERDOWN),math.log(TTZJERUP),proc)
                elif(proc=='TTW'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(TTWPUDOWN),math.log(TTWPUUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(TTWPDFDOWN),math.log(TTWPDFUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewTop',math.log(TTWSCALEDOWN),math.log(TTWSCALEUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(TTWJECDOWN),math.log(TTWJECUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(TTWJERDOWN),math.log(TTWJERUP),proc)
                elif(proc=='TTH'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(TTHPUDOWN),math.log(TTHPUUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(TTHPDFDOWN),math.log(TTHPDFUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewTop',math.log(TTHSCALEDOWN),math.log(TTHSCALEUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(TTHJECDOWN),math.log(TTHJECUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(TTHJERDOWN),math.log(TTHJERUP),proc)
                elif(proc=='TTTT'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(TTTTPUDOWN),math.log(TTTTPUUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(TTTTPDFDOWN),math.log(TTTTPDFUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewTop',math.log(TTTTSCALEDOWN),math.log(TTTTSCALEUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(TTTTJECDOWN),math.log(TTTTJECUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(TTTTJERDOWN),math.log(TTTTJERUP),proc)
                elif(proc=='WZ'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(WZPUDOWN),math.log(WZPUUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(WZPDFDOWN),math.log(WZPDFUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewEwk',math.log(WZSCALEDOWN),math.log(WZSCALEUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(WZJECDOWN),math.log(WZJECUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(WZJERDOWN),math.log(WZJERUP),proc)
                elif(proc=='ZZ'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(ZZPUDOWN),math.log(ZZPUUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(ZZPDFDOWN),math.log(ZZPDFUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewEwk',math.log(ZZSCALEDOWN),math.log(ZZSCALEUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(ZZJECDOWN),math.log(ZZJECUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(ZZJERDOWN),math.log(ZZJERUP),proc)
                elif(proc=='WpWp'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(WpWpPUDOWN),math.log(WpWpPUUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(WpWpPDFDOWN),math.log(WpWpPDFUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewEwk',math.log(WpWpSCALEDOWN),math.log(WpWpSCALEUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(WpWpJECDOWN),math.log(WpWpJECUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(WpWpJERDOWN),math.log(WpWpJERUP),proc)
                elif(proc=='WWZ'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(WWZPUDOWN),math.log(WWZPUUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(WWZPDFDOWN),math.log(WWZPDFUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewEwk',math.log(WWZSCALEDOWN),math.log(WWZSCALEUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(WWZJECDOWN),math.log(WWZJECUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(WWZJERDOWN),math.log(WWZJERUP),proc)
                elif(proc=='WZZ'):
                    model.add_asymmetric_lognormal_uncertainty('pileup',math.log(WZZPUDOWN),math.log(WZZPUUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(WZZPDFDOWN),math.log(WZZPDFUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewEwk',math.log(WZZSCALEDOWN),math.log(WZZSCALEUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jec',math.log(WZZJECDOWN),math.log(WZZJECUP),proc)
                    model.add_asymmetric_lognormal_uncertainty('jer',math.log(WZZJERDOWN),math.log(WZZJERUP),proc)
                else: print 'UNKNOWN PROC'

            else:     #   signal
                model.add_asymmetric_lognormal_uncertainty('pdfNew',math.log(SIGPDFDOWN),math.log(SIGPDFUP),proc)
                model.add_asymmetric_lognormal_uncertainty('muRFcorrdNewSig',math.log(SIGSCALEDOWN),math.log(SIGSCALEUP),proc)
                model.add_asymmetric_lognormal_uncertainty('jer',math.log(SIGJERDOWN),math.log(SIGJERUP),proc) 
                model.add_asymmetric_lognormal_uncertainty('jec',math.log(SIGJECDOWN),math.log(SIGJECUP),proc) 
                model.add_lognormal_uncertainty('pileup',math.log(1.01),proc) 
    
    #model.scale_predictions(120./35.9)
    return model

##################################################################################################################

model1L2017 = get_model1L2017()
model1L2018 = get_model1L2018()
model1L2017.combine(model1L2018)

## for later when combining with other leptonic final states
#model2L = get_model2L()
#model3L = get_model3L()
#model1L.combine(model2L)
#model1L.combine(model3L)

model_summary(model1L2017)

plot_exp, plot_obs = bayesian_limits(model1L2017,'all', n_toy = 3000, n_data = 300)

plot_exp.write_txt('limits_'+rFileName+'_expected.txt')
#plot_obs.write_txt('limits_'+rFileName+'_observed.txt')

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
