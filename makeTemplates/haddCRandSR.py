import os,sys

masslist = [900,1100,1200,1300,1400,1500,1600,1700,1800]
brlist = [
'bW0p0_tZ0p0_tH1p0_',
#'bW0p0_tZ0p2_tH0p8_',
#'bW0p0_tZ0p4_tH0p6_',
'bW0p0_tZ0p5_tH0p5_',
#'bW0p0_tZ0p6_tH0p4_',
#'bW0p0_tZ0p8_tH0p2_',
'bW0p0_tZ1p0_tH0p0_',
#'bW0p2_tZ0p0_tH0p8_',
#'bW0p2_tZ0p2_tH0p6_',
#'bW0p2_tZ0p4_tH0p4_',
#'bW0p2_tZ0p6_tH0p2_',
#'bW0p2_tZ0p8_tH0p0_',
#'bW0p4_tZ0p0_tH0p6_',
#'bW0p4_tZ0p2_tH0p4_',
#'bW0p4_tZ0p4_tH0p2_',
#'bW0p4_tZ0p6_tH0p0_',
'bW0p5_tZ0p25_tH0p25_',
#'bW0p6_tZ0p0_tH0p4_',
#'bW0p6_tZ0p2_tH0p2_',
#'bW0p6_tZ0p4_tH0p0_',
#'bW0p8_tZ0p0_tH0p2_',
#'bW0p8_tZ0p2_tH0p0_',
'bW1p0_tZ0p0_tH0p0_',
]

# Combine:
pre = 'templates_DnnTprime'
pre3 = 'templates_HTNtag'
postCR = '41p53_Combine_chi2_rebinned_stat0p3.root'
postSR = '41p53_Combine_rebinned_stat0p3_smoothedLOWESS.root'

for br in brlist:
    brBB = br.replace('bW','tW').replace('tZ','bZ').replace('tH','bH')
    os.system('hadd -f templatesSRCR_Feb2021BB/'+pre.replace('Tp','Bp')+'_'+brBB+postSR+' templatesCR_Feb2021BB/'+pre3.replace('Tp','Bp')+'_'+brBB+postCR+' templatesSR_Feb2021BB/'+pre.replace('Tp','Bp')+'_'+brBB+postSR)
    os.system('hadd -f templatesSRCR_Feb2021TT/'+pre+'_'+br+postSR+' templatesCR_Feb2021TT/'+pre3+'_'+br+postCR+' templatesSR_Feb2021TT/'+pre+'_'+br+postSR)


# pre = 'templates_DnnTprime_TTM'
# pre3 = 'templates_HTNtag_TTM'
# postCR = '41p53fb_chi2_rebinned_stat0p3.root'
# postSR = '41p53fb_rebinned_stat0p3_smoothedLOWESS.root'

# for mass in [1400]:
#     for br in brlist:
#         brBB = br.replace('bW','tW').replace('tZ','bZ').replace('tH','bH')
#         #os.system('hadd -f templatesSRCR_June2020BB/'+pre.replace('TTM','BBM').replace('Tp','Bp')+str(mass)+'_'+brBB+postSR+' templatesCR_June2020BB/'+pre3.replace('TTM','BBM')+str(mass)+'_'+brBB+postCR+' templatesSR_June2020BB/'+pre.replace('TTM','BBM').replace('Tp','Bp')+str(mass)+'_'+brBB+postSR)
#         #os.system('hadd -f templatesSRCR_June2020TT/'+pre+str(mass)+'_'+br+postSR+' templatesCR_June2020TT/'+pre3+str(mass)+'_'+br+postCR+' templatesSR_June2020TT/'+pre+str(mass)+'_'+br+postSR)
