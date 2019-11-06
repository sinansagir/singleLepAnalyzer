import os,sys
import ROOT as rt

inputDir  = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_4t_081019_step1hadds/nominal/'
rootfiles = os.popen('ls '+inputDir)

for file in rootfiles:
    if 'Single' in file: continue
    RFile = rt.TFile(inputDir+file.strip(),'READ')
    hist1 = RFile.Get("NumTrueHist").Clone("NumTrueHist")
    hist2 = RFile.Get("weightHist").Clone("weightHist")
    print hist1.Integral(),hist2.GetBinContent(1),file.strip()
