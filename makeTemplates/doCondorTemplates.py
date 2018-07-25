import os,sys,datetime,itertools

thisDir = os.getcwd()
outputDir = thisDir+'/'
region='SRNoB0' #PS,SR,TTCR,WJCR
categorize=0 #1==categorize into t/W/b/j, 0==only split into flavor

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
if region=='TTCR': pfix='ttbar_NewEl'
elif region=='WJCR': pfix='wjets_NewEl'
elif region=='HCR': pfix='higgs_NewEl'
elif region=='CRall': pfix='control_NewEl'  #alllll the categories
elif region=='CR': pfix='templatesCR_NewEl' #more inclusive categories to be faster
else: pfix='templates_NewEl'
if not categorize: pfix='kinematics_'+region+'_NewEl'
#pfix+='_'+date+'_wJSF'#+'_'+time

iPlotList = [#distribution name as defined in "doHists.py"
	# 'minMlbST',
 	# 'ST',
	'HT',
 	'minMlb',
	'minMlj',	
	'lepPt',
	# 'deltaRjet1',
	# 'deltaRjet2',
	# 'deltaRAK8',
	# 'lepIso',
	'HT',
	'JetPt',
	'MET',
	'NJets',
	'NBJets',
	'NBJetsNotH',
	# 'NBJetsNotPH',
	'NWJets',
	# 'PuppiNWJets',
	'NH1bJets',
	'NH2bJets',
	# 'PuppiNH1bJets',
	# 'PuppiNH2bJets',
	'NJetsAK8',
	'JetPtAK8',
	'Tau21',
	'Tau21Nm1',
	# 'PuppiTau21',
	# 'PuppiTau21Nm1',
	# 'Pruned',
	'PrunedWNm1',
	'PrunedHNm1',
	'PrunedNsubBNm1',
	# 'PuppiSD',
	# 'PuppiSDWNm1',
	# 'PuppiSDHNm1',
	# 'PuppiNsubBNm1',
	# 'PuppiSDRawWNm1',
	# 'SoftDrop', 
	# 'SoftDropHNm1',
	# 'SoftDropNsubBNm1',
	# 'NPV',
	# 'mindeltaR',
	# 'PtRel',
	# 'lepEta',
	# 'JetEta',
	# 'JetEtaAK8',
	# 'topPt',
	# 'Jet1Pt',
	# 'Jet2Pt',
	# 'Jet3Pt',
	# 'Jet4Pt',

 	#'PuppiSDRaw',
	#'PuppiSDCorr',
	#'PuppiSDCorrWNm1',
	#'topMass',
	#'minDRlepAK8',
	#'deltaRlepAK81',
	#'deltaRlepAK82',
	#'masslepAK81',
	#'masslepAK82',
	#'Tau1',
	#'Tau2',
	#'Tau3',
	#'Bjet1Pt',
	#'Wjet1Pt',
#	'MTlmet',
#	'deltaRjet3',
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
elif 'CR' in region: 
	if region == 'HCR': nHtaglist = ['1b','2b']
	elif region=='CR': nHtaglist = ['0','1p']
	elif region=='CRall': nHtaglist = ['0','1b','2b']
	else: nHtaglist = ['0']
else: nHtaglist = ['0p']

if region=='TTCR' or region=='HCR' or region=='CR': nWtaglist = ['0p']
else: nWtaglist=['0','0p','1p']

if region=='WJCR': nbtaglist = ['0']
elif region=='HCR': nbtaglist = ['0','1p']
elif region=='TTCR': nbtaglist = ['1','2','3p']
elif region=='CR': nbtaglist = ['0','1p']
else: nbtaglist = ['0','1','1p','2','3p']

if not categorize: 	
	nHtaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0p']
	if region=='WJCR': nbtaglist = ['0']
	if region=='TTCR': nbtaglist = ['1p']
	if region=='HCR': 
		nHtaglist = ['1p']
		nbtaglist = ['0','1p']
njetslist = ['3p']
if region=='PS': njetslist = ['3p']

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.system('cp ../analyze.py doHists.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

catlist = list(itertools.product(isEMlist,nHtaglist,nWtaglist,nbtaglist,njetslist))
print catlist

count=0
for iplot in iPlotList:
	for cat in list(itertools.product(isEMlist,nHtaglist,nWtaglist,nbtaglist,njetslist)):
		catDir = cat[0]+'_nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]		
		if categorize:
			if 'b' in cat[1]:
				#print 'got an H tag'
				if cat[2] != '0p': continue
				if ((region == 'SR' or region == 'TTCR') and cat[3] != '1p') or (region == 'WJCR' and cat[3] != '0') or (region == 'HCR' and cat[3] != '0' and cat[3] != '1p'): continue
			else:
				#print 'no H tag'
				if (region == 'SR' or region == 'WJCR') and cat[2] == '0p': continue
				if cat[3] == '1p' and region != 'CR': continue
		print catDir
		#######
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
                  
