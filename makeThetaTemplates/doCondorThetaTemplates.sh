#!/bin/bash

condorDir=$PWD
theDir=$1

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $theDir
eval `scramv1 runtime -sh`

python doHists.py $condorDir \
                  --lepPtCut=${2} \
                  --jet1PtCut=${3} \
                  --jet2PtCut=${4} \
                  --metCut=${5} \
                  --njetsCut=${6} \
                  --nbjetsCut=${7} \
                  --jet3PtCut=${8} \
                  --drCut=${9} \
                  --isEM=${10} \
                  --nttag=${11} \
                  --nWtag=${12} \
                  --nbtag=${13}
