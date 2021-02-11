import os,sys
from ROOT import TFile, TH1F, TCanvas, TGraphAsymmErrors, kBlack, kAzure, kOrange, kMagenta, kGray, THStack, gStyle, TPad, TLatex, TLegend, gROOT
parent = os.path.dirname(os.getcwd())
sys.path.append(parent)
from weights import *
from utils import *

gROOT.SetBatch()

limitdir = sys.argv[1]
mass = sys.argv[2]
lumi = 41.5

BR = 'bW0p5_tZ0p25_tH0p25'
sig1 = 'TTM1400'
sig1leg = 'T#bar{T} (1.4 TeV)'
if 'BB' in mass: 
    BR = 'tW0p5_bZ0p25_bH0p25'
    sig1 = 'BBM1400'
    sig1leg = 'B#bar{B} (1.4 TeV)'
mass = mass.replace('BB','')

name = limitdir.replace('limits_templatesCR_June2020','').replace('limits_templatesSRCR_June2020','')
path = limitdir+'/'+BR+'/cmb/'+mass

isSR = False
if 'SRCR' in limitdir: isSR = True

os.chdir(path)

shapesfile = ''
if not isSR:
    shapesfile = 'CRPostFitShapes.root'
    if not os.path.exists(shapesfile):
        print 'Creating pre and post-fit histograms from CR'
        print 'Command = PostFitShapesFromWorkspace -d combined.txt.cmb -w initialFitWorkspace.root -o CRPostFitShapes.root -m '+str(mass)+' -f fitDiagnostics.root:fit_b --postfit --sampling --print'
        os.system('PostFitShapesFromWorkspace -d combined.txt.cmb -w initialFitWorkspace.root -o CRPostFitShapes.root -m '+str(mass)+' -f fitDiagnostics.root:fit_b --postfit --sampling --print')


else:
    shapesfile = 'SRMorphedPrefitShapes.root'
    if not os.path.exists(shapesfile):
        masks = 'mask_TT_isSR_isE_notV01T1H_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV01T2pH_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV0T0H0Z01W_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV0T0H0Z2pW_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV0T0H1pZ_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV1T0H_DeepAK8_0_2017=0,mask_TT_isSR_isE_notV2pT_DeepAK8_0_2017=0,mask_TT_isSR_isE_notVbW_DeepAK8_0_2017=0,mask_TT_isSR_isE_notVtH_DeepAK8_0_2017=0,mask_TT_isSR_isE_notVtZ_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedbWbW_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedtHbW_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedtZHtZH_DeepAK8_0_2017=0,mask_TT_isSR_isE_taggedtZbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV01T1H_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV01T2pH_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV0T0H0Z01W_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV0T0H0Z2pW_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV0T0H1pZ_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV1T0H_DeepAK8_0_2017=0,mask_TT_isSR_isM_notV2pT_DeepAK8_0_2017=0,mask_TT_isSR_isM_notVbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_notVtH_DeepAK8_0_2017=0,mask_TT_isSR_isM_notVtZ_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedbWbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedtHbW_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedtZHtZH_DeepAK8_0_2017=0,mask_TT_isSR_isM_taggedtZbW_DeepAK8_0_2017=0'
        if 'tW' in BR: masks = masks.replace(',mask_TT_isSR_isE_taggedtZHtZH_DeepAK8_0_2017=0','').replace(',mask_TT_isSR_isM_taggedtZHtZH_DeepAK8_0_2017=0','').replace('bW','tW').replace('tZ','bZ').replace('tH','bH').replace('TT','BB')

        print 'Creating morphed prefit histograms for SR, after dummy FitDiagnostics command...'
        print 'Command = combine -M FitDiagnostics -d morphedWorkspace.root --snapshotName initialFit --saveWorkspace --bypassFrequentistFit -t -1 -n Morphed --setParameters (all masks 0)'
        print 'Command = PostFitShapesFromWorkspace -d combined.txt.cmb -w higgsCombineMorphed.FitDiagnostics.mH120.root -o SRMorphedPrefitShapes.root -m '+str(mass)+' --print'

        os.system('combine -M FitDiagnostics -d morphedWorkspace.root --snapshotName initialFit --saveWorkspace --bypassFrequentistFit -t -1 -n Morphed --setParameters '+masks)
        os.system('PostFitShapesFromWorkspace -d combined.txt.cmb -w higgsCombineMorphed.FitDiagnostics.mH120.root -o SRMorphedPrefitShapes.root -m '+str(mass)+' --print')



def formatUpperHist(histogram,th1hist):
    histogram.SetTitle('')
    histogram.GetXaxis().SetLabelSize(0)
    lowside = th1hist.GetBinLowEdge(1)
    highside = th1hist.GetBinLowEdge(th1hist.GetNbinsX()+1)
    histogram.GetXaxis().SetRangeUser(lowside,highside)
    histogram.GetXaxis().SetTitle('')
    histogram.GetYaxis().SetLabelSize(0.05)
    histogram.GetYaxis().SetTitleSize(0.06)
    histogram.GetYaxis().SetTitleOffset(.82)
    histogram.GetYaxis().CenterTitle()
    histogram.SetMinimum(0.00101)
    if blind:
        histogram.GetXaxis().SetLabelSize(0.045)
        histogram.GetXaxis().SetTitleSize(0.055)
        histogram.GetYaxis().SetLabelSize(0.04)
        histogram.GetYaxis().SetTitleSize(0.05)
        histogram.GetYaxis().SetTitleOffset(1.1)
        histogram.GetXaxis().SetNdivisions(506)
    if not yLog: 
        histogram.SetMinimum(0.000101);
    else:
        uPad.SetLogy()
        if 'dnnLargeJ' not in histogram.GetName(): 
            histogram.SetMaximum(500*histogram.GetMaximum())
        else:             
            histogram.SetMaximum(200*histogram.GetMaximum())

		
def formatLowerHist(histogram):
    histogram.SetTitle('')
    histogram.GetXaxis().SetLabelSize(.15)
    histogram.GetXaxis().SetTitleSize(0.18)
    histogram.GetXaxis().SetTitleOffset(0.95)
    histogram.GetXaxis().SetNdivisions(506)
    if iPlot=='HTNtag': 
        if 'dnnLargeT' in histogram.GetName(): 
            histogram.GetXaxis().SetTitle("N DeepAK8 t jets")
        elif 'dnnLargeH' in histogram.GetName(): 
            histogram.GetXaxis().SetTitle("N DeepAK8 H jets")
        elif 'dnnLargeZ' in histogram.GetName(): 
            histogram.GetXaxis().SetTitle("N DeepAK8 Z jets")
        elif 'dnnLargeW' in histogram.GetName(): 
            histogram.GetXaxis().SetTitle("N DeepAK8 W jets")
        elif 'dnnLargeB' in histogram.GetName(): 
            histogram.GetXaxis().SetTitle("N DeepAK8 B jets")

    histogram.GetYaxis().SetLabelSize(0.15)
    histogram.GetYaxis().SetTitleSize(0.145)
    histogram.GetYaxis().SetTitleOffset(.3)
    histogram.GetYaxis().SetTitle('#frac{(data-bkg)}{std. dev.}')
    histogram.GetYaxis().SetNdivisions(7)
    histogram.GetYaxis().SetRangeUser(-2.99,2.99)
    histogram.GetYaxis().CenterTitle()

tFile = TFile.Open(shapesfile)

chns = []
iPlot = ''

if not isSR: 
    iPlot = 'HTNtag'
    chns = [k.GetName() for k in tFile.GetListOfKeys() if k.GetName().endswith('_postfit')]
else:
    iPlot = 'DnnTprime'    
    chns = [k.GetName() for k in tFile.GetListOfKeys() if k.GetName().endswith('_prefit')]
bkgProcList = ['top','ewk','qcd']
bkgHistColors = {'top':kAzure+8,'ewk':kMagenta-2,'qcd':kOrange+5}
bkghists = {}
bkghistsmerged = {}

for chn in chns:
    if 'taggedbWbW' not in chn and 'taggedtWtW' not in chn: continue
    blind = False
    if 'isSR' in chn: blind = True
    yLog = True

    perNGeV = 0.01
    if 'dnnLargeJwjet' in chn or 'dnnLargeJttbar' in chn: perNGeV = 100
    elif 'dnnLarge' in chn: perNGeV = 1
    print '------------------ ',chn,' with perNGeV = ',perNGeV,'-----------------------'
    
    for proc in bkgProcList:         
        try:     
            bkghists[chn+proc] = tFile.Get(chn+'/'+proc).Clone()
        except:
            print "There is no "+proc+"!"
            print "tried to open "+chn+'/'+proc
            pass
    hData = tFile.Get(chn+'/data_obs').Clone()
    histrange = [hData.GetBinLowEdge(1),hData.GetBinLowEdge(hData.GetNbinsX()+1)]
    gaeData = TGraphAsymmErrors(hData.Clone(hData.GetName().replace('data_obs','gaeDATA')))
    hsig1 = tFile.Get(chn+'/'+sig1.replace('1400','')).Clone(chn+'__sig')
    hsig1.Scale(xsec[sig1]*10) # input is 100fb rather than 1 pb
    poissonNormByBinWidth(gaeData,hData,perNGeV)
    for proc in bkgProcList:
        try: 
            normByBinWidth(bkghists[chn+proc],perNGeV)
        except: pass
    normByBinWidth(hsig1,perNGeV)
    normByBinWidth(hData,perNGeV)
    # Yes, there are easier ways using the TH1's but
    # it would be rough to swap objects lower down

    bkgHT = bkghists[chn+bkgProcList[0]].Clone()
    for proc in bkgProcList:
        if proc==bkgProcList[0]: continue
        try: 
            bkgHT.Add(bkghists[chn+proc])
        except: pass

    bkgHTgerr = TGraphAsymmErrors(bkgHT.Clone("bkgHTgerrPostFit"))    

    drawQCD = False
    try: drawQCD = bkghists[chn+'qcd'].Integral()/bkgHT.Integral() > 0.005
    except: pass

    stackbkgHT = THStack("stackbkgHT","")
    for proc in bkgProcList:
        try: 
            if drawQCD or proc != 'qcd': stackbkgHT.Add(bkghists[chn+proc])
            bkghists[chn+proc].SetLineColor(bkgHistColors[proc])
            bkghists[chn+proc].SetFillColor(bkgHistColors[proc])
            bkghists[chn+proc].SetLineWidth(2)
        except:
            pass

    hsig1.SetLineColor(kBlack)
    hsig1.SetFillStyle(0)
    hsig1.SetLineWidth(3)

    gaeData.SetMarkerStyle(20)
    gaeData.SetMarkerSize(1.2)
    gaeData.SetMarkerColor(kBlack)
    gaeData.SetLineWidth(2)
    gaeData.SetLineColor(kBlack)

    bkgHTgerr.SetFillStyle(3004)
    bkgHTgerr.SetFillColor(kBlack)
                            

    gStyle.SetOptStat(0)
    c1 = TCanvas("c1","c1",1200,1000)
    gStyle.SetErrorX(0.5)
    yDiv=0.25
    if blind: yDiv=0.01
    # for some reason the markers at 0 don't show with this setting:
    uMargin = 0.00001
    if blind: uMargin = 0.12
    rMargin=.04
    # overlap the pads a little to hide the error bar gap:
    uPad={}
    if yLog and not blind: uPad=TPad("uPad","",0,yDiv-0.009,1,1) #for actual plots
    else: uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
    uPad.SetTopMargin(0.08)
    uPad.SetBottomMargin(uMargin)
    uPad.SetRightMargin(rMargin)
    uPad.SetLeftMargin(.105)
    uPad.Draw()

    if not blind:
        lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
        lPad.SetTopMargin(0)
        lPad.SetBottomMargin(.4)
        lPad.SetRightMargin(rMargin)
        lPad.SetLeftMargin(.105)
        lPad.SetGridy()
        lPad.Draw()

    hData.SetMinimum(0.015)
    hData.SetTitle("")
    gaeData.SetMaximum(1.6*max(gaeData.GetMaximum(),bkgHT.GetMaximum()))
    gaeData.SetMinimum(0.015)
    gaeData.SetTitle("")
    if iPlot == 'DnnTprime' or (iPlot == 'HTNtag' and perNGeV < 10): 
        gaeData.GetYaxis().SetTitle("< Events / "+str(perNGeV)+" >")
    else: 
        gaeData.GetYaxis().SetTitle("< Events / "+str(perNGeV)+" GeV >")

    formatUpperHist(gaeData,hData)
    uPad.cd()
    gaeData.SetTitle("")

    if iPlot == 'DnnTprime' or (iPlot == 'HTNtag' and perNGeV < 10): 
        hData.GetYaxis().SetTitle("< Events / "+str(perNGeV)+" >")
        if blind: hsig1.GetYaxis().SetTitle("< Events / "+str(perNGeV)+" >")
    else: 
        hData.GetYaxis().SetTitle("< Events / "+str(perNGeV)+" GeV >")
        if blind: hsig1.GetYaxis().SetTitle("< Events / "+str(perNGeV)+" GeV >")

    if not blind: 
        gaeData.Draw("apz")
    else:
        hsig1.SetMinimum(0.015)
        hsig1.SetMaximum(1.5*max(hData.GetMaximum(),bkgHT.GetMaximum()))
        formatUpperHist(hsig1,hsig1)
        hsig1.Draw("HIST")
        

    stackbkgHT.Draw("SAME HIST")
    hsig1.Draw("SAME HIST")
    if not blind: gaeData.Draw("PZ") #redraw data so its not hidden
    uPad.RedrawAxis()
    bkgHTgerr.Draw("SAME E2")

    chLatex = TLatex()
    chLatex.SetNDC()
    chLatex.SetTextSize(0.06)
    if blind: chLatex.SetTextSize(0.04)
    chLatex.SetTextAlign(21) # align center
    flvString = ''
    tagString = ''
    if 'isE' in chn: flvString+='e+jets'
    else: flvString+='#mu+jets'
    tagString = chn.split('_')[3]
    chLatex.DrawLatex(0.28, 0.84, flvString)
    chLatex.DrawLatex(0.28, 0.78, tagString)
    if 'postfit' in chn: chLatex.DrawLatex(0.28, 0.72, 'post-fit')

    if drawQCD: 
        leg = TLegend(0.45,0.64,0.95,0.89)
    else:
        leg = TLegend(0.45,0.76,0.95,0.89)
    leg.SetShadowColor(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetLineColor(0)
    leg.SetLineStyle(0)
    leg.SetBorderSize(0) 
    leg.SetNColumns(2)
    leg.SetTextFont(62)#42)
    if drawQCD:
        if not blind:
            leg.AddEntry(gaeData,"Data","pel")  #left
            leg.AddEntry(bkghists[chn+'qcd'],"QCD","f") #right
            leg.AddEntry(hsig1,sig1leg,"l")  #left
            try: 
                leg.AddEntry(bkghists[chn+'top'],"TOP","f") #right
            except: pass
            leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #left
            try: 
                leg.AddEntry(bkghists[chn+'ewk'],"EW","f") #right
            except: pass
        else:
            leg.AddEntry(hsig1,sig1leg,"l")  #left
            leg.AddEntry(bkghists[chn+'qcd'],"QCD","f") #right
            leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #left
            try: 
                leg.AddEntry(bkghists[chn+'top'],"TOP","f") #right
            except: pass
            leg.AddEntry(0,"","") #left
            try: 
                leg.AddEntry(bkghists[chn+'ewk'],"EW","f") #right
            except: pass
            
    else:
        if not blind:
            leg.AddEntry(gaeData,"Data","pel")  #left
            try: 
                leg.AddEntry(bkghists[chn+'top'],"TOP","f") #right
            except: pass
            leg.AddEntry(hsig1,sig1leg,"l") #left
            try: 
                leg.AddEntry(bkghists[chn+'ewk'],"EW","f") #right
            except: pass
            leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #left
        else:
            leg.AddEntry(hsig1,sig1leg,"l") #left
            try: 
                leg.AddEntry(bkghists[chn+'top'],"TOP","f") #right
            except: pass
            leg.AddEntry(bkgHTgerr,"Bkg. uncert.","f") #left
            try: 
                leg.AddEntry(bkghists[chn+'ewk'],"EW","f") #right
            except: pass


    leg.Draw("same")

    prelimTex=TLatex()
    prelimTex.SetNDC()
    prelimTex.SetTextAlign(31) # align right
    prelimTex.SetTextFont(42)
    prelimTex.SetTextSize(0.05)
    prelimTex.SetLineWidth(2)
    prelimTex.DrawLatex(0.95,0.94,str(lumi)+" fb^{-1} (13 TeV)")

    prelimTex2=TLatex()
    prelimTex2.SetNDC()
    prelimTex2.SetTextFont(61)
    prelimTex2.SetLineWidth(2)
    prelimTex2.SetTextSize(0.08)
    prelimTex2.DrawLatex(0.12,0.93,"CMS")

    prelimTex3=TLatex()
    prelimTex3.SetNDC()
    prelimTex3.SetTextAlign(12)
    prelimTex3.SetTextFont(52)
    prelimTex3.SetTextSize(0.055)
    prelimTex3.SetLineWidth(2)
    prelimTex3.DrawLatex(0.23,0.945,"Work in progress") #"Preliminary")
    if blind: prelimTex3.DrawLatex(0.26,0.945,"Work in progress") #"Preliminary")

    if not blind:
        #formatUpperHist(hData,hData)
        lPad.cd()
        pull=hData.Clone(chn+"pull")
        for binNo in range(1,hData.GetNbinsX()+1):
            # case for data < MC:
            dataerror = gaeData.GetErrorYhigh(binNo-1)
            MCerror = bkgHTgerr.GetErrorYlow(binNo-1)
            # case for data > MC: 
            if(hData.GetBinContent(binNo) > bkgHT.GetBinContent(binNo)):
                dataerror = gaeData.GetErrorYlow(binNo-1)
                MCerror = bkgHTgerr.GetErrorYhigh(binNo-1)
            pull.SetBinContent(binNo,(hData.GetBinContent(binNo)-bkgHT.GetBinContent(binNo))/math.sqrt(MCerror**2+dataerror**2))
        pull.SetMaximum(3)
        pull.SetMinimum(-3)
        pull.SetFillColor(kGray+2)
        pull.SetLineColor(kGray+2)
        formatLowerHist(pull)
        pull.Draw("HIST")

    savePrefix = 'PostFitPlots/'
    if not os.path.exists(savePrefix): os.system('mkdir -p '+savePrefix)
    savePrefix+=iPlot+'_'+str(lumi).replace('.','p')+'fb_'+chn+'_NBBW_pull'
    if blind: savePrefix+='_blind'
    if yLog: savePrefix+='_logy'

    c1.SaveAs(savePrefix+".pdf")
    c1.SaveAs(savePrefix+".png")

    for proc in bkgProcList:
        try: 
            del bkghists[chn+proc]
        except: pass
    del c1

    if '_isM_' in chn: continue

    for proc in bkgProcList:
        try: 
            bkghistsmerged[chn.replace('isE','isL')+proc] = tFile.Get(chn+'/'+proc).Clone()
            bkghistsmerged[chn.replace('isE','isL')+proc].Add(tFile.Get(chn.replace('isE','isM')+'/'+proc))
        except: pass

    hDatamerged = tFile.Get(chn+'/data_obs').Clone()
    hsig1merged = tFile.Get(chn+'/'+sig1.replace('1400','')).Clone(chn+'__sigmerged')
    hDatamerged.Add(tFile.Get(chn.replace('isE','isM')+'/data_obs').Clone())
    hsig1merged.Add(tFile.Get(chn.replace('isE','isM')+'/'+sig1.replace('1400','')).Clone())
    hsig1merged.Scale(xsec[sig1]*10)
    histrange = [hDatamerged.GetBinLowEdge(1),hDatamerged.GetBinLowEdge(hDatamerged.GetNbinsX()+1)]
    gaeDatamerged = TGraphAsymmErrors(hDatamerged.Clone(hDatamerged.GetName().replace("data_obs","gaeDATA")))

    poissonNormByBinWidth(gaeDatamerged,hDatamerged,perNGeV)
    for proc in bkgProcList:
        try: 
            normByBinWidth(bkghistsmerged[chn.replace('isE','isL')+proc],perNGeV)
        except: pass
    normByBinWidth(hsig1merged,perNGeV)
    normByBinWidth(hDatamerged,perNGeV)

    bkgHTmerged = bkghistsmerged[chn.replace('isE','isL')+bkgProcList[0]].Clone()
    for proc in bkgProcList:
        if proc==bkgProcList[0]: continue
        try: 
            bkgHTmerged.Add(bkghistsmerged[chn.replace('isE','isL')+proc])
        except: pass

    bkgHTgerrmerged = TGraphAsymmErrors(bkgHTmerged.Clone("bkgHTgerrmerged"))

    drawQCDmerged = False
    try: 
        drawQCDmerged = bkghistsmerged[chn.replace('isE','isL')+'qcd'].Integral()/bkgHTmerged.Integral()>.005
    except: pass

    stackbkgHTmerged = THStack("stackbkgHTmerged","")
    for proc in bkgProcList:
        try: 
            if drawQCDmerged or proc!='qcd': stackbkgHTmerged.Add(bkghistsmerged[chn.replace('isE','isL')+proc])
            bkghistsmerged[chn.replace('isE','isL')+proc].SetLineColor(bkgHistColors[proc])
            bkghistsmerged[chn.replace('isE','isL')+proc].SetFillColor(bkgHistColors[proc])
            bkghistsmerged[chn.replace('isE','isL')+proc].SetLineWidth(2)
        except: pass

    hsig1merged.SetLineColor(kBlack)
    hsig1merged.SetFillStyle(0)
    hsig1merged.SetLineWidth(3)

    gaeDatamerged.SetMarkerStyle(20)
    gaeDatamerged.SetMarkerSize(1.2)
    gaeDatamerged.SetLineWidth(2)
    gaeDatamerged.SetMarkerColor(kBlack)
    gaeDatamerged.SetLineColor(kBlack)

    bkgHTgerrmerged.SetFillStyle(3004)
    bkgHTgerrmerged.SetFillColor(kBlack)

    gStyle.SetOptStat(0)
    c1merged = TCanvas("c1merged","c1merged",1200,1000)
    gStyle.SetErrorX(0.5)
    yDiv=0.25
    if blind: yDiv = 0.01
    uMargin = 0.00001
    if blind: uMargin = 0.12
    rMargin=.04
    uPad={}
    if yLog and not blind: 
        uPad=TPad("uPad","",0,yDiv-0.009,1,1) #for actual plots
    else: uPad=TPad("uPad","",0,yDiv,1,1) #for actual plots
    uPad.SetTopMargin(0.08)
    uPad.SetBottomMargin(uMargin)
    uPad.SetRightMargin(rMargin)
    uPad.SetLeftMargin(.105)
    uPad.Draw()

    if not blind:
        lPad=TPad("lPad","",0,0,1,yDiv) #for sigma runner
        lPad.SetTopMargin(0)
        lPad.SetBottomMargin(.4)
        lPad.SetRightMargin(rMargin)
        lPad.SetLeftMargin(.105)
        lPad.SetGridy()
        lPad.Draw()

    gaeDatamerged.SetMaximum(1.6*max(gaeDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
    gaeDatamerged.SetMinimum(0.015)
    if iPlot == 'DnnTprime' or (iPlot == 'HTNtag' and perNGeV < 10): 
        gaeDatamerged.GetYaxis().SetTitle("< Events / "+str(perNGeV)+" >")
        if blind: hsig1merged.GetYaxis().SetTitle("< Events / "+str(perNGeV)+" >")
    else: 
        gaeDatamerged.GetYaxis().SetTitle("< Events / "+str(perNGeV)+" GeV >")
        if blind: hsig1merged.GetYaxis().SetTitle("< Events / "+str(perNGeV)+" GeV >")

    formatUpperHist(gaeDatamerged,hData)
    uPad.cd()
    gaeDatamerged.SetTitle("")
    stackbkgHTmerged.SetTitle("")
    if not blind: 
        gaeDatamerged.Draw("apz")
    else:
        hsig1merged.SetMinimum(0.015)
        hsig1merged.SetMaximum(1.5*max(hDatamerged.GetMaximum(),bkgHTmerged.GetMaximum()))
        formatUpperHist(hsig1merged,hsig1merged)
        hsig1merged.Draw("HIST")

    stackbkgHTmerged.Draw("SAME HIST")
    hsig1merged.Draw("SAME HIST")
    if not blind: gaeDatamerged.Draw("PZ") #redraw data so its not hidden
    uPad.RedrawAxis()
    bkgHTgerrmerged.Draw("SAME E2")

    chLatexmerged = TLatex()
    chLatexmerged.SetNDC()
    chLatexmerged.SetTextSize(0.06)
    if blind: chLatexmerged.SetTextSize(0.04)
    chLatexmerged.SetTextAlign(21) # align center
    flvString = 'e/#mu+jets'
    tagString = chn.split('_')[3]
    chLatexmerged.DrawLatex(0.28, 0.85, flvString)    
    chLatexmerged.DrawLatex(0.28, 0.78, tagString)
    if 'postfit' in chn: chLatexmerged.DrawLatex(0.28, 0.72, 'post-fit')

    if drawQCDmerged: 
        legmerged = TLegend(0.45,0.64,0.95,0.89)
    else: 
        legmerged = TLegend(0.45,0.76,0.95,0.89)

    legmerged.SetShadowColor(0)
    legmerged.SetFillColor(0)
    legmerged.SetFillStyle(0)
    legmerged.SetLineColor(0)
    legmerged.SetLineStyle(0)
    legmerged.SetBorderSize(0) 
    legmerged.SetNColumns(2)
    legmerged.SetTextFont(62)#42)                                      
    if drawQCDmerged:
        if not blind:
            legmerged.AddEntry(gaeDatamerged,"Data","pel")  #left
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'qcd'],"QCD","f") #right
            legmerged.AddEntry(hsig1merged,sig1leg,"l")  #left
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'top'],"TOP","f") #right
            except: pass
            legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f") #left
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ewk'],"EW","f") #right
            except: pass
        else:
            legmerged.AddEntry(hsig1merged,sig1leg,"l")  #left
            legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'qcd'],"QCD","f") #right
            legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f") #left
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'top'],"TOP","f") #right
            except: pass
            legmerged.AddEntry(0,"","") #left
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ewk'],"EW","f") #right
            except: pass
    else:
        if not blind:
            legmerged.AddEntry(gaeDatamerged,"Data","pel") #left 
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'top'],"TOP","f") #right
            except: pass
            legmerged.AddEntry(hsig1merged,sig1leg,"l") #left
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ewk'],"EW","f") #right
            except: pass
            legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f") #left
        else:
            legmerged.AddEntry(hsig1merged,sig1leg,"l") #left
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'top'],"TOP","f") #right
            except: pass
            legmerged.AddEntry(bkgHTgerrmerged,"Bkg. uncert.","f") #left
            try: 
                legmerged.AddEntry(bkghistsmerged[chn.replace('isE','isL')+'ewk'],"EW","f") #right
            except: pass

            

    legmerged.Draw("same")
 
    prelimTex=TLatex()
    prelimTex.SetNDC()
    prelimTex.SetTextAlign(31) # align right
    prelimTex.SetTextFont(42)
    prelimTex.SetTextSize(0.05)
    prelimTex.SetLineWidth(2)
    prelimTex.DrawLatex(0.95,0.94,str(lumi)+" fb^{-1} (13 TeV)")
 
    prelimTex2=TLatex()
    prelimTex2.SetNDC()
    prelimTex2.SetTextFont(61)
    prelimTex2.SetLineWidth(2)
    prelimTex2.SetTextSize(0.08)
    prelimTex2.DrawLatex(0.12,0.93,"CMS")

    prelimTex3=TLatex()
    prelimTex3.SetNDC()
    prelimTex3.SetTextAlign(12)
    prelimTex3.SetTextFont(52)
    prelimTex3.SetTextSize(0.055)
    prelimTex3.SetLineWidth(2)
    prelimTex3.DrawLatex(0.23,0.945,"Work in progress") #"Preliminary")
    if blind: prelimTex3.DrawLatex(0.26,0.945,"Work in progress") #"Preliminary")

    if not blind:
        #formatUpperHist(hDatamerged,hDatamerged)
        lPad.cd()
        pullmerged=hDatamerged.Clone(chn.replace('isE','isL')+"pullmerged")
        for binNo in range(1,hDatamerged.GetNbinsX()+1):
            # case for data < MC:
            dataerror = gaeDatamerged.GetErrorYhigh(binNo-1)
            MCerror = bkgHTgerrmerged.GetErrorYlow(binNo-1)
            # case for data > MC:
            if(hDatamerged.GetBinContent(binNo) > bkgHTmerged.GetBinContent(binNo)):
                dataerror = gaeDatamerged.GetErrorYlow(binNo-1)
                MCerror = bkgHTgerrmerged.GetErrorYhigh(binNo-1)
            pullmerged.SetBinContent(binNo,(hDatamerged.GetBinContent(binNo)-bkgHTmerged.GetBinContent(binNo))/math.sqrt(MCerror**2+dataerror**2))
        pullmerged.SetMaximum(3)
        pullmerged.SetMinimum(-3)
        pullmerged.SetFillColor(kGray+2)
        pullmerged.SetLineColor(kGray+2)
        formatLowerHist(pullmerged)
        pullmerged.Draw("HIST")

    savePrefixMerged = 'PostFitPlots/'
    if not os.path.exists(savePrefixMerged): os.system('mkdir -p '+savePrefixMerged)
    savePrefixMerged+=iPlot+'_'+str(lumi).replace('.','p')+'fb_'+chn.replace('isE','isL')+'_NBBW_pull'
    if blind: savePrefixMerged+='_blind'
    if yLog: savePrefixMerged+='_logy'

    c1merged.SaveAs(savePrefixMerged+".pdf")
    c1merged.SaveAs(savePrefixMerged+".png")

    for proc in bkgProcList:
        try: 
            del bkghistsmerged[chn.replace('isE','isL')+proc]
        except: pass
    del c1merged
