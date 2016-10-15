from ROOT import *
from array import array
import math
from math import *
import os,sys

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

lumiPlot = '1.28'
lumiStr = '1'
spin='left'
discriminant='ST_Cat2'
histPrefix=discriminant+'_'+str(lumiStr)+'fb_'+spin+'_'
blind=False
stat=''#0.75#9999999
isRebinned='rebinnedCustom5'+str(stat).replace('.','p')#'_rebinned'
templateDir='/user_data/ssagir/optimization_x53x53_allSystematics/rebinnedStat0p75/limits_2015_11_12_16_14_50/'
cutString='lep80_MET100_leadJet200_subLeadJet90_leadbJet0_ST0_HT0_NJets6_NBJets1_3rdJet0_4thJet0_5thJet0_WJet0' # best ST cuts w/o categorization
LH700file='/limits_templates_'+discriminant+'_T53T53M700'+spin+'_'+str(lumiStr)+'fb_'+cutString+isRebinned+'_expected.txt'	

def PlotLimits():

    mass = array('d', [700,800,900,1000,1100,1200,1300,1400,1500,1600])
    masserr = array('d', [0,0,0,0,0,0,0,0,0,0])

    mass_str = ['700','800','900','1000','1100','1200','1300','1400','1500','1600']
    
    sigma3   =array('d',[0 for i in range(len(mass))])
    sigma3err   =array('d',[0 for i in range(len(mass))])
    sigma5   =array('d',[0 for i in range(len(mass))])
    sigma5err   =array('d',[0 for i in range(len(mass))])
    exp   =array('d',[0 for i in range(len(mass))])
    test  =array('d',[0 for i in range(len(mass))])
    experr=array('d',[0 for i in range(len(mass))])
    obs   =array('d',[0 for i in range(len(mass))])
    obserr=array('d',[0 for i in range(len(mass))]) 
    exp68H=array('d',[0 for i in range(len(mass))])
    exp68L=array('d',[0 for i in range(len(mass))])
    exp95H=array('d',[0 for i in range(len(mass))])
    exp95L=array('d',[0 for i in range(len(mass))])

    #xsec = array('d', [0.064,0.036,0.020,0.012,0.007,0.004,0.003,0.002,0.001,0.0007]) #xsec*BR
    xsec = array('d', [1,1,1,1,1,1,1,1,1,1])
    #xsec = array('d', [0.305,0.170,0.097,0.057,0.034,0.021,0.013,0.008,0.005,0.003]) #xsec -- BR=100%=1
    theory_br = [.1285,.1285,.1285,.1285,.1285,.1285,.1285,.1285,.1285,.1285]
    if spin=='right':theory_xsec  = [0.442,0.190,0.0877,0.0427,0.0217,0.0114,0.00618,0.00342,0.00193,0.00111]
    elif spin=='left':theory_xsec = [0.442,0.190,0.0877,0.0427,0.0217,0.0114,0.00618,0.00342,0.00193,0.00111]
    else: print "Please enter left or right"
                   
    theory = TGraph(len(theory_xsec))
    for i in range(len(theory_xsec)):
        theory.SetPoint(i, mass[i], theory_xsec[i])
    
    ljust_i = 10
    print
    print 'mass'.ljust(ljust_i), 'observed'.ljust(ljust_i), 'expected'.ljust(ljust_i), '-2 Sigma'.ljust(ljust_i), '-1 Sigma'.ljust(ljust_i), '+1 Sigma'.ljust(ljust_i), '+2 Sigma'.ljust(ljust_i)
	
	
    for i in range(len(mass)):
        lims = {}

        if blind:fobs = open(templateDir+cutString+LH700file.replace('T53T53M700','T53T53M'+mass_str[i]), 'rU')
        if not blind: fobs = open(templateDir+cutString+LH700file.replace('T53T53M700','T53T53M'+mass_str[i]).replace('expected','observed'), 'rU')
        linesObs = fobs.readlines()
        fobs.close()
        
        fexp = open(templateDir+cutString+LH700file.replace('T53T53M700','T53T53M'+mass_str[i]), 'rU')
        linesExp = fexp.readlines()
        fexp.close()
        
        f3sigma = open(templateDir+cutString+LH700file.replace('T53T53M700','T53T53M'+mass_str[i]).replace('limits_','3sigmaSignif_').replace('_expected',''), 'rU')
        lines3sigma = f3sigma.readlines()
        f3sigma.close()
        
        f5sigma = open(templateDir+cutString+LH700file.replace('T53T53M700','T53T53M'+mass_str[i]).replace('limits_','5sigmaSignif_').replace('_expected',''), 'rU')
        lines5sigma = f5sigma.readlines()
        f5sigma.close()
        
        sigma3[i] = float(lines3sigma[1].strip().split()[1])
        sigma5[i] = float(lines5sigma[1].strip().split()[1])
        print sigma3[i],sigma5[i]
        sigma3err[i] = 0
        sigma5err[i] = 0
        
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

        round_i = 5
        print str(mass[i]).ljust(ljust_i), str(round(lims[-1],round_i)).ljust(ljust_i), str(round(lims[.5],round_i)).ljust(ljust_i), str(round(lims[.025],round_i)).ljust(ljust_i), str(round(lims[.16],round_i)).ljust(ljust_i), str(round(lims[.84],round_i)).ljust(ljust_i), str(round(lims[.975],round_i)).ljust(ljust_i)
    print
    print exp, obs, test

    print mass,exp,masserr,exp68L,exp95H
    massv = TVectorD(len(mass),mass)
    expv = TVectorD(len(mass),exp)
    exp68Hv = TVectorD(len(mass),exp68H)
    exp68Lv = TVectorD(len(mass),exp68L)
    exp95Hv = TVectorD(len(mass),exp95H)
    exp95Lv = TVectorD(len(mass),exp95L)
    testv = TVectorD(len(mass),test)
    #exp95Lv = TVectorD(len(mass),exp68L)

    sigma3v = TVectorD(len(mass),sigma3)
    sigma5v = TVectorD(len(mass),sigma5)
    sigma3errv = TVectorD(len(mass),sigma3err)
    sigma5errv = TVectorD(len(mass),sigma5err)
    
    obsv = TVectorD(len(mass),obs)
    masserrv = TVectorD(len(mass),masserr)
    obserrv = TVectorD(len(mass),obserr)
    experrv = TVectorD(len(mass),experr)       


    sigma3gr = TGraphAsymmErrors(massv,sigma3v,masserrv,masserrv,sigma3errv,sigma3errv)
    sigma3gr.SetLineColor(ROOT.kBlue)
    sigma3gr.SetLineWidth(2)
    sigma3gr.SetMarkerStyle(20)
    sigma5gr = TGraphAsymmErrors(massv,sigma5v,masserrv,masserrv,sigma5errv,sigma5errv)
    sigma5gr.SetLineColor(ROOT.kGreen)
    sigma5gr.SetLineWidth(2)
    sigma5gr.SetMarkerStyle(20)
    
    observed = TGraphAsymmErrors(massv,obsv,masserrv,masserrv,obserrv,obserrv)
    observed.SetLineColor(ROOT.kBlack)
    observed.SetLineWidth(2)
    observed.SetMarkerStyle(20)
    expected = TGraphAsymmErrors(massv,expv,masserrv,masserrv,experrv,experrv)
    expected.SetLineColor(ROOT.kRed)
    expected.SetLineWidth(2)
    expected.SetMarkerStyle(20)
    ## I'm confused, somehow this is the way that works
    expected68 = TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp68Lv,exp68Hv)
    #expected68 = TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp68Lv,exp68Hv)
    expected68.SetFillColor(ROOT.kGreen)
    expected95 = TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp95Lv,exp95Hv)
    #expected95 = TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp95Lv,exp95Hv)
    expected95.SetFillColor(ROOT.kYellow)

    c4 = TCanvas("c4","Limits", 1000, 800)
    c4.SetBottomMargin(0.15)
    c4.SetRightMargin(0.06)
    c4.SetLogy()

    expected.Draw("AL")
    expected.GetYaxis().SetRangeUser(.003+.00001,1.65)
    expected.GetXaxis().SetRangeUser(700,1300)
    expected.GetXaxis().SetTitle("X_{5/3} mass [GeV]")
    expected.GetYaxis().SetTitle("#sigma (X_{5/3}#bar{X}_{5/3})[pb]")

    #expected68.Draw("3same")
    #expected.Draw("same")
    sigma3gr.Draw("same")
    sigma5gr.Draw("same")

    #observed.Draw("cpsame")
    theory.SetLineColor(1)
    theory.SetMarkerStyle(20)
    theory.SetLineWidth(2)
    theory.Draw("same")


    '''
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.04)
    latex.SetTextAlign(11) # align right
    latex.DrawLatex(0.12, 0.95, "CMS Preliminary");
    '''

    '''
    latex.SetTextSize(0.5*c4.GetTopMargin())
    latex.SetTextFont(52)
    latex.SetTextAlign(11)
    latex.DrawLatex(0.20, 0.8, "Preliminary");
    '''
                                                                     
        
    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.03)
    latex2.SetTextAlign(11) # align right
    latex2.DrawLatex(0.58, 0.96, "CMS Preliminary, " + str(lumiPlot) + " fb^{-1} (13 TeV)")
    #latex2.DrawLatex(0.58, 0.95, "CMS Simulation, " + str(lumiPlot) + " fb^{   -1} (13 TeV)")

    latex4 = TLatex()
    latex4.SetNDC()
    latex4.SetTextSize(0.04)
    latex4.SetTextAlign(31) # align right
    #latex4.DrawLatex(0.80, 0.87, "e+jets N_{b tags} #geq 1 ");


    #legend = TLegend(.2,.6,.5,.9).2,.2,.5,.5
    legend = TLegend(.2,.2,.5,.5)    
    #legend . AddEntry(observed , '95% CL observed', "lp")
    legend . AddEntry(expected , '95% CL expected', "l")
    legend . AddEntry(sigma3gr , '3#sigma', "l")
    legend . AddEntry(sigma5gr , '5#sigma', "l")
    #legend . AddEntry(expected68 , '#pm 1#sigma expected', "f")
    #legend . AddEntry(expected95 , '#pm 2#sigma expected', "f")
    legend . AddEntry(theory, 'Signal Cross Section', 'l')

    legend.SetShadowColor(0);
    legend.SetFillColor(0);
    legend.SetLineColor(0);
    legend.Draw()
    
    c4.RedrawAxis()

    folder = '.'
    if not os.path.exists(folder+'/'+templateDir.split('/')[-2]+'plots'): os.system('mkdir '+folder+'/'+templateDir.split('/')[-2]+'plots')
    c4.SaveAs(folder+'/'+templateDir.split('/')[-2]+'plots/SignificancePlot_'+histPrefix+cutString+isRebinned+'.root')
    c4.SaveAs(folder+'/'+templateDir.split('/')[-2]+'plots/SignificancePlot_'+histPrefix+cutString+isRebinned+'.pdf')
    c4.SaveAs(folder+'/'+templateDir.split('/')[-2]+'plots/SignificancePlot_'+histPrefix+cutString+isRebinned+'.png')

PlotLimits()

