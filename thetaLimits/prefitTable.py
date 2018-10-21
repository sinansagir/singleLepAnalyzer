#!/usr/bin/python

import os,sys,time,math

prefitFile = 'templates_M17WtSF_2017_3_31_SRpCRplots/prefit900left.txt' # replace "plusminus" sign with "pm" in the file

fprefit = open(prefitFile, 'rU')
prefitlines = fprefit.readlines()
fprefit.close()

obsIndexes  = []
observables = []
for ind in range(len(prefitlines)):
	if prefitlines[ind].startswith('process / nuisance parameter'): 
		obsIndexes.append(ind)
		observables.append(prefitlines[ind-2])

nuisNam = [
			'pdfNew',
			'muRFcorrdNew',
			'toppt',
			'tau21',
			'jms',
			'jmr',
			'taupt',
			'topsf',
			'btag',
			'mistag',
			'jer',
			'jec',
			'pileup',
			'ht',
			'mutrigeff',
			'eltrigeff',
			'muIsoSys',
			'elIsoSys',
			'muIdSys',
			'elIdSys',
			'lumiSys',
			]

nuisNamPlot = {
		   'pdfNew':'PDF',
		   'muRFcorrdNew':'muRF(TOP)',
		   'ewkmuRFcorrdNew':'muRF(EWK)',
		   'qcdmuRFcorrdNew':'muRF(QCD)',
		   'qcdScale':'muRF(QCD)',
		   'sigmuRFcorrdNew':'muRF(muRF(LH-900GeV))',
		   'muRFcorrdNew':'muRF',
		   'toppt':'top \\pt',
		   'tau21':'$\\tau_{2}/\\tau_{1}$',
		   'jms':'JMS',
		   'jmr':'JMR',
		   'taupt':'$\\tau_{2}/\\tau_{1}$ $p_{T}$',
		   'topsf':'t-tag',
		   'btag':'b/c-tag',
		   'mistag':'udsg-mistag',
		   'jer':'JER',
		   'jec':'JEC',
		   'pileup':'pileup',
		   'eltrigeff':'elTrig',
		   'mutrigeff':'muTrig',
		   'ht':'\\HT',
		   'muIsoSys':'muIso',
		   'elIsoSys':'elIso',
		   'muIdSys':'muId',
		   'elIdSys':'elId',
		   'lumiSys':'lumi',
		   }

ewkInd = 1
qcdInd = 2
sigInd = 3
topInd = 4
procs = ['ewk','qcd','sig','top']
prefitUncs = {}
for ind in obsIndexes:
	lowerBy = 0
	prefitUncs[ind] = {}
	data = prefitlines[ind].strip().split()
	prefitUncs[ind]['main'] = []
	for item in data: 
		if 'process' in item or '/' in item or 'nuisance' in item or 'parameter' in item or 'gauss' in item: continue
		prefitUncs[ind]['main'].append([item,'(gauss)'])
	procInd = 0
	for proc in procs:
		procInd+=1
		if prefitlines[ind+procInd-lowerBy].startswith(proc): 
			data = prefitlines[ind+procInd-lowerBy].strip().split()
			prefitUncs[ind][proc] = []
			for it in range(1,len(data)): 
				if '(s)' in data[it] or '(r)' in data[it]: continue
				if it==len(data)-1 and data[it]!='---': continue
				if data[it]!='---': 
					if data[it].startswith('pm'): prefitUncs[ind][proc].append([data[it].replace('pm','$\pm$'),data[it+1]])
					else:
						for k in range(1,len(data[it])):
							if not (data[it][k].isdigit() or data[it][k]=='.'): 
								up = data[it][:k]
								dn = data[it][k:]
						prefitUncs[ind][proc].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
				else: prefitUncs[ind][proc].append([data[it].replace('---','-'),''])
		else: lowerBy+=1

nCat = 1
shifts = {}
for nui in nuisNam: shifts[nui] = []
for ind in obsIndexes:
	print "\\begin{table}"
	print "\\centering"
	print "\\topcaption{Pre-fit uncertainties in the",
	if "isE" in observables[obsIndexes.index(ind)]: print "electron channel with",
	if "isM" in observables[obsIndexes.index(ind)]: print "muon channel with",
	if "nT0p" in observables[obsIndexes.index(ind)]: print "0 or more top tag,",
	elif "nT0" in observables[obsIndexes.index(ind)]: print "0 top tag,",
	if "nT1p" in observables[obsIndexes.index(ind)]: print "1 or more top tag,",
	if "nW0p" in observables[obsIndexes.index(ind)]: print "0 or more W tag, and",
	elif "nW0" in observables[obsIndexes.index(ind)]: print "0 W tag, and",
	if "nW1p" in observables[obsIndexes.index(ind)]: print "1 or more W tag, and",
	if "nB0" in observables[obsIndexes.index(ind)]: print "0 b tag.}"
	if "nB1" in observables[obsIndexes.index(ind)]: print "1 b tag.}"
	if "nB2p" in observables[obsIndexes.index(ind)]: print "2 or more b tag.}"
	print "\\begin{tabular}{|c|c|c|c|c|}"
	print "\\hline"
	print "Nuisance Parameter & X53X53900LH & TOP & EWK & QCD \\\\"
	print "\\hline"
	for nui in nuisNam:
		if nui!='muRFcorrdNew':continue
		print nuisNamPlot[nui]+' (gauss)'+' & ',
		i = prefitUncs[ind]['main'].index(['sig'+nui,'(gauss)'])
		print prefitUncs[ind]['sig'][i][0]+' '+prefitUncs[ind]['sig'][i][1]+' & ',
		i = prefitUncs[ind]['main'].index(['top'+nui,'(gauss)'])
		print prefitUncs[ind]['top'][i][0]+' '+prefitUncs[ind]['top'][i][1]+' & ',
		shifts[nui].append(abs(float(prefitUncs[ind]['top'][i][0].split('}_{')[0][3:])))
		shifts[nui].append(abs(float(prefitUncs[ind]['top'][i][0].split('}_{')[1][:-2])))
		i = prefitUncs[ind]['main'].index(['ewk'+nui,'(gauss)'])
		try: print prefitUncs[ind]['ewk'][i][0]+' '+prefitUncs[ind]['ewk'][i][1]+' & ',
		except: print '-  & ',
		i = prefitUncs[ind]['main'].index(['qcd'+nui,'(gauss)'])
		try: print prefitUncs[ind]['qcd'][i][0]+' '+prefitUncs[ind]['qcd'][i][1]+' \\\\'
		except: print '- \\\\'
# 		try:
# 			shifts[nui].append(abs(float(prefitUncs[ind]['sig'][i][0].split('}_{')[0][3:])))
# 			shifts[nui].append(abs(float(prefitUncs[ind]['sig'][i][0].split('}_{')[1][:-2])))
# 		except: pass
		try:
			shifts[nui].append(abs(float(prefitUncs[ind]['top'][i][0].split('}_{')[0][3:])))
			shifts[nui].append(abs(float(prefitUncs[ind]['top'][i][0].split('}_{')[1][:-2])))
		except: pass
		try: 
			shifts[nui].append(abs(float(prefitUncs[ind]['ewk'][i][0].split('}_{')[0][3:])))
			shifts[nui].append(abs(float(prefitUncs[ind]['ewk'][i][0].split('}_{')[1][:-2])))
		except: pass
# 		try: 
# 			shifts[nui].append(abs(float(prefitUncs[ind]['qcd'][i][0].split('}_{')[0][3:])))
# 			shifts[nui].append(abs(float(prefitUncs[ind]['qcd'][i][0].split('}_{')[1][:-2])))
# 		except: pass
	for nui in nuisNam:
		if nui=='muRFcorrdNew':continue
		i = prefitUncs[ind]['main'].index([nui,'(gauss)'])
		if prefitUncs[ind]['sig'][i][0]=='-' and prefitUncs[ind]['top'][i][0]=='-' and prefitUncs[ind]['ewk'][i][0]=='-': continue
		print nuisNamPlot[nui]+' (gauss)'+' & ',
		print prefitUncs[ind]['sig'][i][0]+' '+prefitUncs[ind]['sig'][i][1]+' & ',
		print prefitUncs[ind]['top'][i][0]+' '+prefitUncs[ind]['top'][i][1]+' & ',
		try: print prefitUncs[ind]['ewk'][i][0]+' '+prefitUncs[ind]['ewk'][i][1]+' & ',
		except: print '-  & ',
		try: print prefitUncs[ind]['qcd'][i][0]+' '+prefitUncs[ind]['qcd'][i][1]+' \\\\'
		except: print '- \\\\'
# 		try:
# 			shifts[nui].append(abs(float(prefitUncs[ind]['sig'][i][0].split('}_{')[0][3:])))
# 			shifts[nui].append(abs(float(prefitUncs[ind]['sig'][i][0].split('}_{')[1][:-2])))
# 		except: pass
		try:
			shifts[nui].append(abs(float(prefitUncs[ind]['top'][i][0].split('}_{')[0][3:])))
			shifts[nui].append(abs(float(prefitUncs[ind]['top'][i][0].split('}_{')[1][:-2])))
		except: pass
		try: 
			shifts[nui].append(abs(float(prefitUncs[ind]['ewk'][i][0].split('}_{')[0][3:])))
			shifts[nui].append(abs(float(prefitUncs[ind]['ewk'][i][0].split('}_{')[1][:-2])))
		except: pass
# 		try: 
# 			shifts[nui].append(abs(float(prefitUncs[ind]['qcd'][i][0].split('}_{')[0][3:])))
# 			shifts[nui].append(abs(float(prefitUncs[ind]['qcd'][i][0].split('}_{')[1][:-2])))
# 		except: pass
	print "\\hline"
	print "\\end{tabular}"
	print "\\label{tab:prefitCat"+str(nCat)+"}"
	nCat+=1
	print "\\end{table}"
	print

preFitUncRanges = {}
for nui in shifts.keys():
	try: preFitUncRanges[nui]=[min(shifts[nui]),max(shifts[nui])]
	except: preFitUncRanges[nui]=[]
for nui in sorted(preFitUncRanges.keys()): print nui,preFitUncRanges[nui]