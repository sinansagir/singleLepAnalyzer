#!/bin/bash

condorDir=$PWD
theDir=$1

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $theDir
eval `scramv1 runtime -sh`

python doHists.py $condorDir \
					--iPlot=${2} \
					--region=${3} \
					--isCategorized=${4} \
					--isEM=${5} \
					--nhott=${6} \
					--nttag=${7} \
					--nWtag=${8} \
					--nbtag=${9} \
					--njets=${10} \
					