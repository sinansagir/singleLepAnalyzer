#!/usr/bin/python

import os,sys,time,math,datetime,pickle,itertools,getopt
from ROOT import TH1D,gROOT,TFile,TTree
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from numpy import linspace
from weights import *
from analyze import *
from samples import *
from utils import *

gROOT.SetBatch(1)
start_time = time.time()

lumiStr = str(targetlumi/1000).replace('.','p') # 1/fb
step1Dir = '/user_data/ssagir/LJMet_1lep_080816_HTB_step2/nominal'
#massPt = 500
if len(sys.argv)>1: massPt=int(sys.argv[1])
else: massPt = 500
#step1Dir = '/user_data/zmao/chargedHiggs/normal/'+str(massPt)+'/'
#step1Dir = '/user_data/zmao/chargedHiggs/atLeast3B/normal/'+str(massPt)+'/'

"""
Note: 
--Each process in step1 (or step2) directories should have the root files hadded! 
--The code will look for <step1Dir>/<process>_hadd.root for nominal trees.
The uncertainty shape shifted files will be taken from <step1Dir>/../<shape>/<process>_hadd.root,
where <shape> is for example "JECUp". hadder.py can be used to prepare input files this way! 
--Each process given in the lists below must have a definition in "samples.py"
--Check the set of cuts in "analyze.py"
"""

bkgList = [
	'DY',
	'WJetsMG',
	'WW','WZ','ZZ',
	'TTJetsPH0to1000inc',
	'TTJetsPH1000toINFinc',
	'TTJetsPH1000mtt',
	'TTWl','TTWq',
	'TTZl','TTZq',
	'Tt','Tbt','Ts',
	'TtW','TbtW',
	#'QCDht100','QCDht200',
	'QCDht300','QCDht500','QCDht700','QCDht1000','QCDht1500','QCDht2000',
	]

dataList = ['DataEPRC','DataEPRB','DataEPRD','DataMPRC','DataMPRB','DataMPRD']

whichSignal = 'HTB' #TT, BB, HTB, or X53X53
signalMassRange = [200,500]#[massPt,massPt]
sigList = [whichSignal+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100)]
if whichSignal=='X53X53': sigList = [whichSignal+'M'+str(mass)+chiral for mass in range(signalMassRange[0],signalMassRange[1]+100,100) for chiral in ['left','right']]
if whichSignal=='HTB': sigList = [whichSignal+'M'+str(mass) for mass in [180]+range(signalMassRange[0],signalMassRange[1]+50,50)]
#if whichSignal=='HTB': sigList = [whichSignal+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+50,50)]
if whichSignal=='TT': decays = ['BWBW','THTH','TZTZ','TZBW','THBW','TZTH'] #T' decays
if whichSignal=='BB': decays = ['TWTW','BHBH','BZBZ','BZTW','BHTW','BZBH'] #B' decays
if whichSignal=='X53X53': decays = [''] #decays to tWtW 100% of the time
if whichSignal=='HTB': decays = ['']

region = 'SR' #no need to change
isotrig = 1
doJetRwt = 0
doAllSys= False
doQ2sys = False
q2List  = [#energy scale sample to be processed
	       'TTJetsPHQ2U','TTJetsPHQ2D',
	       #'TtWQ2U','TbtWQ2U',
	       #'TtWQ2D','TbtWQ2D',
	       ]

lepPtCut  = '50'
metCut    = '30'
njetsCut  = '4p'
nbjetsCut = '2'
drCut     = '0'
jet1PtCut = '50'
jet2PtCut = '40'
jet3PtCut = '0'

isEMlist =['E','M']
nttaglist=['0p']
nWtaglist=['0p']
nbtaglist=['2','3','3p','4p']
njetslist=['4','5','6p']
# nbtaglist=['2','3p']
# njetslist=['4p']

try: 
	opts, args = getopt.getopt(sys.argv[2:], "", ["lepPtCut=",
	                                              "jet1PtCut=",
	                                              "jet2PtCut=",
	                                              "jet3PtCut=",
	                                              "metCut=",
	                                              "njetsCut=",
	                                              "nbjetsCut=",
	                                              "drCut=",
	                                              "isEM=",
	                                              "nttag=",
	                                              "nWtag=",
	                                              "nbtag=",
	                                              ])
	print opts,args
except getopt.GetoptError as err:
	print str(err)
	sys.exit(1)

for o, a in opts:
	print o, a
	if o == '--lepPtCut': lepPtCut = a
	if o == '--jet1PtCut': jet1PtCut = a
	if o == '--jet2PtCut': jet2PtCut = a
	if o == '--jet3PtCut': jet3PtCut = a
	if o == '--metCut': metCut = a
	if o == '--njetsCut': njetsCut = a
	if o == '--nbjetsCut': nbjetsCut = a
	if o == '--drCut': drCut = a
	if o == '--isEM': isEMlist = [str(a)]
	if o == '--nttag': nttaglist = [str(a)]
	if o == '--nWtag': nWtaglist = [str(a)]
	if o == '--nbtag': nbtaglist = [str(a)]

cutList = {'lepPtCut':lepPtCut,
           'jet1PtCut':jet1PtCut,
           'jet2PtCut':jet2PtCut,
           'jet3PtCut':jet3PtCut,
           'metCut':metCut,
           'njetsCut':njetsCut,
           'nbjetsCut':nbjetsCut,
           'drCut':drCut,
           }

cutString  = 'lep'+cutList['lepPtCut']+'_MET'+cutList['metCut']
cutString += '_NJets'+cutList['njetsCut']+'_NBJets'+cutList['nbjetsCut']
#cutString += '_DR'+str(cutList['drCut'])
cutString += '_1jet'+cutList['jet1PtCut']+'_2jet'+cutList['jet2PtCut']
#cutString += '_3jet'+str(int(cutList['jet3PtCut']))
# cutString += '_4jet'+str(int(cutList['jet4PtCut']))+'_5jet'+str(int(cutList['jet5PtCut']))
# cutString += '_1Wjet'+str(cutList['Wjet1PtCut'])+'_1bjet'+str(cutList['bjet1PtCut'])
# cutString += '_HT'+str(cutList['htCut'])+'_ST'+str(cutList['stCut'])+'_minMlb'+str(cutList['minMlbCut'])

cTime=datetime.datetime.now()
datestr='%i_%i_%i'%(cTime.year,cTime.month,cTime.day)
timestr='%i_%i_%i'%(cTime.hour,cTime.minute,cTime.second)
pfix='templates_HT'#_HTBM'+str(massPt)
pfix+='_'+datestr#+'_'+timestr

def readTree(file):
	if not os.path.exists(file): 
		print "Error: File does not exist! Aborting ...",file
		os._exit(1)
	tFile = TFile(file,'READ')
	tTree = tFile.Get('ljmet')
	return tFile, tTree 

print "READING TREES"
shapesFiles = ['jec','jer']
tTreeData = {}
tFileData = {}
for data in dataList:
	print "READING:", data
	tFileData[data],tTreeData[data]=readTree(step1Dir+'/'+samples[data]+'_hadd.root')

tTreeSig = {}
tFileSig = {}
for sig in sigList:
	for decay in decays:
		print "READING:", sig+decay
		print "        nominal"
		tFileSig[sig+decay],tTreeSig[sig+decay]=readTree(step1Dir+'/'+samples[sig+decay]+'_hadd.root')
		if doAllSys:
			for syst in shapesFiles:
				for ud in ['Up','Down']:
					print "        "+syst+ud
					tFileSig[sig+decay+syst+ud],tTreeSig[sig+decay+syst+ud]=readTree(step1Dir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[sig+decay]+'_hadd.root')

tTreeBkg = {}
tFileBkg = {}
for bkg in bkgList+q2List:
	if bkg in q2List and not doQ2sys: continue
	print "READING:",bkg
	print "        nominal"
	tFileBkg[bkg],tTreeBkg[bkg]=readTree(step1Dir+'/'+samples[bkg]+'_hadd.root')
	if doAllSys:
		for syst in shapesFiles:
			for ud in ['Up','Down']:
				if bkg in q2List:
					tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=None,None
				else:
					print "        "+syst+ud
					tFileBkg[bkg+syst+ud],tTreeBkg[bkg+syst+ud]=readTree(step1Dir.replace('nominal',syst.upper()+ud.lower())+'/'+samples[bkg]+'_hadd.root')
print "FINISHED READING"

plotList = {#discriminantName:(discriminantLJMETName, binning, xAxisLabel)
	'HT':('AK4HT',linspace(0, 5000, 51).tolist(),';H_{T} (GeV);'),
	'ST':('AK4HTpMETpLepPt',linspace(0, 5000, 51).tolist(),';S_{T} (GeV);'),
	'minMlb':('minMleppBjet',linspace(0, 800, 51).tolist(),';min[M(l,b)] (GeV);'),
	'BDT':('BDT',linspace(-1, 1, 37).tolist(),';BDT;'),
	'LeadJetPt':('theJetLeadPt',linspace(0, 1500, 51).tolist(),';p_{T}(j_{1}) (GeV);'),
	'aveBBdr':('aveBBdr',linspace(0, 6, 51).tolist(),';#topbar{#Delta(b,b)}'),
	'mass_maxJJJpt':('mass_maxJJJpt',linspace(0, 3000, 51).tolist(),';M(jjj) with max[p_{T}(jjj)] (GeV);'),
	'mass_maxBBmass':('mass_maxBBmass',linspace(0, 1500, 51).tolist(),';max[M(b,b)] (GeV);'),
	'mass_maxBBpt':('mass_maxBBpt',linspace(0, 1500, 51).tolist(),';M(b,b) with max[p_{T}(bb)] (GeV);'),
	'lepDR_minBBdr':('lepDR_minBBdr',linspace(0, 6, 51).tolist(),';#Delta(l,bb) with min#Delta(b,b)'),
	'mass_minLLdr':('mass_minLLdr',linspace(0, 1000, 51).tolist(),';M(b,b) with min#[Delta(b,b)] (GeV);'),
	'mass_minBBdr':('mass_minBBdr',linspace(0, 1000, 51).tolist(),';M(j,j) with min#[Delta(j,j)], j #neq b (GeV);'),
	}

iPlot='HT' #choose a discriminant from plotList!
print "PLOTTING:",iPlot
print "         LJMET Variable:",plotList[iPlot][0]
print "         X-AXIS TITLE  :",plotList[iPlot][2]
print "         BINNING USED  :",plotList[iPlot][1]

catList = list(itertools.product(isEMlist,nttaglist,nWtaglist,nbtaglist,njetslist))
nCats  = len(catList)
catInd = 1
for cat in catList:
 	if cat[4]=='4':
 		if cat[3]=='3' or cat[3]=='4p': continue
  	if cat[4]=='5' or cat[4]=='6p':
 		if cat[3]=='3p': continue
	catDir = cat[0]+'_nT'+cat[1]+'_nW'+cat[2]+'_nB'+cat[3]+'_nJ'+cat[4]
 	datahists = {}
 	bkghists  = {}
 	sighists  = {}
#  	if len(sys.argv)>1: outDir=sys.argv[1]
#  	else: 
	outDir = os.getcwd()
	outDir+='/'+pfix
	if not os.path.exists(outDir): os.system('mkdir '+outDir)
	outDir+='/'+cutString
	if not os.path.exists(outDir): os.system('mkdir '+outDir)
	outDir+='/'+catDir
	if not os.path.exists(outDir): os.system('mkdir '+outDir)
 	category = {'isEM':cat[0],'nttag':cat[1],'nWtag':cat[2],'nbtag':cat[3],'njet':cat[4]}
 	for data in dataList: 
 		datahists.update(analyze(tTreeData,data,cutList,isotrig,False,doJetRwt,iPlot,plotList[iPlot],category,region))
 		if catInd==nCats: del tFileData[data]
 	for bkg in bkgList: 
 		bkghists.update(analyze(tTreeBkg,bkg,cutList,isotrig,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region))
 		if catInd==nCats: del tFileBkg[bkg]
 		if doAllSys and catInd==nCats:
 			for syst in shapesFiles:
 				for ud in ['Up','Down']: del tFileBkg[bkg+syst+ud]
 	for sig in sigList: 
 		for decay in decays: 
 			sighists.update(analyze(tTreeSig,sig+decay,cutList,isotrig,doAllSys,doJetRwt,iPlot,plotList[iPlot],category,region))
 			if catInd==nCats: del tFileSig[sig+decay]
 			if doAllSys and catInd==nCats:
 				for syst in shapesFiles:
 					for ud in ['Up','Down']: del tFileSig[sig+decay+syst+ud]
 	if doQ2sys: 
 		for q2 in q2List: 
 			bkghists.update(analyze(tTreeBkg,q2,cutList,isotrig,False,doJetRwt,iPlot,plotList[iPlot],category,region))
 			if catInd==nCats: del tFileBkg[q2]

 	#Negative Bin Correction
 	for bkg in bkghists.keys(): negBinCorrection(bkghists[bkg])
 	for sig in sighists.keys(): negBinCorrection(sighists[sig])

 	#OverFlow Correction
 	for data in datahists.keys(): overflow(datahists[data])
 	for bkg in bkghists.keys():   overflow(bkghists[bkg])
 	for sig in sighists.keys():   overflow(sighists[sig])

 	pickle.dump(datahists,open(outDir+'/datahists.p','wb'))
 	pickle.dump(bkghists,open(outDir+'/bkghists.p','wb'))
 	pickle.dump(sighists,open(outDir+'/sighists.p','wb'))
 	catInd+=1

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))

