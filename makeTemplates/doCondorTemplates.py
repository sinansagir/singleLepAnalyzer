import os,sys,datetime,itertools

thisDir = os.getcwd()
if thisDir[-13:] == 'makeTemplates': runDir = thisDir[:-13]
else: runDir = thisDir
if os.getcwd()[-17:] == 'singleLepAnalyzer': os.chdir(os.getcwd()+'/makeTemplates/')
outputDir = thisDir+'/'
region='PS' #PS,PSalgos,SR,STalgos,NoDR,CR. Use "algos" for (el,mu)x(3 jet algorithms)
categorize=0 #1==categorize into (el,mu)x(6 decays + notValid)x(3 jet algorithms)

proxyPath=os.popen('voms-proxy-info -path')
proxyPath=proxyPath.readline().strip()

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix = 'templates'+region
if not categorize: pfix='kinematics'+region
pfix+='_Oct11'

iPlotList = [#distribution name as defined in "doHists.py"

	### for NoDR
	# 'deltaRAK8',

	### for SR templates
	# 'ST',
	# 'Tp2Mass',

	### Require 3 AK8s -- SR kinematics, SRalgos
        # 'Tp1Mass',
        # 'Tp2Pt',
        # 'Tp1Pt',
        # 'Tp1Eta',
        # 'Tp2Eta',
        # 'Tp1Phi',
        # 'Tp2Phi',
        # 'Tp1deltaR',
        # 'Tp2deltaR',

	### Don't require 3 AK8s -- SRalgos, PSalgos
        # 'probSumDecay',
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

	## Not algorithm dependent -- SR kinematics, PS kinematics 
	'tmass',
        'Wmass',
	'HT',
	'ST',
	'minDRlepAK8',
	'Tau21Nm1',
	'Tau32Nm1',
	'SoftDropHNm1',
	'SoftDropWZNm1',
	'SoftDropTNm1',
	'DoubleBNm1',
	'JetPt', 
	'MET',   
	'NJets', 
	'NBJets',
	'NJetsAK8',
	'JetPtAK8',
	'lepPt', 
	'NPV',   
	'lepEta',
	'JetEta',
	'JetEtaAK8',
	'mindeltaR',
	'PtRel',

	]

isEMlist = ['E','M']

algolist = ['BEST','DeepAK8','DeepAK8DC']
if not categorize and 'algos' not in region: algolist = ['all']

taglist = ['all']
if categorize:
	if region=='SR': taglist=['taggedbWbW','taggedtHbW','taggedtHtH','taggedtZbW','taggedtZtH','taggedtZtZ','taggedtZHtZH','notV']
	elif region=='CR': taglist=['taggedbWbW','taggedtHbW','taggedtHtH','taggedtZbW','taggedtZtH','taggedtZtZ','taggedtZHtZH','notV']
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
			  'isEM':cat[0],'tag':cat[1],'algo':cat[2],'PROXY':proxyPath}
		print dict
		jdf=open('condor.job','w')
		jdf.write(
			"""x509userproxy = %(PROXY)s
universe = vanilla
Executable = %(rundir)s/makeTemplates/doCondorTemplates.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Transfer_Input_Files = %(rundir)s/analyze.py, %(rundir)s/samples.py, %(rundir)s/utils.py, %(rundir)s/weights.py, %(rundir)s/makeTemplates/doHists.py
Output = condor_%(iPlot)s.out
Error = condor_%(iPlot)s.err
Log = condor_%(iPlot)s.log
Notification = Never
Notification = Error
Arguments = %(dir)s %(iPlot)s %(region)s %(isCategorized)s %(isEM)s %(tag)s %(algo)s

Queue 1"""%dict)
		jdf.close()

		os.system('condor_submit condor.job')
		os.chdir('..')
		count+=1

print "Total jobs submitted:", count
                  
