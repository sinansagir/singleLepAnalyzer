import os,sys
from ROOT import TFile, TObject, RooArgSet

## Arguments: limit directory name; mass point; signal amount to inject; number of toys

## Make a datacard first with datacard.py!

limitdir = sys.argv[1]
BR = sys.argv[2]
path = limitdir+'/'+BR+'/'
os.chdir(path)

taglist=['taggedbWbW','taggedtHbW','taggedtZbW','taggedtZHtZH','notVtH','notVtZ','notVbW','notV2pT','notV01T2pH','notV01T1H','notV1T0H','notV0T0H1pZ','notV0T0H0Z2pW','notV0T0H0Z01W']

for tag in taglist:
    print '------------',tag,'---------------'

    print 'Running Asymptotic CLs limits for all masses'
    print 'Command = combineTool.py -M AsymptoticLimits -d isSR_isM_'+tag+'_DeepAK8/*/*.txt --there -n .limit --run=blind'
    os.system('combineTool.py -M AsymptoticLimits -d isSR_isM_'+tag+'_DeepAK8/*/*.txt --there -n .limit --run=blind')
    
    print 'Making a JSON file'
    print 'Command = combineTool.py -M CollectLimits isSR_isM_'+tag+'_DeepAK8/*/*.limit.* --use-dirs -o limits.json'
    os.system('combineTool.py -M CollectLimits isSR_isM_'+tag+'_DeepAK8/*/*.limit.* --use-dirs -o limits.json')
    
print 'Done!'
