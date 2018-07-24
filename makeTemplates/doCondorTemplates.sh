#!/bin/bash

hostname 

outDir=$1
iPlot=$2
region=$3
isCategorized=$4
isEM=$5
nttag=$6
nWtag=$7
nbtag=$8
njets=$9

source /cvmfs/cms.cern.ch/cmsset_default.sh
scramv1 project CMSSW CMSSW_9_4_6_patch1
cd CMSSW_9_4_6_patch1
eval `scramv1 runtime -sh`
cd -

python -u doHists.py $outDir $iPlot $region $isCategorized $isEM $nttag $nWtag $nbtag $njets

