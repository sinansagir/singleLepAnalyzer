#!/usr/bin/python

import os, sys, fnmatch
import math

inDir = '/user_data/ssagir/x53x53_limits_2016/templates_ST_2016_10_29_discovery/all'
folders = [x for x in os.walk(inDir).next()[1]]

currentDir = os.getcwd()

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

grandTot = 0
for folder in folders:
	files = [x for x in os.listdir(inDir+'/'+folder) if '.log' in x]
	for file in files: 
		if not os.path.exists(inDir+'/'+folder+'/'+file.replace('.log','.json')): 
			grandTot+=1
			print folder, file
			print "*" * 40
			print ">cd " + inDir+'/'+folder
			os.chdir(inDir+'/'+folder)
			print ">condor_submit " + file.replace('.log','.job')
			os.system('rm ' + file)
			os.system('rm ' + file.replace('.log','.err'))
			os.system('rm ' + file.replace('.log','.out'))
			os.system('condor_submit ' + file.replace('.log','.job'))
			print "*" * 40
print grandTot
