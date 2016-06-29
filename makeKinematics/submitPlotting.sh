#!/bin/bash

date

python -u plotKinematics.py kinematics_preSel_noJSF_2016_6_22 0 0
sleep 5
python -u plotKinematics.py kinematics_preSel_noJSF_2016_6_22 1 0
sleep 5
python -u plotKinematics.py kinematics_preSel_noJSF_2016_6_22 0 1
sleep 5
python -u plotKinematics.py kinematics_finalSelnoDR_noJSF_2016_6_22 0 0
sleep 5
python -u plotKinematics.py kinematics_finalSelnoDR_noJSF_2016_6_22 1 0
sleep 5
python -u plotKinematics.py kinematics_finalSelnoDR_noJSF_2016_6_22 0 1
sleep 5
python -u plotKinematics.py kinematics_finalSel_noJSF_2016_6_22 0 0
sleep 5
python -u plotKinematics.py kinematics_finalSel_noJSF_2016_6_22 1 0
sleep 5
python -u plotKinematics.py kinematics_finalSel_noJSF_2016_6_22 0 1
sleep 5

python -u plotKinematics.py kinematics_preSel_noJSF_2016_6_22_WJetsHTbins 0 0
sleep 5
python -u plotKinematics.py kinematics_preSel_noJSF_2016_6_22_WJetsHTbins 1 0
sleep 5
python -u plotKinematics.py kinematics_preSel_noJSF_2016_6_22_WJetsHTbins 0 1
sleep 5
python -u plotKinematics.py kinematics_finalSelnoDR_noJSF_2016_6_22_WJetsHTbins 0 0
sleep 5
python -u plotKinematics.py kinematics_finalSelnoDR_noJSF_2016_6_22_WJetsHTbins 1 0
sleep 5
python -u plotKinematics.py kinematics_finalSelnoDR_noJSF_2016_6_22_WJetsHTbins 0 1
sleep 5
python -u plotKinematics.py kinematics_finalSel_noJSF_2016_6_22_WJetsHTbins 0 0
sleep 5
python -u plotKinematics.py kinematics_finalSel_noJSF_2016_6_22_WJetsHTbins 1 0
sleep 5
python -u plotKinematics.py kinematics_finalSel_noJSF_2016_6_22_WJetsHTbins 0 1
sleep 5

python -u plotKinematics.py kinematics_preSel_withJSF_2016_6_22 0 0
sleep 5
python -u plotKinematics.py kinematics_preSel_withJSF_2016_6_22 1 0
sleep 5
python -u plotKinematics.py kinematics_preSel_withJSF_2016_6_22 0 1
sleep 5
python -u plotKinematics.py kinematics_finalSelnoDR_withJSF_2016_6_22 0 0
sleep 5
python -u plotKinematics.py kinematics_finalSelnoDR_withJSF_2016_6_22 1 0
sleep 5
python -u plotKinematics.py kinematics_finalSelnoDR_withJSF_2016_6_22 0 1
sleep 5
python -u plotKinematics.py kinematics_finalSel_withJSF_2016_6_22 0 0
sleep 5
python -u plotKinematics.py kinematics_finalSel_withJSF_2016_6_22 1 0
sleep 5
python -u plotKinematics.py kinematics_finalSel_withJSF_2016_6_22 0 1
sleep 5

echo "DONE"

date