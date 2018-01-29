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
	#'muRFcorrdNewTTbar',
	#'muRFcorrdNewWJets',
	#'muRFcorrdNewSingleTop',
	#'muRFcorrdNewEWK',
	#'muRFcorrdNewDYJets',
	#'muRFcorrdNewQCD',
	'TTbarscale',
	'SingleTopscale',
	'EWKscale',
	'QCDscale',
	'muRFcorrdNewSig',
	'pdfNew',
	#'toppt',
	'jsf',
	'btag',
	'mistag',
	'taupt',
	'tau21',
	'jmr',
	'jms',
	'htag_prop',
	'jer',
	'jec',
	'pileup',
	'lumiSys',
	'trigeffEl',
	'trigeffMu',
	'muIsoSys',
	'elIsoSys',
	'muIdSys',
	'elIdSys',
	'muRecoSys',
	'elRecoSys',
	]

nuisNamPlot = [
	'\\ttbar scale',
	#'W+jets scale',
	'Single t scale',
	'W/Z/V scale',
	#'DY+jets scale',
	'QCD scale',
	'Signal scale',
	'PDF',
	#'Top \pt',
	'\HT scale',
	'B tag: bc',
	'B tag: udsg',
	'W tag: $\\tau_{2}/\\tau_{1}$ \pt',
	'W tag: $\\tau_{2}/\\tau_{1}$',
	'W/H tag: smear',
	'W/H tag: scale',
	'H tag: prop',
	'JER',
	'JES',
	'Pileup',
	'Lumi',
	'Trigger: e',	
	'Trigger: $\mu$',
	'Iso: $\mu$',
	'Iso: $e$',
	'ID: $\mu$',
	'ID: $e$',
	'Reco: $\mu$',
	'Reco: $e$',
	]

dyInd = 1
qcdInd = 2
stInd = 3
ttInd = 4
#wjInd = 5
#vvInd = 6
#sigInd = 7
sigInd = 5
prefitUncs = {}
for ind in obsIndexes:
	lowerBy = 0
	prefitUncs[ind] = {}
	data = prefitlines[ind].strip().split()
	prefitUncs[ind]['main'] = []
	for item in data: 
		if 'process' in item or '/' in item or 'nuisance' in item or 'parameter' in item or 'gauss' in item: continue
		prefitUncs[ind]['main'].append([item,'(gauss)'])
	#if prefitlines[ind+dyInd-lowerBy].startswith('DYJets'): 
	if prefitlines[ind+dyInd-lowerBy].startswith('EWK'): 
		data = prefitlines[ind+dyInd-lowerBy].strip().split()
		prefitUncs[ind]['ewk'] = []
		for it in range(1,len(data)): 
			if '(s)' in data[it] or '(r)' in data[it]: continue
			if it==len(data)-1 and data[it]!='---': continue
			if data[it]!='---': 
				if data[it].startswith('pm'): prefitUncs[ind]['ewk'].append([data[it].replace('pm','$\pm$'),data[it+1]])
				elif data[it].startswith('mp'): prefitUncs[ind]['ewk'].append([data[it].replace('mp','$\mp$'),data[it+1]])
				else:
					for k in range(1,len(data[it])):
						if not (data[it][k].isdigit() or data[it][k]=='.'): 
							up = data[it][:k]
							dn = data[it][k:]
					prefitUncs[ind]['ewk'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
			else: prefitUncs[ind]['ewk'].append([data[it].replace('---','-'),''])
	else: lowerBy+=1
	if prefitlines[ind+qcdInd-lowerBy].startswith('QCD'): 
		data = prefitlines[ind+qcdInd-lowerBy].strip().split()
		prefitUncs[ind]['qcd'] = []
		for it in range(1,len(data)): 
			if '(s)' in data[it] or '(r)' in data[it]: continue
			if it==len(data)-1 and data[it]!='---': continue
			if data[it]!='---': 
				if data[it].startswith('pm'): prefitUncs[ind]['qcd'].append([data[it].replace('pm','$\pm$'),data[it+1]])
				elif data[it].startswith('mp'): prefitUncs[ind]['qcd'].append([data[it].replace('mp','$\mp$'),data[it+1]])
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
				elif data[it].startswith('mp'): prefitUncs[ind]['st'].append([data[it].replace('mp','$\mp$'),data[it+1]])
				else:
					for k in range(1,len(data[it])):
						if not (data[it][k].isdigit() or data[it][k]=='.'): 
							up = data[it][:k]
							dn = data[it][k:]
					prefitUncs[ind]['st'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
			else: prefitUncs[ind]['st'].append([data[it].replace('---','-'),''])	
	else: lowerBy+=1
	if prefitlines[ind+ttInd-lowerBy].startswith('TTbar'): 
		data = prefitlines[ind+ttInd-lowerBy].strip().split()
		prefitUncs[ind]['top'] = []
		for it in range(1,len(data)): 
			if '(s)' in data[it] or '(r)' in data[it]: continue
			if it==len(data)-1 and data[it]!='---': continue
			if data[it]!='---': 
				if data[it].startswith('pm'): prefitUncs[ind]['top'].append([data[it].replace('pm','$\pm$'),data[it+1]])
				elif data[it].startswith('mp'): prefitUncs[ind]['top'].append([data[it].replace('mp','$\mp$'),data[it+1]])
				else:
					for k in range(1,len(data[it])):
						if not (data[it][k].isdigit() or data[it][k]=='.'): 
							up = data[it][:k]
							dn = data[it][k:]
					prefitUncs[ind]['top'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
			else: prefitUncs[ind]['top'].append([data[it].replace('---','-'),''])	
	else: lowerBy+=1
	# if prefitlines[ind+wjInd-lowerBy].startswith('WJets'): 
	# 	data = prefitlines[ind+wjInd-lowerBy].strip().split()
	# 	prefitUncs[ind]['wj'] = []
	# 	for it in range(1,len(data)): 
	# 		if '(s)' in data[it] or '(r)' in data[it]: continue
	# 		if it==len(data)-1 and data[it]!='---': continue
	# 		if data[it]!='---': 
	# 			if data[it].startswith('pm'): prefitUncs[ind]['wj'].append([data[it].replace('pm','$\pm$'),data[it+1]])
	# 			elif data[it].startswith('mp'): prefitUncs[ind]['wj'].append([data[it].replace('mp','$\mp$'),data[it+1]])
	# 			else:
	# 				for k in range(1,len(data[it])):
	# 					if not (data[it][k].isdigit() or data[it][k]=='.'): 
	# 						up = data[it][:k]
	# 						dn = data[it][k:]
	# 				prefitUncs[ind]['wj'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
	# 		else: prefitUncs[ind]['wj'].append([data[it].replace('---','-'),''])
	# else: lowerBy+=1
	# if prefitlines[ind+vvInd-lowerBy].startswith('ewk'): 
	# 	data = prefitlines[ind+vvInd-lowerBy].strip().split()
	# 	prefitUncs[ind]['dib'] = []
	# 	for it in range(1,len(data)): 
	# 		if '(s)' in data[it] or '(r)' in data[it]: continue
	# 		if it==len(data)-1 and data[it]!='---': continue
	# 		if data[it]!='---': 
	# 			if data[it].startswith('pm'): prefitUncs[ind]['dib'].append([data[it].replace('pm','$\pm$'),data[it+1]])
	# 			elif data[it].startswith('mp'): prefitUncs[ind]['dib'].append([data[it].replace('mp','$\mp$'),data[it+1]])
	# 			else:
	# 				for k in range(1,len(data[it])):
	# 					if not (data[it][k].isdigit() or data[it][k]=='.'): 
	# 						up = data[it][:k]
	# 						dn = data[it][k:]
	# 				prefitUncs[ind]['dib'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
	# 		else: prefitUncs[ind]['dib'].append([data[it].replace('---','-'),''])
	# else: lowerBy+=1
	if prefitlines[ind+sigInd-lowerBy].startswith('sig'): 
		data = prefitlines[ind+sigInd-lowerBy].strip().split()
		prefitUncs[ind]['sig'] = []
		for it in range(1,len(data)): 
			if '(s)' in data[it] or '(r)' in data[it]: continue
			if it==len(data)-1 and data[it]!='---': continue
			if data[it]!='---': 
				if data[it].startswith('pm'): prefitUncs[ind]['sig'].append([data[it].replace('pm','$\pm$'),data[it+1]])
				elif data[it].startswith('mp'): prefitUncs[ind]['sig'].append([data[it].replace('mp','$\mp$'),data[it+1]])
				else:
					for k in range(1,len(data[it])):
						if not (data[it][k].isdigit() or data[it][k]=='.'): 
							up = data[it][:k]
							dn = data[it][k:]
					prefitUncs[ind]['sig'].append(['$^{'+up+'}_{'+dn+'}$',data[it+1]])
			else: prefitUncs[ind]['sig'].append([data[it].replace('---','-'),''])	


nCat = 1
for ind in obsIndexes:
	print "\\begin{table}"
	print "\\centering"
	print "\\topcaption{Pre-fit uncertainties in the",
	if "isE" in observables[obsIndexes.index(ind)] and 'isSR' in observables[obsIndexes.index(ind)]: print "electron channel signal region with",
	if "isM" in observables[obsIndexes.index(ind)] and 'isSR' in observables[obsIndexes.index(ind)]: print "muon channel signal region with",
	if "isE" in observables[obsIndexes.index(ind)] and 'isCR' in observables[obsIndexes.index(ind)]: print "electron channel control region with",
	if "isM" in observables[obsIndexes.index(ind)] and 'isCR' in observables[obsIndexes.index(ind)]: print "muon channel control region with",
	if "nH1b" in observables[obsIndexes.index(ind)]: print "a 1b Higgs tag,",
	if "nH2b" in observables[obsIndexes.index(ind)]: print "a 2b Higgs tag,",
	if "nH1p" in observables[obsIndexes.index(ind)]: print "$\geq 1$ Higgs tags,",
	if "nW0_" in observables[obsIndexes.index(ind)]: print "0 Higgs tags, 0 W tags and",
	if "nW0p_" in observables[obsIndexes.index(ind)]: 
		if "nH0" not in observables[obsIndexes.index(ind)]: print "$\geq 0$ W tags and",
		else: print "0 Higgs tags, $\geq 0$ W tags and",
	if "nW1p" in observables[obsIndexes.index(ind)]: print "0 Higgs tags, $\geq 1$ W tags and",
	if "nB0_" in observables[obsIndexes.index(ind)]: print "0 b tags.}"
	if "nB1_" in observables[obsIndexes.index(ind)]: print "1 b tag.}"
	if "nB1p_" in observables[obsIndexes.index(ind)]: print "$\geq 1$ b tags.}"
	if "nB2_" in observables[obsIndexes.index(ind)]: print "2 b tags.}"
	if "nB3p" in observables[obsIndexes.index(ind)]: print "$\geq 3$ b tags.}"
	print
	#print "\\begin{tabular}{|l||c|c|c|c|c|c|c|}"
	print "\\begin{tabular}{|l||c|c|c|c|c|c|c|}"
	print "\\hline"
	#print "Nuisance & \TTbar (1.0 \TeV) & \\ttbar & W + jets & single t & Z + jets & VV & QCD \\\\"
	print "Nuisance & \TTbar (1.0 \TeV) & \\ttbar & single t & EWK & QCD \\\\"
	print "\\hline"

	for nui in nuisNam:
		i = prefitUncs[ind]['main'].index([nui,'(gauss)'])
		#if prefitUncs[ind]['sig'][i][0]=='-' and prefitUncs[ind]['top'][i][0]=='-' and prefitUncs[ind]['st'][i][0]=='-' and prefitUncs[ind]['wj'][i][0]=='-': 
		if prefitUncs[ind]['sig'][i][0]=='-' and prefitUncs[ind]['top'][i][0]=='-' and prefitUncs[ind]['st'][i][0]=='-': 
			if 'SignalRegion' in observables[obsIndexes.index(ind)]:
				if nui != 'muRFcorrdNewEWK' and nui != 'muRFcorrdNewQCD' and nui != 'EWKscale' and nui != 'QCDscale': continue
			elif nui != 'muRFcorrdNewEWK' and nui != 'muRFcorrdNewQCD' and nui != 'EWKscale' and nui != 'QCDscale': continue
			#else: continue
		print nuisNamPlot[nuisNam.index(nui)]+' & ',
		print prefitUncs[ind]['sig'][i][0]+' '+prefitUncs[ind]['sig'][i][1]+' & ',
		print prefitUncs[ind]['top'][i][0]+' '+prefitUncs[ind]['top'][i][1]+' & ',
		#print prefitUncs[ind]['wj'][i][0]+' '+prefitUncs[ind]['wj'][i][1]+' & ',
		print prefitUncs[ind]['st'][i][0]+' '+prefitUncs[ind]['st'][i][1]+' & ',
		try: print prefitUncs[ind]['ewk'][i][0]+' '+prefitUncs[ind]['ewk'][i][1]+' & ',
		except: print '- & ',
		#try: print prefitUncs[ind]['dib'][i][0]+' '+prefitUncs[ind]['dib'][i][1]+' & ',
		#except: print '- & ',
		try: print prefitUncs[ind]['qcd'][i][0]+' '+prefitUncs[ind]['qcd'][i][1]+' \\\\'
		except: print '- \\\\'
			

	print "\\hline"
	print "\\end{tabular}"
	print "\\label{tab:prefitCat"+str(nCat)+"}"
	nCat+=1
	print "\\end{table}"
	print

