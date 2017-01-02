#!/usr/bin/python

import os,sys,time,math,fnmatch
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from array import array
from weights import *
from modSyst_split import *
from utils import *
from ROOT import *
start_time = time.time()

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Run as:
# > python modifyBinning.py
# 
# Optional arguments:
# -- statistical uncertainty threshold
#
# Notes:
# -- Finds certain root files in a given directory and rebins all histograms in each file
# -- A selection of subset of files in the input directory can be done below under "#Setup the selection ..."
# -- A custom binning choice can also be given below and this choice can be activated by giving a stat unc 
#    threshold larger than 100% (>1.) in the argument
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

cutString = 'split'
templateDir = os.getcwd()+'/templates_minMlb_PaperARC_HTweightNew/'+cutString
combinefile = 'templates_minMlb_2p318fb.root'

rebinCombine = False #else rebins theta templates
doStatShapes = False
normalizeRENORM = True #only for signals
normalizePDF    = True #only for signals
#X53X53, TT, BB, etc --> this is used to identify signal histograms for combine templates when normalizing the pdf and muRF shapes to nominal!!!!
sigName = 'TT' #MAKE SURE THIS WORKS FOR YOUR ANALYSIS PROPERLY!!!!!!!!!!!
signalMassList = ['0700','0800','0900','1000','1100','1200','1300','1400','1500','1600','1700','1800']
sigProcList = ['TpTp-M'+mass for mass in signalMassList]
#sigProcList = [sigName+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100)]
if sigName=='X53X53': 
	sigProcList = [sigName+chiral+'M'+str(mass) for mass in range(signalMassRange[0],signalMassRange[1]+100,100) for chiral in ['left','right']]
	if not rebinCombine: sigProcList = [sigName+'M'+str(mass)+chiral for mass in range(signalMassRange[0],signalMassRange[1]+100,100) for chiral in ['left','right']]
bkgProcList = ['TTbar','WJets','SingleTop','DYJets','Diboson','QCD'] #put the most dominant process first
era = "13TeV"

stat = 0.3 #statistical uncertainty requirement (enter >1.0 for no rebinning; i.g., "1.1")
if len(sys.argv)>1: stat=float(sys.argv[1])

if rebinCombine:
	dataName = 'data_obs'
	upTag = 'Up'
	downTag = 'Down'
else: #theta
	dataName = 'DATA'
	upTag = '__plus'
	downTag = '__minus'

addCRsys = True
addShapes = True
lumiSys = 0.027 #lumi uncertainty
eltrigSys = 0.05 #electron trigger uncertainty
mutrigSys = 0.05 #muon trigger uncertainty
elIdSys = 0.01 #electron id uncertainty
muIdSys = 0.01 #muon id uncertainty
elIsoSys = 0.01 #electron isolation uncertainty
muIsoSys = 0.01 #muon isolation uncertainty
elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2)

def findfiles(path, filtre):
    for root, dirs, files in os.walk(path):
        for f in fnmatch.filter(files, filtre):
            yield os.path.join(root, f)

#Setup the selection of the files to be rebinned:          
rfiles = [file for file in findfiles(templateDir, '*.root') if 'rebinned' not in file and combinefile not in file and 'modified' not in file and 'bW' in file]
if rebinCombine: rfiles = [templateDir+'/'+combinefile]

tfile = TFile(rfiles[0])
datahists = [k.GetName() for k in tfile.GetListOfKeys() if '__'+dataName in k.GetName()]
channels = [hist[hist.find('fb_')+3:hist.find('__')] for hist in datahists]
allhists = {chn:[hist.GetName() for hist in tfile.GetListOfKeys() if chn in hist.GetName()] for chn in channels}

removalKeys = {} # True == keep, False == remove
removalKeys['muR__']       = False
removalKeys['muF__']       = False
removalKeys['muRFcorrd__'] = False
removalKeys['btag__']      = False
removalKeys['mistag__']    = False
removalKeys['pileup__']    = False
removalKeys['tau21__']     = True
removalKeys['taupt__']     = True
removalKeys['jsf__']       = True

totBkgHists = {}
for hist in datahists:
	channel = hist[hist.find('fb_')+3:hist.find('__')]
	totBkgHists[channel]=tfile.Get(hist.replace('__'+dataName,'__TTbar')).Clone()
	try: totBkgHists[channel].Add(tfile.Get(hist.replace('__'+dataName,'__SingleTop')))
	except: pass
	try: totBkgHists[channel].Add(tfile.Get(hist.replace('__'+dataName,'__WJets')))
	except: pass
	try: totBkgHists[channel].Add(tfile.Get(hist.replace('__'+dataName,'__DYJets')))
	except: pass
	try: totBkgHists[channel].Add(tfile.Get(hist.replace('__'+dataName,'__Diboson')))
	except: pass
	try: totBkgHists[channel].Add(tfile.Get(hist.replace('__'+dataName,'__QCD')))
	except: pass

xbinsListTemp = {}
for chn in totBkgHists.keys():
	if 'isE' not in chn: continue
	xbinsListTemp[chn]=[tfile.Get(datahists[0]).GetXaxis().GetBinUpEdge(tfile.Get(datahists[0]).GetXaxis().GetNbins())]
	Nbins = tfile.Get(datahists[0]).GetNbinsX()
	totTempBinContent_E = 0.
	totTempBinContent_M = 0.
	totTempBinErrSquared_E = 0.
	totTempBinErrSquared_M = 0.
	for iBin in range(1,Nbins+1):
		totTempBinContent_E += totBkgHists[chn].GetBinContent(Nbins+1-iBin)
		totTempBinContent_M += totBkgHists[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
		totTempBinErrSquared_E += totBkgHists[chn].GetBinError(Nbins+1-iBin)**2
		totTempBinErrSquared_M += totBkgHists[chn.replace('isE','isM')].GetBinError(Nbins+1-iBin)**2
		if totTempBinContent_E>0. and totTempBinContent_M>0.:
			if math.sqrt(totTempBinErrSquared_E)/totTempBinContent_E<=stat and math.sqrt(totTempBinErrSquared_M)/totTempBinContent_M<=stat:
				totTempBinContent_E = 0.
				totTempBinContent_M = 0.
				totTempBinErrSquared_E = 0.
				totTempBinErrSquared_M = 0.
				xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))
	if xbinsListTemp[chn][-1]!=0: xbinsListTemp[chn].append(0)
	if totBkgHists[chn].GetBinContent(1)==0. or totBkgHists[chn.replace('isE','isM')].GetBinContent(1)==0.: 
		if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
	elif totBkgHists[chn].GetBinError(1)/totBkgHists[chn].GetBinContent(1)>stat or totBkgHists[chn.replace('isE','isM')].GetBinError(1)/totBkgHists[chn.replace('isE','isM')].GetBinContent(1)>stat: 
		if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
	xbinsListTemp[chn.replace('isE','isM')]=xbinsListTemp[chn]
	if stat>1.0:
		xbinsListTemp[chn] = [tfile.Get(datahists[0]).GetXaxis().GetBinUpEdge(tfile.Get(datahists[0]).GetXaxis().GetNbins())]
		for iBin in range(1,Nbins+1): 
			xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))
		xbinsListTemp[chn.replace('isE','isM')] = xbinsListTemp[chn]

print "==> Here is the binning I found with",stat*100,"% uncertainty threshold: "
print "//"*40
xbinsList = {}
for chn in xbinsListTemp.keys():
	xbinsList[chn] = []
	for bin in range(len(xbinsListTemp[chn])): xbinsList[chn].append(xbinsListTemp[chn][len(xbinsListTemp[chn])-1-bin])
	print chn,"=",xbinsList[chn]
print "//"*40

xbins = {}
for key in xbinsList.keys(): xbins[key] = array('d', xbinsList[key])

#os._exit(1)

muSFsUp = {'TpTp_M-0700':0.750,'TpTp_M-0800':0.750,'TpTp_M-0900':0.750,'TpTp_M-1000':0.749,'TpTp_M-1100':0.749,'TpTp_M-1200':0.748,'TpTp_M-1300':0.747,'TpTp_M-1400':0.746,'TpTp_M-1500':0.745,'TpTp_M-1600':0.744,'TpTp_M-1700':0.743,'TpTp_M-1800':0.741}
muSFsDn = {'TpTp_M-0700':1.302,'TpTp_M-0800':1.303,'TpTp_M-0900':1.303,'TpTp_M-1000':1.304,'TpTp_M-1100':1.305,'TpTp_M-1200':1.307,'TpTp_M-1300':1.309,'TpTp_M-1400':1.311,'TpTp_M-1500':1.313,'TpTp_M-1600':1.315,'TpTp_M-1700':1.317,'TpTp_M-1800':1.319}
pdfSFsUp = {'TpTp_M-0700':0.912,'TpTp_M-0800':0.908,'TpTp_M-0900':0.902,'TpTp_M-1000':0.890,'TpTp_M-1100':0.889,'TpTp_M-1200':0.895,'TpTp_M-1300':0.895,'TpTp_M-1400':0.888,'TpTp_M-1500':0.897,'TpTp_M-1600':0.904,'TpTp_M-1700':0.885,'TpTp_M-1800':0.873}
pdfSFsDn = {'TpTp_M-0700':1.107,'TpTp_M-0800':1.106,'TpTp_M-0900':1.104,'TpTp_M-1000':1.099,'TpTp_M-1100':1.099,'TpTp_M-1200':1.093,'TpTp_M-1300':1.098,'TpTp_M-1400':1.102,'TpTp_M-1500':1.099,'TpTp_M-1600':1.122,'TpTp_M-1700':1.121,'TpTp_M-1800':1.133}

if sigName == 'BB':
	muSFsUp = {'BpBp_M-0700':0.750,'BpBp_M-0800':0.750,'BpBp_M-0900':0.750,'BpBp_M-1000':0.749,'BpBp_M-1100':0.749,'BpBp_M-1200':0.748,'BpBp_M-1300':0.747,'BpBp_M-1400':0.746,'BpBp_M-1500':0.745,'BpBp_M-1600':0.744,'BpBp_M-1700':0.743,'BpBp_M-1800':0.741}
	muSFsDn = {'BpBp_M-0700':1.302,'BpBp_M-0800':1.303,'BpBp_M-0900':1.303,'BpBp_M-1000':1.304,'BpBp_M-1100':1.305,'BpBp_M-1200':1.307,'BpBp_M-1300':1.309,'BpBp_M-1400':1.311,'BpBp_M-1500':1.313,'BpBp_M-1600':1.315,'BpBp_M-1700':1.317,'BpBp_M-1800':1.319}
	pdfSFsUp = {'BpBp_M-0700':0.912,'BpBp_M-0800':0.908,'BpBp_M-0900':0.902,'BpBp_M-1000':0.890,'BpBp_M-1100':0.889,'BpBp_M-1200':0.895,'BpBp_M-1300':0.895,'BpBp_M-1400':0.888,'BpBp_M-1500':0.897,'BpBp_M-1600':0.904,'BpBp_M-1700':0.885,'BpBp_M-1800':0.873}
	pdfSFsDn = {'BpBp_M-0700':1.107,'BpBp_M-0800':1.106,'BpBp_M-0900':1.104,'BpBp_M-1000':1.099,'BpBp_M-1100':1.099,'BpBp_M-1200':1.093,'BpBp_M-1300':1.098,'BpBp_M-1400':1.102,'BpBp_M-1500':1.099,'BpBp_M-1600':1.122,'BpBp_M-1700':1.121,'BpBp_M-1800':1.133}


iRfile=0
yieldsAll = {}
yieldsErrsAll = {}
yieldsSystErrsAll = {}
for rfile in rfiles: 
	print "REBINNING FILE:",rfile
	tfiles = {}
	outputRfiles = {}
	tfiles[iRfile] = TFile(rfile)	
	outputRfiles[iRfile] = TFile(rfile.replace('.root','_rebinnedDV.root'),'RECREATE')

        mass = rfile.split('/')[-1]
        mass = mass.split('_')[2]
        mass = mass[3:]
        if mass == '700' or mass == '800' or mass == '900': mass = '0'+mass
        newSIGname = 'TpTp_M-'+mass
        if sigName == 'BB': newSIGname = 'BpBp_M-'+mass

	print "PROGRESS:"
	for chn in channels:
		print "         ",chn
		rebinnedHists = {}
		#Rebinning histograms
		for hist in allhists[chn]:
			rebinnedHists[hist]=tfiles[iRfile].Get(hist).Rebin(len(xbins[chn])-1,hist,xbins[chn])
			rebinnedHists[hist].SetDirectory(0)
			# if 'sig__mu' in hist and normalizeRENORM: #normalize the renorm/fact shapes to nominal
			# 	#renormNomHist = tfiles[iRfile].Get(hist[:hist.find('__mu')]).Clone()
			# 	#renormSysHist = tfiles[iRfile].Get(hist).Clone()
			# 	#rebinnedHists[hist].Scale(renormNomHist.Integral()/renormSysHist.Integral())
			# 	if 'plus' in hist: scalefactor = muSFsUp[newSIGname]
			# 	else: scalefactor = muSFsDn[newSIGname]
			# 	rebinnedHists[hist].Scale(scalefactor)
			# if 'sig__pdf' in hist and normalizePDF: #normalize the pdf shapes to nominal
			# 	#renormNomHist = tfiles[iRfile].Get(hist[:hist.find('__pdf')]).Clone()
			# 	#renormSysHist = tfiles[iRfile].Get(hist).Clone()
			# 	#rebinnedHists[hist].Scale(renormNomHist.Integral()/renormSysHist.Integral())
			# 	if 'plus' in hist: scalefactor = pdfSFsUp[newSIGname]
			# 	else: scalefactor = pdfSFsDn[newSIGname]
			# 	rebinnedHists[hist].Scale(scalefactor)
			if '__sig' in hist:
				rebinnedHists[hist.replace('sig',newSIGname)] = rebinnedHists[hist].Clone(hist.replace('sig',newSIGname))
			if '__pdf' in hist:
				if 'Up' not in hist or 'Down' not in hist: continue

			if not any([item in hist and not removalKeys[item] for item in removalKeys.keys()]):                    
				rebinnedHists[hist.replace('sig',newSIGname)].Write()		    

			yieldHistName = hist
			if not rebinCombine: yieldHistName = hist.replace('_sig','_'+rfile.split('_')[-2])
			yieldsAll[yieldHistName] = rebinnedHists[hist].Integral()
			yieldsErrsAll[yieldHistName] = 0.
			for ibin in range(1,rebinnedHists[hist].GetXaxis().GetNbins()+1):
				yieldsErrsAll[yieldHistName] += rebinnedHists[hist].GetBinError(ibin)**2
			yieldsErrsAll[yieldHistName] = math.sqrt(yieldsErrsAll[yieldHistName])


		#print "REBINNED HISTS = "
		#for hist in rebinnedHists.keys():
		#	if 'TpTp' in hist: print rebinnedHists[hist]

		#add statistical uncertainty shapes:
		if rebinCombine and doStatShapes:
			chnHistName = [hist for hist in datahists if chn in hist][0]
			rebinnedHists['chnTotBkgHist'] = rebinnedHists[chnHistName.replace(dataName,bkgProcList[0])].Clone()
			for bkg in bkgProcList:
				if bkg!=bkgProcList[0]:rebinnedHists['chnTotBkgHist'].Add(rebinnedHists[chnHistName.replace(dataName,bkg)])
			for ibin in range(1, rebinnedHists['chnTotBkgHist'].GetNbinsX()+1):
				dominantBkgProc = bkgProcList[0]
				val = rebinnedHists[chnHistName.replace(dataName,bkgProcList[0])].GetBinContent(ibin)
				for bkg in bkgProcList:
					if rebinnedHists[chnHistName.replace(dataName,bkg)].GetBinContent(ibin)>val: 
						val = rebinnedHists[chnHistName.replace(dataName,bkg)].GetBinContent(ibin)
						dominantBkgProc = bkg
				#if val==0: continue #SHOULD WE HAVE THIS???
				error  = rebinnedHists['chnTotBkgHist'].GetBinError(ibin)
				err_up_name = rebinnedHists[chnHistName.replace(dataName,dominantBkgProc)].GetName()+'__CMS_'+sigName+'_'+chn+'_'+era+'_'+dominantBkgProc+"_bin_%iUp" % ibin
				err_dn_name = rebinnedHists[chnHistName.replace(dataName,dominantBkgProc)].GetName()+'__CMS_'+sigName+'_'+chn+'_'+era+'_'+dominantBkgProc+"_bin_%iDown" % ibin
				rebinnedHists[err_up_name] = rebinnedHists[chnHistName.replace(dataName,dominantBkgProc)].Clone(err_up_name)
				rebinnedHists[err_dn_name] = rebinnedHists[chnHistName.replace(dataName,dominantBkgProc)].Clone(err_dn_name)
				rebinnedHists[err_up_name].SetBinContent(ibin, val + error)
				rebinnedHists[err_dn_name].SetBinContent(ibin, val - error)
				if val-error<0: rebinnedHists[err_dn_name].SetBinContent(ibin, 0.) #IS THIS CORRECT???
				rebinnedHists[err_up_name].Write()
				rebinnedHists[err_dn_name].Write()
				for sig in sigProcList:
					sigNameNoMass = sigName
					if 'left' in sig: sigNameNoMass = sigName+'left'
					if 'right' in sig: sigNameNoMass = sigName+'right'
					val = rebinnedHists[chnHistName.replace(dataName,sig)].GetBinContent(ibin)
					#if val==0: continue #SHOULD WE HAVE THIS???
					error  = rebinnedHists[chnHistName.replace(dataName,sig)].GetBinError(ibin)
					err_up_name = rebinnedHists[chnHistName.replace(dataName,sig)].GetName()+'__CMS_'+sigName+'_'+chn+'_'+era+'_'+sigNameNoMass+"_bin_%iUp" % ibin
					err_dn_name = rebinnedHists[chnHistName.replace(dataName,sig)].GetName()+'__CMS_'+sigName+'_'+chn+'_'+era+'_'+sigNameNoMass+"_bin_%iDown" % ibin
					rebinnedHists[err_up_name] = rebinnedHists[chnHistName.replace(dataName,sig)].Clone(err_up_name)
					rebinnedHists[err_dn_name] = rebinnedHists[chnHistName.replace(dataName,sig)].Clone(err_dn_name)
					rebinnedHists[err_up_name].SetBinContent(ibin, val + error)
					rebinnedHists[err_dn_name].SetBinContent(ibin, val - error)
					if val-error<0: rebinnedHists[err_dn_name].SetBinContent(ibin, 0.)
					rebinnedHists[err_up_name].Write()
					rebinnedHists[err_dn_name].Write()
								
		#Change names
		btagUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'btag'+upTag in k.GetName() and chn in k.GetName()]
		for hist in btagUphists:
			if 'sig__' in hist: hist = hist.replace('sig',newSIGname)
			newBTAGName = 'btag_bc'
			btagNewUpHist = rebinnedHists[hist].Clone(hist.replace('btag'+upTag,newBTAGName+upTag))
			btagNewDnHist = rebinnedHists[hist.replace('btag'+upTag,'btag'+downTag)].Clone(hist.replace('btag'+upTag,newBTAGName+downTag))    
			btagNewUpHist.Write()
			btagNewDnHist.Write()

		mistagUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'mistag'+upTag in k.GetName() and chn in k.GetName()]
		for hist in mistagUphists:
			if 'sig__' in hist: hist = hist.replace('sig',newSIGname)
			newMISTAGName = 'btag_udsg'
			mistagNewUpHist = rebinnedHists[hist].Clone(hist.replace('mistag'+upTag,newMISTAGName+upTag))
			mistagNewDnHist = rebinnedHists[hist.replace('mistag'+upTag,'mistag'+downTag)].Clone(hist.replace('mistag'+upTag,newMISTAGName+downTag))
			mistagNewUpHist.Write()
			mistagNewDnHist.Write()

		pileupUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'pileup'+upTag in k.GetName() and chn in k.GetName()]
		for hist in pileupUphists:
			if 'sig__' in hist: hist = hist.replace('sig',newSIGname)
			newPILEUPName = 'pu'
			pileupNewUpHist = rebinnedHists[hist].Clone(hist.replace('pileup'+upTag,newPILEUPName+upTag))
			pileupNewDnHist = rebinnedHists[hist.replace('pileup'+upTag,'pileup'+downTag)].Clone(hist.replace('pileup'+upTag,newPILEUPName+downTag))
			pileupNewUpHist.Write()
			pileupNewDnHist.Write()

		#Constructing muRF shapes
		muRUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'muR'+upTag in k.GetName() and chn in k.GetName()]
		newMuRFName = 'ScaleVar'
		for hist in muRUphists:
			if 'sig__' in hist: hist = hist.replace('sig',newSIGname)
			muRFcorrdNewUpHist = rebinnedHists[hist].Clone(hist.replace('muR'+upTag,newMuRFName+upTag))
			muRFcorrdNewDnHist = rebinnedHists[hist].Clone(hist.replace('muR'+upTag,newMuRFName+downTag))
			histList = [
				rebinnedHists[hist[:hist.find('__mu')]], #nominal
				rebinnedHists[hist], #renormWeights[4]
				rebinnedHists[hist.replace('muR'+upTag,'muR'+downTag)], #renormWeights[2]
				rebinnedHists[hist.replace('muR'+upTag,'muF'+upTag)], #renormWeights[1]
				rebinnedHists[hist.replace('muR'+upTag,'muF'+downTag)], #renormWeights[0]
				rebinnedHists[hist.replace('muR'+upTag,'muRFcorrd'+upTag)], #renormWeights[5]
				rebinnedHists[hist.replace('muR'+upTag,'muRFcorrd'+downTag)] #renormWeights[3]
				]
			for ibin in range(1,histList[0].GetNbinsX()+1):
				weightList = [histList[ind].GetBinContent(ibin) for ind in range(len(histList))]
				indCorrdUp = weightList.index(max(weightList))
				indCorrdDn = weightList.index(min(weightList))

				muRFcorrdNewUpHist.SetBinContent(ibin,histList[indCorrdUp].GetBinContent(ibin))
				muRFcorrdNewDnHist.SetBinContent(ibin,histList[indCorrdDn].GetBinContent(ibin))

				muRFcorrdNewUpHist.SetBinError(ibin,histList[indCorrdUp].GetBinError(ibin))
				muRFcorrdNewDnHist.SetBinError(ibin,histList[indCorrdDn].GetBinError(ibin))
			if (newSIGname+'__mu' in hist and normalizeRENORM) or (rebinCombine and '__'+sigName in hist and '__mu' in hist and normalizeRENORM): #normalize the renorm/fact shapes to nominal
				#print 'MU up =',muRFcorrdNewUpHist.Integral(),', dn =',muRFcorrdNewDnHist.Integral()
				#renormNomHist = histList[0].Clone()
				#renormNomHist = tfiles[iRfile].Get(hist[:hist.find('__mu')]).Clone()
				#muRFcorrdNewUpHist.Scale(renormNomHist.Integral()/muRFcorrdNewUpHist.Integral())
				#muRFcorrdNewDnHist.Scale(renormNomHist.Integral()/muRFcorrdNewDnHist.Integral())
				scalefactorUp = muSFsUp[newSIGname]
				scalefactorDn = muSFsDn[newSIGname]
				#print 'New up =',muRFcorrdNewUpHist.Integral()*scalefactorUp,', dn =',muRFcorrdNewDnHist.Integral()*scalefactorDn
				muRFcorrdNewUpHist.Scale(scalefactorUp)
				muRFcorrdNewDnHist.Scale(scalefactorDn)
				#print 'Xcheck up =',muRFcorrdNewUpHist.Integral(),', dn =',muRFcorrdNewDnHist.Integral()

			muRFcorrdNewUpHist.Write()
			muRFcorrdNewDnHist.Write()
			yieldsAll[muRFcorrdNewUpHist.GetName()] = muRFcorrdNewUpHist.Integral()
			yieldsAll[muRFcorrdNewDnHist.GetName()] = muRFcorrdNewDnHist.Integral()

		#Constructing PDF shapes
		pdfUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'pdf0' in k.GetName() and chn in k.GetName()]
		newPDFName = 'PDF'
		for hist in pdfUphists:
			if 'sig__' in hist: hist = hist.replace('sig',newSIGname)
			pdfNewUpHist = rebinnedHists[hist].Clone(hist.replace('pdf0',newPDFName+upTag))
			pdfNewDnHist = rebinnedHists[hist].Clone(hist.replace('pdf0',newPDFName+downTag))
			for ibin in range(1,pdfNewUpHist.GetNbinsX()+1):
				weightList = [rebinnedHists[hist.replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(100)]
				indPDFUp = sorted(range(len(weightList)), key=lambda k: weightList[k])[83]
				indPDFDn = sorted(range(len(weightList)), key=lambda k: weightList[k])[15]
				pdfNewUpHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinContent(ibin))
				pdfNewDnHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinContent(ibin))
				pdfNewUpHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinError(ibin))
				pdfNewDnHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinError(ibin))
			if (newSIGname+'__pdf' in hist and normalizePDF) or (rebinCombine and '__'+sigName in hist and '__pdf' in hist and normalizePDF): #normalize the renorm/fact shapes to nominal
				#print 'PDF up =',pdfNewUpHist.Integral(),', dn =',pdfNewDnHist.Integral()
				#renormNomHist = rebinnedHists[hist[:hist.find('__pdf')]].Clone() #nominal
				#renormNomHist = tfiles[iRfile].Get(hist[:hist.find('__pdf')]).Clone()
				#pdfNewUpHist.Scale(renormNomHist.Integral()/pdfNewUpHist.Integral())
				#pdfNewDnHist.Scale(renormNomHist.Integral()/pdfNewDnHist.Integral())
				scalefactorUp = pdfSFsUp[newSIGname]
				scalefactorDn = pdfSFsDn[newSIGname]
				#print 'Mass',newSIGname,': assigning SFup =',scalefactorUp,', SFdn =',scalefactorDn
				pdfNewUpHist.Scale(scalefactorUp)
				pdfNewDnHist.Scale(scalefactorDn)

			pdfNewUpHist.Write()
			pdfNewDnHist.Write()
			yieldsAll[pdfNewUpHist.GetName()] = pdfNewUpHist.Integral()
			yieldsAll[pdfNewDnHist.GetName()] = pdfNewDnHist.Integral()
			
	tfiles[iRfile].Close()
	outputRfiles[iRfile].Close()
	iRfile+=1
tfile.Close()
print ">> Rebinning Done!"
'''
for chn in channels:
	modTag = chn[chn.find('nW'):]
	modelingSys[dataName+'_'+modTag]=0.
	modelingSys['TTbar_'+modTag] = modelingSys['TTJets_'+modTag]
	modelingSys['SingleTop_'+modTag] = modelingSys['top_'+modTag]
	modelingSys['Diboson_'+modTag] = modelingSys['VV_'+modTag]
	modelingSys['QCD_'+modTag]=0.
	modelingSys['DYJets_'+modTag]=0.
	if not addCRsys: modelingSys['ewk_'+modTag],modelingSys['top_'+modTag] = 0.,0.
	
isEMlist =[]
nttaglist=[]
nWtaglist=[]
nbtaglist=[]
for chn in channels:
	if chn.split('_')[0+rebinCombine] not in isEMlist: isEMlist.append(chn.split('_')[0+rebinCombine])
	if chn.split('_')[1+rebinCombine] not in nttaglist: nttaglist.append(chn.split('_')[1+rebinCombine])
	if chn.split('_')[2+rebinCombine] not in nWtaglist: nWtaglist.append(chn.split('_')[2+rebinCombine])
	if chn.split('_')[3+rebinCombine] not in nbtaglist: nbtaglist.append(chn.split('_')[3+rebinCombine])

def getShapeSystUnc(proc,chn):
	if not addShapes: return 0
	systematicList = sorted([hist[hist.find(proc)+len(proc)+2:hist.find(upTag)] for hist in yieldsAll.keys() if chn in hist and '__'+proc+'__' in hist and upTag in hist])
	totUpShiftPrctg=0
	totDnShiftPrctg=0
	for syst in systematicList:
		for ud in [upTag,downTag]:
			histoPrefix = allhists[chn][0][:allhists[chn][0].find('__')+2]
			nomHist = histoPrefix+proc
			shpHist = histoPrefix+proc+'__'+syst+ud
			shift = yieldsAll[shpHist]/(yieldsAll[nomHist]+1e-20)-1
			if shift>0.: totUpShiftPrctg+=shift**2
			if shift<0.: totDnShiftPrctg+=shift**2
	shpSystUncPrctg = (math.sqrt(totUpShiftPrctg)+math.sqrt(totDnShiftPrctg))/2 #symmetrize the total shape uncertainty up/down shifts
	return shpSystUncPrctg	

table = []
for isEM in isEMlist:
	if isEM=='isE': corrdSys = elcorrdSys
	if isEM=='isM': corrdSys = mucorrdSys
	for nttag in nttaglist:
		table.append(['break'])
		table.append(['',isEM+'_'+nttag+'_yields'])
		table.append(['break'])
		table.append(['YIELDS']+[chn for chn in channels if isEM in chn and nttag in chn]+['\\\\'])
		for proc in bkgProcList+['totBkg',dataName,'dataOverBkg']+sigProcList:
			row = [proc]
			for chn in channels:
				if not (isEM in chn and nttag in chn): continue
				modTag = chn[chn.find('nW'):]
				histoPrefix = allhists[chn][0][:allhists[chn][0].find('__')+2]
				yieldtemp = 0.
				yielderrtemp = 0.
				if proc=='totBkg' or proc=='dataOverBkg':
					for bkg in bkgProcList:
						try:
							yieldtemp += yieldsAll[histoPrefix+bkg]
							yielderrtemp += yieldsErrsAll[histoPrefix+bkg]**2
							yielderrtemp += (modelingSys[bkg+'_'+modTag]*yieldsAll[histoPrefix+bkg])**2
							yielderrtemp += (getShapeSystUnc(bkg,chn)*yieldsAll[histoPrefix+bkg])**2
						except:
							print "Missing",bkg,"for channel:",chn
							pass
					yielderrtemp += (corrdSys*yieldtemp)**2
					if proc=='dataOverBkg':
						dataTemp = yieldsAll[histoPrefix+dataName]+1e-20
						dataTempErr = yieldsErrsAll[histoPrefix+dataName]**2
						yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
						yieldtemp = dataTemp/yieldtemp
				else:
					try:
						yieldtemp += yieldsAll[histoPrefix+proc]
						yielderrtemp += yieldsErrsAll[histoPrefix+proc]**2
						yielderrtemp += (getShapeSystUnc(proc,chn)*yieldsAll[histoPrefix+proc])**2
					except:
						print "Missing",proc,"for channel:",chn
						pass
					if proc in sigProcList:
						
						signal=proc
						if 'left' in signal: signal=proc.replace('left','')+'left'
						if 'right' in signal: signal=proc.replace('right','')+'right'
						yieldtemp*=xsec[signal]
						yielderrtemp*=xsec[signal]**2
					else: yielderrtemp += (modelingSys[proc+'_'+modTag]*yieldtemp)**2
					yielderrtemp += (corrdSys*yieldtemp)**2
				yielderrtemp = math.sqrt(yielderrtemp)
				if proc==dataName: row.append(' & '+str(int(yieldsAll[histoPrefix+proc])))
				else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
			row.append('\\\\')
			table.append(row)
			
for nttag in nttaglist:
	table.append(['break'])
	table.append(['','isL_'+nttag+'_yields'])
	table.append(['break'])
	table.append(['YIELDS']+[chn.replace('isE','isL') for chn in channels if 'isE' in chn and nttag in chn]+['\\\\'])
	for proc in bkgProcList+['totBkg',dataName,'dataOverBkg']+sigProcList:
		row = [proc]
		for chn in channels:
			if not ('isE' in chn and nttag in chn): continue
			modTag = chn[chn.find('nW'):]
			histoPrefixE = allhists[chn][0][:allhists[chn][0].find('__')+2]
			histoPrefixM = histoPrefixE.replace('isE','isM')
			yieldtemp = 0.
			yieldtempE = 0.
			yieldtempM = 0.
			yielderrtemp = 0. 
			if proc=='totBkg' or proc=='dataOverBkg':
				for bkg in bkgProcList:
					yieldEplusMtemp = 0
					try:
						yieldtempE += yieldsAll[histoPrefixE+bkg]
						yieldtemp += yieldsAll[histoPrefixE+bkg]
						yieldEplusMtemp += yieldsAll[histoPrefixE+bkg]
						yielderrtemp += yieldsErrsAll[histoPrefixE+bkg]**2
						yielderrtemp += (getShapeSystUnc(bkg,chn)*yieldsAll[histoPrefixE+bkg])**2
					except:
						print "Missing",bkg,"for channel:",chn
						pass
					try:
						yieldtempM += yieldsAll[histoPrefixM+bkg]
						yieldtemp += yieldsAll[histoPrefixM+bkg]
						yieldEplusMtemp += yieldsAll[histoPrefixM+bkg]
						yielderrtemp += yieldsErrsAll[histoPrefixM+bkg]**2
						yielderrtemp += (getShapeSystUnc(bkg,chn.replace('isE','isM'))*yieldsAll[histoPrefixM+bkg])**2
					except:
						print "Missing",bkg,"for channel:",chn.replace('isE','isM')
						pass
					yielderrtemp += (modelingSys[bkg+'_'+modTag]*yieldEplusMtemp)**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
				yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
				if proc=='dataOverBkg':
					dataTemp = yieldsAll[histoPrefixE+dataName]+yieldsAll[histoPrefixM+dataName]+1e-20
					dataTempErr = yieldsErrsAll[histoPrefixE+dataName]**2+yieldsErrsAll[histoPrefixM+dataName]**2
					yielderrtemp = ((dataTemp/yieldtemp)**2)*(dataTempErr/dataTemp**2+yielderrtemp/yieldtemp**2)
					yieldtemp = dataTemp/yieldtemp
			else:
				try:
					yieldtempE += yieldsAll[histoPrefixE+proc]
					yieldtemp  += yieldsAll[histoPrefixE+proc]
					yielderrtemp += yieldsErrsAll[histoPrefixE+proc]**2
					yielderrtemp += (getShapeSystUnc(proc,chn)*yieldsAll[histoPrefixE+proc])**2
				except:
					print "Missing",proc,"for channel:",chn
					pass
				try:
					yieldtempM += yieldsAll[histoPrefixM+proc]
					yieldtemp  += yieldsAll[histoPrefixM+proc]
					yielderrtemp += yieldsErrsAll[histoPrefixM+proc]**2
					yielderrtemp += (getShapeSystUnc(proc,chn.replace('isE','isM'))*yieldsAll[histoPrefixM+proc])**2
				except:
					print "Missing",proc,"for channel:",chn.replace('isE','isM')
					pass
				if proc in sigProcList:
					signal=proc
					if 'left' in signal: signal=proc.replace('left','')+'left'
					if 'right' in signal: signal=proc.replace('right','')+'right'
					yieldtempE*=xsec[signal]
					yieldtempM*=xsec[signal]
					yieldtemp*=xsec[signal]
					yielderrtemp*=xsec[signal]**2
				else: yielderrtemp += (modelingSys[proc+'_'+modTag]*yieldtemp)**2 #(addSys*(Nelectron+Nmuon))**2 --> correlated across e/m
				yielderrtemp += (elcorrdSys*yieldtempE)**2+(mucorrdSys*yieldtempM)**2
			yielderrtemp = math.sqrt(yielderrtemp)
			if proc==dataName: row.append(' & '+str(int(yieldsAll[histoPrefixE+proc]+yieldsAll[histoPrefixM+proc])))
			else: row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
		row.append('\\\\')
		table.append(row)

#systematics
table.append(['break'])
table.append(['','Systematics'])
table.append(['break'])
for proc in bkgProcList+sigProcList:
	table.append([proc]+[chn for chn in channels]+['\\\\'])
	systematicList = sorted([hist[hist.find(proc)+len(proc)+2:hist.find(upTag)] for hist in yieldsAll.keys() if channels[0] in hist and '__'+proc+'__' in hist and upTag in hist])
	for syst in systematicList:
		for ud in [upTag,downTag]:
			row = [syst+ud]
			for chn in channels:
				histoPrefix = allhists[chn][0][:allhists[chn][0].find('__')+2]
				nomHist = histoPrefix+proc
				shpHist = histoPrefix+proc+'__'+syst+ud
				try: row.append(' & '+str(round(yieldsAll[shpHist]/(yieldsAll[nomHist]+1e-20),2)))
				except:
					if not ((syst=='toppt' or syst=='q2') and proc!='top'):
						print "Missing",proc,"for channel:",chn,"and systematic:",syst
					pass
			row.append('\\\\')
			table.append(row)
	table.append(['break'])

postFix = ''
if addShapes: postFix+='_addShps'
if not addCRsys: postFix+='_noCRunc'
out=open(templateDir+'/'+combinefile.replace('templates','yields').replace('.root','_rebinned_stat'+str(stat).replace('.','p'))+postFix+'.txt','w')
printTable(table,out)
'''
print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


