#!/usr/bin/python

import os, sys, fnmatch
import math

theDir = '/home/ssagir/CMSSW_7_3_0/src/optimization_x53x53/templates_2015_10_20_16_23_57/'

lepPtCutList = [40,45,50,60,80,100] # suggest: 40 - 100
leadJetPtCutList = [200,250,300,450,750] # suggest: 150 - 300, 450
subLeadJetPtCutList = [90,150,300,450] # suggest: 50 -150
metCutList = [20,25,30,40,50,75,150] # suggest: 20 - 100
bjetPtCutList = [0] # suggest: 100 - 250 with large steps
STcutList = [0] # suggest: 700 - 1300
HTcutList = [0] # suggest:
njetsCutList = [3,4,5]
nbjetsCutList = [1]

count=0
countTotal=0
os.chdir(theDir)
for lepPtCut in lepPtCutList:
	#if count>1: break
	for leadJetPtCut in leadJetPtCutList:
		for subLeadJetPtCut in subLeadJetPtCutList:
			for metCut in metCutList:
				for bjetPtCut in bjetPtCutList:
					for STcut in STcutList:
						for HTcut in HTcutList:
							for njetsCut in njetsCutList:
								for nbjetsCut in nbjetsCutList:
									if leadJetPtCut <= subLeadJetPtCut: continue
									cutString = 'lep'+str(int(lepPtCut))+'_MET'+str(int(metCut))+'_leadJet'+str(int(leadJetPtCut))+'_subLeadJet'+str(int(subLeadJetPtCut))+'_leadbJet'+str(int(bjetPtCut))+'_ST'+str(int(STcut))+'_HT'+str(int(HTcut)) +'_NJets'+str(int(njetsCut))+'_NBJets'+str(int(nbjetsCut))
									#rFile = rootFileDir+'/Treeout_TSD_entry'+str(i)+'.root'
									jFile = theDir+cutString+'/condor.job'
									lFile = theDir+cutString+'/condor.log'
									eFile = theDir+cutString+'/condor.err'
									oFile = theDir+cutString+'/condor.out'
									#statement = os.path.exists(rFile) and os.path.getsize(rFile)>1000
									errFdata = open(eFile).read()
									try: 
										logFdata = open(lFile).read()
										statement1 = 'Normal termination (return value 0)' in logFdata
									except: statement1 = False
									outFdata = open(oFile).read()
									statement2 = os.path.getsize(eFile)==0
									statement3 = not ('error' in errFdata or 'Error' in errFdata)
									statement4 = 'minutes ---' in outFdata
									statement5 = '_NJets3_' in cutString
									countTotal+=1
									if not (statement1 and statement2 and statement3 and statement4):# and statement5:
									#if not (statement2 and statement3):
										print "*" * 40
										print theDir+cutString
										if not statement1: print "Failed log file"
										if not statement2: print "Failed err size file"
										if not statement3: print "error in err file"
										if not statement4: print "Failed out file"
										
										os.chdir(cutString)
										#print ">condor_submit " + jFile
										#os.system('rm ' + lFile)
										#os.system('condor_submit ' + jFile)
										
										#print ">mv "+theDir+cutString+" /eos/uscms/store/user/lpcljm/noreplica/ssagir/X53_optimization/"+theDir.split('/')[-2]
										#os.system("cp -r "+theDir+cutString+" /eos/uscms/store/user/lpcljm/noreplica/ssagir/X53_optimization/"+theDir.split('/')[-2])
										print "*" * 40
										os.chdir('..')
										count+=1
										
print count, "jobs failed", "out of",countTotal
	

