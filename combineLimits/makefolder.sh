#source makefolder.sh 40vars_6j_NJetsCSV_053121lim_newbin3
mkdir $1
cd $1
cp -r ../limits_R1*_$1_BDT .
mkdir BDTcomb
cd BDTcomb
cp ../../BDTcomb/*$1_BDT* .
cd ../../
zip -r $1.zip $1
cp $1.zip ~/public_html/
echo "https://web1.hep.brown.edu/~eusai/$1.zip"