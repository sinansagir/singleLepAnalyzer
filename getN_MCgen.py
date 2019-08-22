import os,sys
import ROOT as rt

inputDir  = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_4t_071919_step1hadds/nominal/'
rootfiles = os.popen('ls '+inputDir)

for file in rootfiles:
    if 'Single' in file: continue
    print file.strip()
    RFile = rt.TFile(inputDir+file.strip(),'READ')
    hist = RFile.Get("NumTrueHist").Clone()
    print hist.Integral()
