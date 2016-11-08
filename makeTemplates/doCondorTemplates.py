import os,sys,datetime,itertools

thisDir = os.getcwd()
outputDir = thisDir+'/'

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='templates_ST'
pfix+='_'+date#+'_'+time

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.system('cp ../analyze.py doHists.py ../weights.py ../samples.py doCondorTemplates.py doCondorTemplates.sh '+outDir+'/')
os.chdir(outDir)

isEMlist =['E','M']
nttaglist=['0','1p']
nWtaglist=['0','1p']
nbtaglist=['1','2p']

#Optimized selections:
lepPtCutList  = [30]
metCutList    = [100]
njetsCutList  = [4]
nbjetsCutList = [0]
drCutList     = [1]
jet1PtCutList = [250]
jet2PtCutList = [50]
jet3PtCutList = [0]
#'lep30_MET150_NJets4_NBJets0_DR1_1jet450_2jet150_3jet0', #minMlb
#'lep30_MET100_NJets4_NBJets0_DR1_1jet250_2jet50_3jet0', #ST

cutConfigs = list(itertools.product(lepPtCutList,jet1PtCutList,jet2PtCutList,metCutList,njetsCutList,nbjetsCutList,jet3PtCutList,drCutList))

count=0
for conf in cutConfigs:
	lepPtCut,jet1PtCut,jet2PtCut,metCut,njetsCut,nbjetsCut,jet3PtCut,drCut=conf[0],conf[1],conf[2],conf[3],conf[4],conf[5],conf[6],conf[7]
	if jet2PtCut >= jet1PtCut or jet3PtCut >= jet1PtCut: continue
	if jet3PtCut >= jet2PtCut: continue
	cutString = 'lep'+str(int(lepPtCut))+'_MET'+str(int(metCut))+'_NJets'+str(int(njetsCut))
	#cutString+= '_NBJets'+str(int(nbjetsCut))
	cutString+= '_DR'+str(drCut) + '_1jet'+str(int(jet1PtCut))+'_2jet'+str(int(jet2PtCut))#+'_3jet'+str(int(jet3PtCut))+'_4jet'+str(int(jet4PtCut))+'_5jet'+str(int(jet5PtCut))
	#cutString+= '_1Wjet'+str(Wjet1PtCut)+'_1bjet'+str(bjet1PtCut)+'_HT'+str(htCut)+'_ST'+str(stCut)+'_minMlb'+str(minMlbCut)
	print cutString
	if not os.path.exists(outDir+'/'+cutString): os.system('mkdir '+cutString)
	os.chdir(cutString)
	for cat in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist)):
		catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]
		print catDir
		if not os.path.exists(outDir+'/'+cutString+'/'+catDir): os.system('mkdir '+catDir)
		os.chdir(catDir)

		dict={'dir':outputDir,'lepPtCut':lepPtCut,'jet1PtCut':jet1PtCut,'jet2PtCut':jet2PtCut,
			  'metCut':metCut,'njetsCut':njetsCut,'nbjetsCut':nbjetsCut,'jet3PtCut':jet3PtCut,
			  'drCut':drCut,'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3]}
		jdf=open('condor.job','w')
		jdf.write(
"""universe = vanilla
Executable = %(dir)s/doCondorTemplates.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 3072
arguments = ""
Output = condor.out
Error = condor.err
Log = condor.log
Notification = Error
Arguments = %(dir)s %(lepPtCut)s %(jet1PtCut)s %(jet2PtCut)s %(metCut)s %(njetsCut)s %(nbjetsCut)s %(jet3PtCut)s %(drCut)s %(isEM)s %(nttag)s %(nWtag)s %(nbtag)s
Queue 1"""%dict)
		jdf.close()
		
		os.system('condor_submit condor.job')
		os.chdir('..')
		count+=1
	os.chdir('..')
									
print "Total jobs submitted:", count



                
