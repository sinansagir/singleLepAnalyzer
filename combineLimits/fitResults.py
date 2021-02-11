import sys, subprocess, ROOT

w_f = ROOT.TFile.Open('higgsCombineTest.FitDiagnostics.mH120.root')
w = w_f.Get('w')
fr_f = ROOT.TFile.Open('fitDiagnostics.root')
fr = fr_f.Get('fit_b')
myargs = ROOT.RooArgSet(fr.floatParsFinal())
w.saveSnapshot('initialFit',myargs,True)
fout = ROOT.TFile('initialFitWorkspace.root',"recreate")
fout.WriteTObject(w,'w')
fout.Close()

