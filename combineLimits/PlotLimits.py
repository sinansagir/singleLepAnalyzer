from ROOT import *
from array import array
import os,sys,math,json

gROOT.SetBatch(1)

from tdrStyle import *
setTDRStyle()

blind=False
signal = 'X53'
lumiPlot = '2.3'
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

theory_xsec_up = [math.sqrt(scale**2+pdf**2)*x_sec/100 for x_sec,scale,pdf in zip(theory_xsec,scale_up,pdf_up)]
theory_xsec_dn = [math.sqrt(scale**2+pdf**2)*x_sec/100 for x_sec,scale,pdf in zip(theory_xsec,scale_dn,pdf_dn)]

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

def PlotLimits(json_file,chiral,binning,saveKey):
    ljust_i = 10
    print
    print 'mass'.ljust(ljust_i), 'observed'.ljust(ljust_i), 'expected'.ljust(ljust_i), '-2 Sigma'.ljust(ljust_i), '-1 Sigma'.ljust(ljust_i), '+1 Sigma'.ljust(ljust_i), '+2 Sigma'.ljust(ljust_i)
    
    json_data=open(json_file)
    data_lims = json.load(json_data)
    json_data.close()
        
    limExpected = 700
    limObserved = 700
    for i in range(len(mass)):
        lims = {}
        
        lims[-1] = data_lims[str(mass[i])]['obs']
        obs[i] = data_lims[str(mass[i])]['obs']
        obserr[i] = 0
        
        lims[.5] = data_lims[str(mass[i])]['exp0']
        exp[i] = data_lims[str(mass[i])]['exp0']
        experr[i] = 0
        lims[.16] = data_lims[str(mass[i])]['exp-1']
        exp68L[i] = data_lims[str(mass[i])]['exp-1']
        lims[.84] = data_lims[str(mass[i])]['exp+1']
        exp68H[i] = data_lims[str(mass[i])]['exp+1']
        lims[.025] = data_lims[str(mass[i])]['exp-2']
        exp95L[i] = data_lims[str(mass[i])]['exp-2']
        lims[.975] = data_lims[str(mass[i])]['exp+2']
        exp95H[i] = data_lims[str(mass[i])]['exp+2']
    
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
    print "Expected lower limit %s%i GeV (%s,%s,%s,%s)" %(signExp,int(round(limExpected)),json_file,chiral,binning,saveKey)
    if not blind: print "Observed lower limit %s%i GeV" %(signObs,int(round(limObserved)))
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
    expected95.GetYaxis().SetRangeUser(.008+.00001,10.45)
    expected95.GetXaxis().SetRangeUser(700,1500)
    if signal=='X53':
    	expected95.GetXaxis().SetTitle("X_{5/3} mass [GeV]")
    	expected95.GetYaxis().SetTitle("#sigma(X_{5/3}#bar{X}_{5/3})[pb] - "+chiral.replace('left','LH').replace('right','RH'))
    else:
		expected95.GetXaxis().SetTitle(signal+" mass [GeV]")
		expected95.GetYaxis().SetTitle("#sigma ("+signal+"#bar{"+signal+"})[pb]")
		
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
        
    latex2 = TLatex()
    latex2.SetNDC()
    latex2.SetTextSize(0.03)
    latex2.SetTextAlign(11) # align right
    latex2.DrawLatex(0.58, 0.96, "CMS Preliminary, " + str(lumiPlot) + " fb^{-1} (13 TeV)")

    latex4 = TLatex()
    latex4.SetNDC()
    latex4.SetTextSize(0.06)
    latex4.SetTextAlign(31) # align right

    legend = TLegend(.32,.72,.92,.92) # top right
    if not blind: legend.AddEntry(observed , '95% CL observed', "lp")
    legend.AddEntry(expected68, '#pm 1#sigma expected', "f")
    legend.AddEntry(expected, '95% CL expected', "l")
    legend.AddEntry(expected95, '#pm 2#sigma expected', "f")
    legend.AddEntry(theory_xsec_gr, 'Signal Cross Section', 'lf')

    legend.SetShadowColor(0)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetLineColor(0)
    legend.SetNColumns(2)
    legend.Draw()
    
    c4.RedrawAxis()

    folder = '.'
    outDir=folder+'/plots'
    if not os.path.exists(outDir): os.system('mkdir '+outDir)
    histPrefix=discriminant+'_'+lumiPlot.replace('.','p')+'fb'+chiral
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+'_'+str(binning).replace('.','p')+saveKey+'.eps')
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+'_'+str(binning).replace('.','p')+saveKey+'.pdf')
    c4.SaveAs(outDir+'/LimitPlot_'+histPrefix+'_'+str(binning).replace('.','p')+saveKey+'.png')
    return int(round(limExpected)), int(round(limObserved))

#PlotLimits(json_file,chiral,binning,saveKey)

print "=========>>>>>>>>>>> X53X53_LH"
expLim,obsLim = PlotLimits('LIMITS_LH/limits_isSR_isE.json','LH','0p2','_isE')
expLim,obsLim = PlotLimits('LIMITS_LH/limits_isSR_isM.json','LH','0p2','_isM')
expLim,obsLim = PlotLimits('LIMITS_LH/limits_cmb.json','LH','0p2','_all')
print "=========>>>>>>>>>>> X53X53_RH"
expLim,obsLim = PlotLimits('LIMITS_RH/limits_isSR_isE.json','RH','0p2','_isE')
expLim,obsLim = PlotLimits('LIMITS_RH/limits_isSR_isM.json','RH','0p2','_isM')
expLim,obsLim = PlotLimits('LIMITS_RH/limits_cmb.json','RH','0p2','_all')


