#Arguements: iPlot, region, isCategorized, directory, blind, yLog

# plotListNew='DnnTprime ST Tp2Mass dnnLargest' #DnnWJets DnnTTbar HT tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET METmod minDPhiMetJet NJets NBJets NJetsAK8 JetPtAK8 lepPt NTrue SoftDrop mindeltaR PtRel mindeltaRAK8 PtRelAK8 deltaRAK8'
# for iPlot in $plotListNew; do
#      echo $iPlot
#      python plotTemplates.py $iPlot PS False kinematicsPS_Apr5Dnn0p5Met50 False False 
#      python plotTemplates.py $iPlot PS False kinematicsPS_Apr5Dnn0p5Met50 False True  
#      # python plotTemplates.py $iPlot CR False kinematicsCR_Apr5 False False 
#      # python plotTemplates.py $iPlot CR False kinematicsCR_Apr5 False True  
#      python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Apr5Dnn0p5Met50 False False 
#      python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Apr5Dnn0p5Met50 False True  
#      python plotTemplates.py $iPlot WJCR False kinematicsWJCR_Apr5Dnn0p5Met50 False False 
#      python plotTemplates.py $iPlot WJCR False kinematicsWJCR_Apr5Dnn0p5Met50 False 
#      python plotTemplates.py $iPlot SR False kinematicsSR_Apr5Dnn0p5Met50 True False 
#      python plotTemplates.py $iPlot SR False kinematicsSR_Apr5Dnn0p5Met50 True True  
# #     #python plotTemplates.py $iPlot PS0b False kinematicsPS0b_Mar30 False False 
# #     #python plotTemplates.py $iPlot PS0b False kinematicsPS0b_Mar30 False True  
# #     #python plotTemplates.py $iPlot PS2b False kinematicsPS2b_Mar30 False False 
# #     #python plotTemplates.py $iPlot PS2b False kinematicsPS2b_Mar30 False True  
# #     python plotTemplates.py $iPlot PS False kinematicsPS_Mar30NoTRWT False False 
# #     python plotTemplates.py $iPlot PS False kinematicsPS_Mar30NoTRWT False True  
# #     #python plotTemplates.py $iPlot PS2b False kinematicsPS2b_Mar30NoTRWT False False 
# #     #python plotTemplates.py $iPlot PS2b False kinematicsPS2b_Mar30NoTRWT False True  
# done

# plotList='probSumDecay probSumFour tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT JetPt MET METmod minDPhiMetJet NJets NBJets NJetsAK8 JetPtAK8 lepPt NPV lepEta lepIso JetEta JetEtaAK8 SoftDrop mindeltaR PtRel mindeltaRAK8 PtRelAK8 deltaRAK8 minMlj probb probh probj probt probw probz dnnLargest nB nH nT nW nZ'
# plotList2='Tp1Mass Tp2Pt Tp1Pt Tp1Eta Tp2Eta Tp1Phi Tp2Phi Tp1deltaR Tp2deltaR'
# plotList3='Tp2Mass ST DnnTprime DnnWJets DnnTTbar'

# for iPlot in $plotList; do
#     echo $iPlot
#     python plotTemplates.py $iPlot PS False kinematicsPS_Apr22 False False 
#     python plotTemplates.py $iPlot PS False kinematicsPS_Apr22 False True  
#     python plotTemplates.py $iPlot CR False kinematicsCR_Apr22 False False 
#     python plotTemplates.py $iPlot CR False kinematicsCR_Apr22 False True  
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Apr22 False False 
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Apr22 False True  
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_Apr22 False False 
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_Apr22 False True  
#     #python plotTemplates.py $iPlot SR False kinematicsSR_Apr22 True False 
#     #python plotTemplates.py $iPlot SR False kinematicsSR_Apr22 True True  
# done

# for iPlot in $plotList2; do
#     echo $iPlot
#     python plotTemplates.py $iPlot CR False kinematicsCR_Apr22 False False 
#     python plotTemplates.py $iPlot CR False kinematicsCR_Apr22 False True  
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Apr22 False False 
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Apr22 False True  
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_Apr22 False False 
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_Apr22 False True  
#     #python plotTemplates.py $iPlot SR False kinematicsSR_Apr22 True False 
#     #python plotTemplates.py $iPlot SR False kinematicsSR_Apr22 True True  
# done

# for iPlot in $plotList3; do
#     echo $iPlot
#     python plotTemplates.py $iPlot PS False kinematicsPS_Apr22 False False 
#     python plotTemplates.py $iPlot PS False kinematicsPS_Apr22 False True  
#     python plotTemplates.py $iPlot CR False kinematicsCR_Apr22 False False 
#     python plotTemplates.py $iPlot CR False kinematicsCR_Apr22 False True  
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Apr22 False False 
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Apr22 False True  
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_Apr22 False False 
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_Apr22 False True  
#     python plotTemplates.py $iPlot SR False kinematicsSR_Apr22 True False 
#     python plotTemplates.py $iPlot SR False kinematicsSR_Apr22 True True
#     python plotTemplates.py $iPlot CR False kinematicsCR_Apr22Dnn0p9 False False 
#     python plotTemplates.py $iPlot CR False kinematicsCR_Apr22Dnn0p9 False True  
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Apr22Dnn0p9 False False 
#     python plotTemplates.py $iPlot TTCR False kinematicsTTCR_Apr22Dnn0p9 False True  
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_Apr22Dnn0p9 False False 
#     python plotTemplates.py $iPlot WJCR False kinematicsWJCR_Apr22Dnn0p9 False True  
#     python plotTemplates.py $iPlot SR False kinematicsSR_Apr22Dnn0p9 True False 
#     python plotTemplates.py $iPlot SR False kinematicsSR_Apr22Dnn0p9 True True  
# done

#DnnTprime Tp2Mass  Tp2MDnn
# plotListTheta='ST Tp2MST' 
# for iPlot in $plotListTheta; do
#     echo $iPlot
#     python plotTemplates.py $iPlot SR True templatesSR_Apr22 True True
#     python plotTemplates.py $iPlot SR True templatesSR_Apr22 True False
#     python plotTemplates.py $iPlot SR True templatesSR_Apr22Dnn0p9 True True
#     python plotTemplates.py $iPlot SR True templatesSR_Apr22Dnn0p9 True False
#     python plotTemplates.py $iPlot SR True templatesSR_Apr22Counts True True
#     python plotTemplates.py $iPlot SR True templatesSR_Apr22Counts True False
#     python plotTemplates.py $iPlot SR True templatesSR_Apr22Dnn0p9Counts True True
#     python plotTemplates.py $iPlot SR True templatesSR_Apr22Dnn0p9Counts True False
# done


plotList='HT ST MET NJets NBJets NJetsAK8 lepPt NPV lepEta lepIso JetEta JetAK8Eta DnnTprime DnnTTbar DnnWJets'
#plotList='tmass Wmass HT ST deltaRAK8 MET NJets NJetsAK8 lepPt NPV lepEta mindeltaR PtRel mindeltaRAK8 PtRelAK8 DnnTprime DnnTTbar DnnWJets'
#plotList='tmass Wmass HT ST minDRlepAK8 Tau21Nm1 Tau32Nm1 SoftDropHNm1 SoftDropWZNm1 SoftDropTNm1 DoubleBNm1 JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt DnnTprime DnnTTbar DnnWJets'
for iPlot in $plotList; do
   echo $iPlot
   #python plotTemplates.py $iPlot SR False kinematicsSR_Jan5 True False 
   #python plotTemplates.py $iPlot SR False kinematicsSR_Jan5 True True  
   python plotTemplates.py $iPlot PS False kinematicsPS_HighPU False False 
   python plotTemplates.py $iPlot PS False kinematicsPS_HighPU False True  
done

#plotList='probb probh probj probt probw probz dnnLargest nB nH  nT nW  nZ probSumDecay probSumFour'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot PSalgos False kinematicsPSalgos_Jan5 False False 
#    python plotTemplates.py $iPlot PSalgos False kinematicsPSalgos_Jan5 False True  
#done

#plotList='Tp2Mass Tp1Mass Tp2Pt Tp1Pt Tp1Eta Tp2Eta Tp1Phi Tp2Phi Tp1deltaR Tp2deltaR probb probh probj probt probw probz dnnLargest nB nH  nT nW  nZ probSumDecay probSumFour'
#for iPlot in $plotList; do
    #echo $iPlot
    #python plotTemplates.py $iPlot TTCRalgos False kinematicsTTCRalgos_Jan5 False False 
    #python plotTemplates.py $iPlot TTCRalgos False kinematicsTTCRalgos_Jan5 False True  
    #python plotTemplates.py $iPlot WJCRalgos False kinematicsWJCRalgos_Jan5 False False 
    #python plotTemplates.py $iPlot WJCRalgos False kinematicsWJCRalgos_Jan5 False True  
    #python plotTemplates.py $iPlot SRalgos False kinematicsSRalgos_Jan5 True False 
    #python plotTemplates.py $iPlot SRalgos False kinematicsSRalgos_Jan5 True True  
    #python plotTemplates.py $iPlot CRalgos False kinematicsCRalgos_Jan5 True False 
    #python plotTemplates.py $iPlot CRalgos False kinematicsCRalgos_Jan5 True True  
#done

#python plotTemplates.py Tp2Mass SR True templatesSR_Dec8 True True  
#python plotTemplates.py Tp2Mass SR True templatesSR_Dec8 True False 

#python plotTemplates.py Tp2MDnn SR True templatesSR_Dec8 True True  
#python plotTemplates.py Tp2MDnn SR True templatesSR_Dec8 True False 

#python plotTemplates.py ST SR True templatesSR_Dec8 True True  
#python plotTemplates.py ST SR True templatesSR_Dec8 True False 

#python plotTemplates.py DnnTprime SR True templatesSR_Dec8 True True  
#python plotTemplates.py DnnTprime SR True templatesSR_Dec8 True False 
 
#python plotTemplates.py Tp2MST SR True templatesSR_Dec8 True True

#for iPlot in NsubBNm1 SoftDropNm1; do
#for iPlot in ST NBJetsNotH lepPt lepEta mindeltaR deltaRAK8 PtRel deltaRjet1 deltaRjet2 HT ST minMlb minMlj lepIso NPV JetEta JetPt MET NJets NBJets NWJets NH1bJets NH2bJets PuppiNH1bJets PuppiNH2bJets NJetsAK8 JetPtAK8 JetEtaAK8 Tau21 Tau21Nm1 Pruned PrunedWNm1 PrunedHNm1 PrunedNsubBNm1 SoftDrop SoftDropNm1 NsubBNm1 PuppiNsubBNm1 PuppiSD PuppiSDNm1; do
#for iPlot in ST; do
#for iPlot in minMlbST HT ST YLD; do
#for iPlot in minMlb minMlj ST; do
#for iPlot in NBJetsNotH NBJetsNotPH lepPt lepEta mindeltaR deltaRAK8 PtRel deltaRjet1 deltaRjet2 HT ST minMlb minMlj lepIso NPV JetEta JetPt MET NJets NBJets NWJets PuppiNWJets NH1bJets NH2bJets PuppiNH1bJets PuppiNH2bJets NJetsAK8 JetPtAK8 JetEtaAK8 Tau21 Tau21Nm1 PuppiTau21 PuppiTau21Nm1 Pruned PrunedWNm1 PrunedHNm1 PrunedNsubBNm1 SoftDrop SoftDropHNm1 SoftDropNsubBNm1 PuppiNsubBNm1 PuppiSD PuppiSDWNm1 PuppiSDHNm1; do

plotList='tmass Wmass HT ST minDRlepAK8 Tau21Nm1 Tau32Nm1 SoftDropHNm1 SoftDropWZNm1 SoftDropTNm1 DoubleBNm1 JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt NPV lepEta JetEta JetEtaAK8 mindeltaR PtRel'
for iPlot in $plotList; do
    echo $iPlot
    python plotTemplates.py $iPlot PS False kinematicsPS_Oct11 False False 
    python plotTemplates.py $iPlot PS False kinematicsPS_Oct11 False True  
done

#python makeTemplates/plotTemplates.py MET CR
#python plotPaper.py deltaRAK8 SR kinematics_SRNoB0noDR_NewEl
#python plotPaper.py HT CR templatesCR_NewEl

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
 
