#!/usr/bin/python

import os,sys,time,math,json,itertools
from array import array
import ROOT as rt
parent = os.path.dirname(os.getcwd())
thisdir= os.path.dirname(os.getcwd()+'/')
sys.path.append(parent)
import CMS_lumi, tdrstyle

rt.gROOT.SetBatch(1)

blind=True
chiral = 'LH'
year = 'R17'
signal = 'X53'
if   year=='R16': lumi=35.9 #for plots
elif year=='R17': lumi=41.5 #for plots
elif year=='R18': lumi=59.97 #for plots

if chiral == 'RH': 
	mass_str = ['900','1000','1100','1200','1300','1400','1500','1600','1700']
if chiral == 'LH':
	if   year == 'R17': mass_str = ['1100','1200','1400','1700']
	elif year == 'R18': mass_str = ['1100','1200','1400','1500','1700']
theory_xsec_dicts = {
'800':0.196,    '800su':1.9, '800sd':1.8, '800pu':3.9, '800pd':3.7,
'900':0.0903,   '900su':1.9, '900sd':1.7, '900pu':4.1, '900pd':3.9,
'1000':0.0440,  '1000su':1.8,'1000sd':1.6,'1000pu':4.4,'1000pd':4.0,
'1100':0.0224,  '1100su':1.8,'1100sd':1.6,'1100pu':4.7,'1100pd':4.2,
'1200':0.0118,  '1200su':1.8,'1200sd':1.5,'1200pu':5.1,'1200pd':4.5,
'1300':0.00639, '1300su':1.7,'1300sd':1.5,'1300pu':5.6,'1300pd':4.8,
'1400':0.00354, '1400su':1.8,'1400sd':1.5,'1400pu':6.1,'1400pd':5.2,
'1500':0.00200, '1500su':1.7,'1500sd':1.5,'1500pu':6.7,'1500pd':5.6,
'1600':0.001148,'1600su':1.6,'1600sd':1.5,'1600pu':7.0,'1600pd':6.1,
'1700':0.000666,'1700su':1.7,'1700sd':1.5,'1700pu':8.0,'1700pd':6.6,
'1800':0.000391,'1800su':1.7,'1800sd':1.5,'1800pu':9.0,'1800pd':7.2,
}
theory_xsec = [theory_xsec_dicts[item] for item in mass_str]
scale_up = [theory_xsec_dicts[item+'su'] for item in mass_str]#%
scale_dn = [theory_xsec_dicts[item+'sd'] for item in mass_str]#%
pdf_up   = [theory_xsec_dicts[item+'pu'] for item in mass_str]#%
pdf_dn   = [theory_xsec_dicts[item+'pd'] for item in mass_str]#%

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

theory_xsec_up = [math.sqrt(scale**2+pdf**2)*x_sec/100 for x_sec,scale,pdf in zip(theory_xsec,scale_up,pdf_up)]
theory_xsec_dn = [math.sqrt(scale**2+pdf**2)*x_sec/100 for x_sec,scale,pdf in zip(theory_xsec,scale_dn,pdf_dn)]

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

#set the tdr style
tdrstyle.setTDRStyle()

#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.lumi_7TeV = "4.8 fb^{-1}"
CMS_lumi.lumi_8TeV = "18.3 fb^{-1}"
CMS_lumi.lumi_13TeV= str(lumi)+" fb^{-1}"
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "13 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600; 
W_ref = 800; 
W = W_ref
H  = H_ref

iPeriod = 4 #see CMS_lumi.py module for usage!

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref 
L = 0.12*W_ref
R = 0.04*W_ref

def PlotLimits(json_file,chiral,binning,saveKey):
    ljust_i = 10
    print
    print 'mass'.ljust(ljust_i), 'expected'.ljust(ljust_i), '-2 Sigma'.ljust(ljust_i), '-1 Sigma'.ljust(ljust_i), '+1 Sigma'.ljust(ljust_i), '+2 Sigma'.ljust(ljust_i)
 
    json_data=open(json_file)
    data_lims = json.load(json_data)
    json_data.close()
        
    limExpected = 700
    limObserved = 700
    for i in range(len(mass)):
        lims = {}
        
        if not blind:
            lims[-1] = data_lims[str(mass[i])]['obs']*theory_xsec[i]
            obs[i] = data_lims[str(mass[i])]['obs']*theory_xsec[i]
            obserr[i] = 0
        
        lims[.5] = data_lims[str(mass[i])]['exp0']*theory_xsec[i]
        exp[i] = data_lims[str(mass[i])]['exp0']*theory_xsec[i]
        experr[i] = 0
        lims[.16] = data_lims[str(mass[i])]['exp-1']*theory_xsec[i]
        exp68L[i] = data_lims[str(mass[i])]['exp-1']*theory_xsec[i]
        lims[.84] = data_lims[str(mass[i])]['exp+1']*theory_xsec[i]
        exp68H[i] = data_lims[str(mass[i])]['exp+1']*theory_xsec[i]
        lims[.025] = data_lims[str(mass[i])]['exp-2']*theory_xsec[i]
        exp95L[i] = data_lims[str(mass[i])]['exp-2']*theory_xsec[i]
        lims[.975] = data_lims[str(mass[i])]['exp+2']*theory_xsec[i]
        exp95H[i] = data_lims[str(mass[i])]['exp+2']*theory_xsec[i]
    
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
        print str(mass[i]).ljust(ljust_i), str(round(lims[.5],round_i)).ljust(ljust_i), str(round(lims[.025],round_i)).ljust(ljust_i), str(round(lims[.16],round_i)).ljust(ljust_i), str(round(lims[.84],round_i)).ljust(ljust_i), str(round(lims[.975],round_i)).ljust(ljust_i)
    print
    signExp = "="
    signObs = "="
    if limExpected==700: signExp = "<"
    if limObserved==700: signObs = "<"
    print "Expected lower limit "+signExp,int(round(limExpected)),"GeV"
    print "Observed lower limit "+signObs,int(round(limObserved)),"GeV"
    print

    massv = rt.TVectorD(len(mass),mass)
    expv = rt.TVectorD(len(mass),exp)
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

    expv.Print()
    massv.Print()
    canv = rt.TCanvas("canv","canv",50,50,W,H)
    canv.SetFillColor(0)
    canv.SetBorderMode(0)
    canv.SetFrameFillStyle(0)
    canv.SetFrameBorderMode(0)
    canv.SetLeftMargin( L/W )
    canv.SetRightMargin( R/W )
    canv.SetTopMargin( T/H )
    canv.SetBottomMargin( B/H )
    #canv.SetTickx(0)
    #canv.SetTicky(0)
    canv.SetLogy()

    if signal=='X53':
    	XaxisTitle = "X_{5/3} mass [GeV]"
    	#YaxisTitle = "#sigma(_{}X_{5/3}#bar{X}_{5/3}) [pb] - "+chiral.replace('left','LH').replace('right','RH')
    	YaxisTitle = "#sigma(_{}X_{5/3}#bar{X}_{5/3}) [pb]"
    else:
		XaxisTitle = signal+" mass [GeV]"
		YaxisTitle = "#sigma("+signal+"#bar{"+signal+"}) [pb]"
    
    expected95.Draw("a3")
    expected95.GetYaxis().SetRangeUser(.0008+.00001,1.45)#.001+.00001,1.45)
    expected95.GetXaxis().SetRangeUser(900,1700)#mass[0],mass[-1])
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
    CMS_lumi.CMS_lumi(canv, iPeriod, iPos)

    #legend = rt.TLegend(.32,.72,.92,.92) # top right
    legend = rt.TLegend(.37,.69,.94,.89) # top right
    if not blind: legend.AddEntry(observed, "95% CL observed", "lp")
    legend.AddEntry(expected68, '#pm 1#sigma expected', "f")
    legend.AddEntry(expected, "Median expected", "l")
    legend.AddEntry(expected95, '#pm 2#sigma expected', "f")
    legend.AddEntry(theory_xsec_gr, "Signal cross section", "lf")

    legend.SetShadowColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetNColumns(2)
    legend.Draw()

    chiralText = rt.TLatex()
    chiralText.SetNDC()
    chiralText.SetTextSize(0.06)
    chiralText.SetTextAlign(21) # align center
    thetext = "X_{5/3}#bar{X}_{5/3} - "+chiral.replace('left','LH').replace('right','RH')
    if signal=='X53': chiralText.DrawLatex(0.76, 0.56, thetext)
        
    canv.cd()
    canv.Update()
    canv.RedrawAxis()
    frame = canv.GetFrame()
    frame.Draw()

    folder = '.'
    outDir=folder+'/'+json_file.split('/')[-2]+'plots'+'/'
    if not os.path.exists(outDir): os.system('mkdir '+outDir)
    plotName = 'LimitPlot_'+str(lumi).replace('.','p')+'fb_'+chiral+saveKey
    canv.SaveAs(outDir+'/'+plotName+'.eps')
    canv.SaveAs(outDir+'/'+plotName+'.pdf')
    canv.SaveAs(outDir+'/'+plotName+'.png')
    return int(round(limExpected)), int(round(limObserved))

print "=========>>>>>>>>>>> X53X53_LH"
#expLim,obsLim = PlotLimits('LIMITS_LH/limits_isSR_isE.json','LH','0p2','_isE')
#expLim,obsLim = PlotLimits('LIMITS_LH/limits_isSR_isM.json','LH','0p2','_isM')
#expLim,obsLim = PlotLimits('LIMITS_LH/limits_cmb.json','LH','0p2','_all')
print "=========>>>>>>>>>>> X53X53_RH"
#expLim,obsLim = PlotLimits('LIMITS_RH/limits_isSR_isE.json','RH','0p2','_isE')
#expLim,obsLim = PlotLimits('LIMITS_RH/limits_isSR_isM.json','RH','0p2','_isM')
expLim,obsLim = PlotLimits('./limits_'+year+'_211018_'+chiral+'_HT/limits_cmb.json',chiral,'','')


