#!/bin/bash

date

python -u modifyBinning.py ttbar_noJSF_notTag_2016_6_22 0.3
sleep 5
python -u modifyBinning.py ttbar_noJSF_notTag_2016_6_22_WJetsHTbins 0.3
sleep 5
python -u modifyBinning.py ttbar_withJSF_notTag_2016_6_22 0.3
sleep 5
python -u modifyBinning.py wjets_noJSF_notTag_2016_6_22 0.3
sleep 5
python -u modifyBinning.py wjets_noJSF_notTag_2016_6_22_WJetsHTbins 0.3
sleep 5
python -u modifyBinning.py wjets_withJSF_notTag_2016_6_22 0.3
sleep 5

echo "DONE"

date