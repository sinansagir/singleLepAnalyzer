#!/bin/bash
theDir=$1
condorDir=$PWD
configfile=$2

source /cvmfs/cms.cern.ch/cmsset_default.sh

cd $theDir
eval `scramv1 runtime -sh`

/uscms_data/d3/ssagir/ljmet/CMSSW_7_3_0/src/theta/utils/theta-auto.py $configfile