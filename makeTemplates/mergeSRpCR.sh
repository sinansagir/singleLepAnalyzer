runConf=M17WtSF_2017_3_31
postFix=35p867fb_rebinned_stat0p3.root
ttbarDir=ttbar_${runConf}
wjetsDir=wjets_${runConf}
templateDir=templates_${runConf}
outDir=${templateDir}_SRpCR
mkdir $outDir
cd $outDir
for disc in minMlb; do
	for mass in 800 900 1000 1100 1200 1300 1400 1500 1600; do
		for sig in left right; do
			echo HADDING_${disc}_${mass}_${sig}
			hadd templates_${disc}_X53X53M${mass}${sig}_${postFix} \
			../${templateDir}/templates_${disc}_X53X53M${mass}${sig}_${postFix} \
			../${ttbarDir}/templates_${disc}_X53X53M${mass}${sig}_${postFix} \
			../${wjetsDir}/templates_${disc}_X53X53M${mass}${sig}_${postFix}
		done
	done
done
