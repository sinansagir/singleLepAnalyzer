import os,sys,datetime,itertools

thisDir = os.getcwd()
outputDir = thisDir+'/'

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='templates_minMlb_ObjRev'
#pfix+='_'+date#+'_'+time

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.system('cp analyze.py doHists.py weights.py samples.py doCondorThetaTemplates.py doCondorThetaTemplates.sh '+outDir+'/')
os.chdir(outDir)

isEMlist =['E','M']
#nttaglist=['0','1p']
#nWtaglist=['0','0p','1p']
#nbtaglist=['0','1','2','2p','3p']
nttaglist=['0p']
nWtaglist=['0','1p']
nbtaglist=['0','1','2','3p']

#Basic kinematic cuts optimization configuration (w/o shapes) -- selected TpTp optimum cuts -- Jan 19, 2016:
lepPtCutList  = [40]
jet1PtCutList = [300]
jet2PtCutList = [150]
jet3PtCutList = [100]
metCutList    = [75]
njetsCutList  = [3]
nbjetsCutList = [0]
drCutList     = [1]

cutConfigs = list(itertools.product(lepPtCutList,jet1PtCutList,jet2PtCutList,metCutList,njetsCutList,nbjetsCutList,jet3PtCutList,drCutList))

count=0
for conf in cutConfigs:
	lepPtCut,jet1PtCut,jet2PtCut,metCut,njetsCut,nbjetsCut,jet3PtCut,drCut=conf[0],conf[1],conf[2],conf[3],conf[4],conf[5],conf[6],conf[7]
	if jet2PtCut >= jet1PtCut or jet3PtCut >= jet1PtCut: continue
	if jet3PtCut >= jet2PtCut: continue
	cutString = 'SelectionFile'

	"""
	'lep'+str(int(lepPtCut))+'_MET'+str(int(metCut))+'_1jet'+str(int(jet1PtCut))+'_2jet'+str(int(jet2PtCut))+'_NJets'+str(int(njetsCut))+'_NBJets'+str(int(nbjetsCut))+'_3jet'+str(int(jet3PtCut))+'_DR'+str(drCut)
	"""
	print cutString
	if not os.path.exists(outDir+'/'+cutString): os.system('mkdir '+cutString)
	os.chdir(cutString)
	for cat in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist)):

		if cat[1]=='1p':
			if cat[2] != '0p': continue
			if cat[3] == '2' or cat[3] == '3p': continue
		if cat[1]=='0':
			if cat[2] == '0p': continue
			if cat[3] == '2p': continue

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
Executable = %(dir)s/doCondorThetaTemplates.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
notify_user = Sinan_Sagir@brown.edu
request_memory = 3072

arguments      = ""

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

#Basic kinematic cuts optimization configuration (w/o shapes) -- Step1:
# lepPtCutList  = [40,50,60,80,100]
# jet1PtCutList = [125,150,200,300,400,500]
# jet2PtCutList = [75,100,150,200]
# metCutList    = [40,50,75,100,125]
# njetsCutList  = [3,4,5]
# nbjetsCutList = [0]
# jet3PtCutList = [30,40,50,75,100,150,200]
# jet4PtCutList = [0]
# jet5PtCutList = [0]
# drCutList     = [1]
# Wjet1PtCutList= [0]
# bjet1PtCutList= [0]
# htCutList     = [0]
# stCutList     = [0]
# minMlbCutList = [0]

#Additional kinematic cuts optimization configuration (w/o shapes) for minMlb -- Step2:
# lepPtCutList  = [80]
# jet1PtCutList = [300]
# jet2PtCutList = [200]
# metCutList    = [40]
# njetsCutList  = [3]
# nbjetsCutList = [0]
# jet3PtCutList = [100]
# jet4PtCutList = [0]
# jet5PtCutList = [0]
# drCutList     = [0,1,1.25,1.5]
# Wjet1PtCutList= [0,200,250,300,400]
# bjet1PtCutList= [0,100,150,200,300]
# htCutList     = [0]
# stCutList     = [0,600,800,1000,1200,1500,1750,2000]
# minMlbCutList = [0]


                  
