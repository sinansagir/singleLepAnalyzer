import ROOT
from CombineHarvester.CombineTools.plotting import *
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
 
# Style and pads
signal='T'
blind=True
ModTDRStyle()
canv = ROOT.TCanvas('limit', 'limit')
pads = OnePad()
print 'pads: ',pads 
# Get limit TGraphs as a dictionary
graphs = StandardLimitsFromJSONFile('limits.json')
 
# Create an empty TH1 from the first TGraph to serve as the pad axis and frame
axis = CreateAxisHist(graphs.values()[0])
axis.GetXaxis().SetTitle('T mass [GeV]')
axis.GetYaxis().SetTitle('#sigma (T#bar{T})[pb]')
pads[0].cd()
axis.Draw('axis')
 
# Create a legend in the top left
#legend = PositionedLegend(0.3, 0.2, 3, 0.015)

##Adding theory line, color changes, log scale

mass = array('d', [900,1100,1200,1300,1400,1500,1600,1700,1800])#
masserr = array('d', [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0])#
mass_str = ['900','1100','1200','1300','1400','1500','1600','1700','1800']#

exp   =array('d',[0 for i in range(len(mass))])
experr=array('d',[0 for i in range(len(mass))])
exp68H=array('d',[0 for i in range(len(mass))])
exp68L=array('d',[0 for i in range(len(mass))])
exp95H=array('d',[0 for i in range(len(mass))])
exp95L=array('d',[0 for i in range(len(mass))])
xsec = array('d',[1 for i in range(len(mass))])
theory_xsec = [0.0903,0.0224,0.0118,0.00639,0.00354,0.00200,0.001148,0.000666,0.000391]#pb# ##CHECK WHERE TO GET THESE VALUES FOR 900 and 1000 GEV. 
xsecErrUp = [4.0,1.1,0.64,0.37,0.22,0.14,0.087,0.056,0.037]#fb
xsecErrDn = [3.8,1.0,0.56,0.32,0.19,0.12,0.072,0.045,0.029]#fb

theory_xsec_up = [item/1000 for item in xsecErrUp]
theory_xsec_dn = [item/1000 for item in xsecErrDn]

theory_xsec_v    = ROOT.TVectorD(len(mass),array('d',theory_xsec))
theory_xsec_up_v = ROOT.TVectorD(len(mass),array('d',theory_xsec_up))
theory_xsec_dn_v = ROOT.TVectorD(len(mass),array('d',theory_xsec_dn))

theory_xsec_gr = ROOT.TGraphAsymmErrors(ROOT.TVectorD(len(mass),mass),theory_xsec_v,ROOT.TVectorD(len(mass),masserr),ROOT.TVectorD(len(mass),masserr),theory_xsec_dn_v,theory_xsec_up_v)
theory_xsec_gr.SetFillStyle(3001)
theory_xsec_gr.SetFillColor(ROOT.kRed)

theory = ROOT.TGraph(len(mass))
legend = ROOT.TLegend(.62,.49,.99,.88,"95% CL upper limits") # mixes

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
for i in range(len(mass)):
	if i!=0:
		if(exp[i]>theory_xsec[i] and exp[i-1]<theory_xsec[i-1]) or (exp[i]<theory_xsec[i] and exp[i-1]>theory_xsec[i-1]):
                        limExpected,ycross = getSensitivity(i,exp)



# Set the standard green and yellow colors and draw
StyleLimitBand(graphs)
DrawLimitBand(pads[0], graphs, legend=legend)
massv = ROOT.TVectorD(len(mass),mass)
masserrv = ROOT.TVectorD(len(mass),masserr)
expv = ROOT.TVectorD(len(mass),exp)
experrv = ROOT.TVectorD(len(mass),experr)
exp68Hv = ROOT.TVectorD(len(mass),exp68H)
exp68Lv = ROOT.TVectorD(len(mass),exp68L)
exp95Hv = ROOT.TVectorD(len(mass),exp95H)
exp95Lv = ROOT.TVectorD(len(mass),exp95L)
#
expected = ROOT.TGraphAsymmErrors(massv,expv,masserrv,masserrv,experrv,experrv)
#expected.SetLineColor(ROOT.kBlack)
expected68 = ROOT.TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp68Lv,exp68Hv)
#expected68.SetFillColor(ROOT.kGreen+1)
expected95 = ROOT.TGraphAsymmErrors(massv,expv,masserrv,masserrv,exp95Lv,exp95Hv)
#expected95.SetFillColor(ROOT.kOrange)

canv.SetBottomMargin(0.12)
canv.SetRightMargin(0.04)
canv.SetLeftMargin(0.12)
canv.SetTopMargin(0.08)
canv.SetLogy()
pads[0].SetLogy()

if signal == 'T': axis.GetYaxis().SetRangeUser(.0005+.00001,2.01)
else: axis.GetYaxis().SetRangeUser(.002+.00001,80.1)

#if not blind: legend.AddEntry(observed , 'Observed', "lp")
#legend.AddEntry(expected, 'Expected', "l")
#legend.AddEntry(expected68, '68% expected', "f")
#legend.AddEntry(expected95, '95% expected', "f")
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
 
# Re-draw the frame and tick marks
#Drawing theory line
pads[0].RedrawAxis()
pads[0].GetFrame().Draw()
#expected95.Draw("a3")
#expected68.Draw("3same")
#expected.Draw("same")
theory_xsec_gr.SetLineColor(2)
theory_xsec_gr.SetLineStyle(1)
theory_xsec_gr.SetLineWidth(2)
theory_xsec_gr.Draw("3same")
theory.SetLineColor(2)
theory.SetLineStyle(1)
theory.SetLineWidth(2)
theory.Draw("same")
 
# Adjust the y-axis range such that the maximum graph value sits 25% below
# the top of the frame. Fix the minimum to zero.
#FixBothRanges(pads[0], 0.01, 0, GetPadYMax(pads[0]), 0.25)
 
# Standard CMS logo
DrawCMSLogo(pads[0], 'CMS', 'Internal', 11, 0.045, 0.035, 1.2, '', 0.8)
 
canv.Print('.pdf')
canv.Print('.png')
