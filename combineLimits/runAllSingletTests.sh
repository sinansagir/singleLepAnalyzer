#!/bin/bash
echo "--------------- Working on CR for TT -------------------"

dir=limits_templatesCR_Feb2021_HTdnnL_100fbChi20p3FM
mass=1400TT
BR=bW0p5_tZ0p25_tH0p25

echo "Running bias test:"
python -u runSignalInjectionToys.py $dir $mass 0 500 >& $dir/$BR/cmb/1400/R0injection.log 
python -u signalInjectionPlotter.py $dir $mass 0

echo "Running nuisance plot:"
python -u diffNuisances.py -g $dir/$BR/cmb/1400/nuisancepulls.root $dir/$BR/cmb/1400/fitDiagnostics.root >& $dir/$BR/cmb/1400/nuisancepulls.txt

# echo "Running covariance plot:"
# python -u covariancePlotter.py $dir $mass

# echo "Running GOF test:"
# python -u runGOF.py $dir $mass 500 >& $dir/$BR/cmb/1400/GOF.log
# python -u GoFPlotter.py $dir $mass

# echo "Done!"

# echo "--------------- Working on CR for BB -------------------"

# dir=limits_templatesCR_Feb2021_HTdnnL_100fbChi20p3FM
# mass=1400BB
# BR=tW0p5_bZ0p25_bH0p25

# echo "Running bias test:"
# python -u runSignalInjectionToys.py $dir $mass 0 500 >& $dir/$BR/cmb/1400/R0injection.log 
# python -u signalInjectionPlotter.py $dir $mass 0

# echo "Running nuisance plot:"
# python -u diffNuisances.py -g $dir/$BR/cmb/1400/nuisancepulls.root $dir/$BR/cmb/1400/fitDiagnostics.root >& $dir/$BR/cmb/1400/nuisancepulls.txt

# echo "Running covariance plot:"
# python -u covariancePlotter.py $dir $mass

# echo "Running GOF test:"
# python -u runGOF.py $dir $mass 500 >& $dir/$BR/cmb/1400/GOF.log
# python -u GoFPlotter.py $dir $mass

# echo "Done!"

# echo "--------------- Working on SR+CR for TT -------------------"

# dir=limits_templatesSRCR_June2020100fb0p3smoothedL
# mass=1400
# BR=bW0p5_tZ0p25_tH0p25

# echo "Running bias test:"
# python -u runSignalInjectionToys.py $dir $mass 0 500 >& $dir/$BR/cmb/1400/R0injection.log 
# python -u signalInjectionPlotter.py $dir $mass 0

# echo "Running nuisance plot:"
# python -u diffNuisances.py -g $dir/$BR/cmb/1400/nuisancepulls.root $dir/$BR/cmb/1400/fitDiagnostics.root >& $dir/$BR/cmb/1400/nuisancepulls.txt

# echo "Running covariance plot:"
# python -u covariancePlotter.py $dir $mass

# echo "Running signal injection of r = 1:"
# python -u runSignalInjectionToys.py $dir $mass 1 500 >& $dir/$BR/cmb/1400/R1injection.log 
# python -u signalInjectionPlotter.py $dir $mass 1

# echo "Running signal injection of r = 5:"
# python -u runSignalInjectionToys.py $dir $mass 5 500 >& $dir/$BR/cmb/1400/R5injection.log 
# python -u signalInjectionPlotter.py $dir $mass 5

# echo "Running impact test:"
# python -u runImpacts.py $dir $mass >& $dir/$BR/cmb/1400/impacts.log
# python -u plotImpacts.py --input $dir/$BR/cmb/1400/impacts.json --output $dir/$BR/cmb/1400/impacts

# echo "Done!"

# echo "--------------- Working on SR+CR for BB -------------------"

# mass=1400BB
# BR=tW0p5_bZ0p25_bH0p25

# echo "Running bias test:"
# python -u runSignalInjectionToys.py $dir $mass 0 500 >& $dir/$BR/cmb/1400/R0injection.log 
# python -u signalInjectionPlotter.py $dir $mass 0

# echo "Running nuisance plot:"
# python -u diffNuisances.py -g $dir/$BR/cmb/1400/nuisancepulls.root $dir/$BR/cmb/1400/fitDiagnostics.root >& $dir/$BR/cmb/1400/nuisancepulls.txt

# echo "Running covariance plot:"
# python -u covariancePlotter.py $dir $mass

# echo "Running signal injection of r = 1:"
# python -u runSignalInjectionToys.py $dir $mass 1 500 >& $dir/$BR/cmb/1400/R1injection.log 
# python -u signalInjectionPlotter.py $dir $mass 1

# echo "Running signal injection of r = 5:"
# python -u runSignalInjectionToys.py $dir $mass 5 500 >& $dir/$BR/cmb/1400/R5injection.log 
# python -u signalInjectionPlotter.py $dir $mass 5

# echo "Running impact test:"
# python -u runImpacts.py $dir $mass >& $dir/$BR/cmb/1400/impacts.log
# python -u plotImpacts.py --input $dir/$BR/cmb/1400/impacts.json --output $dir/$BR/cmb/1400/impacts

# echo "Done!"

