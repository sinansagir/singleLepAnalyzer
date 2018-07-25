#!/bin/bash

condorDir=$PWD
theDir=$1
iPlot=$2
region=$3
isCategorized=$4
isEM=$5
tag=$6
algo=$7

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $theDir
eval `scramv1 runtime -sh`

python doHists.py $condorDir $iPlot $region $isCategorized $isEM $tag $algo
