training

python makeTemplates/doCondorTemplates.py R17 BDT 40vars_6j /mnt/hadoop/store/group/bruxljm/FWLJMET102X_1lep2018_Oct2019_4t_05182020_step3_wenyu/BDT_SepRank6j73vars2017year40top_40vars_mDepth2_4j_year2018/

python makeTemplates/doTemplates.py R17 40vars_6j

python makeTemplates/modifyBinning.py R17 BDT 40vars_6j

python makeTemplates/plotTemplates.py R17 BDT 40vars_6j

python combineLimits/dataCard.py R17 BDT 40vars_6j