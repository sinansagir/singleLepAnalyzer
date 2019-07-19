import os,sys,fnmatch

runDir='/uscms_data/d3/escharni/CMSSW_10_2_10/src/singleLepAnalyzer/'
templateDir=runDir+'makeTemplates/templatesSR_July_MVA_Update_Round2' # Do NOT put backslash at the end of this directory
postfix = ''

thetaConfigTemp = os.getcwd()+'/theta_config_template.py'
#thetaConfigTemp = os.getcwd()+'/theta_discovery.py'

#systematicsInFile = ['pileup','prefire','jsf','btag','jec','muRFcorrdNew']#,'toppt']
#cats = ['isE_taggedbWbW_DeepAK8','isE_taggedtZbW_DeepAK8','isE_taggedtHbW_DeepAK8','isE_taggedtZHtZH_DeepAK8',
#        'isE_notVbW_DeepAK8','isE_notVtZ_DeepAK8','isE_notVtH_DeepAK8','isE_notV_DeepAK8',
#        'isM_taggedbWbW_DeepAK8','isM_taggedtZbW_DeepAK8','isM_taggedtHbW_DeepAK8','isM_taggedtZHtZH_DeepAK8',
#        'isM_notVbW_DeepAK8','isM_notVtZ_DeepAK8','isM_notVtH_DeepAK8','isM_notV_DeepAK8',
#        ]

toFilter0 = ['_toppt_','_muRFcorrd_'] #always remove in case they are in templates
toFilter0 = [item for item in toFilter0]

limitConfs = {#'<limit type>':[filter list]
    'ST':[],
    'Tp2Mass':[],
    'Tp2MST':[],
    'Tp2MDnn':[],
    'DnnTprime':[],
    #'isE':['isM'], #only electron channel
    #'isM':['isE'], #only muon channel
    #'valid':['isE_notVbW_DeepAK8','isE_notVtZ_DeepAK8','isE_notVtH_DeepAK8','isE_notV_DeepAK8','isM_notVbW_DeepAK8','isM_notVtZ_DeepAK8','isM_notVtH_DeepAK8','isM_notV_DeepAK8']
    }

limitType = ''  #label for bookkeeping
outputDir = os.getcwd()+'/limitsJul19/'+templateDir.split('/')[-1]+'/'
if not os.path.exists(outputDir): os.system('mkdir '+outputDir)
outputDir+= '/'+limitType+'/'
if not os.path.exists(outputDir): os.system('mkdir '+outputDir)
print outputDir

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)
            
rootfilelist = []
i=0
for rootfile in findfiles(templateDir, '*.root'):
    #if 'splitLess' not in rootfile:continue
    if 'rebinned_stat0p3.root' not in rootfile: continue
    if 'plots' in rootfile: continue
    if '0p5' not in rootfile and '1p0' not in rootfile: continue
    rootfilelist.append(rootfile)
    i+=1

f = open(thetaConfigTemp, 'rU')
thetaConfigLines = f.readlines()
f.close()

def makeThetaConfig(rFile,outDir):
    rFileDir = postfix
    with open(outDir+'/'+rFileDir+'/'+rFile.split('/')[-1][:-5]+'.py','w') as fout:
        for line in thetaConfigLines:
            if line.startswith('outDir ='): fout.write('outDir = \''+outDir+'/'+rFileDir+'\'') ## this doesn't happen...
            elif line.startswith('input ='): fout.write('input = \''+rFile.split('/')[-1]+'\'') ## should remove any file path
            elif line.startswith('    model = build_model_from_rootfile('): 
                if len(toFilter)!=0:
                    model='    model = build_model_from_rootfile(input,include_mc_uncertainties=True,histogram_filter = (lambda s:  s.count(\''+toFilter[0]+'\')==0'
                    #model='    model = build_model_from_rootfile(input,include_mc_uncertainties=False,histogram_filter = (lambda s:  s.count(\''+toFilter[0]+'\')==0'
                    for item in toFilter: 
                        if item!=toFilter[0]: model+=' and s.count(\''+item+'\')==0'
                    model+='))'
                    fout.write(model)
                else: fout.write(line)                 #else: fout.write(line.replace('include_mc_uncertainties=True','include_mc_uncertainties=False')) 
            else: fout.write(line)
        ### this part below won't work with fermilab condor
	# with open(outDir+'/'+rFileDir+'/'+rFile.split('/')[-1][:-5]+'.sh','w') as fout:
	# 	fout.write('#!/bin/sh \n')
	# 	fout.write('cd /home/ssagir/CMSSW_7_3_0/src/\n')
	# 	fout.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
	# 	fout.write('cmsenv\n')
	# 	fout.write('cd '+outDir+'/'+rFileDir+'\n')
	# 	fout.write('/home/ssagir/CMSSW_7_3_0/src/theta/utils2/theta-auto.py ' + outDir+'/'+rFileDir+'/'+rFile.split('/')[-1][:-5]+'.py')

count=0
savedir = os.getcwd()
for limitConf in limitConfs:
    toFilter = toFilter0 + limitConfs[limitConf]
    print limitConf,'=',toFilter
    for file in rootfilelist:

        ## Get files for just this type of plot -- need to fix for doing some specific categories
        if '_'+limitConf+'_' not in file: continue
        fileName = file.split('/')[-1]
        signal = fileName.split('_')[2]
        BRStr = fileName[fileName.find(signal)+len(signal):fileName.find('_41p53fb')]

        ## Make the output directory, go there, and make the config
        ## Will pick up executable from main dir
        outDir = outputDir+limitConf+BRStr+'/'
        print signal,BRStr
        if not os.path.exists(outDir+postfix): os.system('mkdir -p '+outDir+postfix)
        os.chdir(outDir+postfix)
        makeThetaConfig(file,outDir)
        
        dict={'rundir':runDir,'configdir':outDir+postfix,'rootfile':file,'configfile':file.split('/')[-1][:-5]}
        
        jdf=open(file.split('/')[-1][:-5]+'.job','w')
        jdf.write(
            """use_x509userproxy = true
universe = vanilla
Executable = %(rundir)s/thetaLimits/doThetaLimits.sh
Should_Transfer_Files = YES
Transfer_Input_Files = %(configfile)s.py, %(rootfile)s
WhenToTransferOutput = ON_EXIT
Output = %(configfile)s.out
Error = %(configfile)s.err
Log = %(configfile)s.log
arguments = %(configfile)s
Queue 1"""%dict)
        jdf.close()        
        os.system('condor_submit '+file.split('/')[-1][:-5]+'.job')
        os.chdir(savedir)
        count+=1
print "Total number of jobs submitted:", count
                  
