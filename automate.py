import os,time

cmsswbase = '/user_data/ssagir/CMSSW_10_2_13/src'

trainings=[]

years=['18']
prod={
'16':'Oct2019',
'17':'Oct2019',
'18':'Oct2019',
}

vrs=['BDT']

for y in years:
		tmp={
		'year':'R'+y,
		'variable':vrs,#['BDT'],
		'postfix':'ABCDnn_nJ6pnB2p_v2',
		'path':'/isilon/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+y+'_'+prod[y]+'_4t_05202022_step3_40vars_6j_NJetsCSV_nickBDTrun',
		}
		trainings.append(tmp)

combinations = [

{
	'variable':'BDT',
	'postfix':'splitjes_R18binsNj8p'
},	

]

#which step would you like to run?
#1 doCondorTemplates
#2 doTemplates
#3 modifyBinning + plotTemplates
#4 dataCard + limit + significance
#5 combination limit + significance
#6 print results
step=2
myconfig = '_R18binsNj8p'

if step==1:
	os.chdir('makeTemplates')
	for train in trainings:
		for v in train['variable']:
			os.system('python doCondorTemplates.py '+train['year']+' '+v+' '+train['postfix']+' '+train['path'])
			time.sleep(2)
	os.chdir('..')

if step==2:
	os.chdir('makeTemplates')
	for train in trainings:
		shell_name = 'cfg/condor_step2_'+train['year']+'_'+train['postfix']+'.sh'
		shell=open(shell_name,'w')
		shell.write(
'#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd '+cmsswbase+'\n\
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
request_memory = 5000\n\
Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.out\n\
Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.err\n\
Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
		jdf.close()
		os.system('condor_submit '+jdf_name)
		print(shell_name)
		# os.system('source '+shell_name+' & ')
		time.sleep(1)
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
cd '+cmsswbase+'\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
# python modifyTemplates.py '+train['year']+' '+v+' '+train['postfix']+'\n\
python modifyBinning.py '+train['year']+' '+v+' '+train['postfix']+'\n\
# python plotFullRun2.py '+v+' '+train['postfix']+'\n\
# python plotTemplates.py '+train['year']+' '+v+' '+train['postfix']+'\n')
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
			# print('python modifyTemplates.py '+train['year']+' '+v+' '+train['postfix'])
			os.system('condor_submit '+jdf_name)
			# print(shell_name)
			# os.system('source '+shell_name+' & ')
			# time.sleep(2)
	os.chdir('..')



if step==4:
	os.chdir('combineLimits')
	for train in trainings:
		for v in train['variable']:
			shell_name = 'cfg/condor_step4_'+train['year']+'_'+train['postfix']+myconfig+'_'+v+'.sh'
			shell=open(shell_name,'w')
			shell.write(
'#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd '+cmsswbase+'\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
python dataCard.py '+train['year']+' '+v+' '+train['postfix']+'\n\
#python dataCardDecoupleTTbarUncs.py '+train['year']+' '+v+' '+train['postfix']+'\n\
cd limits_'+train['year']+'_'+train['postfix']+myconfig+'_'+v+'\n\
combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> sig_exp.txt\n\
combine -M Significance cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> sig_obs.txt\n\
combine -M AsymptoticLimits cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> asy.txt\n\
# combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> sig_exp_freezetth.txt\n\
# combine -M Significance cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> sig_obs_freezetth.txt\n\
# combine -M AsymptoticLimits cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> asy_freezetth.txt\n\
# combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> sig_exp_freezetthf.txt\n\
# combine -M Significance cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> sig_obs_freezetthf.txt\n\
# combine -M AsymptoticLimits cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> asy_freezetthf.txt\n\
# combine -M MultiDimFit cmb/workspace.root --cminDefaultMinimizerStrategy 0 &> mlfit.txt\n\
cd ..\n')
			shell.close()
			jdf_name = 'cfg/condor_step4_'+train['year']+'_'+train['postfix']+myconfig+'_'+v+'.job'
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
cd '+cmsswbase+'\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
combineCards.py R16=limits_R16_'+combo+'/cmb/combined.txt.cmb R17=limits_R17_'+combo+'/cmb/combined.txt.cmb R18=limits_R18_'+combo+'/cmb/combined.txt.cmb &> BDTcomb/'+combo+'.txt\n\
text2workspace.py  BDTcomb/'+combo+'.txt  -o BDTcomb/'+combo+'.root\n\
combine -M Significance BDTcomb/'+combo+'.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> BDTcomb/sig_exp_'+combo+'.txt\n\
combine -M Significance BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> BDTcomb/sig_obs_'+combo+'.txt\n\
combine -M AsymptoticLimits BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> BDTcomb/asy_'+combo+'.txt\n\
# combine -M Significance BDTcomb/'+combo+'.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> BDTcomb/sig_exp_'+combo+'_freezetth.txt\n\
# combine -M Significance BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> BDTcomb/sig_obs_'+combo+'_freezetth.txt\n\
# combine -M AsymptoticLimits BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> BDTcomb/asy_'+combo+'_freezetth.txt\n\
# combine -M Significance BDTcomb/'+combo+'.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> BDTcomb/sig_exp_'+combo+'_freezetthf.txt\n\
# combine -M Significance BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> BDTcomb/sig_obs_'+combo+'_freezetthf.txt\n\
# combine -M AsymptoticLimits BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> BDTcomb/asy_'+combo+'_freezetthf.txt\n\
\n')
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

def printlim(spec,year,variable,isComb,pfix):

	try:
		inputDir='limits_'+year+'_'+spec+'_'+variable
		sigExpFile = inputDir+'/sig_exp'+pfix+'.txt'
		sigObsFile = inputDir+'/sig_obs'+pfix+'.txt'
		limFile = inputDir+'/asy'+pfix+'.txt'
		if isComb:
			inputDir='BDTcomb/'
			sigExpFile = inputDir+'/sig_exp_'+spec+'_'+variable+pfix+'.txt'
			sigObsFile = inputDir+'/sig_obs_'+spec+'_'+variable+pfix+'.txt'
			limFile = inputDir+'/asy_'+spec+'_'+variable+pfix+'.txt'

		sigExpData = open(sigExpFile,'r').read()
		sigExplines = sigExpData.split('\n')
		sigObsData = open(sigObsFile,'r').read()
		sigObslines = sigObsData.split('\n')
		limData = open(limFile,'r').read()
		limlines = limData.split('\n')
		theSigExp = ''
		theSigObs = ''
		theLim = ['']*6
		for line in sigExplines:
			if line.startswith('Significance:'): theSigExp = line.split()[-1]
		for line in sigObslines:
			if line.startswith('Significance:'): theSigObs = line.split()[-1]
		for line in limlines:
			if line.startswith('Observed Limit:'): theLim[5] =  "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected  2.5%:'): theLim[0] =  "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 16.0%:'): theLim[1] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 50.0%:'): theLim[2] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 84.0%:'): theLim[3] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 97.5%:'): theLim[4] = "{:.2f}".format(float(line.split()[-1])*12)
		print year+' , '+variable+' , '+spec+pfix+' , '+theSigObs+' , '+theSigExp+' , '+theLim[5]+' , '+theLim[2]+' , '+theLim[1]+' , '+theLim[3]+' , '+theLim[0]+' , '+theLim[4]
	except Exception as e:
		pass

if step==6:
	# print 'Year , Var , Specifications , Exp. Sig. , Obs. Sig. , -2sigma, -1sigma, central, +1sigma, +2sigma, Obs. Limit'
	print 'Year , Var , Specifications , Obs. Sig. , Exp. Sig. , Obs. Limit , central , -1sigma, +1sigma, -2sigma , +2sigma'
	os.chdir('combineLimits')
	for train in trainings:
		for v in train['variable']:
			printlim(train['postfix'] , train['year'] , v ,False,'')
			# printlim(train['postfix'] , train['year'] , v ,False,'_freezetth')
			# printlim(train['postfix'] , train['year'] , v ,False,'_freezetthf')
	for combo in combinations:
		printlim(combo['postfix'],'R16+17+18',combo['variable'],True,'')
		# printlim(combo['postfix'],'R16+17+18',combo['variable'],True,'_freezetth')
		# printlim(combo['postfix'],'R16+17+18',combo['variable'],True,'_freezetthf')
	os.chdir('..')

# standalone commands
# in makeTemplates:
# python doCondorTemplates.py R17 BDT 40vars_6j /mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_05182020_step3_wenyu/BDT_SepRank6j73vars2017year40top_40vars_mDepth2_4j_year2018/
# python doTemplates.py R17 40vars_6j
# python modifyBinning.py R17 BDT 40vars_6j
# python plotTemplates.py R17 BDT 40vars_6j
# in combineLimits:
# python dataCard.py R17 BDT 40vars_6j
