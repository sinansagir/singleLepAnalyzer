#!/usr/bin/python

import os,sys,time,math,fnmatch
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from array import array
from utils import *
from ROOT import *
start_time = time.time()

year=sys.argv[1]
if year=='R16':
	from weights16 import *
elif year=='R17':
	from weights17 import *
elif year=='R18':
	from weights18 import *

iPlot=sys.argv[2]
saveKey = '_new'#'_2b300GeV3b150GeV4b50GeVbins'
lumiStr = str(targetlumi/1000).replace('.','p')+'fb' # 1/fb
templateDir = os.getcwd()+'/templates_'+year+'_'+sys.argv[3]
combinefile = 'templates_'+iPlot+'_'+lumiStr+'.root'
njetslist = {
'_nJ6':('_nJ6','_nJ7','_nJ8','_nJ9','_nJ10p'),
'_nJ7':('_nJ7','_nJ8','_nJ9','_nJ10p'),
'_nJ8':('_nJ8','_nJ9','_nJ10p'),
}

rebinCombine = True #else rebins theta templates
sigName = 'tttt' #MAKE SURE THIS WORKS FOR YOUR ANALYSIS PROPERLY!!!!!!!!!!!
massList = [690]
sigProcList = [sigName+'M'+str(mass) for mass in massList]
if sigName=='tttt': sigProcList = [sigName]
		
if rebinCombine:
	dataName = 'data_obs'
	upTag = 'Up'
	downTag = 'Down'
else: #theta
	dataName = 'DATA'
	upTag = '__plus'
	downTag = '__minus'

def gettime():
	return str(round((time.time() - start_time)/60,2))+'mins'
	
def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

#Setup the selection of the files to be rebinned: 
rfiles = []         
for file in findfiles(templateDir, '*.root'):
	if 'rebinned' in file or combinefile in file or '_'+iPlot+'_' not in file.split('/')[-1]: continue
	if not any([signal in file for signal in sigProcList]): continue
	if not file.endswith('fb.root'): continue
	rfiles.append(file)
if rebinCombine: rfiles = [templateDir+'/'+combinefile]

tfile = TFile(rfiles[0])
datahists = [k.GetName() for k in tfile.GetListOfKeys() if '__'+dataName in k.GetName()]
channels = [hist[hist.find('fb_')+3:hist.find('__')] for hist in datahists if 'isL_' not in hist]
allhists = {chn:[hist.GetName() for hist in tfile.GetListOfKeys() if '_'+chn+'_' in hist.GetName()] for chn in channels}
tfile.Close()

iRfile=0
for rfile in rfiles: 
	print "REBINNING FILE:",rfile
	tfiles = {}
	outputRfiles = {}
	tfiles[iRfile] = TFile(rfile)	
	outputRfiles[iRfile] = TFile(rfile.replace('.root',saveKey+'.root'),'RECREATE')

	print "PROGRESS:"
	for chn in channels:
		print "         ",chn,gettime()
		rebinnedHists = {}
		#Rebinning histograms
		for hist in allhists[chn]:
			rebinnedHists[hist]=tfiles[iRfile].Get(hist)
			rebinnedHists[hist].SetDirectory(0)
			rebinnedHists[hist].Write()				
			#Add new inclusive categories
			nJet_ = '_'+chn.split('_')[-1]
			if nJet_ in njetslist.keys():
				newHname = rebinnedHists[hist].GetName().replace(nJet_,nJet_+'p')
				rebinnedHists[newHname] = rebinnedHists[hist].Clone(newHname)
				for ijet in njetslist[nJet_]:
					if nJet_==ijet:continue
					try: rebinnedHists[newHname].Add(tfiles[iRfile].Get(hist.replace(nJet_,ijet)).Clone())
					except:
						print 'MISSING PROC:',hist.replace(nJet_,ijet)
				rebinnedHists[newHname].Write()
	tfiles[iRfile].Close()
	outputRfiles[iRfile].Close()
	iRfile+=1

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


