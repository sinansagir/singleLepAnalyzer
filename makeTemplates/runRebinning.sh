#for iPlot in MTlmet lepPt lepEta mindeltaR PtRel deltaRjet1 deltaRjet2 deltaRjet3 lepIso deltaRAK8 NPV JetEta JetPt Jet1Pt Jet2Pt Jet3Pt Jet4Pt Jet5Pt Jet6Pt MET NJets NBJets NBJetsNoSF NWJets NTJets NJetsAK8 JetPtAK8 JetEtaAK8 Tau21 Tau21Nm1 Tau32 Tau32Nm1 PrunedSmeared PrunedSmearedNm1 SoftDropMass SoftDropMassNm1 Bjet1Pt Wjet1Pt Tjet1Pt HT ST minMlb minMlj; do
#for iPlot in Jet1Pt Jet2Pt NJets NBJets Tau21 Tau1 Tau2 Tau3 Tau32 PrunedSmeared SoftDropMass HT ST topPt; do
#for iPlot in lepPt lepEta mindeltaR PtRel deltaRjet1 deltaRjet2 HT ST minMlb minMlj lepIso NPV JetEta JetPt Jet1Pt Jet2Pt Jet3Pt Jet4Pt MET NJets NBJets NWJets NH1bJets NH2bJets NJetsAK8 JetPtAK8 JetEtaAK8 topMass topPt Tau1 Tau2 Tau3 Tau21 Tau21Nm1 PrunedSmeared PrunedSmearedNm1 SoftDropMass Bjet1Pt Wjet1Pt; do
for iPlot in minMlb; do
    echo $iPlot
    python modifyBinning.py $iPlot
done
