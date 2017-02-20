import os,sys,datetime,itertools

thisDir = os.getcwd()
outputDir = thisDir+'/'

region='SR' #PS,SR,TTCR,WJCR
categorize=1 #1==categorize into t/W/b/j, 0==only split into flavor

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
if region=='TTCR': pfix='ttbar'
elif region=='WJCR': pfix='wjets'
else: pfix='templates'
if not categorize: pfix='kinematics_'+region+'Wkshp'
#pfix+='_'+date+'_wJSF'#+'_'+time

iPlotList = [#distribution name as defined in "doHists.py"
	#'lepPt',
	#'lepEta',
	#'mindeltaR',
	#'PtRel',
	#'deltaRjet1',
	#'deltaRjet2',
	#'HT',
	'ST',
	'minMlb',	
	#'minMlj',
	#'lepIso',
	#'NPV',
	#'JetEta',
	#'JetPt',
	#'Jet1Pt',
	#'Jet2Pt',
	#'Jet3Pt',
	#'Jet4Pt',
	#'MET',
	#'NJets',
	#'NBJets',
	#'NWJets',
	#'NH1bJets',
	#'NH2bJets',
	#'NJetsAK8',
	#'JetPtAK8',
	#'JetEtaAK8',
	#'topMass',
	#'topPt',
	#'Tau1',
	#'Tau2',
	#'Tau3',
	#'Tau21',
	#'Tau21Nm1',
	#'PrunedSmeared',
	#'PrunedSmearedNm1',
	#'SoftDropMass', 
	#'Bjet1Pt',
	#'Wjet1Pt',

#	'MTlmet',
#	'deltaRjet3',
#	'deltaRAK8',
#	'Jet5Pt',
#	'Jet6Pt',
#	'Tau32',
#	'Tau32Nm1',
#	'SoftDropMassNm1', 
#	'Tjet1Pt',	
	# 'JetPtBins',
	# 'Jet1PtBins',
	# 'Jet2PtBins',
	# 'Jet3PtBins',
	# 'Jet4PtBins',
	# 'Jet5PtBins',
	# 'Jet6PtBins',
	# 'JetPtBinsAK8',
	# 'minMljDR',
	# 'minMljDPhi',
	# 'minMlbDR',
	# 'minMlbDPhi',
 	# 'METphi',
	# 'lepPhi',
	# 'lepDxy',
	# 'lepDz',
	# 'lepCharge',
	# 'JetPhi',
	# 'JetPhiAK8',
	]

isEMlist = ['E','M']
if region=='SR': nHtaglist = ['0','1b','2b']
else: nHtaglist = ['0p']
if region=='TTCR': nWtaglist = ['0p']
else: nWtaglist=['0','0p','1p']
if region=='WJCR': nbtaglist = ['0']
else: nbtaglist = ['0','1','1p','2','3p']
if not categorize: 	
	nHtaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0p']
	if region=='WJCR': nbtaglist = ['0']
	if region=='TTCR': nbtaglist = ['2p']
njetslist = ['3p']
if region=='PS': njetslist = ['3p']

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.system('cp ../analyze.py doHists.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

count=0
for iplot in iPlotList:
	for cat in list(itertools.product(isEMlist,nHtaglist,nWtaglist,nbtaglist,njetslist)):
		if categorize:
			if 'b' in cat[1]:
				if cat[2] != '0p': continue
				if cat[3] != '1p': continue
			else:
				if cat[2] == '0p': continue
				if cat[3] == '1p': continue
		catDir = cat[0]+'_nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]		
		print catDir
		if not os.path.exists(outDir+'/'+catDir): os.system('mkdir '+catDir)
		os.chdir(catDir)			
	
		dict={'dir':outputDir,'iPlot':iplot,'region':region,'isCategorized':categorize,
			  'isEM':cat[0],'nHtag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4]}
	
		jdf=open('condor.job','w')
		jdf.write(
"""universe = vanilla
Executable = %(dir)s/doCondorTemplates.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 3072
Output = condor_%(iPlot)s.out
Error = condor_%(iPlot)s.err
Log = condor_%(iPlot)s.log
Notification = Error
Arguments = %(dir)s %(iPlot)s %(region)s %(isCategorized)s %(isEM)s %(nHtag)s %(nWtag)s %(nbtag)s %(njets)s
Queue 1"""%dict)
		jdf.close()

		os.system('condor_submit condor.job')
		os.chdir('..')
		count+=1

print "Total jobs submitted:", count
                  
