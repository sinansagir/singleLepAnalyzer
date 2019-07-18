#Arguements: iPlot, region, isCategorized, directory, blind, yLog, rebinning

plotList='probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet lepPhi'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot PS False kinematicsPS_July_MVA_Update_Round2 False False 
    python plotTemplates.py $iPlot PS False kinematicsPS_July_MVA_Update_Round2 False True  
    python plotTemplates.py $iPlot CR False kinematicsCR_July_MVA_Update_Round2 False False
    python plotTemplates.py $iPlot CR False kinematicsCR_July_MVA_Update_Round2 False True
done

plotList='Tp2Mass Tp1Mass Tp2Pt Tp1Pt Tp1Eta Tp2Eta Tp1Phi Tp2Phi Tp1deltaR Tp2deltaR'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_July_MVA_Update_Round2 False False
    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_July_MVA_Update_Round2 False True
    python plotTemplates.py $iPlot CR False kinematicsCR_July_MVA_Update_Round2 False False
    python plotTemplates.py $iPlot CR False kinematicsCR_July_MVA_Update_Round2 False True
    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_July_MVA_Update_Round2 False False
    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_July_MVA_Update_Round2 False True
    python plotTemplates.py $iPlot SR False kinematicsSR_July_MVA_Update_Round2 True False
    python plotTemplates.py $iPlot SR False kinematicsSR_July_MVA_Update_Round2 True True
done

plotList='ST HT DnnTprime DnnWJets DnnTTbar'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_July_MVA_Update_Round2 False False 
    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_July_MVA_Update_Round2 False True
    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_July_MVA_Update_Round2 False False 
    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_July_MVA_Update_Round2 False True
    python plotTemplates.py $iPlot SR False kinematicsSR_July_MVA_Update_Round2 True False
    python plotTemplates.py $iPlot SR False kinematicsSR_July_MVA_Update_Round2 True True
done

#plotList='ST HT Tp2Mass DnnTprime'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot SR True templatesSR_July_MVA_Update_Round2 True False 0p3
#    python plotTemplates.py $iPlot SR True templatesSR_July_MVA_Update_Round2 True True 0p3
#done

