# /home/wzhang/work/fwljmet_201905/CMSSW_10_2_16_UL/src/singleLepAnalyzer/makeTemplates/kinematics_SR_R17_BDTvars_2020_8_25/plots/GOFtests_AK4HT_41p53fb.txt
# /home/wzhang/work/fwljmet_201905/CMSSW_10_2_16_UL/src/singleLepAnalyzer/makeTemplates/kinematics_SR_R18_BDTvars_2020_8_25/plots/GOFtests_AK4HT_59p97fb.txt
# /home/wzhang/work/fwljmet_201905/CMSSW_10_2_16_UL/src/singleLepAnalyzer/makeTemplates/kinematics_SR_R17_BDTvars_2020_9_8/plots/GOFtests_AK4HT_41p53fb.txt
# /home/wzhang/work/fwljmet_201905/CMSSW_10_2_16_UL/src/singleLepAnalyzer/makeTemplates/kinematics_SR_R18_BDTvars_2020_9_8/plots/GOFtests_AK4HT_59p97fb.txt

# ---------------------------------------------------------------------------------------------------
# Categories                      prob_KS          prob_KS_X   prob_chi2           chi2            ndof  
# ---------------------------------------------------------------------------------------------------
# isE_nHOT0p_nT0p_nW0p_nB2p_nJ4p  1.0              0.651       0.99993588163       45.3002728977   87    
# isM_nHOT0p_nT0p_nW0p_nB2p_nJ4p  0.94286956548    0.0         1.19751253294e-07   173.001151578   87    
# isL_nHOT0p_nT0p_nW0p_nB2p_nJ4p  0.999966204121   0.007       0.94605265336       66.9075727342   87  

#Categories, prob_KS, prob_KS_X, prob_KS_X_switch, prob_KS_stat, prob_KS_X_stat, prob_KS_X_stat_switch, prob_chi2, chi2, prob_chi2_stat, chi2_stat, ndof  

# https://www.dropbox.com/home/fourtops/BDT/kinematics_step2_0812_year2017/isL?preview=BDTtrijet3_41p53fb_isL_nB2p_nJ4p_logy.png
# https://www.dropbox.com/home/fourtops/BDT/kinematics_step2_0812_year2017/isL?preview=HOTGoodTrijet2_dRtrijetJetnotdijet_41p53fb_isL_nB2p_nJ4_logy.png

# folders=['/home/wzhang/work/fwljmet_201905/CMSSW_10_2_16_UL/src/singleLepAnalyzer/makeTemplates/kinematics_SR_R17_BDTvars_2020_8_25/plots/GOFtests_',
# '/home/wzhang/work/fwljmet_201905/CMSSW_10_2_16_UL/src/singleLepAnalyzer/makeTemplates/kinematics_SR_R18_BDTvars_2020_8_25/plots/GOFtests_',
# '/home/wzhang/work/fwljmet_201905/CMSSW_10_2_16_UL/src/singleLepAnalyzer/makeTemplates/kinematics_SR_R17_BDTvars_2020_9_8/plots/GOFtests_',
# '/home/wzhang/work/fwljmet_201905/CMSSW_10_2_16_UL/src/singleLepAnalyzer/makeTemplates/kinematics_SR_R18_BDTvars_2020_9_8/plots/GOFtests_']

base='/home/eusai/4t/singleLepAnalyzer/makeTemplates/'
tail = '/plots/GOFtests_'

folders = [

# base+'templates_R17_New_StdBin_4p'+tail,
# base+'templates_R17_New_FineBin10_4p'+tail,

# base+'templates_R17_StdBin_234pB'+tail,
# base+'templates_R17_StdBin_456p'+tail,
# base+'templates_R17_StdBin_4p'+tail,
# base+'templates_R17_FineBin10_4p'+tail,

# base+'templates_R18_StdBin_234pB'+tail,
# base+'templates_R18_StdBin_456p'+tail,
# base+'templates_R18_StdBin_4p'+tail,
# base+'templates_R18_FineBin10_4p'+tail,

# base+'templates_R16_GOF'+tail,
# base+'templates_R17_GOF'+tail,
# base+'templates_R18_GOF'+tail,

# base+'templates_R17_GOF'+tail,

# base+'templates_R17_GOF_angularfix_2DHTSF'+tail,
# base+'templates_R17_GOF_angularfix_no2DHTSF'+tail,

# base+'templates_R17_GOF_2DHTSF_v3'+tail,
# base+'templates_R17_GOF_no2DHTSF_v3'+tail,

base+'templates_R16_40vars_6j_NJetsCSV_053121cr3'+tail,
base+'templates_R17_40vars_6j_NJetsCSV_053121cr3'+tail,
base+'templates_R18_40vars_6j_NJetsCSV_053121cr3'+tail,

# base+'templates_R18_cr3lopu'+tail,
# base+'templates_R18_cr3hipu'+tail,

# base+'templates_R17_GOF_deepjet_2DHTSF'+tail,
# base+'templates_R17_GOF_deepjet_no2DHTSF'+tail,

# base+'templates_R17_GOF_deepjet_2DHTSF_v3'+tail,
# base+'templates_R17_GOF_deepjet_no2DHTSF_v3'+tail,





]

isdeepjet=False

rebins=[
# '',
'_merge_rebinned_statVar',
# '_no1stbin',
# '_rebinned_stat0p3_no1stbin',
# '_rebinned_stat0p301_10pEvts_no1stbin',
# '_rebinned_stat0p301_10pEvts',
#'norebin',
#'rebinned_stat0p3_rebin',
#'rebinned_stat0p301_noemptybin'
]

# variables=['AK4HT','AK4HTpMETpLepPt','Aplanarity','BDTtrijet1','BDTtrijet2','BDTtrijet3','BDTtrijet4','BJetLeadPt',
# 'FW_momentum_0','FW_momentum_1','FW_momentum_2','FW_momentum_3','FW_momentum_4','FW_momentum_5','FW_momentum_6',
# 'HOTGoodTrijet1_csvJetnotdijet','HOTGoodTrijet1_dRtridijet','HOTGoodTrijet1_dRtrijetJetnotdijet',
# 'HOTGoodTrijet1_dijetmass','HOTGoodTrijet1_mass','HOTGoodTrijet1_pTratio','HOTGoodTrijet2_csvJetnotdijet',
# 'HOTGoodTrijet2_dRtridijet','HOTGoodTrijet2_dRtrijetJetnotdijet','HOTGoodTrijet2_dijetmass','HOTGoodTrijet2_mass',
# 'HOTGoodTrijet2_pTratio','HT_2m','HT_bjets','MT2bb','MT_lepMet','M_allJet_W','NJetsCSVwithSF_MultiLepCalc','NJetsCSV_MultiLepCalc',
# 'NJetsTtagged','NJetsWtagged','NJets_JetSubCalc','NresolvedTops1pFake','PtFifthJet','Sphericity','aveBBdr','aveCSVpt',
# 'centrality','corr_met_MultiLepCalc','csvJet3','csvJet4','deltaEta_maxBB','deltaPhi_lepJetInMinMljet',
# 'deltaPhi_lepbJetInMinMlb','deltaR_lepBJet_maxpt','deltaR_lepJetInMinMljet','deltaR_lepbJetInMinMlb','deltaR_minBB',
# 'fifthJetPt','fourthcsvb_bb','hemiout','lepDR_minBBdr','leptonPt_MultiLepCalc','mass_lepBJet0','mass_lepBJet_mindr',
# 'mass_lepJets0','mass_lepJets1','mass_lepJets2','mass_maxBBmass','mass_maxJJJpt','mass_minBBdr','mass_minLLdr',
# 'minDR_lepBJet','minMleppBjet','ratio_HTdHT4leadjets','secondJetPt','sixthJetPt','theJetLeadPt','thirdcsvb_bb']

variables=[
'NJets_JetSubCalc',
'fourthcsvb_bb',
'thirdcsvb_bb',
'sixthJetPt',
'ratio_HTdHT4leadjets',
'BDTtrijet2',
'AK4HTpMETpLepPt',
'AK4HT',
'fifthJetPt',
'NJetsCSV_MultiLepCalc',
'PtFifthJet',
'hemiout',
'HT_2m',
'BDTtrijet3',
'M_allJet_W',
'HT_bjets',
'FW_momentum_6',
'secondJetPt',
'NresolvedTops1pFake',
'FW_momentum_5',
'mass_lepBJet0',
'MT_lepMet',
'NJetsTtagged',
'FW_momentum_4',
'HOTGoodTrijet2_pTratio',
'HOTGoodTrijet2_dRtrijetJetnotdijet',
'HOTGoodTrijet2_dijetmass',
'HOTGoodTrijet2_mass',
'deltaR_minBB',
'HOTGoodTrijet2_dRtridijet',
'HOTGoodTrijet2_csvJetnotdijet',
'BDTtrijet1',
'Aplanarity',
'mass_maxBBmass',
'corr_met_MultiLepCalc',
'theJetLeadPt',
'BJetLeadPt',
'mass_lepBJet_mindr',
'Sphericity',
'HOTGoodTrijet1_mass']
# if isdeepjet:
# 	variables=['thirddeepjetb','fourthdeepjetb','NJetsCSV_JetSubCalc','NJets_JetSubCalc','BDTtrijet2','AK4HTpMETpLepPt',
# 'sixthJetPt','PtFifthJet','hemiout','AK4HT','BDTtrijet3','HT_bjets','fifthJetPt','ratio_HTdHT4leadjets','MT_lepMet',
# 'HT_2m','mass_maxBBmass','aveBBdr','mass_lepBJet0','deltaR_minBB','NresolvedTops1pFake','HOTGoodTrijet2_pTratio',
# 'HOTGoodTrijet2_mass','HOTGoodTrijet2_dijetmass','HOTGoodTrijet2_deepjet_Jetnotdijet','HOTGoodTrijet2_dRtridijet',
# 'mass_lepBJet_mindr','HOTGoodTrijet2_dRtrijetJetnotdijet','corr_met_MultiLepCalc','minMleppBjet','M_allJet_W',
# 'NJetsTtagged','BJetLeadPt','secondJetPt','deltaEta_maxBB','Aplanarity','centrality','FW_momentum_6','Sphericity',
# 'BDTtrijet1',]

data=[]

lumi={'R16':'35p867fb','R18':'59p97fb', 'R17':'41p53fb'}
# newstr={True:'_New',False:''}
import pandas as pd
ranking=pd.read_csv('ranking40.csv')
# if isdeepjet:
# 	ranking=pd.read_csv('rankingdeep40.csv')

for f in folders:
	for r in rebins:
		for v in variables:
			year='R17'
			if '_R18_' in f:
				year='R18'
			if '_R16_' in f:
				year='R16'
			filename=f+v+'_'+lumi[year]+r+'.txt'
			gofFile = open(filename,'r').read()
			gofLines = gofFile.split('\n')[3:-1]
			v_rank=ranking.loc[ranking['nameInStep2'] == v]
			if v_rank.empty:
				continue
			rank=v_rank.iloc[0]['Rank']
			# separation=v_rank.iloc[0]['Separation']
			# isFine = False
			# if '_2DHTSF_' in f:
			# 	isFine=True
			# isNew =False
			# if 'New' in f:
			# 	isNew=True
			# rebinType='norebin'
			# if "0p3" in r:
			# 	rebinType='rebin'
			# if "_noemptybin" in r:
			# 	rebinType='noemptybin'
			for l in gofLines:
				entry={}
				cells = [i for i in l.split(' ') if i != '']
				entry['variable']=v
				entry['year']=year
				subcells=cells[0].split('_')
				entry['lepton']=subcells[0].replace('is','')
				if entry['lepton'] == 'L':
					continue
				entry['njets']=subcells[-1].replace('nJ','')
				entry['nB']=subcells[-2].replace('nB','')
				entry['nHOT']=subcells[1].replace('nHOT','')
				# entry['isFine']=isFine
				# entry['isNew']=isNew
				# entry['rebinType']=rebinType


				# entry['prob_KS']=float(cells[1])
				entry['prob_KS_X']=float(cells[2])
				# entry['prob_KS_X_switch']=float(cells[3])
				# entry['prob_KS_stat']=float(cells[4])
				# entry['prob_KS_X_stat']=float(cells[5])
				# entry['prob_KS_X_stat_switch']=float(cells[6])
				entry['prob_chi2']=float(cells[3])
				entry['chi2']=float(cells[4])
				entry['prob_AD']=float(cells[5])
				# entry['prob_chi2_stat']=float(cells[9])
				# entry['chi2_stat']=float(cells[10])
				entry['ndof']=float(cells[6])

				# entry['no1stbin'] = 'no1stbin' in r 
				# entry['10pEvts'] = '10pEvts' in r
				# entry['prob_KS']=float(cells[1])
				# entry['prob_KS_X']=float(cells[2])
				# entry['prob_chi2']=float(cells[3])
				# entry['chi2']=float(cells[4])
				# entry['ndof']=float(cells[5])
			# entry['prob_KS']=cells[1]
			# entry['prob_KS_X']=cells[2]
			# entry['prob_chi2']=cells[3]
			# entry['chi2']=cells[4]
			# entry['ndof']=cells[5]

				entry['rank']=rank
				entry['pu']=0
				if 'lopu' in f:
					entry['pu']=1
				if 'hipu' in f:
					entry['pu']=-1
				# entry['separation']=separation

				# https://www.dropbox.com/home/fourtops/BDT/R17_StdBinOct20?preview=AK4HT_41p53fb_isE_nB2_nJ4p_logy.png
				# https://www.dropbox.com/home/fourtops/BDT/R18_GOF?preview=BDTtrijet2_59p97fb_isE_nB2p_nJ6p_rebinned_stat0p3_logy_totBand.png
				entry['link'] = 'https://web1.hep.brown.edu/~eusai/merge/'+f.replace(base,'').replace(tail,'')+'/'+entry['variable']+'_'+lumi[entry['year']]+'_is'+entry['lepton']+'_nHOT'+entry['nHOT']+'_nB'+entry['nB']+'_nJ'+entry['njets']+'_merge_rebinned_statVar_logy_totBand.png'
				# entry['link2'] = 'https://www.dropbox.com/home/fourtops/BDT/'+entry['year']+'_GOF_deepjet_no2DHTSF_v2?preview='+entry['variable']+'_'+lumi[entry['year']]+'_is'+entry['lepton']+'_nB'+entry['nB']+'_nJ'+entry['njets']+r+'_logy_totBand.png'
				# 'https://web1.hep.brown.edu/~eusai/plot/'+f.replace(base,'').replace(tail,'')+'/'+entry['variable']+'_'+lumi[entry['year']]+'_is'+entry['lepton']+'_nHOT'+entry['nHOT']+'_nB'+entry['nB']+'_nJ'+entry['njets']+'_rebinned_statVar_NBBW_logy_totBand.png'
				#https://www.dropbox.com/home/fourtops/BDT/R17_New_StdBin_4p?preview=AK4HT_41p53fb_isE_nB2p_nJ4p_norebin_logy.png
				# entry['link'] = 'https://www.dropbox.com/home/fourtops/BDT/'+f.replace(base,'').replace(tail,'').replace('templates_','')+'?preview='+entry['variable']+'_'+lumi[entry['year']]+'_is'+entry['lepton']+'_nB'+entry['nB']+'_nJ'+entry['njets']+'_'+r+'_logy.png'
				# if (year=='R18'):
				# 	entry['link']=''
				# else: 
				# 	entry['link']='https://www.dropbox.com/home/fourtops/BDT/kinematics_step2_0812_year2017/is'+entry['lepton']+'?preview='+entry['variable']+'_'+lumi[entry['year']]+'_is'+entry['lepton']+'_nB2p_nJ'+entry['njets']+'_logy.png'
				data.append(entry)
			# print entry
			# print cells


df=pd.DataFrame(data)
df.to_csv('GOFdata.csv',compression=None)
# print df
# for v in vars
# print ranking
c='\t'
r='\n'
s='  '

# year='R18'
# new=True


def form(a):
	if a=='':
		return ''
	if abs(a)>0 and abs(a)<0.01:
		return "{:.2e}".format(a)
	elif abs(a)>=0.01 and abs(a)<=1.0:
		return "{:.2f}".format(a)
	else:
		return "{:.1f}".format(a)

for year in ['R16','R17','R18']:

	outfile = open("GOF_"+year+"_Dec2021_incl.tsv", "w")
# outfile.write('Channel'+c+'prob_KS 17'+c+'prob_KS_X 17'+c+'prob_chi2 17'+c+
# 				'chi2 17'+c+'ndof 17'+c+'prob_KS 18'+c+'prob_KS_X 18'+c+
# 				'prob_chi2 18'+c+'chi2 18'+c+'ndof 18'+c+'link 17'+r) 
# outfile.write('Channel'+c+'prob_chi2'+c+'prob_chi2_stat'+c+'prob_chi2 (norebin)'+c+'prob_chi2_stat (norebin)'+r)#c+'prob_chi2 (norebin)'+c+'prob_chi2_stat (norebin)'+c+
#	'prob_KS'+c+'prob_KS_X'+c+'prob_KS_X_switch'+c+'prob_KS_stat'+c+'prob_KS_X_stat'+c+'prob_KS (fine)'+c+
#	'prob_KS_X_switch (fine)'+c+'link'+r) 
# outfile.write('Channel'+c+'prob_chi2'+c+'prob_chi2 (10pEvts)'+c+'prob_chi2 (no1stbin)'+c+'prob_chi2 (10pEvts+no1stbin)'+c+'ndof'+c+'ndof (10pEvts)'+c+'prob_chi2 (norebin)'+c+'prob_chi2 (norebin+no1stbin)'+c+'ndof (norebin)'+c+'link (norebin)'+c+'link (std rebin)'+c+'link (10pEvts rebin)'+r)
	outfile.write('Channel'+c+'prob_chi2'+c+'prob_KS_X'+c+'prob_AD'+c+'ndof'+c+'link'+r)
	for index, row in ranking.iterrows():
		var=str(row['nameInStep2'])
		outfile.write(str(row['Rank'])+c+str(row['Variable'])+r)
		#for njet in [['4p','2p'],['4','2p'],['5','2p'],['6p','2p'],['4p','2'],['4p','3'],['4p','4p']]:
		for njet in [['6p','2p','0'],['8p','2p','0'],['6p','2p','1p'],['8p','2p','1p'],]:
		# for njet in [['4p','2p'],['4','2p'],['5','2p'],['6p','2p'],['4p','2'],['4p','3'],['4p','4p']]:
			for lepton in ['M','E']:
				# if njet == ['4p','2p']:
					# R_norebin_fine = df.loc[(df['isFine']==True) & (df['rebinType']=='norebin') & (df['isNew']==new) & (df['njets']==njet[0]) & (df['nB']==njet[1]) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']==year)].iloc[0]
				# else:
					# R_norebin_fine = {'prob_KS':'', 'prob_KS_X_switch':''}
				# print njet,var,lepton,year
				#R_norebin_std = df.loc[ (df['no1stbin']==False) & (df['10pEvts']==False) & (df['isFine']==False) & (df['rebinType']=='norebin') & (df['njets']==njet[0]) & (df['nB']==njet[1]) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']==year)].iloc[0]
				#R_norebin_no1stbin = df.loc[ (df['no1stbin']==True) & (df['10pEvts']==False) & (df['isFine']==False) & (df['rebinType']=='norebin') & (df['njets']==njet[0]) & (df['nB']==njet[1]) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']==year)].iloc[0]
				print(var)
				R_rebin = df.loc[ (df['nHOT']==njet[2]) & (df['njets']==njet[0]) & (df['nB']==njet[1]) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']==year)].iloc[0]
				# R_rebin_no2DHTSF = df.loc[ (df['no1stbin']==False) & (df['10pEvts']==False) & (df['isFine']==False) & (df['rebinType']=='rebin') & (df['njets']==njet[0]) & (df['nB']==njet[1]) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']==year)].iloc[0]
				# R_rebin_2DHTSF =   df.loc[ (df['no1stbin']==False) & (df['10pEvts']==False) & (df['isFine']==True) & (df['rebinType']=='rebin') & (df['njets']==njet[0]) & (df['nB']==njet[1]) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']==year)].iloc[0]
				#R_rebin_no1stbin = df.loc[ (df['no1stbin']==True) & (df['10pEvts']==False) & (df['isFine']==False) & (df['rebinType']=='rebin') & (df['njets']==njet[0]) & (df['nB']==njet[1]) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']==year)].iloc[0]
				#R_rebin_10pEvts = df.loc[ (df['no1stbin']==False) & (df['10pEvts']==True) & (df['isFine']==False) & (df['rebinType']=='rebin') & (df['njets']==njet[0]) & (df['nB']==njet[1]) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']==year)].iloc[0]
				#R_rebin_10pEvts_no1stbin = df.loc[ (df['no1stbin']==True) & (df['10pEvts']==True) & (df['isFine']==False) & (df['rebinType']=='rebin') & (df['njets']==njet[0]) & (df['nB']==njet[1]) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']==year)].iloc[0]
			
				# R_noemptybin_std = df.loc[(df['isFine']==False) & (df['rebinType']=='noemptybin') & (df['isNew']==new) & (df['njets']==njet[0]) & (df['nB']==njet[1]) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']==year)].iloc[0]

#Categories,  prob_chi2 noempty, prob_chi2_stat noempty,
			#outfile.write(lepton+'_'+njet[0]+'J_'+njet[1]+'B'+c+form(R_rebin_std['prob_chi2'])+c+form(R_rebin_std['prob_chi2_stat'])+c+
			# outfile.write(lepton+'_'+njet[0]+'J_'+njet[1]+'B'+c+form(R_noemptybin_std['prob_chi2'])+c+form(R_noemptybin_std['prob_chi2_stat'])+c+
#prob_chi2, prob_chi2_stat, 
#form(R_norebin_std['prob_chi2'])+c+form(R_norebin_std['prob_chi2_stat'])+r)
# form(R_rebin_std['prob_chi2'])+c+form(R_rebin_std['prob_chi2_stat'])+c+
# form(R_norebin_std['prob_chi2'])+c+form(R_norebin_std['prob_chi2_stat'])+c+
#prob_KS, prob_KS_X, prob_KS_X_switch, prob_KS_stat, prob_KS_X_stat,
# form(R_norebin_std['prob_KS'])+c+form(R_norebin_std['prob_KS_X'])+c+form(R_norebin_std['prob_KS_X_switch'])+c+form(R_norebin_std['prob_KS_stat'])+c+form(R_norebin_std['prob_KS_X_stat'])+c+
#prob_KS fine, prob_KS_X_switch fine
# form(R_norebin_fine['prob_KS'])+c+form(R_norebin_fine['prob_KS_X_switch'])+c+R_rebin_std['link']+r)

# outfile.write('Channel'+c+'
				outfile.write(lepton+'_T'+njet[2]+'_'+njet[0]+'J_'+njet[1]+'B'+c+
#prob_chi2'+c+'prob_chi2 (10pEvts)'
form(R_rebin['prob_chi2'])+c+#form(R_rebin_10pEvts['prob_chi2'])+c+
# form(R_rebin['prob_KS'])+c+
form(R_rebin['prob_KS_X'])+c+
form(R_rebin['prob_AD'])+c+
#+c+'prob_chi2 (no1stbin)'+c+'prob_chi2 (10pEvts+no1stbin)'
#form(R_rebin_no1stbin['prob_chi2'])+c+form(R_rebin_10pEvts_no1stbin['prob_chi2'])+c+
#+c+'ndof'+c+'ndof (10pEvts)'+c+
str(R_rebin['ndof'])+c+#str(R_rebin_10pEvts['ndof'])+c+
#'prob_chi2 (norebin)'+c+'prob_chi2 (norebin+no1stbin)'+c
#form(R_norebin_std['prob_chi2'])+c+form(R_norebin_no1stbin['prob_chi2'])+c+
#+'ndof (norebin)'+r)
#str(R_norebin_std['ndof'])+c+
#+c+'link (norebin)'+c+'link (std rebin)'+c+'link (10pEvts rebin)'+r)
R_rebin['link']+c+
# R_rebin_no2DHTSF['link']+c+#R_rebin_10pEvts['link']
# R_rebin_2DHTSF['link']+c+
r)

			# R17= df.loc[(df['njets']==njet) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']=='R17')].iloc[0]
			# R18= df.loc[(df['njets']==njet) & (df['variable']==var) & (df['lepton']==lepton) & (df['year']=='R18')].iloc[0]
			# outfile.write(lepton+njet+c+form(R17['prob_KS'])+c+form(R17['prob_KS_X'])+c+form(R17['prob_chi2'])+c+
			# 	form(R17['chi2'])+c+form(R17['ndof'])+c+form(R18['prob_KS'])+c+form(R18['prob_KS_X'])+c+
			# 	form(R18['prob_chi2'])+c+form(R18['chi2'])+c+form(R18['ndof'])+c+R17['link']+r)
			# outfile.write(lepton+njet+c+str(R17['prob_KS'])+c+str(R17['prob_KS_X'])+c+str(R17['prob_chi2'])+c+
			# 	str(R17['chi2'])+c+str(R17['ndof'])+c+str(R18['prob_KS'])+c+str(R18['prob_KS_X'])+c+
			# 	str(R18['prob_chi2'])+c+str(R18['chi2'])+c+str(R18['ndof'])+c+str(R17['link'])+r)
			
			# outfile.write(lepton+njet+c+R17['prob_KS']+c+R17['prob_KS_X']+c+R17['prob_chi2']+c+
			# 	R17['chi2']+c+R17['ndof']+c+R18['prob_KS']+c+R18['prob_KS_X']+c+
			# 	R18['prob_chi2']+c+R18['chi2']+c+R18['ndof']+c+R17['link']+r)
		outfile.write(c+c+c+c+r)
		outfile.write(c+c+c+c+r)

# ranked by separation

# var1  rank separation

#     2017 ks ksx chi probchi ndof  2018 ks ksx chi probchi ndof plot link (2017)
# 4
# 5
# 6p
# 4p