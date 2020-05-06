#!/usr/bin/python

targetlumi = 41530. # 1/pb

# Number of processed MC events (before selections)
nRun={}
# new counts for 2017
#Do NGen*[1-2X], where X is the neg event fraction calculated from the jobs completed! 
#A = P - N = F - 2*N   A/F = 1 - 2*(N/F)  N/F = (1 - A/F)/2
nRun['TTJets'] = 14188545. #need negative counts

BR_TTJetsHad = 0.457
BR_TTJetsSemiLep = 0.438
BR_TTJets2L2nu = 0.105
filtEff_TTJets1000mtt = 0.02474
filtEff_TTJets700mtt = 0.0921
filtEff_TTJets0mtt = 0.8832 # 1-filtEff_TTJets700mtt-filtEff_TTJets1000mtt
filtEff_TTJetsSemiLepNjet9 = 0.0057 # from McM
nRun_TTJetsHad = 129092906.0 # from integral 130262340.0, file TTToHadronic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_hadd.root
nRun_TTJetsSemiLep = 109124472.0 # from integral 110085096.0, file TTToSemiLeptonic_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_hadd.root
nRun_TTJets2L2nu = 68448328.0 # from integral 69155808.0, file TTTo2L2Nu_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_hadd.root
nRun_TTJets700mtt = 38299363.0 # from 39258853, file TT_Mtt-700to1000_TuneCP5_13TeV-powheg-pythia8_hadd.root
nRun_TTJets1000mtt = 21288395.0 # from integral 22458751.0, file TT_Mtt-1000toInf_TuneCP5_PSweights_13TeV-powheg
nRun_TTJetsSemiLepNjet9 = 8648145.0 # from integral, file TTToSemiLepton_HT500Njet9_TuneCP5_PSweights_13TeV-powheg-pythia8_Mtt0to700_hadd.root
nRun['TTJetsHad0']    = nRun_TTJetsHad * filtEff_TTJets0mtt 
nRun['TTJetsHad700']  = nRun_TTJetsHad * filtEff_TTJets700mtt  + nRun_TTJets700mtt  * BR_TTJetsHad
nRun['TTJetsHad1000'] = nRun_TTJetsHad * filtEff_TTJets1000mtt + nRun_TTJets1000mtt * BR_TTJetsHad
nRun['TTJetsSemiLep0']    = nRun_TTJetsSemiLep * filtEff_TTJets0mtt 
nRun['TTJetsSemiLep700']  = nRun_TTJetsSemiLep * filtEff_TTJets700mtt  + nRun_TTJets700mtt  * BR_TTJetsSemiLep
nRun['TTJetsSemiLep1000'] = nRun_TTJetsSemiLep * filtEff_TTJets1000mtt + nRun_TTJets1000mtt * BR_TTJetsSemiLep
nRun['TTJets2L2nu0']    = nRun_TTJets2L2nu * filtEff_TTJets0mtt 
nRun['TTJets2L2nu700']  = nRun_TTJets2L2nu * filtEff_TTJets700mtt  + nRun_TTJets700mtt  * BR_TTJets2L2nu
nRun['TTJets2L2nu1000'] = nRun_TTJets2L2nu * filtEff_TTJets1000mtt + nRun_TTJets1000mtt * BR_TTJets2L2nu
nRun['TTJets700mtt']  = nRun_TTJets700mtt  + nRun_TTJetsHad * filtEff_TTJets700mtt  + nRun_TTJetsSemiLep * filtEff_TTJets700mtt  + nRun_TTJets2L2nu * filtEff_TTJets700mtt
nRun['TTJets1000mtt'] = nRun_TTJets1000mtt + nRun_TTJetsHad * filtEff_TTJets1000mtt + nRun_TTJetsSemiLep * filtEff_TTJets1000mtt + nRun_TTJets2L2nu * filtEff_TTJets1000mtt

nRun['TTJetsHad'] = nRun_TTJetsHad
nRun['TTJetsSemiLepNjet0'] = nRun_TTJetsSemiLep * ( 1. - filtEff_TTJetsSemiLepNjet9 ) 
nRun['TTJetsSemiLepNjet9'] = nRun_TTJetsSemiLep * filtEff_TTJetsSemiLepNjet9 + nRun_TTJetsSemiLepNjet9
nRun['TTJetsSemiLepNjet9bin'] = nRun['TTJetsSemiLepNjet9']
nRun['TTJets2L2nu'] = nRun_TTJets2L2nu
nRun['TTJetsSemiLep'] = nRun_TTJetsSemiLep

nRun['TTJets2L2nuUEdn'] = 5431150.0 # from integral, file TTTo2L2Nu_TuneCP5down_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJets2L2nuUEup'] = 5455598.0 # from integral, file TTTo2L2Nu_TuneCP5up_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJets2L2nuHDAMPdn'] = 5248352.0 # from integral, file TTTo2L2Nu_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJets2L2nuHDAMPup'] = 5389169.0 # from integral, file TTTo2L2Nu_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJetsSemiLepUEdn'] = 26885578.0 # from integral, file TTToSemiLeptonic_TuneCP5down_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJetsSemiLepUEup'] = 25953874.0 # from integral, file TTToSemiLeptonic_TuneCP5up_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJetsSemiLepHDAMPdn'] = 26359926.0 # from integral, file TTToSemiLeptonic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJetsSemiLepHDAMPup'] = 27068397.0 # from integral, file TTToSemiLeptonic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJetsHadUEdn'] = 25943263.0 # from integral, file TTToHadronic_TuneCP5down_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJetsHadUEup'] = 26986311.0 # from integral, file TTToHadronic_TuneCP5up_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJetsHadHDAMPdn'] = 26007959.0 # from integral, file TTToHadronic_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJetsHadHDAMPup'] = 25586551.0 # from integral, file TTToHadronic_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root

nRun['Ts'] = 6895750.0 # from integral 6898000.0, file ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia_hadd.root
nRun['Tbs'] = 2952214.0 # from integral 2953000.0, file ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia_hadd.root
nRun['Tt'] = 122688200.0 # from integral 109621700.0, file ST_t-channel_top_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_hadd.root
nRun['Tbt']= 64818800.0 # from integral 50194500.0, file ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_hadd.root
nRun['TtW'] = 7884388.0 # from integral 7945242.0, file ST_tW_top_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_hadd.root
nRun['TbtW'] = 7686032.0 # from integral 7745276.0, file ST_tW_antitop_5f_inclusiveDecays_TuneCP5_PSweights_13TeV-powheg-pythia8_hadd.root

nRun['WJetsMG200'] = 16118580.0 # from integral 21250517.0, file WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WJetsMG400'] = 14237953.0 # from integral 14252285.0, file WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WJetsMG600'] = 21570948.0 # from integral 21455857.0, file WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WJetsMG800'] = 20187318.0 # from integral 20432728.0, file WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WJetsMG1200'] = 39694923.0 # from integral 20216830.0, file WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['WJetsMG2500'] = 34500020.0 # from integral 21495421.0, file WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root

nRun['DYMG200'] = 10699051.0 # from integral 10728447.0, file DYJetsToLL_M-50_HT-200to400_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG400'] = 10174800.0 # from integral 10219524.0, file DYJetsToLL_M-50_HT-400to600_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG600'] = 8691608.0 # from integral 8743640.0, file DYJetsToLL_M-50_HT-600to800_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG800'] = 3089712.0 # from integral 3114980.0, file DYJetsToLL_M-50_HT-800to1200_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG1200']= 616906.0 # from integral 625517.0, file DYJetsToLL_M-50_HT-1200to2500_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root
nRun['DYMG2500']=  401334.0 # from integral 419308.0, file DYJetsToLL_M-50_HT-2500toInf_TuneCP5_13TeV-madgraphMLM-pythia8_hadd.root

nRun['WW'] = 7765828.0 # from integral 7765828.0, file WW_TuneCP5_13TeV-pythia8_hadd.root
nRun['WZ'] = 3928567.0 # from integral 3928630.0, file WZ_TuneCP5_13TeV-pythia8_hadd.root
nRun['ZZ'] = 1925931.0 # from integral 1925931.0, file ZZ_TuneCP5_13TeV-pythia8_hadd.root

nRun['QCDht200'] = 59360369.0 # from integral 59074480.0, file QCD_HT200to300_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht300'] = 59459614.0 # from integral 59569132.0, file QCD_HT300to500_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht500'] = 56041018.0 # from integral 56207744.0, file QCD_HT500to700_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht700'] = 135551578.0 # from integral 46840955.0, file QCD_HT700to1000_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht1000'] = 16770762.0 # from integral 16882838.0, file QCD_HT1000to1500_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht1500'] = 11508604.0 # from integral 11634434.0, file QCD_HT1500to2000_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['QCDht2000'] = 5825566.0 # from integral 5941306.0, file QCD_HT2000toInf_TuneCP5_13TeV-madgraph-pythia8_hadd.root

nRun['TTW'] = 9384328. # from integral 9425384.0, file ttWJets_TuneCP5_13TeV_madgraphMLM_pythia8_hadd.root
nRun['TTZ'] = 8519074. # from integral 8536618.0, file ttZJets_TuneCP5_13TeV_madgraphMLM_pythia8_hadd.root
nRun['TTH'] = 9580578. # from integral 9783674.0, file ttH_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root
nRun['TTWl'] = 2686141.0 # from integral, file TTWJetsToLNu_TuneCP5_PSweights_13TeV-amcatnloFXFX-madspin-pythia8_hadd.root
nRun['TTWq'] = 441560.0 # from integral 811306.0, file TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_hadd.root
nRun['TTZlM10'] = 5239484.0 # from integral, file TTZToLLNuNu_M-10_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_hadd.root
nRun['TTZlM1to10'] = 129114.0 # from integral, file TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root
nRun['TTZq'] = 351164. # from 749400
nRun['TTHB'] = 7833734.0 # from integral 8000000.0, file ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root
nRun['TTHnoB'] = 7814711.0 # from integral 7161154.0, file ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8_hadd.root

nRun['TTHH'] = 199371.0 # from integral, file TTHH_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['TTTJ'] = 198546.0 # from integral, file TTTJ_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['TTTW'] = 199699.0 # from integral, file TTTW_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['TTWH'] = 198978.0 # from integral, file TTWH_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['TTWW'] = 199008.0 # from integral, file TTWW_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['TTWZ'] = 198756.0 # from integral, file TTWZ_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['TTZH'] = 199285.0 # from integral, file TTZH_TuneCP5_13TeV-madgraph-pythia8_hadd.root
nRun['TTZZ'] = 199363.0 # from integral, file TTZZ_TuneCP5_13TeV-madgraph-pythia8_hadd.root

#4 tops
#nRun['TTTTM690'] = 373734.0 # from 1M generated events, file TTTT_TuneCP5_13TeV-amcatnlo-pythia8_hadd.root
nRun['TTTTM690'] = 849964.0 # from file TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_hadd.root

# Cross sections for MC samples (in pb) -- most unchanged for 2017
xsec={}
xsec['TTJets'] = 831.76
xsec['TTJetsHad0']    = xsec['TTJets'] * BR_TTJetsHad * filtEff_TTJets0mtt # BRs from PDG Top Review 2018: 45.7%/43.8%/10.5% 0/1/2 leptons
xsec['TTJetsHad700']  = xsec['TTJets'] * BR_TTJetsHad * filtEff_TTJets700mtt
xsec['TTJetsHad1000'] = xsec['TTJets'] * BR_TTJetsHad * filtEff_TTJets1000mtt
xsec['TTJetsSemiLep0']    = xsec['TTJets'] * BR_TTJetsSemiLep * filtEff_TTJets0mtt
xsec['TTJetsSemiLep700']  = xsec['TTJets'] * BR_TTJetsSemiLep * filtEff_TTJets700mtt
xsec['TTJetsSemiLep1000'] = xsec['TTJets'] * BR_TTJetsSemiLep * filtEff_TTJets1000mtt
xsec['TTJets2L2nu0']    = xsec['TTJets'] * BR_TTJets2L2nu * filtEff_TTJets0mtt
xsec['TTJets2L2nu700']  = xsec['TTJets'] * BR_TTJets2L2nu * filtEff_TTJets700mtt
xsec['TTJets2L2nu1000'] = xsec['TTJets'] * BR_TTJets2L2nu * filtEff_TTJets1000mtt
xsec['TTJets700mtt']  = xsec['TTJets'] * filtEff_TTJets700mtt # (xsec*filtering coeff.)
xsec['TTJets1000mtt'] = xsec['TTJets'] * filtEff_TTJets1000mtt # (xsec*filtering coeff.)

xsec['TTJetsHad'] = xsec['TTJets'] * BR_TTJetsHad
xsec['TTJetsSemiLepNjet0'] = xsec['TTJets'] * BR_TTJetsSemiLep * ( 1. - filtEff_TTJetsSemiLepNjet9 ) 
xsec['TTJetsSemiLepNjet9'] = xsec['TTJets'] * BR_TTJetsSemiLep * filtEff_TTJetsSemiLepNjet9
xsec['TTJetsSemiLepNjet9bin'] = xsec['TTJetsSemiLepNjet9']
xsec['TTJets2L2nu'] = xsec['TTJets'] * BR_TTJets2L2nu
xsec['TTJetsSemiLep'] = xsec['TTJets'] * BR_TTJetsSemiLep

xsec['TTJets2L2nuUEdn'] = xsec['TTJets'] * BR_TTJets2L2nu
xsec['TTJets2L2nuUEup'] = xsec['TTJets'] * BR_TTJets2L2nu
xsec['TTJets2L2nuHDAMPdn'] = xsec['TTJets'] * BR_TTJets2L2nu
xsec['TTJets2L2nuHDAMPup'] = xsec['TTJets'] * BR_TTJets2L2nu
xsec['TTJetsSemiLepUEdn'] = xsec['TTJets'] * BR_TTJetsSemiLep
xsec['TTJetsSemiLepUEup'] = xsec['TTJets'] * BR_TTJetsSemiLep
xsec['TTJetsSemiLepHDAMPdn'] = xsec['TTJets'] * BR_TTJetsSemiLep
xsec['TTJetsSemiLepHDAMPup'] = xsec['TTJets'] * BR_TTJetsSemiLep
xsec['TTJetsHadUEdn'] = xsec['TTJets'] * BR_TTJetsHad
xsec['TTJetsHadUEup'] = xsec['TTJets'] * BR_TTJetsHad
xsec['TTJetsHadHDAMPdn'] = xsec['TTJets'] * BR_TTJetsHad
xsec['TTJetsHadHDAMPup'] = xsec['TTJets'] * BR_TTJetsHad

xsec['Ts'] = 7.20/3 #(1/3 was suggested by Thomas Peiffer to account for the leptonic branching ratio)# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['Tbs'] = 4.16/3 #(1/3 was suggested by Thomas Peiffer to account for the leptonic branching ratio)# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['Tt'] = 136.02 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['Tbt'] = 80.95 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['TtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['TbtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma

xsec['WJets'] = 61526.7
xsec['WJetsMG'] = 61526.7
xsec['WJetsMG100'] = 1345.*1.21 # (1.21 = k-factor )# https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG200'] = 359.7*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG400'] = 48.91*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG600'] = 12.05*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG800'] = 5.501*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG1200'] = 1.329*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsMG2500'] = 0.03216*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns 
xsec['WJetsPt100'] = 676.3 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt250'] = 23.94 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt400'] = 3.031 #B2G-17-010 / AN2016_480_v5
xsec['WJetsPt600'] = 0.4524 #B2G-17-010 / AN2016_480_v5

xsec['DY'] = 6025.2 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG'] = 6025.2 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG100'] = 147.4*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG200'] = 40.99*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG400'] = 5.678*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG600'] = 1.367*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG800'] = 0.6304*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG1200'] = 0.1514*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG2500'] = 0.003565*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns

xsec['WW'] = 118.7 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeVInclusive
xsec['WZ'] = 47.13 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
xsec['ZZ'] = 16.523 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson

xsec['QCDht100'] = 27990000. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht200'] = 1712000. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht300'] = 347700. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht500'] = 32100. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht700'] = 6831. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht1000'] = 1207. # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD
xsec['QCDht1500'] = 119.9 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD 
xsec['QCDht2000'] = 25.24 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#QCD

xsec['TTW'] = 0.4611 # from XsecDB, LO
xsec['TTZ'] = 0.5407 # from XsecDB, LO
xsec['TTH'] = 0.5269 # from XsecDB, NLO
xsec['TTWl'] = 0.2043 # from McM
xsec['TTWq'] = 0.4062 # from McM
xsec['TTZlM10'] = 0.2529 # from McM
xsec['TTZlM1to10'] = 0.2529 # from McM
xsec['TTZq'] = 0.5297 # from McM
xsec['TTHB'] = 0.2934
xsec['TTHnoB'] = 0.215

xsec['TTHH'] = 0.0007408 # from McM
xsec['TTTJ'] = 0.0004741 # from McM
xsec['TTTW'] = 0.000733 # from McM
xsec['TTWH'] = 0.001359 # from McM
xsec['TTWW'] = 0.007883 # from McM
xsec['TTWZ'] = 0.002974 # from McM
xsec['TTZH'] = 0.001253 # from McM
xsec['TTZZ'] = 0.001572 # from McM

#4 Tops
xsec['TTTTM690'] = 0.012 # from https://arxiv.org/pdf/1711.02116.pdf, in McM: 0.008213

# Calculate lumi normalization weights
weight = {}
for sample in sorted(nRun.keys()): 
	weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])

weight['WJetsMG12001'] = weight['WJetsMG1200']
weight['WJetsMG12002'] = weight['WJetsMG1200']
weight['WJetsMG12003'] = weight['WJetsMG1200']
weight['WJetsMG25001'] = weight['WJetsMG2500'] 
weight['WJetsMG25002'] = weight['WJetsMG2500'] 
weight['WJetsMG25003'] = weight['WJetsMG2500'] 
weight['WJetsMG25004'] = weight['WJetsMG2500']

weight['TTJets2L2nuTT1b'] = weight['TTJets2L2nu']
weight['TTJets2L2nuTT2b'] = weight['TTJets2L2nu']
weight['TTJets2L2nuTTbb'] = weight['TTJets2L2nu']
weight['TTJets2L2nuTTcc'] = weight['TTJets2L2nu']
weight['TTJets2L2nuTTjj'] = weight['TTJets2L2nu']
weight['TTJetsHadTT1b'] = weight['TTJetsHad']
weight['TTJetsHadTT2b'] = weight['TTJetsHad']
weight['TTJetsHadTTbb'] = weight['TTJetsHad']
weight['TTJetsHadTTcc'] = weight['TTJetsHad']
weight['TTJetsHadTTjj'] = weight['TTJetsHad']
weight['TTJetsSemiLepNjet0TT1b'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TT2b'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTbb'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTcc'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj1'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj2'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj3'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj4'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj5'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet9TT1b'] = weight['TTJetsSemiLepNjet9']
weight['TTJetsSemiLepNjet9TT2b'] = weight['TTJetsSemiLepNjet9']
weight['TTJetsSemiLepNjet9TTbb'] = weight['TTJetsSemiLepNjet9']
weight['TTJetsSemiLepNjet9TTcc'] = weight['TTJetsSemiLepNjet9']
weight['TTJetsSemiLepNjet9TTjj'] = weight['TTJetsSemiLepNjet9']
weight['TTJetsSemiLepNjet9binTT1b'] = weight['TTJetsSemiLepNjet9bin']
weight['TTJetsSemiLepNjet9binTT2b'] = weight['TTJetsSemiLepNjet9bin']
weight['TTJetsSemiLepNjet9binTTbb'] = weight['TTJetsSemiLepNjet9bin']
weight['TTJetsSemiLepNjet9binTTcc'] = weight['TTJetsSemiLepNjet9bin']
weight['TTJetsSemiLepNjet9binTTjj'] = weight['TTJetsSemiLepNjet9bin']

weight['TTJets2L2nuUEdnTT1b'] = weight['TTJets2L2nuUEdn']
weight['TTJets2L2nuUEdnTT2b'] = weight['TTJets2L2nuUEdn']
weight['TTJets2L2nuUEdnTTbb'] = weight['TTJets2L2nuUEdn']
weight['TTJets2L2nuUEdnTTcc'] = weight['TTJets2L2nuUEdn']
weight['TTJets2L2nuUEdnTTjj'] = weight['TTJets2L2nuUEdn']
weight['TTJets2L2nuUEupTT1b'] = weight['TTJets2L2nuUEup']
weight['TTJets2L2nuUEupTT2b'] = weight['TTJets2L2nuUEup']
weight['TTJets2L2nuUEupTTbb'] = weight['TTJets2L2nuUEup']
weight['TTJets2L2nuUEupTTcc'] = weight['TTJets2L2nuUEup']
weight['TTJets2L2nuUEupTTjj'] = weight['TTJets2L2nuUEup']
weight['TTJets2L2nuHDAMPdnTT1b'] = weight['TTJets2L2nuHDAMPdn']
weight['TTJets2L2nuHDAMPdnTT2b'] = weight['TTJets2L2nuHDAMPdn']
weight['TTJets2L2nuHDAMPdnTTbb'] = weight['TTJets2L2nuHDAMPdn']
weight['TTJets2L2nuHDAMPdnTTcc'] = weight['TTJets2L2nuHDAMPdn']
weight['TTJets2L2nuHDAMPdnTTjj'] = weight['TTJets2L2nuHDAMPdn']
weight['TTJets2L2nuHDAMPupTT1b'] = weight['TTJets2L2nuHDAMPup']
weight['TTJets2L2nuHDAMPupTT2b'] = weight['TTJets2L2nuHDAMPup']
weight['TTJets2L2nuHDAMPupTTbb'] = weight['TTJets2L2nuHDAMPup']
weight['TTJets2L2nuHDAMPupTTcc'] = weight['TTJets2L2nuHDAMPup']
weight['TTJets2L2nuHDAMPupTTjj'] = weight['TTJets2L2nuHDAMPup']

weight['TTJetsHadUEdnTT1b'] = weight['TTJetsHadUEdn']
weight['TTJetsHadUEdnTT2b'] = weight['TTJetsHadUEdn']
weight['TTJetsHadUEdnTTbb'] = weight['TTJetsHadUEdn']
weight['TTJetsHadUEdnTTcc'] = weight['TTJetsHadUEdn']
weight['TTJetsHadUEdnTTjj'] = weight['TTJetsHadUEdn']
weight['TTJetsHadUEupTT1b'] = weight['TTJetsHadUEup']
weight['TTJetsHadUEupTT2b'] = weight['TTJetsHadUEup']
weight['TTJetsHadUEupTTbb'] = weight['TTJetsHadUEup']
weight['TTJetsHadUEupTTcc'] = weight['TTJetsHadUEup']
weight['TTJetsHadUEupTTjj'] = weight['TTJetsHadUEup']
weight['TTJetsHadHDAMPdnTT1b'] = weight['TTJetsHadHDAMPdn']
weight['TTJetsHadHDAMPdnTT2b'] = weight['TTJetsHadHDAMPdn']
weight['TTJetsHadHDAMPdnTTbb'] = weight['TTJetsHadHDAMPdn']
weight['TTJetsHadHDAMPdnTTcc'] = weight['TTJetsHadHDAMPdn']
weight['TTJetsHadHDAMPdnTTjj'] = weight['TTJetsHadHDAMPdn']
weight['TTJetsHadHDAMPupTT1b'] = weight['TTJetsHadHDAMPup']
weight['TTJetsHadHDAMPupTT2b'] = weight['TTJetsHadHDAMPup']
weight['TTJetsHadHDAMPupTTbb'] = weight['TTJetsHadHDAMPup']
weight['TTJetsHadHDAMPupTTcc'] = weight['TTJetsHadHDAMPup']
weight['TTJetsHadHDAMPupTTjj'] = weight['TTJetsHadHDAMPup']

weight['TTJetsSemiLepUEdnTT1b'] = weight['TTJetsSemiLepUEdn']
weight['TTJetsSemiLepUEdnTT2b'] = weight['TTJetsSemiLepUEdn']
weight['TTJetsSemiLepUEdnTTbb'] = weight['TTJetsSemiLepUEdn']
weight['TTJetsSemiLepUEdnTTcc'] = weight['TTJetsSemiLepUEdn']
weight['TTJetsSemiLepUEdnTTjj'] = weight['TTJetsSemiLepUEdn']
weight['TTJetsSemiLepUEupTT1b'] = weight['TTJetsSemiLepUEup']
weight['TTJetsSemiLepUEupTT2b'] = weight['TTJetsSemiLepUEup']
weight['TTJetsSemiLepUEupTTbb'] = weight['TTJetsSemiLepUEup']
weight['TTJetsSemiLepUEupTTcc'] = weight['TTJetsSemiLepUEup']
weight['TTJetsSemiLepUEupTTjj'] = weight['TTJetsSemiLepUEup']
weight['TTJetsSemiLepHDAMPdnTT1b'] = weight['TTJetsSemiLepHDAMPdn']
weight['TTJetsSemiLepHDAMPdnTT2b'] = weight['TTJetsSemiLepHDAMPdn']
weight['TTJetsSemiLepHDAMPdnTTbb'] = weight['TTJetsSemiLepHDAMPdn']
weight['TTJetsSemiLepHDAMPdnTTcc'] = weight['TTJetsSemiLepHDAMPdn']
weight['TTJetsSemiLepHDAMPdnTTjj'] = weight['TTJetsSemiLepHDAMPdn']
weight['TTJetsSemiLepHDAMPupTT1b'] = weight['TTJetsSemiLepHDAMPup']
weight['TTJetsSemiLepHDAMPupTT2b'] = weight['TTJetsSemiLepHDAMPup']
weight['TTJetsSemiLepHDAMPupTTbb'] = weight['TTJetsSemiLepHDAMPup']
weight['TTJetsSemiLepHDAMPupTTcc'] = weight['TTJetsSemiLepHDAMPup']
weight['TTJetsSemiLepHDAMPupTTjj'] = weight['TTJetsSemiLepHDAMPup']
