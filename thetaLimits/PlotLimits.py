from ROOT import *
from array import array
import os,sys,math
from math import *

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

blind=False
saveKey=''#'_test'
signal = 'HTB'
lumiPlot = '36'
lumiStr = '36p4'

mass_str = ['180','200','250','300','350','400','450','500']
theory_xsec = [0.919,0.783951,0.4982015,0.324766,0.2184385,0.148574,0.104141,0.0735225][:len(mass_str)]#pb
scale_up = [1.9,1.9,1.9,1.8,1.8,1.8,1.7,1.8,1.7,1.6,1.7,1.7][:len(mass_str)]#%
scale_dn = [1.9,1.8,1.7,1.6,1.6,1.5,1.5,1.5,1.5,1.5,1.5,1.5][:len(mass_str)]#%
pdf_up   = [3.7,3.9,4.1,4.4,4.7,5.1,5.6,6.1,6.7,7.0,8.0,9.0][:len(mass_str)]#%
pdf_dn   = [3.6,3.7,3.9,4.0,4.2,4.5,4.8,5.2,5.6,6.1,6.6,7.2][:len(mass_str)]#%

mass   =array('d', [float(item) for item in mass_str])
masserr=array('d',[0 for i in range(len(mass))])
exp   =array('d',[0 for i in range(len(mass))])
experr=array('d',[0 for i in range(len(mass))])
obs   =array('d',[0 for i in range(len(mass))])
obserr=array('d',[0 for i in range(len(mass))]) 
exp68H=array('d',[0 for i in range(len(mass))])
exp68L=array('d',[0 for i in range(len(mass))])
exp95H=array('d',[0 for i in range(len(mass))])
exp95L=array('d',[0 for i in range(len(mass))])

theory_xsec_up = [math.sqrt(scale**2+pdf**2)*xsec*0/100 for xsec,scale,pdf in zip(theory_xsec,scale_up,pdf_up)]
theory_xsec_dn = [math.sqrt(scale**2+pdf**2)*xsec*0/100 for xsec,scale,pdf in zip(theory_xsec,scale_dn,pdf_dn)]

theory_xsec_v    = TVectorD(len(mass),array('d',theory_xsec))
theory_xsec_up_v = TVectorD(len(mass),array('d',theory_xsec_up))
theory_xsec_dn_v = TVectorD(len(mass),array('d',theory_xsec_dn))      

theory_xsec_gr = TGraphAsymmErrors(TVectorD(len(mass),mass),theory_xsec_v,TVectorD(len(mass),masserr),TVectorD(len(mass),masserr),theory_xsec_dn_v,theory_xsec_up_v)
theory_xsec_gr.SetFillStyle(3001)
theory_xsec_gr.SetFillColor(ROOT.kRed)
			   
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

def PlotLimits(limitDir,limitFile,discriminant,chiral,tempKey):
    histPrefix=discriminant+'_'+str(lumiStr)+'fb'+chiral
    ljust_i = 10
    print
    print 'mass'.ljust(ljust_i), 'observed'.ljust(ljust_i), 'expected'.ljust(ljust_i), '-2 Sigma'.ljust(ljust_i), '-1 Sigma'.ljust(ljust_i), '+1 Sigma'.ljust(ljust_i), '+2 Sigma'.ljust(ljust_i)
    
    limExpected = 180
    limObserved = 180
    for i in range(len(mass)):
        lims = {}
        
        try:
        	if blind:fobs = open(limitDir+cutString+limitFile.replace(signal+'M180',signal+'M'+mass_str[i]), 'rU')
        	if not blind: fobs = open(limitDir+cutString+limitFile.replace(signal+'M180',signal+'M'+mass_str[i]).replace('expected','observed'), 'rU')
        	linesObs = fobs.readlines()
        	fobs.close()
        	
        	fexp = open(limitDir+cutString+limitFile.replace(signal+'M180',signal+'M'+mass_str[i]), 'rU')
        	linesExp = fexp.readlines()
        	fexp.close()
        except: 
        	print "SKIPPING SIGNAL: "+mass_str[i]
        	continue
        
        lims[-1] = float(linesObs[1].strip().split()[1])#/10
        obs[i] = float(linesObs[1].strip().split()[1])#/10
        obserr[i] = 0
        
        lims[.5] = float(linesExp[1].strip().split()[1])
        exp[i] = float(linesExp[1].strip().split()[1])
        experr[i] = 0
        lims[.16] = float(linesExp[1].strip().split()[4])
        exp68L[i] = float(linesExp[1].strip().split()[4])
        lims[.84] = float(linesExp[1].strip().split()[5])
        exp68H[i] = float(linesExp[1].strip().split()[5])
        lims[.025] = float(linesExp[1].strip().split()[2])
        exp95L[i] = float(linesExp[1].strip().split()[2])
        lims[.975] = float(linesExp[1].strip().split()[3])
        exp95H[i] = float(linesExp[1].strip().split()[3])
    
        if i!=0:
        	if(exp[i]>theory_xsec[i] and exp[i-1]<theory_xsec[i-1]) or (exp[i]<theory_xsec[i] and exp[i-1]>theory_xsec[i-1]):
        		limExpected,ycross = getSensitivity(i,exp)
        	if(obs[i]>theory_xsec[i] and obs[i-1]<theory_xsec[i-1]) or (obs[i]<theory_xsec[i] and obs[i-1]>theory_xsec[i-1]):
        		limObserved,ycross = getSensitivity(i,obs)
        		
        exp95L[i]=(exp[i]-exp95L[i])
        exp95H[i]=abs(exp[i]-exp95H[i])
        exp68L[i]=(exp[i]-exp68L[i])
        exp68H[i]=abs(exp[i]-exp68H[i])

        round_i = 5
        print str(mass[i]).ljust(ljust_i), str(round(lims[-1],round_i)).ljust(ljust_i), str(round(lims[.5],round_i)).ljust(ljust_i), str(round(lims[.025],round_i)).ljust(ljust_i), str(round(lims[.16],round_i)).ljust(ljust_i), str(round(lims[.84],round_i)).ljust(ljust_i), str(round(lims[.975],round_i)).ljust(ljust_i)
    print
    signExp = "= "
    signObs = "= "
    if limExpected==180: signExp = "< "
    if limObserved==180: signObs = "< "
    print "Expected lower limit "+signExp,int(round(limExpected)),"GeV"
    print "Observed lower limit "+signObs,int(round(limObserved)),"GeV"
    print

    massv = TVectorD(len(mass),mass)
    expv = TVectorD(len(mass),exp)
    exp68Hv = TVectorD(len(mass),exp68H)
    exp68Lv = TVectorD(len(mass),exp68L)
    exp95Hv = TVectorD(len(mass),exp95H)
    exp95Lv = TVectorD(len(mass),exp95L)

    obsv = TVectorD(len(mass),obs)
    masserrv = TVectorD(len(mass),masserr)
    obserrv = TVectorD(len(mass),obserr)
    experrv = TVectorD(len(mass),experr)       


    observed = TGraphAsymmErrors(massv,obsv,masserrv,masserrv,obserrv,obserrv)
    observed.SetLineColor(ROOT.kBlack)
    observed.SetLineWidth(2)
    observed.SetMarkerStyle(20)
    expected = TGraphAsymmErrors(massv,expv,masserrv,masserrv,experrv,experrv)
    expected.SetLineColor(ROOT.kBlack)
    expected.SetLineWidth(2)
    expected.SetLineStyle(2)
    expected68 = TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp68Lv,exp68Hv)
    expected68.SetFillColor(ROOT.kGreen)
    expected95 = TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp95Lv,exp95Hv)
    expected95.SetFillColor(ROOT.kYellow)

    c4 = TCanvas("c4","Limits", 1000, 800)
    c4.SetBottomMargin(0.15)
    c4.SetRightMargin(0.06)
    c4.SetLogy()

    expected95.Draw("a3")
    expected95.GetYaxis().SetRangeUser(0.301+.00001,100.45)
    #expected95.GetYaxis().SetRangeUser(.008+.00001,200.45)
    expected95.GetXaxis().SetRangeUser(180,500)
    if tempKey=='nB0': expected95.GetYaxis().SetRangeUser(.008+.00001,25.45)   
    if signal=='X53':
    	expected95.GetXaxis().SetTitle("X_{5/3} mass [GeV]")
    	expected95.GetYaxis().SetTitle("#sigma(X_{5/3}#bar{X}_{5/3})[pb] - "+chiral.replace('left','LH').replace('right','RH'))
    if signal=='HTB':
    	expected95.GetXaxis().SetTitle("H^{#pm} mass [GeV]")
    	expected95.GetYaxis().SetTitle("#sigma#times(H^{#pm}#rightarrowtb)[pb]")
    else:
		expected95.GetXaxis().SetTitle(signal+" mass [GeV]")
		expected95.GetYaxis().SetTitle("#sigma ("+signal+"#bar{"+signal+"})[pb]")
		
    expected68.Draw("3same")
    expected.Draw("same")

    if not blind: observed.Draw("cpsame")
    theory_xsec_gr.SetLineColor(2)
    theory_xsec_gr.SetLineStyle(1)
    theory_xsec_gr.SetLineWidth(2)
    #theory_xsec_gr.Draw("3same") 
    theory.SetLineColor(2)
    theory.SetLineStyle(1)
    theory.SetLineWidth(2)
    #theory.Draw("same")                                                             
        
    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.03)
    latex2.SetTextAlign(11) # align right
    latex2.DrawLatex(0.58, 0.96, "CMS Preliminary, " + str(lumiPlot) + " fb^{-1} (13 TeV)")

    latex4 = TLatex()
    latex4.SetNDC()
    latex4.SetTextSize(0.06)
    latex4.SetTextAlign(31) # align right
    #if chiral=='left': latex4.DrawLatex(0.30, 0.82, "LH")
    #if chiral=='right': latex4.DrawLatex(0.30, 0.82, "RH")

    #legend = TLegend(.62,.62,.92,.92) # top right
    legend = TLegend(.32,.72,.92,.92) # top right
    #if tempKey=='nB0': legend = TLegend(.62,.32,.92,.62)
    if tempKey=='nB0': legend = TLegend(.32,.42,.92,.62)
    if not blind: legend.AddEntry(observed , '95% CL observed', "lp")
    legend.AddEntry(expected68, '#pm 1#sigma expected', "f")
    legend.AddEntry(expected, '95% CL expected', "l")
    legend.AddEntry(expected95, '#pm 2#sigma expected', "f")
    #legend.AddEntry(theory_xsec_gr, 'Signal Cross Section', 'lf')

    legend.SetShadowColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetNColumns(2)
    legend.Draw()
    
    c4.RedrawAxis()

    folder = '.'
    outDir=folder+'/'+limitDir.split('/')[-3]+'plots'
    if not os.path.exists(outDir): os.system('mkdir '+outDir)
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+'_'+binning+saveKey+'_'+tempKey+'.eps')
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+'_'+binning+saveKey+'_'+tempKey+'.pdf')
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+'_'+binning+saveKey+'_'+tempKey+'.png')
    return int(round(limExpected)), int(round(limObserved))

doBRScan = False
BRs={}
BRs['BW']=[0.50,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
BRs['TH']=[0.25,0.0,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]
BRs['TZ']=[0.25,1.0,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
nBRconf=len(BRs['BW'])
if not doBRScan: nBRconf=1

#tempKeys = ['subset']#,'all_lumiFlat','isSR','isCR','isE','isM']
# tempKeys = ['all','isSR','isCR','isE','isM','nB2_nJ4','nB2_nJ5','nB2_nJ6p','nB3_nJ5','nB3_nJ6p','nB3p_nJ4','nB4p_nJ5','nB4p_nJ6p']
# tempKeys = [item+'_noBBB' for item in tempKeys]
tempKeys = ['nB1_nJ3','nB1_nJ4','nB1_nJ5','nB1_nJ6p',
		    'nB2p_nJ3','nB2_nJ4','nB2_nJ5','nB2_nJ6p',
		    'nB3p_nJ4','nB3_nJ5','nB3_nJ6p',
		    'nB4p_nJ5','nB4p_nJ6p','isCR','isSR','all']
tempKeys = ['all']#_merged','all_unmerged']
cutString=''
dirs = {
		'conf1':'templates_bkgSplit_wRwt_cats_2016_12_10_flatSysts',
		}
dirKeyList = ['conf1']
binnings = ['0p15','0p2','0p25','0p3']
binnings = ['WJsplit_rebinned_stat0p3_merged','WJsplit_TTsplit_rebinned_stat0p3_merged',
'WJsplit_rebinned_stat0p3_unmerged','WJsplit_TTsplit_rebinned_stat0p3_unmerged']
iPlots = ['YLD']#,'HT','ST','minMlb']

expLims = {}
obsLims = {}
for dirKey in dirKeyList:
	dir = dirs[dirKey]
	expLims[dirKey] = {}
	obsLims[dirKey] = {}
	for iPlot in iPlots:
		expLims[dirKey][iPlot] = {}
		obsLims[dirKey][iPlot] = {}
		for binning in binnings:
			expLims[dirKey][iPlot][binning] = []
			obsLims[dirKey][iPlot][binning] = []
			for tempKey in tempKeys:
				for BRind in range(nBRconf):
					BRconfStr=''
					if doBRScan: BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
					limitDir='/user_data/ssagir/HTB_limits_2016/'+dir+'/'+tempKey+BRconfStr+'/'
					limitFile='/limits_templates_'+iPlot+'_'+signal+'M180'+BRconfStr+'_'+str(lumiStr)+'fb_'+binning+'_expected.txt'	
					print limitDir+cutString+limitFile
					expTemp,obsTemp = PlotLimits(limitDir,limitFile,iPlot,'',tempKey+BRconfStr)
					expLims[dirKey][iPlot][binning].append(expTemp)
					obsLims[dirKey][iPlot][binning].append(obsTemp)
if doBRScan:
	print "BRs_bW:",BRs['BW']
	print "BRs_tH:",BRs['TH']
	print "BRs_tZ:",BRs['TZ']
# print "Configs :",tempKeys
# for dir in dirs:
# 	print dir
# 	for binning in binnings:
# 		print binning
# 		print "Expected:",expLims[dir][binning]
# 		print "Observed:",obsLims[dir][binning]
for dirKey in dirKeyList: print dirKey,
print
for ind in range(len(tempKeys)):
	print "////////////////////////////////"
	print "Channel Configuration: "+tempKeys[ind]
	print "////////////////////////////////"
	for binning in binnings:
		for dirKey in dirKeyList:
			for iPlot in iPlots: print dirKey+'_'+iPlot+'_'+binning,
	print
	print "Expected:"
	for binning in binnings:
		for dirKey in dirKeyList: 
			for iPlot in iPlots: print expLims[dirKey][iPlot][binning][ind],
	print
	print "Observed:"
	for binning in binnings:
		for dirKey in dirKeyList: 
			for iPlot in iPlots: print obsLims[dirKey][iPlot][binning][ind],
	print


