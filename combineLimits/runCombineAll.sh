#!/bin/bash

inputDir=limits_R2017_Xtrig_2020_3_20_corrd/

for d in $(ls ${inputDir} | grep "isSR"); 
do
    cd ${inputDir}/${d}/690/ 
    echo $d
    combine -M Significance TTTT_${d}_0_13TeV.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 >& Significance.txt
    combine -M AsymptoticLimits TTTT_${d}_0_13TeV.root -t -1 --run=blind --cminDefaultMinimizerStrategy 0 >& AsymptoticLimits.txt
    cd -
done
