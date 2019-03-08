#!/usr/bin/python

import os,sys,datetime,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from utils import *

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
if not categorize: pfix='kinematics_'+region
pfix+='_'+date#+'_'+time

iPlotList = [#distribution name as defined in "doHists.py"
# 			'lepPt',
# 			'lepEta',
# 			'deltaRjet1',
# 			'deltaRjet2',
# 			'deltaRjet3',
# 			'NPV',
# 			'JetEta',
# 			'JetPt',
# 			'Jet1Pt',
# 			'Jet2Pt',
# 			'Jet3Pt',
# 			'Jet4Pt',
# 			'MET',
# 			'NJets',
# 			'NBJets',
# 			'NWJets',
# 			'NTJets',
# 			'NJetsAK8',
# 			'JetPtAK8',
# 			'JetEtaAK8',
# 			'Tau21',
# 			'Tau21Nm1',
# 			'Tau32',
# 			'Tau32Nm1',
# 			'SoftDropMass', 
# 			'SoftDropMassNm1W',
# 			'SoftDropMassNm1t',
# 			'mindeltaR',
# 			'PtRel',
			
			'HT',
# 			'ST',
# 			'minMlb',
# 			'minMlbSBins',

# 			'NJets_vs_NBJets',

# 			'NBJetsNoSF',
# 			'nTrueInt',
# 	        'MTlmet',
# 			'minMlj',
# 			'lepIso',
# 			'deltaRAK8',
# 			'Bjet1Pt',
# 			'Wjet1Pt',
# 			'Tjet1Pt',
# 			'deltaPhiLMET',	
# 			'Jet5Pt',
# 			'Jet6Pt',
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
# 			'topPt',
# 			'topMass',
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

isEMlist  = ['E','M']
nttaglist = ['0','1','0p','1p','2p']
nWtaglist = ['0','1','0p','1p','2p']
nbtaglist = ['1','2','3','3p','4p']
njetslist = ['4','5','6','7','8','9','9p','10p']
if not categorize: 	
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['2p']
	njetslist = ['4p']
catList = list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))
	
outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.system('cp ../analyze.py doHists.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

count=0
for iplot in iPlotList:
	for cat in catList:
		if skip(cat): continue #check the "skip" function in utils module to see if you want to remove specific categories there!!!
		catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
		print "iPlot: "+iplot+", cat: "+catDir
		if not os.path.exists(outDir+'/'+catDir): os.system('mkdir '+catDir)
		os.chdir(catDir)
		os.system('cp '+outputDir+'/doCondorTemplates.sh '+outDir+'/'+catDir+'/'+cat[0]+'T'+cat[1]+'W'+cat[2]+'B'+cat[3]+'J'+cat[4]+iplot+'.sh')			
	
		dict={'dir':outputDir,'iPlot':iplot,'region':region,'isCategorized':categorize,
			  'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njets':cat[4],
			  'exeDir':outDir+'/'+catDir}
	
		jdf=open('condor.job','w')
		jdf.write(
"""universe = vanilla
Executable = %(exeDir)s/%(isEM)sT%(nttag)sW%(nWtag)sB%(nbtag)sJ%(njets)s%(iPlot)s.sh
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
                  
