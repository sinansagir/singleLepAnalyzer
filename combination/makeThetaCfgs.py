#!/usr/bin/python

import os

#make list of card files

limitDir = "limits_9Oct16_tau21fix_noCRsys/"
thisDir = os.getcwd()+'/'
ssdl_dir = 'templates_ssdl_15Sep16/'
ljets_dir = 'templates_ljets_9Oct16/'
allfiles_ssdl  = os.listdir('./'+ssdl_dir)
allfiles_ljets = os.listdir('./'+ljets_dir)
ssdlfiles = []

#get ssdl files
for file in allfiles_ssdl:
    if file.find(".root")==-1:
        continue
    if file.find("Limits_M")==-1:
        continue
    if file.find("HT900")==-1:
        continue

    ssdlfiles.append(file)

#get ljets files
ljetsfiles=[]
for file in allfiles_ljets:
    #skip if not a card file, and if not a theta card file
    if file.find("templates")==-1:
        continue
    if file.find(".root")==-1:
        continue

    ljetsfiles.append(file)




for card in ssdlfiles:

    #open template file
    template = open("theta_template_noCRsys.py",'r')
    mass = card.split("_M")[1].split("_")[0]
    if mass=="700":
        xsec='0.442'
    elif mass=='800':
        xsec='0.190'
    elif mass=='900':
        xsec='0.0877'
    elif mass=='1000':
        xsec='0.0427'
    elif mass=='1100':
        xsec='0.0217'
    elif mass=='1200':
        xsec='0.0114'
    elif mass=='1300':
        xsec='0.00618'
    elif mass=='1400':
        xsec='0.00342'
    elif mass=='1500':
        xsec='0.00193'
    else:
        xsec='0.00111'


    #now that we have mass let's get chirality and then find corresponding ljets file
    chi = card.split("_LL")[0].split("_")[2]
    ljetfile = ''
    spin=''
    if chi == 'RH':
        spin = 'right'
    elif chi == 'LH':
        spin ='left'
    print spin, chi
    for ljfile in ljetsfiles:
        if ljfile.find(spin)!=-1 and ljfile.find(mass)!=-1:
            ljetfile=ljfile

    filename = "X53X53_Combination_M"+mass+"_"+chi
    #filename += (card.split("_theta.root")[0]).split("Limits_")[1]
    exptxt = filename+"_expected.txt"
    obstxt = filename+"_observed.txt"
    htmlout = filename+"_html"
    jsonname=filename
    filename+=".py"
    outfile= open(limitDir+filename,'w')
    for line in template:
        line = line.replace('SSDLROOTFILE',thisDir+ssdl_dir+card)
        line = line.replace('LJETSFILE',thisDir+ljets_dir+ljetfile)
        line = line.replace('EXPTXTFILE',exptxt)
        line = line.replace('OBSTXTFILE',obstxt)
        line = line.replace('HTMLOUT',htmlout)
        line = line.replace('MASS',mass)
        line = line.replace('XSEC',xsec)
        line = line.replace('JSONNAME',jsonname)
        outfile.write(line)
    template.close()
    outfile.close()
    
    shfilename=filename.replace(".py",".sh")
    shoutfile= open(limitDir+shfilename,'w')
    shoutfile.write('#!/bin/sh \n')
    shoutfile.write('cd /home/ssagir/CMSSW_7_3_0/src/\n')
    shoutfile.write('source /cvmfs/cms.cern.ch/cmsset_default.sh\n')
    shoutfile.write('cmsenv\n')
    shoutfile.write('cd -\n')
    shoutfile.write('cd '+limitDir+'\n')
    shoutfile.write('/home/ssagir/CMSSW_7_3_0/src/theta/utils2/theta-auto.py ' + thisDir+limitDir+filename)
    shoutfile.close()
    
    os.chdir(limitDir)
    dict={'configfile':shfilename[:-3]}
    jdf=open(shfilename.replace(".sh",".job"),'w')
    jdf.write(
"""universe = vanilla
Executable = %(configfile)s.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
Notification = Error
request_memory = 3072
Output = %(configfile)s.out
Error = %(configfile)s.err
Log = %(configfile)s.log
Queue 1"""%dict)
    jdf.close()
    
    os.system('chmod +x '+shfilename)
    os.system('condor_submit '+shfilename.replace(".sh",".job"))
    os.chdir('..')
