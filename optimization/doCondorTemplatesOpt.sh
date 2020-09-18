#!/bin/bash

condorDir=$PWD
theDir=$1

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $theDir
eval `scramv1 runtime -sh`

python -u doHistsOpt.py $condorDir \
					--elPtCut=${2} \
					--muPtCut=${3} \
					--metCut=${4} \
					--mtCut=${5} \
					--jet1PtCut=${6} \
					--jet2PtCut=${7} \
					--jet3PtCut=${8} \
					--AK4HTCut=${9} \
					--AK4HTbCut=${10} \
					--maxJJJptCut=${11} \
