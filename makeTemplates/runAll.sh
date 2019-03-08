for iPlot in lepPt lepEta deltaRjet1 deltaRjet2 deltaRjet3 NPV JetEta JetPt Jet1Pt Jet2Pt Jet3Pt Jet4Pt MET NJets NBJets NWJets NTJets NJetsAK8 JetPtAK8 JetEtaAK8 Tau21 Tau21Nm1 Tau32 Tau32Nm1 SoftDropMass SoftDropMassNm1W SoftDropMassNm1t mindeltaR PtRel HT ST minMlb NBJetsNoSF nTrueInt MTlmet minMlj lepIso; do
    echo $iPlot
    #python modifyBinning.py $iPlot
    python plotTemplates.py $iPlot
done
