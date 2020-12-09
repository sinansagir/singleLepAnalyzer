#!/usr/bin/python

targetlumi2016 = 35867.
targetlumi     = 41530. # 1/pb
targetlumi2018 = 59690.

genHTweight={}
genHTweight['WJetsMG100'] = 0.998056#https://github.com/jmhogan/GenHTweight/blob/master/WJetsToLNuSFs.txt
genHTweight['WJetsMG200'] = 0.978569
genHTweight['WJetsMG400'] = 0.928054
genHTweight['WJetsMG600'] = 0.856705
genHTweight['WJetsMG800'] = 0.757463
genHTweight['WJetsMG1200']= 0.608292
genHTweight['WJetsMG2500']= 0.454246

genHTweight['DYMG100'] = 1.007516#https://github.com/jmhogan/GenHTweight/blob/master/DYJetsToLLSFs.txt
genHTweight['DYMG200'] = 0.992853
genHTweight['DYMG400'] = 0.974071
genHTweight['DYMG600'] = 0.948367
genHTweight['DYMG800'] = 0.883340
genHTweight['DYMG1200']= 0.749894
genHTweight['DYMG2500']= 0.617254

BR={}
BR['BW'] = 0.5
BR['TZ'] = 0.25
BR['TH'] = 0.25
BR['TTBWBW'] = BR['BW']*BR['BW']
BR['TTTHBW'] = 2*BR['TH']*BR['BW']
BR['TTTZBW'] = 2*BR['TZ']*BR['BW']
BR['TTTZTZ'] = BR['TZ']*BR['TZ']
BR['TTTZTH'] = 2*BR['TZ']*BR['TH']
BR['TTTHTH'] = BR['TH']*BR['TH']

BR['TW'] = 0.5
BR['BZ'] = 0.25
BR['BH'] = 0.25
BR['BBTWTW'] = BR['TW']*BR['TW']
BR['BBBHTW'] = 2*BR['BH']*BR['TW']
BR['BBBZTW'] = 2*BR['BZ']*BR['TW']
BR['BBBZBZ'] = BR['BZ']*BR['BZ']
BR['BBBZBH'] = 2*BR['BZ']*BR['BH']
BR['BBBHBH'] = BR['BH']*BR['BH']

# Number of processed MC events (before selections)
nRun={}
# new counts for 2017

nrunttJets2L2Nu = 68448328.0 # :from integral 69007316.0, file TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root
nruntthad = 129092906.0 # :from integral 130143186.0, file TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root
nrunttJetsSemiLep =  109124472.0 # :from integral 110014744.0, file TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_1_hadd.root
nruntt1000 = 19417657.0 # from integral 20471915.0, file TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8_1_hadd.root
nruntt700 = 38407913.0 # from integral 39143691.0, file TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8_1_hadd.root

nRun['TTJetsHad0'] = nruntthad*0.8832   # hadronic*BR(0-700)
nRun['TTJetsHad700'] = nruntthad*0.0921 + nruntt700*0.457 #hadronic*BR(700-1000) + mass700*BR(hadronic)
nRun['TTJetsHad1000'] = nruntthad*0.02474 + nruntt1000*0.457 #hadronic*BR(1000+) + mass1000*BR(hadronic
nRun['TTJetsSemiLep0'] = nrunttJetsSemiLep*0.8832  # semilept*BR(0-700)
nRun['TTJetsSemiLep700'] = nrunttJetsSemiLep*0.0921 + nruntt700*0.438 #semilept*BR(700-1000) + mass700*BR(semilept)
nRun['TTJetsSemiLep1000'] = nrunttJetsSemiLep*0.02474 + nruntt1000*0.438 #semilept*BR(1000+) + mass1000*BR(semilept)
nRun['TTJets2L2nu0'] = nrunttJets2L2Nu*0.8832  #dilepton*BR(0-700)
nRun['TTJets2L2nu700'] = nrunttJets2L2Nu*0.0921 + nruntt700*0.105 #dilepton*BR(700-1000) + mass700*BR(dilepton)
nRun['TTJets2L2nu1000'] = nrunttJets2L2Nu*0.02474 + nruntt1000*0.105 #dilepton*BR(1000+) + mass1000*BR(dilepton)
nRun['TTJetsPH700mtt'] = nruntt700 + nruntthad*0.0921 + nrunttJetsSemiLep*0.0921 + nrunttJets2L2Nu*0.0921 #mass700 + inclusive*BR(700)
nRun['TTJetsPH1000mtt'] = nruntt1000 + nruntthad*0.02474 + nrunttJetsSemiLep*0.02474 + nrunttJets2L2Nu*0.02474 #mass1000 + inclusive*BR(1000)
nRun['Ts'] = 6895750.0 # :from integral 6898000.0, file ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia_hadd.root
nRun['Tbs'] = 2952214.0 # :from integral 2953000.0, file ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia_hadd.root
nRun['Tt'] = 122688200.0 # :from integral 122688200.0, file ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_1_hadd.root
nRun['Tbt']= 64818800.0 # :from integral 64818800.0, file ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_1_hadd.root
nRun['TtW'] = 7884388.0 # from integral 7945242.0, file ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_1_hadd.root
nRun['TbtW'] = 7686032.0 # :from integral 7745276.0, file ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_1_hadd.root
nRun['WJets'] = 6776900. # from 9908534.
nRun['WJetsMG'] = 86731806. 
nRun['WJetsMG100'] = 79356685.
nRun['WJetsMG200'] = 21192211.0 # from integral 21250517.0, file WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WJetsMG400'] = 14237953.0 # :from integral 14301047.0, file WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root
nRun['WJetsMG600'] = 21570948.0 # :from integral 21697666.0, file WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root
nRun['WJetsMG800'] = 20187318.0 # :from integral 20346454.0, file WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root
nRun['WJetsMG1200'] = 37350377.0 # from integral 37849011.0, file WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root
nRun['WJetsMG2500'] = 20469295.0 # from integral 21328621.0, file WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root
nRun['WJetsPt100'] = 120124110.*(1.-2.*0.32) #Full =120124110, neg frac 0.32
nRun['WJetsPt250'] = 12022587.*(1.-2.*0.31555) #Full = 12022587, neg frac 0.31555 
nRun['WJetsPt400'] = 1939947.*(1.-2.*0.30952) #Full = 1939947, neg frac 0.30952
nRun['WJetsPt600'] = 1974619.*(1.-2.*0.29876) #Full = 1974619, neg frac 0.29876
nRun['DY'] = 123584520. # from 182359896, this is the ext1 sample
nRun['DYMG'] = 49082157. # from integral 49125561.0, file DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG100'] = 10607207.
nRun['DYMG200'] = 10699051.0 # from integral 10728447.0, file DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG400'] = 10174800.0 # from integral 10219524.0, file DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG600'] = 8691608.0 # from integral 8743640.0, file DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG800'] = 3089712.0 # from integral 3114980.0, file DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG1200']= 616923.0 # from integral 625517.0, file DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG2500']= 401334.0 # from integral 419308.0, file DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WW'] = 7765828.0 # from integral 7765828.0, file WW_TuneCP5_13TeV-pythia8_hadd.root
nRun['WZ'] = 3928630.0 # from integral 3928630.0, file WZ_TuneCP5_13TeV-pythia8_hadd.root
nRun['ZZ'] = 1925931.0 # from integral 1925931.0, file ZZ_TuneCP5_13TeV-pythia8_hadd.root
nRun['QCDht100'] = 80684349.
nRun['QCDht200'] = 59007662.0 # from integral 59074480.0, file QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht300'] = 59459614.0 # :from integral 59569132.0, file QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht500'] = 56041018.0 # :from integral 56207744.0, file QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht700'] = 68392328.0 # from integral 68687810.0, file QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht1000'] = 16770762.0 # :from integral 16882838.0, file QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht1500'] = 11508604.0 # :from integral 11634434.0, file QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht2000'] = 5825566.0 # :from integral 5941306.0, file QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['TTW'] = 9384328. # from integral 9425384.0, file ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8_hadd.root
nRun['TTZ'] = 8519074. # from integral 8536618.0, file ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8_hadd.root
nRun['TTH'] = 9580578. # from integral 9783674.0, file ttH_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root
nRun['TTWl'] = 2686141.0 # :from integral 4908905.0, file TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8_hadd.root
nRun['TTZl'] = 5239484.0 # :from integral 11092000.0, file TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_1_hadd.root
nRun['TTHB'] = 7833734.0 # from integral 8000000.0, file ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_1_hadd.root
nRun['TTHnoB'] = 7814711.0 # from integral 7966779.0, file ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_1_hadd.root
nRun['TTWq'] = 441560.0 # from integral 811306.0, file TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_hadd.root


## TTPrime Effective integral from dumpCounts Nov2020, pdf4LHC integral from E.S. dumpMuPDF
nRunTTM1000 = 1002517.455 # from integral 842000.0, TprimeTprime_M-1000_TuneCP5_13TeV-madgraph-pythia8
nRunTTM1100 = 895042.045*742000.0/745000.0 # from integral 745000.0, TprimeTprime_M-1100_TuneCP5_13TeV-madgraph-pythia8
nRunTTM1200 = 1003441.777 # from integral 829000.0, TprimeTprime_M-1200_TuneCP5_13TeV-madgraph-pythia8
nRunTTM1300 = 1026082.979 # from integral 847000.0, TprimeTprime_M-1300_TuneCP5_13TeV-madgraph-pythia8
nRunTTM1400 = 979603.275 # from integral 811000.0, TprimeTprime_M-1400_TuneCP5_13TeV-madgraph-pythia8
nRunTTM1500 = 985756.619*821000.0/827000.0 # from integral 827000.0, TprimeTprime_M-1500_TuneCP5_13TeV-madgraph-pythia8
nRunTTM1600 = 989851.281*841000.0/850000.0 # from integral 850000.0, TprimeTprime_M-1600_TuneCP5_13TeV-madgraph-pythia8
nRunTTM1700 = 939135.751*830000.0/836000.0 # from integral 836000.0, TprimeTprime_M-1700_TuneCP5_13TeV-madgraph-pythia8
nRunTTM1800 = 884660.318 # from integral 827000.0, TprimeTprime_M-1800_TuneCP5_13TeV-madgraph-pythia8 
nRun['TTM1000BWBW'] = nRunTTM1000/9.0
nRun['TTM1100BWBW'] = nRunTTM1100/9.0
nRun['TTM1200BWBW'] = nRunTTM1200/9.0
nRun['TTM1300BWBW'] = nRunTTM1300/9.0
nRun['TTM1400BWBW'] = nRunTTM1400/9.0
nRun['TTM1500BWBW'] = nRunTTM1500/9.0
nRun['TTM1600BWBW'] = nRunTTM1600/9.0
nRun['TTM1700BWBW'] = nRunTTM1700/9.0
nRun['TTM1800BWBW'] = nRunTTM1800/9.0
nRun['TTM1000THBW'] = nRunTTM1000*2.0/9.0
nRun['TTM1100THBW'] = nRunTTM1100*2.0/9.0
nRun['TTM1200THBW'] = nRunTTM1200*2.0/9.0
nRun['TTM1300THBW'] = nRunTTM1300*2.0/9.0
nRun['TTM1400THBW'] = nRunTTM1400*2.0/9.0
nRun['TTM1500THBW'] = nRunTTM1500*2.0/9.0
nRun['TTM1600THBW'] = nRunTTM1600*2.0/9.0
nRun['TTM1700THBW'] = nRunTTM1700*2.0/9.0
nRun['TTM1800THBW'] = nRunTTM1800*2.0/9.0
nRun['TTM1000TZBW'] = nRunTTM1000*2.0/9.0
nRun['TTM1100TZBW'] = nRunTTM1100*2.0/9.0
nRun['TTM1200TZBW'] = nRunTTM1200*2.0/9.0
nRun['TTM1300TZBW'] = nRunTTM1300*2.0/9.0
nRun['TTM1400TZBW'] = nRunTTM1400*2.0/9.0
nRun['TTM1500TZBW'] = nRunTTM1500*2.0/9.0
nRun['TTM1600TZBW'] = nRunTTM1600*2.0/9.0
nRun['TTM1700TZBW'] = nRunTTM1700*2.0/9.0
nRun['TTM1800TZBW'] = nRunTTM1800*2.0/9.0
nRun['TTM1000TZTZ'] = nRunTTM1000/9.0
nRun['TTM1100TZTZ'] = nRunTTM1100/9.0
nRun['TTM1200TZTZ'] = nRunTTM1200/9.0
nRun['TTM1300TZTZ'] = nRunTTM1300/9.0
nRun['TTM1400TZTZ'] = nRunTTM1400/9.0
nRun['TTM1500TZTZ'] = nRunTTM1500/9.0
nRun['TTM1600TZTZ'] = nRunTTM1600/9.0
nRun['TTM1700TZTZ'] = nRunTTM1700/9.0
nRun['TTM1800TZTZ'] = nRunTTM1800/9.0
nRun['TTM1000TZTH'] = nRunTTM1000*2.0/9.0
nRun['TTM1100TZTH'] = nRunTTM1100*2.0/9.0
nRun['TTM1200TZTH'] = nRunTTM1200*2.0/9.0
nRun['TTM1300TZTH'] = nRunTTM1300*2.0/9.0
nRun['TTM1400TZTH'] = nRunTTM1400*2.0/9.0
nRun['TTM1500TZTH'] = nRunTTM1500*2.0/9.0
nRun['TTM1600TZTH'] = nRunTTM1600*2.0/9.0
nRun['TTM1700TZTH'] = nRunTTM1700*2.0/9.0
nRun['TTM1800TZTH'] = nRunTTM1800*2.0/9.0
nRun['TTM1000THTH'] = nRunTTM1000/9.0
nRun['TTM1100THTH'] = nRunTTM1100/9.0
nRun['TTM1200THTH'] = nRunTTM1200/9.0
nRun['TTM1300THTH'] = nRunTTM1300/9.0
nRun['TTM1400THTH'] = nRunTTM1400/9.0
nRun['TTM1500THTH'] = nRunTTM1500/9.0
nRun['TTM1600THTH'] = nRunTTM1600/9.0
nRun['TTM1700THTH'] = nRunTTM1700/9.0
nRun['TTM1800THTH'] = nRunTTM1800/9.0


## BBPrimes Effective integral from dumpCounts Nov2020, pdf4LHC integral from E.S. dumpMuPDF
nRunBBM1000 = 1011510.55*844000.0/850000.0 # from integral 850000.0, BprimeBprime_M-1000_TuneCP5_13TeV-madgraph-pythia8
nRunBBM1100 = 969137.0*803000.0/806000.0 # from integral 806000.0, BprimeBprime_M-1100_TuneCP5_13TeV-madgraph-pythia8
nRunBBM1200 = 1027818.122 # from integral 850000.0, BprimeBprime_M-1200_TuneCP5_13TeV-madgraph-pythia8
nRunBBM1300 = 917763.768 # from integral 758000.0, BprimeBprime_M-1300_TuneCP5_13TeV-madgraph-pythia8
nRunBBM1400 = 877071.614*716000.0/728000.0 # from integral 728000.0, BprimeBprime_M-1400_TuneCP5_13TeV-madgraph-pythia8
nRunBBM1500 = 804769.156 # from integral 675000.0, BprimeBprime_M-1500_TuneCP5_13TeV-madgraph-pythia8
nRunBBM1600 = 895604.498*766000.0/769000.0 # from integral 769000.0, BprimeBprime_M-1600_TuneCP5_13TeV-madgraph-pythia8
nRunBBM1700 = 946782.494*824000.0/842000.0 # from integral 842000.0, BprimeBprime_M-1700_TuneCP5_13TeV-madgraph-pythia8
nRunBBM1800 = 915634.724 # from integral 850000.0, BprimeBprime_M-1800_TuneCP5_13TeV-madgraph-pythia8
nRun['BBM1000TWTW'] = nRunBBM1000/9.0
nRun['BBM1100TWTW'] = nRunBBM1100/9.0
nRun['BBM1200TWTW'] = nRunBBM1200/9.0
nRun['BBM1300TWTW'] = nRunBBM1300/9.0
nRun['BBM1400TWTW'] = nRunBBM1400/9.0
nRun['BBM1500TWTW'] = nRunBBM1500/9.0
nRun['BBM1600TWTW'] = nRunBBM1600/9.0
nRun['BBM1700TWTW'] = nRunBBM1700/9.0
nRun['BBM1800TWTW'] = nRunBBM1800/9.0
nRun['BBM1000BHTW'] = nRunBBM1000*2.0/9.0
nRun['BBM1100BHTW'] = nRunBBM1100*2.0/9.0
nRun['BBM1200BHTW'] = nRunBBM1200*2.0/9.0
nRun['BBM1300BHTW'] = nRunBBM1300*2.0/9.0
nRun['BBM1400BHTW'] = nRunBBM1400*2.0/9.0
nRun['BBM1500BHTW'] = nRunBBM1500*2.0/9.0
nRun['BBM1600BHTW'] = nRunBBM1600*2.0/9.0
nRun['BBM1700BHTW'] = nRunBBM1700*2.0/9.0
nRun['BBM1800BHTW'] = nRunBBM1800*2.0/9.0
nRun['BBM1000BZTW'] = nRunBBM1000*2.0/9.0
nRun['BBM1100BZTW'] = nRunBBM1100*2.0/9.0
nRun['BBM1200BZTW'] = nRunBBM1200*2.0/9.0
nRun['BBM1300BZTW'] = nRunBBM1300*2.0/9.0
nRun['BBM1400BZTW'] = nRunBBM1400*2.0/9.0
nRun['BBM1500BZTW'] = nRunBBM1500*2.0/9.0
nRun['BBM1600BZTW'] = nRunBBM1600*2.0/9.0
nRun['BBM1700BZTW'] = nRunBBM1700*2.0/9.0
nRun['BBM1800BZTW'] = nRunBBM1800*2.0/9.0
nRun['BBM1000BZBZ'] = nRunBBM1000/9.0
nRun['BBM1100BZBZ'] = nRunBBM1100/9.0
nRun['BBM1200BZBZ'] = nRunBBM1200/9.0
nRun['BBM1300BZBZ'] = nRunBBM1300/9.0
nRun['BBM1400BZBZ'] = nRunBBM1400/9.0
nRun['BBM1500BZBZ'] = nRunBBM1500/9.0
nRun['BBM1600BZBZ'] = nRunBBM1600/9.0
nRun['BBM1700BZBZ'] = nRunBBM1700/9.0
nRun['BBM1800BZBZ'] = nRunBBM1800/9.0
nRun['BBM1000BZBH'] = nRunBBM1000*2.0/9.0
nRun['BBM1100BZBH'] = nRunBBM1100*2.0/9.0
nRun['BBM1200BZBH'] = nRunBBM1200*2.0/9.0
nRun['BBM1300BZBH'] = nRunBBM1300*2.0/9.0
nRun['BBM1400BZBH'] = nRunBBM1400*2.0/9.0
nRun['BBM1500BZBH'] = nRunBBM1500*2.0/9.0
nRun['BBM1600BZBH'] = nRunBBM1600*2.0/9.0
nRun['BBM1700BZBH'] = nRunBBM1700*2.0/9.0
nRun['BBM1800BZBH'] = nRunBBM1800*2.0/9.0
nRun['BBM1000BHBH'] = nRunBBM1000/9.0
nRun['BBM1100BHBH'] = nRunBBM1100/9.0
nRun['BBM1200BHBH'] = nRunBBM1200/9.0
nRun['BBM1300BHBH'] = nRunBBM1300/9.0
nRun['BBM1400BHBH'] = nRunBBM1400/9.0
nRun['BBM1500BHBH'] = nRunBBM1500/9.0
nRun['BBM1600BHBH'] = nRunBBM1600/9.0
nRun['BBM1700BHBH'] = nRunBBM1700/9.0
nRun['BBM1800BHBH'] = nRunBBM1800/9.0

nRun['X53X53M700left']  = 300000.
nRun['X53X53M700right'] = 299800.
nRun['X53X53M800left']  = 300000.
nRun['X53X53M800right'] = 300000.
nRun['X53X53M900left']  = 300000.
nRun['X53X53M900right'] = 300000.
nRun['X53X53M1000left']  = 300000.
nRun['X53X53M1000right'] = 300000.
nRun['X53X53M1100left']  = 300000.
nRun['X53X53M1100right'] = 300000.
nRun['X53X53M1200left']  = 300000.
nRun['X53X53M1200right'] = 299800.
nRun['X53X53M1300left']  = 299800.
nRun['X53X53M1300right'] = 300000.
nRun['X53X53M1400left']  = 300000.
nRun['X53X53M1400right'] = 299800.
nRun['X53X53M1500left']  = 296400.
nRun['X53X53M1500right'] = 300000.
nRun['X53X53M1600left']  = 300000.
nRun['X53X53M1600right'] = 300000.

# Cross sections for MC samples (in pb) -- most unchanged for 2017
xsec={}
xsec['DY'] = 6025.2 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG'] = 6025.2 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG100'] = 147.4*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG200'] = 40.99*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG400'] = 5.678*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG600'] = 1.367*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG800'] = 0.6304*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG1200'] = 0.1514*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG2500'] = 0.003565*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['TTJets'] = 831.76
xsec['WJets'] = 61526.7
xsec['WJetsMG'] = 61526.7
xsec['TTJetsPH'] = 831.76 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
#xsec['TTJetsPH0to700inc'] = 831.76
#xsec['TTJetsPH700to1000inc'] = 831.76*0.0921 #(xsec*filtering coeff.)
#xsec['TTJetsPH1000toINFinc'] = 831.76*0.02474 #(xsec*filtering coeff.)
xsec['TTJetsHad0'] = 831.76*0.8832*0.457  ## BRs from PDG Top Review 2018: 45.7%/43.8%/10.5% 0/1/2 leptons
xsec['TTJetsHad700'] = 831.76*0.0921*0.457
xsec['TTJetsHad1000'] = 831.76*0.02474*0.457
xsec['TTJetsSemiLep0'] = 831.76*0.8832*0.438
xsec['TTJetsSemiLep700'] = 831.76*0.0921*0.438
xsec['TTJetsSemiLep1000'] = 831.76*0.02474*0.438
xsec['TTJets2L2nu0'] = 831.76*0.8832*0.105
xsec['TTJets2L2nu700'] = 831.76*0.0921*0.105
xsec['TTJets2L2nu1000'] = 831.76*0.02474*0.105
xsec['TTJetsPH700mtt'] = 831.76*0.0921 #(xsec*filtering coeff.)
xsec['TTJetsPH1000mtt'] = 831.76*0.02474 #(xsec*filtering coeff.)
#xsec['TTJetsPH700mtt'] = 38407913.0 # :from integral 39143691.0, file TT_Mtt-700to1000_TuneCP5_PSweights_13TeV-powheg-pythia8_1_hadd.root
#xsec['TTJetsPH1000mtt'] = 21290463.0 # :from integral 22446291.0, file TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg-pythia8_1_hadd.root

xsec['TTHB'] = 0.2934
# xsec['TTHB'] = 7776731.0 # :from integral 7941843.0, file ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_1_hadd.root
xsec['TTHnoB'] = 0.215
# xsec['TTHnoB'] = 7814711.0 # :from integral 7966779.0, file ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_1_hadd.root

xsec['WJetsMG100'] = 1345.*1.21 # (1.21 = k-factor )# https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG200'] = 359.7*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG400'] = 48.91*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['WJetsMG400'] = 14237953.0 # :from integral 14301047.0, file WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root
xsec['WJetsMG600'] = 12.05*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['WJetsMG600'] = 21570948.0 # :from integral 21697666.0, file WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root
xsec['WJetsMG800'] = 5.501*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['WJetsMG800'] = 19621253.0 # :from integral 19775877.0, file WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root
xsec['WJetsMG1200'] = 1.329*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['WJetsMG1200'] = 37723518.0 # :from integral 38226974.0, file WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root
xsec['WJetsMG2500'] = 0.03216*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns 
# xsec['WJetsMG2500'] = 20362902.0 # :from integral 21217774.0, file WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_1_hadd.root
xsec['WJetsPt100'] = 676.3 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt250'] = 23.94 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt400'] = 3.031 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt600'] = 0.4524 #B2G-17-010 / AN2016_480_v5
xsec['WW'] = 118.7 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeVInclusive
# xsec['WW'] = 7765828.0 # :from integral 7765828.0, file WW_TuneCP5_13TeV-pythia8_hadd.root
xsec['WZ'] = 47.13 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
# xsec['WZ'] = 3928630.0 # :from integral 3928630.0, file WZ_TuneCP5_13TeV-pythia8_hadd.root
xsec['ZZ'] = 16.523 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
# xsec['ZZ'] = 1925931.0 # :from integral 1925931.0, file ZZ_TuneCP5_13TeV-pythia8_hadd.root
xsec['TTH'] = 0.5269 # from XsecDB, NLO
xsec['TTW'] = 0.4611 # from XsecDB, LO
xsec['TTZ'] = 0.5407 # from XsecDB, LO
xsec['TTZl'] = 0.2529 # from McM
xsec['TTZq'] = 0.5297 # from McM
xsec['TTWl'] = 0.2043 # from McM
xsec['TTWq'] = 0.4062 # from McM
xsec['Tt'] = 136.02 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Tbt'] = 80.95 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Ts'] = 6.35*0.333 #(leptonic) https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Tbs'] = 3.97*0.333 #(leptonic)# https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['TtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['TbtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec

xsec['TTM700']   = 0.455 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
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

xsec['BBM700']   = 0.455 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM800']  = 0.196 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM900']   = 0.0903 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1000']  = 0.0440 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1100']  = 0.0224 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1300']  = 0.00639 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1500']  = 0.00200 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1700']  = 0.000666 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo
xsec['BBM1800'] = 0.000391 # from https://twiki.cern.ch/twiki/bin/view/CMS/B2GMonteCarlo

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

xsec['QCDht100'] = 27990000. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht200'] = 1712000. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht300'] = 347700. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht500'] = 32100. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht700'] = 6831. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht1000'] = 1207. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht1500'] = 119.9 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht2000'] = 25.24 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD

# Calculate lumi normalization weights
weight = {}
for sample in sorted(nRun.keys()): 
	if 'BBM' not in sample and 'TTM' not in sample: 
		#print sample, (xsec[sample]) , (nRun[sample])
		weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])
	else: weight[sample] = (targetlumi*BR[sample[:2]+sample[-4:]]*xsec[sample[:-4]]) / (nRun[sample])
# Samples for Jet reweighting (to be able to run w/ and w/o JSF together!):
for sample in sorted(nRun.keys()):
	if 'QCDht' in sample or 'WJetsMG' in sample: weight[sample+'JSF'] = weight[sample]

#  LocalWords:  nRun
