from ROOT import *
from array import array
from numpy import linspace
from math import *
import os,sys

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

lumiPlot = '2.2'
lumiStr = '2p215'
spin=''#'right'
distribution = 'HT'
limitDir='/user_data/ssagir/limits/limits_HT_2016_1_13_9_49_29/'
#postfix='VaryinglepPt' # for varying lepPt
#postfix='VaryingMET' # for varying MET
#postfix='VaryingJet1Pts' # for varying jet1Pts
#postfix='VaryingJet2Pts' # for varying jet2Pts
#postfix='VaryingJet3Pts' # for varying jet3Pts
#postfix='VaryingNjets' # for varying NJets
#postfix='VaryingDRs' # for varying DRs
#postfix='VaryingWJet1Pts' # for varying Wjet1Pts
#postfix='VaryingBJet1Pts' # for varying bjet1Pts
#postfix='VaryingHTs' # for varying HTs
#postfix='VaryingSTs' # for varying STs
postfix='VaryingminMlbs' # for varying minMlbs
stat=''#0.75
isRebinned=''#'_rebinned_modified'+str(stat).replace('.','p')
xrange_min=700.
xrange_max=1300.
yrange_min=.0003+.03
yrange_max=1.55

if postfix=='VaryinglepPt': lepPtCutList = [40,50,60,80,100]
else: lepPtCutList = [40]
if postfix=='VaryingJet1Pts': jet1PtCutList = [125,150,200,300,400,500]
else: jet1PtCutList = [125]
if postfix=='VaryingJet2Pts': jet2PtCutList = [75,100,150,200]
else: jet2PtCutList = [75]
if postfix=='VaryingMET': metCutList = [40,50,75,100,125]
else: metCutList = [75]
if postfix=='VaryingNjets': njetsCutList = [3,4,5]
else: njetsCutList = [3]
nbjetsCutList = [0]
if postfix=='VaryingJet3Pts': jet3PtCutList = [30,40,50,75,100,150,200]
else: jet3PtCutList = [40]
jet4PtCutList = [0]
jet5PtCutList = [0]
if postfix=='VaryingDRs': drCutList = [0,1,1.25,1.5]
else: drCutList = [1]
if postfix=='VaryingWJet1Pts': Wjet1PtCutList = [0,200,250,300,400]
else: Wjet1PtCutList = [0]
if postfix=='VaryingBJet1Pts': bjet1PtCutList = [0,100,150,200,300]
else: bjet1PtCutList = [0]
if postfix=='VaryingHTs': htCutList = [0]
else: htCutList = [0]
if postfix=='VaryingSTs': stCutList = [0,600,800,1000,1200,1500,1750,2000]
else: stCutList = [0]#1500]
if postfix=='VaryingminMlbs': minMlbCutList = [0,50,75,100,120,150,200,250,300]
else: minMlbCutList = [200]

#minMlbCutList = [0]
massPoints = [700,800,900,1000,1100,1200,1300]
mass = array('d', massPoints)
masserr = array('d', [0]*len(massPoints))
mass_str = [str(item) for item in massPoints]

#theory_br = [.1285,.1285,.1285,.1285,.1285,.1285,.1285]
theory_xsec_dicts = {'700':0.455,'800':0.196,'900':0.0903,'1000':0.0440,'1100':0.0224,'1200':0.0118,'1300':0.00639}#,0.00354,0.00200,0.001148,0.000666,0.000391]
theory_xsec = [theory_xsec_dicts[item] for item in mass_str]
xsec = array('d', [1]*len(massPoints)) # scales the limits

theory = TGraph(len(mass))
for i in range(len(mass)):
	theory.SetPoint(i, mass[i], theory_xsec[i])

def getSensitivity(index, exp):
	a1=mass[index]-mass[index-1]
	b1=mass[index]-mass[index-1]
	c1=0
	a2=exp[index]-exp[index-1]
	b2=theory_xsec[index]-theory_xsec[index-1]
	c2=theory_xsec[index-1]-exp[index-1]
	s = (c1*b2-c2*b1)/(a1*b2-a2*b1)
	t = (a1*c2-a2*c1)/(a1*b2-a2*b1)
	return mass[index-1]+s*(mass[index]-mass[index-1]), exp[index-1]+s*(exp[index]-exp[index-1])

observed = {}
expected = {}
expected68 = {}
expected95 = {}
crossingList = {}
crossingList2 = {}
ind=1                                                                                               
for conf in cutConfigs:
	lepPtCut,jet1PtCut,jet2PtCut,metCut,njetsCut,nbjetsCut,jet3PtCut,jet4PtCut,jet5PtCut,drCut,Wjet1PtCut,bjet1PtCut,htCut,stCut,minMlbCut=conf[0],conf[1],conf[2],conf[3],conf[4],conf[5],conf[6],conf[7],conf[8],conf[9],conf[10],conf[11],conf[12],conf[13],conf[14]
	#if drCut==1: Wjet1PtCut,bjet1PtCut,stCut=0,0,0
	cutString = 'lep'+str(int(lepPtCut))+'_MET'+str(int(metCut))+'_1jet'+str(int(jet1PtCut))+'_2jet'+str(int(jet2PtCut))+'_NJets'+str(int(njetsCut))+'_NBJets'+str(int(nbjetsCut))+'_3jet'+str(int(jet3PtCut))+'_4jet'+str(int(jet4PtCut))+'_5jet'+str(int(jet5PtCut))+'_DR'+str(drCut)+'_1Wjet'+str(Wjet1PtCut)+'_1bjet'+str(bjet1PtCut)+'_HT'+str(htCut)+'_ST'+str(stCut)+'_minMlb'+str(minMlbCut)
	plotLimits = True
	for i in range(len(mass)):
		try: 
			ftemp = open(limitDir+'/'+cutString+'/limits_templates_'+distribution+'_TTM'+mass_str[i]+'_'+lumiStr+'fb'+isRebinned+'_expected.txt', 'rU')
		except: plotLimits = False
	if not plotLimits: continue
	print
	print cutString
	cutString0 = cutString

	exp   =array('d',[0 for i in range(len(mass))])
	experr=array('d',[0 for i in range(len(mass))])
	obs   =array('d',[0 for i in range(len(mass))])
	obserr=array('d',[0 for i in range(len(mass))])
	exp68H=array('d',[0 for i in range(len(mass))])
	exp68L=array('d',[0 for i in range(len(mass))])
	exp95H=array('d',[0 for i in range(len(mass))])
	exp95L=array('d',[0 for i in range(len(mass))])

	ljust_i = 10
	print
	print 'mass'.ljust(ljust_i), 'observed'.ljust(ljust_i), 'expected'.ljust(ljust_i), '-2 Sigma'.ljust(ljust_i), '-1 Sigma'.ljust(ljust_i), '+1 Sigma'.ljust(ljust_i), '+2 Sigma'.ljust(ljust_i)
	observed[cutString] = TGraph(len(mass))
	expected[cutString] = TGraph(len(mass))

	isCrossed = False
	for i in range(len(mass)):
		lims = {}

		fobs = open(limitDir+'/'+cutString+'/limits_templates_'+distribution+'_TTM'+mass_str[i]+spin+'_'+lumiStr+'fb'+isRebinned+'_observed.txt', 'rU')
		linesObs = fobs.readlines()
		fobs.close()

		fexp = open(limitDir+'/'+cutString+'/limits_templates_'+distribution+'_TTM'+mass_str[i]+spin+'_'+lumiStr+'fb'+isRebinned+'_expected.txt', 'rU')
		linesExp = fexp.readlines()
		fexp.close()

		lims[-1] = float(linesObs[1].strip().split()[1])
		obs[i] = float(linesObs[1].strip().split()[1]) * xsec[i]
		obserr[i] = 0

		lims[.5] = float(linesExp[1].strip().split()[1])
		exp[i] = float(linesExp[1].strip().split()[1]) * xsec[i]
		experr[i] = 0
		lims[.16] = float(linesExp[1].strip().split()[4])
		exp68L[i] = float(linesExp[1].strip().split()[4]) * xsec[i]
		lims[.84] = float(linesExp[1].strip().split()[5])
		exp68H[i] = float(linesExp[1].strip().split()[5]) * xsec[i]
		lims[.025] = float(linesExp[1].strip().split()[2])
		exp95L[i] = float(linesExp[1].strip().split()[2]) * xsec[i]
		lims[.975] = float(linesExp[1].strip().split()[3])
		exp95H[i] = float(linesExp[1].strip().split()[3]) * xsec[i]

		exp95L[i]=(exp[i]-exp95L[i])
		exp95H[i]=abs(exp[i]-exp95H[i])
		exp68L[i]=(exp[i]-exp68L[i])
		exp68H[i]=abs(exp[i]-exp68H[i])
		observed[cutString].SetPoint(i,mass[i],obs[i])
		expected[cutString].SetPoint(i,mass[i],exp[i])

		if i!=0: 
			if(exp[i]>theory_xsec[i] and exp[i-1]<theory_xsec[i-1]) or (exp[i]<theory_xsec[i] and exp[i-1]>theory_xsec[i-1]):
				xcross,ycross = getSensitivity(i,exp)
				crossingList[cutString]=xcross
				isCrossed = True

		round_i = 5
		print str(mass[i]).ljust(ljust_i), str(round(lims[-1],round_i)).ljust(ljust_i), str(round(lims[.5],round_i)).ljust(ljust_i), str(round(lims[.025],round_i)).ljust(ljust_i), str(round(lims[.16],round_i)).ljust(ljust_i), str(round(lims[.84],round_i)).ljust(ljust_i), str(round(lims[.975],round_i)).ljust(ljust_i)
	if not isCrossed:
		crossingList[cutString]=0
		crossingList2[cutString]=0

	print

	observed[cutString].SetLineColor(ROOT.kBlack)
	observed[cutString].SetLineWidth(2)
	observed[cutString].SetMarkerStyle(20)							
	expected[cutString].SetLineColor(ind)
	expected[cutString].SetLineWidth(2)
	expected[cutString].SetLineStyle(1)
	ind+=1

sensitivity = 0
insensitivity = 999999
sensitivityStr = 'None'
insensitivityStr = 'None'
for key in crossingList.keys():
	if crossingList[key]>sensitivity: 
		sensitivity = crossingList[key]
		sensitivityStr = key
	if crossingList[key]==0: print key
	elif crossingList[key]<insensitivity: 
		insensitivity = crossingList[key]
		insensitivityStr = key
print "********************************************************************************"
print "Run over", ind-1, "sets of cuts"
print "********************************************************************************"
print "The best set of cuts are ", sensitivityStr
print "with sensitivity up to ", sensitivity, "GeV"
print "********************************************************************************"
print "The worst set of cuts are ", insensitivityStr
print "with sensitivity up to ", insensitivity, "GeV"

if sensitivityStr!='None': cutString0 = sensitivityStr
                                               
c0 = TCanvas("c0","Limits", 1000, 800)
c0.SetBottomMargin(0.15)
c0.SetRightMargin(0.06)
c0.SetLogy()
	
expected[cutString0].Draw('AL')
expected[cutString0].GetYaxis().SetRangeUser(yrange_min,yrange_max)
expected[cutString0].GetXaxis().SetRangeUser(xrange_min,xrange_max)
expected[cutString0].GetXaxis().SetTitle("T' mass [GeV]")
expected[cutString0].GetYaxis().SetTitle("#sigma (T#bar{T})[pb]")

for key in expected.keys():
	#if key == cutString0: continue
	expected[key].Draw("same")

theory.SetLineColor(2)
theory.SetLineStyle(1)
theory.SetLineWidth(2)
theory.Draw("same")

sensitivityline = TLine(sensitivity,yrange_min,sensitivity,yrange_max)
sensitivityline.SetLineStyle(2)
sensitivityline.Draw("same")
insensitivityline = TLine(insensitivity,yrange_min,insensitivity,yrange_max)
insensitivityline.Draw("same")
insensitivityline.SetLineStyle(2)

prelimtex = TLatex()
prelimtex.SetNDC()
prelimtex.SetTextSize(0.03)
prelimtex.SetTextAlign(11) # align right
prelimtex.DrawLatex(0.58, 0.96, "CMS Preliminary, " + str(lumiPlot) + " fb^{-1} (13 TeV)")

if postfix=='VaryinglepPt':   legend = TLegend(.15,.70,.93,.93) # for varying lepPt
if postfix=='VaryingMET':     legend = TLegend(.15,.70,.93,.93) # for varying MET
if postfix=='VaryingJet1Pts': legend = TLegend(.15,.72,.93,.93) # for varying jet1Pts
if postfix=='VaryingJet2Pts': legend = TLegend(.15,.82,.93,.93) # for varying jet2Pts
if postfix=='VaryingJet3Pts': legend = TLegend(.15,.70,.93,.93) # for varying jet3Pts
if postfix=='VaryingNjets':   legend = TLegend(.15,.82,.93,.93) # for varying Njets
if postfix=='VaryingDRs':     legend = TLegend(.15,.76,.93,.93) # for varying DRs
if postfix=='VaryingWJet1Pts':legend = TLegend(.15,.76,.93,.93) # for varying WJet1Pts
if postfix=='VaryingBJet1Pts':legend = TLegend(.15,.76,.93,.93) # for varying bJet1Pts
if postfix=='VaryingHTs':     legend = TLegend(.15,.82,.93,.93) # for varying HTs
if postfix=='VaryingSTs':     legend = TLegend(.15,.60,.93,.93) # for varying STs
if postfix=='VaryingminMlbs': legend = TLegend(.15,.60,.93,.93) # for varying minMlbs

for lepPtCut in lepPtCutList:
	for metCut in metCutList:
		for jet1PtCut in jet1PtCutList:
			for jet2PtCut in jet2PtCutList:
				for jet3PtCut in jet3PtCutList:
					for njetsCut in njetsCutList:
						for drCut in drCutList:
							for Wjet1PtCut in Wjet1PtCutList:
								for bjet1PtCut in bjet1PtCutList:
									for htCut in htCutList:
										for stCut in stCutList:
											for minMlbCut in minMlbCutList:
												#if drCut==1: Wjet1PtCut,bjet1PtCut,stCut=0,0,0
												cutKey = 'lep'+str(int(lepPtCut))+'_MET'+str(int(metCut))+'_1jet'+str(int(jet1PtCut))+'_2jet'+str(int(jet2PtCut))+'_NJets'+str(int(njetsCut))+'_NBJets'+str(int(nbjetsCut))+'_3jet'+str(int(jet3PtCut))+'_4jet'+str(int(jet4PtCut))+'_5jet'+str(int(jet5PtCut))+'_DR'+str(drCut)+'_1Wjet'+str(Wjet1PtCut)+'_1bjet'+str(bjet1PtCut)+'_HT'+str(htCut)+'_ST'+str(stCut)+'_minMlb'+str(minMlbCut)
												legendStr='lep'+str(lepPtCut)+'_MET'+str(metCut)+'_Ljet'+str(jet1PtCut)+'_SLjet'+str(jet2PtCut)+'_SSLjet'+str(jet3PtCut)+'_Njets'+str(int(njetsCut))+'_DR'+str((drCut))+'_LWjet'+str((Wjet1PtCut))+'_LBjet'+str((bjet1PtCut))+'_HT'+str((htCut))+'_ST'+str((stCut))+'_minMlb'+str((minMlbCut))
												try: legend.AddEntry(expected[cutKey], legendStr, "l")
												except: pass

legend.SetShadowColor(0);
legend.SetFillColor(0);
legend.SetLineColor(0);
legend.Draw()                                               
c0.RedrawAxis()

folder='.'
if not os.path.exists(folder+'/'+limitDir.split('/')[-2]+'plots'): os.system('mkdir '+folder+'/'+limitDir.split('/')[-2]+'plots')
c0.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+spin+distribution+postfix+'_logy.root')
c0.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+spin+distribution+postfix+'_logy.pdf')
c0.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+spin+distribution+postfix+'_logy.png')
c0.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/PlotCombined'+spin+distribution+postfix+'_logy.C')


