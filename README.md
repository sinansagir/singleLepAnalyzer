# singleLepAnalyzer

Analyzer for plotting the output of "StepX" ROOT files, slimmed versions of "LJMet" ROOT files.
	 
-----------------------------------------------------------------------------------------------

makeTemplates: produce templates for 

	-- Categories: lepton x N Top jets x N W jets x N b jets x N AK4 jets

	-- One job per category per distribution (either a list of kinematics or the main discriminant)

	PREP:

	1. Edit weights.py and samples.py to define files/counts/xsecs

	2. Edit analyze.py to control TTree->Draw cuts/weights/hists

	3. Edit doHists.py to control histogram names/bins/labels, samples to run, selections to apply, and files to read in

	4. Edit doCondorTemplates.py to control output directory, categories, region, and distributions. 

	RUN:

	1. python -u doHists.py --> this is a test, does it crash?

	2. python -u doCondorTemplates.py

	PLOT:

	1. Edit doTemplates.py to control samples and uncertainties. This script converts pickle files to ROOT files and write a latex-formatted yield table. You can choose to do a branching ratio scan here.

	2. Edit modifyBinning.py to control binning, add certain uncertainties, and produce new yield tables with shape uncertainties included (optional)

	3. python -u doTemplates.py

	4. python -u modifyBinning.py

	5. python -u plotTemplates.py (edit for all plot-level controls)

-----------------------------------------------------------------------------------------------

Uncertainties: various special scripts to treat them

	-- makeThetaTemplates/getCRUncerts.py: Given 3 yield files (templates, ttbar CR, wjets CR), this script returns flat uncertainties based on control regions corresponding to signal region categories.

	-- plotShapeShifts: creates plots of each individual shape uncertainty for cross checks

-----------------------------------------------------------------------------------------------

thetaLimits: set limits

	Prep:

	1. Set up theta_config_template(_*).py of your choice with your uncertainties

	2. Set up doThetaLimits.py with directories and an types of histograms to remove from the file

	RUN:

	1. python -u doThetaLimits.py

	PLOT:

	1. python -u PlotLimits.py
	
