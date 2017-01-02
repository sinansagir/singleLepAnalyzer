#!/usr/bin/python

import os,sys,time,math

prefitFile = 'prefit.txt' # replace "plusminus" sign with "pm" in the file

fprefit = open(prefitFile, 'rU')
prefitlines = fprefit.readlines()
fprefit.close()

obsIndexes  = []
observables = []
for ind in range(len(prefitlines)):
	if prefitlines[ind].startswith('process / nuisance parameter'): 
		obsIndexes.append(ind)
		observables.append(prefitlines[ind-1])

nuisNam = [
	'TTbar_rate',
	'WJets_rate',
	'SingleTop_rate',
	'Diboson_rate',
	#'DYJets_rate',
	'QCD_rate',
	'PDF',
	'ScaleVar',
	'q2',
	'taupt',
	'tau21',
	#'jms',
	#'jmr',
	'jsf',
	'btag_bc',
	'btag_udsg',
	'higgs_smear',
	'higgs_py2hw',
	'jer',
	'jec',
	'pu',
	'luminosity',
	'sfmu_trg',
	'sfel_trg',
	'sfmu_iso',
	'sfel_iso',
	'sfmu_id',
	'sfel_id',
	#'top1pW3pBSys',
	#'top1pW2BSys',
	#'top1pW1BSys',
	#'top1pW0BSys',
	#'top0W3pBSys',
	#'top0W2BSys',
	#'top0W1BSys',
	#'top0W0BSys',
	#'ewk1pW3pBSys',
	#'ewk1pW2BSys',
	#'ewk1pW1BSys',
	#'ewk1pW0BSys',
	#'ewk0W3pBSys',
	#'ewk0W2BSys',
	#'ewk0W1BSys',
	#'ewk0W0BSys',
	]

nuisNamPlot = [
	'\\ttbar rate',
	'W+jets rate',
	'Single t rate',
	'VV rate',
	#'DY+jets rate',
	'QCD rate',
	'PDF',
	'ME Scale',
	'Top shower',
	#'Top \pt',
	'W tag: $\\tau_{2}/\\tau_{1}$ \pt',
	'W tag: $\\tau_{2}/\\tau_{1}$',
	#'W tag: scale',
	#'W tag: res',
	'Jet Reweight',
	'B tag: bc',
	'B tag: udsg',
	'H tag: smear',
	'H tag: gen',
	'JER',
	'JES',
	'Pileup',
	'Lumi',
	'Trigger: $\mu$',
	'Trigger: $e$',
	'Iso: $\mu$',
	'Iso: $e$',
	'ID: $\mu$',
	'ID: $e$',
	#'Top 1+W 3+b',
	#'Top 1+W 2b',
	#'Top 1+W 1b',
	#'Top 1+W 0b',
	#'Top 0W 3+b',
	#'Top 0W 2b',
	#'Top 0W 1b',
	#'Top 0W 0b',
	#'Ewk 1+W 3+b',
	#'Ewk 1+W 2b',
	#'Ewk 1+W 1b',
	#'Ewk 1+W 0b',
	#'Ewk 0W 3+b',
	#'Ewk 0W 2b',
	#'Ewk 0W 1b',
	#'Ewk 0W 0b',
	]

ewkInd = 1
dibInd = 2
qcdInd = 3
stInd = 4
topInd = 5
sigInd = 6
wjInd = 7
prefitUncs = {}
for ind in obsIndexes:
	lowerBy = 0
	prefitUncs[ind] = {}
	data = prefitlines[ind].strip().split()
	prefitUncs[ind]['main'] = []
	for item in data: 
		if 'process' in item or '/' in item or 'nuisance' in item or 'parameter' in item or 'gauss' in item: continue
		prefitUncs[ind]['main'].append([item,'(gauss)'])
	if prefitlines[ind+ewkInd-lowerBy].startswith('DYJets'): 
		data = prefitlines[ind+ewkInd-lowerBy].strip().split()
		prefitUncs[ind]['ewk'] = []
		for it in range(1,len(data)): 
			if '(s)' in data[it] or '(r)' in data[it]: continue
			if it==len(data)-1 and data[it]!='---': continue
			if data[it]!='---': 
				if data[it].startswith('pm'): prefitUncs[ind]['ewk'].append([data[it].replace('pm','$\pm$'),data[it+1]])
				else:
					for k in range(1,len(data[it])):
						if not (data[it][k].isdigit() or data[it][k]=='.'): 
							up = data[it][:k]
							dn = data[it][k:]
					prefitUncs[ind]['ewk'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
			else: prefitUncs[ind]['ewk'].append([data[it].replace('---','-'),''])
	else: lowerBy+=1
	if prefitlines[ind+dibInd-lowerBy].startswith('Diboson'): 
		data = prefitlines[ind+dibInd-lowerBy].strip().split()
		prefitUncs[ind]['dib'] = []
		for it in range(1,len(data)): 
			if '(s)' in data[it] or '(r)' in data[it]: continue
			if it==len(data)-1 and data[it]!='---': continue
			if data[it]!='---': 
				if data[it].startswith('pm'): prefitUncs[ind]['dib'].append([data[it].replace('pm','$\pm$'),data[it+1]])
				else:
					for k in range(1,len(data[it])):
						if not (data[it][k].isdigit() or data[it][k]=='.'): 
							up = data[it][:k]
							dn = data[it][k:]
					prefitUncs[ind]['dib'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
			else: prefitUncs[ind]['dib'].append([data[it].replace('---','-'),''])
	else: lowerBy+=1
	if prefitlines[ind+qcdInd-lowerBy].startswith('QCD'): 
		data = prefitlines[ind+qcdInd-lowerBy].strip().split()
		prefitUncs[ind]['qcd'] = []
		for it in range(1,len(data)): 
			if '(s)' in data[it] or '(r)' in data[it]: continue
			if it==len(data)-1 and data[it]!='---': continue
			if data[it]!='---': 
				if data[it].startswith('pm'): prefitUncs[ind]['qcd'].append([data[it].replace('pm','$\pm$'),data[it+1]])
				else:
					for k in range(1,len(data[it])):
						if not (data[it][k].isdigit() or data[it][k]=='.'): 
							up = data[it][:k]
							dn = data[it][k:]
					prefitUncs[ind]['qcd'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
			else: prefitUncs[ind]['qcd'].append([data[it].replace('---','-'),''])	
	else: lowerBy+=1
	if prefitlines[ind+stInd-lowerBy].startswith('SingleTop'): 
		data = prefitlines[ind+stInd-lowerBy].strip().split()
		prefitUncs[ind]['st'] = []
		for it in range(1,len(data)): 
			if '(s)' in data[it] or '(r)' in data[it]: continue
			if it==len(data)-1 and data[it]!='---': continue
			if data[it]!='---': 
				if data[it].startswith('pm'): prefitUncs[ind]['st'].append([data[it].replace('pm','$\pm$'),data[it+1]])
				else:
					for k in range(1,len(data[it])):
						if not (data[it][k].isdigit() or data[it][k]=='.'): 
							up = data[it][:k]
							dn = data[it][k:]
					prefitUncs[ind]['st'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
			else: prefitUncs[ind]['st'].append([data[it].replace('---','-'),''])	
	else: lowerBy+=1
	if prefitlines[ind+topInd-lowerBy].startswith('TTbar'): 
		data = prefitlines[ind+topInd-lowerBy].strip().split()
		prefitUncs[ind]['top'] = []
		for it in range(1,len(data)): 
			if '(s)' in data[it] or '(r)' in data[it]: continue
			if it==len(data)-1 and data[it]!='---': continue
			if data[it]!='---': 
				if data[it].startswith('pm'): prefitUncs[ind]['top'].append([data[it].replace('pm','$\pm$'),data[it+1]])
				else:
					for k in range(1,len(data[it])):
						if not (data[it][k].isdigit() or data[it][k]=='.'): 
							up = data[it][:k]
							dn = data[it][k:]
					prefitUncs[ind]['top'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
			else: prefitUncs[ind]['top'].append([data[it].replace('---','-'),''])	
	else: lowerBy+=1
	if prefitlines[ind+sigInd-lowerBy].startswith('TpTp'): 
		data = prefitlines[ind+sigInd-lowerBy].strip().split()
		prefitUncs[ind]['sig'] = []
		for it in range(1,len(data)): 
			if '(s)' in data[it] or '(r)' in data[it]: continue
			if it==len(data)-1 and data[it]!='---': continue
			if data[it]!='---': 
				if data[it].startswith('pm'): prefitUncs[ind]['sig'].append([data[it].replace('pm','$\pm$'),data[it+1]])
				else:
					for k in range(1,len(data[it])):
						if not (data[it][k].isdigit() or data[it][k]=='.'): 
							up = data[it][:k]
							dn = data[it][k:]
					prefitUncs[ind]['sig'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
			else: prefitUncs[ind]['sig'].append([data[it].replace('---','-'),''])	
	else: lowerBy+=1
	if prefitlines[ind+wjInd-lowerBy].startswith('WJets'): 
		data = prefitlines[ind+wjInd-lowerBy].strip().split()
		prefitUncs[ind]['wj'] = []
		for it in range(1,len(data)): 
			if '(s)' in data[it] or '(r)' in data[it]: continue
			if it==len(data)-1 and data[it]!='---': continue
			if data[it]!='---': 
				if data[it].startswith('pm'): prefitUncs[ind]['wj'].append([data[it].replace('pm','$\pm$'),data[it+1]])
				else:
					for k in range(1,len(data[it])):
						if not (data[it][k].isdigit() or data[it][k]=='.'): 
							up = data[it][:k]
							dn = data[it][k:]
					prefitUncs[ind]['wj'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
			else: prefitUncs[ind]['wj'].append([data[it].replace('---','-'),''])

nCat = 1
for ind in obsIndexes:
	print "\\begin{table}"
	print "\\centering"
	print "\\topcaption{Pre-fit uncertainties in the",
	if "isE" in observables[obsIndexes.index(ind)]: print "electron channel with",
	if "isM" in observables[obsIndexes.index(ind)]: print "muon channel with",
	if "El45" in observables[obsIndexes.index(ind)]: print "electron channel with",
	if "Mu45" in observables[obsIndexes.index(ind)]: print "muon channel with",
	if "SignalRegion1b" in observables[obsIndexes.index(ind)]: print "a 1b Higgs tag.}",
	if "SignalRegion2b" in observables[obsIndexes.index(ind)]: print "a 2b Higgs tag.}",
	if "nW0" in observables[obsIndexes.index(ind)]: print "0 W tag and",
	if "nW1p" in observables[obsIndexes.index(ind)]: print "1 or more W tag and",
	if "nB0" in observables[obsIndexes.index(ind)]: print "0 b tag.}"
	if "nB1" in observables[obsIndexes.index(ind)]: print "1 b tag.}"
	if "nB2" in observables[obsIndexes.index(ind)]: print "2 b tag.}"
	if "nB3p" in observables[obsIndexes.index(ind)]: print "3 or more b tag.}"
	print
	print "\\begin{tabular}{|l||c|c|c|c|c|c|c|}"
	print "\\hline"
	print "Nuisance & \TTbar (0.8 \GeV) & \\ttbar & W + jets & single t & DY + jets & VV & QCD \\\\"
	print "\\hline"

	for nui in nuisNam:
		i = prefitUncs[ind]['main'].index([nui,'(gauss)'])
		if prefitUncs[ind]['sig'][i][0]=='-' and prefitUncs[ind]['top'][i][0]=='-' and prefitUncs[ind]['st'][i][0]=='-' and prefitUncs[ind]['wj'][i][0]=='-': 
			if 'SignalRegion' in observables[obsIndexes.index(ind)]:
				if nui != 'Diboson_rate' and nui != 'QCD_rate': continue
			elif nui != 'Diboson_rate': continue
			#else: continue
		print nuisNamPlot[nuisNam.index(nui)]+' & ',
		print prefitUncs[ind]['sig'][i][0]+' '+prefitUncs[ind]['sig'][i][1]+' & ',
		print prefitUncs[ind]['top'][i][0]+' '+prefitUncs[ind]['top'][i][1]+' & ',
		print prefitUncs[ind]['wj'][i][0]+' '+prefitUncs[ind]['wj'][i][1]+' & ',
		print prefitUncs[ind]['st'][i][0]+' '+prefitUncs[ind]['st'][i][1]+' & ',
		try: print prefitUncs[ind]['ewk'][i][0]+' '+prefitUncs[ind]['ewk'][i][1]+' & ',
		except: print '- & ',
		try: print prefitUncs[ind]['dib'][i][0]+' '+prefitUncs[ind]['dib'][i][1]+' & ',
		except: print '- & ',
		try: print prefitUncs[ind]['qcd'][i][0]+' '+prefitUncs[ind]['qcd'][i][1]+' \\\\'
		except: print '- \\\\'
			

	print "\\hline"
	print "\\end{tabular}"
	print "\\label{tab:prefitCat"+str(nCat)+"}"
	nCat+=1
	print "\\end{table}"
	print

