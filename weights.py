#!/usr/bin/python

targetlumi = 41298. # 1/pb

# Number of processed MC events (before selections)
nRun={}
# new counts for 2017
nRun['TTJetsHad0'] = 130725364*0.8832
nRun['TTJetsHad700'] = 130725364*0.0921 + 39258853*0.442
nRun['TTJetsHad1000'] = 130725364*0.02474 + 14970062*0.442
nRun['TTJetsSemiLep0'] = 111325048*0.8832
nRun['TTJetsSemiLep700'] = 111325048*0.0921 + 39258853*0.405
nRun['TTJetsSemiLep1000'] = 111325048*0.02474 + 14970062*0.405
nRun['TTJets2L2nu0'] = 66979742*0.8832
nRun['TTJets2L2nu700'] = 66979742*0.0921 + 39258853*0.079
nRun['TTJets2L2nu1000'] = 66979742*0.02474 + 14970062*0.079
nRun['TTJetsPH700mtt'] = 39258853 + 130725364*0.0921 + 111325048*0.0921 + 66979742*0.0921
nRun['TTJetsPH1000mtt'] = 14970062 + 130725364*0.02474 + 111325048*0.02474 + 66979742*0.02474
nRun['Ts'] = 6179792. #from 9906720
nRun['Tt'] = 17743720.
nRun['Tbt']= 7690150.
nRun['TtW'] = 7660001.
nRun['TbtW'] = 7993682.
nRun['WJetsMG400'] = 14313274.#
nRun['WJetsMG600'] = 21709087.#
nRun['WJetsMG800'] = 20432728.#
nRun['WJetsMG1200']= 20258624.#
nRun['WJetsMG2500']= 21495421.#
nRun['DY'] = 123584520. # from 182359896, this is the ext1 sample
nRun['QCDht300'] = 60316577.#
nRun['QCDht500'] = 54624037.#
nRun['QCDht700'] = 47724800.#
nRun['QCDht1000'] = 16595628.#
nRun['QCDht1500'] = 11634434.#
nRun['QCDht2000'] = 5941306.#
nRun['TTWl'] = 2692366. #from 4919674
nRun['TTZl'] = 131210. #from 250000

# not updated for 2017
#Do NGen*[1-2X], where X is the neg event fraction calculated from the jobs completed! 
#A = P - N = F - 2*N   A/F = 1 - 2*(N/F)  N/F = (1 - A/F)/2
nRun['TTJets'] = 14188545. #need negative counts
nRun['WJets'] = 6776900. # from 9908534.
nRun['WJetsMG'] = 86731806. 
nRun['WJetsMG100'] = 79356685.
nRun['WJetsMG200'] = 39680891.
nRun['WJetsPt100'] = 120124110.*(1.-2.*0.32) #Full =120124110, neg frac 0.32
nRun['WJetsPt250'] = 12022587.*(1.-2.*0.31555) #Full = 12022587, neg frac 0.31555 
nRun['WJetsPt400'] = 1939947.*(1.-2.*0.30952) #Full = 1939947, neg frac 0.30952
nRun['WJetsPt600'] = 1974619.*(1.-2.*0.29876) #Full = 1974619, neg frac 0.29876
nRun['DYMG'] = 96658943.  # just ext2, could get bigger
nRun['DYMG100'] = 10607207.
nRun['DYMG200'] = 9653731.
nRun['DYMG400'] = 10008776.
nRun['DYMG600'] = 8292957.
nRun['DYMG800'] = 2668730.
nRun['DYMG1200']= 596079.
nRun['DYMG2500']=  399492.
nRun['WW'] = 7981136.-494070. # couldn't run file #2 because one of the files was deleted...
nRun['WZ'] = 3995828.
nRun['ZZ'] = 1988098.
nRun['QCDht100'] = 80684349.
nRun['QCDht200'] = 57580393.
nRun['TTWq'] = 430310. #from 833298
nRun['TTZq'] = 351164. #from 749400

## values with # are updated for 2017
nRun['4TM690'] = 1000000.

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
# new ttbar splitting in 2017
xsec['TTJetsHad0'] = 831.76*0.8832*0.442
xsec['TTJetsHad700'] = 831.76*0.0921*0.442
xsec['TTJetsHad1000'] = 831.76*0.02474*0.442
xsec['TTJetsSemiLep0'] = 831.76*0.8832*0.405
xsec['TTJetsSemiLep700'] = 831.76*0.0921*0.405
xsec['TTJetsSemiLep1000'] = 831.76*0.02474*0.405
xsec['TTJets2L2nu0'] = 831.76*0.8832*0.079
xsec['TTJets2L2nu700'] = 831.76*0.0921*0.079
xsec['TTJets2L2nu1000'] = 831.76*0.02474*0.079
xsec['TTJetsPH700mtt'] = 831.76*0.0921 #(xsec*filtering coeff.)
xsec['TTJetsPH1000mtt'] = 831.76*0.02474 #(xsec*filtering coeff.)

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
xsec['WW'] = 118.7 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/StandardModelCrossSectionsat13TeVInclusive
xsec['WZ'] = 47.13 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
xsec['ZZ'] = 16.523 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SummaryTable1G25ns#Diboson
xsec['TTZl'] = 0.2529 # from McM
xsec['TTZq'] = 0.5297 # from McM
xsec['TTWl'] = 0.2043 # from McM
xsec['TTWq'] = 0.4062 # from McM
xsec['Tt'] = 136.02 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['Tbt'] = 80.95 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['Ts'] = 11.36/3 #(1/3 was suggested by Thomas Peiffer to account for the leptonic branching ratio)# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['TtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['TbtW'] = 35.83 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma

xsec['4TM690'] = 1.

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
	weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])
