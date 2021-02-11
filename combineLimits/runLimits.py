import os,sys
from ROOT import TFile, TObject, RooArgSet

## Arguments: limit directory name; mass point; signal amount to inject; number of toys

## Make a datacard first with datacard.py!

limitdir = sys.argv[1]
BR = sys.argv[2]
path = limitdir+'/'+BR+'/'
os.chdir(path)

for mass in [900,1000,1100,1200,1300,1400,1500,1600,1700,1800]:
    if os.path.exists('cmb/'+str(mass)) and not os.path.exists('cmb/'+str(mass)+'/morphedWorkspace.root'):
        masks = 'mask_TT_isSR_isE_notV01T1H_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV01T2pH_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV0T0H0Z01W_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV0T0H0Z2pW_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV0T0H1pZ_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV1T0H_DeepAK8_0_2017=1,mask_TT_isSR_isE_notV2pT_DeepAK8_0_2017=1,mask_TT_isSR_isE_notVbW_DeepAK8_0_2017=1,mask_TT_isSR_isE_notVtH_DeepAK8_0_2017=1,mask_TT_isSR_isE_notVtZ_DeepAK8_0_2017=1,mask_TT_isSR_isE_taggedbWbW_DeepAK8_0_2017=1,mask_TT_isSR_isE_taggedtHbW_DeepAK8_0_2017=1,mask_TT_isSR_isE_taggedtZHtZH_DeepAK8_0_2017=1,mask_TT_isSR_isE_taggedtZbW_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV01T1H_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV01T2pH_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV0T0H0Z01W_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV0T0H0Z2pW_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV0T0H1pZ_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV1T0H_DeepAK8_0_2017=1,mask_TT_isSR_isM_notV2pT_DeepAK8_0_2017=1,mask_TT_isSR_isM_notVbW_DeepAK8_0_2017=1,mask_TT_isSR_isM_notVtH_DeepAK8_0_2017=1,mask_TT_isSR_isM_notVtZ_DeepAK8_0_2017=1,mask_TT_isSR_isM_taggedbWbW_DeepAK8_0_2017=1,mask_TT_isSR_isM_taggedtHbW_DeepAK8_0_2017=1,mask_TT_isSR_isM_taggedtZHtZH_DeepAK8_0_2017=1,mask_TT_isSR_isM_taggedtZbW_DeepAK8_0_2017=1'
        if 'tW' in BR: masks = masks.replace(',mask_TT_isSR_isE_taggedtZHtZH_DeepAK8_0_2017=1','').replace(',mask_TT_isSR_isM_taggedtZHtZH_DeepAK8_0_2017=1','').replace('bW','tW').replace('tZ','bZ').replace('tH','bH').replace('TT','BB')

        os.chdir('cmb/'+str(mass))

        print "Running Fit Diagnostics for initial workspace with SR channels masked"
        print 'Command = combine -M FitDiagnostics -d workspace.root --saveWorkspace -n Masked --setParameters '+masks
        os.system('combine -M FitDiagnostics -d workspace.root --saveWorkspace -n Masked --setParameters '+masks)

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
        w_f.Close()
        fr_f.Close()

        os.chdir('../../')


masks = 'mask_TT_isSR_isE_notV01T1H_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV01T2pH_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV0T0H0Z01W_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV0T0H0Z2pW_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV0T0H1pZ_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV1T0H_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV2pT_DeepAK8_0_2017=0,mask_TT_isSR_isE_notVbW_DeepAK8_0_2017=0,mask_TT_isSR_isE_notVtH_DeepAK8_0_2017=0,mask_TT_isSR_isE_notVtZ_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedbWbW_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedtHbW_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedtZHtZH_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedtZbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV01T1H_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV01T2pH_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV0T0H0Z01W_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV0T0H0Z2pW_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV0T0H1pZ_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV1T0H_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV2pT_DeepAK8_0_2017=0,mask_TT_isSR_isM_notVbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_notVtH_DeepAK8_0_2017=0,mask_TT_isSR_isM_notVtZ_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedbWbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedtHbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedtZHtZH_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedtZbW_DeepAK8_0_2017=0'
if 'tW' in BR: masks = masks.replace(',mask_TT_isSR_isE_taggedtZHtZH_DeepAK8_0_2017=0','').replace(',mask_TT_isSR_isM_taggedtZHtZH_DeepAK8_0_2017=0','').replace('bW','tW').replace('tZ','bZ').replace('tH','bH').replace('TT','BB')


print 'Running Asymptotic CLs limits for all masses'
print 'Command = combineTool.py -M AsymptoticLimits -d cmb/*/morphedWorkspace.root --snapshotName initialFit --there -n .limit --run=blind --setParameters '+masks
os.system('combineTool.py -M AsymptoticLimits -d cmb/*/morphedWorkspace.root --snapshotName initialFit --there -n .limit --run=blind --setParameters '+masks)

print 'Making a JSON file'
print 'Command = combineTool.py -M CollectLimits cmb/*/*.limit.* --use-dirs -o limits.json'
os.system('combineTool.py -M CollectLimits cmb/*/*.limit.* --use-dirs -o limits.json')

print 'Done!'
