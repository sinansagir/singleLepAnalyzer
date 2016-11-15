import os,sys,datetime,itertools

thisDir = os.getcwd()
outputDir = thisDir+'/'

#iplot='minMlb' #ST,minMlb,etc
region='PS' #PS,SR,TTCR,WJCR
categorize=0 #1==categorize into t/W/b/j, 0==only split into flavor

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
if region=='TTCR': pfix='ttbar'
elif region=='WJCR': pfix='wjets'
else: pfix='templates'
if not categorize: pfix='kinematics_'+region
#pfix+=iplot+'_wJSF'
pfix+='_'+date+'_wJSF'#+'_'+time

iPlotList = [#distribution name as defined in "doHists.py"
	        'MTlmet',
			'lepPt',
			'lepEta',
			'mindeltaR',
			'PtRel',
			'deltaRjet1',
			'deltaRjet2',
			'deltaRjet3',
			'minMlj',
			'lepIso',
			'deltaRAK8',
			'NPV',
			'JetEta',
			'JetPt',
			'Jet1Pt',
			'Jet2Pt',
			'Jet3Pt',
			'Jet4Pt',
			'Jet5Pt',
			'Jet6Pt',
			'MET',
			'NJets',
			'NBJets',
			'NWJets',
			'NTJets',
			'NJetsAK8',
			'JetPtAK8',
			'JetEtaAK8',
			'Tau21',
			'Tau21Nm1',
			'Tau32',
			'Tau32Nm1',
			'PrunedSmeared',
			'PrunedSmearedNm1',
			'SoftDropMass', 
			'SoftDropMassNm1', 
			'Bjet1Pt',
			'Wjet1Pt',
			'Tjet1Pt',

			'HT',
			'ST',
			'minMlb',
	
# 			'topPt',
# 			'JetPtBins',
# 			'Jet1PtBins',
# 			'Jet2PtBins',
# 			'Jet3PtBins',
# 			'Jet4PtBins',
# 			'Jet5PtBins',
# 			'Jet6PtBins',
# 			'JetPtBinsAK8',
# 			'minMljDR',
# 			'minMljDPhi',
# 			'minMlbDR',
# 			'minMlbDPhi',
# 			'topMass',
# 			'topPt',
# 			'nLepGen',
# 			'METphi',
# 			'lepPhi',
# 			'lepDxy',
# 			'lepDz',
# 			'lepCharge',
# 			'Tau1',
# 			'Tau2',
# 			'Tau3',
# 			'JetPhi',
# 			'JetPhiAK8',
			]

isEMlist = ['E','M']
if region=='SR': nttaglist = ['0','1p']
else: nttaglist = ['0p']
if region=='TTCR': nWtaglist = ['0p']
else: nWtaglist=['0','1p']
if region=='WJCR': nbtaglist = ['0']
else: nbtaglist = ['1','2p']
if not categorize: 	
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['1p']
	if region=='WJCR': nbtaglist = ['0']
njetslist = ['4p']
if region=='PS': njetslist = ['3p']

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.system('cp ../analyze.py doHists.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

count=0
for iplot in iPlotList:
	for cat in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist)):
		catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
		print catDir
		if not os.path.exists(outDir+'/'+catDir): os.system('mkdir '+catDir)
		os.chdir(catDir)			
	
		dict={'dir':outputDir,'iPlot':iplot,'region':region,'isCategorized':categorize,
			  'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4]}
	
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
Arguments = %(dir)s %(iPlot)s %(region)s %(isCategorized)s %(isEM)s %(nttag)s %(nWtag)s %(nbtag)s %(njets)s
Queue 1"""%dict)
		jdf.close()

		os.system('condor_submit condor.job')
		os.chdir('..')
		count+=1

print "Total jobs submitted:", count
                  
