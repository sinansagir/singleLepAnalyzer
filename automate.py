import os

trainings=[

{
'year':'R17',
'variable':['BDT','HT'],
'postfix':'66vars_4j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_66vars_mDepth2_4j_year2017/'
},
{
'year':'R17',
'variable':['BDT','HT'],
'postfix':'66vars_6j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_66vars_mDepth2_6j_year2017/'
},
{
'year':'R17',
'variable':['BDT','HT'],
'postfix':'73vars_4j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_4j_year2017/'
},
{
'year':'R17',
'variable':['BDT','HT'],
'postfix':'73vars_6j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_6j_year2017/'
},

{
'year':'R18',
'variable':['BDT','HT'],
'postfix':'66vars_4j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_66vars_mDepth2_4j_year2018/'
},
{
'year':'R18',
'variable':['BDT','HT'],
'postfix':'66vars_6j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_66vars_mDepth2_6j_year2018/'
},
{
'year':'R18',
'variable':['BDT','HT'],
'postfix':'73vars_4j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_4j_year2018/'
},
{
'year':'R18',
'variable':['BDT','HT'],
'postfix':'73vars_6j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_6j_year2018/'
},

]

combinations = [
{
	'variable':'BDT',
	'postfix':'66vars_4j_pt20'
},
{
	'variable':'BDT',
	'postfix':'66vars_6j_pt20'
},
{
	'variable':'BDT',
	'postfix':'73vars_4j_pt20'
},
{
	'variable':'BDT',
	'postfix':'73vars_6j_pt20'
}
]

#which step would you like to run?
#1 doCondorTemplates
#2 doTemplates
#3 modifyBinning + plotTemplates
#4 dataCard + limit + significance
#5 combination limit + significance
#6 print results
step=1

if step==1:
	os.chdir('makeTemplates')
	for train in trainings:
		os.system('python doCondorTemplates.py '+train['year']+' '+train['variable']+' '+train['postfix']+' '+train['path'])
	os.chdir('..')

if step==2:
	os.chdir('makeTemplates')
	for train in trainings:
		shell_name = 'cfg/condor_step2_'+train['year']+'_'+train['postfix']+'.sh'
		shell=open(shell_name,'w')
		shell.write(
'#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd /home/eusai/4t/CMSSW_10_2_16_UL/src\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
python doTemplates.py '+train['year']+' '+train['postfix']+'\n')
		shell.close()
		jdf_name = 'cfg/condor_step2_'+train['year']+'_'+train['postfix']+'.job'
		jdf=open(jdf_name,'w')
		jdf.write(
'universe = vanilla\n\
Executable = '+os.getcwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 3072\n\
Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.out\n\
Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.err\n\
Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
		jdf.close()
		os.system('condor_submit '+jdf_name)
	os.chdir('..')



if step==3:
	os.chdir('makeTemplates')
	for train in trainings:
		for v in train['variable']:
			shell_name = 'cfg/condor_step3_'+train['year']+'_'+train['postfix']+'_'+v+'.sh'
			shell=open(shell_name,'w')
			shell.write(
'#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd /home/eusai/4t/CMSSW_10_2_16_UL/src\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
python modifyBinning.py '+train['year']+' '+v+' '+train['postfix']+'\n\
python plotTemplates.py '+train['year']+' '+v+' '+train['postfix']+'\n')
			shell.close()
			jdf_name = 'cfg/condor_step3_'+train['year']+'_'+train['postfix']+'_'+v+'.job'
			jdf=open(jdf_name,'w')
			jdf.write(
'universe = vanilla\n\
Executable = '+os.getcwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 3072\n\
Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.out\n\
Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.err\n\
Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
			jdf.close()
			os.system('condor_submit '+jdf_name)
	os.chdir('..')



if step==4:
	os.chdir('combineLimits')
	for train in trainings:
		for v in train['variable']:
			shell_name = 'cfg/condor_step4_'+train['year']+'_'+train['postfix']+'_'+v+'.sh'
			shell=open(shell_name,'w')
			shell.write(
'#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd /home/eusai/4t/CMSSW_10_2_16_UL/src\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
python dataCard.py '+train['year']+' '+v+' '+train['postfix']+'\n\
cd limits_'+train['year']+'_'+train['postfix']+'_'+v+'\n\
combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> sig.txt\n\
combine -M AsymptoticLimits cmb/workspace.root --run=blind --cminDefaultMinimizerStrategy 0 &> asy.txt\n\
cd ..\n')
			shell.close()
			jdf_name = 'cfg/condor_step4_'+train['year']+'_'+train['postfix']+'_'+v+'.job'
			jdf=open(jdf_name,'w')
			jdf.write(
'universe = vanilla\n\
Executable = '+os.getcwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 3072\n\
Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.out\n\
Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.err\n\
Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
			jdf.close()
			os.system('condor_submit '+jdf_name)
	os.chdir('..')


if step==5:
	os.chdir('combineLimits')
	for c in combinations:
		combo=c['postfix']+'_'+c['variable']
		shell_name = 'cfg/condor_step5_'+combo+'.sh'
		shell=open(shell_name,'w')
		shell.write(
'#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd /home/eusai/4t/CMSSW_10_2_16_UL/src\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
combineCards.py R17=limits_R17_'+combo+'/cmb/combined.txt.cmb R18=limits_R18_'+combo+'/cmb/combined.txt.cmb &> BDTcomb/'+combo+'.txt\n\
text2workspace.py  BDTcomb/'+combo+'.txt  -o BDTcomb/'+combo+'.root\n\
combine -M Significance BDTcomb/'+combo+'.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> BDTcomb/sig_'+combo+'.txt\n\
combine -M AsymptoticLimits BDTcomb/'+combo+'.root --run=blind --cminDefaultMinimizerStrategy 0 &> BDTcomb/asy_'+combo+'.txt\n')
		shell.close()
		jdf_name = 'cfg/condor_step5_'+combo+'.job'
		jdf=open(jdf_name,'w')
		jdf.write(
'universe = vanilla\n\
Executable = '+os.getcwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 3072\n\
Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.out\n\
Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.err\n\
Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
		jdf.close()
		os.system('condor_submit '+jdf_name)
	os.chdir('..')

def printlim(spec,year,variable,isComb):

	inputDir='limits_'+year+'_'+spec+'_'+variable
	sigFile = inputDir+'/sig.txt'
	limFile = inputDir+'/asy.txt'
	if isComb:
		inputDir='BDTcomb/'
		sigFile = inputDir+'/sig_'+spec+'_'+variable+'.txt'
		limFile = inputDir+'/asy_'+spec+'_'+variable+'.txt'

	sigData = open(sigFile,'r').read()
	siglines = sigData.split('\n')
	limData = open(limFile,'r').read()
	limlines = limData.split('\n')
	theSig = ''
	theLim = ['']*5
	for line in siglines:
		if line.startswith('Significance:'): theSig = line.split()[-1]
	for line in limlines:
		if line.startswith('Expected  2.5%:'): theLim[0] =  "{:.2f}".format(float(line.split()[-1])*12)
		if line.startswith('Expected 16.0%:'): theLim[1] = "{:.2f}".format(float(line.split()[-1])*12)
		if line.startswith('Expected 50.0%:'): theLim[2] = "{:.2f}".format(float(line.split()[-1])*12)
		if line.startswith('Expected 84.0%:'): theLim[3] = "{:.2f}".format(float(line.split()[-1])*12)
		if line.startswith('Expected 97.5%:'): theLim[4] = "{:.2f}".format(float(line.split()[-1])*12)
	print year+' , '+variable+' , '+spec+' , '+theSig+' , '+theLim[0]+' , '+theLim[1]+' , '+theLim[2]+' , '+theLim[3]+' , '+theLim[4]


if step==6:
	print 'Year , Var , Specifications , Significance , -2sigma, -1sigma, central, +1sigma, +2sigma'
	os.chdir('combineLimits')
	for train in trainings:
		printlim(train['postfix'] , train['year'] , train['variable'],False)
	for combo in combinations:
		printlim(combo['postfix'],'R17+18',combo['variable'],True)
	os.chdir('..')

# standalone commands
# in makeTemplates:
# python doCondorTemplates.py R17 BDT 40vars_6j /mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_05182020_step3_wenyu/BDT_SepRank6j73vars2017year40top_40vars_mDepth2_4j_year2018/
# python doTemplates.py R17 40vars_6j
# python modifyBinning.py R17 BDT 40vars_6j
# python plotTemplates.py R17 BDT 40vars_6j
# in combineLimits:
# python dataCard.py R17 BDT 40vars_6j
