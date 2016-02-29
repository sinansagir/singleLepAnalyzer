#!/bin/bash

condorDir=$PWD
theDir=$1
isTTbarCR=$2
isEM=$3
nttag=$4
nWtag=$5
nbtag=$6

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $theDir
eval `scramv1 runtime -sh`

python doHists.py $condorDir $isTTbarCR $isEM $nttag $nWtag $nbtag
