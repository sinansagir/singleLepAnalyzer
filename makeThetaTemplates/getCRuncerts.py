#!/usr/bin/python

import os,sys,time,math

templateYields = 'templates_minMlb_JECv7JSF_tptp_2016_2_15/lep40_MET75_1jet300_2jet150_NJets3_NBJets0_3jet100_4jet0_5jet0_DR1_1Wjet0_1bjet0_HT0_ST0_minMlb0/yields_minMlb_2p263fb_.txt' 
ttbarYields = '../makeCRs/ttbar_JECv7JSF_2016_2_15/yields_minMlb_2p263fb_.txt'
wjetsYields = '../makeCRs/wjets_JECv7JSF_2016_2_15/yields_minMlb_2p263fb_.txt'

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

yields = {}
yields['top_E_0p_0'] = float(templatelines[EpJetsLineTemplateInd+10].strip().split()[2])+float(templatelines[EpJetsLineTemplateInd+10].strip().split()[2+16])
yields['top_M_0p_0'] = float(templatelines[MpJetsLineTemplateInd+10].strip().split()[2])+float(templatelines[MpJetsLineTemplateInd+10].strip().split()[2+16])
yields['top_E_0p_1'] = float(templatelines[EpJetsLineTemplateInd+10].strip().split()[6])+float(templatelines[EpJetsLineTemplateInd+10].strip().split()[6+16])
yields['top_M_0p_1'] = float(templatelines[MpJetsLineTemplateInd+10].strip().split()[6])+float(templatelines[MpJetsLineTemplateInd+10].strip().split()[6+16])
yields['top_E_0p_2p']= float(templatelines[EpJetsLineTemplateInd+10].strip().split()[10])+float(templatelines[EpJetsLineTemplateInd+10].strip().split()[10+16])+float(templatelines[EpJetsLineTemplateInd+10].strip().split()[14])+float(templatelines[EpJetsLineTemplateInd+10].strip().split()[14+16])
yields['top_M_0p_2p']= float(templatelines[MpJetsLineTemplateInd+10].strip().split()[10])+float(templatelines[MpJetsLineTemplateInd+10].strip().split()[10+16])+float(templatelines[MpJetsLineTemplateInd+10].strip().split()[14])+float(templatelines[MpJetsLineTemplateInd+10].strip().split()[14+16])

yields['ewk_E_0_0p'] = float(templatelines[EpJetsLineTemplateInd+9].strip().split()[2])+float(templatelines[EpJetsLineTemplateInd+9].strip().split()[6])+float(templatelines[EpJetsLineTemplateInd+9].strip().split()[10])+float(templatelines[EpJetsLineTemplateInd+9].strip().split()[14])
yields['ewk_M_0_0p'] = float(templatelines[MpJetsLineTemplateInd+9].strip().split()[2])+float(templatelines[MpJetsLineTemplateInd+9].strip().split()[6])+float(templatelines[MpJetsLineTemplateInd+9].strip().split()[10])+float(templatelines[MpJetsLineTemplateInd+9].strip().split()[14])
yields['ewk_E_1p_0p']= float(templatelines[EpJetsLineTemplateInd+9].strip().split()[2+16])+float(templatelines[EpJetsLineTemplateInd+9].strip().split()[6+16])+float(templatelines[EpJetsLineTemplateInd+9].strip().split()[10+16])+float(templatelines[EpJetsLineTemplateInd+9].strip().split()[14+16])
yields['ewk_M_1p_0p']= float(templatelines[MpJetsLineTemplateInd+9].strip().split()[2+16])+float(templatelines[MpJetsLineTemplateInd+9].strip().split()[6+16])+float(templatelines[MpJetsLineTemplateInd+9].strip().split()[10+16])+float(templatelines[MpJetsLineTemplateInd+9].strip().split()[14+16])

dataOverBkg = {}
dataOverBkg['top_E_0p_0'] = abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[2]))
dataOverBkg['top_M_0p_0'] = abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[2]))
dataOverBkg['top_E_0p_1'] = abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[6]))
dataOverBkg['top_M_0p_1'] = abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[6]))
dataOverBkg['top_E_0p_2p']= abs(1-float(ttbarlines[EpJetsLineTtbarInd+14].strip().split()[10]))
dataOverBkg['top_M_0p_2p']= abs(1-float(ttbarlines[MpJetsLineTtbarInd+14].strip().split()[10]))

dataOverBkg['ewk_E_0_0p'] = abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[2]))
dataOverBkg['ewk_M_0_0p'] = abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[2]))
dataOverBkg['ewk_E_1p_0p']= abs(1-float(wjetslines[EpJetsLineWjetsInd+14].strip().split()[6]))
dataOverBkg['ewk_M_1p_0p']= abs(1-float(wjetslines[MpJetsLineWjetsInd+14].strip().split()[6]))

for key in yields.keys():
	if '_M_' in key: continue
	print key.replace('E_',''),':',(yields[key]*dataOverBkg[key]+yields[key.replace('_E_','_M_')]*dataOverBkg[key.replace('_E_','_M_')])/(yields[key]+yields[key.replace('_E_','_M_')])
print

ewk_isE=(yields['ewk_E_0_0p']*dataOverBkg['ewk_E_0_0p']+yields['ewk_E_1p_0p']*dataOverBkg['ewk_E_1p_0p'])/(yields['ewk_E_0_0p']+yields['ewk_E_1p_0p'])
ewk_isM=(yields['ewk_M_0_0p']*dataOverBkg['ewk_M_0_0p']+yields['ewk_M_1p_0p']*dataOverBkg['ewk_M_1p_0p'])/(yields['ewk_M_0_0p']+yields['ewk_M_1p_0p'])
ewk_all=((yields['ewk_E_0_0p']+yields['ewk_E_1p_0p'])*ewk_isE+(yields['ewk_M_0_0p']+yields['ewk_M_1p_0p'])*ewk_isM)/(yields['ewk_E_0_0p']+yields['ewk_E_1p_0p']+yields['ewk_M_0_0p']+yields['ewk_M_1p_0p'])
print 'ewk_isE :',ewk_isE
print 'ewk_isM :',ewk_isM 
print 'ewk_all :',ewk_all

top_isE=(yields['top_E_0p_0']*dataOverBkg['top_E_0p_0']+yields['top_E_0p_1']*dataOverBkg['top_E_0p_1']+yields['top_E_0p_2p']*dataOverBkg['top_E_0p_2p'])/(yields['top_E_0p_0']+yields['top_E_0p_1']+yields['top_E_0p_2p'])
top_isM=(yields['top_M_0p_0']*dataOverBkg['top_M_0p_0']+yields['top_M_0p_1']*dataOverBkg['top_M_0p_1']+yields['top_M_0p_2p']*dataOverBkg['top_M_0p_2p'])/(yields['top_M_0p_0']+yields['top_M_0p_1']+yields['top_M_0p_2p'])
top_all=((yields['top_E_0p_0']+yields['top_E_0p_1']+yields['top_E_0p_2p'])*top_isE+(yields['top_M_0p_0']+yields['top_M_0p_1']+yields['top_M_0p_2p'])*top_isM)/(yields['top_E_0p_0']+yields['top_E_0p_1']+yields['top_E_0p_2p']+yields['top_M_0p_0']+yields['top_M_0p_1']+yields['top_M_0p_2p'])
print 'top_isE :',top_isE
print 'top_isM :',top_isM 
print 'top_all :',top_all 


