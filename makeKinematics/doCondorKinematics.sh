#!/bin/bash

condorDir=$PWD
theDir=$1
plotIndex=$2
category=$3
cutConf=$4

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $theDir
eval `scramv1 runtime -sh`
cd -

python doHists.py $condorDir $plotIndex $category $cutConf
