#Arguements: iPlot, region, isCategorized, directory, blind, yLog, rebinning

## WHAT HAVE YOU DONE:
## -- PS: TT cat0 NAD DR3
## -- CR: TT cat0 NAD DR3 R3
## -- TTCR: TT cat0 R3 and FSRT
## -- WJCR: TT cat0 R3 and FSRT
## -- SR: TT cat0 R3 and FSRT
## -- TTCR: BB cat0 and R3 FSRT
## -- WJCR: BB cat0 and R3 FSRT
## -- SR: BB cat0 R3 and FSRT
## -- CR: BB cat0 R3 and FSRT
## -- SR: TT cat1
## -- CR: BB cat1


##plotlist for NAD and DR3
#plotList='probSumDecay probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnBprime DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet' # lepPhi'
#plotList='lepPhi NBDeepJets'
#for iPlot in $plotList; do
#    echo $iPlot
#python plotTemplates.py $iPlot PS False kinematicsPS_June2020TT False False
#python plotTemplates.py $iPlot PS False kinematicsPS_June2020TT False True
#FINISHED    python plotTemplates.py $iPlot PS False kinematicsPS_June2020TT False False
#FINISHED    python plotTemplates.py $iPlot PS False kinematicsPS_June2020TT False True  
#done

#Plotlist for 3 letEta Tests
plotList='lepEta'
for iPlot in $plotList; do
	echo $iPlot
	python plotTemplates.py $iPlot PS False kinematicsPS_Test1_PS_noTrigg_noPrefire False False
	python plotTemplates.py $iPlot PS False kinematicsPS_Test1_PS_noTrigg_noPrefire False True
	python plotTemplates.py $iPlot PS False kinematicsPS_Test2_PS_noTrigg_noPrefire False False
	python plotTemplates.py $iPlot PS False kinematicsPS_Test2_PS_noTrigg_noPrefire False True
	python plotTemplates.py $iPlot PS False kinematicsPS_Test3_PS_noTrigg_noPrefire False False
	python plotTemplates.py $iPlot PS False kinematicsPS_Test3_PS_noTrigg_noPrefire False True
done


#plotlist for R3 NAD and DR3
## DnnWjetsBB of BB samples
#plotList='Tp2Mass Tp1Mass Tp2Pt Tp1Pt Tp1Eta Tp2Eta Tp1Phi Tp2Phi Tp1deltaR Tp2deltaR probSumDecay probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet'
#plotList='Bp2Mass Bp1Mass Bp2Pt Bp1Pt Bp1Eta Bp2Eta Bp1Phi Bp2Phi Bp1deltaR Bp2deltaR probSumDecay probSumFour probb probh probj probt probw probz dnnLargest nB nH nT nW nZ DnnBprime DnnWJetsBB DnnTTbarBB tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot CR False kinematicsCR_June2020TT False False
#FINISHED    python plotTemplates.py $iPlot CR False kinematicsCR_June2020TT False True
#FINISHED    python plotTemplates.py $iPlot CR False kinematicsCR_June2020BB False False
#FINISHED    python plotTemplates.py $iPlot CR False kinematicsCR_June2020BB False True
#done

##plotlist for R3 and FSRT
#plotList='Bp2Mass Bp1Mass Bp2Pt Bp1Pt Bp1Eta Bp2Eta Bp1Phi Bp2Phi Bp1deltaR Bp2deltaR ST HT DnnBprime DnnWJetsBB DnnTTbarBB'
#plotList='Tp2Mass Tp1Mass Tp2Pt Tp1Pt Tp1Eta Tp2Eta Tp1Phi Tp2Phi Tp1deltaR Tp2deltaR ST HT DnnBprime DnnWJets DnnTTbar'
#for iPlot in $plotList; do
#    echo $iPlot
#FINISHED    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False False
#FINISHED    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020TT False True
#FINISHED    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False False
#FINISHED    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020TT False True
#FINISHED    python plotTemplates.py $iPlot SR False kinematicsSR_June2020TT True False
#FINISHED    python plotTemplates.py $iPlot SR False kinematicsSR_June2020TT True True
#FINISHED    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020BB False False
#FINISHED    python plotTemplates.py $iPlot TTCR False kinematicsTTCR_June2020BB False True
#FINISHED    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020BB False False
#FINISHED    python plotTemplates.py $iPlot WJCR False kinematicsWJCR_June2020BB False True
#FINISHED    python plotTemplates.py $iPlot SR False kinematicsSR_June2020BB True False
#FINISHED    python plotTemplates.py $iPlot SR False kinematicsSR_June2020BB True True
#done

##plotlist for HTNtag
#plotList='HTNtag'
#for iPlot in $plotList; do
#    echo $iPlot
#ProllyGoodNow    python plotTemplates.py $iPlot CR True templatesCR_June2020TT False False 0p3
#ProllyGoodNow    python plotTemplates.py $iPlot CR True templatesCR_June2020TT False True 0p3
#FINISHED    python plotTemplates.py $iPlot CR True templatesCR_June2020BB False False 0p3
#FINISHED    python plotTemplates.py $iPlot CR True templatesCR_June2020BB False True 0p3
#done


##plotlist for DnnTprime DnnBprime
#plotList='DnnTprime' 
#plotList='DnnBprime'
#for iPlot in $plotList; do
#    echo $iPlot
#FINISHED    python plotTemplates.py $iPlot SR True templatesSR_June2020TT True False 0p3
#FINISHED    python plotTemplates.py $iPlot SR True templatesSR_June2020TT True True 0p3
#    python plotTemplates.py $iPlot SR True templatesSR_June2020BB True False 0p3
#    python plotTemplates.py $iPlot SR True templatesSR_June2020BB True True 0p3
#done



# SPECIAL PS PLOTS
#plotList='DnnTprime DnnWJets DnnTTbar tmass Wmass tpt Wpt tdrWb Wdrlep isLepW HT ST JetPt MET NJets NBJets NJetsAK8 JetPtAK8 lepPt SoftDrop deltaRAK8 minMlj mindeltaR PtRel mindeltaRAK8 PtRelAK8 lepEta lepIso JetEta JetEtaAK8 NTrue minMlb METmod minDPhiMetJet'
#for iPlot in $plotList; do
#    echo $iPlot
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False False
#    python plotTemplates.py $iPlot PS False kinematicsPS_July2019_TT_Rerun_Special False True
#done
