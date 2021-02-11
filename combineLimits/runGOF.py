import os,sys

## Arguments: limit directory name; mass point; number of toys

## Make a datacard first with datacard.py!

limitdir = sys.argv[1]
mass = sys.argv[2]
nToys = int(sys.argv[3])

BR = 'bW0p5_tZ0p25_tH0p25'
if 'BB' in mass: BR = 'tW0p5_bZ0p25_bH0p25'
mass = mass.replace('BB','')

name = limitdir.replace('limits_templatesCR_June2020','').replace('limits_templatesSRCR_June2020','')
path = limitdir+'/'+BR+'/cmb/'+mass

os.chdir(path)

print 'Running background-only GOF with data'
print 'Command = combine -M GoodnessOfFit workspace.root --algo=saturated --fixedSignalStrength=0'
os.system('combine -M GoodnessOfFit workspace.root --algo=saturated')

print 'Running background-only GOF with toys, after frequentist fit'
print 'Command = combine -M GoodnessOfFit workspace.root --algo=saturated -t '+str(nToys)+' --toysFrequentist --fixedSignalStrength=0'
os.system('combine -M GoodnessOfFit workspace.root --algo=saturated -t '+str(nToys)+' --toysFrequentist --fixedSignalStrength=0')

print 'Done!'
