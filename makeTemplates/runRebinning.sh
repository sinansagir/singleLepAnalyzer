#for iPlot in NBJetsNotH NBJetsNotPH lepPt lepEta mindeltaR deltaRAK8 PtRel deltaRjet1 deltaRjet2 HT ST minMlb minMlj lepIso NPV JetEta JetPt MET NJets NBJets NWJets PuppiNWJets NH1bJets NH2bJets PuppiNH1bJets PuppiNH2bJets NJetsAK8 JetPtAK8 JetEtaAK8 Tau21 Tau21Nm1 PuppiTau21 PuppiTau21Nm1 Pruned PrunedWNm1 PrunedHNm1 PrunedNsubBNm1 SoftDrop SoftDropHNm1 NsubBNm1 PuppiNsubBNm1 PuppiSD PuppiSDWNm1 PuppiSDHNm1; do
#for iPlot in ST; do
    #echo $iPlot
    #python -u modifyBinning.py $iPlot kinematicsPS_Mar30 1.1
#done

## WHAT HAVE I DONE:
# -- CR: TT cat0
# -- PS: TT cat0
# -- SR: TT cat0
# -- TTCR: TT cat0
# -- WJCR: TT cat0
# -- CR: TT cat1
# -- All BB cat0 samples
# -- CR: BB cat1
# -- SR: BB cat1


## I'm calling all of the catagorized
#for iPlot in HT; do
#    echo $iPlot
#FINISHED    python -u modifyBinning.py $iPlot kinematicsCR_June2020BB 1.1
#FINISHEDAND SANITY CHECKED    python -u modifyBinning.py $iPlot kinematicsCR_June2020TT 1.1
#FINISHED    python -u modifyBinning.py $iPlot kinematicsPS_June2020TT 1.1
#FINSIHED    python -u modifyBinning.py $iPlot kinematicsSR_June2020BB 1.1
#FINISHED    python -u modifyBinning.py $iPlot kinematicsSR_June2020TT 1.1
#FINSIHED    python -u modifyBinning.py $iPlot kinematicsTTCR_June2020BB 1.1
#FINISHED    python -u modifyBinning.py $iPlot kinematicsTTCR_June2020TT 1.1
#FINSIHED    python -u modifyBinning.py $iPlot kinematicsWJCR_June2020BB 1.1
#FINISHED    python -u modifyBinning.py $iPlot kinematicsWJCR_June2020TT 1.1
#done

## I'm calling all of the Catagorized 
## IPlot foldername stat_saved(0.3orSomething) FullMu rebinCombine

#for iPlot in HTNtag; do
#     echo $iPlot
#FINISHED     python -u modifyBinning.py $iPlot templatesCR_June2020BB 0.3 True False  #FullMu: True && Combine: False -> FOR PLOTS
#FINISHED     python -u modifyBinning.py $iPlot templatesCR_June2020BB 0.3 False True  #FullMu: False && Combine: True
#FINISHED     python -u modifyBinning.py $iPlot templatesCR_June2020BB 0.3 False False  #FullMu: False && Combine: False -> BKGNORM
#FINISHED     python -u modifyBinning.py $iPlot templatesCR_June2020TT 0.3 True False  #FullMu: True && Combine: False -> FOR PLOTS
#FINISHED     python -u modifyBinning.py $iPlot templatesCR_June2020TT 0.3 False True  #FullMu: False && Combine: True
#FINISHED     python -u modifyBinning.py $iPlot templatesCR_June2020TT 0.3 False False  #FullMu: False && Combine: False -> BKGNORM
#done

#for iPlot in DnnTprime; do
#     echo $iPlot
#FINISHED     python -u modifyBinning.py $iPlot templatesSR_June2020TT 0.3 True False  #FullMu: True && Combine: False -> FOR PLOTS
#FINISHED     python -u modifyBinning.py $iPlot templatesSR_June2020TT 0.3 False True  #FullMu: False && Combine: True
#FINISHED     python -u modifyBinning.py $iPlot templatesSR_June2020TT 0.3 False False  #FullMu: False && Combine: False -> BKGNORM
#done

#for iPlot in DnnBprime; do
#     echo $iPlot
#FINISHED     python -u modifyBinning.py $iPlot templatesSR_June2020BB 0.3 True False  #FullMu: True && Combine: False -> FOR PLOTS
#FINISHED     python -u modifyBinning.py $iPlot templatesSR_June2020BB 0.3 False True  #FullMu: False && Combine: True
#FINISHED     python -u modifyBinning.py $iPlot templatesSR_June2020BB 0.3 False False  #FullMu: False && Combine: False -> BKGNORM
#done

