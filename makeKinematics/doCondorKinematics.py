import os,sys,datetime

thisDir = os.getcwd()
outputDir = thisDir+'/'

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='kinematics_Presel'
pfix+='_'+date#+'_'+time

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.chdir(outDir)

catList = ['E','M','All']

plotList = [#distribution name as defined in "doHists.py"
	'MTlmet',
	'lepPt' ,
	'lepEta',
	'mindeltaR',
	'PtRel',
	'deltaRjet1',
	'deltaRjet2',
	'deltaRjet3',
	'minMlb' ,
	'minMlj',
	'lepIso',
	'deltaRAK8',
	'NPV'   ,
	'JetEta',
	'JetPt' ,
	'Jet1Pt',
	'Jet2Pt',
	'Jet3Pt',
	'Jet4Pt',
	'Jet5Pt',
	'Jet6Pt',
	'HT'    ,
	'ST'    ,
	'MET'   ,
	'NJets' ,
	'NBJets',
	'NWJets',
	'NTJets',
	'NJetsAK8',
	'JetPtAK8',
	'JetEtaAK8',
	'Tau21'  ,
	'Tau21Nm1'  ,
	'Tau32'  ,
	'Tau32Nm1'  ,
	'Pruned' ,
	'PrunedNm1' ,
	'SoftDropMass', 
	'SoftDropMassNm1', 
	'Bjet1Pt',
	'Wjet1Pt',
	'Tjet1Pt',
	
	#'topPt',
	#'JetPtBins' ,
	#'Jet1PtBins',
	#'Jet2PtBins',
	#'Jet3PtBins',
	#'Jet4PtBins',
	#'Jet5PtBins',
	#'Jet6PtBins',
	#'JetPtBinsAK8',
	#'minMljDR',
	#'minMljDPhi',
	#'minMlbDR',
	#'minMlbDPhi',
	#'topMass',
	#'topPt',
	#'nLepGen',
	#'METphi',
	#'lepPhi',
	#'lepDxy',
	#'lepDz',
	#'lepCharge',
	#'Tau1',
	#'Tau2',
	#'Tau3',
	#'JetPhi',
	#'JetPhiAK8',
	]

count = 0
for distribution in plotList:
	for cat in catList:
		print cat
		if not os.path.exists(outDir+'/'+cat): os.system('mkdir '+cat)
		os.chdir(cat)
		
		dict={'dir':outputDir,'dist':distribution,'cat':cat}

		jdf=open('condor_'+distribution+'.job','w')
		jdf.write(
"""universe = vanilla
Executable = %(dir)s/doCondorKinematics.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 3072
arguments = ""
Output = condor_%(dist)s.out
Error = condor_%(dist)s.err
Log = condor_%(dist)s.log
Notification = Error
Arguments = %(dir)s %(dist)s %(cat)s

Queue 1"""%dict)
		jdf.close()

		os.system('condor_submit condor_'+distribution+'.job')
		os.chdir('..')
		count+=1
									
print "Total jobs submitted:", count



                  
