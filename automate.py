import os

trainings=[

{
'year':'R17',
'variable':'BDT',
'postfix':'66vars_4j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_66vars_mDepth2_4j_year2017/'
},
{
'year':'R17',
'variable':'BDT',
'postfix':'66vars_6j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_66vars_mDepth2_6j_year2017/'
},
{
'year':'R17',
'variable':'BDT',
'postfix':'73vars_4j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_4j_year2017/'
},
{
'year':'R17',
'variable':'BDT',
'postfix':'73vars_6j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_6j_year2017/'
},

{
'year':'R18',
'variable':'BDT',
'postfix':'66vars_4j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_66vars_mDepth2_4j_year2018/'
},
{
'year':'R18',
'variable':'BDT',
'postfix':'66vars_6j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_66vars_mDepth2_6j_year2018/'
},
{
'year':'R18',
'variable':'BDT',
'postfix':'73vars_4j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_4j_year2018/'
},
{
'year':'R18',
'variable':'BDT',
'postfix':'73vars_6j_pt20',
'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_08262020_step3_wenyu/BDT_SepRank6j73vars2017year_73vars_mDepth2_6j_year2018/'
},

]

combinations = [
'66vars_4j_pt20_BDT',
'66vars_6j_pt20_BDT',
'73vars_4j_pt20_BDT',
'73vars_6j_pt20_BDT'
 ]

#which step would you like to run?
#1 doCondorTemplates
#2 doTemplates + modifyBinning + plotTemplates
#3 dataCard + limit + significance
#4 combination limit + significance
step=1

if step==1:
	os.chdir('makeTemplates')
	for train in trainings:
		os.system('python doCondorTemplates.py '+train['year']+' '+train['variable']+' '+train['postfix']+' '+train['path'])
	os.chdir('..')

if step==2:
	os.chdir('makeTemplates')
	for train in trainings:
		shell_name = 'condor_step2_'+train['postfix']+'.sh'
		shell=open(shell_name,'w')
		shell.write(
'source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd /home/eusai/4t/CMSSW_10_2_16_UL/src\n\
eval `scramv1 runtime -sh`\n\
cd '+os.cwd()+'\n\
python doTemplates.py '+train['year']+' '+train['postfix']+'\n\
python modifyBinning.py '+train['year']+' '+train['variable']+' '+train['postfix']+'\n\
python plotTemplates.py '+train['year']+' '+train['variable']+' '+train['postfix']+'\n')
		shell.close()
		jdf_name = 'condor_step2_'+train['postfix']+'.job'
		jdf=open(jdf_name,'w')
		jdf.write(
'universe = vanilla\n\
Executable = '+os.cwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 3072\n\
Output = '+os.cwd()+'/log/'+shell_name.split('.')[0]+'.out\n\
Error = '+os.cwd()+'/log/'+shell_name.split('.')[0]+'.err\n\
Log = '+os.cwd()+'/log/'+shell_name.split('.')[0]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
		jdf.close()
		os.system('condor_submit '+jdf_name)
	os.chdir('..')


if step==3:
	os.chdir('combineLimits')
	for train in trainings:
		shell_name = 'condor_step3_'+train['postfix']+'.sh'
		shell=open(shell_name,'w')
		shell.write(
'source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd /home/eusai/4t/CMSSW_10_2_16_UL/src\n\
eval `scramv1 runtime -sh`\n\
cd '+os.cwd()+'\n\
python dataCard.py '+train['year']+' '+train['variable']+' '+train['postfix']+'\n\
cd limits_'+train['year']+'_'+train['postfix']+'_'+train['variable']+'\n\
combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> sig.txt\n\
combine -M AsymptoticLimits cmb/workspace.root --run=blind --cminDefaultMinimizerStrategy 0 &> asy.txt\n\
cd ..\n')
		shell.close()
		jdf_name = 'condor_step3_'+train['postfix']+'.job'
		jdf=open(jdf_name,'w')
		jdf.write(
'universe = vanilla\n\
Executable = '+os.cwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 3072\n\
Output = '+os.cwd()+'/log/'+shell_name.split('.')[0]+'.out\n\
Error = '+os.cwd()+'/log/'+shell_name.split('.')[0]+'.err\n\
Log = '+os.cwd()+'/log/'+shell_name.split('.')[0]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
		jdf.close()
		os.system('condor_submit '+jdf_name)
	os.chdir('..')


if step==4:
	os.chdir('combineLimits')
	for combo in combinations:

		shell_name = 'condor_step4_'+combo+'.sh'
		shell=open(shell_name,'w')
		shell.write(
'source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd /home/eusai/4t/CMSSW_10_2_16_UL/src\n\
eval `scramv1 runtime -sh`\n\
cd '+os.cwd()+'\n\
combineCards.py R17=limits_R17_'+combo+'/cmb/combined.txt.cmb R18=limits_R18_'+combo+'/cmb/combined.txt.cmb &> BDTcomb/'+combo+'.txt\n\
text2workspace.py  BDTcomb/'+combo+'.txt  -o BDTcomb/'+combo+'.root\n\
combine -M Significance BDTcomb/'+combo+'.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> BDTcomb/sig_'+combo+'.txt\n\
combine -M AsymptoticLimits BDTcomb/'+combo+'.root --run=blind --cminDefaultMinimizerStrategy 0 &> BDTcomb/asy_'+combo+'.txt\n')
		shell.close()
		jdf_name = 'condor_step4_'+combo+'.job'
		jdf=open(jdf_name,'w')
		jdf.write(
'universe = vanilla\n\
Executable = '+os.cwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 3072\n\
Output = '+os.cwd()+'/log/'+shell_name.split('.')[0]+'.out\n\
Error = '+os.cwd()+'/log/'+shell_name.split('.')[0]+'.err\n\
Log = '+os.cwd()+'/log/'+shell_name.split('.')[0]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
		jdf.close()
		os.system('condor_submit '+jdf_name)
	os.chdir('..')

# python makeTemplates/doCondorTemplates.py R17 BDT 40vars_6j /mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_05182020_step3_wenyu/BDT_SepRank6j73vars2017year40top_40vars_mDepth2_4j_year2018/
# python makeTemplates/doTemplates.py R17 40vars_6j
# python makeTemplates/modifyBinning.py R17 BDT 40vars_6j
# python makeTemplates/plotTemplates.py R17 BDT 40vars_6j
# python combineLimits/dataCard.py R17 BDT 40vars_6j