import os,sys,fnmatch

templateDir='/user_data/jhogan/CMSSW_7_4_14/src/tptp_2015/makeTemplates/templates_minMlb_PaperARC_HTweightNew'
thetaConfigTemp = os.getcwd()+'/theta_combined_template.py'
whichSignal = 'BB'

skipcode = '_bW'
if whichSignal == 'BB': skipcode = '_tW'

toFilter = []
toFilterHiggs = []
systematicsInFile = ['pileup','q2','jec','jer','jmr','jms','btag','tau21','pdfNew','muRFcorrdNew','toppt','jsf']
btagChannels = ['nB0','nB1','nB2','nB3p']
#toFilter = [syst for syst in systematicsInFile if syst!='muRFenv']
#toFilter = ['muR','muF','muRFcorrd','muRFdecorrdNew']
#toFilter = ['__'+item+'__' for item in toFilter]
#toFilter += [chan for chan in btagChannels if chan!='nB3p']
#toFilter+= ['isM']
#toFilter+= ['qcd__pdfNew','qcd__muRFcorrdNew']
print toFilter

if not os.path.exists('/user_data/jhogan/CMSSW_7_4_14/src/tptp_2015/thetaLimits/limitsDec16/'+templateDir.split('/')[-1]): os.system('mkdir /user_data/jhogan/CMSSW_7_4_14/src/tptp_2015/thetaLimits/limitsDec16/'+templateDir.split('/')[-1]) #prevent writing these (they are large) to brux6 common area
outputDir = '/user_data/jhogan/CMSSW_7_4_14/src/tptp_2015/thetaLimits/limitsDec16/'+templateDir.split('/')[-1]+'/'
limitType = 'all_noQ2'

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)
            
rootfilelist = []
i=0
for rootfile in findfiles(templateDir, '*.root'):
    if '_rebinnedDV.root' not in rootfile: continue
    if '_modified.root' in rootfile: continue
    #if skipcode not in rootfile: continue
    if '0p5' not in rootfile: continue
    rootfilelist.append(rootfile)
    i+=1

print 'Filelist = ',rootfilelist

f = open(thetaConfigTemp, 'rU')
thetaConfigLines = f.readlines()
f.close()

def makeThetaConfig(rFile,dFile,outDir,signal):
	rFileDir = rFile.split('/')[-2]
	with open(outDir+'/'+rFileDir+'/'+rFile.split('/')[-1][:-5]+'.py','w') as fout:
		for line in thetaConfigLines:
                    if line.startswith('outDir ='): fout.write('outDir = \''+outDir+'/'+rFileDir+'\'')
                    elif line.startswith('input0H ='): fout.write('input0H = \''+rFile+'\'')
                    elif line.startswith('input1H ='): fout.write('input1H = \''+dFile+'\'')
                    elif line.startswith('    model.set_signal_processes('):
                        if whichSignal=='BB': fout.write('    model.set_signal_processes(\'BpBp_M-*\')')
                        else: fout.write(line)
                    elif line.startswith('    model = build_model_from_rootfile(input0H'): 
                        if len(toFilter)!=0:
                            model='    model = build_model_from_rootfile(input0H,include_mc_uncertainties=True,histogram_filter = (lambda s:  s.count(\''+toFilter[0]+'\')==0'
                            for item in toFilter: 
                                if item!=toFilter[0]: model+=' and s.count(\''+item+'\')==0'
                            model+='))'
                            fout.write(model)
                        else: fout.write(line)
                    elif line.startswith('    model = build_model_from_rootfile(input1H'):
                        if len(toFilterHiggs)!=0:
                            model='    model = build_model_from_rootfile(input1H,include_mc_uncertainties=True,histogram_filter = (lambda s:  s.count(\'sfel\')==0 and s.count(\'sfmu\')==0'
                            for item in toFilterHiggs: 
                                model+=' and s.count(\'BpBp_M-'+item+'\')==0'
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
        filebase = file.rsplit('/',1)[0]
	BRStr = file.split('/')[-1][file.split('/')[-1].find(signal)+len(signal):file.split('/')[-1].find('_2p318fb')]

        #if 'bH0p5' in BRStr or 'tW0p5' in BRStr: continue

        Dsignal = signal
        if whichSignal == 'TT':
            if signal == 'TTM700' or signal == 'TTM800' or signal == 'TTM900': Dsignal = 'TTM0'+signal[3:]
        else:
            if signal == 'BBM700' or signal == 'BBM800' or signal == 'BBM900': Dsignal = 'BBM0'+signal[3:]

        sigmass = Dsignal[3:]

        DominiksFile = '/user_data/jhogan/CMSSW_7_4_14/src/tptp_2015/makeTemplates/BoostedHiggs/HiggsTagTemplate'+BRStr+'_'+Dsignal+'.root'

        if whichSignal == 'BB':
            DominiksFile = '/user_data/jhogan/CMSSW_7_4_14/src/tptp_2015/makeTemplates/BoostedHiggs/BB_templates/HiggsTagTemplate'+BRStr+'_'+Dsignal+'.root'

        #print DominiksFile

	outDir = outputDir+limitType+BRStr+'/'
	print signal,BRStr
	if not os.path.exists(outDir): os.system('mkdir '+outDir)
	os.chdir(outDir)
	fileDir = file.split('/')[-2]
	#if os.path.exists(outDir+fileDir+'/'+file.split('/')[-1][:-5]+'.job'): continue
	if not os.path.exists(outDir+fileDir): os.system('mkdir '+fileDir)
	os.chdir(fileDir)
	makeThetaConfig(file,DominiksFile,outDir,sigmass)

	dict={'configdir':outDir+fileDir,'configfile':file.split('/')[-1][:-5]}

	jdf=open(file.split('/')[-1][:-5]+'.job','w')
	jdf.write(
"""universe = vanilla
Executable = %(configfile)s.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Notification = Error
notify_user = Sinan_Sagir@brown.edu
request_memory = 3072
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
                  
