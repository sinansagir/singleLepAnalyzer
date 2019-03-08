#!/usr/bin/python

import os,sys,math,itertools

tags = {}

nttaglist = ['0','1','0p','1p','2p']
nWtaglist = ['0','1','0p','1p','2p']
nbtaglist = ['1','2','3','3p','4p']
njetslist = ['4','5','6','7','8','9','9p','10p']
def skip(cat):
	if (cat[0]=='1' or cat[0]=='1p' or cat[0]=='2p') and (cat[1]=='1' or cat[1]=='2p'): return True
	elif (cat[0]=='2p') and (cat[1]=='1p' or cat[1]=='2p') and (cat[3]=='4' or cat[3]=='5'): return True
	elif (cat[0]=='2p') and (cat[1]=='1p' or cat[1]=='2p') and (cat[2]=='4p'): return True
	else: return False
tags['all'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip(tag)]

nttaglist = ['0','1p']
nWtaglist = ['0','0p','1p']
nbtaglist = ['2','3','4p']
njetslist = ['4','5','6','7','8','9','10p']
def skip63(cat):
	if (cat[0]=='0') and (cat[1]=='0p'): return True
	elif (cat[0]=='1p') and (cat[1]!='0p'): return True
	else: return False
tags['tag63'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip63(tag)]

njetslist = ['6','7','8','9','10p']
tags['tag45'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip63(tag)]

njetslist = ['7','8','9','10p']
tags['tag36'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip63(tag)]

njetslist = ['7','8','9p']
tags['tag27'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip63(tag)]

nttaglist = ['0p']
nWtaglist = ['0p']
njetslist = ['6','7','8','9','10p']
tags['noTW15'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]

nWtaglist = ['0','1p']
njetslist = ['6','7','8','9','10p']
tags['onlyW30'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]

nttaglist = ['0','1p']
nWtaglist = ['0p']
njetslist = ['6','7','8','9','10p']
tags['onlyT30'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]

nttaglist = ['0','1','2p']
nWtaglist = ['0','1','1p','2p']
nbtaglist = ['2','3','3p','4p']
njetslist = ['5','6','7','8','9','10p']
def skip120(cat):
	if (cat[0]=='0') and (cat[1]=='1p' or cat[2]=='3p'): return True
	elif (cat[0]=='1') and (cat[1]=='1' or cat[1]=='2p' or cat[2]=='3p'): return True
	elif (cat[0]=='2p') and (cat[1]=='1' or cat[1]=='2p'): return True
	elif (cat[0]=='2p' and cat[1]=='0') and (cat[2]=='3p'): return True
	elif (cat[0]=='2p' and cat[1]=='1p') and (cat[2]=='3' or cat[2]=='4p'): return True
	else: return False
tags['tag120'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip120(tag)]

#print len(tags['all']), len(tags['onlyT30']), len([tag for tag in tags['all'] if tag not in tags['onlyT30']])
#print len(tags['tag27']), tags['tag27']
