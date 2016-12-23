#!/bin/bash

date

echo "START"

cd "$1"/

combineTool.py -M T2W -i cmb/*0 -o workspace.root --parallel 16
sleep 10
combineTool.py -M Asymptotic -d cmb/*0/workspace.root --there -n .limit --parallel 16 #--rMin 0 --rMax 2.5
sleep 10
combineTool.py -M CollectLimits cmb/*0/*.limit.* --use-dirs -o limits.json
sleep 10
cd ../

echo "DONE"

date