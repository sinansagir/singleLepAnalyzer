import os,sys,datetime,itertools

thisDir = os.getcwd()
outputDir = thisDir+'/'

region='SR' #PS,SR,TTCR,WJCR
categorize=1 #1==categorize into t/W/b/j, 0==only split into flavor

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
if region=='TTCR': pfix='ttbar_PreApp'
elif region=='WJCR': pfix='wjets_PreApp'
else: pfix='templates_Optimization_PreApp'
if not categorize: pfix='kinematics_'+region+'_NoSF_PreApp'
#pfix+='_'+date+'_wJSF'#+'_'+time

iPlotList = [#distribution name as defined in "doHists.py"
	'minMlbST',
	]

jet1PtCutList = [200, 300, 400]
jet2PtCutList = [100, 150, 200, 300]
metCutList    = [60, 75, 100]
jet3PtCutList = [50, 100, 150, 200]

cutConfigs = list(itertools.product(jet1PtCutList,jet2PtCutList,metCutList,jet3PtCutList))


isEMlist = ['E','M']
if region=='SR' or 'CR' in region: nHtaglist = ['0','1b','2b']
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
	if region=='TTCR': nbtaglist = ['1p']
	if region=='HTAG': 
		nHtaglist = ['1p']
		nbtaglist = ['1p']
njetslist = ['3p']
if region=='PS': njetslist = ['3p']

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.system('cp ../analyze.py doHists.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

catlist = list(itertools.product(isEMlist,nHtaglist,nWtaglist,nbtaglist,njetslist))
print catlist

count=0
for conf in cutConfigs:
	jet1PtCut,jet2PtCut,metCut,jet3PtCut=conf[0],conf[1],conf[2],conf[3]
	if jet2PtCut >= jet1PtCut or jet3PtCut >= jet1PtCut: continue
	if jet3PtCut >= jet2PtCut: continue
	if jet1PtCut+jet2PtCut+jet3PtCut < 400: continue
	cutString = 'MET'+str(int(metCut))+'_1jet'+str(int(jet1PtCut))+'_2jet'+str(int(jet2PtCut))+'_3jet'+str(int(jet3PtCut))

	print cutString
	if not os.path.exists(outDir+'/'+cutString): os.system('mkdir '+cutString)
	os.chdir(cutString)

	for cat in list(itertools.product(isEMlist,nHtaglist,nWtaglist,nbtaglist,njetslist)):
		catDir = cat[0]+'_nH'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]		
		if categorize:
			if 'b' in cat[1]:
				#print 'got an H tag'
				if cat[2] != '0p': continue
				if (region == 'SR' and cat[3] != '1p') or (region == 'WJCR' and cat[3] != '0'): continue
			else:
				#print 'no H tag'
				if (region == 'SR' or region == 'WJCR') and cat[2] == '0p': continue
				if cat[3] == '1p': continue
		print catDir
		if not os.path.exists(outDir+'/'+cutString+'/'+catDir): os.system('mkdir '+catDir)
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
                  
