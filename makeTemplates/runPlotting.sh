#for iPlot in NsubBNm1 SoftDropNm1; do
#for iPlot in ST NBJetsNotH lepPt lepEta mindeltaR deltaRAK8 PtRel deltaRjet1 deltaRjet2 HT ST minMlb minMlj lepIso NPV JetEta JetPt MET NJets NBJets NWJets NH1bJets NH2bJets PuppiNH1bJets PuppiNH2bJets NJetsAK8 JetPtAK8 JetEtaAK8 Tau21 Tau21Nm1 Pruned PrunedWNm1 PrunedHNm1 PrunedNsubBNm1 SoftDrop SoftDropNm1 NsubBNm1 PuppiNsubBNm1 PuppiSD PuppiSDNm1; do
#for iPlot in ST; do
#for iPlot in minMlbST HT ST YLD; do
#for iPlot in minMlb minMlj ST; do
#for iPlot in NBJetsNotH NBJetsNotPH lepPt lepEta mindeltaR deltaRAK8 PtRel deltaRjet1 deltaRjet2 HT ST minMlb minMlj lepIso NPV JetEta JetPt MET NJets NBJets NWJets PuppiNWJets NH1bJets NH2bJets PuppiNH1bJets PuppiNH2bJets NJetsAK8 JetPtAK8 JetEtaAK8 Tau21 Tau21Nm1 PuppiTau21 PuppiTau21Nm1 Pruned PrunedWNm1 PrunedHNm1 PrunedNsubBNm1 SoftDrop SoftDropHNm1 SoftDropNsubBNm1 PuppiNsubBNm1 PuppiSD PuppiSDWNm1 PuppiSDHNm1; do

#for iPlot in PrunedHNm1 PrunedWNm1 Tau21Nm1; do
    #echo $iPlot
    #python plotPaper.py $iPlot SR kinematics_SRNoB0_NewEl
    # python plotTemplates.py $iPlot TTCR ttbar_ARC
    # python plotTemplates.py $iPlot TTCR ttbar_ARCpuppiW
    # python plotTemplates.py $iPlot WJCR wjets_ARC
    # python plotTemplates.py $iPlot WJCR wjets_ARCpuppiW
    # python plotTemplates.py $iPlot HCR higgs_ARC
    # python plotTemplates.py $iPlot HCR higgs_ARCpuppiW
    # python plotTemplates.py $iPlot CR templatesCR_NewEl
    # python plotTemplates.py $iPlot CRall control_NewEl
    # python plotTemplates.py $iPlot SR templates_NewEl
    # python plotTemplates.py $iPlot SR templates_ARCpuppiW
    # python plotTemplates.py $iPlot SR kinematics_SRnoDR_NewEl
    # python plotTemplates.py $iPlot SR kinematics_SRNoB0_NewEl
    # python plotTemplates.py $iPlot SR kinematics_SR_ARCpuppiW
    # python plotTemplates.py $iPlot SR kinematics_PS_NewEl
#done

python plotPaper.py PrunedNsubBNm1 SR kinematics_SRNoB0_NewEl True
#python plotPaper.py deltaRAK8 SR kinematics_SRNoB0noDR_NewEl
#python plotPaper.py HT CR templatesCR_NewEl

# echo 'Templates minMlbST'
# python plotPaper.py minMlbST SR templates_NewEl True

# echo 'CR templates HT'
# python plotPaper.py HT CR templatesCR_NewEl True
