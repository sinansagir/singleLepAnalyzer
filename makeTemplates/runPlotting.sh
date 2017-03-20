for iPlot in NPV MTlmet topPt Bjet1Pt lepPt lepEta JetEta JetPt Jet1Pt Jet2Pt Jet3Pt mindeltaR MET NJets NBJetsNoSF NBJets PtRel HT ST minMlb deltaPhilepJets0 deltaPhilepJets1 deltaPhilepJets2 deltaRlepJets0 deltaRlepJets1 deltaRlepJets2 deltaR_lepBJets0 mindeltaRlb masslepJets0 masslepJets1 masslepJets2 masslepBJets0 LeadJetPt aveBBdr minBBdr mass_maxJJJpt mass_maxBBmass mass_maxBBpt lepDR_minBBdr mass_minLLdr mass_minBBdr mass_lepBB_minBBdr mass_lepJJ_minJJdr; do
    echo $iPlot
    python plotTemplates.py $iPlot
done
