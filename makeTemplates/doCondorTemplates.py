import os,sys,datetime,itertools,math

thisDir = os.getcwd()
if thisDir[-13:] == 'makeTemplates': runDir = thisDir[:-13]
else: runDir = thisDir
if os.getcwd()[-17:] == 'singleLepAnalyzer': os.chdir(os.getcwd()+'/makeTemplates/')
outputDir = thisDir+'/'
## UNDERLINED
region='TR' #PS,SR,TTCR,WJCR
## 0 OR 1 ONE BOARD
categorize=0 #1==categorize into t/W/b/j, 0==only split into flavor

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix = 'templates'+region
if not categorize: pfix='kinematics'+region
## REMEMBER TO CHANGE
pfix+='_Nov2020TT_HTdnnJ3corrsSF2D'

plotList = [#distribution name as defined in "doHists.py"
	#'NBDeepJets',
	#'lepPhi',
	#For Signal Region Templates -> FSRT
	#'ST',
	#'DnnTprime',
	#'DnnTTbar',
	#'DnnWJets',

        # 'DnnTTbar',
        # 'DnnWJets',
        # 'dnnLargest',
	
	'HTNtag', #-> Not part of this block it's own entity
        'HTdnnL'

        ## Training
        #'probj',
        #'probjlow',
        #'probjhigh',
        #'probj1low',
        #'probj2low',
        #'probj1fake',
        #'probj2fake',
        'probj1',
        'probj2',
        'probj3',
        'JetPtAK81',
        'JetPtAK82',
        'JetPtAK83',
        'SoftDrop1',
        'SoftDrop2',
        'SoftDrop3',
        'Tau211',
        'Tau212',
        'Tau213',
	'HT',
        'tpt',
	'tmass',
	'tdrWb',
	'ST',
	'MET',   
	'NJets', 
	'NBDeepJets',
	'NJetsAK8',
	'deltaRAK8',
        
	#Require 3 AK8s -> R3
	#'Tp2Mass',
        #'Tp1Mass',
        #'Tp2Pt',
        #'Tp1Pt',
        #'Tp1Eta',
        #'Tp2Eta',
        #'Tp1Phi',
        #'Tp2Phi',
        #'Tp1deltaR',
        #'Tp2deltaR',
	
        #Don't require 3 AK8s -> DR3
	#'probSumDecay',  	
        #'probSumFour',
        #'probb',
        #'probh',
        #'probj',
        #'probt',
        #'probw',
        #'probz',
        #'dnnLargest',
        #'nB',
        #'nH',
        #'nT',
        #'nW',
        #'nZ',

	##Not algorithm dependent -> NAD
	#'DnnTprime',
	#'DnnWJets',
	#'DnnTTbar',
        #'Wmass',
	#'tpt',
	#'Wpt',
	#'Wdrlep',	
	#'isLepW',
	#'HT',
	#'JetPt', 
	#'NBJets',
	#'NBDeepJetsNoSF',
	#'JetPtAK8',
	#'lepPt', 
	#'SoftDrop',
	#'minMlj',
	#'mindeltaR',
	#'PtRel',
	#'mindeltaRAK8',
	#'PtRelAK8',
	#'lepEta',
	#'lepIso',
	#'JetEta',
	#'JetEtaAK8',
	#'NTrue',
	#'minMlb',
	#'METmod',
	#'minDPhiMetJet',
	#'Tau21',

	# Not plotting for now
	#'Tau21Nm1',
	#'Tau32Nm1',
	#'SoftDropHNm1',
	#'SoftDropWZNm1',
	#'SoftDropTNm1',
	#'DoubleBNm1',
	#'deltaRlepAK81',
	#'deltaRlepAK82',
	#'MTlmet',
	#'Jet1Pt',
	#'Jet2Pt',
	#'Jet2Pt',
	#'Jet3Pt',
	#'Jet4Pt',
	#'Jet5Pt',
	#'Jet6Pt',
	#'JetPtBins', 
	#'Jet1PtBins',
	#'Jet2PtBins',
	#'Jet3PtBins',
	#'Jet4PtBins',
	#'Jet5PtBins',
	#'Jet6PtBins',
	#'NBJetsNotH',
	#'NBJetsNotPH',
	#'NBJetsNoSF',
	#'NWJets',
	#'PuppiNWJets',
	#'NTJets',
	#'NH1bJets',
	#'NH2bJets',
	#'PuppiNH1bJets',
	#'PuppiNH2bJets',
	#'JetPtBinsAK8',
	#'Tau21',  
	#'Tau32',  
	#'SoftDrop', 
	#'SoftDropTNm1',
	#'SoftDropNsubBNm1',
	#'deltaRjet1',
	#'deltaRjet2',
	#'deltaRjet3',
	#'nLepGen',
	#'METphi',
	#'lepPhi',
	#'lepIso',
	#'Tau1',
	#'Tau2',
	#'Tau3',
	#'JetPhi',
	#'JetPhiAK8',
	#'Bjet1Pt',
	#'Wjet1Pt',
	#'Tjet1Pt',
	#'topMass',
	#'topPt',
	#'minMlbST'
	]

isEMlist = ['E','M']
if '2D' in pfix: isEMlist = ['L']

#algolist = ['BEST','DeepAK8','DeepAK8DC']
algolist = ['DeepAK8']
if not categorize and 'algos' not in region and 'SR' not in region: algolist = ['all']

taglist = ['all']
if categorize:
	if region=='SR': 
		#taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH','notVtH','notVtZ','notVbW','notV']
		#taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH']
		#taglist=['notVtH','notVtZ','notVbW','notV']
		if 'BB' in pfix:
			taglist=['taggedtWtW','taggedbZtW','taggedbHtW','notVbH','notVbZ','notVtW',
			 'notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W']
		else:
			taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH','notVtH','notVtZ','notVbW',
			 'notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W']
			 #'notV3pW0Z0H0T',
			 #'notV2W0Z0H0T','notV2pW0Z0H1pT','notV2pW0Z1pH0pT','notV2pW1pZ0pH0pT',
			 #'notV1W0Z0H0T','notV1W0Z1H0T','notV1W0Z0H1pT','notV1W0Z1H1pT','notV1W0Z2pH0pT','notV1W1Z0H0pT','notV1W1Z1pH0pT','notV1W2pZ0pH0pT',
			 #'notV0W0Z0H0T','notV0W0Z1H0T','notV0W0Z0H1pT','notV0W0Z1H1pT','notV0W0Z2pH0pT','notV0W1Z0H0pT','notV0W1Z1pH0pT','notV0W2pZ0pH0pT']
	elif 'CR' in region: taglist=['dnnLargeT','dnnLargeH','dnnLargeZ','dnnLargeW','dnnLargeB','dnnLargeJttbar','dnnLargeJwjet']
	else: taglist = ['all']

outDir = outputDir+pfix+'/'
print outDir
if not os.path.exists(outDir): os.system('mkdir '+outDir)
if '2D' in outDir:
        os.system('cp ../analyze2D.py doHists2D.py ../dnnJcorrSF.py ../utils.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates2D.sh '+outDir+'/')
else:
        os.system('cp ../analyze.py doHists.py ../dnnJcorrSF.py ../utils.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

catlist = list(itertools.product(isEMlist,taglist,algolist))

iPlotList = []
dimstr = ''
if '2D' in outDir:
        dimstr = '2D'
        templist = list(itertools.combinations(plotList,2))
        for item in templist:
                if 'NJetsAK8' not in item[0] and 'NJetsAK8' not in item[1]: continue
                iPlotList.append('X'+item[0]+'Y'+item[1])
else:
        iPlotList = plotList
        
print 'Dimensions:',dimstr
print 'iPlotList:',iPlotList

count=0
for iplot in iPlotList:
	for cat in list(itertools.product(isEMlist,taglist,algolist)):
		catDir = cat[0]+'_'+cat[1]+'_'+cat[2]		
		outDir = outputDir+pfix+'/'+catDir
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		os.chdir(outDir)			

		dict={'rundir':runDir, 'dir':'.','iPlot':iplot,'region':region,'isCategorized':categorize,
			  'isEM':cat[0],'tag':cat[1],'algo':cat[2],'2D':dimstr}
		print dict
		jdf=open('condor.job','w')
		jdf.write(
			"""use_x509userproxy = true
universe = vanilla
Executable = %(rundir)s/makeTemplates/doCondorTemplates%(2D)s.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = ../analyze%(2D)s.py, ../dnnJcorrSF.py, ../samples.py, ../utils.py, ../weights.py, ../doHists%(2D)s.py
Output = condor_%(iPlot)s.out
Error = condor_%(iPlot)s.err
Log = condor_%(iPlot)s.log
Notification = Never
Arguments = %(dir)s %(iPlot)s %(region)s %(isCategorized)s %(isEM)s %(tag)s %(algo)s

Queue 1"""%dict)
		jdf.close()

		os.system('condor_submit condor.job')
		os.chdir('..')
		count+=1

print "Total jobs submitted:", count
                  
