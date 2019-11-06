#!/bin/bash

inputDir=limits_noHOTtW_OR_onlyHOTtW_2019_10_24/

for d in $(ls ${inputDir} | grep "isSR"); 
do
    cd ${inputDir}/${d}/690/ 
    echo $d
    combine -M Significance TTTT_${d}_0_13TeV.root -t -1 --expectSignal=1 >& Significance.txt
    combine -M AsymptoticLimits TTTT_${d}_0_13TeV.root -t -1 --run=blind >& AsymptoticLimits.txt
    cd -
done
