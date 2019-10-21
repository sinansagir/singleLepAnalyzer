from ROOT import *
from array import array
import math
from math import *
import os,sys

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

blind=True
combination=True
saveKey=''
signal = 'T'
lumiPlot = '41.5'# '97.4'#
lumiStr = '41p53'
chiral=''#'right'
discriminant=str(sys.argv[1]) #'DnnTprime' #'Tp2MDnn' #'Tp2Mass' #
histPrefix=discriminant+'_'+str(lumiStr)+'fb'+chiral
stat='0.3'#0.75
isRebinned='_rebinned_stat'+str(stat).replace('.','p')#+'_renamed'
#cutString='lep40_MET75_1jet300_2jet150_NJets3_NBJets0_3jet100_4jet0_5jet0_DR1_1Wjet0_1bjet0_HT0_ST0_minMlb0'
cutString=''#split'

mass = array('d', [1100,1200,1300,1400,1500,1600,1700,1800])#
masserr = array('d', [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])#
mass_str = ['1100','1200','1300','1400','1500','1600','1700','1800']#
#mass = array('d', [900,1000,1100,1200,1300,1400,1500])#800,,1600,1700,1800
#masserr = array('d', [0,0,0,0,0,0,0])#0,,0,0,0
#mass_str = ['900','1000','1100','1200','1300','1400','1500']#'800','1600','1700','1800'

exp   =array('d',[0 for i in range(len(mass))])
experr=array('d',[0 for i in range(len(mass))])
obs   =array('d',[0 for i in range(len(mass))])
obserr=array('d',[0 for i in range(len(mass))]) 
exp68H=array('d',[0 for i in range(len(mass))])
exp68L=array('d',[0 for i in range(len(mass))])
exp95H=array('d',[0 for i in range(len(mass))])
exp95L=array('d',[0 for i in range(len(mass))])

xsec = array('d', [1,1,1,1,1,1,1,1,1,1,1])
if chiral=='right':theory_xsec  = [0.190,0.0877,0.0427,0.0217,0.0114,0.00618,0.00342,0.00193,0.00111]
elif chiral=='left':theory_xsec = [0.190,0.0877,0.0427,0.0217,0.0114,0.00618,0.00342,0.00193,0.00111]
else: print "Using TT xsec, for XX enter left or right"
theory_xsec = [0.0224,0.0118,0.00639,0.00354,0.00200,0.001148,0.000666,0.000391]#pb#
xsecErrUp = [1.1,0.64,0.37,0.22,0.14,0.087,0.056,0.037]#fb 
xsecErrDn = [1.0,0.56,0.32,0.19,0.12,0.072,0.045,0.029]#fb 
#theory_xsec = [0.0903,0.0440,0.0224,0.0118,0.00639,0.00354,0.00200]#pb#0.196, ,0.001148,0.000666,0.000391
#xsecErrUp = [4.0,2.1,1.1,0.64,0.37,0.22,0.14]#fb 8.5,,0.087,0.056,0.037
#xsecErrDn = [3.8,1.9,1.0,0.56,0.32,0.19,0.12]#fb 8.1,,0.072,0.045,0.029

theory_xsec_up = [item/1000 for item in xsecErrUp]
theory_xsec_dn = [item/1000 for item in xsecErrDn]
if signal=='X53':
	theory_xsec_up = [0.*item/1000 for item in xsecErrUp]
	theory_xsec_dn = [0.*item/1000 for item in xsecErrDn]

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

def PlotLimits(limitDir,limitFile,tempKey):
    ljust_i = 10
    print
    print 'mass'.ljust(ljust_i), 'observed'.ljust(ljust_i), 'expected'.ljust(ljust_i), '-2 Sigma'.ljust(ljust_i), '-1 Sigma'.ljust(ljust_i), '+1 Sigma'.ljust(ljust_i), '+2 Sigma'.ljust(ljust_i)
    
    limExpected = 1100
    limObserved = 1100
    for i in range(len(mass)):
        lims = {}
        
        if blind:fobs = open(limitDir+cutString+limitFile.replace(signal+signal+'M1100',signal+signal+'M'+mass_str[i]), 'rU')
        if not blind: fobs = open(limitDir+cutString+limitFile.replace(signal+signal+'M1100',signal+signal+'M'+mass_str[i]).replace('expected','observed'), 'rU')
        linesObs = fobs.readlines()
        fobs.close()
        
        fexp = open(limitDir+cutString+limitFile.replace(signal+signal+'M1100',signal+signal+'M'+mass_str[i]), 'rU')
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
    signExp = "="
    signObs = "="
    if limExpected==1100: signExp = "<"
    if limObserved==1100: signObs = "<"
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
    expected68.SetFillColor(ROOT.kGreen+1)
    expected95 = TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp95Lv,exp95Hv)
    expected95.SetFillColor(ROOT.kOrange)
    #'''
    c4 = TCanvas("c4","Limits", 600, 500)
    c4.SetBottomMargin(0.12)
    c4.SetRightMargin(0.04)
    c4.SetLeftMargin(0.12)
    c4.SetTopMargin(0.08)
    c4.SetLogy()

    expected95.Draw("a3")
    if signal == 'T': expected95.GetYaxis().SetRangeUser(.0005+.00001,2.01)
    else: expected95.GetYaxis().SetRangeUser(.002+.00001,80.1)
    expected95.GetXaxis().SetRangeUser(1100,1800)
    if tempKey=='nB0': expected95.GetYaxis().SetRangeUser(.008+.00001,25.45)   
    expected95.GetXaxis().SetTitle(signal+" mass [GeV]")
    expected95.GetYaxis().SetTitle("#sigma ("+signal+"#bar{"+signal+"})[pb]")
    expected95.GetYaxis().SetTitleOffset(0.9)

    expected68.Draw("3same")
    expected.Draw("same")

    if not blind: observed.Draw("cpsame")
    theory_xsec_gr.SetLineColor(2)
    theory_xsec_gr.SetLineStyle(1)
    theory_xsec_gr.SetLineWidth(2)
    theory_xsec_gr.Draw("3same") 
    theory.SetLineColor(2)
    theory.SetLineStyle(1)
    theory.SetLineWidth(2)
    theory.Draw("same")                                                             

    chLatex = TLatex()
    chLatex.SetNDC()
    chLatex.SetTextSize(0.045)
    chLatex.SetTextAlign(11) # align right
    chString = ''
    if signal == 'T':
	    if 'bW1p0' in tempKey: chString = 'B(bW) = 1.0'
	    #elif 'bW0p5' in tempKey: chString = 'B(bW) = 2B(tH) = 0.5'
	    #elif 'tH0p5' in tempKey: chString = 'B(tH) = B(tZ) = 0.5'
	    elif 'bW0p5' in tempKey: chString = '#bf{#it{#Beta}}(bW) = 2#bf{#it{#Beta}}(tH,tZ) = 0.5'
	    elif 'tH0p5' in tempKey: chString = '#bf{#it{#Beta}}(tH) = #bf{#it{#Beta}}(tZ) = 0.5'
	    elif 'tH1p0' in tempKey: chString = 'B(tH) = 1.0'
	    elif 'tZ1p0' in tempKey: chString = 'B(tZ) = 1.0'
    else:
	    if 'tW1p0' in tempKey: chString = 'B(tW) = 1.0'
	    #elif 'tW0p5' in tempKey: chString = 'B(tW) = 2B(bH) = 0.5'
	    #elif 'bH0p5' in tempKey: chString = 'B(bH) = B(bZ) = 0.5'
	    elif 'tW0p5' in tempKey: chString = '#bf{#it{#Beta}}(tW) = 2#bf{#it{#Beta}}(bH,bZ) = 0.5'
	    elif 'bH0p5' in tempKey: chString = '#bf{#it{#Beta}}(bH) = #bf{#it{#Beta}}(bZ) = 0.5'
	    elif 'bH1p0' in tempKey: chString = 'B(bH) = 1.0'
	    elif 'bZ1p0' in tempKey: chString = 'B(bZ) = 1.0'
    chLatex.DrawLatex(0.16, 0.74, chString)
    if tempKey=='all' or 'minMlbST' in tempKey: chString = '1-lep'
    elif 'dilep' in tempKey: chString = '2-lep'
    elif 'ssdl' in tempKey: chString = 'SS 2-lep'
    elif 'triL' in tempKey: chString = '3-lep'
    elif 'comb123' in tempKey: chString = '1+2+3 lep'
    elif 'DeepAK8' in tempKey: chString = 'DeepAK8'
    else: chString = 'BEST'
    chLatex.DrawLatex(0.16, 0.69, chString)
        
    #latex2 = TLatex()
    #latex2.SetNDC()
    #latex2.SetTextSize(0.04)
    #latex2.SetTextAlign(11) # align right
    #latex2.DrawLatex(0.17,0.96,"CMS "+str(lumiPlot)+" fb^{-1} (13 TeV)");
    #latex2.DrawLatex(0.54, 0.96, "CMS " + str(lumiPlot) + " fb^{-1} (13 TeV)")
    #latex2.DrawLatex(0.58, 0.96, "CMS " + str(lumiPlot) + " fb^{-1} (13 TeV)")

    prelimTex=TLatex()
    prelimTex.SetNDC()
    prelimTex.SetTextAlign(31) # align right
    prelimTex.SetTextFont(42)
    prelimTex.SetTextSize(0.05)
    prelimTex.SetLineWidth(2)
    prelimTex.DrawLatex(0.95,0.94,str(lumiPlot)+" fb^{-1} (13 TeV)")
    
    prelimTex2=TLatex()
    prelimTex2.SetNDC()
    prelimTex2.SetTextFont(61)
    prelimTex2.SetLineWidth(2)
    prelimTex2.SetTextSize(0.08)
    prelimTex2.DrawLatex(0.16,0.82,"CMS")

    #legend = TLegend(.55,.5,.89,.89) # good for BR of 1
    legend = TLegend(.62,.49,.99,.88,"95% CL upper limits") # mixes
    if tempKey=='nB0': legend = TLegend(.62,.31,.99,.61,"95% CL upper limits")
    if not blind: legend.AddEntry(observed , 'Observed', "lp")
    legend.AddEntry(expected, 'Expected', "l")
    legend.AddEntry(expected68, '68% expected', "f")
    legend.AddEntry(expected95, '95% expected', "f")    
    legend.AddEntry(theory_xsec_gr,'',"")
    if signal == 'T': 
	    legend.AddEntry(theory_xsec_gr, 'pp #rightarrow T#bar{T}', 'lf')
    else: 
	    legend.AddEntry(theory_xsec_gr, 'pp #rightarrow B#bar{B}', 'lf')
    legend.SetShadowColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.Draw()
    
    c4.RedrawAxis()
    
    folder = '/uscms_data/d3/escharni/CMSSW_10_2_10/src/singleLepAnalyzer/thetaLimits/'
    outDir=folder+'/plots_Jul19/July_MVA_Update_Round2/'
    #outDir = folder
    if not os.path.exists(outDir): os.system('mkdir -p '+outDir)
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'_'+tempKey+'.root')
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'_'+tempKey+'.pdf')
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'_'+tempKey+'.png')
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'_'+tempKey+'.C')
    #c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'.root')
    #c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'.pdf')
    #c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'.png')
    #c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'.C')
    #'''
    return int(round(limExpected)), int(round(limObserved))

doBRScan = True
BRs={}
BRs['BW']=[0.0,0.50,0.0,1.0,0.0]#,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]#
BRs['TH']=[0.5,0.25,1.0,0.0,0.0]#,0.0,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]#
BRs['TZ']=[0.5,0.25,0.0,0.0,1.0]#,1.0,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]#
nBRconf=len(BRs['BW'])
if not doBRScan: nBRconf=1

tempKeys = ['DeepAK8']#['comb123']#,'isE','isM','nW0','nW1p','nB0','nB1','nB2','nB3p']#
if combination: tempKeys = ['comb1718']

expLims = []
obsLims = []
for tempKey in tempKeys:
	for BRind in range(nBRconf):
		BRconfStr=''
		if doBRScan: 
			if signal=='T': BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
			else: BRconfStr='_tW'+str(BRs['BW'][BRind]).replace('.','p')+'_bZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_bH'+str(BRs['TH'][BRind]).replace('.','p')
		#limitDir='/uscms_data/d3/saj32265/CMSSW_9_4_6_patch1/src/singleLepAnalyzer/thetaLimits/limitsAug18/'
		limitDir='/uscms_data/d3/escharni/CMSSW_10_2_10/src/singleLepAnalyzer/thetaLimits/limitsJul19/templatesSR_July_MVA_Update_Round2/'+discriminant+BRconfStr+'/'
		if signal=='B': limitDir='/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/limitsOct17/templates4CRhtSR_BB_NewEl/'+discriminant+BRconfStr+'/'
		if tempKey=='ssdltest': limitDir='/user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/limitsOct17/templates4CRhtSR_NewEl/'+tempKey+'_bW0p5_tZ0p25_tH0p25/splitLess/'
				
		limitFile='/limits_templates_'+discriminant+'_'+signal+signal+'M1100'+chiral+BRconfStr+'_'+str(lumiStr)+'fb'+isRebinned+'_'+tempKey+'_expected.txt'
		if 'ssdl' in tempKey: limitFile='/limits_Limits_'+signal+signal+'M1100'+chiral+BRconfStr+'_All_LL40_SL35_HT1200_nConst4_expected.txt'
		if tempKey=='comb1718':
			limitDir='/uscms_data/d3/escharni/CMSSW_10_2_10/src/singleLepAnalyzer/thetaLimits/limitsJul19/templatesSR_July_MVA_Update_Round2/'+tempKey+BRconfStr+'/templatesSR_July_MVA_Update_Round2/'
			limitFile='limits_templates_'+discriminant+'_'+signal+signal+'M1100'+chiral+BRconfStr+'_'+str(lumiStr)+'fb'+isRebinned+'_expected.txt'
		try: 		
			expTemp,obsTemp = PlotLimits(limitDir,limitFile,tempKey+BRconfStr)
			expLims.append(expTemp)
			obsLims.append(obsTemp)
		except: 
			expLims.append(-1)
			obsLims.append(-1)
			pass
print "BRs_bW:",BRs['BW']
print "BRs_tH:",BRs['TH']
print "BRs_tZ:",BRs['TZ']
print "Expected:",expLims
print "Observed:",obsLims

