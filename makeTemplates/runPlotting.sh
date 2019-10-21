#Arguements: iPlot, region, isCategorized, directory, blind, yLog, rebinning

plotList='probSumDecay probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnBprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet lepPhi'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_BB_Trained_MVA False False 
    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_BB_Trained_MVA False True  
    python plotTemplates.py $iPlot CR False kinematicsCR_July2019_BB_Trained_MVA False False
    python plotTemplates.py $iPlot CR False kinematicsCR_July2019_BB_Trained_MVA False True
done

plotList='Bp2Mass Bp1Mass Bp2Pt Bp1Pt Bp1Eta Bp2Eta Bp1Phi Bp2Phi Bp1deltaR Bp2deltaR'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_July2019_BB_Trained_MVA False False
    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_July2019_BB_Trained_MVA False True
    python plotTemplates.py $iPlot CR False kinematicsCR_July2019_BB_Trained_MVA False False
    python plotTemplates.py $iPlot CR False kinematicsCR_July2019_BB_Trained_MVA False True
    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_July2019_BB_Trained_MVA False False
    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_July2019_BB_Trained_MVA False True
    python plotTemplates.py $iPlot SR False kinematicsSR_July2019_BB_Trained_MVA True False
    python plotTemplates.py $iPlot SR False kinematicsSR_July2019_BB_Trained_MVA True True
done

plotList='ST HT DnnBprime DnnWJets DnnTTbar'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_July2019_BB_Trained_MVA False False 
    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_July2019_BB_Trained_MVA False True
    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_July2019_BB_Trained_MVA False False 
    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_July2019_BB_Trained_MVA False True
    python plotTemplates.py $iPlot SR False kinematicsSR_July2019_BB_Trained_MVA True False
    python plotTemplates.py $iPlot SR False kinematicsSR_July2019_BB_Trained_MVA True True
done

plotList='DnnBprime ST Bp2Mass'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot SR True templatesSR_July2019_BB_Trained_MVA True False 0p3
    python plotTemplates.py $iPlot SR True templatesSR_July2019_BB_Trained_MVA True True 0p3
done



# SPECIAL PS PLOTS
#plotList='DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False False
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False True
#done
