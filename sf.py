#!/usr/bin/python

from ROOT import TFile
import sys

# f=TFile('makeTemplates/templates_R16_40vars_6j_NJetsCSV_053121lim_newbin1/templates_BDT_35p867fb_rebinned_stat0p3.root','READ')
# out=TFile('makeTemplates/templates_R16_40vars_6j_NJetsCSV_053121lim_newbin1/templates_BDT_35p867fb_tthscale_rebinned_stat0p3.root','RECREATE')

# f=TFile('makeTemplates/templates_R17_40vars_6j_NJetsCSV_053121lim_newbin1/templates_BDT_41p53fb_rebinned_stat0p3.root','READ')
# out=TFile('makeTemplates/templates_R17_40vars_6j_NJetsCSV_053121lim_newbin1/templates_BDT_41p53fb_tthscale_rebinned_stat0p3.root','RECREATE')

# f=TFile('makeTemplates/templates_R18_40vars_6j_NJetsCSV_053121lim_newbin1/templates_BDT_59p97fb_rebinned_stat0p3.root','READ')
# out=TFile('makeTemplates/templates_R18_40vars_6j_NJetsCSV_053121lim_newbin1/templates_BDT_59p97fb_tthscale_rebinned_stat0p3.root','RECREATE')

f=TFile(sys.argv[1],'READ')
out=TFile(sys.argv[2],'RECREATE')

# 'BDT_59p97fb_isM_nHOT1p_nT0p_nW0p_nB4p_nJ8p__tttt__lowessisr_R18Down'
# bkgs=['ttnobb','ttbb','ttH','top','ewk','qcd']
# data='data_obs'
# reg={
# 	'CR1':'nB2_nJ6p',
# 	'CR2':'nB2_nJ8p',
# 	'CR3':'nB3_nJ6p',
# 	'VR': 'nB4p_nJ6p',
# 	'SR1':'nB3_nJ8p',
# 	'SR2':'nB4p_nJ8p',
# }
hists=[i.GetName() for i in f.GetListOfKeys()]
out.cd()
for h in hists:
	print h
	a=f.Get(h).Clone()
	# if 'ttH' in h:
	# 	a.Scale(1.49)
	if 'ttbb' in h:
		a.Scale(1.30)
	a.Write()
out.Close()
f.Close()
