# singleLepAnalyzer

Analyzer for plotting the output of "StepX" ROOT files, slimmed versions of "LJMet" ROOT files.

makeKinematics: plot kinematic distributions. 
	-- Categories: E, M, All
	-- One distribution per category per job
	PREP:
	1. Edit weights.py and samples.py to define files/counts/xsecs
	2. Edit analyze.py to control TTree->Draw cuts/weights/hists
	3. Edit doHists.py to control histogram names/bins/labels, samples to run, cuts to apply, and files to read in
	4. Edit doCondorKinematics.py to control output directory, categories, and which distributions to plot.
	RUN:
	1. python -u doHists.py --> this is a test, does it crash?
	2. python -u doCondorKinematics.py
	PLOT:
	1. Edit doKinematics.py to control samples and uncertainties. This script converts pickle files to ROOT files and write a latex-formatted yield table
	2. python -u doKinematics.py
	3. python -u plotKinematics.py (edit for all plot-level controls)

makeCRs: plot ttbar and wjets control regions.
	-- Categories: lepton x N Top jets x N W jets x N b jets
	-- One job per category, giving one distribution (the main discriminant)
	PREP:
	1. Edit weights.py and samples.py to define files/counts/xsecs
	2. Edit analyze.py to control TTree->Draw cuts/weights/hists
	3. Edit doHists.py to control histogram names/bins/labels, samples to run, and files to read in
	4. Edit doCondorCRs.py to control output directory, categories, cuts, and which control region to plot.
	RUN:
	1. python -u doHists.py --> this is a test, does it crash?
	2. python -u doCondorCRs.py
	PLOT:
	1. Edit doCRs.py to control samples and uncertainties. This script converts pickle files to ROOT files and write a latex-formatted yield table
	2. python -u doCRs.py
	3. python -u plotCRs.py (edit for all plot-level controls)
	 
makeThetaTemplates: plot templates for 
	-- Categories: lepton x N Top jets x N W jets x N b jets
	-- One job per category, giving one distribution (the main discriminant)
	PREP:
	1. Edit weights.py and samples.py to define files/counts/xsecs
	2. Edit analyze.py to control TTree->Draw cuts/weights/hists
	3. Edit doHists.py to control histogram names/bins/labels, samples to run, and files to read in
	4. Edit doCondorThetaTemplates.py to control output directory, categories, and cuts. 
	RUN:
	1. python -u doHists.py --> this is a test, does it crash?
	2. python -u doCondorThetaTemplates.py
	PLOT:
	1. Edit doThetaTemplates.py to control samples and uncertainties. This script converts pickle files to ROOT files and write a latex-formatted yield table. You can choose to do a branching ratio scan here.
	2. Edit modifyBinning.py to control binning and add certain uncertainties
	3. python -u doThetaTemplates.py
	4. python -u modifyBinning.py
	3. python -u plotThetaTemplates.py (edit for all plot-level controls)


Uncertainties: various special scripts to treat them
	-- makeThetaTemplates/getCRUncerts.py: Given 3 yield files (templates, ttbar CR, wjets CR), this script returns flat uncertainties based on control regions corresponding to signal region categories.
	-- plotShapeShifts: creates plots of each individual shape uncertainty for cross checks

makeLimits: plot limits
	Prep:
	1. Set up theta_config_template(_*).py of your choice with your uncertainties
	2. Set up doThetaLimits.py with directories and an types of histograms to remove from the file
	RUN:
	1. python -u doThetaLimits.py
	PLOT:
	1. python -u PlotLimits.py
	
