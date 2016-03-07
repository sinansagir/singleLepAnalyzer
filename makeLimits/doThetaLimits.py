import os,sys,fnmatch

templateDir='/home/ssagir/CMSSW_7_3_0/src/singleLepAnalyzer/makeThetaTemplates/templates_minMlb_tau21LT0p6_bpbp_2016_3_5'
thetaConfigTemp = os.getcwd()+'/theta_config_template.py'

systematicsInFile = ['pileup','q2','jec','jer','jmr','jms','btag','tau21','pdf','pdfNew','muR','muF','muRFcorrd','muRFcorrdNew','muRFdecorrdNew','toppt','jsf','muRFenv']
btagChannels = ['nB0','nB1','nB2','nB3p']
#toFilter = [syst for syst in systematicsInFile if syst!='muRFenv']
toFilter = ['pdf','muR','muF','muRFcorrd','muRFdecorrdNew','muRFenv']
toFilter = ['__'+item+'__' for item in toFilter]
#toFilter+= [chan for chan in btagChannels if chan!='nB3p']
#toFilter+= ['nW1p']
#toFilter+= ['qcd__pdfNew','qcd__muRFcorrdNew']
print toFilter

if not os.path.exists('/user_data/ssagir/limits/'+templateDir.split('/')[-1]): os.system('mkdir /user_data/ssagir/limits/'+templateDir.split('/')[-1]) #prevent writing these (they are large) to brux6 common area
outputDir = '/user_data/ssagir/limits/'+templateDir.split('/')[-1]+'/'
limitType = 'all'#'pdf_RF_'+'decorrelated/'

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)
            
rootfilelist = []
i=0
for rootfile in findfiles(templateDir, '*.root'):
    if '00_2p318fb_rebinned.root' not in rootfile: continue
    if 'TTM1800' in rootfile: continue
    if 'TTM1700' in rootfile: continue
    if 'TTM1600' in rootfile: continue
    if 'TTM1500' in rootfile: continue
    if 'TTM1400' in rootfile: continue
    rootfilelist.append(rootfile)
    i+=1

f = open(thetaConfigTemp, 'rU')
thetaConfigLines = f.readlines()
f.close()

def makeThetaConfig(rFile,outDir):
	rFileDir = rFile.split('/')[-2]
	with open(outDir+'/'+rFileDir+'/'+rFile.split('/')[-1][:-5]+'.py','w') as fout:
		for line in thetaConfigLines:
			if line.startswith('outDir ='): fout.write('outDir = \''+outDir+'/'+rFileDir+'\'')
			elif line.startswith('input ='): fout.write('input = \''+rFile+'\'')
			elif line.startswith('    model = build_model_from_rootfile('): 
				if len(toFilter)!=0:
					model='    model = build_model_from_rootfile(input,include_mc_uncertainties=True,histogram_filter = (lambda s:  s.count(\''+toFilter[0]+'\')==0'
					for item in toFilter: 
						if item!=toFilter[0]: model+=' and s.count(\''+item+'\')==0'
					model+='))'
					fout.write(model)
				else: fout.write(line)
			else: fout.write(line)
	with open(outDir+'/'+rFileDir+'/'+rFile.split('/')[-1][:-5]+'.sh','w') as fout:
		fout.write('#!/bin/sh \n')
		fout.write('cd /home/ssagir/CMSSW_7_3_0/src/\n')
		fout.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
		fout.write('cmsenv\n')
		fout.write('cd '+outDir+'/'+rFileDir+'\n')
		fout.write('/home/ssagir/CMSSW_7_3_0/src/theta/utils2/theta-auto.py ' + outDir+'/'+rFileDir+'/'+rFile.split('/')[-1][:-5]+'.py')

count=0
for file in rootfilelist:
	signal = file.split('/')[-1].split('_')[2]
	BRStr = file.split('/')[-1][file.split('/')[-1].find(signal)+len(signal):file.split('/')[-1].find('_2p318fb')]
	outDir = outputDir+limitType+BRStr+'/'
	print signal,BRStr
	if not os.path.exists(outDir): os.system('mkdir '+outDir)
	os.chdir(outDir)
	fileDir = file.split('/')[-2]
	#if os.path.exists(outDir+fileDir+'/'+file.split('/')[-1][:-5]+'.job'): continue
	if not os.path.exists(outDir+fileDir): os.system('mkdir '+fileDir)
	os.chdir(fileDir)
	makeThetaConfig(file,outDir)

	dict={'configdir':outDir+fileDir,'configfile':file.split('/')[-1][:-5]}

	jdf=open(file.split('/')[-1][:-5]+'.job','w')
	jdf.write(
"""universe = vanilla
Executable = %(configfile)s.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Notification = Error
notify_user = Sinan_Sagir@brown.edu

arguments      = ""

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
                  
