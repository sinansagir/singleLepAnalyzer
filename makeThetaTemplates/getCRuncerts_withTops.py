#!/usr/bin/python

import os,sys,time,math

templateYields = 'templates_minMlb_69mb/SelectionFile/yields_minMlb_12p892fb.txt' 
ttbarYields = '../makeCRs/ttbar_tptp_69mb/yields_minMlb_12p892fb.txt'
wjetsYields = '../makeCRs/wjets_tptp_69mb/yields_minMlb_12p892fb.txt'

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
yields['top_E_nB0_nWT00']  = yieldsEl['top_isE_nT0_nW0_nB0']
yields['top_E_nB0_nWT10']  = yieldsEl['top_isE_nT0_nW1p_nB0']
yields['top_E_nB0_nWT01']  = yieldsEl['top_isE_nT1p_nW0p_nB0']
yields['top_E_nB1_nWT00']  = yieldsEl['top_isE_nT0_nW0_nB1']
yields['top_E_nB1_nWT10']  = yieldsEl['top_isE_nT0_nW1p_nB1']
yields['top_E_nB1_nWT01']  = yieldsEl['top_isE_nT1p_nW0p_nB1']
yields['top_E_nB2p_nWT00'] = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'top' in cat and ('nB2' in cat or 'nB2p' in cat or 'nB3p' in cat) and 'nW0_' in cat])
yields['top_E_nB2p_nWT10'] = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'top' in cat and ('nB2' in cat or 'nB2p' in cat or 'nB3p' in cat) and 'nW1p' in cat])
yields['top_E_nB2p_nWT01'] = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'top' in cat and ('nB2' in cat or 'nB2p' in cat or 'nB3p' in cat) and 'nW0p' in cat])
yields['ewk_E_nB0p_nWT00'] = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'ewk' in cat and 'nW0_' in cat])
yields['ewk_E_nB0p_nWT10'] = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'ewk' in cat and 'nW1p' in cat])
yields['ewk_E_nB0p_nWT01'] = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'ewk' in cat and 'nW0p' in cat])

yields['top_M_nB0_nWT00']  = yieldsMu['top_isM_nT0_nW0_nB0']
yields['top_M_nB0_nWT10']  = yieldsMu['top_isM_nT0_nW1p_nB0']
yields['top_M_nB0_nWT01']  = yieldsMu['top_isM_nT1p_nW0p_nB0']
yields['top_M_nB1_nWT00']  = yieldsMu['top_isM_nT0_nW0_nB1']
yields['top_M_nB1_nWT10']  = yieldsMu['top_isM_nT0_nW1p_nB1']
yields['top_M_nB1_nWT01']  = yieldsMu['top_isM_nT1p_nW0p_nB1']
yields['top_M_nB2p_nWT00'] = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'top' in cat and ('nB2' in cat or 'nB2p' in cat or 'nB3p' in cat) and 'nW0_' in cat])
yields['top_M_nB2p_nWT10'] = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'top' in cat and ('nB2' in cat or 'nB2p' in cat or 'nB3p' in cat) and 'nW1p' in cat])
yields['top_M_nB2p_nWT01'] = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'top' in cat and ('nB2' in cat or 'nB2p' in cat or 'nB3p' in cat) and 'nW0p' in cat])
yields['ewk_M_nB0p_nWT00'] = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'ewk' in cat and 'nW0_' in cat])
yields['ewk_M_nB0p_nWT10'] = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'ewk' in cat and 'nW1p' in cat])
yields['ewk_M_nB0p_nWT01'] = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'ewk' in cat and 'nW0p' in cat])

dataOverBkg = {} #find the correct numbers....
dataOverBkg['top_E_nB1_nWT00'] = abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[2]))
dataOverBkg['top_E_nB1_nWT10'] = abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[10]))
dataOverBkg['top_E_nB1_nWT01'] = abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[18]))
dataOverBkg['top_M_nB1_nWT00'] = abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[2]))
dataOverBkg['top_M_nB1_nWT10'] = abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[10]))
dataOverBkg['top_M_nB1_nWT01'] = abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[18]))
dataOverBkg['top_E_nB2p_nWT00']= abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[6]))
dataOverBkg['top_E_nB2p_nWT10']= abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[14]))
dataOverBkg['top_E_nB2p_nWT01']= abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[22]))
dataOverBkg['top_M_nB2p_nWT00']= abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[6]))
dataOverBkg['top_M_nB2p_nWT10']= abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[14]))
dataOverBkg['top_M_nB2p_nWT01']= abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[22]))

dataOverBkg['top_E_nB0_nWT00'] = abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[2]))
dataOverBkg['top_E_nB0_nWT10'] = abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[6]))
dataOverBkg['top_E_nB0_nWT01'] = abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[10]))
dataOverBkg['top_M_nB0_nWT00'] = abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[2]))
dataOverBkg['top_M_nB0_nWT10'] = abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[6]))
dataOverBkg['top_M_nB0_nWT01'] = abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[10]))
dataOverBkg['ewk_E_nB0p_nWT00'] = abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[2]))
dataOverBkg['ewk_E_nB0p_nWT10'] = abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[6]))
dataOverBkg['ewk_E_nB0p_nWT01'] = abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[10]))
dataOverBkg['ewk_M_nB0p_nWT00'] = abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[2]))
dataOverBkg['ewk_M_nB0p_nWT10'] = abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[6]))
dataOverBkg['ewk_M_nB0p_nWT01'] = abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[10]))

for key in yields.keys():
	#print key, yields[key]
	if '_M_' in key: continue
	print key.replace('E_',''),': yield E =',yields[key],', yield M =',yields[key.replace('_E_','_M_')],', unc =',(yields[key]*dataOverBkg[key]+yields[key.replace('_E_','_M_')]*dataOverBkg[key.replace('_E_','_M_')])/(yields[key]+yields[key.replace('_E_','_M_')])
print

sumE = 0;
sumM = 0;
numE = 0;
numM = 0;
for key in yields.keys():
	if 'ewk' not in key: continue
	if '_E_' in key:
		numE += yields[key]*dataOverBkg[key]
		sumE += yields[key]
	if '_M_' in key:
		numM += yields[key]*dataOverBkg[key]
		sumM += yields[key]
ewk_isE = numE / sumE
ewk_isM = numM / sumM
ewk_all = (numE+numM)/(sumE+sumM)
print 'ewk_isE :',ewk_isE
print 'ewk_isM :',ewk_isM 
print 'ewk_all :',ewk_all

sumE = 0
sumM = 0
numE = 0
numM = 0
for key in yields.keys():
	if 'top' not in key: continue
	if '_E_' in key:
		numE += yields[key]*dataOverBkg[key]
		sumE += yields[key]
	if '_M_' in key:
		numM += yields[key]*dataOverBkg[key]
		sumM += yields[key]
		
top_isE = numE / sumE
top_isM = numM / sumM
top_all = (numE+numM)/(sumE+sumM)
print 'top_isE :',top_isE
print 'top_isM :',top_isM 
print 'top_all :',top_all 


