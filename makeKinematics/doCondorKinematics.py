import os,sys,datetime

thisDir = os.getcwd()
outputDir = thisDir+'/'

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='kinematics_substructure'
#pfix+='_'+date+'_'+time

plotList = [#distribution name as defined in "doHists.py"
#	'deltaRb1Nonb',
#	'deltaRb2Nonb',
#	'deltaRWNonb',
#	'deltaEtab1Nonb',
#	'deltaEtab2Nonb',
#	'deltaEtaWNonb',
#	'deltaPhib1Nonb',
#	'deltaPhib2Nonb',
#	'deltaPhiWNonb',
#	'TTbarPtBalance',

#	'deltaRAK8',
#	'MTlmet',
#	'NPV',
#	'lepPt',
#	'lepEta',
# 	'JetEta',
#	'JetPt' ,
#	'Jet1Pt',
#	'Jet2Pt',
#	'Jet3Pt',
#	'Jet4Pt',
#	'HT',
#	'ST',
#	'MET',
#	'NJets' ,
#	'NBJets',
	'NWJetsSmeared',
	'NWJetsSmeared0p55SF',
	'NWJetsSmeared0p55noSF',
#	'NJetsAK8',
#	'JetPtAK8',
#	'JetEtaAK8',
 	'Tau21',
 	'Tau21Nm1',
 	'PrunedSmeared',
 	'PrunedSmearedNm1',
# 	'mindeltaR',
#	'deltaRjet1',
#	'deltaRjet2',
# 	'deltaRjet3',
# 	'minMlb',
#	'METphi',
#	'lepPhi',
#	'lepDxy',
#	'lepDz',
#	'lepCharge',
#	'lepIso',
#	'Tau1',
#	'Tau2',
#	'JetPhi',
#	'JetPhiAK8',
#	'Bjet1Pt',
#	'Wjet1Pt',
#	'topMass',
#	'topPt',
#	'minMlj',
#	'minMljDR',
#	'minMljDPhi',
#	'minMlbDR',
#	'minMlbDPhi',
#	'nonMinMlbDR',
#	'MWb1',
#	'MWb2',
#	'HT4jets',
#	'deltaRlb1',
#	'deltaRlb2',
#	'deltaRtW',
#	'deltaRlW',
#	'deltaRWb1',
#	'deltaRWb2',
#	'deltaPhilb1',
#	'deltaPhilb2',
#	'deltaPhitW',
#	'deltaPhilW',
#	'deltaPhiWb1',
#	'deltaPhiWb2',
#	'WjetPt',
#	'PtRel',

# 	'METwJetSF',
# 	'METwJetSFraw',
#	'Jet5Pt',
#	'Jet6Pt',
#	'HTtest',
#	'STnewMET',
#	'NWJets',
#	'JetPtBinsAK8',
#	'Pruned',
#	'nTrueInt',
#	'nLepGen',
	]

catList = ['E','M','All']

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.chdir(outDir)

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
transfer_input_files = %(dir)s/doHists.py,%(dir)s/samples.py,%(dir)s/weights.py,%(dir)s/analyze.py
WhenToTransferOutput = ON_EXIT
notify_user = Sinan_Sagir@brown.edu

arguments      = ""

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



                  
