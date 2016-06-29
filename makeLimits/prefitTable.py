#!/usr/bin/python

import os,sys,time,math

prefitFile = 'templates_minMlb_noJSF_2016_6_22plots/prefit800left.txt' # replace "plusminus" sign with "pm" in the file

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
			'q2',
			'toppt',
			'tau21',
			'jms',
			'jmr',
			#'jsf',
			'topsf',
			'btag',
			'mistag',
			'jer',
			'jec',
			'pileup',
			'top0T0W1BSys',
			'top0T0W2pBSys',
			'top0T1pW1BSys',
			'top0T1pW2pBSys',
			'top1pT0W1BSys',
			'top1pT0W2pBSys',
			'top1pT1pW1BSys',
			'top1pT1pW2pBSys',
			'ewk0T0W1BSys',
			'ewk0T0W2pBSys',
			'ewk0T1pW1BSys',
			'ewk0T1pW2pBSys',
			'ewk1pT0W1BSys',
			'ewk1pT0W2pBSys',
			'ewk1pT1pW1BSys',
			'ewk1pT1pW2pBSys',
			'muTrigSys',
			'elTrigSys',
			'muIsoSys',
			'elIsoSys',
			'muIdSys',
			'elIdSys',
			'lumiSys',
			]

nuisNamPlot = [
			'PDF',
			'muRF',
			'$Q^{2}$',
			'Top Pt',
			'Tau21',
			'JMS',
			'JMR',
			#'JSF',
			't-tag',
			'b-tag',
			'mis-tag',
			'JER',
			'JEC',
			'pileup',
			'top\_0t\_0W\_1b',
			'top\_0t\_0W\_2+b',
			'top\_0t\_1+W\_1b',
			'top\_0t\_1+W\_2+b',
			'top\_1+t\_0W\_1b',
			'top\_1+t\_0W\_2+b',
			'top\_1+t\_1+W\_1b',
			'top\_1+t\_1+W\_2+b',
			'ewk\_0t\_0W\_1b',
			'ewk\_0t\_0W\_2+b',
			'ewk\_0t\_1+W\_1b',
			'ewk\_0t\_1+W\_2+b',
			'ewk\_1+t\_0W\_1b',
			'ewk\_1+t\_0W\_2+b',
			'ewk\_1+t\_1+W\_1b',
			'ewk\_1+t\_1+W\_2+b',
			'muTrig',
			'elTrig',
			'muIso',
			'elIso',
			'muId',
			'elId',
			'lumi',
			]

ewkInd = 1
qcdInd = 2
sigInd = 3
topInd = 4
prefitUncs = {}
for ind in obsIndexes:
	lowerBy = 0
	prefitUncs[ind] = {}
	data = prefitlines[ind].strip().split()
	prefitUncs[ind]['main'] = []
	for item in data: 
		if 'process' in item or '/' in item or 'nuisance' in item or 'parameter' in item or 'gauss' in item: continue
		prefitUncs[ind]['main'].append([item,'(gauss)'])
	if prefitlines[ind+ewkInd-lowerBy].startswith('ewk'): 
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
	if prefitlines[ind+qcdInd-lowerBy].startswith('qcd'): 
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
	if prefitlines[ind+sigInd-lowerBy].startswith('sig'): 
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
	if prefitlines[ind+topInd-lowerBy].startswith('top'): 
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

nCat = 1
for ind in obsIndexes:
	print "\\begin{table}"
	print "\\centering"
	print "\\topcaption{Pre-fit uncertainties in the",
	if "isE" in observables[obsIndexes.index(ind)]: print "electron channel with",
	if "isM" in observables[obsIndexes.index(ind)]: print "muon channel with",
	if "nT0" in observables[obsIndexes.index(ind)]: print "0 top tag and",
	if "nT1p" in observables[obsIndexes.index(ind)]: print "1 or more top tag and",
	if "nW0" in observables[obsIndexes.index(ind)]: print "0 W tag and",
	if "nW1p" in observables[obsIndexes.index(ind)]: print "1 or more W tag and",
	if "nB0" in observables[obsIndexes.index(ind)]: print "0 b tag.}"
	if "nB1" in observables[obsIndexes.index(ind)]: print "1 b tag.}"
	if "nB2p" in observables[obsIndexes.index(ind)]: print "2 or more b tag.}"
	print "\\begin{tabular}{|c||c|c|c|c|}"
	print "\\hline"
	print "Nuisance Parameter & X53X53800LH & TOP & EWK & QCD \\\\"
	print "\\hline"
	for nui in nuisNam:
		i = prefitUncs[ind]['main'].index([nui,'(gauss)'])
		if prefitUncs[ind]['sig'][i][0]=='-' and prefitUncs[ind]['top'][i][0]=='-': continue
		print nuisNamPlot[nuisNam.index(nui)]+' (gauss)'+' & ',
		print prefitUncs[ind]['sig'][i][0]+' '+prefitUncs[ind]['sig'][i][1]+' & ',
		print prefitUncs[ind]['top'][i][0]+' '+prefitUncs[ind]['top'][i][1]+' & ',
		try: print prefitUncs[ind]['ewk'][i][0]+' '+prefitUncs[ind]['ewk'][i][1]+' & ',
		except: print '-  & ',
		try: print prefitUncs[ind]['qcd'][i][0]+' '+prefitUncs[ind]['qcd'][i][1]+' \\\\'
		except: print '- \\\\'
	print "\\hline"
	print "\\end{tabular}"
	print "\\label{tab:prefitCat"+str(nCat)+"}"
	nCat+=1
	print "\\end{table}"
	print

