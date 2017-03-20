import os,sys,datetime,itertools
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from utils import *

thisDir = os.getcwd()
outputDir = thisDir+'/'

region='SR' #SR,CR --> matters only when plotting kinematics
categorize=1 #1==categorize into t/W/b/j, 0==only split into flavor
#sigTrained='180' #Low/Med/High 
sigTrainedList=[str(item) for item in ['Low','Med','High']]#,180,200,220,250,300,350,400,500,800,1000,2000,3000]]

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)

iPlotList = [#distribution name as defined in "doHists.py"
# 			'NPV',
# 			'MTlmet',
# 			'topPt',
# 			'Bjet1Pt',
# 			'lepPt',
# 			'lepEta',
# 			'JetEta',
# 			'JetPt',
# 			'Jet1Pt',
# 			'Jet2Pt',
# 			'Jet3Pt',
# 			'mindeltaR',
# 			'MET',
# 			'NJets',
# 			'NBJetsNoSF',
# 			'NBJets',
# 			'PtRel',
			
# 			'HT',
# 			'ST',
# 			'minMlb',
# 			'BDT',
			
# 			'STpBDT',
			'HTpBDT',
			'minMlbpBDT',
			
# 			'deltaPhilepJets0',
# 			'deltaPhilepJets1',
# 			'deltaPhilepJets2',
# 			'deltaRlepJets0',
# 			'deltaRlepJets1',
# 			'deltaRlepJets2',
# 			'deltaR_lepBJets0',
# 			'mindeltaRlb',
# 			'masslepJets0',
# 			'masslepJets1',
# 			'masslepJets2',
# 			'masslepBJets0',
# 			'LeadJetPt',
# 			'aveBBdr',
# 			'minBBdr',
# 			'mass_maxJJJpt',
# 			'mass_maxBBmass',
# 			'mass_maxBBpt',
# 			'lepDR_minBBdr',
# 			'mass_minLLdr', 
# 			'mass_minBBdr',
# 			'mass_lepBB_minBBdr',
# 			'mass_lepJJ_minJJdr',
			]

isEMlist = ['E','M']
nttaglist = ['0p']
nWtaglist = ['0p']
nbtaglist = ['1','2','2p','3p']
njetslist = ['3','4','5','6p']
# nbtaglist = ['1','2','3p']
# njetslist = ['4p']
# nbtaglist = ['1','1p','2p']
# njetslist = ['3p']
if not categorize: 
	nbtaglist = ['1p']
	njetslist = ['3p']
catList = list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))

for sigTrained in sigTrainedList:
	pfix='templates'
	if not categorize: pfix='kinematics_'+region
	pfix+='_BDTGhalfTT_Brown_16vars_M'+sigTrained+'_'+date#+'_'+time

	outDir = outputDir+pfix
	if not os.path.exists(outDir): os.system('mkdir '+outDir)
	os.chdir(outputDir)
	os.system('cp ../analyze.py doHists.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
	os.chdir(outDir)

	count=0
	for iplot in iPlotList:
		for cat in catList:
			if skip(cat[4],cat[3]) and categorize: continue #DO YOU WANT TO HAVE THIS??
			catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
			print "Training: "+sigTrained+", iPlot: "+iplot+", cat: "+catDir
			if not os.path.exists(outDir+'/'+catDir): os.system('mkdir '+catDir)
			os.chdir(catDir)			
	
			dict={'dir':outputDir,'iPlot':iplot,'region':region,'isCategorized':categorize,'sigTrained':sigTrained,
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
Arguments = %(dir)s %(iPlot)s %(region)s %(isCategorized)s %(isEM)s %(nttag)s %(nWtag)s %(nbtag)s %(njets)s %(sigTrained)s
Queue 1"""%dict)
			jdf.close()

			os.system('condor_submit condor.job')
			os.chdir('..')
			count+=1

print "Total jobs submitted:", count
                  
