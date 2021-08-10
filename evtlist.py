#!/usr/bin/python

from ROOT import TFile

data={
'E16':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2016_Oct2019_4t_053121_step3_40vars_6j_NJetsCSV/nominal/SingleElectron_hadd.root',
'M16':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2016_Oct2019_4t_053121_step3_40vars_6j_NJetsCSV/nominal/SingleMuon_hadd.root',

'E17':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_053121_step3_40vars_6j_NJetsCSV/nominal/SingleElectron_hadd.root',
'M17':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2017_Oct2019_4t_053121_step3_40vars_6j_NJetsCSV/nominal/SingleMuon_hadd.root',

'M18':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_053121_step3_40vars_6j_NJetsCSV/nominal/SingleMuon_hadd.root',
'E18':'/mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_053121_step3_40vars_6j_NJetsCSV/nominal/EGamma_hadd.root',
}

j=0
for key in data:
	txt = open(key+".txt","w")
	f=TFile(data[key],'READ')
	cutList = {'elPtCut':20,'muPtCut':20,'metCut':60,'mtCut':60,'jet1PtCut':0,'jet2PtCut':0,'jet3PtCut':0,'AK4HTCut':500}
	if '16' in key: 
		cutList['elPtCut'] = 35
		cutList['muPtCut'] = 26
	entries=f.ljmet.GetEntries()
	i=0
	for evt in f.ljmet:
		i+=1
		if ((evt.leptonPt_MultiLepCalc > cutList['elPtCut']) and (evt.isElectron==1)) or ((evt.leptonPt_MultiLepCalc > cutList['muPtCut']) and (evt.isMuon==1)):
			if (evt.corr_met_MultiLepCalc > cutList['metCut']) and \
			(evt.MT_lepMet > cutList['mtCut']) and \
			(evt.theJetPt_JetSubCalc_PtOrdered[0] > cutList['jet1PtCut']) and \
			(evt.theJetPt_JetSubCalc_PtOrdered[1] > cutList['jet2PtCut']) and \
			(evt.theJetPt_JetSubCalc_PtOrdered[2] > cutList['jet3PtCut']) and \
			(evt.minDR_lepJet > 0.4) and \
			(evt.AK4HT  > cutList['AK4HTCut']):
				if (evt.NJets_JetSubCalc>=6) and (evt.NJetsCSV_MultiLepCalc>=3):
					j+=1
					if j%100==0:
						print key,1.0*i/entries,str(evt.run_CommonCalc)+':'+str(evt.lumi_CommonCalc)+':'+str(evt.event_CommonCalc)
					txt.write(str(evt.run_CommonCalc)+':'+str(evt.lumi_CommonCalc)+':'+str(evt.event_CommonCalc)+'\n')
	f.Close()
	txt.close()
