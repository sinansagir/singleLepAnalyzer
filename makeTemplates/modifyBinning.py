#!/usr/bin/python

import os,sys,time,math,fnmatch
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from array import array
#from weights import *
from modSyst import *
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
# -- A custom binning choice can also be given by manually filling "xbinsList[chn]" for each channel
#    with the preferred choice of binning
# -- If no rebinning is wanted, but want to add PDF and R/F uncertainties, use a stat unc threshold 
#    that is larger than 100% (i.e, >1.)
# -- If CR and SR templates are in the same file and single bins are required for CR templates,
#    this can be done with "singleBinCR" bool (assumes that the CR templates contain "isCR" tags!).
# -- Use "removalKeys" to remove specific systematics from the output file.
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

year=sys.argv[1]
if year=='R17':
	from weights17 import *
else:
	from weights18 import *

iPlot=sys.argv[2]
saveKey = ''#'_50GeV_100GeVnB2'
# if len(sys.argv)>1: iPlot=str(sys.argv[1])
cutString = ''#'lep30_MET150_NJets4_DR1_1jet450_2jet150'
lumiStr = str(targetlumi/1000).replace('.','p')+'fb' # 1/fb
templateDir = os.getcwd()+'/templates_'+year+'_'+sys.argv[3]+'/'+cutString
combinefile = 'templates_'+iPlot+'_'+lumiStr+'.root'

quiet = True #if you don't want to see the warnings that are mostly from the stat. shape algorithm!
rebinCombine = True #else rebins theta templates
doStatShapes = False
doPDF = True
doMURF = True
doPSWeights = True
normalizeTheorySystSig = True #normalize renorm/fact, PDF and ISR/FSR systematics to nominal templates for signals
normalizeTheorySystBkg = False #normalize renorm/fact, PDF and ISR/FSR systematics to nominal templates for backgrounds
#tttt, X53, TT, BB, HTB, etc --> this is used to identify signal histograms for combine templates when normalizing the pdf and muRF shapes to nominal!!!!
sigName = 'tttt' #MAKE SURE THIS WORKS FOR YOUR ANALYSIS PROPERLY!!!!!!!!!!!
massList = [690]
sigProcList = [sigName+'M'+str(mass) for mass in massList]
if sigName=='tttt': sigProcList = [sigName]
if sigName=='X53': 
	sigProcList = [sigName+'LHM'+str(mass) for mass in [1100,1200,1400,1700]]
	sigProcList+= [sigName+'RHM'+str(mass) for mass in range(900,1700+1,100)]
ttProcList = ['ttnobb','ttbb'] # ['ttjj','ttcc','ttbb','ttbj']
bkgProcList = ttProcList + ['top','ewk','qcd'] #put the most dominant process first
removeSystFromYields = ['hdamp','ue','njet','njetsf'] #list of systematics to be removed from yield errors

minNbins=1 #min number of bins to be merged
stat = 0.3 #statistical uncertainty requirement (enter >1.0 for no rebinning; i.g., "1.1")
statThres = 0.05 #statistical uncertainty threshold on total background to assign BB nuisances -- enter 0.0 to assign BB for all bins
#if len(sys.argv)>1: stat=float(sys.argv[1])
singleBinCR = False
symmetrizeTopPtShift = False
scaleSignalsToXsec = False # !!!!!Make sure you know signal x-sec used in input files to this script. If this is True, it will scale signal histograms by x-sec in weights.py!!!!!
zero = 1E-12
xMin = -1e9
xMax = 1e9

if iPlot.startswith('HT') and stat<1.: 
	minNbins=2 #(assuming initial hists are 25 GeV bins) min 50GeV bin width (_nB2_ categories are set to min 100GeV bin width below)
	xMin = 0
	if iPlot=='HT': xMin = 500
	xMax = 3000
if iPlot=='maxJJJpt' and stat<1.: 
	minNbins=2 #(assuming initial hists are 15 GeV bins) min 30GeV bin width
	xMin = 0
	xMax = 3000
if iPlot=='ST' and stat<1.: 
	minNbins=2 #(assuming initial hists are 15 GeV bins) min 30GeV bin width
	xMin = 500
	xMax = 4000
if iPlot=='BDT' and stat<1.: 
	minNbins=2 #(assuming initial hists are 15 GeV bins) min 30GeV bin width
	xMin = -1
	xMax = 1
		
if rebinCombine:
	dataName = 'data_obs'
	upTag = 'Up'
	downTag = 'Down'
else: #theta
	dataName = 'DATA'
	upTag = '__plus'
	downTag = '__minus'

addCRsys = False
addShapes = True
lumiSys = 0.025 # lumi uncertainty
if year=='R17': lumiSys = 0.023
eltrigSys = 0.0 #electron trigger uncertainty
mutrigSys = 0.0 #muon trigger uncertainty
elIdSys = 0.03 #electron id uncertainty
muIdSys = 0.03 #muon id uncertainty
elIsoSys = 0.0 #electron isolation uncertainty
muIsoSys = 0.0 #muon isolation uncertainty
htRwtSys = 0.0
#njetSys = 0.048
#if year=='R17': njetSys = 0.075
elcorrdSys = math.sqrt(lumiSys**2+eltrigSys**2+elIdSys**2+elIsoSys**2+htRwtSys**2)#+njetSys**2)
mucorrdSys = math.sqrt(lumiSys**2+mutrigSys**2+muIdSys**2+muIsoSys**2+htRwtSys**2)#+njetSys**2)

removalKeys = {} # True == keep, False == remove
removalKeys['jsf__'] = False

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

totBkgHists = {}
dataHists_ = {}
for hist in datahists:
	channel = hist[hist.find('fb_')+3:hist.find('__')]
	dataHists_[channel]=tfile.Get(hist).Clone()
	print hist
	procfirst = 0
	try: totBkgHists[channel]=tfile.Get(hist.replace('__'+dataName,'__'+bkgProcList[0])).Clone()
	except: 
		totBkgHists[channel]=tfile.Get(hist.replace('__'+dataName,'__'+bkgProcList[1])).Clone()
		procfirst = 1
	for proc in bkgProcList:
		if proc==bkgProcList[procfirst]: continue
		try: totBkgHists[channel].Add(tfile.Get(hist.replace('__'+dataName,'__'+proc)))
		except: 
			print 'WARNING! Missing',proc,'for category:',hist,'Skipping this process!!!!'
			pass

totNbins = 0
xbinsListTemp = {}
for chn in totBkgHists.keys():
	if 'isE' not in chn: continue
	xbinsListTemp[chn]=[totBkgHists[chn].GetXaxis().GetBinUpEdge(totBkgHists[chn].GetXaxis().GetNbins())]
	Nbins = totBkgHists[chn].GetNbinsX()
	totTempBinContent_E = 0.
	totTempBinContent_M = 0.
	totTempBinErrSquared_E = 0.
	totTempBinErrSquared_M = 0.
	totDataTempBinContent_E = 0.
	totDataTempBinContent_M = 0.
	totDataTempBinErrSquared_E = 0.
	totDataTempBinErrSquared_M = 0.
	nBinsMerged = 0
	for iBin in range(1,Nbins+1):
		totTempBinContent_E += totBkgHists[chn].GetBinContent(Nbins+1-iBin)
		totTempBinContent_M += totBkgHists[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
		totTempBinErrSquared_E += totBkgHists[chn].GetBinError(Nbins+1-iBin)**2
		totTempBinErrSquared_M += totBkgHists[chn.replace('isE','isM')].GetBinError(Nbins+1-iBin)**2
		totDataTempBinContent_E += dataHists_[chn].GetBinContent(Nbins+1-iBin)
		totDataTempBinContent_M += dataHists_[chn.replace('isE','isM')].GetBinContent(Nbins+1-iBin)
		totDataTempBinErrSquared_E += dataHists_[chn].GetBinError(Nbins+1-iBin)**2
		totDataTempBinErrSquared_M += dataHists_[chn.replace('isE','isM')].GetBinError(Nbins+1-iBin)**2
		nBinsMerged+=1
		#if nBinsMerged<minNbins: continue
		if nBinsMerged<minNbins or ('_nB2_' in chn and nBinsMerged<4 and (iPlot.startswith('HT') or iPlot=='ST' or iPlot=='BDT')): continue
		if totTempBinContent_E>0. and totTempBinContent_M>0.:
			if math.sqrt(totTempBinErrSquared_E)/totTempBinContent_E<=stat and math.sqrt(totTempBinErrSquared_M)/totTempBinContent_M<=stat:
				totTempBinContent_E = 0.
				totTempBinContent_M = 0.
				totTempBinErrSquared_E = 0.
				totTempBinErrSquared_M = 0.
				totDataTempBinContent_E = 0.
				totDataTempBinContent_M = 0.
				totDataTempBinErrSquared_E = 0.
				totDataTempBinErrSquared_M = 0.
				nBinsMerged=0
				xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))
	if xbinsListTemp[chn][-1]!=totBkgHists[chn].GetXaxis().GetBinLowEdge(1): xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(1))
	if totBkgHists[chn].GetBinContent(1)==0. or totBkgHists[chn.replace('isE','isM')].GetBinContent(1)==0.: 
		if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
	elif totBkgHists[chn].GetBinError(1)/totBkgHists[chn].GetBinContent(1)>stat or totBkgHists[chn.replace('isE','isM')].GetBinError(1)/totBkgHists[chn.replace('isE','isM')].GetBinContent(1)>stat: 
		if len(xbinsListTemp[chn])>2: del xbinsListTemp[chn][-2]
	xbinsListTemp[chn.replace('isE','isM')]=xbinsListTemp[chn]
	if stat>1.0:
		xbinsListTemp[chn] = [totBkgHists[chn].GetXaxis().GetBinUpEdge(totBkgHists[chn].GetXaxis().GetNbins())]
		for iBin in range(1,Nbins+1): 
			xbinsListTemp[chn].append(totBkgHists[chn].GetXaxis().GetBinLowEdge(Nbins+1-iBin))
		xbinsListTemp[chn.replace('isE','isM')] = xbinsListTemp[chn]
	totNbins+=len(xbinsListTemp[chn])

tfile.Close()

print "==> Here is the binning I found with",stat*100,"% uncertainty threshold: "
print "//"*40
xbinsList = {}
for chn in xbinsListTemp.keys():
	xbinsList[chn] = []
	for ibin in range(len(xbinsListTemp[chn])): xbinsList[chn].append(xbinsListTemp[chn][len(xbinsListTemp[chn])-1-ibin])
	if 'isCR' in chn and singleBinCR: xbinsList[chn] = [xbinsList[chn][0],xbinsList[chn][-1]]
	if (iPlot.startswith('HT') or iPlot=='maxJJJpt' or iPlot=='ST') and stat<1.: xMax = xbinsList[chn][-2]+(500-xbinsList[chn][-2]%500)
	if xMin>xbinsList[chn][0]: xbinsList[chn][0] = xMin
	if xMax<xbinsList[chn][-1] and xMin!=xMax: xbinsList[chn][-1] = xMax
	for ibin in range(1,len(xbinsList[chn])-1):
		if xbinsList[chn][ibin]<=xbinsList[chn][0] or xbinsList[chn][ibin]>=xbinsList[chn][-1]: del xbinsList[chn][ibin]
	print chn,"=",xbinsList[chn]
print "//"*40
print "==> Total number of bins =",totNbins
print "//"*40

xbins = {}
for key in xbinsList.keys(): xbins[key] = array('d', xbinsList[key])

iRfile=0
yieldsAll = {}
yieldsErrsAll = {}
nBBnuis = {}
nBBnuis['bkg'] = 0
for sig in sigProcList: nBBnuis[sig] = 0
for rfile in rfiles: 
	print "REBINNING FILE:",rfile
	tfiles = {}
	outputRfiles = {}
	tfiles[iRfile] = TFile(rfile)	
	outputRfiles[iRfile] = TFile(rfile.replace('.root',saveKey+'_rebinned_stat'+str(stat).replace('.','p')+'.root'),'RECREATE')

	print "PROGRESS:"
	for chn in channels:
		print "         ",chn,gettime()
		rebinnedHists = {}
		#Rebinning histograms
		for hist in allhists[chn]:
			rebinnedHists[hist]=tfiles[iRfile].Get(hist).Rebin(len(xbins[chn])-1,hist,xbins[chn])
			rebinnedHists[hist].SetDirectory(0)
			overflow(rebinnedHists[hist])
			underflow(rebinnedHists[hist])
			if '__pdf' in hist:
				if upTag not in hist and downTag not in hist: continue
			if '__mu' in hist or '__isr' in hist or '__fsr' in hist: continue
			if any([item in hist and not removalKeys[item] for item in removalKeys.keys()]): continue
			if '__toppt'+downTag in hist and symmetrizeTopPtShift:
				for ibin in range(1, rebinnedHists[hist].GetNbinsX()+1):
					rebinnedHists[hist].SetBinContent(ibin, 2.*rebinnedHists[hist.replace('__toppt'+downTag,'')].GetBinContent(ibin)-rebinnedHists[hist.replace('__toppt'+downTag,'__toppt'+upTag)].GetBinContent(ibin))
			rebinnedHists[hist].Write()
			if '__trigeff' in hist:
				if 'isE' in hist: 
					newEname = rebinnedHists[hist].GetName().replace('__trigeff','__eltrigeff')
					rebinnedHists[newEname] = rebinnedHists[hist].Clone(newEname)
					rebinnedHists[newEname].Write()
				if 'isM' in hist:
					newMname = rebinnedHists[hist].GetName().replace('__trigeff','__mutrigeff')
					rebinnedHists[newMname] = rebinnedHists[hist].Clone(newMname)
					rebinnedHists[newMname].Write()
			
			#Add additional shift histograms to be able to uncorrelate them across years
			if hist.endswith(upTag) or hist.endswith(downTag):
				newEname = rebinnedHists[hist].GetName().replace(upTag,'_'+year+upTag).replace(downTag,'_'+year+downTag)
				rebinnedHists[newEname] = rebinnedHists[hist].Clone(newEname)
				rebinnedHists[newEname].Write()
			yieldHistName = hist
			if not rebinCombine: yieldHistName = hist.replace('_sig','_'+rfile.split('_')[-2])
			yieldsAll[yieldHistName] = rebinnedHists[hist].Integral()
			yieldsErrsAll[yieldHistName] = 0.
			for ibin in range(1,rebinnedHists[hist].GetXaxis().GetNbins()+1):
				yieldsErrsAll[yieldHistName] += rebinnedHists[hist].GetBinError(ibin)**2
			yieldsErrsAll[yieldHistName] = math.sqrt(yieldsErrsAll[yieldHistName])

		#add statistical uncertainty shapes:
		if rebinCombine and doStatShapes:
			chnHistName = [hist for hist in datahists if chn in hist][0]
			rebinnedHists['chnTotBkgHist'] = rebinnedHists[chnHistName.replace(dataName,bkgProcList[0])].Clone()
			for bkg in bkgProcList:
				if bkg!=bkgProcList[0]:rebinnedHists['chnTotBkgHist'].Add(rebinnedHists[chnHistName.replace(dataName,bkg)])
			for ibin in range(1, rebinnedHists['chnTotBkgHist'].GetNbinsX()+1):
				if rebinnedHists['chnTotBkgHist'].GetBinError(ibin)/rebinnedHists['chnTotBkgHist'].GetBinContent(ibin)<=statThres: continue
				if rebinnedHists['chnTotBkgHist'].GetNbinsX()==1:
					for bkg in bkgProcList:
						val = rebinnedHists[chnHistName.replace(dataName,bkg)].GetBinContent(ibin)
						if val==0:
							if not quiet: print "WARNING: "+bkg+" has zero content in "+chn+" channel and bin#"+str(ibin)+", is this what you expect??? I will not assign stat shape shifts for this proc and chn!!!"
							continue
						error = rebinnedHists[chnHistName.replace(dataName,bkg)].GetBinError(ibin)
						err_up_name = rebinnedHists[chnHistName.replace(dataName,bkg)].GetName()+'__CMS_'+sigName+'_'+chn+'_'+year+'_'+bkg+"_bin_%iUp" % ibin
						err_dn_name = rebinnedHists[chnHistName.replace(dataName,bkg)].GetName()+'__CMS_'+sigName+'_'+chn+'_'+year+'_'+bkg+"_bin_%iDown" % ibin
						rebinnedHists[err_up_name] = rebinnedHists[chnHistName.replace(dataName,bkg)].Clone(err_up_name)
						rebinnedHists[err_dn_name] = rebinnedHists[chnHistName.replace(dataName,bkg)].Clone(err_dn_name)
						rebinnedHists[err_up_name].SetBinContent(ibin, val + error)
						rebinnedHists[err_dn_name].SetBinContent(ibin, val - error)
						if val-error<0: negBinCorrection(rebinnedHists[err_dn_name])
						elif val-error==0:
							if not quiet: print "WARNING: "+bkg+" has zero down shift in "+chn+" channel and bin#"+str(ibin)+" (1 event). Setting down shift to (bin content)*0.001"
							rebinnedHists[err_dn_name].SetBinContent(ibin, val*0.001)
						rebinnedHists[err_up_name].Write()
						rebinnedHists[err_dn_name].Write()
						nBBnuis['bkg']+=1
				else:
					dominantBkgProc = bkgProcList[0]
					val = rebinnedHists[chnHistName.replace(dataName,bkgProcList[0])].GetBinContent(ibin)
					for bkg in bkgProcList:
						if rebinnedHists[chnHistName.replace(dataName,bkg)].GetBinContent(ibin)>val: 
							val = rebinnedHists[chnHistName.replace(dataName,bkg)].GetBinContent(ibin)
							dominantBkgProc = bkg
					if val==0 and not quiet: print "WARNING: The most dominant bkg proc "+dominantBkgProc+" has zero content in "+chn+" channel and bin#"+str(ibin)+". Something is wrong!!!"
					error = rebinnedHists['chnTotBkgHist'].GetBinError(ibin)
					err_up_name = rebinnedHists[chnHistName.replace(dataName,dominantBkgProc)].GetName()+'__CMS_'+sigName+'_'+chn+'_'+year+'_'+dominantBkgProc+"_bin_%iUp" % ibin
					err_dn_name = rebinnedHists[chnHistName.replace(dataName,dominantBkgProc)].GetName()+'__CMS_'+sigName+'_'+chn+'_'+year+'_'+dominantBkgProc+"_bin_%iDown" % ibin
					rebinnedHists[err_up_name] = rebinnedHists[chnHistName.replace(dataName,dominantBkgProc)].Clone(err_up_name)
					rebinnedHists[err_dn_name] = rebinnedHists[chnHistName.replace(dataName,dominantBkgProc)].Clone(err_dn_name)
					rebinnedHists[err_up_name].SetBinContent(ibin, val + error)
					rebinnedHists[err_dn_name].SetBinContent(ibin, val - error)
					if val-error<0: negBinCorrection(rebinnedHists[err_dn_name])
					rebinnedHists[err_up_name].Write()
					rebinnedHists[err_dn_name].Write()
					nBBnuis['bkg']+=1
				for sig in sigProcList:
					sigNameNoMass = sigName
					if 'LH' in sig: sigNameNoMass = sigName+'LH'
					if 'RH' in sig: sigNameNoMass = sigName+'RH'
					val = rebinnedHists[chnHistName.replace(dataName,sig)].GetBinContent(ibin)
					if val==0: #This is not a sensitive bin, so no need for stat shape??
						if not quiet: print "WARNING: "+sig+" has zero content in "+chn+" channel and bin#"+str(ibin)+". I won't assign shape shifts for this bin!!!"
						continue
					error = rebinnedHists[chnHistName.replace(dataName,sig)].GetBinError(ibin)
					if error/val<=statThres: continue
					err_up_name = rebinnedHists[chnHistName.replace(dataName,sig)].GetName()+'__CMS_'+sigName+'_'+chn+'_'+year+'_'+sigNameNoMass+"_bin_%iUp" % ibin
					err_dn_name = rebinnedHists[chnHistName.replace(dataName,sig)].GetName()+'__CMS_'+sigName+'_'+chn+'_'+year+'_'+sigNameNoMass+"_bin_%iDown" % ibin
					rebinnedHists[err_up_name] = rebinnedHists[chnHistName.replace(dataName,sig)].Clone(err_up_name)
					rebinnedHists[err_dn_name] = rebinnedHists[chnHistName.replace(dataName,sig)].Clone(err_dn_name)
					rebinnedHists[err_up_name].SetBinContent(ibin, val + error)
					rebinnedHists[err_dn_name].SetBinContent(ibin, val - error)
					if val-error<0: negBinCorrection(rebinnedHists[err_dn_name])
					rebinnedHists[err_up_name].Write()
					rebinnedHists[err_dn_name].Write()
					nBBnuis[sig]+=1
								
		#Constructing muRF shapes
		if doMURF:
			muRUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'muR'+upTag in k.GetName() and '_'+chn+'_' in k.GetName()]
			newMuRFName = 'muRF'
			for hist in muRUphists:
				proc_ = hist.split('__')[1]
				if proc_ in ttProcList: proc_ = 'tt'
				muRFUpHist = rebinnedHists[hist].Clone(hist.replace('muR'+upTag,newMuRFName+upTag))
				muRFDnHist = rebinnedHists[hist].Clone(hist.replace('muR'+upTag,newMuRFName+downTag))
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

					muRFUpHist.SetBinContent(ibin,histList[indCorrdUp].GetBinContent(ibin))
					muRFDnHist.SetBinContent(ibin,histList[indCorrdDn].GetBinContent(ibin))

					muRFUpHist.SetBinError(ibin,histList[indCorrdUp].GetBinError(ibin))
					muRFDnHist.SetBinError(ibin,histList[indCorrdDn].GetBinError(ibin))
				if (normalizeTheorySystSig and ('__sig' in hist or '__'+sigName in hist)) or (normalizeTheorySystBkg and not ('__sig' in hist or '__'+sigName in hist)): #normalize up/down shifts to nominal
					muRFUpHist.Scale(histList[0].Integral()/(muRFUpHist.Integral()+zero))
					muRFDnHist.Scale(histList[0].Integral()/(muRFDnHist.Integral()+zero))
				muRFUpHist.Write()
				muRFDnHist.Write()
				yieldsAll[muRFUpHist.GetName().replace('_sig','_'+rfile.split('_')[-2])] = muRFUpHist.Integral()
				yieldsAll[muRFDnHist.GetName().replace('_sig','_'+rfile.split('_')[-2])] = muRFDnHist.Integral()
				
				#Decorrelate muRF systematic ("muRF" still need to be removed in doThetaLimits.py!):
				muRFUpHist2 = muRFUpHist.Clone(hist.replace('muR'+upTag,newMuRFName+'_'+proc_+upTag))
				muRFDnHist2 = muRFDnHist.Clone(hist.replace('muR'+upTag,newMuRFName+'_'+proc_+downTag))
				muRFUpHist2.Write()
				muRFDnHist2.Write()
				
				#Add additional shift histograms to be able to uncorrelate them across years
				muRFUpHist3 = muRFUpHist.Clone(hist.replace('muR'+upTag,newMuRFName+'_'+proc_+'_'+year+upTag))
				muRFDnHist3 = muRFDnHist.Clone(hist.replace('muR'+upTag,newMuRFName+'_'+proc_+'_'+year+downTag))
				muRFUpHist3.Write()
				muRFDnHist3.Write()
				muRFUpHist4 = muRFUpHist.Clone(hist.replace('muR'+upTag,newMuRFName+'_'+year+upTag))
				muRFDnHist4 = muRFDnHist.Clone(hist.replace('muR'+upTag,newMuRFName+'_'+year+downTag))
				muRFUpHist4.Write()
				muRFDnHist4.Write()

		#constructing PSweights
		if doPSWeights:
			isrUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'isr'+upTag in k.GetName() and '_'+chn+'_' in k.GetName()]
			newPSwgtName = 'PSwgt'
			for hist in isrUphists:
				proc_ = hist.split('__')[1]
				if proc_ in ttProcList: proc_ = 'tt'
				PSwgtUpHist = rebinnedHists[hist].Clone(hist.replace('isr'+upTag,newPSwgtName+upTag))
				PSwgtDnHist = rebinnedHists[hist].Clone(hist.replace('isr'+upTag,newPSwgtName+downTag))
				histList = [
					rebinnedHists[hist[:hist.find('__isr')]], #nominal
					rebinnedHists[hist], #renormWeights[4]
					rebinnedHists[hist.replace('isr'+upTag,'isr'+downTag)],
					rebinnedHists[hist.replace('isr'+upTag,'fsr'+upTag)],
					rebinnedHists[hist.replace('isr'+upTag,'fsr'+downTag)],
					]
				for ibin in range(1,histList[0].GetNbinsX()+1):
					weightList = [histList[ind].GetBinContent(ibin) for ind in range(len(histList))]
					indCorrdUp = weightList.index(max(weightList))
					indCorrdDn = weightList.index(min(weightList))

					PSwgtUpHist.SetBinContent(ibin,histList[indCorrdUp].GetBinContent(ibin))
					PSwgtDnHist.SetBinContent(ibin,histList[indCorrdDn].GetBinContent(ibin))

					PSwgtUpHist.SetBinError(ibin,histList[indCorrdUp].GetBinError(ibin))
					PSwgtDnHist.SetBinError(ibin,histList[indCorrdDn].GetBinError(ibin))
				if (normalizeTheorySystSig and ('__sig' in hist or '__'+sigName in hist)) or (normalizeTheorySystBkg and not ('__sig' in hist or '__'+sigName in hist)): #normalize up/down shifts to nominal
					PSwgtUpHist.Scale(histList[0].Integral()/(PSwgtUpHist.Integral()+zero))
					PSwgtDnHist.Scale(histList[0].Integral()/(PSwgtDnHist.Integral()+zero))
				PSwgtUpHist.Write()
				PSwgtDnHist.Write()
				yieldsAll[PSwgtUpHist.GetName().replace('_sig','_'+rfile.split('_')[-2])] = PSwgtUpHist.Integral()
				yieldsAll[PSwgtDnHist.GetName().replace('_sig','_'+rfile.split('_')[-2])] = PSwgtDnHist.Integral()
				
				#Decorrelate PSwgt systematic ("PSwgt" still need to be removed in doThetaLimits.py!):
				PSwgtUpHist2 = PSwgtUpHist.Clone(hist.replace('isr'+upTag,newPSwgtName+'_'+proc_+upTag))
				PSwgtDnHist2 = PSwgtDnHist.Clone(hist.replace('isr'+upTag,newPSwgtName+'_'+proc_+downTag))
				PSwgtUpHist2.Write()
				PSwgtDnHist2.Write()

				#Add additional shift histograms to be able to uncorrelate them across years
				PSwgtUpHist3 = PSwgtUpHist.Clone(hist.replace('isr'+upTag,newPSwgtName+'_'+proc_+'_'+year+upTag))
				PSwgtDnHist3 = PSwgtDnHist.Clone(hist.replace('isr'+upTag,newPSwgtName+'_'+proc_+'_'+year+downTag))
				PSwgtUpHist3.Write()
				PSwgtDnHist3.Write()
				PSwgtUpHist4 = PSwgtUpHist.Clone(hist.replace('isr'+upTag,newPSwgtName+'_'+year+upTag))
				PSwgtDnHist4 = PSwgtDnHist.Clone(hist.replace('isr'+upTag,newPSwgtName+'_'+year+downTag))
				PSwgtUpHist4.Write()
				PSwgtDnHist4.Write()

		#Constructing PDF shapes
		if doPDF:
			pdfUphists = [k.GetName() for k in tfiles[iRfile].GetListOfKeys() if 'pdf0' in k.GetName() and chn in k.GetName()]
			PDFName = 'pdf'
			for hist in pdfUphists:
				pdfUpHist = rebinnedHists[hist].Clone(hist.replace('pdf0',PDFName+upTag))
				pdfDnHist = rebinnedHists[hist].Clone(hist.replace('pdf0',PDFName+downTag))
				for ibin in range(1,pdfUpHist.GetNbinsX()+1):
					weightList = [rebinnedHists[hist.replace('pdf0','pdf'+str(pdfInd))].GetBinContent(ibin) for pdfInd in range(100)]
					indPDFUp = sorted(range(len(weightList)), key=lambda k: weightList[k])[83]
					indPDFDn = sorted(range(len(weightList)), key=lambda k: weightList[k])[15]
					pdfUpHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinContent(ibin))
					pdfDnHist.SetBinContent(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinContent(ibin))
					pdfUpHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFUp))].GetBinError(ibin))
					pdfDnHist.SetBinError(ibin,rebinnedHists[hist.replace('pdf0','pdf'+str(indPDFDn))].GetBinError(ibin))
				if (normalizeTheorySystSig and ('__sig' in hist or '__'+sigName in hist)) or (normalizeTheorySystBkg and not ('__sig' in hist or '__'+sigName in hist)): #normalize up/down shifts to nominal
					nominalInt = rebinnedHists[hist[:hist.find('__pdf')]].Integral()
					pdfUpHist.Scale(nominalInt/(pdfUpHist.Integral()+zero))
					pdfDnHist.Scale(nominalInt/(pdfDnHist.Integral()+zero))
				pdfUpHist.Write()
				pdfDnHist.Write()
				yieldsAll[pdfUpHist.GetName().replace('_sig','_'+rfile.split('_')[-2])] = pdfUpHist.Integral()
				yieldsAll[pdfDnHist.GetName().replace('_sig','_'+rfile.split('_')[-2])] = pdfDnHist.Integral()

				#Add additional shift histograms to be able to uncorrelate them across years
				pdfUpHist2 = pdfUpHist.Clone(hist.replace('pdf0',PDFName+'_'+year+upTag))
				pdfDnHist2 = pdfDnHist.Clone(hist.replace('pdf0',PDFName+'_'+year+downTag))
				pdfUpHist2.Write()
				pdfDnHist2.Write()

	tfiles[iRfile].Close()
	outputRfiles[iRfile].Close()
	iRfile+=1

print ">> Rebinning Done!"
print "===>>> Number of BB nuisances added:"
print "                                    bkg:",nBBnuis['bkg']
for sig in sigProcList: print "                                    "+sig+":",nBBnuis[sig]

for chn in channels:
	modTag = chn[chn.find('nW'):]
	modelingSys[dataName+'_'+modTag]=0.
	modelingSys['qcd_'+modTag]=0.
	if not addCRsys: #else CR uncertainties are defined in modSyst.py module
		for proc in bkgProcList:
			modelingSys[proc+'_'+modTag] = 0.
	
isEMlist =[]
nhottlist=[]
nttaglist=[]
nWtaglist=[]
nbtaglist=[]
njetslist=[]
for chn in channels:
	print chn
	if chn.split('_')[0] not in isEMlist: isEMlist.append(chn.split('_')[0])
	if chn.split('_')[1] not in nhottlist: nhottlist.append(chn.split('_')[1])
	if chn.split('_')[2] not in nttaglist: nttaglist.append(chn.split('_')[2])
	if chn.split('_')[3] not in nWtaglist: nWtaglist.append(chn.split('_')[3])
	if chn.split('_')[4] not in nbtaglist: nbtaglist.append(chn.split('_')[4])
	if chn.split('_')[5] not in njetslist: njetslist.append(chn.split('_')[5])

procNames={}
procNames['dataOverBkg'] = 'Data/Bkg'
procNames['totBkg'] = 'Total bkg'
procNames['data_obs'] = 'Data'
procNames['DATA'] = 'Data'
procNames['top']  = 'TOP'
procNames['ewk']  = 'EWK'
procNames['qcd']  = 'QCD'
procNames['ttcc'] = '\\ttbar+ c(c)'
procNames['ttjj'] = '\\ttbar+ j(j)'
procNames['ttbj'] = '\\ttbar+ b(j)'
procNames['ttbb'] = '$\\ttbar+\\bbbar$'
procNames['tt1b'] = '\\ttbar+ b'
procNames['tt2b'] = '\\ttbar+ 2B'
procNames['ttnobb'] = '$\\ttbar+!\\bbbar$'
for sig in sigProcList: 
	if 'LH' in sig:  procNames[sig]='LH \\xft ('+str(float(sig[6:])/1000)+' \\TeV)'
	elif 'RH' in sig: procNames[sig]='RH \\xft ('+str(float(sig[6:])/1000)+' \\TeV)'
	else: procNames[sig]='\\fourt'

print "List of systematics for "+bkgProcList[0]+" process and "+channels[0]+" channel:"
print "        ",sorted([hist[hist.find(bkgProcList[0]+'__')+len(bkgProcList[0])+2:hist.find(upTag)] for hist in yieldsAll.keys() if channels[0] in hist and '__'+bkgProcList[0]+'__' in hist and upTag in hist])# and 'muRF' not in hist
print "        following will be removed from yield errors:",sorted(removeSystFromYields)

def getShapeSystUnc(proc,chn):
	if not addShapes: return 0
	systematicList = sorted([hist[hist.find(proc+'__')+len(proc)+2:hist.find(upTag)] for hist in yieldsAll.keys() if chn in hist and '__'+proc+'__' in hist and upTag in hist])# and 'muRF' not in hist
	totUpShiftPrctg=0
	totDnShiftPrctg=0
	histoPrefix = allhists[chn][0][:allhists[chn][0].find('__')+2]
	nomHist = histoPrefix+proc
	for syst in systematicList:
		if syst in removeSystFromYields: continue
		for ud in [upTag,downTag]:
			shpHist = histoPrefix+proc+'__'+syst+ud
			shift = yieldsAll[shpHist]/(yieldsAll[nomHist]+zero)-1
			if shift>0.: totUpShiftPrctg+=shift**2
			if shift<0.: totDnShiftPrctg+=shift**2
	shpSystUncPrctg = (math.sqrt(totUpShiftPrctg)+math.sqrt(totDnShiftPrctg))/2 #symmetrize the total shape uncertainty up/down shifts
	return shpSystUncPrctg	

table = []
exceltable = {}
exceltable['YIELDS'] = [proc for proc in bkgProcList+['totBkg',dataName,'dataOverBkg']+sigProcList]
for chn in channels: exceltable[chn] = []

for isEM in isEMlist:
	if isEM=='isE': corrdSys = elcorrdSys
	if isEM=='isM': corrdSys = mucorrdSys
	for nhott in nhottlist:
		for nttag in nttaglist:
			for nWtag in nWtaglist:
				for nbtag in nbtaglist:
					table.append(['break'])
					table.append(['',isEM+'_'+nhott+'_'+nttag+'_'+nWtag+'_'+nbtag+'_yields'])
					table.append(['break'])
					table.append(['YIELDS']+[chn for chn in channels if isEM in chn and nhott+'_' in chn and nttag+'_' in chn and nWtag+'_' in chn and nbtag+'_' in chn]+['\\\\'])
					for proc in bkgProcList+['totBkg',dataName,'dataOverBkg']+sigProcList:
						row = [procNames[proc]]
						for chn in channels:
							if not (isEM in chn and nhott+'_' in chn and nttag+'_' in chn and nWtag+'_' in chn and nbtag+'_' in chn): continue
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
									dataTemp = yieldsAll[histoPrefix+dataName]+zero
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
								if signal in sigProcList:
									if scaleSignalsToXsec:
										yieldtemp*=xsec[signal]
										yielderrtemp*=xsec[signal]**2
								else: yielderrtemp += (modelingSys[proc+'_'+modTag]*yieldtemp)**2
								yielderrtemp += (corrdSys*yieldtemp)**2
							yielderrtemp = math.sqrt(yielderrtemp)
							if proc==dataName: 
								row.append(' & '+str(int(yieldsAll[histoPrefix+proc])))
								exceltable[chn].append(str(int(yieldsAll[histoPrefix+proc])))
							else: 
								row.append(' & '+str(round_sig(yieldtemp,5))+' $\pm$ '+str(round_sig(yielderrtemp,2)))
								exceltable[chn].append(str(yieldtemp)+' $\pm$ '+str(yielderrtemp))
						row.append('\\\\')
						table.append(row)
					iSig = 0
					for sig in sigProcList:
						row=['S/$\sigma_{B}$'+sig]
						iChn = 1
						for chn in channels: 
							if not (isEM in chn and nhott+'_' in chn and nttag+'_' in chn and nWtag+'_' in chn and nbtag+'_' in chn): continue
							bkgYld_ = float([iList for iList in table[table.index(['',isEM+'_'+nhott+'_'+nttag+'_'+nWtag+'_'+nbtag+'_yields']):] if iList[0] == procNames['totBkg']][0][iChn].strip().split()[1])
							bkgYldErr_ = float([iList for iList in table[table.index(['',isEM+'_'+nhott+'_'+nttag+'_'+nWtag+'_'+nbtag+'_yields']):] if iList[0] == procNames['totBkg']][0][iChn].strip().split()[3])
							sigYld_ = float([iList for iList in table[table.index(['',isEM+'_'+nhott+'_'+nttag+'_'+nWtag+'_'+nbtag+'_yields']):] if iList[0] == procNames[sig]][0][iChn].strip().split()[1])
							sigYldErr_ = float([iList for iList in table[table.index(['',isEM+'_'+nhott+'_'+nttag+'_'+nWtag+'_'+nbtag+'_yields']):] if iList[0] == procNames[sig]][0][iChn].strip().split()[3])
							row.append(' & '+str(round_sig(sigYld_/bkgYldErr_,5)))
							iChn+=1
						row.append('\\\\')
						table.append(row)
						iSig+=1
			
for nhott in nhottlist:
	for nttag in nttaglist:
		for nWtag in nWtaglist:
			for nbtag in nbtaglist:
				table.append(['break'])
				table.append(['','isL_'+nhott+'_'+nttag+'_'+nWtag+'_'+nbtag+'_yields'])
				table.append(['break'])
				table.append(['YIELDS']+[chn.replace('isE','isL') for chn in channels if 'isE' in chn and nhott+'_' in chn and nttag+'_' in chn and nWtag+'_' in chn and nbtag+'_' in chn]+['\\\\'])
				for proc in bkgProcList+['totBkg',dataName,'dataOverBkg']+sigProcList:
					row = [procNames[proc]]
					for chn in channels:
						if not ('isE' in chn and nhott+'_' in chn and nttag+'_' in chn and nWtag+'_' in chn and nbtag+'_' in chn): continue
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
								dataTemp = yieldsAll[histoPrefixE+dataName]+yieldsAll[histoPrefixM+dataName]+zero
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
							if signal in sigProcList:
								if scaleSignalsToXsec:
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
				iSig=0
				for sig in sigProcList:
					row=['S/$\sigma_{B}$'+sig]
					iChn = 1
					for chn_ in channels: 
						if not ('isE' in chn and nhott+'_' in chn and nttag+'_' in chn and nWtag+'_' in chn and nbtag+'_' in chn): continue
						chn = chn_.replace('isE','isL')
						bkgYld_ = float([iList for iList in table[table.index(['','isL_'+nhott+'_'+nttag+'_'+nWtag+'_'+nbtag+'_yields']):] if iList[0] == procNames['totBkg']][0][iChn].strip().split()[1])
						bkgYldErr_ = float([iList for iList in table[table.index(['','isL_'+nhott+'_'+nttag+'_'+nWtag+'_'+nbtag+'_yields']):] if iList[0] == procNames['totBkg']][0][iChn].strip().split()[3])
						sigYld_ = float([iList for iList in table[table.index(['','isL_'+nhott+'_'+nttag+'_'+nWtag+'_'+nbtag+'_yields']):] if iList[0] == procNames[sig]][0][iChn].strip().split()[1])
						sigYldErr_ = float([iList for iList in table[table.index(['','isL_'+nhott+'_'+nttag+'_'+nWtag+'_'+nbtag+'_yields']):] if iList[0] == procNames[sig]][0][iChn].strip().split()[3])
						row.append(' & '+str(round_sig(sigYld_/bkgYldErr_,5)))
						iChn+=1
					row.append('\\\\')
					table.append(row)
					iSig+=1

#systematics
table.append(['break'])
table.append(['','Systematics'])
table.append(['break'])
for proc in bkgProcList+sigProcList:
	table.append([proc]+[chn for chn in channels]+['\\\\'])
	systematicList = sorted([hist[hist.find(proc+'__')+len(proc)+2:hist.find(upTag)] for hist in yieldsAll.keys() if channels[0] in hist and '__'+proc+'__' in hist and upTag in hist])
	for syst in systematicList:
		for ud in [upTag,downTag]:
			row = [syst+ud]
			for chn in channels:
				histoPrefix = allhists[chn][0][:allhists[chn][0].find('__')+2]
				nomHist = histoPrefix+proc
				shpHist = histoPrefix+proc+'__'+syst+ud
				try: row.append(' & '+str(round(yieldsAll[shpHist]/(yieldsAll[nomHist]+zero),2)))
				except:
					print "Missing",proc,"for channel:",chn,"and systematic:",syst
					pass
			row.append('\\\\')
			table.append(row)
	row = ['stat']
	for chn in channels:
		histoPrefix = allhists[chn][0][:allhists[chn][0].find('__')+2]
		nomHist = histoPrefix+proc
		try: row.append(' & '+str(round(yieldsErrsAll[nomHist]/(yieldsAll[nomHist]+zero),2)))
		except:
			print "Missing",proc,"for channel:",chn,"and systematic: stat"
			pass
	row.append('\\\\')
	table.append(row)	
	table.append(['break'])

#Yields for excel tables:
table.append(['break'])
table.append(['YIELDS']+exceltable['YIELDS'])
for chn in channels: table.append([chn]+exceltable[chn])			
table.append(['break'])
table.append(['break'])

postFix = ''
if addShapes: postFix+='_addShps'
if addCRsys: postFix+='_addCRunc'
out=open(templateDir+'/'+combinefile.replace('templates','yields').replace('.root',saveKey+'_rebinned_stat'+str(stat).replace('.','p'))+postFix+'.txt','w')
printTable(table,out)

print "       WRITING SUMMARY TEMPLATES: "
for signal in sigProcList:
	print "              ... "+signal
	yldRfileName = templateDir+'/'+combinefile.replace(iPlot,iPlot+'YLD_'+signal).replace('.root',saveKey+'_rebinned_stat'+str(stat).replace('.','p')+'.root')
	yldRfile = TFile(yldRfileName,'RECREATE')
	for isEM in isEMlist:		
		for proc in bkgProcList+[dataName,signal]:
			yldHists = {}
			yldHists[isEM+proc]=TH1F(iPlot+'YLD_'+lumiStr+'_'+isEM+'_nHOT0p_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data_obs','DATA'),'',len(channels)/2,0,len(channels)/2)
			systematicList = sorted([hist[hist.find(proc)+len(proc)+2:hist.find(upTag)] for hist in yieldsAll.keys() if channels[0] in hist and '__'+proc+'__' in hist and upTag in hist])
			for syst in systematicList:
				for ud in ['__plus','__minus']: yldHists[isEM+proc+syst+ud]=TH1F(iPlot+'YLD_'+lumiStr+'_'+isEM+'_nHOT0p_nT0p_nW0p_nB0p_nJ0p__'+proc.replace(signal,'sig').replace('data_obs','DATA')+'__'+syst+ud,'',len(channels)/2,0,len(channels)/2)
			ibin = 1
			for chn in channels:
				if isEM not in chn: continue
				nhottag = chn.split('_')[-5][4:]
				nttag = chn.split('_')[-4][2:]
				nWtag = chn.split('_')[-3][2:]
				nbtag = chn.split('_')[-2][2:]
				njets = chn.split('_')[-1][2:]
				binStr = ''
				if nhottag!='0p':
					if 'p' in nhottag: binStr+='#geq'+nhottag[:-1]+'res-t/'
					else: binStr+=nhottag+'res-t/'
				if nttag!='0p':
					if 'p' in nttag: binStr+='#geq'+nttag[:-1]+'t/'
					else: binStr+=nttag+'t/'
				if nWtag!='0p':
					if 'p' in nWtag: binStr+='#geq'+nWtag[:-1]+'W/'
					else: binStr+=nWtag+'W/'
				if nbtag!='0p':
					if 'p' in nbtag: binStr+='#geq'+nbtag[:-1]+'b/'
					else: binStr+=nbtag+'b/'
				if njets!='0p' and len(njetslist)>1:
					if 'p' in njets: binStr+='#geq'+njets[:-1]+'j'
					else: binStr+=njets+'j'
				if binStr.endswith('/'): binStr=binStr[:-1]
				histoPrefix = allhists[chn][0][:allhists[chn][0].find('__')+2]
				try: 
					yldTemp = yieldsAll[histoPrefix+proc]
					yldErrTemp = yieldsErrsAll[histoPrefix+proc]
				except: 
					print "Missing "+proc+" for channel: "+chn+" (setting yield to zero!!!)"
					yldTemp = 0
					yldErrTemp = 0
				yldHists[isEM+proc].SetBinContent(ibin,yldTemp)
				yldHists[isEM+proc].SetBinError(ibin,yldErrTemp)
				yldHists[isEM+proc].GetXaxis().SetBinLabel(ibin,binStr)
				for syst in systematicList:
					for ud in ['__plus','__minus']:
						try: yldTemp = yieldsAll[histoPrefix+proc+'__'+syst+ud.replace('__plus','Up').replace('__minus','Down')]
						except: yldTemp = 0
						yldHists[isEM+proc+syst+ud].SetBinContent(ibin,yldTemp)
						yldHists[isEM+proc+syst+ud].GetXaxis().SetBinLabel(ibin,binStr)
				ibin+=1
			yldHists[isEM+proc].Write()
			for syst in systematicList:
				for ud in ['__plus','__minus']: yldHists[isEM+proc+syst+ud].Write()
	yldRfile.Close()

print("--- %s minutes ---" % (round((time.time() - start_time)/60,2)))


