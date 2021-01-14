#!/bin/bash

for iPlot in lepPt lepEta lepPhi lepIso deltaRjet1 deltaRjet2 deltaRjet3 \
             JetEta JetPhi JetPt Jet1Pt Jet2Pt Jet3Pt Jet4Pt Jet5Pt Jet6Pt MET METphi \
             NJets NBJets NBJetsNoSF NDCSVBJets NDCSVBJetsNoSF \
             mindeltaR PtRel HT ST minMlb MTlmet minMlj HTb maxJJJpt \
             Bjet1Pt Wjet1Pt Tjet1Pt topMass topPt \
             NHOTtJets HOTtPt HOTtEta HOTtPhi HOTtMass HOTtDisc HOTtNconst HOTtNAK4 \
             HOTtDRmax HOTtDThetaMax HOTtDThetaMin \
             NresolvedTops1p NresolvedTops2p NresolvedTops5p NresolvedTops10p;
	do
    echo $iPlot
    python modifyBinning.py $iPlot
    python plotTemplates.py $iPlot
done
             #NWJets NTJets NJetsAK8 JetPtAK8 JetEtaAK8 JetPhiAK8 deltaRAK8 \
             #Tau1 Tau2 Tau3 Tau21 Tau21Nm1 Tau32 Tau32Nm1 SoftDropMass SoftDropMassNm1W SoftDropMassNm1t \
             #NresolvedTops1pNoSF NresolvedTops2pNoSF NresolvedTops5pNoSF NresolvedTops10pNoSF;
