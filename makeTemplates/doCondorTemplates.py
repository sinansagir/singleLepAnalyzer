import os,sys,datetime,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from utils import *

thisDir = os.getcwd()
outputDir = thisDir+'/'

region='SR' #PS,SR
categorize=0 #1==categorize into t/W/b/j, 0==only split into flavor

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='templates'
if not categorize: pfix='kinematics_'+region
pfix+='_'+date+'_'+time

iPlotList = [#distribution name as defined in "doHists.py"
			'lepPt',
			'lepEta',
			'NPV',
			'JetEta',
			'JetPt',
			'Jet1Pt',
			'Jet2Pt',
			'Jet3Pt',
			'MET',
			'NJets',
			'NBJets',
			'HT',
			'ST',
# 			'BDT',
# 			'LeadJetPt',
# 			'aveBBdr',
# 			'mass_maxJJJpt',
# 			'mass_maxBBmass',
# 			'mass_maxBBpt',
# 			'lepDR_minBBdr',
# 			'mass_minLLdr', 
# 			'mass_minBBdr',
			]

isEMlist = ['E','M']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['2','3','3p','4p']
if not categorize: nbtaglist = ['2p']
njetslist = ['4','5','6p']

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.system('cp ../analyze.py doHists.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

count=0
for iplot in iPlotList:
	for cat in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist)):
		if skip(cat[4],cat[3]): continue #DO YOU WANT TO HAVE THIS??
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
                  
