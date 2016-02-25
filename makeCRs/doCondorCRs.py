import os,sys,datetime

thisDir = os.getcwd()
outputDir = thisDir+'/'

isTTbarCR = 0 # 1:TTBar, 0:Wjets

isEMlist =['E','M']
if isTTbarCR: 
	nWtaglist = ['0p']
	nbtaglist = ['0','1','2p']
else: 
	nWtaglist = ['0','1p']
	nbtaglist = ['0']

cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
if isTTbarCR: pfix='ttbar'
else: pfix='wjets'
pfix+='_JECv7JSF'
pfix+='_'+datestr#+'_'+timestr

outDir = outputDir+pfix
if not os.path.exists(outDir): os.system('mkdir '+outDir)
os.chdir(outDir)

for cat in list(itertools.product(isEMlist,nWtaglist,nbtaglist)):
	isEM,nWtag,nbtag=cat[0],cat[1],cat[2]
	print isEM+'_nW'+nWtag+'_nB'+nbtag
	if not os.path.exists(outDir+'/'+isEM+'_nW'+nWtag+'_nB'+nbtag): os.system('mkdir '+isEM+'_nW'+nWtag+'_nB'+nbtag)
	os.chdir(isEM+'_nW'+nWtag+'_nB'+nbtag)			
	
	dict={'dir':outputDir,'isTTbarCR':isTTbarCR,'isEM':isEM,'nWtag':nWtag,'nbtag':nbtag}
	
	jdf=open('condor.job','w')
	jdf.write(
"""universe = vanilla
Executable = %(dir)s/doCondorCRs.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
notify_user = Sinan_Sagir@brown.edu

arguments      = ""

Output = condor.out
Error = condor.err
Log = condor.log
Notification = Error
Arguments = %(dir)s %(isTTbarCR)s %(isEM)s %(nWtag)s %(nbtag)s

Queue 1"""%dict)
	jdf.close()

	os.system('condor_submit condor.job')
	os.chdir('..')


                  