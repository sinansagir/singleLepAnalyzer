# mkdir $1_impacts
# mkdir $1_impacts_unblind
# ulimit -s unlimited

# cd $1_impacts

# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 --doInitialFit --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doInitialFit_SL_stat15 --cminDefaultMinimizerType Minuit
# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 --doFits --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doFits_SL_stat15 --exclude rgx\{prop_bin.*\} --cminDefaultMinimizerType Minuit
# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 -o impacts_SL_stat15.json --exclude rgx\{prop_bin.*\}
# # plotImpacts.py -i impacts_SL_stat15.json -o impacts_SL_stat15

# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 --doInitialFit --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doInitialFit_SL_stat15 --cminDefaultMinimizerType Minuit --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 --doFits --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doFits_SL_stat15 --exclude rgx\{prop_bin.*\} --cminDefaultMinimizerType Minuit --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 -o impacts_SL_stat15.json --exclude rgx\{prop_bin.*\} --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
# # plotImpacts.py -i impacts_SL_stat15.json -o impacts_SL_stat15

# cd ../$1_impacts_unblind

# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 --doInitialFit --robustFit 1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doInitialFit_SL_stat15 --cminDefaultMinimizerType Minuit
# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 --doFits --robustFit 1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doFits_SL_stat15 --exclude rgx\{prop_bin.*\} --cminDefaultMinimizerType Minuit
# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 -o impacts_SL_stat15.json --exclude rgx\{prop_bin.*\}
# # plotImpacts.py -i impacts_SL_stat15.json -o impacts_SL_stat15

# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 --doInitialFit --robustFit 1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doInitialFit_SL_stat15 --cminDefaultMinimizerType Minuit --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 --doFits --robustFit 1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doFits_SL_stat15 --exclude rgx\{prop_bin.*\} --cminDefaultMinimizerType Minuit --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
# # combineTool.py -M Impacts -d ../limits_$1/cmb/workspace.root -m 125 -o impacts_SL_stat15.json --exclude rgx\{prop_bin.*\} --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
# # plotImpacts.py -i impacts_SL_stat15.json -o impacts_SL_stat15

# cd ../


#combination

cd BDTcomb
mkdir $1_impacts 
mkdir $1_impacts_unblind
ulimit -s unlimited

cd $1_impacts

# combineTool.py -M Impacts -d ../$1.root -m 125 --doInitialFit --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doInitialFit_SL_stat15 --cminDefaultMinimizerType Minuit
# combineTool.py -M Impacts -d ../$1.root -m 125 --doFits --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doFits_SL_stat15 --exclude rgx\{prop_bin.*\} --cminDefaultMinimizerType Minuit
# combineTool.py -M Impacts -d ../$1.root -m 125 -o impacts_SL_stat15.json --exclude rgx\{prop_bin.*\}
# plotImpacts.py -i impacts_SL_stat15.json -o impacts_SL_stat15

# combineTool.py -M Impacts -d ../$1.root -m 125 --doInitialFit --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doInitialFit_SL_stat15 --cminDefaultMinimizerType Minuit --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
# combineTool.py -M Impacts -d ../$1.root -m 125 --doFits --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doFits_SL_stat15 --exclude rgx\{prop_bin.*\} --cminDefaultMinimizerType Minuit --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
combineTool.py -M Impacts -d ../$1.root -m 125 -o impacts_SL_stat15.json --exclude rgx\{prop_bin.*\} --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
plotImpacts.py -i impacts_SL_stat15.json -o impacts_SL_stat15

cd ../$1_impacts_unblind

# combineTool.py -M Impacts -d ../$1.root -m 125 --doInitialFit --robustFit 1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doInitialFit_SL_stat15 --cminDefaultMinimizerType Minuit
# combineTool.py -M Impacts -d ../$1.root -m 125 --doFits --robustFit 1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doFits_SL_stat15 --exclude rgx\{prop_bin.*\} --cminDefaultMinimizerType Minuit
# combineTool.py -M Impacts -d ../$1.root -m 125 -o impacts_SL_stat15.json --exclude rgx\{prop_bin.*\}
# plotImpacts.py -i impacts_SL_stat15.json -o impacts_SL_stat15

# combineTool.py -M Impacts -d ../$1.root -m 125 --doInitialFit --robustFit 1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doInitialFit_SL_stat15 --cminDefaultMinimizerType Minuit --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
# combineTool.py -M Impacts -d ../$1.root -m 125 --doFits --robustFit 1 --expectSignal 1 --rMin -100 --setRobustFitTolerance 0.2 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --task-name doFits_SL_stat15 --exclude rgx\{prop_bin.*\} --cminDefaultMinimizerType Minuit --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
combineTool.py -M Impacts -d ../$1.root -m 125 -o impacts_SL_stat15.json --exclude rgx\{prop_bin.*\} --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH
plotImpacts.py -i impacts_SL_stat15.json -o impacts_SL_stat15

cd ../../


###################

# cd $1
# mkdir impacts 
# cd impacts

# cd BDTcomb
# mkdir $1_impacts 
# cd $1_impacts

# ####

# # combineTool.py -M Impacts -d ../cmb/workspace.root -m 125 --doInitialFit --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0
# # combineTool.py -M Impacts -d ../cmb/workspace.root -m 125 --doFits --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --merge 10

# combineTool.py -M Impacts -d ../$1_BDT.root -m 125 --doInitialFit --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0
# combineTool.py -M Impacts -d ../$1_BDT.root -m 125 --doFits --robustFit 1 -t -1 --expectSignal 1 --rMin -100 --X-rtd MINIMIZER_analytic --cminDefaultMinimizerStrategy 0 --job-mode condor --merge 10  --exclude rgx\{prop_bin.*\}

# ####

# # combineTool.py -M Impacts -d ../cmb/workspace.root -m 125 -o impact.json
# # plotImpacts.py -i impact.json -o impact_out

# # combineTool.py -M Impacts -d ../$1_BDT.root -m 125 -o impact.json
# # plotImpacts.py -i impact.json -o impact_out


# ######

# cd ../../