#!/bin/bash

condorDir=$PWD
theDir=$1

source /cvmfs/cms.cern.ch/cmsset_default.sh

# cd $theDir
# eval `scramv1 runtime -sh`

cd /home/eusai/4t/CMSSW_10_2_16_UL/src
eval `scramv1 runtime -sh`

cd $theDir


pwd
python -u doHists.py $condorDir \
					--iPlot=${2} \
					--region=${3} \
					--isCategorized=${4} \
					--year=${5} \
					--isEM=${6} \
					--nhott=${7} \
					--nttag=${8} \
					--nWtag=${9} \
					--nbtag=${10} \
					--njets=${11} \
					--step1dir=${12} \
					