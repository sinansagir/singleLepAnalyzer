from ROOT import *
from array import array
import math
from math import *
import os,sys

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

blind=False
saveKey=''
signal = 'T'
lumiPlot = '2.3'
lumiStr = '2p263'
chiral=''#'right'
discriminant='minMlb'
histPrefix=discriminant+'_'+str(lumiStr)+'fb'+chiral
stat=''#0.75
isRebinned='_rebinned'+str(stat).replace('.','p')
tempKey='all_2p318invfb'
#limitDir='/user_data/ssagir/limits/limits'+tempKey+'_minMlb_withShapes_2016_1_27_19_9_47/'
limitDir='/user_data/ssagir/limits/templates_minMlb_tau21LT0p6_tptp_2016_2_23/'+tempKey+'/'
cutString='lep40_MET75_1jet300_2jet150_NJets3_NBJets0_3jet100_4jet0_5jet0_DR1_1Wjet0_1bjet0_HT0_ST0_minMlb0'
limitFile='/limits_templates_'+discriminant+'_'+signal+signal+'M700'+chiral+'_'+str(lumiStr)+'fb'+isRebinned+'_expected.txt'	

mass = array('d', [700,800,900,1000,1100,1200,1300])#,1400,1500,1600])
masserr = array('d', [0,0,0,0,0,0,0])#,0,0,0])
mass_str = ['700','800','900','1000','1100','1200','1300']#,'1400','1500','1600']

exp   =array('d',[0 for i in range(len(mass))])
experr=array('d',[0 for i in range(len(mass))])
obs   =array('d',[0 for i in range(len(mass))])
obserr=array('d',[0 for i in range(len(mass))]) 
exp68H=array('d',[0 for i in range(len(mass))])
exp68L=array('d',[0 for i in range(len(mass))])
exp95H=array('d',[0 for i in range(len(mass))])
exp95L=array('d',[0 for i in range(len(mass))])

xsec = array('d', [1,1,1,1,1,1,1])#,1,1,1])
theory_br = [.1285,.1285,.1285,.1285,.1285,.1285,.1285]#,.1285,.1285,.1285]
if chiral=='right':theory_xsec  = [0.442,0.190,0.0877,0.0427,0.0217,0.0114,0.00618,0.00342,0.00193,0.00111]
elif chiral=='left':theory_xsec = [0.442,0.190,0.0877,0.0427,0.0217,0.0114,0.00618,0.00342,0.00193,0.00111]
else: print "Please enter left or right"
theory_xsec = [0.455,0.196,0.0903,0.0440,0.0224,0.0118,0.00639]#,0.00354,0.00200,0.001148,0.000666,0.000391]
			   
theory = TGraph(len(theory_xsec))
for i in range(len(theory_xsec)):
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

def getSensitivity2(index, exp):
	x1=mass[index-1]
	x3=mass[index-1]
	x2=mass[index]
	x4=mass[index]
	y1=theory_xsec[index-1]
	y2=theory_xsec[index]
	y3=exp[index-1]
	y4=exp[index]
	massintersect=((x1*y2-y1*x2)*(x3-x4)-(x1-x2)*(x3*y4-y3*x4))/((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
	limitintersect=1 # just a dummy number, we don't need this!
	return massintersect, limitintersect

def PlotLimits():
    ljust_i = 10
    print
    print 'mass'.ljust(ljust_i), 'observed'.ljust(ljust_i), 'expected'.ljust(ljust_i), '-2 Sigma'.ljust(ljust_i), '-1 Sigma'.ljust(ljust_i), '+1 Sigma'.ljust(ljust_i), '+2 Sigma'.ljust(ljust_i)
    
    limExpected = 700
    limObserved = 700
    for i in range(len(mass)):
        lims = {}
        
        if blind:fobs = open(limitDir+cutString+limitFile.replace(signal+signal+'M700',signal+signal+'M'+mass_str[i]), 'rU')
        if not blind: fobs = open(limitDir+cutString+limitFile.replace(signal+signal+'M700',signal+signal+'M'+mass_str[i]).replace('expected','observed'), 'rU')
        linesObs = fobs.readlines()
        fobs.close()
        
        fexp = open(limitDir+cutString+limitFile.replace(signal+signal+'M700',signal+signal+'M'+mass_str[i]), 'rU')
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
    if limExpected==700: signExp = "<"
    if limObserved==700: signObs = "<"
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
    ## I'm confused, somehow this is the way that works
    expected68 = TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp68Lv,exp68Hv)
    expected68.SetFillColor(ROOT.kGreen)
    expected95 = TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp95Lv,exp95Hv)
    expected95.SetFillColor(ROOT.kYellow)

    c4 = TCanvas("c4","Limits", 1000, 800)
    c4.SetBottomMargin(0.15)
    c4.SetRightMargin(0.06)
    c4.SetLogy()

    expected95.Draw("a3")
    expected95.GetYaxis().SetRangeUser(.008+.00001,10.45)
    expected95.GetXaxis().SetRangeUser(700,1300)
    if tempKey=='nB0': expected95.GetYaxis().SetRangeUser(.008+.00001,25.45)   
    expected95.GetXaxis().SetTitle(signal+" mass [GeV]")
    expected95.GetYaxis().SetTitle("#sigma ("+signal+"#bar{"+signal+"})[pb]")

    expected68.Draw("3same")
    expected.Draw("same")

    if not blind: observed.Draw("cpsame")
    theory.SetLineColor(2)
    theory.SetLineStyle(2)
    theory.SetLineWidth(2)
    theory.Draw("same")                                                              
        
    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.03)
    latex2.SetTextAlign(11) # align right
    latex2.DrawLatex(0.58, 0.96, "CMS Preliminary, " + str(lumiPlot) + " fb^{-1} (13 TeV)")

    latex4 = TLatex()
    latex4.SetNDC()
    latex4.SetTextSize(0.06)
    latex4.SetTextAlign(31) # align right
    if chiral=='left': latex4.DrawLatex(0.40, 0.82, "LH")
    if chiral=='right': latex4.DrawLatex(0.40, 0.82, "RH")

    legend = TLegend(.62,.62,.92,.92) # top right
    if tempKey=='nB0': legend = TLegend(.62,.32,.92,.62)
    if not blind: legend.AddEntry(observed , '95% CL observed', "lp")
    legend.AddEntry(expected, '95% CL expected', "l")
    legend.AddEntry(expected68, '#pm 1#sigma expected', "f")
    legend.AddEntry(expected95, '#pm 2#sigma expected', "f")
    legend.AddEntry(theory, 'Signal Cross Section', 'l')

    legend.SetShadowColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.Draw()
    
    c4.RedrawAxis()

    folder = '.'
    outDir=folder+'/'+limitDir.split('/')[-3]+'plots'
    if not os.path.exists(outDir): os.system('mkdir '+outDir)
    #outDir+='/'+limitDir.split('/')[-2]
    #if not os.path.exists(outDir): os.system('mkdir '+outDir)
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'_'+tempKey+'.root')
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'_'+tempKey+'.pdf')
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'_'+tempKey+'.png')
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+isRebinned+saveKey+'_'+tempKey+'.C')
#     if not os.path.exists(folder+'/'+limitDir.split('/')[-2]+'plots'): os.system('mkdir '+folder+'/'+limitDir.split('/')[-2]+'plots')
#     c4.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/LimitPlot_'+histPrefix+isRebinned+saveKey+'.root')
#     c4.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/LimitPlot_'+histPrefix+isRebinned+saveKey+'.pdf')
#     c4.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/LimitPlot_'+histPrefix+isRebinned+saveKey+'.png')
#     c4.SaveAs(folder+'/'+limitDir.split('/')[-2]+'plots/LimitPlot_'+histPrefix+isRebinned+saveKey+'.C')

PlotLimits()

