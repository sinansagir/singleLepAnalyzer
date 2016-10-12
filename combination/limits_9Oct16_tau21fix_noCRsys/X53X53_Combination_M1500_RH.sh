#!/bin/sh 
cd /home/ssagir/CMSSW_7_3_0/src/
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
cd -
cd limits_9Oct16_tau21fix_noCRsys/
/home/ssagir/CMSSW_7_3_0/src/theta/utils2/theta-auto.py /home/ssagir/CMSSW_7_3_0/src/singleLepAnalyzer/x53x53_2015/combination/limits_9Oct16_tau21fix_noCRsys/X53X53_Combination_M1500_RH.py