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
pfix+='_full_'+date#+'_'+time

iPlotList = [#distribution name as defined in "doHists.py"
# 'lepPt',
# 'lepEta',
# 'deltaRjet1',
# 'deltaRjet2',
# 'deltaRjet3',
# 'JetEta',
# 'JetPt',
# 'Jet1Pt',
# 'Jet2Pt',
# 'Jet3Pt',
# 'Jet4Pt',
# 'MET',
# 'NJets',
# 'NBJets',
# 'NWJets',
# 'NTJets',
# 'NJetsAK8',
# 'JetPtAK8',
# 'JetEtaAK8',
# 'Tau21',
# 'Tau21Nm1',
# 'Tau32',
# 'Tau32Nm1',
# 'SoftDropMass', 
# 'SoftDropMassNm1W',
# 'SoftDropMassNm1t',
# 'mindeltaR',
# 'PtRel',
# 
'HT',
# 'ST',
# 'minMlb',
# 
# 'MTlmet',
# 'minMlj',
# 'lepIso',
# 'deltaRAK8',
# 'Bjet1Pt',
# 'Wjet1Pt',
# 'Tjet1Pt',
# 'Jet5Pt',
# 'Jet6Pt',
# 'METphi',
# 'lepPhi',
# 'Tau1',
# 'Tau2',
# 'Tau3',
# 'JetPhi',
# 'JetPhiAK8',
# 'NresolvedTops1p',
# 'NresolvedTops2p',
# 'NresolvedTops5p',
# 'NresolvedTops10p',
# 'HOTtPt',
# 'HOTtEta',
# 'HOTtPhi',
# 'HOTtMass',
# 'HOTtDisc',
# 'HOTtNconst',
# 'HOTtNAK4',
# 'HOTtDRmax',
# 'HOTtDThetaMax',
# 'HOTtDThetaMin',

# 'NHOTtJets',
# 'NPV',
# 'BDT',
# 'minMlbSBins',
# 'NJets_vs_NBJets',
# 'isHTgt500Njetge9',
# 'deltaPhiLMET',	
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
# 'topPt',
# 'topMass',
]

isEMlist  = ['E','M']
nhottlist = ['0','0p','1p']
nttaglist = ['0','0p','1p']
nWtaglist = ['0','0p','1p','1','2p']
nbtaglist = ['2','3','3p','4p']
njetslist = ['4','5','6','7','8','9','9p','10p']
# nhottlist = ['0p']
# nttaglist = ['0p']
# nWtaglist = ['0p']
# nbtaglist = ['2p']
# njetslist = ['4p','5p','6p','7p','8p','9p','10p']
if not categorize: 	
	nhottlist = ['0p']
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['2p']
	njetslist = ['4p']
catList = list(itertools.product(isEMlist,nhottlist,nttaglist,nWtaglist,nbtaglist,njetslist))
	
outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.system('cp ../analyze.py doHists.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

count=0
for iplot in iPlotList:
	for cat in catList:
		if skip(cat): continue #check the "skip" function in utils module to see if you want to remove specific categories there!!!
		catDir = cat[0]+'_nHOT'+cat[1]+'_nT'+cat[2]+'_nW'+cat[3]+'_nB'+cat[4]+'_nJ'+cat[5]
		print "iPlot: "+iplot+", cat: "+catDir
		if not os.path.exists(outDir+'/'+catDir): os.system('mkdir '+catDir)
		os.chdir(catDir)
	
		dict={'dir':outputDir,'iPlot':iplot,'region':region,'isCategorized':categorize,
			  'isEM':cat[0],'nhott':cat[1],'nttag':cat[2],'nWtag':cat[3],'nbtag':cat[4],'njets':cat[5],
			  'exeDir':thisDir}
	
		jdf=open('condor_'+iplot+'.job','w')
		jdf.write(
"""universe = vanilla
Executable = %(exeDir)s/doCondorTemplates.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 3072
Output = condor_%(iPlot)s.out
Error = condor_%(iPlot)s.err
Log = condor_%(iPlot)s.log
Notification = Error
Arguments = %(dir)s %(iPlot)s %(region)s %(isCategorized)s %(isEM)s %(nhott)s %(nttag)s %(nWtag)s %(nbtag)s %(njets)s
Queue 1"""%dict)
		jdf.close()

		os.system('condor_submit condor_'+iplot+'.job')
		os.chdir('..')
		count+=1

print "Total jobs submitted:", count
                  
