#!/usr/bin/python

import os,sys,fnmatch
from catconfigs import *

templateDir=os.getcwd()+'/../makeTemplates/templates_2019_8_21'
thetaConfigFile = os.getcwd()+'/theta_limit_template.py'
lumiInFile = '41p53fb'
doLimits = False #else it will run discovery significances

toFilter0 = []#['__'+item+'__' for item in toFilter0]

limitConfs = {#'<limit type>':[filter list]
# 			  'all':[],
# 			  'isE':['isM'], #only electron channel
# 			  'isM':['isE'], #only muon channel
# 			  'tag120' :[tag for tag in tags['all'] if tag not in tags['tag120']],
# 			  'tag63'  :[tag for tag in tags['all'] if tag not in tags['tag63']],
# 			  'tag54'  :[tag for tag in tags['all'] if tag not in tags['tag54']],
# 			  'tag45'  :[tag for tag in tags['all'] if tag not in tags['tag45']],
# 			  'tag36'  :[tag for tag in tags['all'] if tag not in tags['tag36']],
# 			  'tag27'  :[tag for tag in tags['all'] if tag not in tags['tag27']],
# 			  'noTW15' :[tag for tag in tags['all'] if tag not in tags['noTW15']],
# 			  'onlyW30':[tag for tag in tags['all'] if tag not in tags['onlyW30']],
# 			  'onlyT30':[tag for tag in tags['all'] if tag not in tags['onlyT30']],
# 			  'noTW18' :[tag for tag in tags['all'] if tag not in tags['noTW18']],
# 			  'onlyW36':[tag for tag in tags['all'] if tag not in tags['onlyW36']],
# 			  'onlyT36':[tag for tag in tags['all'] if tag not in tags['onlyT36']],

			  '165cats'  :[tag for tag in tags['allcats'] if tag not in tags['165cats']],
			  '144cats'  :[tag for tag in tags['allcats'] if tag not in tags['144cats']],
			  '102cats'  :[tag for tag in tags['allcats'] if tag not in tags['102cats']],
			  '90cats'   :[tag for tag in tags['allcats'] if tag not in tags['90cats']],
			  '75cats'   :[tag for tag in tags['allcats'] if tag not in tags['75cats']],
			  '60cats'   :[tag for tag in tags['allcats'] if tag not in tags['60cats']],
			  '45cats'   :[tag for tag in tags['allcats'] if tag not in tags['45cats']],
			  'noHOTtW15':[tag for tag in tags['allcats'] if tag not in tags['noHOTtW15']],
			  'onlyHOT30':[tag for tag in tags['allcats'] if tag not in tags['onlyHOT30']],
			  'onlyT30'  :[tag for tag in tags['allcats'] if tag not in tags['onlyT30']],
			  'onlyW30'  :[tag for tag in tags['allcats'] if tag not in tags['onlyW30']],
			  }
#for cat in catList: limitConfs[cat]=[item for item in catList if item!=cat]

limitType = '_lim'
if not doLimits:
	limitType = '_disc'
	thetaConfigFile = os.getcwd()+'/theta_disc_template.py'
outputDir = '/user_data/ssagir/fourtops_limits_2019/'+templateDir.split('/')[-1]+limitType+'/'
if os.path.exists(outputDir):
	 print "The directory",outputDir,"exists!!! I will not overwrite it. Please specify a different output directory or remove the existing one ..."
	 os._exit(1)
else: os.system('mkdir '+outputDir)

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)
            
rootfilelist = []
for rootfile in findfiles(templateDir, '*.root'):
    if 'rebinned_stat0p3' not in rootfile: continue
    #if 'BDT' not in rootfile: continue
    if 'plots' in rootfile: continue
    if 'YLD' in rootfile: continue
    rootfilelist.append(rootfile)

confile = open(thetaConfigFile, 'rU')
thetaConfigLines = confile.readlines()
confile.close()

def makeThetaConfig(rFile,outDir,toFilter):
	with open(outDir+'/'+rFile.split('/')[-1][:-5]+'.py','w') as fout:
		for line in thetaConfigLines:
			if line.startswith('input ='): fout.write('input = \''+rFile+'\'')
			elif line.startswith('    model = build_model_from_rootfile('): 
				if len(toFilter)!=0:
					model='    model = build_model_from_rootfile(input,include_mc_uncertainties=True,histogram_filter = (lambda s:  s.count(\''+toFilter[0]+'\')==0'
					for item in toFilter: 
						if item!=toFilter[0]: model+=' and s.count(\''+item+'\')==0'
					model+='))'
					fout.write(model)
				else: fout.write(line)
			else: fout.write(line)
	with open(outDir+'/'+rFile.split('/')[-1][:-5]+'.sh','w') as fout:
		fout.write('#!/bin/sh \n')
		fout.write('cd /home/ssagir/CMSSW_7_3_0/src/\n')
		fout.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
		fout.write('cmsenv\n')
		fout.write('cd '+outDir+'\n')
		fout.write('/home/ssagir/CMSSW_7_3_0/src/theta/utils2/theta-auto.py ' + outDir+'/'+rFile.split('/')[-1][:-5]+'.py')

count=0
for limitConf in limitConfs:
	toFilter = toFilter0 + limitConfs[limitConf]
	print limitConf,'=',toFilter
	for file in rootfilelist:
		fileName = file.split('/')[-1]
		signal = fileName.split('_')[2]
		BRStr = fileName[fileName.find(signal)+len(signal):fileName.find('_'+lumiInFile)]
		outDir = outputDir+limitConf+BRStr+'/'
		print signal,BRStr
		if not os.path.exists(outDir): os.system('mkdir '+outDir)
		os.chdir(outDir)
		fileDir = ''
		if templateDir.split('/')[-1]!=file.split('/')[-2]:
			fileDir = file.split('/')[-2]
			if not os.path.exists(outDir+fileDir): os.system('mkdir '+fileDir)
			os.chdir(fileDir)
		outDir=outDir+fileDir
		makeThetaConfig(file,outDir,toFilter)

		dict={'configdir':outDir,'configfile':file.split('/')[-1][:-5]}

		jdf=open(file.split('/')[-1][:-5]+'.job','w')
		jdf.write(
"""universe = vanilla
Executable = %(configfile)s.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Notification = Error
request_memory = 3072
Output = %(configfile)s.out
Error = %(configfile)s.err
Log = %(configfile)s.log

Queue 1"""%dict)
		jdf.close()

		os.system('chmod +x '+file.split('/')[-1][:-5]+'.sh')
		os.system('condor_submit '+file.split('/')[-1][:-5]+'.job')
		os.chdir('..')
		count+=1
print "Total number of jobs submitted:", count
                  
