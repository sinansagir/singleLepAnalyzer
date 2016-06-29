#!/bin/bash

date

python -u doKinematics.py kinematics_preSel_noJSF_2016_6_22
sleep 5
python -u doKinematics.py kinematics_finalSelnoDR_noJSF_2016_6_22
sleep 5
python -u doKinematics.py kinematics_finalSel_noJSF_2016_6_22
sleep 5

python -u doKinematics.py kinematics_preSel_noJSF_2016_6_22_WJetsHTbins
sleep 5
python -u doKinematics.py kinematics_finalSelnoDR_noJSF_2016_6_22_WJetsHTbins
sleep 5
python -u doKinematics.py kinematics_finalSel_noJSF_2016_6_22_WJetsHTbins
sleep 5

python -u doKinematics.py kinematics_preSel_withJSF_2016_6_22
sleep 5
python -u doKinematics.py kinematics_finalSelnoDR_withJSF_2016_6_22
sleep 5
python -u doKinematics.py kinematics_finalSel_withJSF_2016_6_22

echo "DONE"

date