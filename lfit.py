#!/usr/bin/python

import ROOT
f18=ROOT.TFile('/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_09072021_step3_wenyu/BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2018_NJetsCSV/nominal/TTTT_TuneCP5_13TeV-amcatnlo-pythia8_combined_hadd.root','READ')
f17=ROOT.TFile('/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_09072021_step3_wenyu/BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2017_NJetsCSV/nominal/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_correctnPartonsInBorn_hadd.root','READ')
f16=ROOT.TFile('/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2016_Jan2021_4t_09072021_step3_wenyu/BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year2016_NJetsCSV/nominal/TTTT_TuneCP5_PSweights_13TeV-amcatnlo-pythia8_correctnPartonsInBorn_hadd.root','READ')
f1x=[f16,f17,f18]
out=ROOT.TFile('lfitout.root','RECREATE')
out.cd()
ys=['16','17','18']
bdist='[2]*(x**([0]-1))*((1-x)**([1]-1))+[5]*(x**([3]-1))*((1-x)**([4]-1))'
for fi in range(len(f1x)):
	f=f1x[fi]
	y=ys[fi]
	t=f.Get('ljmet')
	formulas=[]
	for bdt in ['BDT_tt','BDT_ttH','BDT_ttbb']:
		c=ROOT.TCanvas()
		t.Draw('('+bdt+'+1)/2>>'+bdt+y)
		# t.Draw('BDT_tt>>BDTtt')
		h = ROOT.gDirectory.Get(bdt+y)
		h.Scale(1/h.Integral())
		beta=ROOT.TF1("bdist",bdist,0.0,1)
		beta.SetParameters(5,3,0.1,5,3,0.1)
		beta.SetParNames("a1","b1",'N1',"a2","b2",'N2')
		beta.SetParLimits(0,0,3000)
		beta.SetParLimits(1,0,3000)
		beta.SetParLimits(2,0,3000)
		beta.SetParLimits(3,0,3000)
		beta.SetParLimits(4,0,3000)
		beta.SetParLimits(5,0,3000)
		opt=ROOT.Math.MinimizerOptions()
		opt.SetMaxIterations(1000000)
		opt.SetDefaultMaxFunctionCalls(1000000)
		h.Fit("bdist","R")
		ff=h.GetFunction("bdist")
		tmp=bdist
		tmp=tmp.replace('x','(('+bdt+'+1)/2)')
		for pn in range(6):
			# tmp=tmp.replace('['+str(pn)+']','('+str(ff.GetParameter(pn))+')')
			tmp=tmp.replace('['+str(pn)+']',str(ff.GetParameter(pn)))
		print(tmp)
		formulas.append(tmp)
		c.SaveAs(bdt+y+'.pdf')
	print(y)
	print(formulas)
	# print('('+formulas[0]+')*('+formulas[1]+')*('+formulas[2]+')')
	# print('tt*ttH:ttbb')
	# print('('+formulas[0]+')*('+formulas[1]+'):('+formulas[2]+')')
	# print('ttH*ttbb:tt')
	# print('('+formulas[1]+')*('+formulas[2]+'):('+formulas[0]+')')
	# print('tt*ttbb:ttH')
	# print('('+formulas[0]+')*('+formulas[2]+'):('+formulas[1]+')')
	# h.Fit("chebyshev6")
	# h.Fit("pol7")