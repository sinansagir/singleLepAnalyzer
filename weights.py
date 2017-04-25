#!/usr/bin/python

targetlumi = 35867. # 1/pb

genHTweight={}
genHTweight['WJetsHT100'] = 0.998056#https://github.com/jmhogan/GenHTweight/blob/master/WJetsToLNuSFs.txt
genHTweight['WJetsHT200'] = 0.978569
genHTweight['WJetsHT400'] = 0.928054
genHTweight['WJetsHT600'] = 0.856705
genHTweight['WJetsHT800'] = 0.757463
genHTweight['WJetsHT1200']= 0.608292
genHTweight['WJetsHT2500']= 0.454246

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
nRun['TTJets'] = 14188545. #need negative counts
nRun['TTJetsPH'] = 77229341.+78006311. #original+backup
for ind in range(1,12): nRun['TTJetsPH_'+str(ind)]=nRun['TTJetsPH']
nRun['TTJetsPHSL'] = 152720952.
for ind in range(1,14): nRun['TTJetsPHSL_'+str(ind)] = nRun['TTJetsPHSL']
nRun['TTJetsPH0to700inc'] = nRun['TTJetsPH']
for ind in range(1,12): nRun['TTJetsPH0to700inc_'+str(ind)]=nRun['TTJetsPH']
nRun['TTJetsPH700to1000inc'] = nRun['TTJetsPH']*0.0921 + 38578334.
nRun['TTJetsPH1000toINFinc'] = nRun['TTJetsPH']*0.02474 + 24561633.
nRun['TTJetsPH700mtt'] = nRun['TTJetsPH700to1000inc']
nRun['TTJetsPH1000mtt'] = nRun['TTJetsPH1000toINFinc']
nRun['TTJetsPH2L'] = 79092400.
nRun['Ts'] = 622990. #from 1000000
nRun['Tt'] = 67240808.
nRun['Tbt']= 38811017.
nRun['TtW'] = 6952830.
nRun['TbtW'] = 6933094.
nRun['WJets'] = 6776900. # from 9908534.
nRun['WJetsMG'] = 86731806. 
nRun['WJetsHT100'] = 79356685.
nRun['WJetsHT200'] = 39680891.
nRun['WJetsHT400'] = 7759701.
nRun['WJetsHT600'] = 18687480.
nRun['WJetsHT800'] = 7745467.
nRun['WJetsHT1200']= 6872441.
nRun['WJetsHT2500']= 2637821.
#Do NGen*[1-2X], where X is the neg event fraction calculated from the jobs completed! 
#A = P - N = F - 2*N   A/F = 1 - 2*(N/F)  N/F = (1 - A/F)/2
nRun['WJetsPt100'] = 120124110.*(1.-2.*0.32) #Full =120124110, neg frac 0.32
nRun['WJetsPt250'] = 12022587.*(1.-2.*0.31555) #Full = 12022587, neg frac 0.31555 
nRun['WJetsPt400'] = 1939947.*(1.-2.*0.30952) #Full = 1939947, neg frac 0.30952
nRun['WJetsPt600'] = 1974619.*(1.-2.*0.29876) #Full = 1974619, neg frac 0.29876
nRun['DY'] = 19223750. # from 28696958
nRun['DYMG'] = 96658943.
nRun['DYMG100'] = 10607207.
nRun['DYMG200'] = 9653731.
nRun['DYMG400'] = 10008776.
nRun['DYMG600'] = 8292957.
nRun['DYMG800'] = 2668730.
nRun['DYMG1200']= 596079.
nRun['DYMG2500']= 399492.
nRun['WW'] = 7981136. 
nRun['WZ'] = 3995828.
nRun['ZZ'] = 1988098.
nRun['QCDht100'] = 80684349.
nRun['QCDht200'] = 57580393.
nRun['QCDht300'] = 54537903.
nRun['QCDht500'] = 62271343.
nRun['QCDht700'] = 45412780.
nRun['QCDht1000'] = 15127293.
nRun['QCDht1500'] = 11826702.
nRun['QCDht2000'] = 6039005.
nRun['TTWl'] = 2716249. #from 5280565
nRun['TTWq'] = 430310. #from 833298
nRun['TTZl'] = 927976. #from 1992438
nRun['TTZq'] = 351164. #from 749400
nRun['TTG']  = 4777013. #from 14756259

nRun['TTTT'] = 1023172. #from 2456040
nRun['VHnonbb'] = 461452. #from 1007898
nRun['WHbb'] = 1279827. #from 2179687
nRun['WWW'] = 210538. #from 240000
nRun['WWZ'] = 221468. #from 250000
nRun['WZZ'] = 216366. #from 246800
nRun['ZZZ'] = 213197. #from 249237
nRun['WWllnn'] = 1999000. 
nRun['WWlnqq'] = 1999200.+6998600. 
nRun['WZlnqq'] = 14057875. #from 24221923
nRun['WZlnnn'] = 942046. #from 1703772
nRun['WZllqq'] = 15879472. #from 26517272
nRun['WZllln'] = 1993200.
nRun['ZZllnn'] = 8842475.
nRun['ZZllqq'] = 9688612. #from 15345572
nRun['ZZllll'] = 6669988.
nRun['tZq'] = 3846170. #from 14509520
nRun['ttHbb'] = 2910760. #from 9794226
nRun['ttHnonbb'] = 3905798. #from 3981250

nRun['Hptb180'] = 404688. #Ngen=1499270
nRun['Hptb200'] = 400501. #Ngen=1473805
nRun['Hptb220'] = 402569. #Ngen=1499361 
nRun['Hptb250'] = 395891. #Ngen=1491475
nRun['Hptb300'] = 390646. #Ngen=1497522
nRun['Hptb350'] = 390221. #Ngen=1496373
nRun['Hptb400'] = 387746. #Ngen=1496088
nRun['Hptb450'] = 379926. #Ngen=1488753 CHECK NEG COUNT in MORIOND17!!!!! Sample not available yet
nRun['Hptb500'] = 400004. #Ngen=1500000
nRun['Hptb750'] = 377320. #Ngen=1488753 CHECK NEG COUNT in MORIOND17!!!!! Sample not available yet
nRun['Hptb800'] = 376326. #Ngen=1494646
nRun['Hptb1000'] = 376708. #Ngen=1491600
nRun['Hptb2000'] = 373174. #Ngen=1500000
nRun['Hptb3000'] = 377717. #Ngen=1497017

nRun['TTM700BWBW'] = 798600.0*0.333*0.333 #not used
nRun['TTM800BWBW'] = 766000.0*0.333*0.333
nRun['TTM900BWBW'] = 828000.0*0.333*0.333
nRun['TTM1000BWBW'] = 832200.0*0.333*0.333
nRun['TTM1100BWBW'] = 816400.0*0.333*0.333
nRun['TTM1200BWBW'] = 828600.0*0.333*0.333
nRun['TTM1300BWBW'] = 824000.0*0.333*0.333
nRun['TTM1400BWBW'] = 810000.0*0.333*0.333
nRun['TTM1500BWBW'] = 828200.0*0.333*0.333
nRun['TTM1600BWBW'] = 111800.0*0.333*0.333
nRun['TTM1700BWBW'] = 795000.0*0.333*0.333
nRun['TTM1800BWBW'] = 812400.0*0.333*0.333
nRun['TTM700THBW'] = 798600.0*0.333*0.333*2 #not used
nRun['TTM800THBW'] = 766000.0*0.333*0.333*2
nRun['TTM900THBW'] = 828000.0*0.333*0.333*2
nRun['TTM1000THBW'] = 832200*0.333*0.333*2
nRun['TTM1100THBW'] = 816400.0*0.333*0.333*2
nRun['TTM1200THBW'] = 828600.0*0.333*0.333*2
nRun['TTM1300THBW'] = 824000.0*0.333*0.333*2
nRun['TTM1400THBW'] = 810000.0*0.333*0.333*2
nRun['TTM1500THBW'] = 828200.0*0.333*0.333*2
nRun['TTM1600THBW'] = 111800.0*0.333*0.333*2
nRun['TTM1700THBW'] = 795000.0*0.333*0.333*2
nRun['TTM1800THBW'] = 812400.0*0.333*0.333*2
nRun['TTM700TZBW'] = 798600.0*0.333*0.333*2 #not used
nRun['TTM800TZBW'] = 766000.0*0.333*0.333*2
nRun['TTM900TZBW'] = 828000.0*0.333*0.333*2
nRun['TTM1000TZBW'] = 832200*0.333*0.333*2
nRun['TTM1100TZBW'] = 816400.0*0.333*0.333*2
nRun['TTM1200TZBW'] = 828600.0*0.333*0.333*2
nRun['TTM1300TZBW'] = 824000.0*0.333*0.333*2
nRun['TTM1400TZBW'] = 810000.0*0.333*0.333*2
nRun['TTM1500TZBW'] = 828200.0*0.333*0.333*2
nRun['TTM1600TZBW'] = 111800.0*0.333*0.333*2
nRun['TTM1700TZBW'] = 795000.0*0.333*0.333*2
nRun['TTM1800TZBW'] = 812400.0*0.333*0.333*2
nRun['TTM700TZTZ'] = 798600.0*0.333*0.333 #not used
nRun['TTM800TZTZ'] = 766000.0*0.333*0.333
nRun['TTM900TZTZ'] = 828000.0*0.333*0.333
nRun['TTM1000TZTZ'] = 832200*0.333*0.333
nRun['TTM1100TZTZ'] = 816400.0*0.333*0.333
nRun['TTM1200TZTZ'] = 828600.0*0.333*0.333
nRun['TTM1300TZTZ'] = 824000.0*0.333*0.333
nRun['TTM1400TZTZ'] = 810000.0*0.333*0.333
nRun['TTM1500TZTZ'] = 828200.0*0.333*0.333
nRun['TTM1600TZTZ'] = 111800.0*0.333*0.333
nRun['TTM1700TZTZ'] = 795000.0*0.333*0.333
nRun['TTM1800TZTZ'] = 812400.0*0.333*0.333
nRun['TTM700TZTH'] = 798600.0*0.333*0.333*2 #not used
nRun['TTM800TZTH'] = 766000.0*0.333*0.333*2
nRun['TTM900TZTH'] = 828000.0*0.333*0.333*2
nRun['TTM1000TZTH'] = 832200*0.333*0.333*2
nRun['TTM1100TZTH'] = 816400.0*0.333*0.333*2
nRun['TTM1200TZTH'] = 828600.0*0.333*0.333*2
nRun['TTM1300TZTH'] = 824000.0*0.333*0.333*2
nRun['TTM1400TZTH'] = 810000.0*0.333*0.333*2
nRun['TTM1500TZTH'] = 828200.0*0.333*0.333*2
nRun['TTM1600TZTH'] = 111800.0*0.333*0.333*2
nRun['TTM1700TZTH'] = 795000.0*0.333*0.333*2
nRun['TTM1800TZTH'] = 812400.0*0.333*0.333*2
nRun['TTM700THTH'] = 798600.0*0.333*0.333 #not used
nRun['TTM800THTH'] = 766000.0*0.333*0.333
nRun['TTM900THTH'] = 828000.0*0.333*0.333
nRun['TTM1000THTH'] = 832200*0.333*0.333
nRun['TTM1100THTH'] = 816400.0*0.333*0.333
nRun['TTM1200THTH'] = 828600.0*0.333*0.333
nRun['TTM1300THTH'] = 824000.0*0.333*0.333
nRun['TTM1400THTH'] = 810000.0*0.333*0.333
nRun['TTM1500THTH'] = 828200.0*0.333*0.333
nRun['TTM1600THTH'] = 111800.0*0.333*0.333
nRun['TTM1700THTH'] = 795000.0*0.333*0.333
nRun['TTM1800THTH'] = 812400.0*0.333*0.333

nRun['BBM700TWTW'] = 814800.0*0.333*0.333
nRun['BBM800TWTW'] = 826200.0*0.333*0.333
nRun['BBM900TWTW'] = 799800.0*0.333*0.333
nRun['BBM1000TWTW'] = 825600.0*0.333*0.333
nRun['BBM1100TWTW'] = 832000.0*0.333*0.333
nRun['BBM1200TWTW'] = 832200.0*0.333*0.333
nRun['BBM1300TWTW'] = 807200.0*0.333*0.333
nRun['BBM1400TWTW'] = 816800.0*0.333*0.333
nRun['BBM1500TWTW'] = 831000.0*0.333*0.333
nRun['BBM1600TWTW'] = 696600.0*0.333*0.333
nRun['BBM1700TWTW'] = 832600.0*0.333*0.333
nRun['BBM1800TWTW'] = 795400.0*0.333*0.333
nRun['BBM700BHTW'] = 814800.0*0.333*0.333*2
nRun['BBM800BHTW'] = 826200.0*0.333*0.333*2
nRun['BBM900BHTW'] = 799800.0*0.333*0.333*2
nRun['BBM1000BHTW'] = 825600.0*0.333*0.333*2
nRun['BBM1100BHTW'] = 832000.0*0.333*0.333*2
nRun['BBM1200BHTW'] = 832200.0*0.333*0.333*2
nRun['BBM1300BHTW'] = 807200.0*0.333*0.333*2
nRun['BBM1400BHTW'] = 816800.0*0.333*0.333*2
nRun['BBM1500BHTW'] = 831000.0*0.333*0.333*2
nRun['BBM1600BHTW'] = 696600.0*0.333*0.333*2
nRun['BBM1700BHTW'] = 832600.0*0.333*0.333*2
nRun['BBM1800BHTW'] = 795400.0*0.333*0.333*2
nRun['BBM700BZTW'] = 814800.0*0.333*0.333*2
nRun['BBM800BZTW'] = 826200.0*0.333*0.333*2
nRun['BBM900BZTW'] = 799800.0*0.333*0.333*2
nRun['BBM1000BZTW'] = 825600.0*0.333*0.333*2
nRun['BBM1100BZTW'] = 832000.0*0.333*0.333*2
nRun['BBM1200BZTW'] = 832200.0*0.333*0.333*2
nRun['BBM1300BZTW'] = 807200.0*0.333*0.333*2
nRun['BBM1400BZTW'] = 816800.0*0.333*0.333*2
nRun['BBM1500BZTW'] = 831000.0*0.333*0.333*2
nRun['BBM1600BZTW'] = 696600.0*0.333*0.333*2
nRun['BBM1700BZTW'] = 832600.0*0.333*0.333*2
nRun['BBM1800BZTW'] = 795400.0*0.333*0.333*2
nRun['BBM700BZBZ'] = 814800.0*0.333*0.333
nRun['BBM800BZBZ'] = 826200.0*0.333*0.333
nRun['BBM900BZBZ'] = 799800.0*0.333*0.333
nRun['BBM1000BZBZ'] = 825600.0*0.333*0.333
nRun['BBM1100BZBZ'] = 832000.0*0.333*0.333
nRun['BBM1200BZBZ'] = 832200.0*0.333*0.333
nRun['BBM1300BZBZ'] = 807200.0*0.333*0.333
nRun['BBM1400BZBZ'] = 816800.0*0.333*0.333
nRun['BBM1500BZBZ'] = 831000.0*0.333*0.333
nRun['BBM1600BZBZ'] = 696600.0*0.333*0.333
nRun['BBM1700BZBZ'] = 832600.0*0.333*0.333
nRun['BBM1800BZBZ'] = 795400.0*0.333*0.333
nRun['BBM700BZBH'] = 814800.0*0.333*0.333*2
nRun['BBM800BZBH'] = 826200.0*0.333*0.333*2
nRun['BBM900BZBH'] = 799800.0*0.333*0.333*2
nRun['BBM1000BZBH'] = 825600.0*0.333*0.333*2
nRun['BBM1100BZBH'] = 832000.0*0.333*0.333*2
nRun['BBM1200BZBH'] = 832200.0*0.333*0.333*2
nRun['BBM1300BZBH'] = 807200.0*0.333*0.333*2
nRun['BBM1400BZBH'] = 816800.0*0.333*0.333*2
nRun['BBM1500BZBH'] = 831000.0*0.333*0.333*2
nRun['BBM1600BZBH'] = 696600.0*0.333*0.333*2
nRun['BBM1700BZBH'] = 832600.0*0.333*0.333*2
nRun['BBM1800BZBH'] = 795400.0*0.333*0.333*2
nRun['BBM700BHBH'] = 814800.0*0.333*0.333
nRun['BBM800BHBH'] = 826200.0*0.333*0.333
nRun['BBM900BHBH'] = 799800.0*0.333*0.333
nRun['BBM1000BHBH'] = 825600.0*0.333*0.333
nRun['BBM1100BHBH'] = 832000.0*0.333*0.333
nRun['BBM1200BHBH'] = 832200.0*0.333*0.333
nRun['BBM1300BHBH'] = 807200.0*0.333*0.333
nRun['BBM1400BHBH'] = 816800.0*0.333*0.333
nRun['BBM1500BHBH'] = 831000.0*0.333*0.333
nRun['BBM1600BHBH'] = 696600.0*0.333*0.333
nRun['BBM1700BHBH'] = 832600.0*0.333*0.333
nRun['BBM1800BHBH'] = 795400.0*0.333*0.333

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

#energy scale samples (Q^2)
nRun['TTJetsPHQ2U'] = 9933327.
nRun['TTJetsPHQ2D'] = 9942427.
nRun['TtWQ2U'] = 497600. #not used
nRun['TtWQ2D'] = 499200. #not used
nRun['TbtWQ2U'] = 500000. #not used
nRun['TbtWQ2D'] = 497600. #not used



# Cross sections for MC samples (in pb)
xsec={}
xsec['DY'] = 6025.2 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['DYMG'] = 1921.8*3. # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
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
for ind in range(1,12): xsec['TTJetsPH_'+str(ind)]=xsec['TTJetsPH']
xsec['TTJetsPHSL'] = 831.76*2.*(3.*0.108)*(1.-3.*0.108)
for ind in range(1,14): xsec['TTJetsPHSL_'+str(ind)] = xsec['TTJetsPHSL'] 
xsec['TTJetsPH0to700inc'] = 831.76
for ind in range(1,12): xsec['TTJetsPH0to700inc_'+str(ind)]=xsec['TTJetsPH0to700inc']
xsec['TTJetsPH700to1000inc'] = 831.76*0.0921 #(xsec*filtering coeff.)
xsec['TTJetsPH1000toINFinc'] = 831.76*0.02474 #(xsec*filtering coeff.)
xsec['TTJetsPH700mtt'] = xsec['TTJetsPH700to1000inc']
xsec['TTJetsPH1000mtt'] = xsec['TTJetsPH1000toINFinc']
xsec['TTJetsPH2L'] = 831.76*((3.*0.108)**2)
xsec['WJetsHT100'] = 1345.*1.21 # (1.21 = k-factor )# https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsHT200'] = 359.7*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsHT400'] = 48.91*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsHT600'] = 12.05*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsHT800'] = 5.501*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsHT1200']= 1.329*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
xsec['WJetsHT2500']= 0.03216*1.21 # https://twiki.cern.ch/twiki/bin/view/CMS/SummaryTable1G25ns
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
xsec['TTG'] = 3.697
xsec['Tt'] = 136.02 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['Tbt'] = 80.95 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['Ts'] = 11.36/3 #(1/3 was suggested by Thomas Peiffer to account for the leptonic branching ratio)# https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['TtW'] = 35.85 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma
xsec['TbtW'] = 35.85 # https://twiki.cern.ch/twiki/bin/viewauth/CMS/SingleTopSigma

xsec['TTTT'] = 0.009103
xsec['VHnonbb'] = 0.952
xsec['WHbb'] = 0.419
xsec['WWW'] = 0.2086
xsec['WWZ'] = 0.1651
xsec['WZZ'] = 0.05565
xsec['ZZZ'] = 0.01398
xsec['WWllnn'] = 12.178
xsec['WWlnqq'] = 49.997
xsec['WZlnqq'] = 10.71
xsec['WZlnnn'] = 3.033
xsec['WZllqq'] = 5.595
xsec['WZllln'] = 4.42965
xsec['ZZllnn'] = 0.564
xsec['ZZllqq'] = 3.22
xsec['ZZllll'] = 1.256
xsec['tZq'] = 0.0758
xsec['ttHbb'] = 0.2934045
xsec['ttHnonbb'] = 0.215

#Scaling all HTB signal x-secs to 1pb as agreed with POM, 
#so we have the signal yields scaled to 1pb
xsec['Hptb180'] = 1.#((0.824531)**2/0.683584)*0.75 #interpolation using the fact that xsec proportuonal to exp(-m) http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb200'] = 1.#0.824531*0.75 #was 0.783951 http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb220'] = 1.#0.683584*0.75 #was 0.648629 http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb250'] = 1.#0.524247*0.75 #was 0.4982015 interpolation using the fact that xsec proportuonal to exp(-m) http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb300'] = 1.#0.343796*0.75 #was 0.324766 http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb350'] = 1.#0.2312180*0.75 #was 0.2184385 interpolation using the fact that xsec proportuonal to exp(-m) http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb400'] = 1.#0.158142*0.75 #was 0.148574 http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb450'] = 1.#0.1106674*0.75 #was 0.104141 interpolation using the fact that xsec proportuonal to exp(-m) http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb500'] = 1.#0.0785572*0.75 #was 0.0735225 http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb750'] = 1.#0.0172205*0.75 #http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb800'] = 1.#0.0130645*0.75 #http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb1000'] = 1.#0.00474564*0.75 #http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb2000'] = 1.#(8.70916e-05)*0.75 #http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['Hptb3000'] = 1.#((8.70916e-05)**2/0.00474564)*0.75 #interpolation using the fact that xsec proportuonal to exp(-m) http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt

xsec['HTBM180'] = 1.#((0.824531)**2/0.683584)*0.75 #interpolation using the fact that xsec proportuonal to exp(-m) http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM200'] = 1.#0.824531*0.75 #was 0.783951 http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM220'] = 1.#0.683584*0.75 #was 0.648629 http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM250'] = 1.#0.524247*0.75 #was 0.4982015 interpolation using the fact that xsec proportuonal to exp(-m) http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM300'] = 1.#0.343796*0.75 #was 0.324766 http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM350'] = 1.#0.2312180*0.75 #was 0.2184385 interpolation using the fact that xsec proportuonal to exp(-m) http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM400'] = 1.#0.158142*0.75 #was 0.148574 http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM450'] = 1.#0.1106674*0.75 #was 0.104141 interpolation using the fact that xsec proportuonal to exp(-m) http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM500'] = 1.#0.0785572*0.75 #was 0.0735225 http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM750'] = 1.#0.0172205*0.75 #http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM800'] = 1.#0.0130645*0.75 #http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM1000'] = 1.#0.00474564*0.75 #http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM2000'] = 1.#(8.70916e-05)*0.75 #http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt
xsec['HTBM3000'] = 1.#((8.70916e-05)**2/0.00474564)*0.75 #interpolation using the fact that xsec proportuonal to exp(-m) http://www.hephy.at/user/mflechl/hp_xsec/xsec_13TeV_tHp_2016_2_5.txt

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

#energy scale samples (Q^2)
xsec['TTJetsPHQ2U'] = xsec['TTJetsPH']
xsec['TTJetsPHQ2D'] = xsec['TTJetsPH']
xsec['TtWQ2U'] = xsec['TtW']
xsec['TtWQ2D'] = xsec['TtW']
xsec['TbtWQ2U'] = xsec['TbtW']
xsec['TbtWQ2D'] = xsec['TbtW']

# Calculate lumi normalization weights
weight = {}
for sample in sorted(nRun.keys()): 
	if 'BBM' not in sample and 'TTM' not in sample: 
		weight[sample] = (targetlumi*xsec[sample]) / (nRun[sample])
		#print sample, (xsec[sample]) / (nRun[sample])
	else: weight[sample] = (targetlumi*BR[sample[:2]+sample[-4:]]*xsec[sample[:-4]]) / (nRun[sample])
# Samples for Jet reweighting (to be able to run w/ and w/o JSF together!):
for sample in sorted(nRun.keys()):
	if 'QCDht' in sample or 'WJetsHT' in sample: weight[sample+'JSF'] = weight[sample]

for smp in weight.keys():
	if 'TTJets' in smp:
	    for hf in ['_tt2b','_ttbb','_ttb','_ttcc','_ttlf']: 
	    	weight[smp+hf]=weight[smp]

# for sample in sorted(weight.keys()): 
# 	if 'BBM' in sample or 'TTM' in sample or 'X53' in sample or 'JSF' in sample: continue
# 	print sample,xsec[sample] / nRun[sample]