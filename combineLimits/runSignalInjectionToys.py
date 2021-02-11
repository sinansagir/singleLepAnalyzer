import os,sys
from ROOT import TFile, TObject, RooArgSet

## Arguments: limit directory name; mass point; signal amount to inject; number of toys

## Make a datacard first with datacard.py!

limitdir = sys.argv[1]
mass = sys.argv[2]
rInj = int(sys.argv[3])
nToys = int(sys.argv[4])

BR = 'bW0p5_tZ0p25_tH0p25'
if 'BB' in mass: BR = 'tW0p5_bZ0p25_bH0p25'
mass = mass.replace('BB','')

name = limitdir.replace('limits_templatesCR_Feb2021','').replace('limits_templatesSRCR_Feb2021','')+'InjR'+str(rInj)
path = limitdir+'/'+BR+'/cmb/'+mass

isSR = False
if 'SRCR' in limitdir: isSR = True

os.chdir(path)

filename = 'initialFitWorkspace.root'
if isSR: filename = 'morphedWorkspace.root'

if not isSR and not os.path.exists(filename):

    print "Running Fit Diagnostics for initial workspace"
    print 'Command = combine -M FitDiagnostics -d workspace.root --saveWorkspace --saveShapes --plots'
    os.system('combine -M FitDiagnostics -d workspace.root --saveWorkspace --saveShapes --plots')
    
    print "Creating initialFit snapshot file: initialFitWorkspace.root"
    w_f = TFile.Open('higgsCombineTest.FitDiagnostics.mH120.root')
    w = w_f.Get('w')
    fr_f = TFile.Open('fitDiagnostics.root')
    fr = fr_f.Get('fit_b')
    myargs = RooArgSet(fr.floatParsFinal())
    w.saveSnapshot('initialFit',myargs,True)
    fout = TFile('initialFitWorkspace.root',"recreate")
    fout.WriteTObject(w,'w')
    fout.Close()

if isSR and not os.path.exists(filename):

    masks = 'mask_TT_isSR_isE_notV01T1H_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV01T2pH_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV0T0H0Z01W_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV0T0H0Z2pW_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV0T0H1pZ_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV1T0H_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV2pT_DeepAK8_0_2017=1,mask_TT_isSR_isE_notVbW_DeepAK8_0_2017=1,mask_TT_isSR_isE_notVtH_DeepAK8_0_2017=1,mask_TT_isSR_isE_notVtZ_DeepAK8_0_2017=1,mask_TT_isSR_isE_taggedbWbW_DeepAK8_0_2017=1,mask_TT_isSR_isE_taggedtHbW_DeepAK8_0_2017=1,mask_TT_isSR_isE_taggedtZHtZH_DeepAK8_0_2017=1,mask_TT_isSR_isE_taggedtZbW_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV01T1H_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV01T2pH_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV0T0H0Z01W_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV0T0H0Z2pW_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV0T0H1pZ_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV1T0H_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV2pT_DeepAK8_0_2017=1,mask_TT_isSR_isM_notVbW_DeepAK8_0_2017=1,mask_TT_isSR_isM_notVtH_DeepAK8_0_2017=1,mask_TT_isSR_isM_notVtZ_DeepAK8_0_2017=1,mask_TT_isSR_isM_taggedbWbW_DeepAK8_0_2017=1,mask_TT_isSR_isM_taggedtHbW_DeepAK8_0_2017=1,mask_TT_isSR_isM_taggedtZHtZH_DeepAK8_0_2017=1,mask_TT_isSR_isM_taggedtZbW_DeepAK8_0_2017=1'
    if 'tW' in BR: masks = masks.replace(',mask_TT_isSR_isE_taggedtZHtZH_DeepAK8_0_2017=1','').replace(',mask_TT_isSR_isM_taggedtZHtZH_DeepAK8_0_2017=1','').replace('bW','tW').replace('tZ','bZ').replace('tH','bH').replace('TT','BB')

    print "Running Fit Diagnostics for initial workspace with SR channels masked"
    print 'Command = combine -M FitDiagnostics -d workspace.root --saveWorkspace --saveShapes --plots -n Masked --setParameters '+masks
    os.system('combine -M FitDiagnostics -d workspace.root --saveWorkspace --saveShapes --plots -n Masked --setParameters '+masks)

    print "Creating initialFit snapshot file: morphedWorkspace.root"
    w_f = TFile.Open('higgsCombineMasked.FitDiagnostics.mH120.root')
    w = w_f.Get('w')
    fr_f = TFile.Open('fitDiagnosticsMasked.root')
    fr = fr_f.Get('fit_b')
    myargs = RooArgSet(fr.floatParsFinal())
    w.saveSnapshot('initialFit',myargs,True)
    fout = TFile('morphedWorkspace.root', "recreate")
    fout.WriteTObject(w,'w')
    fout.Close()


## Toy generation is SR-safe, it throws toys off fit_b, which will be CR-data-only from masking. --bypassFrequentistFit should be bypassing any re-fitting
if isSR:
    masks = 'mask_TT_isSR_isE_notV01T1H_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV01T2pH_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV0T0H0Z01W_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV0T0H0Z2pW_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV0T0H1pZ_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV1T0H_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV2pT_DeepAK8_0_2017=0,mask_TT_isSR_isE_notVbW_DeepAK8_0_2017=0,mask_TT_isSR_isE_notVtH_DeepAK8_0_2017=0,mask_TT_isSR_isE_notVtZ_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedbWbW_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedtHbW_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedtZHtZH_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedtZbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV01T1H_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV01T2pH_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV0T0H0Z01W_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV0T0H0Z2pW_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV0T0H1pZ_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV1T0H_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV2pT_DeepAK8_0_2017=0,mask_TT_isSR_isM_notVbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_notVtH_DeepAK8_0_2017=0,mask_TT_isSR_isM_notVtZ_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedbWbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedtHbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedtZHtZH_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedtZbW_DeepAK8_0_2017=0'
    if 'tW' in BR: masks = masks.replace(',mask_TT_isSR_isE_taggedtZHtZH_DeepAK8_0_2017=0','').replace(',mask_TT_isSR_isM_taggedtZHtZH_DeepAK8_0_2017=0','').replace('bW','tW').replace('tZ','bZ').replace('tH','bH').replace('TT','BB')

print "Generating toys from fit_b snapshot"
if isSR:
    print 'Command = combine -M GenerateOnly -d '+filename+' --snapshotName initialFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --saveToys --expectSignal '+str(rInj)+' -n '+name+' --setParameters '+masks
    os.system('combine -M GenerateOnly -d '+filename+' --snapshotName initialFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --saveToys --expectSignal '+str(rInj)+' -n '+name+' --setParameters '+masks)
else:
    print 'Command = combine -M GenerateOnly -d '+filename+' --snapshotName initialFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --saveToys --expectSignal '+str(rInj)+' -n '+name
    os.system('combine -M GenerateOnly -d '+filename+' --snapshotName initialFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --saveToys --expectSignal '+str(rInj)+' -n '+name)

## Toy fits again should be ok, since it's just fitting the previously-made toys
print "Fitting toys...."
print 'Command = combine -M FitDiagnostics -d '+filename+' --snapshotName initialFit --robustFit=1 --skipBOnlyFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --toysFile higgsCombine'+name+'.GenerateOnly.mH120.123456.root --rMin '+str(rInj-10)+' --rMax '+str(rInj+10)+' -n '+name
os.system('combine -M FitDiagnostics -d '+filename+' --snapshotName initialFit --robustFit=1 --skipBOnlyFit --toysFrequentist --bypassFrequentistFit -t '+str(nToys)+' --toysFile higgsCombine'+name+'.GenerateOnly.mH120.123456.root --rMin '+str(rInj-10)+' --rMax '+str(rInj+10)+' -n '+name)

print "Done!"
