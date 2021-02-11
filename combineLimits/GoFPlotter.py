import os,sys
from ROOT import TFile, TCanvas, TLine, TTree

limitdir = sys.argv[1]
mass = sys.argv[2]
#datachi2 = float(sys.argv[3])

BR = 'bW0p5_tZ0p25_tH0p25'
if 'BB' in mass: BR = 'tW0p5_bZ0p25_bH0p25'
mass = mass.replace('BB','')

name = limitdir.replace('limits_templatesCR_June2020','').replace('limits_templatesSRCR_June2020','')
path = limitdir+'/'+BR+'/cmb/'+mass

os.chdir(path)

RFile=TFile.Open('higgsCombineTest.GoodnessOfFit.mH120.root')
data = RFile.Get('limit')
data.GetEntry(0)
datachi2 = data.limit

RFile1=TFile.Open('higgsCombineTest.GoodnessOfFit.mH120.123456.root')
limit1=RFile1.Get('limit')
GoF_can=TCanvas('GoodnessOfFit','GoodnessOfFit',800,600)
limit1.Draw('limit','','pe')
line=TLine(datachi2,0,datachi2,25)
line.SetLineColor(2)
line.SetLineWidth(2)
GoF_can.Update()
line.Draw('Draw')

GoF_can.SaveAs('GoodnessOfFit.png')
GoF_can.SaveAs('GoodnessOfFit.pdf')

