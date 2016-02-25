#!/bin/bash

condorDir=$PWD
theDir=$1
lepPtCut=$2
jet1PtCut=$3
jet2PtCut=$4
metCut=$5
njetsCut=$6
nbjetsCut=$7
jet3PtCut=$8
jet4PtCut=$9
jet5PtCut=${10}
drCut=${11}
Wjet1PtCut=${12}
bjet1PtCut=${13}
htCut=${14}
stCut=${15}
minMlbCut=${16}
isEM=${17}
nWtag=${18}
nbtag=${19}

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $theDir
eval `scramv1 runtime -sh`

python doHists.py $condorDir $lepPtCut $jet1PtCut $jet2PtCut $metCut $njetsCut $nbjetsCut $jet3PtCut $jet4PtCut $jet5PtCut $drCut $Wjet1PtCut $bjet1PtCut $htCut $stCut $minMlbCut $isEM $nWtag $nbtag
