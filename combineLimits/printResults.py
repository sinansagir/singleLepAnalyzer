#!/usr/bin/python

import os,copy,math,glob

inputDir="limits_onlyHOTcats_DeepCSV_2020_1_22/"

limDirsNoJet = [tag for tag in sorted(os.listdir(inputDir)) if '_nJ6' in tag]
print len(limDirsNoJet)*5

for inputPathh in sorted(os.listdir(inputDir)):
	if 'isSR' not in inputPathh: continue
	if '_nJ6' not in inputPathh: continue
	for nJet in ['_nJ5','_nJ6','_nJ7','_nJ8','_nJ9','_nJ10p']:
		inputPath = inputPathh.replace('_nJ6',nJet)
		sigFile = inputDir+inputPath+'/690/Significance.txt'
		sigData = open(sigFile,'r').read()
		siglines = sigData.split('\n')
		limFile = inputDir+inputPath+'/690/AsymptoticLimits.txt'
		limData = open(limFile,'r').read()
		limlines = limData.split('\n')
		theSig = ''
		theLim = ''
		for line in siglines:
			if line.startswith('Significance:'): theSig = line.split()[-1]
		for line in limlines:
			if line.startswith('Expected 50.0%:'): theLim = line.split()[-1]
		print inputPath,theSig,theLim