import ROOT as rt
from array import array
import os,sys,math
from math import *
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= "2.3 fb^{-1}"
CMS_lumi.writeExtraText = 0
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref

# 
# Simple example of macro: plot with CMS name and lumi text
#  (this script does not pretend to work in all configurations)
# iPeriod = 1*(0/1 7 TeV) + 2*(0/1 8 TeV)  + 4*(0/1 13 TeV) 
# For instance: 
#               iPeriod = 3 means: 7 TeV + 8 TeV
#               iPeriod = 7 means: 7 TeV + 8 TeV + 13 TeV 
#               iPeriod = 0 means: free form (uses lumi_sqrtS)
# Initiated by: Gautier Hamel de Monchenault (Saclay)
# Translated in Python by: Joshua Hardenbrook (Princeton)
# Updated by:   Dinko Ferencek (Rutgers)
#

iPeriod = 4

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

blind=False
saveKey=''#'_test'
signal = 'X53'
lumiPlot = '2.3'
lumiStr = '2p318'
discriminant='minMlb'

mass_str = ['700','800','900','1000','1100','1200','1300','1400','1500']#,'1600']
theory_xsec = [0.455,0.196,0.0903,0.0440,0.0224,0.0118,0.00639,0.00354,0.00200,0.001148,0.000666,0.000391][:len(mass_str)]#pb
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

theory_xsec_up = [math.sqrt(scale**2+pdf**2)*xsec/100 for xsec,scale,pdf in zip(theory_xsec,scale_up,pdf_up)]
theory_xsec_dn = [math.sqrt(scale**2+pdf**2)*xsec/100 for xsec,scale,pdf in zip(theory_xsec,scale_dn,pdf_dn)]

theory_xsec_v    = rt.TVectorD(len(mass),array('d',theory_xsec))
theory_xsec_up_v = rt.TVectorD(len(mass),array('d',theory_xsec_up))
theory_xsec_dn_v = rt.TVectorD(len(mass),array('d',theory_xsec_dn))      

theory_xsec_gr = rt.TGraphAsymmErrors(rt.TVectorD(len(mass),mass),theory_xsec_v,rt.TVectorD(len(mass),masserr),rt.TVectorD(len(mass),masserr),theory_xsec_dn_v,theory_xsec_up_v)
theory_xsec_gr.SetFillStyle(3001)
theory_xsec_gr.SetFillColor(rt.kRed)
			   
theory = rt.TGraph(len(mass))
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

def PlotLimits(limitDir,limitFile,chiral,tempKey):
    histPrefix=discriminant+'_'+str(lumiStr)+'fb'+chiral
    ljust_i = 10
    print
    print 'mass'.ljust(ljust_i), 'observed'.ljust(ljust_i), 'expected'.ljust(ljust_i), '-2 Sigma'.ljust(ljust_i), '-1 Sigma'.ljust(ljust_i), '+1 Sigma'.ljust(ljust_i), '+2 Sigma'.ljust(ljust_i)
    
    limExpected = 700
    limObserved = 700
    for i in range(len(mass)):
        lims = {}
        
        try:
        	if blind:fobs = open(limitDir+cutString+limitFile.replace(signal+signal+'M700',signal+signal+'M'+mass_str[i]), 'rU')
        	if not blind: fobs = open(limitDir+cutString+limitFile.replace(signal+signal+'M700',signal+signal+'M'+mass_str[i]).replace('expected','observed'), 'rU')
        	linesObs = fobs.readlines()
        	fobs.close()
        	
        	fexp = open(limitDir+cutString+limitFile.replace(signal+signal+'M700',signal+signal+'M'+mass_str[i]), 'rU')
        	linesExp = fexp.readlines()
        	fexp.close()
        except: 
        	print "SKIPPING SIGNAL: "+mass_str[i]
        	continue
        
        lims[-1] = float(linesObs[1].strip().split()[1])
        obs[i] = float(linesObs[1].strip().split()[1])
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
    signExp = "="
    signObs = "="
    if limExpected==700: signExp = "<"
    if limObserved==700: signObs = "<"
    print "Expected lower limit "+signExp,int(round(limExpected)),"GeV"
    print "Observed lower limit "+signObs,int(round(limObserved)),"GeV"
    print

    massv = rt.TVectorD(len(mass),mass)
    expv  = rt.TVectorD(len(mass),exp)
    exp68Hv = rt.TVectorD(len(mass),exp68H)
    exp68Lv = rt.TVectorD(len(mass),exp68L)
    exp95Hv = rt.TVectorD(len(mass),exp95H)
    exp95Lv = rt.TVectorD(len(mass),exp95L)

    obsv = rt.TVectorD(len(mass),obs)
    masserrv = rt.TVectorD(len(mass),masserr)
    obserrv = rt.TVectorD(len(mass),obserr)
    experrv = rt.TVectorD(len(mass),experr)       


    observed = rt.TGraphAsymmErrors(massv,obsv,masserrv,masserrv,obserrv,obserrv)
    observed.SetLineColor(rt.kBlack)
    observed.SetLineWidth(2)
    observed.SetMarkerStyle(20)
    expected = rt.TGraphAsymmErrors(massv,expv,masserrv,masserrv,experrv,experrv)
    expected.SetLineColor(rt.kBlue)
    expected.SetLineWidth(2)
    expected.SetLineStyle(2)
    expected68 = rt.TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp68Lv,exp68Hv)
    expected68.SetFillColor(rt.kGreen+1)
    expected95 = rt.TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp95Lv,exp95Hv)
    expected95.SetFillColor(rt.kOrange)

    canvas = rt.TCanvas("c4","c4",50,50,W,H)
    canvas.SetFillColor(0)
    canvas.SetBorderMode(0)
    canvas.SetFrameFillStyle(0)
    canvas.SetFrameBorderMode(0)
    canvas.SetLeftMargin( L/W )
    canvas.SetRightMargin( R/W )
    canvas.SetTopMargin( T/H )
    canvas.SetBottomMargin( B/H )
    canvas.SetTickx(0)
    canvas.SetTicky(0)
    canvas.SetLogy()

    if signal=='X53':
    	XaxisTitle = "X_{5/3} mass [GeV]"
    	YaxisTitle = "#sigma(_{}X_{5/3}#bar{X}_{5/3})[pb] - "+chiral.replace('left','LH').replace('right','RH')
    else:
		XaxisTitle = signal+" mass [GeV]"
		YaxisTitle = "#sigma("+signal+"#bar{"+signal+"})[pb]"
    
    expected95.Draw("a3")
    expected95.GetYaxis().SetRangeUser(.008+.00001,10.45)
    expected95.GetXaxis().SetRangeUser(700,1500)
    expected95.GetXaxis().SetTitle(XaxisTitle)
    expected95.GetYaxis().SetTitle(YaxisTitle)
    expected95.GetYaxis().SetTitleOffset(1)
		
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
    
    #draw the lumi text on the canvas
    CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)

    legend = rt.TLegend(.37,.69,.94,.89) # top right
    if tempKey=='nB0': legend = rt.TLegend(.32,.42,.92,.62)
    if not blind: legend.AddEntry(observed, "95% CL observed", "lp")
    #legend.AddEntry(expected68, "#pm 1 std. deviation", "f")
    legend.AddEntry(expected68, "#pm 1 s.d.", "f")
    legend.AddEntry(expected, "95% CL expected", "l")
    #legend.AddEntry(expected95, "#pm 2 std. deviation", "f")
    legend.AddEntry(expected95, "#pm 2 s.d.", "f")
    legend.AddEntry(theory_xsec_gr, "Signal Cross Section", "lf")

    legend.SetShadowColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetNColumns(2)
    legend.Draw()
    
    canvas.cd()
    canvas.Update()
    canvas.RedrawAxis()
    frame = canvas.GetFrame()
    frame.Draw()

    folder = '.'
    outDir=folder+'/'+limitDir.split('/')[-3]+'plots'
    if not os.path.exists(outDir): os.system('mkdir '+outDir)
    canvas.SaveAs(outDir+'/LimitPlot_'+histPrefix+'_rebinned_stat'+str(binning).replace('.','p')+saveKey+'_'+tempKey+'.eps')
    canvas.SaveAs(outDir+'/LimitPlot_'+histPrefix+'_rebinned_stat'+str(binning).replace('.','p')+saveKey+'_'+tempKey+'.pdf')
    canvas.SaveAs(outDir+'/LimitPlot_'+histPrefix+'_rebinned_stat'+str(binning).replace('.','p')+saveKey+'_'+tempKey+'.png')
    canvas.SaveAs(outDir+'/LimitPlot_'+histPrefix+'_rebinned_stat'+str(binning).replace('.','p')+saveKey+'_'+tempKey+'.root')
    return int(round(limExpected)), int(round(limObserved))

doBRScan = False
BRs={}
BRs['BW']=[0.50,0.0,0.0,0.0,0.0,0.0,0.0,0.2,0.2,0.2,0.2,0.2,0.4,0.4,0.4,0.4,0.6,0.6,0.6,0.8,0.8,1.0]
BRs['TH']=[0.25,0.0,0.2,0.4,0.6,0.8,1.0,0.0,0.2,0.4,0.6,0.8,0.0,0.2,0.4,0.6,0.0,0.2,0.4,0.0,0.2,0.0]
BRs['TZ']=[0.25,1.0,0.8,0.6,0.4,0.2,0.0,0.8,0.6,0.4,0.2,0.0,0.6,0.4,0.2,0.0,0.4,0.2,0.0,0.2,0.0,0.0]
nBRconf=len(BRs['BW'])
if not doBRScan: nBRconf=1

tempKeys = ['all']#,'isE','isM','nW0','nW1p','nB1','nB2p','nT0','nT1p']
#tempKeys = [item+'_moreToys' for item in tempKeys]
#tempKeys = ['all_moreToys','noJMS','noJMR','noTAU21','noTOPSF','noWTAGsys','noWtTAGsys','noTtbarCRsys','noCRsys','noCRWtTAGsys']
#tempKeys+= ['no_nT0_nW0_nB0']
# tempKeys = ['isE_nT0_nW0_nB0', 'isE_nT0_nW0_nB1', 'isE_nT0_nW0_nB2p', 'isE_nT0_nW1p_nB0', 'isE_nT0_nW1p_nB1', 'isE_nT0_nW1p_nB2p',
#         'isE_nT1p_nW0_nB0','isE_nT1p_nW0_nB1','isE_nT1p_nW0_nB2p','isE_nT1p_nW1p_nB0','isE_nT1p_nW1p_nB1','isE_nT1p_nW1p_nB2p',
#         'isM_nT0_nW0_nB0', 'isM_nT0_nW0_nB1', 'isM_nT0_nW0_nB2p', 'isM_nT0_nW1p_nB0', 'isM_nT0_nW1p_nB1', 'isM_nT0_nW1p_nB2p',
#         'isM_nT1p_nW0_nB0','isM_nT1p_nW0_nB1','isM_nT1p_nW0_nB2p','isM_nT1p_nW1p_nB0','isM_nT1p_nW1p_nB1','isM_nT1p_nW1p_nB2p',
#         ]
# dirs = {'ttag_Inclusive':'templates_minMlb_noJSF_tau21Fix2_2016_10_6',#_lessToys',
# 		'ttag_HTbins':'templates_minMlb_noJSF_2016_6_22_WJetsHTbins',
# 		'ttag_HTbinsJSF':'templates_minMlb_withJSF_2016_6_22',
# 		'no_ttag_Inclusive':'templates_minMlb_noJSF_notTag_2016_6_22',
# 		'no_ttag_HTbins':'templates_minMlb_noJSF_notTag_2016_6_22_WJetsHTbins',
# 		'no_ttag_HTbinsJSF':'templates_minMlb_withJSF_notTag_2016_6_22',
# 		}
cutString='lep80_MET100_NJets4_DR1_1jet200_2jet90'
dirs = {
		'ttag':'templates_minMlb_noJSF_tau21Fix1_2016_10_8',
		'ttag_noCRunc':'templates_minMlb_noJSF_tau21Fix1_2016_10_8_noCRuncerts',
		#'ttag':'templates_minMlb_2016_10_28_noCRuncerts',
		}
dirKeyList = ['ttag_noCRunc']#,'ttag']
binnings = ['0p15']#,'0p25']

expLimsL = {}
obsLimsL = {}
expLimsR = {}
obsLimsR = {}
for dirKey in dirKeyList:
	dir = dirs[dirKey]
	expLimsL[dirKey] = {}
	obsLimsL[dirKey] = {}
	expLimsR[dirKey] = {}
	obsLimsR[dirKey] = {}
	for binning in binnings:
		expLimsL[dirKey][binning] = []
		obsLimsL[dirKey][binning] = []
		expLimsR[dirKey][binning] = []
		obsLimsR[dirKey][binning] = []
		for tempKey in tempKeys:
			for BRind in range(nBRconf):
				BRconfStr=''
				if doBRScan: BRconfStr='_bW'+str(BRs['BW'][BRind]).replace('.','p')+'_tZ'+str(BRs['TZ'][BRind]).replace('.','p')+'_tH'+str(BRs['TH'][BRind]).replace('.','p')
				limitDir='/user_data/ssagir/x53x53_limits_2015/'+dir+'/'+tempKey+BRconfStr+'/'
				limitFile='/limits_templates_'+discriminant+'_'+signal+signal+'M700left'+BRconfStr+'_'+str(lumiStr)+'fb_rebinned_stat'+str(binning).replace('.','p')+'_expected.txt'	
				print limitDir+cutString+limitFile
				expTemp,obsTemp = PlotLimits(limitDir,limitFile,'left',tempKey+BRconfStr)
				expLimsL[dirKey][binning].append(expTemp)
				obsLimsL[dirKey][binning].append(obsTemp)
				limitFile='/limits_templates_'+discriminant+'_'+signal+signal+'M700right'+BRconfStr+'_'+str(lumiStr)+'fb_rebinned_stat'+str(binning).replace('.','p')+'_expected.txt'	
				expTemp,obsTemp = PlotLimits(limitDir,limitFile,'right',tempKey+BRconfStr)
				expLimsR[dirKey][binning].append(expTemp)
				obsLimsR[dirKey][binning].append(obsTemp)
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
			print 'LH_'+dirKey+'_'+binning,
			print 'RH_'+dirKey+'_'+binning,
	print
	print "Expected:"
	for binning in binnings:
		for dirKey in dirKeyList: 
			print expLimsL[dirKey][binning][ind],
			print expLimsR[dirKey][binning][ind],
	print
	print "Observed:"
	for binning in binnings:
		for dirKey in dirKeyList: 
			print obsLimsL[dirKey][binning][ind],
			print obsLimsR[dirKey][binning][ind],
	print


