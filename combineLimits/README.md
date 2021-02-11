## Combine setup

Combine should be run on an **SL7** machine. Follow the setup instructions for CMSSW_10_2_13 from the Combine Harvester documentation, in the [Getting Started section](https://cms-analysis.github.io/CombineHarvester/index.html).

Important documentation websites:
 * Higgs Combine: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/
   * Toys and snapshots: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/runningthetool/#toy-data-generation
   * Limits and blinding: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/commonstatsmethods/#asymptotic-frequentist-limits
   * Goodness of fit: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/commonstatsmethods/#goodness-of-fit-tests
   * Fit diagnostics: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#fitting-diagnostics
   * Impacts: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#nuisance-parameter-impacts
   * Channel masking: http://cms-analysis.github.io/HiggsAnalysis-CombinedLimit/part3/nonstandard/#channel-masking
 * Combine Harvester tool package: https://cms-analysis.github.io/CombineHarvester/index.html
   * Getting Started on that page has install instructions
   * Post-fit plots: https://cms-analysis.github.io/CombineHarvester/post-fit-shapes-ws.html
   * Limit collection: https://cms-analysis.github.io/CombineHarvester/limits.html


## Making ROOT files

Go back to makeTemplates and search for "Combine" in `doTemplates.py` and `modifyBinning.py`. Your ROOT files need to have the following formatting:
 * Channel__Process(__UncertUp/Down)
 * Data has the process name "data_obs"
 * Signals should all appear in the same file with process names like "signal$MASS", for $MASS = some number. 
 * No background or signal distributions should have integrals of 0 in any category -- fill in zeroes with some small number

## Making data cards
	
This is the first step for running Combine. All of the procedures below use the same data cards. 

 * `dataCard.py`: edit this script to instruct CombineHarvester to open certain ROOT files, learn channels from them, and add certain systematics to the data cards. 
 * `runDataCard.sh`: a wrapper to call dataCard.py with various arguments, e.g. branching ratio strings or control/signal regions. **Find examples of python script arguments here.**

Essentially, what `dataCard.py` will do is grab input root files, analyze the channels for that region, and make data cards from them for each mass point. You will need to specify which signal to analyze, which ROOT files to open, which uncertainties should be added to the data cards, and what the output directory should be called. The output directory will look something like `limits_(specified directory name)/(branching ratio)/(channel names)/(mass points)`. All of the text files are data cards. Within `limits_(specified directory name)/(branching ratio)/cmb/(mass points)/` you should see a file called `workspace.root`. This file holds a `RooFit` workspace created from the data card that combines all the channels. 

## Running limits

To run Asymptotic CLs limits and plot the results: 

 * `runLimits.py`: this script prepares a workspace file and runs **blinded** Asymptotic CLs limits. 
   * for this analysis, a fit is performed with signal region channels masked, and then the fit results are propagated to a new file called `morphedWorkspace.root`
   * Combine is called with the signal region channels unmasked to compute the limit. The option `--run=blind` is used for blinding.
   * Combine Harvester's limit collection script is used to write a .json file with the results
 * `PlotLimits.py`: this is a copy of the Theta limit plotter so that the graphics are the same. It reads the .json file to fill TGraphs. The plotter from Combine Harvester did not have a clean way to "blind" the plot. 
    * Several arguments are required to set up a meaningful output file name for the plots
    * The "multiplier" argument is **critical**: if your signal histograms are scaled to anything other than 1 pb cross section, give that value here in units of pb.
 * `runAllLimits.sh`: a wrapper to call runLimits.py for each branching fraction, and finally PlotLimits.py. **Find examples of python script arguments here.**

## Signal injection tests

B2G requires several signal injection tests for preapproval. The "bias test" probes whether the fit returns measurable signal when none was present ("injection" of 0 pb as the cross section). The "injection tests" probe whether the fit returns the correct amount of signal when a certain cross section is injected into the toy data.

 * `runSignalInjectionToys.py`: a script to run all the combine calls
   * First, it checks for a post-fit workspace with a snapshop and creates it if needed. The default is to fit to data in the CR, or to fit CR data with SR channels masked. 
   * Second, it loads that fit snapshot to generate N toys with a certain `--expectSignal R` injection setting.
   * Third, it fits the N toys within a reasonable range around the injected signal amount.
 * `signalInjectionPlotter.py`: this script opens the ROOT file created from fitting the toys and makes pull plots with Gaussian fits. 
 * `runAllSingletTests.sh`: a wrapper to call the previous scripts in combination with other tests. **Find examples of python script arguments here.**


## Impact plots

Impact plots are also required for preapproval and show how various nuisance parameters affect the best fit signal strength.

 * `runImpacts.py`: this script runs the set of combine commands needed to create the impact plot. It has options for masking/unmasking SR channels and assumes that an asimov dataset (-t -1) should be used in the SR, while data is used in the CR.
 * `plotImpacts.py`: a copy of the plotter from Combine Harvester. 
 * `runAllSingletTests.sh`: a wrapper to call the previous scripts in combination with other tests. **Find examples of python script arguments here.**
	
## Goodness of fit

This method is only run in the control region for now. It is difficult to test goodness of fit in a blinded way in the signal region. 

 * `runGOF.py`: calls the combine commands to calculated a "saturated chi2" value from data and from N toys.
 * `GofPlotter.py`: plots the chi2 values from the toys and extracts the data chi2 value to plot as a red line.
 * `runAllSingletTests.sh`: a wrapper to call the previous scripts in combination with other tests. **Find examples of python script arguments here.**

