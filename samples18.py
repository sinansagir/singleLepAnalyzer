#!/usr/bin/python

samples = {
'DataE':'EGamma',
'DataM':'SingleMuon',
'DataJ':'JetHT',

#'tttt':'TTTT_TuneCP5_13TeV-amcatnlo-pythia8',
#'tttt':'TTTT_TuneCP5_13TeV-amcatnlo-pythia8_ext',
'tttt':'TTTT_TuneCP5_13TeV-amcatnlo-pythia8_combined',

'X53LHM900':'X53X53_M-900_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1000':'X53X53_M-1000_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1100':'X53X53_M-1100_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1200':'X53X53_M-1200_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1300':'X53X53_M-1300_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1400':'X53X53_M-1400_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1500':'X53X53_M-1500_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1600':'X53X53_M-1600_LH_TuneCP5_13TeV-madgraph-pythia8',
'X53LHM1700':'X53X53_M-1700_LH_TuneCP5_13TeV-madgraph-pythia8',

'X53RHM900':'X53X53_M-900_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1000':'X53X53_M-1000_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1100':'X53X53_M-1100_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1200':'X53X53_M-1200_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1300':'X53X53_M-1300_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1400':'X53X53_M-1400_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1500':'X53X53_M-1500_RH_TuneCP5_13TeV-madgraph-pythia8',  
'X53RHM1600':'X53X53_M-1600_RH_TuneCP5_13TeV-madgraph-pythia8',
'X53RHM1700':'X53X53_M-1700_RH_TuneCP5_13TeV-madgraph-pythia8',

'DYMG200':'DYJetsToLL_M-50_HT-200to400_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
'DYMG400':'DYJetsToLL_M-50_HT-400to600_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
'DYMG600':'DYJetsToLL_M-50_HT-600to800_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
'DYMG800':'DYJetsToLL_M-50_HT-800to1200_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
'DYMG1200':'DYJetsToLL_M-50_HT-1200to2500_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',
'DYMG2500':'DYJetsToLL_M-50_HT-2500toInf_TuneCP5_PSweights_13TeV-madgraphMLM-pythia8',

'WJetsMG200':'WJetsToLNu_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG400':'WJetsToLNu_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG600':'WJetsToLNu_HT-600To800_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG800':'WJetsToLNu_HT-800To1200_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG1200':'WJetsToLNu_HT-1200To2500_TuneCP5_13TeV-madgraphMLM-pythia8',
'WJetsMG2500':'WJetsToLNu_HT-2500ToInf_TuneCP5_13TeV-madgraphMLM-pythia8',

'WW':'WW_TuneCP5_PSweights_13TeV-pythia8',
'WZ':'WZ_TuneCP5_PSweights_13TeV-pythia8',
'ZZ':'ZZ_TuneCP5_13TeV-pythia8',

'TTJets2L2nuTT1b':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_tt1b',
'TTJets2L2nuTT2b':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_tt2b',
'TTJets2L2nuTTbb':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_ttbb',
'TTJets2L2nuTTcc':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_ttcc',
'TTJets2L2nuTTjj':'TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8_ttjj',
'TTJetsHadTT1b':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tt1b',
'TTJetsHadTT2b':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_tt2b',
'TTJetsHadTTbb':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ttbb',
'TTJetsHadTTcc':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ttcc',
'TTJetsHadTTjj':'TTToHadronic_TuneCP5_13TeV-powheg-pythia8_ttjj',
'TTJetsSemiLepNjet9binTT1b':'TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_tt1b',
'TTJetsSemiLepNjet9binTT2b':'TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_tt2b',
'TTJetsSemiLepNjet9binTTbb':'TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_ttbb',
'TTJetsSemiLepNjet9binTTcc':'TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_ttcc',
'TTJetsSemiLepNjet9binTTjj':'TTToSemiLepton_HT500Njet9_TuneCP5_13TeV-powheg-pythia8_ttjj',
'TTJetsSemiLepNjet0TT1b':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt1b',
'TTJetsSemiLepNjet0TT2b':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt2b',
'TTJetsSemiLepNjet0TTbb':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttbb',
'TTJetsSemiLepNjet0TTcc':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttcc',
'TTJetsSemiLepNjet0TTjj1':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_1',
'TTJetsSemiLepNjet0TTjj2':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj_2',
'TTJetsSemiLepNjet9TT1b':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_tt1b',
'TTJetsSemiLepNjet9TT2b':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_tt2b',
'TTJetsSemiLepNjet9TTbb':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttbb',
'TTJetsSemiLepNjet9TTcc':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttcc',
'TTJetsSemiLepNjet9TTjj':'TTToSemiLeptonic_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttjj',

'TTJets2L2nuUEdnTT1b':'TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8_tt1b',
'TTJets2L2nuUEdnTT2b':'TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8_tt2b',
'TTJets2L2nuUEdnTTbb':'TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8_ttbb',
'TTJets2L2nuUEdnTTcc':'TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8_ttcc',
'TTJets2L2nuUEdnTTjj':'TTTo2L2Nu_TuneCP5down_13TeV-powheg-pythia8_ttjj',
'TTJets2L2nuUEupTT1b':'TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8_tt1b',
'TTJets2L2nuUEupTT2b':'TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8_tt2b',
'TTJets2L2nuUEupTTbb':'TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8_ttbb',
'TTJets2L2nuUEupTTcc':'TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8_ttcc',
'TTJets2L2nuUEupTTjj':'TTTo2L2Nu_TuneCP5up_13TeV-powheg-pythia8_ttjj',
'TTJets2L2nuHDAMPdnTT1b':'TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_tt1b',
'TTJets2L2nuHDAMPdnTT2b':'TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_tt2b',
'TTJets2L2nuHDAMPdnTTbb':'TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttbb',
'TTJets2L2nuHDAMPdnTTcc':'TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttcc',
'TTJets2L2nuHDAMPdnTTjj':'TTTo2L2Nu_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttjj',
'TTJets2L2nuHDAMPupTT1b':'TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8_tt1b',
'TTJets2L2nuHDAMPupTT2b':'TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8_tt2b',
'TTJets2L2nuHDAMPupTTbb':'TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttbb',
'TTJets2L2nuHDAMPupTTcc':'TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttcc',
'TTJets2L2nuHDAMPupTTjj':'TTTo2L2Nu_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttjj',

'TTJetsHadUEdnTT1b':'TTToHadronic_TuneCP5down_13TeV-powheg-pythia8_tt1b',
'TTJetsHadUEdnTT2b':'TTToHadronic_TuneCP5down_13TeV-powheg-pythia8_tt2b',
'TTJetsHadUEdnTTbb':'TTToHadronic_TuneCP5down_13TeV-powheg-pythia8_ttbb',
'TTJetsHadUEdnTTcc':'TTToHadronic_TuneCP5down_13TeV-powheg-pythia8_ttcc',
'TTJetsHadUEdnTTjj':'TTToHadronic_TuneCP5down_13TeV-powheg-pythia8_ttjj',
'TTJetsHadUEupTT1b':'TTToHadronic_TuneCP5up_13TeV-powheg-pythia8_tt1b',
'TTJetsHadUEupTT2b':'TTToHadronic_TuneCP5up_13TeV-powheg-pythia8_tt2b',
'TTJetsHadUEupTTbb':'TTToHadronic_TuneCP5up_13TeV-powheg-pythia8_ttbb',
'TTJetsHadUEupTTcc':'TTToHadronic_TuneCP5up_13TeV-powheg-pythia8_ttcc',
'TTJetsHadUEupTTjj':'TTToHadronic_TuneCP5up_13TeV-powheg-pythia8_ttjj',
'TTJetsHadHDAMPdnTT1b':'TTToHadronic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_tt1b',
'TTJetsHadHDAMPdnTT2b':'TTToHadronic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_tt2b',
'TTJetsHadHDAMPdnTTbb':'TTToHadronic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttbb',
'TTJetsHadHDAMPdnTTcc':'TTToHadronic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttcc',
'TTJetsHadHDAMPdnTTjj':'TTToHadronic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttjj',
'TTJetsHadHDAMPupTT1b':'TTToHadronic_hdampUP_TuneCP5_13TeV-powheg-pythia8_tt1b',
'TTJetsHadHDAMPupTT2b':'TTToHadronic_hdampUP_TuneCP5_13TeV-powheg-pythia8_tt2b',
'TTJetsHadHDAMPupTTbb':'TTToHadronic_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttbb',
'TTJetsHadHDAMPupTTcc':'TTToHadronic_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttcc',
'TTJetsHadHDAMPupTTjj':'TTToHadronic_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttjj',

'TTJetsSemiLepUEdnTT1b':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_tt1b',
'TTJetsSemiLepUEdnTT2b':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_tt2b',
'TTJetsSemiLepUEdnTTbb':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_ttbb',
'TTJetsSemiLepUEdnTTcc':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_ttcc',
'TTJetsSemiLepUEdnTTjj':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_ttjj',
'TTJetsSemiLepUEupTT1b':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_tt1b',
'TTJetsSemiLepUEupTT2b':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_tt2b',
'TTJetsSemiLepUEupTTbb':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_ttbb',
'TTJetsSemiLepUEupTTcc':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_ttcc',
'TTJetsSemiLepUEupTTjj':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_ttjj',
'TTJetsSemiLepHDAMPdnTT1b':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_tt1b',
'TTJetsSemiLepHDAMPdnTT2b':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_tt2b',
'TTJetsSemiLepHDAMPdnTTbb':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttbb',
'TTJetsSemiLepHDAMPdnTTcc':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttcc',
'TTJetsSemiLepHDAMPdnTTjj':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttjj',
'TTJetsSemiLepHDAMPupTT1b':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_tt1b',
'TTJetsSemiLepHDAMPupTT2b':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_tt2b',
'TTJetsSemiLepHDAMPupTTbb':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttbb',
'TTJetsSemiLepHDAMPupTTcc':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttcc',
'TTJetsSemiLepHDAMPupTTjj':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttjj',

'TTJetsSemiLepUEdnNjet9binTT1b':'TTToSemiLepton_HT500Njet9_TuneCP5down_13TeV-powheg-pythia8_tt1b',
'TTJetsSemiLepUEdnNjet9binTT2b':'TTToSemiLepton_HT500Njet9_TuneCP5down_13TeV-powheg-pythia8_tt2b',
'TTJetsSemiLepUEdnNjet9binTTbb':'TTToSemiLepton_HT500Njet9_TuneCP5down_13TeV-powheg-pythia8_ttbb',
'TTJetsSemiLepUEdnNjet9binTTcc':'TTToSemiLepton_HT500Njet9_TuneCP5down_13TeV-powheg-pythia8_ttcc',
'TTJetsSemiLepUEdnNjet9binTTjj':'TTToSemiLepton_HT500Njet9_TuneCP5down_13TeV-powheg-pythia8_ttjj',
'TTJetsSemiLepUEdnNjet0TT1b':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_HT0Njet0_tt1b',
'TTJetsSemiLepUEdnNjet0TT2b':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_HT0Njet0_tt2b',
'TTJetsSemiLepUEdnNjet0TTbb':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_HT0Njet0_ttbb',
'TTJetsSemiLepUEdnNjet0TTcc':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_HT0Njet0_ttcc',
'TTJetsSemiLepUEdnNjet0TTjj':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_HT0Njet0_ttjj',
'TTJetsSemiLepUEdnNjet9TT1b':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_HT500Njet9_tt1b',
'TTJetsSemiLepUEdnNjet9TT2b':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_HT500Njet9_tt2b',
'TTJetsSemiLepUEdnNjet9TTbb':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_HT500Njet9_ttbb',
'TTJetsSemiLepUEdnNjet9TTcc':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_HT500Njet9_ttcc',
'TTJetsSemiLepUEdnNjet9TTjj':'TTToSemiLeptonic_TuneCP5down_13TeV-powheg-pythia8_HT500Njet9_ttjj',

'TTJetsSemiLepUEupNjet9binTT1b':'TTToSemiLepton_HT500Njet9_TuneCP5up_13TeV-powheg-pythia8_tt1b',
'TTJetsSemiLepUEupNjet9binTT2b':'TTToSemiLepton_HT500Njet9_TuneCP5up_13TeV-powheg-pythia8_tt2b',
'TTJetsSemiLepUEupNjet9binTTbb':'TTToSemiLepton_HT500Njet9_TuneCP5up_13TeV-powheg-pythia8_ttbb',
'TTJetsSemiLepUEupNjet9binTTcc':'TTToSemiLepton_HT500Njet9_TuneCP5up_13TeV-powheg-pythia8_ttcc',
'TTJetsSemiLepUEupNjet9binTTjj':'TTToSemiLepton_HT500Njet9_TuneCP5up_13TeV-powheg-pythia8_ttjj',
'TTJetsSemiLepUEupNjet0TT1b':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_HT0Njet0_tt1b',
'TTJetsSemiLepUEupNjet0TT2b':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_HT0Njet0_tt2b',
'TTJetsSemiLepUEupNjet0TTbb':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_HT0Njet0_ttbb',
'TTJetsSemiLepUEupNjet0TTcc':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_HT0Njet0_ttcc',
'TTJetsSemiLepUEupNjet0TTjj':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_HT0Njet0_ttjj',
'TTJetsSemiLepUEupNjet9TT1b':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_HT500Njet9_tt1b',
'TTJetsSemiLepUEupNjet9TT2b':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_HT500Njet9_tt2b',
'TTJetsSemiLepUEupNjet9TTbb':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_HT500Njet9_ttbb',
'TTJetsSemiLepUEupNjet9TTcc':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_HT500Njet9_ttcc',
'TTJetsSemiLepUEupNjet9TTjj':'TTToSemiLeptonic_TuneCP5up_13TeV-powheg-pythia8_HT500Njet9_ttjj',

'TTJetsSemiLepHDAMPdnNjet9binTT1b':'TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_tt1b',
'TTJetsSemiLepHDAMPdnNjet9binTT2b':'TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_tt2b',
'TTJetsSemiLepHDAMPdnNjet9binTTbb':'TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttbb',
'TTJetsSemiLepHDAMPdnNjet9binTTcc':'TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttcc',
'TTJetsSemiLepHDAMPdnNjet9binTTjj':'TTToSemiLepton_HT500Njet9_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_ttjj',
'TTJetsSemiLepHDAMPdnNjet0TT1b':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt1b',
'TTJetsSemiLepHDAMPdnNjet0TT2b':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt2b',
'TTJetsSemiLepHDAMPdnNjet0TTbb':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttbb',
'TTJetsSemiLepHDAMPdnNjet0TTcc':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttcc',
'TTJetsSemiLepHDAMPdnNjet0TTjj':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj',
'TTJetsSemiLepHDAMPdnNjet9TT1b':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_tt1b',
'TTJetsSemiLepHDAMPdnNjet9TT2b':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_tt2b',
'TTJetsSemiLepHDAMPdnNjet9TTbb':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttbb',
'TTJetsSemiLepHDAMPdnNjet9TTcc':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttcc',
'TTJetsSemiLepHDAMPdnNjet9TTjj':'TTToSemiLeptonic_hdampDOWN_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttjj',

'TTJetsSemiLepHDAMPupNjet9binTT1b':'TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_13TeV-powheg-pythia8_tt1b',
'TTJetsSemiLepHDAMPupNjet9binTT2b':'TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_13TeV-powheg-pythia8_tt2b',
'TTJetsSemiLepHDAMPupNjet9binTTbb':'TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttbb',
'TTJetsSemiLepHDAMPupNjet9binTTcc':'TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttcc',
'TTJetsSemiLepHDAMPupNjet9binTTjj':'TTToSemiLepton_HT500Njet9_hdampUP_TuneCP5_13TeV-powheg-pythia8_ttjj',
'TTJetsSemiLepHDAMPupNjet0TT1b':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt1b',
'TTJetsSemiLepHDAMPupNjet0TT2b':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_tt2b',
'TTJetsSemiLepHDAMPupNjet0TTbb':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttbb',
'TTJetsSemiLepHDAMPupNjet0TTcc':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttcc',
'TTJetsSemiLepHDAMPupNjet0TTjj':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_HT0Njet0_ttjj',
'TTJetsSemiLepHDAMPupNjet9TT1b':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_tt1b',
'TTJetsSemiLepHDAMPupNjet9TT2b':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_tt2b',
'TTJetsSemiLepHDAMPupNjet9TTbb':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttbb',
'TTJetsSemiLepHDAMPupNjet9TTcc':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttcc',
'TTJetsSemiLepHDAMPupNjet9TTjj':'TTToSemiLeptonic_hdampUP_TuneCP5_13TeV-powheg-pythia8_HT500Njet9_ttjj',

'Ts':'ST_s-channel_4f_leptonDecays_TuneCP5_13TeV-madgraph-pythia8',
# 'Ts':'ST_s-channel_top_leptonDecays_13TeV-PSweights_powheg-pythia',
'Tbs':'ST_s-channel_antitop_leptonDecays_13TeV-PSweights_powheg-pythia',
'Tt':'ST_t-channel_top_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8',
'Tbt':'ST_t-channel_antitop_4f_InclusiveDecays_TuneCP5_13TeV-powheg-madspin-pythia8',
'TtW':'ST_tW_top_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',
'TbtW':'ST_tW_antitop_5f_inclusiveDecays_TuneCP5_13TeV-powheg-pythia8',

'TTHH':'TTHH_TuneCP5_13TeV-madgraph-pythia8',
'TTTJ':'TTTJ_TuneCP5_13TeV-madgraph-pythia8',
'TTTW':'TTTW_TuneCP5_13TeV-madgraph-pythia8',
'TTWH':'TTWH_TuneCP5_13TeV-madgraph-pythia8',
'TTWW':'TTWW_TuneCP5_13TeV-madgraph-pythia8',
'TTWZ':'TTWZ_TuneCP5_13TeV-madgraph-pythia8',
'TTZH':'TTZH_TuneCP5_13TeV-madgraph-pythia8',
'TTZZ':'TTZZ_TuneCP5_13TeV-madgraph-pythia8',
'TTWl':'TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8',
'TTWq':'TTWJetsToQQ_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8', # MISSING IN OCT2019 PRODUCTION
'TTZlM10':'TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8',
'TTZlM1to10':'TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8',
'TTHB':'ttHTobb_M125_TuneCP5_13TeV-powheg-pythia8',
'TTHnoB':'ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8',

'QCDht200':'QCD_HT200to300_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCDht300':'QCD_HT300to500_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCDht500':'QCD_HT500to700_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCDht700':'QCD_HT700to1000_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCDht1000':'QCD_HT1000to1500_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCDht1500':'QCD_HT1500to2000_TuneCP5_13TeV-madgraphMLM-pythia8',
'QCDht2000':'QCD_HT2000toInf_TuneCP5_13TeV-madgraphMLM-pythia8',
}

for sample in samples.keys():
        if 'TTJetsSemiLep' in sample and ('Njet0TT' in sample or 'Njet9TT' in sample):
                samples[sample.replace('TTJetsSemiLep','TTJetsSemiLepInc')] = samples[sample]
