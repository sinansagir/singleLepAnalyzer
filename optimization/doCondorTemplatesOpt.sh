#!/bin/bash

condorDir=$PWD
theDir=$1

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $theDir
eval `scramv1 runtime -sh`

python doHistsOpt.py $condorDir \
					--lepPtCut=${2} \
					--jet1PtCut=${3} \
					--jet2PtCut=${4} \
					--metCut=${5} \
					--njetsCut=${6} \
					--nbjetsCut=${7} \
					--jet3PtCut=${8} \
					--jet4PtCut=${9} \
					--jet5PtCut=${10} \
					--drCut=${11} \
					--Wjet1PtCut=${12} \
					--bjet1PtCut=${13} \
					--htCut=${14} \
					--stCut=${15} \
					--minMlbCut=${16} \
