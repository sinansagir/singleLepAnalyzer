#!/bin/sh 
cd /home/ssagir/CMSSW_7_3_0/src/
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
cd /user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/limits/templates_Wkshp/all_postfit/
/home/ssagir/CMSSW_7_3_0/src/theta/utils2/theta-auto.py /user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/theta_bkg_mle.py