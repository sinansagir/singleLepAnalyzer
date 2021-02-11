# Use: python importPars.py <file with fit result> <card for other fit>
# Example: python importPars.py /path/to/CRfit/fitDiagnostics.root /path/to/SRfit/card.txt

import sys, subprocess, ROOT

toDrop = [] # parameter names to drop from import - I've left it empty as a placeholder

# First convert the card
#subprocess.call(['text2workspace.py -b '+sys.argv[2]+' -o morphedWorkspace.root'],shell=True)

# Open new workspace
w_f = ROOT.TFile.Open(sys.argv[2])
w = w_f.Get('w')

# Open fit result we want to import
fr_f = ROOT.TFile.Open(sys.argv[1])
fr = fr_f.Get('fit_b') # b-only fit result (fit_s for s+b)
myargs = ROOT.RooArgSet(fr.floatParsFinal())

# Drop any parameters we don't want imported
for p in toDrop:
      # For remove(), if parameter is found, it is dropped and true is returned. Else returns false (and we print a warning)
      if not myargs.remove(myargs.find(p)): 
            print 'WARNING: RooAbsArg "%s" was not found in the set of parameters and thus not removed.'%(p)

# Save snapshot and overwrite the original 'w'
w.saveSnapshot('initialFit',myargs,True) # turns out this will automatically check for common parameters and only import those

w_new = ROOT.TFile.Open('morphedWorkspace.root', 'RECREATE')
w_new.WriteTObject(w,'w','Overwrite')

w_f.Close()
w_new.Close()
fr_f.Close()

# Example use of output
# combine -M FitDiagnostics -d morphedWorkspace.root --snapshotName initialFit <other options>
