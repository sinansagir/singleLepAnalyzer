#!/bin/bash

echo "Making data cards for TT CRs"
echo "Singlet..."
python -u dataCard.py bW0p5_tZ0p25_tH0p25 CR HTdnnL_100fbChi20p3FM HTdnnL >& makecard_SgT_CRHTdnnL_100fbChi20p3FM.log 
echo "Singlet HTNtag..."
python -u dataCard.py bW0p5_tZ0p25_tH0p25 CR HTNTag_100fbChi20p3FM HTNTag >& makecard_SgT_CRHTdnnL_100fbChi20p3FM.log 
# echo "tH..."
# python -u dataCard.py bW0p0_tZ0p0_tH1p0 CR 100fbChi20p15FM >& makecard_tH_CR100fbChi20p15FM.log 
# echo "Doublet..."
# python -u dataCard.py bW0p0_tZ0p5_tH0p5 CR 100fbChi20p15FM >& makecard_DbT_CR100fbChi20p15FM.log 
# echo "tZ..."
# python -u dataCard.py bW0p0_tZ1p0_tH0p0 CR 100fbChi20p15FM >& makecard_tZ_CR100fbChi20p15FM.log 
# echo "bW..."
# python -u dataCard.py bW1p0_tZ0p0_tH0p0 CR 100fbChi20p15FM >& makecard_bW_CR100fbChi20p15FM.log 


# echo "Making data cards for BB CRs"
# echo "Singlet..."
# python -u dataCard.py tW0p5_bZ0p25_bH0p25 CR 100fbChi20p15FM >& makecard_SgB_CR100fbChi20p15FM.log 
# echo "bH..."
# python -u dataCard.py tW0p0_bZ0p0_bH1p0 CR 100fbChi20p15FM >& makecard_bH_CR100fbChi20p15FM.log 
# echo "Doublet..."
# python -u dataCard.py tW0p0_bZ0p5_bH0p5 CR 100fbChi20p15FM >& makecard_DbB_CR100fbChi20p15FM.log 
# echo "bZ..."
# python -u dataCard.py tW0p0_bZ1p0_bH0p0 CR 100fbChi20p15FM >& makecard_bZ_CR100fbChi20p15FM.log 
# echo "tW..."
# python -u dataCard.py tW1p0_bZ0p0_bH0p0 CR 100fbChi20p15FM >& makecard_tW_CR100fbChi20p15FM.log 

# echo "Making data cards for TT SRs"
# echo "Singlet already done"
# python -u dataCard.py bW0p5_tZ0p25_tH0p25 SRCR 100fb0p3smoothedL >& makecard_SgT_SR100fb0p3smoothedL.log 
# echo "tH..."
# python -u dataCard.py bW0p0_tZ0p0_tH1p0 SRCR 100fb0p3smoothedL >& makecard_tH_SR100fb0p3smoothedL.log 
# echo "Doublet..."
# python -u dataCard.py bW0p0_tZ0p5_tH0p5 SRCR 100fb0p3smoothedL >& makecard_DbT_SR100fb0p3smoothedL.log 
# echo "tZ..."
# python -u dataCard.py bW0p0_tZ1p0_tH0p0 SRCR 100fb0p3smoothedL >& makecard_tZ_SR100fb0p3smoothedL.log 
# echo "bW..."
# python -u dataCard.py bW1p0_tZ0p0_tH0p0 SRCR 100fb0p3smoothedL >& makecard_bW_SR100fb0p3smoothedL.log 


# echo "Making data cards for BB SRs"
# echo "Singlet..."
# python -u dataCard.py tW0p5_bZ0p25_bH0p25 SRCR 100fb0p3smoothedL >& makecard_SgB_SR100fb0p3smoothedL.log 
# echo "bH..."
# python -u dataCard.py tW0p0_bZ0p0_bH1p0 SRCR 100fb0p3smoothedL >& makecard_bH_SR100fb0p3smoothedL.log 
# echo "Doublet..."
# python -u dataCard.py tW0p0_bZ0p5_bH0p5 SRCR 100fb0p3smoothedL >& makecard_DbB_SR100fb0p3smoothedL.log 
# echo "bZ..."
# python -u dataCard.py tW0p0_bZ1p0_bH0p0 SRCR 100fb0p3smoothedL >& makecard_bZ_SR100fb0p3smoothedL.log 
# echo "tW..."
# python -u dataCard.py tW1p0_bZ0p0_bH0p0 SRCR 100fb0p3smoothedL >& makecard_tW_SR100fb0p3smoothedL.log 

echo "Done!"
