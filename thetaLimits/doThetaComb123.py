import os,sys,fnmatch

ssdl = os.path.dirname(os.getcwd()+'/ssdluncerts/')
sys.path.append(ssdl)

from unc_jec_jer import *
from unc_pdf import *
from unc_pu import *
from unc_scale import *

templateDir='/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/makeTemplates/templates4CRhtSR_NewEl'
thetaConfigTemp = os.getcwd()+'/theta_combine123_template.py'
#thetaConfigTemp = os.getcwd()+'/theta_ssdl_template.py'
whichSignal = 'TT'

skipcode = '_bW'
if whichSignal == 'BB': skipcode = '_tW'

toFilter = []#'toppt__'] #does what's hardcoded unless there are entries here...
toFilterTrilep = []#'muR__','muF__','muRFcorrd__','elelelTrigSys','elelmuTrigSys','elmumuTrigSys','mumumuTrigSys','elIsoSys','elIdSys','muIsoSys','muIdSys','PR__']
systematicsInFile = ['pileup','q2','jec','jer','jmr','jms','btag','tau21','pdfNew','muRFcorrdNew','toppt','jsf']
btagChannels = ['nB0','nB1','nB2','nB3p']
#toFilter = [syst for syst in systematicsInFile if syst!='muRFenv']
#toFilter = ['muR','muF','muRFcorrd','muRFdecorrdNew']
#toFilter = ['__'+item+'__' for item in toFilter]
#toFilter += [chan for chan in btagChannels if chan!='nB3p']
#toFilter+= ['isM']
#toFilter+= ['qcd__pdfNew','qcd__muRFcorrdNew']
print toFilter

if not os.path.exists('/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/limitsOct17/'+templateDir.split('/')[-1]): os.system('mkdir /user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/limitsOct17/'+templateDir.split('/')[-1]) #prevent writing these (they are large) to brux6 common area
outputDir = '/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/limitsOct17/'+templateDir.split('/')[-1]+'/'
limitType = 'comb123fb120'

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)
            
rootfilelist = []
i=0
for rootfile in findfiles(templateDir, '*.root'):
    if '_minMlbST_' not in rootfile: continue
    if 'splitLess' not in rootfile: continue
    if 'BKGNORM_rebinned_stat0p3.root' not in rootfile: continue
    if '_modified.root' in rootfile: continue
    if skipcode not in rootfile: continue
    #if '0p5' in rootfile or '1p0' in rootfile: continue
    #if '0p5' not in rootfile and '1p0' not in rootfile: continue
    if '0p5' not in rootfile: continue
    rootfilelist.append(rootfile)
    i+=1

print 'Filelist = ',rootfilelist

f = open(thetaConfigTemp, 'rU')
thetaConfigLines = f.readlines()
f.close()

def makeThetaConfig(rFile,dFile,aFile,outDir,BRStr):
	rFileDir = rFile.split('/')[-2]
	with open(outDir+'/'+rFileDir+'/'+rFile.split('/')[-1][:-5]+'.py','w') as fout:
		for line in thetaConfigLines:
                    if 'TTZPUDOWN' in line: line = line.replace('TTZPUDOWN',str(2.0-puDn['TTZ']))
                    if 'TTWPUDOWN' in line: line = line.replace('TTWPUDOWN',str(2.0-puDn['TTW']))
                    if 'TTHPUDOWN' in line: line = line.replace('TTHPUDOWN',str(2.0-puDn['TTH']))
                    if 'TTTTPUDOWN' in line: line = line.replace('TTTTPUDOWN',str(2.0-puDn['TTTT']))
                    if 'WpWpPUDOWN' in line: line = line.replace('WpWpPUDOWN',str(2.0-puDn['WpWp']))
                    if 'WWZPUDOWN' in line: line = line.replace('WWZPUDOWN',str(2.0-puDn['WWZ']))
                    if 'WZZPUDOWN' in line: line = line.replace('WZZPUDOWN',str(2.0-puDn['WZZ']))
                    if 'WZPUDOWN' in line: line = line.replace('WZPUDOWN',str(2.0-puDn['WZ']))
                    if 'ZZPUDOWN' in line: line = line.replace('ZZPUDOWN',str(2.0-puDn['ZZ']))

                    if 'TTZPUUP' in line: line = line.replace('TTZPUUP',str(puUp['TTZ']))
                    if 'TTWPUUP' in line: line = line.replace('TTWPUUP',str(puUp['TTW']))
                    if 'TTHPUUP' in line: line = line.replace('TTHPUUP',str(puUp['TTH']))
                    if 'TTTTPUUP' in line: line = line.replace('TTTTPUUP',str(puUp['TTTT']))
                    if 'WpWpPUUP' in line: line = line.replace('WpWpPUUP',str(puUp['WpWp']))
                    if 'WWZPUUP' in line: line = line.replace('WWZPUUP',str(puUp['WWZ']))
                    if 'WZZPUUP' in line: line = line.replace('WZZPUUP',str(puUp['WZZ']))
                    if 'WZPUUP' in line: line = line.replace('WZPUUP',str(puUp['WZ']))
                    if 'ZZPUUP' in line: line = line.replace('ZZPUUP',str(puUp['ZZ']))

                    if 'TTZJECDOWN' in line: line = line.replace('TTZJECDOWN',str(2.0-jecDn['TTZ']))
                    if 'TTWJECDOWN' in line: line = line.replace('TTWJECDOWN',str(2.0-jecDn['TTW']))
                    if 'TTHJECDOWN' in line: line = line.replace('TTHJECDOWN',str(2.0-jecDn['TTH']))
                    if 'TTTTJECDOWN' in line: line = line.replace('TTTTJECDOWN',str(2.0-jecDn['TTTT']))
                    if 'WpWpJECDOWN' in line: line = line.replace('WpWpJECDOWN',str(2.0-jecDn['WpWp']))
                    if 'WWZJECDOWN' in line: line = line.replace('WWZJECDOWN',str(2.0-jecDn['WWZ']))
                    if 'WZZJECDOWN' in line: line = line.replace('WZZJECDOWN',str(2.0-jecDn['WZZ']))
                    if 'WZJECDOWN' in line: line = line.replace('WZJECDOWN',str(2.0-jecDn['WZ']))
                    if 'ZZJECDOWN' in line: line = line.replace('ZZJECDOWN',str(2.0-jecDn['ZZ']))
                    if 'SIGJECDOWN' in line: line = line.replace('SIGJECDOWN',str(2.0-jecDn[BRStr]))

                    if 'TTZJECUP' in line: line = line.replace('TTZJECUP',str(jecUp['TTZ']))
                    if 'TTWJECUP' in line: line = line.replace('TTWJECUP',str(jecUp['TTW']))
                    if 'TTHJECUP' in line: line = line.replace('TTHJECUP',str(jecUp['TTH']))
                    if 'TTTTJECUP' in line: line = line.replace('TTTTJECUP',str(jecUp['TTTT']))
                    if 'WpWpJECUP' in line: line = line.replace('WpWpJECUP',str(jecUp['WpWp']))
                    if 'WWZJECUP' in line: line = line.replace('WWZJECUP',str(jecUp['WWZ']))
                    if 'WZZJECUP' in line: line = line.replace('WZZJECUP',str(jecUp['WZZ']))
                    if 'WZJECUP' in line: line = line.replace('WZJECUP',str(jecUp['WZ']))
                    if 'ZZJECUP' in line: line = line.replace('ZZJECUP',str(jecUp['ZZ']))
                    if 'SIGJECUP' in line: line = line.replace('SIGJECUP',str(jecUp[BRStr]))

                    if 'TTZJERDOWN' in line: line = line.replace('TTZJERDOWN',str(2.0-jerDn['TTZ']))
                    if 'TTWJERDOWN' in line: line = line.replace('TTWJERDOWN',str(2.0-jerDn['TTW']))
                    if 'TTHJERDOWN' in line: line = line.replace('TTHJERDOWN',str(2.0-jerDn['TTH']))
                    if 'TTTTJERDOWN' in line: line = line.replace('TTTTJERDOWN',str(2.0-jerDn['TTTT']))
                    if 'WpWpJERDOWN' in line: line = line.replace('WpWpJERDOWN',str(2.0-jerDn['WpWp']))
                    if 'WWZJERDOWN' in line: line = line.replace('WWZJERDOWN',str(2.0-jerDn['WWZ']))
                    if 'WZZJERDOWN' in line: line = line.replace('WZZJERDOWN',str(2.0-jerDn['WZZ']))
                    if 'WZJERDOWN' in line: line = line.replace('WZJERDOWN',str(2.0-jerDn['WZ']))
                    if 'ZZJERDOWN' in line: line = line.replace('ZZJERDOWN',str(2.0-jerDn['ZZ']))
                    if 'SIGJERDOWN' in line: line = line.replace('SIGJERDOWN',str(2.0-jerDn[BRStr]))

                    if 'TTZJERUP' in line: line = line.replace('TTZJERUP',str(jerUp['TTZ']))
                    if 'TTWJERUP' in line: line = line.replace('TTWJERUP',str(jerUp['TTW']))
                    if 'TTHJERUP' in line: line = line.replace('TTHJERUP',str(jerUp['TTH']))
                    if 'TTTTJERUP' in line: line = line.replace('TTTTJERUP',str(jerUp['TTTT']))
                    if 'WpWpJERUP' in line: line = line.replace('WpWpJERUP',str(jerUp['WpWp']))
                    if 'WWZJERUP' in line: line = line.replace('WWZJERUP',str(jerUp['WWZ']))
                    if 'WZZJERUP' in line: line = line.replace('WZZJERUP',str(jerUp['WZZ']))
                    if 'WZJERUP' in line: line = line.replace('WZJERUP',str(jerUp['WZ']))
                    if 'ZZJERUP' in line: line = line.replace('ZZJERUP',str(jerUp['ZZ']))
                    if 'SIGJERUP' in line: line = line.replace('SIGJERUP',str(jerUp[BRStr]))

                    if 'TTZPDFDOWN' in line: line = line.replace('TTZPDFDOWN',str(2.0-pdfDn['TTZ']))
                    if 'TTWPDFDOWN' in line: line = line.replace('TTWPDFDOWN',str(2.0-pdfDn['TTW']))
                    if 'TTHPDFDOWN' in line: line = line.replace('TTHPDFDOWN',str(2.0-pdfDn['TTH']))
                    if 'TTTTPDFDOWN' in line: line = line.replace('TTTTPDFDOWN',str(2.0-pdfDn['TTTT']))
                    if 'WpWpPDFDOWN' in line: line = line.replace('WpWpPDFDOWN',str(2.0-pdfDn['WpWp']))
                    if 'WWZPDFDOWN' in line: line = line.replace('WWZPDFDOWN',str(2.0-pdfDn['WWZ']))
                    if 'WZZPDFDOWN' in line: line = line.replace('WZZPDFDOWN',str(2.0-pdfDn['WZZ']))
                    if 'WZPDFDOWN' in line: line = line.replace('WZPDFDOWN',str(2.0-pdfDn['WZ']))
                    if 'ZZPDFDOWN' in line: line = line.replace('ZZPDFDOWN',str(2.0-pdfDn['ZZ']))
                    if 'SIGPDFDOWN' in line: line = line.replace('SIGPDFDOWN',str(2.0-pdfDn[BRStr]))

                    if 'TTZPDFUP' in line: line = line.replace('TTZPDFUP',str(pdfUp['TTZ']))
                    if 'TTWPDFUP' in line: line = line.replace('TTWPDFUP',str(pdfUp['TTW']))
                    if 'TTHPDFUP' in line: line = line.replace('TTHPDFUP',str(pdfUp['TTH']))
                    if 'TTTTPDFUP' in line: line = line.replace('TTTTPDFUP',str(pdfUp['TTTT']))
                    if 'WpWpPDFUP' in line: line = line.replace('WpWpPDFUP',str(pdfUp['WpWp']))
                    if 'WWZPDFUP' in line: line = line.replace('WWZPDFUP',str(pdfUp['WWZ']))
                    if 'WZZPDFUP' in line: line = line.replace('WZZPDFUP',str(pdfUp['WZZ']))
                    if 'WZPDFUP' in line: line = line.replace('WZPDFUP',str(pdfUp['WZ']))
                    if 'ZZPDFUP' in line: line = line.replace('ZZPDFUP',str(pdfUp['ZZ']))
                    if 'SIGPDFUP' in line: line = line.replace('SIGPDFUP',str(pdfUp[BRStr]))

                    if 'TTZSCALEDOWN' in line: line = line.replace('TTZSCALEDOWN',str(2.0-scaleDn['TTZ']))
                    if 'TTWSCALEDOWN' in line: line = line.replace('TTWSCALEDOWN',str(2.0-scaleDn['TTW']))
                    if 'TTHSCALEDOWN' in line: line = line.replace('TTHSCALEDOWN',str(2.0-scaleDn['TTH']))
                    if 'TTTTSCALEDOWN' in line: line = line.replace('TTTTSCALEDOWN',str(2.0-scaleDn['TTTT']))
                    if 'WpWpSCALEDOWN' in line: line = line.replace('WpWpSCALEDOWN',str(2.0-scaleDn['WpWp']))
                    if 'WWZSCALEDOWN' in line: line = line.replace('WWZSCALEDOWN',str(2.0-scaleDn['WWZ']))
                    if 'WZZSCALEDOWN' in line: line = line.replace('WZZSCALEDOWN',str(2.0-scaleDn['WZZ']))
                    if 'WZSCALEDOWN' in line: line = line.replace('WZSCALEDOWN',str(2.0-scaleDn['WZ']))
                    if 'ZZSCALEDOWN' in line: line = line.replace('ZZSCALEDOWN',str(2.0-scaleDn['ZZ']))
                    if 'SIGSCALEDOWN' in line: line = line.replace('SIGSCALEDOWN',str(2.0-scaleDn[BRStr]))

                    if 'TTZSCALEUP' in line: line = line.replace('TTZSCALEUP',str(scaleUp['TTZ']))
                    if 'TTWSCALEUP' in line: line = line.replace('TTWSCALEUP',str(scaleUp['TTW']))
                    if 'TTHSCALEUP' in line: line = line.replace('TTHSCALEUP',str(scaleUp['TTH']))
                    if 'TTTTSCALEUP' in line: line = line.replace('TTTTSCALEUP',str(scaleUp['TTTT']))
                    if 'WpWpSCALEUP' in line: line = line.replace('WpWpSCALEUP',str(scaleUp['WpWp']))
                    if 'WWZSCALEUP' in line: line = line.replace('WWZSCALEUP',str(scaleUp['WWZ']))
                    if 'WZZSCALEUP' in line: line = line.replace('WZZSCALEUP',str(scaleUp['WZZ']))
                    if 'WZSCALEUP' in line: line = line.replace('WZSCALEUP',str(scaleUp['WZ']))
                    if 'ZZSCALEUP' in line: line = line.replace('ZZSCALEUP',str(scaleUp['ZZ']))
                    if 'SIGSCALEUP' in line: line = line.replace('SIGSCALEUP',str(scaleUp[BRStr]))

                    if line.startswith('outDir ='): fout.write('outDir = \''+outDir+'/'+rFileDir+'\'')
                    elif line.startswith('input1L ='): fout.write('input1L = \''+rFile+'\'')
                    elif line.startswith('input2L ='): fout.write('input2L = \''+aFile+'\'')
                    elif line.startswith('input3L ='): fout.write('input3L = \''+dFile+'\'')
                    elif line.startswith('    model = build_model_from_rootfile(input1L'): 
                        if len(toFilter)!=0:
                            model='    model = build_model_from_rootfile(input1L,include_mc_uncertainties=True,histogram_filter = (lambda s:  s.count(\''+toFilter[0]+'\')==0'
                            for item in toFilter: 
                                if item!=toFilter[0]: model+=' and s.count(\''+item+'\')==0'
                            model+='))'
                            fout.write(model)
                        else: fout.write(line)
                    elif line.startswith('    model = build_model_from_rootfile(input3L'):
                        if len(toFilterTrilep)!=0:
                            model='    model = build_model_from_rootfile(input3L,include_mc_uncertainties=True,histogram_filter = (lambda s:  s.count(\''+toFilter[0]+'\')==0'
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
        filebase = file.rsplit('/',1)[0]
	BRStr = file.split('/')[-1][file.split('/')[-1].find(signal)+len(signal):file.split('/')[-1].find('_36p814fb')]

        RizkisFile = '/user_data/rsyarif/optimization_reMiniAOD_PRv9_FRv49sys_elMVAfix_AllSys_2017_9_21/lep1Pt0_jetPt0_MET20_NJets3_NBJets1_HT0_ST0_mllOS20/Shape_accurateLHESys_FRsysSep21_newSigSF_AsymmFRsys/templates_STrebinnedv2_'+signal+BRStr+'_35p867fb.root'

        if whichSignal == 'BB':
            RizkisFile = '/user_data/rsyarif/optimization_reMiniAOD_PRv9_FRv49sys_elMVAfix_AllSys_BB_2017_9_21/lep1Pt0_jetPt0_MET20_NJets3_NBJets1_HT0_ST0_mllOS20/Shape_accurateLHESys_FRsysSep21_newSigSF_AsymmFRsys/templates_STrebinnedv2_'+signal+BRStr+'_35p867fb.root'

        AnthonysFile = '/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/ssdluncerts/Oct21_2017_HT1200_nConst4_0NonSSLeps/Limits_'+signal+BRStr+'_All_LL40_SL35_HT1200_nConst4.root'

	outDir = outputDir+limitType+BRStr+'/'
	print signal,BRStr
	if not os.path.exists(outDir): os.system('mkdir '+outDir)
	os.chdir(outDir)
	fileDir = file.split('/')[-2]
	#if os.path.exists(outDir+fileDir+'/'+file.split('/')[-1][:-5]+'.job'): continue
	if not os.path.exists(outDir+fileDir): os.system('mkdir '+fileDir)
	os.chdir(fileDir)
	makeThetaConfig(file,RizkisFile,AnthonysFile,outDir,signal+BRStr)

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
                  
