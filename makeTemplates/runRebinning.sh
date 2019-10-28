#for iPlot in NBJetsNotH NBJetsNotPH lepPt lepEta mindeltaR deltaRAK8 PtRel deltaRjet1 deltaRjet2 HT ST minMlb minMlj lepIso NPV JetEta JetPt MET NJets NBJets NWJets PuppiNWJets NH1bJets NH2bJets PuppiNH1bJets PuppiNH2bJets NJetsAK8 JetPtAK8 JetEtaAK8 Tau21 Tau21Nm1 PuppiTau21 PuppiTau21Nm1 Pruned PrunedWNm1 PrunedHNm1 PrunedNsubBNm1 SoftDrop SoftDropHNm1 NsubBNm1 PuppiNsubBNm1 PuppiSD PuppiSDWNm1 PuppiSDHNm1; do
#for iPlot in ST; do
    #echo $iPlot
    #python -u modifyBinning.py $iPlot kinematicsPS_Mar30 1.1
#done

#Tp2Mass DnnTprime Tp2MDnn 
for iPlot in DnnBprime Bp2Mass; do #ST
#for iPlot in minMlb ST minMlj; do
#for iPlot in deltaRAK8; do
#for iPlot in minMlbST ST; do
    #echo $iPlot
    #python -u modifyBinning.py $iPlot templatesSR_Dec7 0.99
    #python -u modifyBinning.py $iPlot templatesSR_Nov30 0.99
    #python -u modifyBinning.py $iPlot templatesSR_Apr22 0.3
    #python -u modifyBinning.py $iPlot templatesSR_Apr22Counts 0.3
    #python -u modifyBinning.py $iPlot templatesSR_Apr22Dnn0p9 0.3
    #python -u modifyBinning.py $iPlot templatesSR_July_MVA_Update_Round2 0.3
    python -u modifyBinning.py $iPlot templatesSR_July2019_BB_Trained_MVA 0.3

    # python -u modifyBinning.py $iPlot kinematics_PS_NewEl 1.1
    # python -u modifyBinning.py $iPlot higgs_ARC 0.3
    # python -u modifyBinning.py $iPlot control_NewEl 0.3
    # python -u modifyBinning.py $iPlot templates_NewEl 1.1
    # python -u modifyBinning.py $iPlot templatesCR_NewEl 1.1
    # python -u modifyBinning.py $iPlot templatesCR_NewEl 0.3
    # python -u modifyBinning.py $iPlot ttbar_ARCpuppiW
    # python -u modifyBinning.py $iPlot wjets_ARCpuppiW
    # python -u modifyBinning.py $iPlot higgs_ARCpuppiW
    # python -u modifyBinning.py $iPlot templates_ARCpuppiW    
    #python -u modifyBinning_splitLess.py $iPlot ttbar_ARC
    #python -u modifyBinning_splitLess.py $iPlot wjets_ARC
    #python -u modifyBinning_splitLess.py $iPlot higgs_ARC
    #python -u modifyBinning_splitLess.py $iPlot templates_NewEl 1.1
    #python -u modifyBinning_splitLess.py $iPlot templates_BB_NewEl 0.3 BB
    #python -u modifyBinning_splitLess.py $iPlot templates_NewEl 0.15
    #python -u modifyBinning_splitLess.py $iPlot control_NewEl
done

#for iPlot in HT; do
#     echo $iPlot
     #python -u modifyBinning_splitLess.py $iPlot templatesCR_NewEl 0.3
#     python -u modifyBinning_splitLess.py $iPlot templatesCR_BB_NewEl 0.3 BB
#     python -u modifyBinning_splitLess.py $iPlot templatesCR_NewEl 0.15
#done
