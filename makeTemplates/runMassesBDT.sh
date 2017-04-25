for mass in Low Med High 800 1000 2000 3000; do
    echo $mass
    python doTemplates.py BDTG_33vars_mD3_M$mass
    python modifyBinning.py HTpBDT $mass 1.1
    python modifyBinning.py HTpBDT $mass 0.3
done
