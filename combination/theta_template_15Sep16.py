

def getLJetsModel():
    model = build_model_from_rootfile('LJETSFILE',include_mc_uncertainties=True,histogram_filter = (lambda s:  s.count('__pdf__')==0 and s.count('__muRFdecorrdNew__')==0 and s.count('__muRFenv__')==0 and s.count('__muR__')==0 and s.count('__muF__')==0 and s.count('__muRFcorrd__')==0 and s.count('__jsf__')==0 and s.count('nB0')==0))

    model.fill_histogram_zerobins()
    model.set_signal_processes('sig')

    procs = model.processes
    obsvs = model.observables.keys()

    for obs in obsvs:
		if 'isE' in obs:
			model.add_lognormal_uncertainty('elTrigSys', math.log(1.05), '*', obs)
			model.add_lognormal_uncertainty('elIdSys', math.log(1.01), '*', obs)
			model.add_lognormal_uncertainty('elIsoSys', math.log(1.01), '*', obs)
		elif 'isM' in obs:
			model.add_lognormal_uncertainty('muTrigSys', math.log(1.05), '*', obs)
			model.add_lognormal_uncertainty('muIdSys', math.log(1.01), '*', obs)
			model.add_lognormal_uncertainty('muIsoSys', math.log(1.01), '*', obs)
    model.add_lognormal_uncertainty('lumiSys', math.log(1.027), '*', '*')

    #modeling uncertainties: Inclusive WJets sample, NOT REWEIGHTED, 8SEP16--SS
    for obs in obsvs:
		if 'nT0_nW0_nB1' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top0T0W1BSys',  math.log(1.11), 'top', obs) # from ttbar CR
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk0T0W1BSys',  math.log(1.12), 'ewk', obs) # from Wjets CR
		if 'nT0_nW0_nB2p' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top0T0W2pBSys', math.log(1.15), 'top', obs) # from ttbar CR
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk0T0W2pBSys', math.log(1.12), 'ewk', obs) # from Wjets CR
		if 'nT0_nW1p_nB1' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top0T1pW1BSys', math.log(1.11), 'top', obs) # from ttbar CR
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk0T1pW1BSys', math.log(1.12), 'ewk', obs) # from Wjets CR
		if 'nT0_nW1p_nB2p' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top0T1pW2pBSys',math.log(1.15), 'top', obs) # from ttbar CR
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk0T1pW2pBSys',math.log(1.12), 'ewk', obs) # from Wjets CR
		if 'nT1p_nW0_nB1' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top1pT0W1BSys', math.log(1.11), 'top', obs) # from ttbar CR
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk1pT0W1BSys', math.log(1.12), 'ewk', obs) # from Wjets CR
		if 'nT1p_nW0_nB2p' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top1pT0W2pBSys',math.log(1.15), 'top', obs) # from ttbar CR
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk1pT0W2pBSys',math.log(1.12), 'ewk', obs) # from Wjets CR
		if 'nT1p_nW1p_nB1' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top1pT1pW1BSys',math.log(1.11), 'top', obs) # from ttbar CR
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk1pT1pW1BSys',math.log(1.12), 'ewk', obs) # from Wjets CR
		if 'nT1p_nW1p_nB2p' in obs:
			if 'top' in obs: model.add_lognormal_uncertainty('top1pT1pW2pBSys',math.log(1.15),'top', obs) # from ttbar CR
			if 'ewk' in obs: model.add_lognormal_uncertainty('ewk1pT1pW2pBSys',math.log(1.12),'ewk', obs) # from Wjets CR

    return model



def getSSDLModel():
    model = build_model_from_rootfile('SSDLROOTFILE',include_mc_uncertainties=True)


    model.set_signal_processes('sig')
    
    procs = model.processes
    
    
    for proc in procs:
        
    #data driven
        if(proc=="NonPrompt"):
            model.add_lognormal_uncertainty("FakeRate",math.log(1.50),proc)
        elif(proc=="ChargeMisID"):
            model.add_lognormal_uncertainty("ChargeMisIDUnc",math.log(1.30),proc)
    #background MC
        elif(proc!="NonPrompt" and proc!='ChargeMisID' and proc!='sig'):
        #Common
            model.add_lognormal_uncertainty('pileup',math.log(1.06),proc)
            model.add_lognormal_uncertainty('lumiSys',math.log(1.027),proc)
        #lepton ID
            model.add_lognormal_uncertainty('elIdSys',math.log(1.02),proc,'elel')
            model.add_lognormal_uncertainty('elIdSys',math.log(1.01),proc,'elmu')
            model.add_lognormal_uncertainty('muIdSys',math.log(1.01),proc,'elmu')
            model.add_lognormal_uncertainty('muIdSys',math.log(1.02),proc,'mumu')
        #lepton ISO
            model.add_lognormal_uncertainty('elIsoSys',math.log(1.02),proc,'elel')
            model.add_lognormal_uncertainty('elIsoSys',math.log(1.01),proc,'elmu')
            model.add_lognormal_uncertainty('muIsoSys',math.log(1.01),proc,'elmu')
            model.add_lognormal_uncertainty('muIsoSys',math.log(1.02),proc,'mumu')
        #lepton Trig
            model.add_lognormal_uncertainty('LepTrig_elel',math.log(1.03),proc,'elel')
            model.add_lognormal_uncertainty('LepTrig_elmu',math.log(1.03),proc,'elmu')
            model.add_lognormal_uncertainty('LepTrig_mumu',math.log(1.03),proc,'mumu')
            
        #individual
            if(proc=='TTZ'):
                model.add_lognormal_uncertainty('MC',math.log(1.11),proc)
                model.add_lognormal_uncertainty('jec',math.log(1.03),proc)
                model.add_lognormal_uncertainty('jer',math.log(1.02),proc)
            if(proc=='TTW'):
                model.add_lognormal_uncertainty('MC',math.log(1.18),proc)
                model.add_lognormal_uncertainty('jec',math.log(1.04),proc)
                model.add_lognormal_uncertainty('jer',math.log(1.02),proc)
            if(proc=='TTH'):
                model.add_lognormal_uncertainty('MC',math.log(1.12),proc)
                model.add_lognormal_uncertainty('jec',math.log(1.04),proc)
                model.add_lognormal_uncertainty('jer',math.log(1.02),proc)
            if(proc=='TTTT'):
                model.add_lognormal_uncertainty('MC',math.log(1.50),proc)
                model.add_lognormal_uncertainty('jec',math.log(1.02),proc)
                model.add_lognormal_uncertainty('jer',math.log(1.02),proc)
            if(proc=='WZ'):
                model.add_lognormal_uncertainty('MC',math.log(1.12),proc)
                model.add_lognormal_uncertainty('jec',math.log(1.10),proc)
                model.add_lognormal_uncertainty('jer',math.log(1.02),proc)
            if(proc=='ZZ'):
                model.add_lognormal_uncertainty('MC',math.log(1.12),proc)
                model.add_lognormal_uncertainty('jec',math.log(1.07),proc)
                model.add_lognormal_uncertainty('jer',math.log(1.02),proc)
            if(proc=='WpWp'):
                model.add_lognormal_uncertainty('MC',math.log(1.50),proc)
                model.add_lognormal_uncertainty('jec',math.log(1.06),proc)
                model.add_lognormal_uncertainty('jer',math.log(1.02),proc)
            if(proc=='WWZ'):
                model.add_lognormal_uncertainty('MC',math.log(1.50),proc)
                model.add_lognormal_uncertainty('jec',math.log(1.07),proc)
                model.add_lognormal_uncertainty('jer',math.log(1.02),proc)
            if(proc=='WZZ'):
                model.add_lognormal_uncertainty('MC',math.log(1.50),proc)
                model.add_lognormal_uncertainty('jec',math.log(1.09),proc)
                model.add_lognormal_uncertainty('jer',math.log(1.02),proc)
            if(proc=='ZZZ'):
                model.add_lognormal_uncertainty('MC',math.log(1.50),proc)
                model.add_lognormal_uncertainty('jec',math.log(1.09),proc)
                model.add_lognormal_uncertainty('jer',math.log(1.02),proc)

    #   signal
        else:
            model.add_lognormal_uncertainty('jer',math.log(1.03),proc)
            model.add_lognormal_uncertainty('jec',math.log(1.05),proc)
            model.add_lognormal_uncertainty('pileup',math.log(1.01),proc)
            model.add_lognormal_uncertainty('lumiSys',math.log(1.027),proc)                                        
        #lepton ID
            model.add_lognormal_uncertainty('elIdSys',math.log(1.02),proc,'elel')
            model.add_lognormal_uncertainty('elIdSys',math.log(1.01),proc,'elmu')
            model.add_lognormal_uncertainty('muIdSys',math.log(1.01),proc,'elmu')
            model.add_lognormal_uncertainty('muIdSys',math.log(1.02),proc,'mumu')
        #lepton ISO
            model.add_lognormal_uncertainty('elIsoSys',math.log(1.02),proc,'elel')
            model.add_lognormal_uncertainty('elIsoSys',math.log(1.01),proc,'elmu')
            model.add_lognormal_uncertainty('muIsoSys',math.log(1.01),proc,'elmu')
            model.add_lognormal_uncertainty('muIsoSys',math.log(1.02),proc,'mumu')
        #lepton Trig
            model.add_lognormal_uncertainty('LepTrig_elel',math.log(1.03),proc,'elel')
            model.add_lognormal_uncertainty('LepTrig_elmu',math.log(1.03),proc,'elmu')
            model.add_lognormal_uncertainty('LepTrig_mumu',math.log(1.03),proc,'mumu')


    return model

ssdlModel = getSSDLModel()
ljetsModel = getLJetsModel()

ssdlModel.combine(ljetsModel)
                                        
model_summary(ssdlModel)

#Bayesian Limits
plot_exp, plot_obs = bayesian_limits(ssdlModel,'all', n_toy = 100000, n_data = 1000)
#plot_exp, plot_obs = bayesian_limits(ssdlModel,'all', n_toy = 5000, n_data = 500)

plot_exp.write_txt('EXPTXTFILE')
plot_obs.write_txt('OBSTXTFILE')

#signal_process_groups = {'sig': ['sig']}
#import json
#f = open('JSONNAME_discovery.json', 'w')
#disc = discovery(ssdlModel,use_data = False,input_expected='toys:XSEC',spid='sig',Z_error_max=0.1,ts_method=derll)
#print disc
#json.dump(disc, f)

#print "Asymptotic Limits:"
#print asymptotic_cls_limits(ssdlModel, signal_processes=[['sig']], beta_signal_expected=0.0, bootstrap_ssdlModel=True, input=None, n=1, options=None)

report.write_html('HTMLOUT')

