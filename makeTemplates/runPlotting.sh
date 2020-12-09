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


#plotlist for R3 NAD and DR3
## DnnWjetsBB of BB samples
#plotList='Tp2Mass Tp1Mass Tp2Pt Tp1Pt Tp1Eta Tp2Eta Tp1Phi Tp2Phi Tp1deltaR Tp2deltaR probSumDecay probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet'
#plotList='Bp2Mass Bp1Mass Bp2Pt Bp1Pt Bp1Eta Bp2Eta Bp1Phi Bp2Phi Bp1deltaR Bp2deltaR probSumDecay probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnBprime DnnWJetsBB DnnTTbarBB tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot CR False kinematicsCR_June2020TT False False
#FINISHED    python plotTemplates.py $iPlot CR False kinematicsCR_June2020TT False True
#FINISHED    python plotTemplates.py $iPlot CR False kinematicsCR_June2020BB False False
#FINISHED    python plotTemplates.py $iPlot CR False kinematicsCR_June2020BB False True
#done

##plotlist for R3 and FSRT
#plotList='Bp2Mass Bp1Mass Bp2Pt Bp1Pt Bp1Eta Bp2Eta Bp1Phi Bp2Phi Bp1deltaR Bp2deltaR ST HT DnnBprime DnnWJetsBB DnnTTbarBB'
#plotList='Tp2Mass Tp1Mass Tp2Pt Tp1Pt Tp1Eta Tp2Eta Tp1Phi Tp2Phi Tp1deltaR Tp2deltaR ST HT DnnBprime DnnWJets DnnTTbar'
#for iPlot in $plotList; do
#    echo $iPlot
#FINISHED    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False False
#FINISHED    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False True
#FINISHED    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False False
#FINISHED    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False True
#FINISHED    python plotTemplates.py $iPlot SR False kinematicsSR_June2020TT True False
#FINISHED    python plotTemplates.py $iPlot SR False kinematicsSR_June2020TT True True
#FINISHED    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020BB False False
#FINISHED    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020BB False True
#FINISHED    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020BB False False
#FINISHED    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020BB False True
#FINISHED    python plotTemplates.py $iPlot SR False kinematicsSR_June2020BB True False
#FINISHED    python plotTemplates.py $iPlot SR False kinematicsSR_June2020BB True True
#done

##plotlist for HTNtag
#plotList='HTNtag'
#for iPlot in $plotList; do
#    echo $iPlot
#ProllyGoodNow    python plotTemplates.py $iPlot CR True templatesCR_June2020TT False False 0p3
#ProllyGoodNow    python plotTemplates.py $iPlot CR True templatesCR_June2020TT False True 0p3
#FINISHED    python plotTemplates.py $iPlot CR True templatesCR_June2020BB False False 0p3
#FINISHED    python plotTemplates.py $iPlot CR True templatesCR_June2020BB False True 0p3
#done


##plotlist for DnnTprime DnnBprime
#plotList='DnnTprime' 
#plotList='DnnBprime'
#for iPlot in $plotList; do
#    echo $iPlot
#FINISHED    python plotTemplates.py $iPlot SR True templatesSR_June2020TT True False 0p3
#FINISHED    python plotTemplates.py $iPlot SR True templatesSR_June2020TT True True 0p3
#    python plotTemplates.py $iPlot SR True templatesSR_June2020BB True False 0p3
#    python plotTemplates.py $iPlot SR True templatesSR_June2020BB True True 0p3
#done



# SPECIAL PS PLOTS
#plotList='DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False False
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False True
#done
