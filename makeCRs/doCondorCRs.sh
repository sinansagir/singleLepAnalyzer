#!/bin/bash

condorDir=$PWD
theDir=$1
isTTbarCR=$2
isEM=$3
nWtag=$4
nbtag=$5

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $theDir
eval `scramv1 runtime -sh`

python doHists.py $condorDir $isTTbarCR $isEM $nWtag $nbtag
