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
#filtEff_TTJetsSemiLepNjet9 = 0.0057 # from McM
filtEff_TTJetsSemiLepNjet9 = 0.00617938417682763 # from nicholas.james.manganelli@cern.ch
filtEff_TTJetsSemiLepNjet9HDAMPdn = 0.005645170035947885 # from nicholas.james.manganelli@cern.ch
filtEff_TTJetsSemiLepNjet9HDAMPup = 0.006711348259851689 # from nicholas.james.manganelli@cern.ch
filtEff_TTJetsSemiLepNjet9UEdn = 0.006108623095875414 # from nicholas.james.manganelli@cern.ch
filtEff_TTJetsSemiLepNjet9UEup = 0.0062286452403598055 # from nicholas.james.manganelli@cern.ch
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

nRun_TTJetsSemiLepUEdn = nRun['TTJetsSemiLepUEdn']
nRun_TTJetsSemiLepUEup = nRun['TTJetsSemiLepUEup']
nRun_TTJetsSemiLepHDAMPdn = nRun['TTJetsSemiLepHDAMPdn']
nRun_TTJetsSemiLepHDAMPup = nRun['TTJetsSemiLepHDAMPup']
nRun_TTJetsSemiLepUEdnNjet9 = 1992461.0 # from integral, file TTToSemiLepton_HT500Njet9_TuneCP5down_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun_TTJetsSemiLepUEupNjet9 = 1652000.0 # from integral, file TTToSemiLepton_HT500Njet9_TuneCP5up_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun_TTJetsSemiLepHDAMPdnNjet9 = 1802904.0 # from integral, file TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun_TTJetsSemiLepHDAMPupNjet9 = 2322004.0 # from integral, file TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_PSweights_13TeV-powheg-pythia8_ttbb_hadd.root
nRun['TTJetsSemiLepUEdnNjet0'] = nRun_TTJetsSemiLepUEdn * ( 1. - filtEff_TTJetsSemiLepNjet9UEdn ) 
nRun['TTJetsSemiLepUEdnNjet9'] = nRun_TTJetsSemiLepUEdn * filtEff_TTJetsSemiLepNjet9UEdn + nRun_TTJetsSemiLepUEdnNjet9
nRun['TTJetsSemiLepUEdnNjet9bin'] = nRun['TTJetsSemiLepUEdnNjet9']
nRun['TTJetsSemiLepUEupNjet0'] = nRun_TTJetsSemiLepUEup * ( 1. - filtEff_TTJetsSemiLepNjet9UEup ) 
nRun['TTJetsSemiLepUEupNjet9'] = nRun_TTJetsSemiLepUEup * filtEff_TTJetsSemiLepNjet9UEup + nRun_TTJetsSemiLepUEupNjet9
nRun['TTJetsSemiLepUEupNjet9bin'] = nRun['TTJetsSemiLepUEupNjet9']
nRun['TTJetsSemiLepHDAMPdnNjet0'] = nRun_TTJetsSemiLepHDAMPdn * ( 1. - filtEff_TTJetsSemiLepNjet9HDAMPdn ) 
nRun['TTJetsSemiLepHDAMPdnNjet9'] = nRun_TTJetsSemiLepHDAMPdn * filtEff_TTJetsSemiLepNjet9HDAMPdn + nRun_TTJetsSemiLepHDAMPdnNjet9
nRun['TTJetsSemiLepHDAMPdnNjet9bin'] = nRun['TTJetsSemiLepHDAMPdnNjet9']
nRun['TTJetsSemiLepHDAMPupNjet0'] = nRun_TTJetsSemiLepHDAMPup * ( 1. - filtEff_TTJetsSemiLepNjet9HDAMPup ) 
nRun['TTJetsSemiLepHDAMPupNjet9'] = nRun_TTJetsSemiLepHDAMPup * filtEff_TTJetsSemiLepNjet9HDAMPup + nRun_TTJetsSemiLepHDAMPupNjet9
nRun['TTJetsSemiLepHDAMPupNjet9bin'] = nRun['TTJetsSemiLepHDAMPupNjet9']

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
#nRun['tttt'] = 849964.0 # from file TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_hadd.root
nRun['tttt'] = 3739493.0 # from file TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_correctnPartonsInBorn_hadd.root

nRun['X53LHM700'] = 300000.
nRun['X53RHM700'] = 297400.
nRun['X53LHM800'] = 295600.
nRun['X53RHM800'] = 299600.
nRun['X53LHM900'] = 300000. #old
nRun['X53RHM900'] = 281452.0
nRun['X53LHM1000'] = 293600.#old
nRun['X53RHM1000'] = 289224.0
nRun['X53LHM1100'] = 284174.0
nRun['X53RHM1100'] = 273508.0
nRun['X53LHM1200'] = 252566.0 
nRun['X53RHM1200'] = 275384.0
nRun['X53LHM1300'] = 300000. #old
nRun['X53RHM1300'] = 267170.0
nRun['X53LHM1400'] = 251084.0
nRun['X53RHM1400'] = 256020.0
nRun['X53LHM1500'] = 298400. #old
nRun['X53RHM1500'] = 240182.0
nRun['X53LHM1600'] = 300000. #old
nRun['X53RHM1600'] = 212304.0
nRun['X53LHM1700'] = 193068.0
nRun['X53RHM1700'] = 192194.0

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

xsec['TTJetsSemiLepUEdnNjet0'] = xsec['TTJets'] * BR_TTJetsSemiLep * ( 1. - filtEff_TTJetsSemiLepNjet9UEdn ) 
xsec['TTJetsSemiLepUEdnNjet9'] = xsec['TTJets'] * BR_TTJetsSemiLep * filtEff_TTJetsSemiLepNjet9UEdn
xsec['TTJetsSemiLepUEdnNjet9bin'] = xsec['TTJetsSemiLepUEdnNjet9']
xsec['TTJetsSemiLepUEupNjet0'] = xsec['TTJets'] * BR_TTJetsSemiLep * ( 1. - filtEff_TTJetsSemiLepNjet9UEup ) 
xsec['TTJetsSemiLepUEupNjet9'] = xsec['TTJets'] * BR_TTJetsSemiLep * filtEff_TTJetsSemiLepNjet9UEup
xsec['TTJetsSemiLepUEupNjet9bin'] = xsec['TTJetsSemiLepUEupNjet9']
xsec['TTJetsSemiLepHDAMPdnNjet0'] = xsec['TTJets'] * BR_TTJetsSemiLep * ( 1. - filtEff_TTJetsSemiLepNjet9HDAMPdn ) 
xsec['TTJetsSemiLepHDAMPdnNjet9'] = xsec['TTJets'] * BR_TTJetsSemiLep * filtEff_TTJetsSemiLepNjet9HDAMPdn
xsec['TTJetsSemiLepHDAMPdnNjet9bin'] = xsec['TTJetsSemiLepHDAMPdnNjet9']
xsec['TTJetsSemiLepHDAMPupNjet0'] = xsec['TTJets'] * BR_TTJetsSemiLep * ( 1. - filtEff_TTJetsSemiLepNjet9HDAMPup ) 
xsec['TTJetsSemiLepHDAMPupNjet9'] = xsec['TTJets'] * BR_TTJetsSemiLep * filtEff_TTJetsSemiLepNjet9HDAMPup
xsec['TTJetsSemiLepHDAMPupNjet9bin'] = xsec['TTJetsSemiLepHDAMPupNjet9']

xsec['Ts'] = 6.35*0.3259 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Tbs'] = 3.97*0.3259 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Tt'] = 136.02 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['Tbt'] = 80.95 # https://twiki.cern.ch/twiki/bin/view/LHCPhysics/SingleTopRefXsec
xsec['TtW'] = 35.85 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['TbtW'] = 35.85 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma

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
# xsec['DYMG100'] = 147.4*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG200'] = 40.99*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG400'] = 5.678*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG600'] = 1.367*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG800'] = 0.6304*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG1200'] = 0.1514*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
# xsec['DYMG2500'] = 0.003565*1.23 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns

xsec['DYMG100'] = 181.9209 # from OSDL in https://twiki.cern.ch/twiki/bin/view/CMS/FourTopCombination
xsec['DYMG200'] = 54.9330 # from OSDL in https://twiki.cern.ch/twiki/bin/view/CMS/FourTopCombination
xsec['DYMG400'] = 7.8581 # from OSDL in https://twiki.cern.ch/twiki/bin/view/CMS/FourTopCombination
xsec['DYMG600'] = 1.9477 # from OSDL in https://twiki.cern.ch/twiki/bin/view/CMS/FourTopCombination
xsec['DYMG800'] = 0.858682 # from OSDL in https://twiki.cern.ch/twiki/bin/view/CMS/FourTopCombination
xsec['DYMG1200'] = 0.202798 # from OSDL in https://twiki.cern.ch/twiki/bin/view/CMS/FourTopCombination
xsec['DYMG2500'] = 0.00321931 # from OSDL in https://twiki.cern.ch/twiki/bin/view/CMS/FourTopCombination

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

xsec['TTW'] = 0.55 # from Table 3 of https://arxiv.org/pdf/1812.08622.pdf (NLO + NNLL + EW)
xsec['TTZ'] = 0.86 # from Table 3 of https://arxiv.org/pdf/1812.08622.pdf (NLO + NNLL + EW)
xsec['TTH'] = 0.5269 # from XsecDB, NLO
xsec['TTWl'] = 0.55*0.3259 #= 0.1792 pb from Table 3 of https://arxiv.org/pdf/1812.08622.pdf (NLO + NNLL + EW) #0.2043 from McM
xsec['TTWq'] = 0.55*0.6741 #= 0.3708 pb from Table 3 of https://arxiv.org/pdf/1812.08622.pdf (NLO + NNLL + EW) #0.4062 from McM
xsec['TTZlM10'] = 0.86*3*(0.0337+0.0667) #=0.2589pb from Table 3 of https://arxiv.org/pdf/1812.08622.pdf (NLO + NNLL + EW) #0.2529 from McM
xsec['TTZlM1to10'] = 0.0532 # from McM
xsec['TTZq'] = 0.86*0.69911 #= 0.6012 pb from Table 3 of https://arxiv.org/pdf/1812.08622.pdf (NLO + NNLL + EW) #0.5297 from McM
xsec['TTHB'] = 0.2934 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#ttH
xsec['TTHnoB'] = 0.2151 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#ttH

xsec['TTTJ'] = 0.0004741 # from McM
xsec['TTTW'] = 0.0007330 # from McM
xsec['TTHH'] = 0.0007565 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD)
xsec['TTWH'] = 0.001582 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD)
xsec['TTZH'] = 0.001535 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD)
xsec['TTWW'] = 0.011500 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD 4f)
xsec['TTWZ'] = 0.003884 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD)
xsec['TTZZ'] = 0.001982 # from https://arxiv.org/pdf/1610.07922.pdf (NLO QCD)

#4 Tops
xsec['tttt'] = 0.012 # from https://arxiv.org/pdf/1711.02116.pdf, in McM: 0.008213

xsec['X53LHM700'] = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM700'] = 0.455 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM800'] = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM800'] = 0.196 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM900'] = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM900'] = 0.0903 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1000'] = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1000'] = 0.0440 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1100'] = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1100'] = 0.0224 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1200'] = 0.0118 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1300'] = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1300'] = 0.00639 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1400'] = 0.00354 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1500'] = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1500'] = 0.00200 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53RHM1600'] = 0.001148 # from https://twiki.cern.ch/twiki/bin/viewauth/CMS/B2GVHF#Full_NNLO_cross_sections_for_top
xsec['X53LHM1700'] = 0.000666
xsec['X53RHM1700'] = 0.000666

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

for flv in ['jj','cc','bb','1b','2b']:
	weight['TTJets2L2nuTT'+flv] = weight['TTJets2L2nu']
	weight['TTJetsHadTT'+flv] = weight['TTJetsHad']
	weight['TTJetsSemiLepTT'+flv] = weight['TTJetsSemiLep']
	weight['TTJetsSemiLepNjet0TT'+flv] = weight['TTJetsSemiLepNjet0']
	weight['TTJetsSemiLepNjet9TT'+flv] = weight['TTJetsSemiLepNjet9']
	weight['TTJetsSemiLepNjet9binTT'+flv] = weight['TTJetsSemiLepNjet9bin']
	for syst in ['UEdn','UEup','HDAMPdn','HDAMPup']:
		weight['TTJets2L2nu'+syst+'TT'+flv] = weight['TTJets2L2nu'+syst]
		weight['TTJetsHad'+syst+'TT'+flv] = weight['TTJetsHad'+syst]
		weight['TTJetsSemiLep'+syst+'TT'+flv] = weight['TTJetsSemiLep'+syst]
		weight['TTJetsSemiLep'+syst+'Njet0TT'+flv] = weight['TTJetsSemiLep'+syst+'Njet0']
		weight['TTJetsSemiLep'+syst+'Njet9TT'+flv] = weight['TTJetsSemiLep'+syst+'Njet9']
		weight['TTJetsSemiLep'+syst+'Njet9binTT'+flv] = weight['TTJetsSemiLep'+syst+'Njet9bin']

weight['TTJetsSemiLepNjet0TTjj1'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj2'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj3'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj4'] = weight['TTJetsSemiLepNjet0']
weight['TTJetsSemiLepNjet0TTjj5'] = weight['TTJetsSemiLepNjet0']

for sample in weight.keys():
        if 'TTJetsSemiLep' in sample and ('Njet0TT' in sample or 'Njet9TT' in sample):
                weight[sample.replace('TTJetsSemiLep','TTJetsSemiLepInc')] = weight[sample[:sample.find('Njet')]]

