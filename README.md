# singleLepAnalyzer

Analyzer for plotting the output of "StepX" ROOT files, slimmed versions of "LJMet" ROOT files.

-----------------------------------------------------------------------------------------------


makeTemplates: plot kinematic distributions and templates for limits 

	-- Categories: anything you define! see isEMlist, catList, tagList objects. Typically E/M/L for basic kinematics, more specific categories for limit templates.
	
	-- Regions: define "PS", "CR", "SR" cuts, or make new regions. Passed to analyze.py to control cuts

	-- One job per category, giving one distribution
	
	PREP:

	1. Edit weights.py and samples.py to define files/counts/xsecs

	2. Edit analyze.py to control TTree->Draw cuts/weights/hists. Teach it how to interpret your regions and categories.

	3. Edit doHists.py to control histogram names/bins/labels, samples to run, and files to read in

	4. Edit doCondorTemplates.py to control output directory, categories, and cuts. 

	RUN:

	1. python -u doHists.py --> this is a test, does it crash?

	2. python -u doCondorTemplates.py

	PLOT:

	1. Edit doTemplates.py to control samples and uncertainties. This script converts pickle files to ROOT files and write a latex-formatted yield table. You can choose to do a branching ratio scan here.

	2. Edit modifyBinning.py to control binning and add certain uncertainties. Edit runRebinning.sh to rebin multiple plots

	3. python -u doTemplates.py

	4. sh runRebinning.sh

	5. Edit plotTemplates.py for all plot-level controls, including systematic uncertainties. Edit runPlotting.sh for multiple plots.
	
	6. sh runPlotting.sh

-----------------------------------------------------------------------------------------------

Uncertainties: various special scripts to treat them

	-- makeTemplates/getCRUncerts.py: Given 3 yield files (templates, ttbar CR, wjets CR), this script returns flat uncertainties based on control regions corresponding to signal region categories.

	-- plotShapeShifts: creates plots of each individual shape uncertainty for cross checks

-----------------------------------------------------------------------------------------------

makeLimits: set limits

	Prep:

	1. Set up theta_config_template(_*).py of your choice with your uncertainties

	2. Set up doThetaLimits.py with directories and an types of histograms to remove from the file

	RUN:

	1. python -u doThetaLimits.py

	PLOT:

	1. python -u PlotLimits.py
	
