#Arguements: iPlot, region, isCategorized, directory, blind, yLog, rebinning

#plotList='probSumDecay probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnTprime DnnWJets DnnTTbar DnnTprime DnnWJetsBB DnnTTbarBB tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet lepPhi'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot PS False kinematicsPS_October2019_TT_Rerun False False 
#    python plotTemplates.py $iPlot PS False kinematicsPS_October2019_TT_Rerun False True  
#    python plotTemplates.py $iPlot CR False kinematicsCR_October2019_TT_Rerun False False
#    python plotTemplates.py $iPlot CR False kinematicsCR_October2019_TT_Rerun False True
#done

#plotList='Bp2Mass Bp1Mass Bp2Pt Bp1Pt Bp1Eta Bp2Eta Bp1Phi Bp2Phi Bp1deltaR Bp2deltaR'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_October2019_BB_Rerun False False
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_October2019_BB_Rerun False True
#    python plotTemplates.py $iPlot CR False kinematicsCR_October2019_BB_Rerun False False
#    python plotTemplates.py $iPlot CR False kinematicsCR_October2019_BB_Rerun False True
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_October2019_BB_Rerun False False
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_October2019_BB_Rerun False True
#    python plotTemplates.py $iPlot SR False kinematicsSR_October2019_BB_Rerun True False
#    python plotTemplates.py $iPlot SR False kinematicsSR_October2019_BB_Rerun True True
#done

#plotList='ST HT DnnTprime DnnWJets DnnTTbar DnnBprime DnnWJetsBB DnnTTbarBB'
#plotList='DnnBprime DnnWJetsBB'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_October2019_BB_Rerun False False 
#    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_October2019_BB_Rerun False True
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_October2019_BB_Rerun False False 
#    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_October2019_BB_Rerun False True
#    python plotTemplates.py $iPlot SR False kinematicsSR_October2019_BB_Rerun True False
#    python plotTemplates.py $iPlot SR False kinematicsSR_October2019_BB_Rerun True True
#done

plotList='DnnBprime DnnTprime'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot SR True templatesSR_October2019_TT_Rerun True False 0p3
    python plotTemplates.py $iPlot SR True templatesSR_October2019_TT_Rerun True True 0p3
done



# SPECIAL PS PLOTS
#plotList='DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False False
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False True
#done
