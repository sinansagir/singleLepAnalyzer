#Arguments: iPlot, region, isCategorized, directory, blind, yLog

plotList='tmass Wmass HT ST minDRlepAK8 Tau21Nm1 Tau32Nm1 SoftDropHNm1 SoftDropWZNm1 SoftDropTNm1 DoubleBNm1 JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt NPV lepEta JetEta JetEtaAK8 mindeltaR PtRel'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot PS False kinematicsPS_Oct11 False False 
    python plotTemplates.py $iPlot PS False kinematicsPS_Oct11 False True  
done

plotList='tmass Wmass HT ST minDRlepAK8 Tau21Nm1 Tau32Nm1 SoftDropHNm1 SoftDropWZNm1 SoftDropTNm1 DoubleBNm1 JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot SR False kinematicsSR_Oct11 True False 
    python plotTemplates.py $iPlot SR False kinematicsSR_Oct11 True True  
done

plotList='probb probh probj probt probw probz dnnLargest nB nH  nT nW  nZ'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot PSalgos False kinematicsPSalgos_Oct11 False False 
    python plotTemplates.py $iPlot PSalgos False kinematicsPSalgos_Oct11 False True  
done

plotList='Tp2Mass Tp1Mass Tp2Pt Tp1Pt Tp1Eta Tp2Eta Tp1Phi Tp2Phi Tp1deltaR Tp2deltaR probb probh probj probt probw probz dnnLargest nB nH  nT nW  nZ'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot SRalgos False kinematicsSRalgos_Oct11 True False 
    python plotTemplates.py $iPlot SRalgos False kinematicsSRalgos_Oct11 True True  
done

python plotTemplates.py deltaRAK8 NoDR False kinematicsNoDR_Oct11 False False

python plotTemplates.py Tp2Mass SR True templatesSR_Oct11 True True  
python plotTemplates.py Tp2Mass SR True templatesSR_Oct11 True False 
 
