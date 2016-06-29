#!/bin/bash

date

echo "doing 0.1"

python -u modifyBinning.py 0.1

sleep 5

echo "doing 0.15"

python -u modifyBinning.py 0.15

sleep 5

echo "doing 0.2"

python -u modifyBinning.py 0.2

sleep 5

echo "doing 0.3"

python -u modifyBinning.py 0.3

sleep 5

echo "doing 0.4"

python -u modifyBinning.py 0.4

sleep 5

echo "doing 0.5"

python -u modifyBinning.py 0.5

sleep 5

echo "doing 0.75"

python -u modifyBinning.py 0.75

sleep 5

echo "doing 1.0"

python -u modifyBinning.py 1.0

sleep 5

echo "doing 1e9"

python -u modifyBinning.py 1e9

sleep 5

echo "DONE"

date