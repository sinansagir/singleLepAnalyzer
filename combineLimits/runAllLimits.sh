#!/bin/bash

echo "--------------- Working on TT -------------------"

dir=limits_templatesSRCR_June2020100fb0p3smoothedL

echo "Singlet..."
python -u runLimits.py $dir bW0p5_tZ0p25_tH0p25
echo "Double..."
python -u runLimits.py $dir bW0p0_tZ0p5_tH0p5
echo "bW..."
python -u runLimits.py $dir bW1p0_tZ0p0_tH0p0
echo "tZ..."
python -u runLimits.py $dir bW0p0_tZ1p0_tH0p0
echo "tH..."
python -u runLimits.py $dir bW0p0_tZ0p0_tH1p0

echo "Plotting..."
python -u PlotLimits.py $dir 0.3 0.1 T

echo "--------------- Working on BB -------------------"

echo "Singlet..."
python -u runLimits.py $dir tW0p5_bZ0p25_bH0p25
echo "Double..."
python -u runLimits.py $dir tW0p0_bZ0p5_bH0p5
echo "tW..."
python -u runLimits.py $dir tW1p0_bZ0p0_bH0p0
echo "bZ..."
python -u runLimits.py $dir tW0p0_bZ1p0_bH0p0
echo "bH..."
python -u runLimits.py $dir tW0p0_bZ0p0_bH1p0

echo "Plotting..."
python -u PlotLimits.py $dir 0.3 0.1 B

echo "Done!"
