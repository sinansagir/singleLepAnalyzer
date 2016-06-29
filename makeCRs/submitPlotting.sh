#!/bin/bash

date

python -u plotCRs.py noJSF_notTag_2016_6_22 0 0 0
sleep 5
python -u plotCRs.py noJSF_notTag_2016_6_22 1 0 0
sleep 5
python -u plotCRs.py noJSF_notTag_2016_6_22 0 1 0
sleep 5

python -u plotCRs.py noJSF_notTag_2016_6_22 0 0 1
sleep 5
python -u plotCRs.py noJSF_notTag_2016_6_22 1 0 1
sleep 5
python -u plotCRs.py noJSF_notTag_2016_6_22 0 1 1
sleep 5

python -u plotCRs.py noJSF_notTag_2016_6_22_WJetsHTbins 0 0 0
sleep 5
python -u plotCRs.py noJSF_notTag_2016_6_22_WJetsHTbins 1 0 0
sleep 5
python -u plotCRs.py noJSF_notTag_2016_6_22_WJetsHTbins 0 1 0
sleep 5

python -u plotCRs.py noJSF_notTag_2016_6_22_WJetsHTbins 0 0 1
sleep 5
python -u plotCRs.py noJSF_notTag_2016_6_22_WJetsHTbins 1 0 1
sleep 5
python -u plotCRs.py noJSF_notTag_2016_6_22_WJetsHTbins 0 1 1
sleep 5

python -u plotCRs.py withJSF_notTag_2016_6_22 0 0 0
sleep 5
python -u plotCRs.py withJSF_notTag_2016_6_22 1 0 0
sleep 5
python -u plotCRs.py withJSF_notTag_2016_6_22 0 1 0
sleep 5

python -u plotCRs.py withJSF_notTag_2016_6_22 0 0 1
sleep 5
python -u plotCRs.py withJSF_notTag_2016_6_22 1 0 1
sleep 5
python -u plotCRs.py withJSF_notTag_2016_6_22 0 1 1
sleep 5

echo "DONE"

date