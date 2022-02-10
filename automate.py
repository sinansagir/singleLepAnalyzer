import os,time

# cmsswbase = '/user_data/ssagir/CMSSW_10_2_13/src'
cmsswbase = '/home/eusai/4t/CMSSW_10_2_16_UL/src'

trainings=[]

years=['16','17','18']#['16','17','18']#,16]
prod={
'16':'Oct2019',
'17':'Oct2019',
'18':'Oct2019',
}
# prod={
# '16':'Jan2021',
# '17':'Oct2019',
# '18':'Oct2019',
# }


# postfixes=[
# 'GOF_deepjet_2DHTSF_v2',
# 'GOF_deepjet_no2DHTSF_v2', 

# 'GOF_deepjet_2DHTSF_v3',
# 'GOF_deepjet_no2DHTSF_v3', 

# 'GOF_deepjet_2DHTSF',
# 'GOF_deepjet_no2DHTSF',

# '40vars_6j_NJetsCSV_v1',
# '50vars_6j_NJetsCSV_v1',
# '40vars_4j_NJetsCSV_v1',
# '50vars_4j_NJetsCSV_v1',

#######'40vars_6j_NJetsCSV',
# '50vars_6j_NJetsCSV',
    
    
# 'GOF_2DHTSF_v3',
# 'GOF_no2DHTSF_v3',

# 'GOF_angularfix_no2DHTSF',
# 'GOF_angularfix_2DHTSF',

 

# ]

# vrs=[
# 'BDT',
# 'thirdcsvb_bb',
# 'fourthcsvb_bb',
# 'NJetsCSVwithSF_MultiLepCalc',
# 'NJets_JetSubCalc',
# 'BDTtrijet2',
# 'AK4HTpMETpLepPt',
# 'sixthJetPt',
# 'PtFifthJet',
# 'hemiout',
# 'AK4HT',
# 'NJetsCSV_MultiLepCalc',
# ]
#'BDT',
# vrs=['thirdcsvb_bb',
# 'fourthcsvb_bb',
# 'NJetsCSV_MultiLepCalc',
# 'NJets_JetSubCalc',
# 'BDTtrijet2',
# 'AK4HTpMETpLepPt',
# 'sixthJetPt',
# 'PtFifthJet',
# 'hemiout',
# 'AK4HT']

#deepcsv
vrs=['BDT']
# vrs=['thirdcsvb_bb','fourthcsvb_bb','NJetsCSV_MultiLepCalc','NJets_JetSubCalc','BDTtrijet2','AK4HTpMETpLepPt',
# 'sixthJetPt','PtFifthJet','hemiout','AK4HT','BDTtrijet3','HT_bjets','fifthJetPt','ratio_HTdHT4leadjets','MT_lepMet',
# 'HT_2m','mass_maxBBmass','aveBBdr','mass_lepBJet0','deltaR_minBB','NresolvedTops1pFake','HOTGoodTrijet2_pTratio',
# 'HOTGoodTrijet2_mass','HOTGoodTrijet2_dijetmass','HOTGoodTrijet2_csvJetnotdijet','HOTGoodTrijet2_dRtridijet',
# 'mass_lepBJet_mindr','HOTGoodTrijet2_dRtrijetJetnotdijet','corr_met_MultiLepCalc','minMleppBjet','M_allJet_W',
# 'NJetsTtagged','BJetLeadPt','secondJetPt','deltaEta_maxBB','Aplanarity','centrality','FW_momentum_6','Sphericity',
# 'BDTtrijet1',]


#deepjet
# vrs=['thirddeepjetb','fourthdeepjetb','NJetsCSV_JetSubCalc','NJets_JetSubCalc','BDTtrijet2','AK4HTpMETpLepPt',
# 'sixthJetPt','PtFifthJet','hemiout','AK4HT','BDTtrijet3','HT_bjets','fifthJetPt','ratio_HTdHT4leadjets','MT_lepMet',
# 'HT_2m','mass_maxBBmass','aveBBdr','mass_lepBJet0','deltaR_minBB','NresolvedTops1pFake','HOTGoodTrijet2_pTratio',
# 'HOTGoodTrijet2_mass','HOTGoodTrijet2_dijetmass','HOTGoodTrijet2_deepjet_Jetnotdijet','HOTGoodTrijet2_dRtridijet',
# 'mass_lepBJet_mindr','HOTGoodTrijet2_dRtrijetJetnotdijet','corr_met_MultiLepCalc','minMleppBjet','M_allJet_W',
# 'NJetsTtagged','BJetLeadPt','secondJetPt','deltaEta_maxBB','Aplanarity','centrality','FW_momentum_6','Sphericity',
# 'BDTtrijet1',]

# vrs=['BDT','NJetsCSV_MultiLepCalc','NJets_JetSubCalc','thirdcsvb_bb','fourthcsvb_bb']

# vrs=[
# 'BDT_tt','BDT_ttH','BDT_ttbb',

# 'BDTsum',#BDT_tt + BDT_ttH + BDT_ttbb
# 'BDTprod',#(1+BDT_tt) * (1+BDT_ttH) * (1+BDT_ttbb)

# 'BDTtt+tth',#BDT_tt+BDT_ttH
# 'BDTtth+ttbb',#BDT_ttH+BDT_ttbb
# 'BDTtt+ttbb',#BDT_tt+BDT_ttbb

# 'BDTtt*tth',#BDT_tt*BDT_ttH
# 'BDTtth*ttbb',#BDT_ttH*BDT_ttbb
# 'BDTtt*ttbb',#BDT_tt*BDT_ttbb

# 'BDTtt+tthVSttbb',#BDT_tt+BDT_ttH vs BDT_ttbb
# 'BDTtth+ttbbVStt',#BDT_tt vs BDT_ttH+BDT_ttbb
# 'BDTtt+ttbbVStth',#BDT_tt+BDT_ttbb vs BDT_ttH 

# 'BDTtt*tthVSttbb',#(1+BDT_tt)*(1+BDT_ttH) vs (1+BDT_ttbb)
# 'BDTtth*ttbbVStt',#(1+BDT_tt) vs (1+BDT_ttH)*(1+BDT_ttbb)
# 'BDTtt*ttbbVStth',#(1+BDT_tt)*(1+BDT_ttbb) vs (1+BDT_ttH)  

# 'LBDT',#L(BDT_tt)*L(BDT_ttH)*L(BDT_ttbb)
# 'LBDTtt*tthVSttbb',#L(BDT_tt)*L(BDT_ttH) vs L(BDT_ttbb)
# 'LBDTtth*ttbbVStt',#L(BDT_tt) vs L(BDT_ttH)*L(BDT_ttbb)
# 'LBDTtt*ttbbVStth',#L(BDT_tt)*L(BDT_ttbb) vs L(BDT_ttH) 
# ]
# vrs=['BDT',
# 'NJets_JetSubCalc',
# 'fourthcsvb_bb',
# 'thirdcsvb_bb',
# 'sixthJetPt',
# 'ratio_HTdHT4leadjets',
# 'BDTtrijet2',
# 'AK4HTpMETpLepPt',
# 'AK4HT',
# 'fifthJetPt',
# 'NJetsCSV_MultiLepCalc',
# 'PtFifthJet',
# 'hemiout',
# 'HT_2m',
# 'BDTtrijet3',
# 'M_allJet_W',
# 'HT_bjets',
# 'FW_momentum_6',
# 'secondJetPt',
# 'NresolvedTops1pFake',
# 'FW_momentum_5',
# 'mass_lepBJet0',
# 'MT_lepMet',
# 'NJetsTtagged',
# 'FW_momentum_4',
# 'HOTGoodTrijet2_pTratio',
# 'HOTGoodTrijet2_dRtrijetJetnotdijet',
# 'HOTGoodTrijet2_dijetmass',
# 'HOTGoodTrijet2_mass',
# 'deltaR_minBB',
# 'HOTGoodTrijet2_dRtridijet',
# 'HOTGoodTrijet2_csvJetnotdijet',
# 'BDTtrijet1',
# 'Aplanarity',
# 'mass_maxBBmass',
# 'corr_met_MultiLepCalc',
# 'theJetLeadPt',
# 'BJetLeadPt',
# 'mass_lepBJet_mindr',
# 'Sphericity',
# 'HOTGoodTrijet1_mass']

# vrs=['BDT','AK4HT','AK4HTpMETpLepPt','Aplanarity','BDTtrijet1','BDTtrijet2','BDTtrijet3','BDTtrijet4','BJetLeadPt',
# 'FW_momentum_0','FW_momentum_1','FW_momentum_2','FW_momentum_3','FW_momentum_4','FW_momentum_5','FW_momentum_6',
# 'HOTGoodTrijet1_csvJetnotdijet','HOTGoodTrijet1_dRtridijet','HOTGoodTrijet1_dRtrijetJetnotdijet',
# 'HOTGoodTrijet1_dijetmass','HOTGoodTrijet1_mass','HOTGoodTrijet1_pTratio','HOTGoodTrijet2_csvJetnotdijet',
# 'HOTGoodTrijet2_dRtridijet','HOTGoodTrijet2_dRtrijetJetnotdijet','HOTGoodTrijet2_dijetmass','HOTGoodTrijet2_mass',
# 'HOTGoodTrijet2_pTratio','HT_2m','HT_bjets','MT2bb','MT_lepMet','M_allJet_W','NJetsCSV_MultiLepCalc',
# 'NJetsTtagged','NJetsWtagged','NJets_JetSubCalc','NresolvedTops1pFake','PtFifthJet','Sphericity','aveBBdr','aveCSVpt',
# 'centrality','corr_met_MultiLepCalc','csvJet3','csvJet4','deltaEta_maxBB','deltaPhi_lepJetInMinMljet',
# 'deltaPhi_lepbJetInMinMlb','deltaR_lepBJet_maxpt','deltaR_lepJetInMinMljet','deltaR_lepbJetInMinMlb','deltaR_minBB',
# 'fifthJetPt','fourthcsvb_bb','hemiout','lepDR_minBBdr','leptonPt_MultiLepCalc','mass_lepBJet0','mass_lepBJet_mindr',
# 'mass_lepJets0','mass_lepJets1','mass_lepJets2','mass_maxBBmass','mass_maxJJJpt','mass_minBBdr','mass_minLLdr',
# 'minDR_lepBJet','minMleppBjet','ratio_HTdHT4leadjets','secondJetPt','sixthJetPt','theJetLeadPt','thirdcsvb_bb']
#,'NJetsCSVwithSF_MultiLepCalc'

# /mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2016_Jan2021_4t_09072021_step3_wenyu/
# /mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_09072021_step3_wenyu/
# /mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_09072021_step3_wenyu/

for y in years:
		tmp={
		'year':'R'+y,
		# 'variable':['BDT'],
		# 'variable':['NPV'],
		'variable':vrs,#['BDT'],
		# 'postfix':p+'_053121pt50',#+'_lim',#'NoNBtagSF_'+p,
		# 'postfix':'multibdt_cr_2',#+'_lim',#'NoNBtagSF_'+p,
		# 'postfix':'jet12_50',#+'_lim',#'NoNBtagSF_'+p,
		 'postfix':'cr3hipu',
		#'postfix':'40vars_6j_NJetsCSV_053121lim910',
		#'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+y+'_'+prod[y]+'_4t_01272021_step3_wenyu/BDT_SepRank6j73vars2017year40top_40vars_mDepth2_6j_year20'+y+'_NJetsCSV/'
		# 'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+y+'_'+prod[y]+'_4t_03062021_step2/'#DeepCSV 
		#'path':  '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+y+'_'+prod[y]+'_4t_03092021_step2/'#DeepJet
		# 'path':  '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+y+'_'+prod[y]+'_4t_03162021_step2/'#DeepJet

		# 'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+y+'_'+prod[y]+'_4t_09072021_step3_wenyu/BDT_SepRank6j73vars2017Run40top_40vars_mDepth2_6j_year20'+y+'_NJetsCSV/' 
		# 'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+y+'_'+prod[y]+'_4t_053121_step3_40vars_6j_NJetsCSV_rmCSV', 
		# 'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+y+'_'+prod[y]+'_4t_053121_step3_40vars_6j_NJetsCSV',
		'path':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+y+'_'+prod[y]+'_4t_100621_step3_40vars_6j_NJetsCSV',
		# 'path':  '/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep20'+y+'_'+prod[y]+'_4t_03092021_step2p5/'#DeepJet
		}
		trainings.append(tmp)

# #for step2
trainings=[]
for y in years:

	# tmp={
	# 'year':'R'+y,
	# 'variable':vrs,
	# 'postfix':'cr3hipu',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':vrs,
	# 'postfix':'cr3lopu',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDT'],
	# 'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDT'],
	# 'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_bdtcorr_uncorrdsysyear',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	tmp={
	'year':'R'+y,
	'variable':['BDT'],
	'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_bdtcorr_uncorrdsysyearnj',#+'_lim',#'NoNBtagSF_'+p,
	'path':''
	}
	trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDT'],
	# 'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_no2b',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDT'],
	# 'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_bdtcorr',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)


	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDT'],
	# 'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_bdtcorr_no2b',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDT'],
	# 'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_bdtcorr_corrdsys',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)



	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDT'],
	# 'postfix':'40vars_6j_NJetsCSV_053121kin3',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDT'],
	# 'postfix':'40vars_6j_NJetsCSV_053121cr3',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDTYLD'],
	# 'postfix':'jet40',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDTYLD'],
	# 'postfix':'jet50',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDTYLD'],
	# 'postfix':'lopu',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['BDTYLD'],
	# 'postfix':'hipu',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['NPV'],
	# 'postfix':'pu',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':['NPV'],
	# 'postfix':'pukin',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

	# tmp={
	# 'year':'R'+y,
	# 'variable':vrs,
	# 'postfix':'40vars_6j_NJetsCSV_053121cr3',#+'_lim',#'NoNBtagSF_'+p,
	# 'path':''
	# }
	# trainings.append(tmp)

# for y in ['18']:
	
# 	tmp={
# 	'year':'R'+y,
# 	'variable':vrs,
# 	'postfix':'cr3hipu',#+'_lim',#'NoNBtagSF_'+p,
# 	'path':''
# 	}
# 	trainings.append(tmp)

# 	tmp={
# 	'year':'R'+y,
# 	'variable':vrs,
# 	'postfix':'cr3lopu',#+'_lim',#'NoNBtagSF_'+p,
# 	'path':''
# 	}
# 	trainings.append(tmp)





combinations = [

# {
# 	'variable':'BDT',
# 	'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1'
# },

# {
# 	'variable':'BDT',
# 	'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_no2b'
# },

# {
# 	'variable':'BDT',
# 	'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_bdtcorr'
# },

# {
# 	'variable':'BDT',
# 	'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_bdtcorr_no2b'
# },
# {
# 	'variable':'BDT',
# 	'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_bdtcorr_corrdsys'
# },

{
	'variable':'BDT',
	'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_bdtcorr_uncorrdsysyear'
},

{
	'variable':'BDT',
	'postfix':'40vars_6j_NJetsCSV_053121lim_newbin1_bdtcorr_uncorrdsysyearnj'
},
	

]

# for v in vrs:
# 	cm={'variable':v,'postfix':'multibdt_cr_1'}
# 	combinations.append(cm)
# 	cm={'variable':v,'postfix':'multibdt_cr_2'}
# 	combinations.append(cm)




#which step would you like to run?
#1 doCondorTemplates
#2 doTemplates
#3 modifyBinning + plotTemplates
#4 dataCard + limit + significance
#5 combination limit + significance
#6 print results
step=6

if step==1:
	os.chdir('makeTemplates')
	for train in trainings:
		for v in train['variable']:
			os.system('python doCondorTemplates.py '+train['year']+' '+v+' '+train['postfix']+' '+train['path'])
			time.sleep(2)
	os.chdir('..')

if step==2:
	os.chdir('makeTemplates')
	for train in trainings:
		shell_name = 'cfg/condor_step2_'+train['year']+'_'+train['postfix']+'.sh'
		shell=open(shell_name,'w')
		shell.write(
'#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd '+cmsswbase+'\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
python doTemplates.py '+train['year']+' '+train['postfix']+'\n')
		shell.close()
		jdf_name = 'cfg/condor_step2_'+train['year']+'_'+train['postfix']+'.job'
		jdf=open(jdf_name,'w')
		jdf.write(
'universe = vanilla\n\
Executable = '+os.getcwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 5000\n\
Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.out\n\
Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.err\n\
Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
		jdf.close()
		os.system('condor_submit '+jdf_name)
		print(shell_name)
		# os.system('source '+shell_name+' & ')
		time.sleep(1)
	os.chdir('..')



if step==3:
	os.chdir('makeTemplates')
	for train in trainings:
		for v in train['variable']:
			shell_name = 'cfg/condor_step3_'+train['year']+'_'+train['postfix']+'_'+v+'.sh'
			shell=open(shell_name,'w')
			shell.write(
'#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd '+cmsswbase+'\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
# python modifyTemplates.py '+train['year']+' '+v+' '+train['postfix']+'\n\
python modifyBinning.py '+train['year']+' '+v+' '+train['postfix']+'\n\
# python plotFullRun2.py '+v+' '+train['postfix']+'\n\
# python plotTemplates.py '+train['year']+' '+v+' '+train['postfix']+'\n')
			shell.close()
			jdf_name = 'cfg/condor_step3_'+train['year']+'_'+train['postfix']+'_'+v+'.job'
			jdf=open(jdf_name,'w')
			jdf.write(
'universe = vanilla\n\
Executable = '+os.getcwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 3072\n\
Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.out\n\
Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.err\n\
Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
			jdf.close()
			os.system('condor_submit '+jdf_name)
			# print(shell_name)
			# os.system('source '+shell_name+' & ')
			# time.sleep(2)
	os.chdir('..')



if step==4:
	os.chdir('combineLimits')
	for train in trainings:
		for v in train['variable']:
			shell_name = 'cfg/condor_step4_'+train['year']+'_'+train['postfix']+'_'+v+'.sh'
			shell=open(shell_name,'w')
			shell.write(
'#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd '+cmsswbase+'\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
# python dataCard.py '+train['year']+' '+v+' '+train['postfix']+'\n\
python dataCardDecoupleTTbarUncs.py '+train['year']+' '+v+' '+train['postfix']+'\n\
cd limits_'+train['year']+'_'+train['postfix']+'_'+v+'\n\
combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> sig_exp.txt\n\
combine -M Significance cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> sig_obs.txt\n\
combine -M AsymptoticLimits cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> asy.txt\n\
# combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> sig_exp_freezetth.txt\n\
# combine -M Significance cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> sig_obs_freezetth.txt\n\
# combine -M AsymptoticLimits cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> asy_freezetth.txt\n\
# combine -M Significance cmb/workspace.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> sig_exp_freezetthf.txt\n\
# combine -M Significance cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> sig_obs_freezetthf.txt\n\
# combine -M AsymptoticLimits cmb/workspace.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> asy_freezetthf.txt\n\
# combine -M MultiDimFit cmb/workspace.root --cminDefaultMinimizerStrategy 0 &> mlfit.txt\n\
cd ..\n')
			shell.close()
			jdf_name = 'cfg/condor_step4_'+train['year']+'_'+train['postfix']+'_'+v+'.job'
			jdf=open(jdf_name,'w')
			jdf.write(
'universe = vanilla\n\
Executable = '+os.getcwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 3072\n\
Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.out\n\
Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.err\n\
Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
			jdf.close()
			os.system('condor_submit '+jdf_name)
	os.chdir('..')


if step==5:
	os.chdir('combineLimits')
	for c in combinations:
		combo=c['postfix']+'_'+c['variable']
		shell_name = 'cfg/condor_step5_'+combo+'.sh'
		shell=open(shell_name,'w')
		shell.write(
'#!/bin/bash\n\
source /cvmfs/cms.cern.ch/cmsset_default.sh\n\
cd '+cmsswbase+'\n\
eval `scramv1 runtime -sh`\n\
cd '+os.getcwd()+'\n\
combineCards.py R16=limits_R16_'+combo+'/cmb/combined.txt.cmb R17=limits_R17_'+combo+'/cmb/combined.txt.cmb R18=limits_R18_'+combo+'/cmb/combined.txt.cmb &> BDTcomb/'+combo+'.txt\n\
text2workspace.py  BDTcomb/'+combo+'.txt  -o BDTcomb/'+combo+'.root\n\
combine -M Significance BDTcomb/'+combo+'.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> BDTcomb/sig_exp_'+combo+'.txt\n\
combine -M Significance BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> BDTcomb/sig_obs_'+combo+'.txt\n\
combine -M AsymptoticLimits BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 &> BDTcomb/asy_'+combo+'.txt\n\
# combine -M Significance BDTcomb/'+combo+'.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> BDTcomb/sig_exp_'+combo+'_freezetth.txt\n\
# combine -M Significance BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> BDTcomb/sig_obs_'+combo+'_freezetth.txt\n\
# combine -M AsymptoticLimits BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters lowessfsr_ttH,lowessisr_ttH,lowessmuRF_ttH,xsec_ttH &> BDTcomb/asy_'+combo+'_freezetth.txt\n\
# combine -M Significance BDTcomb/'+combo+'.root -t -1 --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> BDTcomb/sig_exp_'+combo+'_freezetthf.txt\n\
# combine -M Significance BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> BDTcomb/sig_obs_'+combo+'_freezetthf.txt\n\
# combine -M AsymptoticLimits BDTcomb/'+combo+'.root --expectSignal=1 --cminDefaultMinimizerStrategy 0 --freezeParameters ttHF &> BDTcomb/asy_'+combo+'_freezetthf.txt\n\
\n')
		shell.close()
		jdf_name = 'cfg/condor_step5_'+combo+'.job'
		jdf=open(jdf_name,'w')
		jdf.write(
'universe = vanilla\n\
Executable = '+os.getcwd()+'/'+shell_name+'\n\
Should_Transfer_Files = YES\n\
WhenToTransferOutput = ON_EXIT\n\
request_memory = 3072\n\
Output = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.out\n\
Error = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.err\n\
Log = '+os.getcwd()+'/log/'+shell_name.split('.')[0].split('/')[1]+'.log\n\
Notification = Error\n\
Arguments = \n\
Queue 1\n')
		jdf.close()
		os.system('condor_submit '+jdf_name)
	os.chdir('..')

def printlim(spec,year,variable,isComb,pfix):

	try:
		inputDir='limits_'+year+'_'+spec+'_'+variable
		sigExpFile = inputDir+'/sig_exp'+pfix+'.txt'
		sigObsFile = inputDir+'/sig_obs'+pfix+'.txt'
		limFile = inputDir+'/asy'+pfix+'.txt'
		if isComb:
			inputDir='BDTcomb/'
			sigExpFile = inputDir+'/sig_exp_'+spec+'_'+variable+pfix+'.txt'
			sigObsFile = inputDir+'/sig_obs_'+spec+'_'+variable+pfix+'.txt'
			limFile = inputDir+'/asy_'+spec+'_'+variable+pfix+'.txt'

		sigExpData = open(sigExpFile,'r').read()
		sigExplines = sigExpData.split('\n')
		sigObsData = open(sigObsFile,'r').read()
		sigObslines = sigObsData.split('\n')
		limData = open(limFile,'r').read()
		limlines = limData.split('\n')
		theSigExp = ''
		theSigObs = ''
		theLim = ['']*6
		for line in sigExplines:
			if line.startswith('Significance:'): theSigExp = line.split()[-1]
		for line in sigObslines:
			if line.startswith('Significance:'): theSigObs = line.split()[-1]
		for line in limlines:
			if line.startswith('Observed Limit:'): theLim[5] =  "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected  2.5%:'): theLim[0] =  "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 16.0%:'): theLim[1] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 50.0%:'): theLim[2] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 84.0%:'): theLim[3] = "{:.2f}".format(float(line.split()[-1])*12)
			if line.startswith('Expected 97.5%:'): theLim[4] = "{:.2f}".format(float(line.split()[-1])*12)
		print year+' , '+variable+' , '+spec+pfix+' , '+theSigObs+' , '+theSigExp+' , '+theLim[5]+' , '+theLim[2]+' , '+theLim[1]+' , '+theLim[3]+' , '+theLim[0]+' , '+theLim[4]
	except Exception as e:
		pass

if step==6:
	# print 'Year , Var , Specifications , Exp. Sig. , Obs. Sig. , -2sigma, -1sigma, central, +1sigma, +2sigma, Obs. Limit'
	print 'Year , Var , Specifications , Obs. Sig. , Exp. Sig. , Obs. Limit , central , -1sigma, +1sigma, -2sigma , +2sigma'
	os.chdir('combineLimits')
	for train in trainings:
		for v in train['variable']:
			printlim(train['postfix'] , train['year'] , v ,False,'')
			# printlim(train['postfix'] , train['year'] , v ,False,'_freezetth')
			# printlim(train['postfix'] , train['year'] , v ,False,'_freezetthf')
	for combo in combinations:
		printlim(combo['postfix'],'R16+17+18',combo['variable'],True,'')
		# printlim(combo['postfix'],'R16+17+18',combo['variable'],True,'_freezetth')
		# printlim(combo['postfix'],'R16+17+18',combo['variable'],True,'_freezetthf')
	os.chdir('..')

# standalone commands
# in makeTemplates:
# python doCondorTemplates.py R17 BDT 40vars_6j /mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_05182020_step3_wenyu/BDT_SepRank6j73vars2017year40top_40vars_mDepth2_4j_year2018/
# python doTemplates.py R17 40vars_6j
# python modifyBinning.py R17 BDT 40vars_6j
# python plotTemplates.py R17 BDT 40vars_6j
# in combineLimits:
# python dataCard.py R17 BDT 40vars_6j
