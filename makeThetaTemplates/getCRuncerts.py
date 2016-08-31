#!/usr/bin/python

import os,sys,time,math

templateYields = 'templates_minMlb_ObjRev/SelectionFile/yields_minMlb_12p892fb.txt' 
ttbarYields = '../makeCRs/ttbar_tptp_ObjRev/yields_minMlb_12p892fb.txt'
wjetsYields = '../makeCRs/wjets_tptp_ObjRev/yields_minMlb_12p892fb.txt'

ftemplate = open(templateYields, 'rU')
templatelines = ftemplate.readlines()
ftemplate.close()
fttbar = open(ttbarYields, 'rU')
ttbarlines = fttbar.readlines()
fttbar.close()
fwjets = open(wjetsYields, 'rU')
wjetslines = fwjets.readlines()
fwjets.close()

EpJetsLineTemplateInd = templatelines.index([line for line in templatelines if line.startswith('YIELDS ELECTRON+JETS')][0])
MpJetsLineTemplateInd = templatelines.index([line for line in templatelines if line.startswith('YIELDS MUON+JETS')][0])
EpJetsLineTtbarInd = ttbarlines.index([line for line in ttbarlines if line.startswith('YIELDS ELECTRON+JETS')][0])
MpJetsLineTtbarInd = ttbarlines.index([line for line in ttbarlines if line.startswith('YIELDS MUON+JETS')][0])
EpJetsLineWjetsInd = wjetslines.index([line for line in wjetslines if line.startswith('YIELDS ELECTRON+JETS')][0])
MpJetsLineWjetsInd = wjetslines.index([line for line in wjetslines if line.startswith('YIELDS MUON+JETS')][0])

yieldsEl = {}
ind = 0
for cat in templatelines[EpJetsLineTemplateInd].split()[2:]:
	yieldsEl['top_'+cat] = float(templatelines[EpJetsLineTemplateInd+10].split()[2+ind*4])
	yieldsEl['ewk_'+cat] = float(templatelines[EpJetsLineTemplateInd+9].split()[2+ind*4])
	ind+=1
yieldsMu = {}
ind = 0
for cat in templatelines[MpJetsLineTemplateInd].split()[2:]:
	yieldsMu['top_'+cat] = float(templatelines[MpJetsLineTemplateInd+10].split()[2+ind*4])
	yieldsMu['ewk_'+cat] = float(templatelines[MpJetsLineTemplateInd+9].split()[2+ind*4])
	ind+=1

yields = {}
yields['top_E_nB0_nW0']  = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'top' in cat and 'nB0' in cat and 'nW0' in cat])
yields['top_E_nB0_nW1p']  = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'top' in cat and 'nB0' in cat and 'nW1p' in cat])
yields['top_E_nB1']  = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'top' in cat and 'nB1' in cat])
yields['top_E_nB2p'] = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'top' in cat and ('nB2' in cat or 'nB3p' in cat)])
yields['ewk_E_nW0']  = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'ewk' in cat and 'nW0' in cat])
yields['ewk_E_nW1p'] = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'ewk' in cat and 'nW1p' in cat])

yields['top_M_nB0_nW0']  = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'top' in cat and 'nB0' in cat and 'nW0' in cat])
yields['top_M_nB0_nW1p']  = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'top' in cat and 'nB0' in cat and 'nW1p' in cat])
yields['top_M_nB1']  = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'top' in cat and 'nB1' in cat])
yields['top_M_nB2p'] = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'top' in cat and ('nB2' in cat or 'nB3p' in cat)])
yields['ewk_M_nW0']  = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'ewk' in cat and 'nW0' in cat])
yields['ewk_M_nW1p'] = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'ewk' in cat and 'nW1p' in cat])

dataOverBkg = {}
dataOverBkg['top_E_nB1'] = abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[2]))
dataOverBkg['top_M_nB1'] = abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[2]))
dataOverBkg['top_E_nB2p']= abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[6]))
dataOverBkg['top_M_nB2p']= abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[6]))

dataOverBkg['top_E_nB0_nW0'] = abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[2]))
dataOverBkg['top_M_nB0_nW0'] = abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[2]))
dataOverBkg['ewk_E_nW0'] = abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[2]))
dataOverBkg['ewk_M_nW0'] = abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[2]))
dataOverBkg['top_E_nB0_nW1p'] = abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[6]))
dataOverBkg['top_M_nB0_nW1p'] = abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[6]))
dataOverBkg['ewk_E_nW1p']= abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[6]))
dataOverBkg['ewk_M_nW1p']= abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[6]))

for key in yields.keys():
	#print key, yields[key]
	if '_M_' in key: continue
	if key == 'top_E_nB0_nW0':
		sumE = yields[key]+yields[key.replace('nW0','nW1p')]
		sumM = yields[key.replace('_E_','_M_')]+yields[key.replace('_E_','_M_').replace('nW0','nW1p')]
		numE = yields[key]*dataOverBkg[key]+yields[key.replace('nW0','nW1p')]*dataOverBkg[key.replace('nW0','nW1p')]
		numM = yields[key.replace('_E_','_M_')]*dataOverBkg[key.replace('_E_','_M_')]+yields[key.replace('_E_','_M_').replace('nW0','nW1p')]*dataOverBkg[key.replace('_E_','_M_').replace('nW0','nW1p')]
		print key.replace('E_',''),':',(numE+numM)/(sumE+sumM)
	elif key == 'top_E_nB0_nW1p': continue
	else: print key.replace('E_',''),':',(yields[key]*dataOverBkg[key]+yields[key.replace('_E_','_M_')]*dataOverBkg[key.replace('_E_','_M_')])/(yields[key]+yields[key.replace('_E_','_M_')])
print

ewk_isE=(yields['ewk_E_nW0']*dataOverBkg['ewk_E_nW0']+yields['ewk_E_nW1p']*dataOverBkg['ewk_E_nW1p'])/(yields['ewk_E_nW0']+yields['ewk_E_nW1p'])
ewk_isM=(yields['ewk_M_nW0']*dataOverBkg['ewk_M_nW0']+yields['ewk_M_nW1p']*dataOverBkg['ewk_M_nW1p'])/(yields['ewk_M_nW0']+yields['ewk_M_nW1p'])
ewk_all=((yields['ewk_E_nW0']+yields['ewk_E_nW1p'])*ewk_isE+(yields['ewk_M_nW0']+yields['ewk_M_nW1p'])*ewk_isM)/(yields['ewk_E_nW0']+yields['ewk_E_nW1p']+yields['ewk_M_nW0']+yields['ewk_M_nW1p'])
print 'ewk_isE :',ewk_isE
print 'ewk_isM :',ewk_isM 
print 'ewk_all :',ewk_all

top_isE=(yields['top_E_nB0_nW0']*dataOverBkg['top_E_nB0_nW0']+yields['top_E_nB0_nW1p']*dataOverBkg['top_E_nB0_nW1p']+yields['top_E_nB1']*dataOverBkg['top_E_nB1']+yields['top_E_nB2p']*dataOverBkg['top_E_nB2p'])/(yields['top_E_nB0_nW0']+yields['top_E_nB0_nW1p']+yields['top_E_nB1']+yields['top_E_nB2p'])
top_isM=(yields['top_M_nB0_nW0']*dataOverBkg['top_M_nB0_nW0']+yields['top_M_nB0_nW1p']*dataOverBkg['top_M_nB0_nW1p']+yields['top_M_nB1']*dataOverBkg['top_M_nB1']+yields['top_M_nB2p']*dataOverBkg['top_M_nB2p'])/(yields['top_M_nB0_nW0']+yields['top_M_nB0_nW1p']+yields['top_M_nB1']+yields['top_M_nB2p'])
top_all=((yields['top_E_nB0_nW0']+yields['top_E_nB0_nW1p']+yields['top_E_nB1']+yields['top_E_nB2p'])*top_isE+(yields['top_M_nB0_nW0']+yields['top_M_nB0_nW1p']+yields['top_M_nB1']+yields['top_M_nB2p'])*top_isM)/(yields['top_E_nB0_nW0']+yields['top_E_nB0_nW1p']+yields['top_E_nB1']+yields['top_E_nB2p']+yields['top_M_nB0_nW0']+yields['top_M_nB0_nW1p']+yields['top_M_nB1']+yields['top_M_nB2p'])
print 'top_isE :',top_isE
print 'top_isM :',top_isM 
print 'top_all :',top_all 


