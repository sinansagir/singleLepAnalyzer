#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools,fnmatch
from ROOT import gROOT,TFile,TH1F

gROOT.SetBatch(1)
start_time = time.time()

region='TTCR' #PS,SR,TTCR,WJCR
isCategorized=1
cutString=''#'lep30_MET100_NJets4_DR1_1jet250_2jet50'
if region=='SR': pfix='templates_'
if region=='TTCR': pfix='ttbar_'
if region=='WJCR': pfix='wjets_'
if not isCategorized: pfix='kinematics_'+region+'_'
pfix+='2017_2_12_JHttbar'
outDir = os.getcwd()+'/'+pfix+'/'+cutString

whichSignal = 'X53X53' #HTB, TT, BB, or X53X53
massList = range(700,1600+1,100)
sigList = [whichSignal+'M'+str(mass) for mass in massList]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in massList for chiral in ['left','right']]

isEMlist =['E','M']
if region=='SR': nttaglist=['0','1p']
else: nttaglist = ['0p']
if region=='TTCR': nWtaglist = ['0p']
else: nWtaglist=['0','1p']
if region=='WJCR': nbtaglist = ['0']
else: nbtaglist=['1','2p']
if not isCategorized: 	
	nttaglist = ['0p']
	nWtaglist = ['0p']
	nbtaglist = ['0','1p']#,'2p']
	if region=='CR': nbtaglist = ['0','0p','1p']
njetslist=['4p']
if region=='PS': njetslist=['3p']
catList = ['is'+item[0]+'_nT'+item[1]+'_nW'+item[2]+'_nB'+item[3]+'_nJ'+item[4] for item in list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))]
tagList = ['nT'+item[0]+'_nW'+item[1]+'_nB'+item[2]+'_nJ'+item[3] for item in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

iPlotList = []
for file in findfiles(outDir+'/'+catList[0][2:]+'/', '*.p'):
    if 'bkghists' not in file: continue
    if not os.path.exists(file.replace('bkghists','datahists')): continue
    if not os.path.exists(file.replace('bkghists','sighists')): continue
    iPlotList.append(file.split('/')[-1].replace('bkghists_','')[:-2])

print "WORKING DIR:",outDir
print iPlotList
for iPlot in iPlotList:
	if iPlot!='minMlb': continue
	print "LOADING DISTRIBUTION: "+iPlot
	for cat in catList:
		print "         ",cat[2:]
		bkghists={}
		bkghists.update(pickle.load(open(outDir+'/'+cat[2:]+'/bkghists_'+iPlot+'.p','rb')))
		bkghists2=pickle.load(open(outDir.replace('2017_2_12_JHttbar','JHttbar_2017_2_25')+'/'+cat[2:]+'/bkghists_'+iPlot+'.p','rb'))
		for key in bkghists2.keys(): 
			#if 'WJetsMGPt100' not in key: continue
			if not key.endswith('TTJetsPH'): continue
			bkghists[key.replace('36p814fb','35p867fb')]=bkghists2[key].Clone(key.replace('36p814fb','35p867fb'))
			bkghists[key.replace('36p814fb','35p867fb')].Scale(35867./36814.)
		pickle.dump(bkghists,open(outDir+'/'+cat[2:]+'/bkghists_'+iPlot+'.p','wb'))

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


