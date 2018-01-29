#!/bin/sh 

category=${1}

cd /home/ssagir/CMSSW_7_3_0/src/
source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
#cd /user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/limitsAug17/templates4CRhtSR_postfit/
#/home/ssagir/CMSSW_7_3_0/src/theta/utils2/theta-auto.py /user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/theta_sigbkg_mle.py $category

cd /user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/limitsOct17/templates4CRhtSR_postfit/
/home/ssagir/CMSSW_7_3_0/src/theta/utils2/theta-auto.py /user_data/jhogan/CMSSW_7_4_14/src/tptp_2016/thetaLimits/theta_bkgonly123_mle.py $category