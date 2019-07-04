import os,sys,datetime,itertools

thisDir = os.getcwd()
if thisDir[-13:] == 'makeTemplates': runDir = thisDir[:-13]
else: runDir = thisDir
if os.getcwd()[-17:] == 'singleLepAnalyzer': os.chdir(os.getcwd()+'/makeTemplates/')
outputDir = thisDir+'/'
region='PS' #PS,SR,TTCR,WJCR
categorize=0 #1==categorize into t/W/b/j, 0==only split into flavor

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix = 'templates'+region
if not categorize: pfix='kinematics'+region
pfix+='_HighPU'

iPlotList = [#distribution name as defined in "doHists.py"
	#'ST',
	#'Tp2Mass',
	#'Tp2MDnn',
	#'Tp2MST',
	#'DnnTprime',
	#'HT',

	### Require 3 AK8s
	# 'Tp2Mass',
        # 'Tp1Mass',
        # 'Tp2Pt',
        # 'Tp1Pt',
        # 'Tp1Eta',
        # 'Tp2Eta',
        # 'Tp1Phi',
        # 'Tp2Phi',
        # 'Tp1deltaR',
        # 'Tp2deltaR',

        # 'probSumDecay',  	###Don't require 3 AK8s
        # 'probSumFour',
        # 'probb',
        # 'probh',
        # 'probj',
        # 'probt',
        # 'probw',
        # 'probz',
	# 'dnnLargest',
	# 'nB',
	# 'nH', 
	# 'nT',
	# 'nW', 
	# 'nZ',
	
	# #Not algorithm dependent
	'DnnTprime',
	'DnnWJets',
	'DnnTTbar',
	# 'tmass',
        # 'Wmass',
	# 'tpt',
	# 'Wpt',
	# 'tdrWb',
	# 'Wdrlep',	
	# 'isLepW',
	'HT',
	'ST',
	'JetPt', 
	'MET',   
	'NJets', 
	'NBJets',
	'NJetsAK8',
	'JetPtAK8',
	'lepPt', 
	# 'SoftDrop',
	# 'deltaRAK8',
	# 'minMlj',
	# 'mindeltaR',
	# 'PtRel',
	# 'mindeltaRAK8',
	# 'PtRelAK8',
	'lepEta',
	'lepIso',
	'JetEta',
	'JetEtaAK8',
	'NPV',   
	# 'NTrue',
	# 'minMlb',
	# 'METmod',
	# 'minDPhiMetJet',

	### Not plotting for now
	# 'Tau21Nm1',
	# 'Tau32Nm1',
	# 'SoftDropHNm1',
	# 'SoftDropWZNm1',
	# 'SoftDropTNm1',
	# 'DoubleBNm1',
	# 'deltaRlepAK81',
	# 'deltaRlepAK82',
	# 'MTlmet',
	# 'Jet1Pt',
	# 'Jet2Pt',
	# 'Jet2Pt',
	# 'Jet3Pt',
	# 'Jet4Pt',
	# 'Jet5Pt',
	# 'Jet6Pt',
	# 'JetPtBins', 
	# 'Jet1PtBins',
	# 'Jet2PtBins',
	# 'Jet3PtBins',
	# 'Jet4PtBins',
	# 'Jet5PtBins',
	# 'Jet6PtBins',
	# 'NBJetsNotH',
	# 'NBJetsNotPH',
	# 'NBJetsNoSF',
	# 'NWJets',
	# 'PuppiNWJets',
	# 'NTJets',
	# 'NH1bJets',
	# 'NH2bJets',
	# 'PuppiNH1bJets',
	# 'PuppiNH2bJets',
	# 'JetPtBinsAK8',
	# 'Tau21',  
	# 'Tau32',  
	# 'SoftDrop', 
	# 'SoftDropTNm1',
	# 'SoftDropNsubBNm1',
	# 'deltaRjet1',
	# 'deltaRjet2',
	# 'deltaRjet3',
	# 'nLepGen',
	# 'METphi',
	# 'lepPhi',
	# 'lepIso',
	# 'Tau1',
	# 'Tau2',
	# 'Tau3',
	# 'JetPhi',
	# 'JetPhiAK8',
	# 'Bjet1Pt',
	# 'Wjet1Pt',
	# 'Tjet1Pt',
	# 'topMass',
	# 'topPt',
	# 'minMlbST'
	]

isEMlist = ['E','M']
#isEMlist = ['L']

#algolist = ['BEST','DeepAK8','DeepAK8DC']
algolist = ['DeepAK8']
if not categorize and 'algos' not in region and 'SR' not in region: algolist = ['all']

taglist = ['all']
if categorize:
	if region=='SR': 
		#taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH','notVtH','notVtZ','notVbW','notV']
		#taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH']
		#taglist=['notVtH','notVtZ','notVbW','notV']
		taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH','notVtH','notVtZ','notVbW',
			 'notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W']
			 #'notV3pW0Z0H0T',
			 #'notV2W0Z0H0T','notV2pW0Z0H1pT','notV2pW0Z1pH0pT','notV2pW1pZ0pH0pT',
			 #'notV1W0Z0H0T','notV1W0Z1H0T','notV1W0Z0H1pT','notV1W0Z1H1pT','notV1W0Z2pH0pT','notV1W1Z0H0pT','notV1W1Z1pH0pT','notV1W2pZ0pH0pT',
			 #'notV0W0Z0H0T','notV0W0Z1H0T','notV0W0Z0H1pT','notV0W0Z1H1pT','notV0W0Z2pH0pT','notV0W1Z0H0pT','notV0W1Z1pH0pT','notV0W2pZ0pH0pT']
	elif 'CR' in region: taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH','notVtH','notVtZ','notVbW','notV']
	else: taglist = ['all']

outDir = outputDir+pfix+'/'
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.system('cp ../analyze.py doHists.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

catlist = list(itertools.product(isEMlist,taglist,algolist))

count=0
for iplot in iPlotList:
	for cat in list(itertools.product(isEMlist,taglist,algolist)):
		catDir = cat[0]+'_'+cat[1]+'_'+cat[2]		
		outDir = outputDir+pfix+'/'+catDir
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		os.chdir(outDir)			

		dict={'rundir':runDir, 'dir':'.','iPlot':iplot,'region':region,'isCategorized':categorize,
			  'isEM':cat[0],'tag':cat[1],'algo':cat[2]}
		print dict
		jdf=open('condor.job','w')
		jdf.write(
			"""use_x509userproxy = true
universe = vanilla
Executable = %(rundir)s/makeTemplates/doCondorTemplates.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(rundir)s/analyze.py, %(rundir)s/samples.py, %(rundir)s/utils.py, %(rundir)s/weights.py, %(rundir)s/makeTemplates/doHists.py
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
                  
