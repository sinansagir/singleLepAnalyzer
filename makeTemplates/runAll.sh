#for iPlot in MTlmet lepPt lepEta mindeltaR PtRel deltaRjet1 deltaRjet2 deltaRjet3 lepIso deltaRAK8 NPV JetEta JetPt Jet1Pt Jet2Pt Jet3Pt Jet4Pt Jet5Pt Jet6Pt MET NJets NBJets NBJetsNoSF NWJets NTJets NJetsAK8 JetPtAK8 JetEtaAK8 Tau21 Tau21Nm1 Tau32 Tau32Nm1 PrunedSmeared PrunedSmearedNm1 SoftDropMass SoftDropMassNm1 Bjet1Pt Wjet1Pt Tjet1Pt HT ST minMlb minMlj topPt deltaPhiLMET; do
#for iPlot in mindeltaR PtRel lepPt lepEta deltaRjet1 deltaRjet2 deltaRjet3 NPV JetEta JetPt Jet1Pt Jet2Pt Jet3Pt Jet4Pt MET NJets NBJets NWJets NTJets NJetsAK8 JetPtAK8 JetEtaAK8 Tau21 Tau21Nm1 Tau32 Tau32Nm1 PrunedSmeared PrunedSmearedNm1 SoftDropMass SoftDropMassNm1 HT ST minMlb topPt; do
for iPlot in NJets NBJets NWJets NTJets NJetsAK8; do
#for iPlot in mindeltaR PtRel deltaRjet2 Tau21 Tau21Nm1 Tau32 Tau32Nm1 PrunedSmeared PrunedSmearedNm1 SoftDropMass SoftDropMassNm1 HT ST minMlb; do
    echo $iPlot
    #python modifyBinning.py $iPlot
    python plotTemplates.py $iPlot
done
