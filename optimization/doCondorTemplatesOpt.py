import os,sys,datetime,itertools

year='R17'

elPtCutList = [50]
muPtCutList = [50]
metCutList = [60]
mtCutList = [60]
jet1PtCutList = [0]
jet2PtCutList = [0]
jet3PtCutList = [0]
AK4HTCutList = [510]
AK4HTbCutList = [0]
maxJJJptCutList = [0]

cutConfigs = list(itertools.product(elPtCutList,muPtCutList,metCutList,mtCutList,jet1PtCutList,jet2PtCutList,jet3PtCutList,AK4HTCutList,AK4HTbCutList,maxJJJptCutList))

thisDir = os.getcwd()
outputDir = thisDir+'/'

cTime=datetime.datetime.now()
date='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
time='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='templates_'+date#+'_'+time

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
if year=='R17': 
	os.system('cp ../weights17.py ../weights.py')
	os.system('cp ../samples17.py ../samples.py')
elif year=='R18': 
	os.system('cp ../weights18.py ../weights.py')
	os.system('cp ../samples18.py ../samples.py')
os.system('cp ../analyze.py ../weights.py ../samples.py ../utils.py ../modSyst.py doHistsOpt.py doCondorTemplatesOpt.py doCondorTemplatesOpt.sh '+outDir+'/')
os.chdir(outDir)


count=0
for conf in cutConfigs:
	elPtCut,muPtCut,metCut,mtCut,jet1PtCut,jet2PtCut,jet3PtCut,AK4HTCut,AK4HTbCut,maxJJJptCut=conf[0],conf[1],conf[2],conf[3],conf[4],conf[5],conf[6],conf[7],conf[8],conf[9]
	if jet2PtCut > jet1PtCut or jet3PtCut > jet1PtCut or jet3PtCut > jet2PtCut: continue
	cutString = 'el'+str(int(elPtCut))+'_mu'+str(int(muPtCut))+'_MET'+str(int(metCut))+'_MT'+str(int(mtCut))
	cutString+= '_HT'+str(AK4HTCut)
	cutString+= '_HTb'+str(AK4HTbCut)+'_3Jpt'+str(maxJJJptCut)
	print cutString
	if not os.path.exists(outDir+'/'+cutString): os.system('mkdir '+cutString)
	os.chdir(cutString)

	dict={'dir':outDir,'elPtCut':elPtCut,'muPtCut':muPtCut,'metCut':metCut,'mtCut':mtCut,
		  'jet1PtCut':jet1PtCut,'jet2PtCut':jet2PtCut,'jet3PtCut':jet3PtCut,'AK4HTCut':AK4HTCut,
		  'AK4HTbCut':AK4HTbCut,'maxJJJptCut':maxJJJptCut}

	jdf=open('condor.job','w')
	jdf.write(
"""universe = vanilla
Executable = %(dir)s/doCondorTemplatesOpt.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 3072
Output = condor.out
Error = condor.err
Log = condor.log
Notification = Error
Arguments = %(dir)s %(elPtCut)s %(muPtCut)s %(metCut)s %(mtCut)s %(jet1PtCut)s %(jet2PtCut)s %(jet3PtCut)s %(AK4HTCut)s %(AK4HTbCut)s %(maxJJJptCut)s

Queue 1"""%dict)
	jdf.close()

	os.system('condor_submit condor.job')
	os.chdir('..')
	count+=1
									
print "Total jobs submitted:", count



                  