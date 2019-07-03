#!/bin/bash
configfile=$1

hostname

source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc530

scramv1 project CMSSW CMSSW_8_0_20
cd CMSSW_8_0_20
eval `scramv1 runtime -sh`
cd -

echo 'Copy theta tarball from EOS'
xrdcp root://cmseos.fnal.gov//store/user/jmanagan/theta8020.tar .
tar -xf theta8020.tar
rm theta8020.tar

python -u theta/utils2/theta-auto.py ${configfile}.py

rm *.root

tar -zcf htmlout_${configfile}.tar htmlout_${configfile}_DeepAK8/

echo "Files I expect to come back:"
ls -l

