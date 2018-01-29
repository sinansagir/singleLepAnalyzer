import os,sys

masslist = [800,900,1000,1100,1200,1300,1400,1500,1600,1700,1800]
brlist = [
'bW0p0_tZ0p0_tH1p0_',
'bW0p0_tZ0p2_tH0p8_',
'bW0p0_tZ0p4_tH0p6_',
'bW0p0_tZ0p5_tH0p5_',
'bW0p0_tZ0p6_tH0p4_',
'bW0p0_tZ0p8_tH0p2_',
'bW0p0_tZ1p0_tH0p0_',
'bW0p2_tZ0p0_tH0p8_',
'bW0p2_tZ0p2_tH0p6_',
'bW0p2_tZ0p4_tH0p4_',
'bW0p2_tZ0p6_tH0p2_',
'bW0p2_tZ0p8_tH0p0_',
'bW0p4_tZ0p0_tH0p6_',
'bW0p4_tZ0p2_tH0p4_',
'bW0p4_tZ0p4_tH0p2_',
'bW0p4_tZ0p6_tH0p0_',
'bW0p5_tZ0p25_tH0p25_',
'bW0p6_tZ0p0_tH0p4_',
'bW0p6_tZ0p2_tH0p2_',
'bW0p6_tZ0p4_tH0p0_',
'bW0p8_tZ0p0_tH0p2_',
'bW0p8_tZ0p2_tH0p0_',
'bW1p0_tZ0p0_tH0p0_',
]

pre = 'splitLess/templates_minMlbST_TTM'
pre3 = 'splitLess/templates_ST_TTM'
pre2 = 'splitLess/templates_HT_TTM'
post = '36p814fb_BKGNORM_rebinned_stat0p3.root'
post15 = '36p814fb_rebinned_stat0p15.root'

for mass in masslist:
    for br in brlist:
        brBB = br.replace('bW','tW').replace('tZ','bZ').replace('tH','bH')
        #os.system('hadd control_ARC/'+pre+str(mass)+'_'+br+post+' ttbar_ARC/'+pre+str(mass)+'_'+br+post+' wjets_ARC/'+pre+str(mass)+'_'+br+post+' higgs_ARC/'+pre+str(mass)+'_'+br+post)
        #os.system('hadd templatesCRSR_NewEl/'+pre+str(mass)+'_'+br+post+' templates_NewEl/'+pre+str(mass)+'_'+br+post+' control_NewEl/'+pre+str(mass)+'_'+br+post)
        #os.system('hadd -f templates4CRhtSR_NewEl/'+pre+str(mass)+'_'+br+post+' templates_NewEl/'+pre+str(mass)+'_'+br+post+' templatesCR_NewEl/'+pre2+str(mass)+'_'+br+post)
        #os.system('hadd -f templates4CRhtSR_NewEl/'+pre+str(mass)+'_'+br+post15+' templates_NewEl/'+pre+str(mass)+'_'+br+post15+' templatesCR_NewEl/'+pre2+str(mass)+'_'+br+post15)
        #os.system('hadd -f templates4CRhtSR_NewEl/'+pre3+str(mass)+'_'+br+post+' templates_NewEl/'+pre3+str(mass)+'_'+br+post+' templatesCR_NewEl/'+pre2+str(mass)+'_'+br+post)
        os.system('hadd -f templates4CRhtSR_BB_NewEl/'+pre.replace('TTM','BBM')+str(mass)+'_'+brBB+post+' templates_BB_NewEl/'+pre.replace('TTM','BBM')+str(mass)+'_'+brBB+post+' templatesCR_BB_NewEl/'+pre2.replace('TTM','BBM')+str(mass)+'_'+brBB+post)
        os.system('hadd -f templates4CRhtSR_BB_NewEl/'+pre3.replace('TTM','BBM')+str(mass)+'_'+brBB+post+' templates_BB_NewEl/'+pre3.replace('TTM','BBM')+str(mass)+'_'+brBB+post+' templatesCR_BB_NewEl/'+pre2.replace('TTM','BBM')+str(mass)+'_'+brBB+post)
        #os.system('hadd templates4CRSR_ARC/'+pre+str(mass)+'_'+br+post+' templates_ARC/'+pre+str(mass)+'_'+br+post+' templatesCR_ARC/'+pre+str(mass)+'_'+br+post)
        
