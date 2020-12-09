#Arguements: iPlot, region, isCategorized, directory, blind, yLog, rebinning

plotList='HT tpt DnnTTbar DnnWJets dnnLargest'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Nov2020TT_tptCorr380 False False 
    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Nov2020TT_tptwgt False False 
    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Nov2020TT_HTcorr False False 
done

#python plotTemplates.py HTNtag CR True templatesCR_June2020TT False False 0p15
#python plotTemplates.py HTNtag CR True templatesCR_June2020TT False True 0p15
#python plotTemplates.py HTNtag CR True templatesCR_June2020BB False False 0p15
#python plotTemplates.py HTNtag CR True templatesCR_June2020BB False True 0p15

# plotList='NBJets NBJetsNoSF NBDeepJets NBDeepJetsNoSF'
# for iPlot in $plotList; do
#     echo $iPlot
#     python plotTemplates.py $iPlot PS False kinematicsPS_EvanNB False False 
#     python plotTemplates.py $iPlot PS False kinematicsPS_EvanNB False True  
# done

#plotList='probSumDecay probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnTprime DnnWJets DnnTTbar DnnTprime DnnWJetsBB DnnTTbarBB tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet lepPhi'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot PS False kinematicsPS_April2020_TT False False 
#    python plotTemplates.py $iPlot PS False kinematicsPS_April2020_TT False True  
#    python plotTemplates.py $iPlot CR False kinematicsCR_April2020_TT False False
#    python plotTemplates.py $iPlot CR False kinematicsCR_April2020_TT False True
#done

# plotList='Tp2Mass Tp1Mass Tp2Pt Tp1Pt Tp1Eta Tp2Eta Tp1Phi Tp2Phi Tp1deltaR Tp2deltaR'
# for iPlot in $plotList; do
#     echo $iPlot
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_April2020_TT False False
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_April2020_TT False True
#     python plotTemplates.py $iPlot CR False kinematicsCR_April2020_TT False False
#     python plotTemplates.py $iPlot CR False kinematicsCR_April2020_TT False True
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_April2020_TT False False
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_April2020_TT False True
#     python plotTemplates.py $iPlot SR False kinematicsSR_April2020_TT True False
#     python plotTemplates.py $iPlot SR False kinematicsSR_April2020_TT True True
# done

# plotList='ST HT' #DnnTprime DnnWJets DnnTTbar DnnBprime DnnWJetsBB DnnTTbarBB'
# for iPlot in $plotList; do
#     echo $iPlot
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_April2020_TT False False 
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_April2020_TT False True
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_April2020_TT False False 
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_April2020_TT False True
#     python plotTemplates.py $iPlot SR False kinematicsSR_April2020_TT True False
#     python plotTemplates.py $iPlot SR False kinematicsSR_April2020_TT True True
# done

#plotList='DnnBprime DnnTprime'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot SR True templatesSR_April2020_TT True False 0p3
#    python plotTemplates.py $iPlot SR True templatesSR_April2020_TT True True 0p3
#done



# SPECIAL PS PLOTS
#plotList='DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False False
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False True
#done
