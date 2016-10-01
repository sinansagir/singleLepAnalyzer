#!/usr/bin/python

import os,sys,time,math

discrim = 'ST'
templateYields = 'templates_'+discrim+'_2016_9_14/lep30_MET100_NJets4_DR1_1jet250_2jet50/yields_'+discrim+'_12p892fb.txt' 
ttbarYields = '../makeCRs/ttbar_'+discrim+'_2016_9_14/yields_'+discrim+'_12p892fb.txt'
wjetsYields = '../makeCRs/wjets_'+discrim+'_2016_9_14/yields_'+discrim+'_12p892fb.txt'

# templateYields = 'templates_ST_2016_9_6/lep30_MET100_NJets4_DR1_1jet250_2jet50/yields_minMlb_12p892fb.txt' 
# ttbarYields = '../makeCRs/ttbar_ST_2016_9_7/yields_minMlb_12p892fb.txt'
# wjetsYields = '../makeCRs/wjets_ST_2016_9_7/yields_minMlb_12p892fb.txt'

ftemplate = open(templateYields, 'rU')
templatelines = ftemplate.readlines()
ftemplate.close()
fttbar = open(ttbarYields, 'rU')
ttbarlines = fttbar.readlines()
fttbar.close()
fwjets = open(wjetsYields, 'rU')
wjetslines = fwjets.readlines()
fwjets.close()

EpJetsLineTemplateInd = templatelines.index([line for line in templatelines if line.startswith('YIELDS ELECTRON+JETS')][0])+1
MpJetsLineTemplateInd = templatelines.index([line for line in templatelines if line.startswith('YIELDS MUON+JETS')][0])+1
EpJetsLineTtbarInd = ttbarlines.index([line for line in ttbarlines if line.startswith('YIELDS ELECTRON+JETS')][0])+1
MpJetsLineTtbarInd = ttbarlines.index([line for line in ttbarlines if line.startswith('YIELDS MUON+JETS')][0])+1
EpJetsLineWjetsInd = wjetslines.index([line for line in wjetslines if line.startswith('YIELDS ELECTRON+JETS')][0])+1
MpJetsLineWjetsInd = wjetslines.index([line for line in wjetslines if line.startswith('YIELDS MUON+JETS')][0])+1

dummyIndexes = []
for line in templatelines[EpJetsLineTemplateInd:MpJetsLineTemplateInd]:
	if line.startswith('#topTag'): dummyIndexes.append(templatelines.index([item for item in templatelines if item==line][0]))
nLineShiftForTtag = 0 # if top tag categories are printed in a separate block
if len(dummyIndexes)==2: nLineShiftForTtag = dummyIndexes[1]-dummyIndexes[0]

yieldsEl = {}
ind = 0
for cat in templatelines[EpJetsLineTemplateInd].split()[1:]:
	yieldsEl['top_'+cat] = float(templatelines[EpJetsLineTemplateInd+10].split()[2+ind*4])
	yieldsEl['ewk_'+cat] = float(templatelines[EpJetsLineTemplateInd+9].split()[2+ind*4])
	ind+=1
ind = 0
if nLineShiftForTtag!=0:
	for cat in templatelines[EpJetsLineTemplateInd+nLineShiftForTtag].split()[1:]:
		yieldsEl['top_'+cat] = float(templatelines[EpJetsLineTemplateInd+10+nLineShiftForTtag].split()[2+ind*4])
		yieldsEl['ewk_'+cat] = float(templatelines[EpJetsLineTemplateInd+9+nLineShiftForTtag].split()[2+ind*4])
		ind+=1
yieldsMu = {}
ind = 0
for cat in templatelines[MpJetsLineTemplateInd].split()[1:]:
	yieldsMu['top_'+cat] = float(templatelines[MpJetsLineTemplateInd+10].split()[2+ind*4])
	yieldsMu['ewk_'+cat] = float(templatelines[MpJetsLineTemplateInd+9].split()[2+ind*4])
	ind+=1
ind = 0
if nLineShiftForTtag!=0:
	for cat in templatelines[MpJetsLineTemplateInd+nLineShiftForTtag].split()[1:]:
		yieldsMu['top_'+cat] = float(templatelines[MpJetsLineTemplateInd+10+nLineShiftForTtag].split()[2+ind*4])
		yieldsMu['ewk_'+cat] = float(templatelines[MpJetsLineTemplateInd+9+nLineShiftForTtag].split()[2+ind*4])
		ind+=1
	
yields = {}
yields['top_E_nB0']  = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'top' in cat and cat.endswith('nB0')])
yields['top_E_nB1']  = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'top' in cat and cat.endswith('nB1')])
yields['top_E_nB2p'] = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'top' in cat and (cat.endswith('nB2') or cat.endswith('nB2p') or cat.endswith('nB3p'))])
yields['ewk_E_nW0']  = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'ewk' in cat and 'nW0_' in cat])
yields['ewk_E_nW1p'] = sum([yieldsEl[cat] for cat in yieldsEl.keys() if 'ewk' in cat and 'nW1p_' in cat])

yields['top_M_nB0']  = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'top' in cat and cat.endswith('nB0')])
yields['top_M_nB1']  = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'top' in cat and cat.endswith('nB1')])
yields['top_M_nB2p'] = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'top' in cat and (cat.endswith('nB2') or cat.endswith('nB2p') or cat.endswith('nB3p'))])
yields['ewk_M_nW0']  = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'ewk' in cat and 'nW0_' in cat])
yields['ewk_M_nW1p'] = sum([yieldsMu[cat] for cat in yieldsMu.keys() if 'ewk' in cat and 'nW1p_' in cat])

dataOverBkg = {}
nB0ind=0#enter 0 if doesn't exist in yield files and 1 if it does
dataOverBkg['top_E_nB0'] = abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[2]))
dataOverBkg['top_M_nB0'] = abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[2]))
dataOverBkg['top_E_nB1'] = abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[2+4*nB0ind]))
dataOverBkg['top_M_nB1'] = abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[2+4*nB0ind]))
dataOverBkg['top_E_nB2p']= abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[2+4*(nB0ind+1)]))
dataOverBkg['top_M_nB2p']= abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[2+4*(nB0ind+1)]))

dataOverBkg['ewk_E_nW0'] = abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[2]))
dataOverBkg['ewk_M_nW0'] = abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[2]))
dataOverBkg['ewk_E_nW1p']= abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[6]))
dataOverBkg['ewk_M_nW1p']= abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[6]))

for key in yields.keys():
	if '_M_' in key: continue
	if not nB0ind and key.endswith('nB0'): continue
	print key.replace('E_',''),':',(yields[key]*dataOverBkg[key]+yields[key.replace('_E_','_M_')]*dataOverBkg[key.replace('_E_','_M_')])/(yields[key]+yields[key.replace('_E_','_M_')])
print

ewk_isE=(yields['ewk_E_nW0']*dataOverBkg['ewk_E_nW0']+yields['ewk_E_nW1p']*dataOverBkg['ewk_E_nW1p'])/(yields['ewk_E_nW0']+yields['ewk_E_nW1p'])
ewk_isM=(yields['ewk_M_nW0']*dataOverBkg['ewk_M_nW0']+yields['ewk_M_nW1p']*dataOverBkg['ewk_M_nW1p'])/(yields['ewk_M_nW0']+yields['ewk_M_nW1p'])
ewk_all=((yields['ewk_E_nW0']+yields['ewk_E_nW1p'])*ewk_isE+(yields['ewk_M_nW0']+yields['ewk_M_nW1p'])*ewk_isM)/(yields['ewk_E_nW0']+yields['ewk_E_nW1p']+yields['ewk_M_nW0']+yields['ewk_M_nW1p'])
print 'ewk_isE :',ewk_isE
print 'ewk_isM :',ewk_isM 
print 'ewk_all :',ewk_all

top_isE=(yields['top_E_nB0']*dataOverBkg['top_E_nB0']+yields['top_E_nB1']*dataOverBkg['top_E_nB1']+yields['top_E_nB2p']*dataOverBkg['top_E_nB2p'])/(yields['top_E_nB0']+yields['top_E_nB1']+yields['top_E_nB2p'])
top_isM=(yields['top_M_nB0']*dataOverBkg['top_M_nB0']+yields['top_M_nB1']*dataOverBkg['top_M_nB1']+yields['top_M_nB2p']*dataOverBkg['top_M_nB2p'])/(yields['top_M_nB0']+yields['top_M_nB1']+yields['top_M_nB2p'])
top_all=((yields['top_E_nB0']+yields['top_E_nB1']+yields['top_E_nB2p'])*top_isE+(yields['top_M_nB0']+yields['top_M_nB1']+yields['top_M_nB2p'])*top_isM)/(yields['top_E_nB0']+yields['top_E_nB1']+yields['top_E_nB2p']+yields['top_M_nB0']+yields['top_M_nB1']+yields['top_M_nB2p'])
print 'top_isE :',top_isE
print 'top_isM :',top_isM 
print 'top_all :',top_all

