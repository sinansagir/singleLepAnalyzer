import os,sys
import ROOT as rt

shift = sys.argv[1]
inputDir  = '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2016_Jan2021_4t_032721_step1hadds/'+shift+'/'
rootfiles = os.popen('ls '+inputDir)

for file in rootfiles:
    if 'SingleElectron' in file: continue
    if 'SingleMuon' in file: continue
    if 'JetHT' in file: continue
    if 'EGamma' in file: continue
    RFile = rt.TFile(inputDir+file.strip(),'READ')
    hist1 = RFile.Get("NumTrueHist").Clone("NumTrueHist")
    hist2 = RFile.Get("weightHist").Clone("weightHist")
    print hist1.Integral(),hist2.GetBinContent(1),file.strip()
