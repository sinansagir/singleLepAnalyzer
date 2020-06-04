#!/usr/bin/python

import os,sys,math,itertools

def skip(cat):
	#return False
	if (cat[2]=='1' or cat[2]=='2p') and not (cat[0]=='0' and cat[1]=='0'): return True
	else: return False

tags = {}

nhottlist_ = ['0','0p','1p']
nttaglist_ = ['0','0p','1p']
nWtaglist_ = ['0','0p','1p','1','2p']
nbtaglist_ = ['2','3','3p','4p']
njetslist_ = ['4','5','6','7','8','9','9p','10p']
tagList_=list(itertools.product(nhottlist_,nttaglist_,nWtaglist_,nbtaglist_,njetslist_))
tags['allcats'] = ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_ if not skip(tag)]

nhottlist_ = ['0','1p']
nttaglist_ = ['0','1p']
nWtaglist_ = ['0','0p','1p','1','2p']
nbtaglist_ = ['2','3','4p']
njetslist_ = ['4','5','6','7','8','9','10p']
tagList_=list(itertools.product(nhottlist_,nttaglist_,nWtaglist_,nbtaglist_,njetslist_))
def skip165(cat):
	if (cat[0]=='0') and (cat[1]=='0') and (cat[2]=='0p' or cat[2]=='1p'): return True
	elif (cat[0]=='0') and (cat[1]=='1p') and (cat[2]=='0p' or cat[2]=='1' or cat[2]=='2p'): return True
	elif (cat[0]=='1p') and (cat[1]=='0') and (cat[2]=='0p' or cat[2]=='1' or cat[2]=='2p'): return True
	elif (cat[0]=='1p') and (cat[1]=='1p') and (cat[2]!='0p'): return True
	elif (cat[0]=='1p') and (cat[1]=='1p' or cat[2]=='1p') and (cat[4]=='4'): return True
	else: return False
tags['165cats']  = ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_ if not skip165(tag)]
nWtaglist_ = ['0','0p','1p']
tagList_=list(itertools.product(nhottlist_,nttaglist_,nWtaglist_,nbtaglist_,njetslist_))
def skip144(cat):
	if (cat[0]=='0') and (cat[1]=='0') and (cat[2]=='0p'): return True
	elif (cat[0]=='0') and (cat[1]=='1p') and (cat[2]=='0p'): return True
	elif (cat[0]=='1p') and (cat[1]=='0') and (cat[2]=='0p'): return True
	elif (cat[0]=='1p') and (cat[1]=='1p') and (cat[2]!='0p'): return True
	elif (cat[0]=='1p') and (cat[1]=='1p' or cat[2]=='1p') and (cat[4]=='4'): return True
	else: return False
tags['144cats']  = ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_ if not skip144(tag)]
def skip102(cat):
	if (cat[0]=='0') and (cat[1]=='0') and (cat[2]=='0p'): return True
	elif (cat[0]=='0') and (cat[1]=='1p') and (cat[2]!='0p'): return True
	elif (cat[0]=='1p') and (cat[1]=='0') and (cat[2]!='0p'): return True
	elif (cat[0]=='1p') and (cat[1]=='1p') and (cat[2]!='0p'): return True
	elif (cat[0]=='1p') and (cat[1]=='1p') and (cat[4]=='4'): return True
	else: return False
tags['102cats']  = ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_ if not skip102(tag)]
njetslist_ = ['5','6','7','8','9','10p']
tagList_=list(itertools.product(nhottlist_,nttaglist_,nWtaglist_,nbtaglist_,njetslist_))
tags['90cats']   = ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_ if not skip102(tag)]
njetslist_ = ['6','7','8','9','10p']
tagList_=list(itertools.product(nhottlist_,nttaglist_,nWtaglist_,nbtaglist_,njetslist_))
tags['75cats']   = ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_ if not skip102(tag)]
njetslist_ = ['7','8','9','10p']
tagList_=list(itertools.product(nhottlist_,nttaglist_,nWtaglist_,nbtaglist_,njetslist_))
tags['60cats']   = ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_ if not skip102(tag)]
njetslist_ = ['7','8','9p']
tagList_=list(itertools.product(nhottlist_,nttaglist_,nWtaglist_,nbtaglist_,njetslist_))
tags['45cats']   = ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_ if not skip102(tag)]
nhottlist_ = ['0p']
nttaglist_ = ['0p']
nWtaglist_ = ['0p']
njetslist_ = ['6','7','8','9','10p']
tagList_=list(itertools.product(nhottlist_,nttaglist_,nWtaglist_,nbtaglist_,njetslist_))
tags['noHOTtW15']= ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_]
nhottlist_ = ['0','1p']
nttaglist_ = ['0p']
nWtaglist_ = ['0p']
tagList_=list(itertools.product(nhottlist_,nttaglist_,nWtaglist_,nbtaglist_,njetslist_))
tags['onlyHOT30']= ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_]
nhottlist_ = ['0p']
nttaglist_ = ['0','1p']
nWtaglist_ = ['0p']
tagList_=list(itertools.product(nhottlist_,nttaglist_,nWtaglist_,nbtaglist_,njetslist_))
tags['onlyT30']  = ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_]
nhottlist_ = ['0p']
nttaglist_ = ['0p']
nWtaglist_ = ['0','1p']
tagList_=list(itertools.product(nhottlist_,nttaglist_,nWtaglist_,nbtaglist_,njetslist_))
tags['onlyW30']  = ['_nHOT'+tag[0]+'_nT'+tag[1]+'_nW'+tag[2]+'_nB'+tag[3]+'_nJ'+tag[4]+'_' for tag in tagList_]

# for tag in tags.keys():
# 	print tag,len(tags[tag])

# nttaglist = ['0','1p']
# nWtaglist = ['0','0p','1p']
# nbtaglist = ['2','3','4p']
# njetslist = ['4','5','6','7','8','9','10p']
# def skip63(cat):
# 	if (cat[0]=='0') and (cat[1]=='0p'): return True
# 	elif (cat[0]=='1p') and (cat[1]!='0p'): return True
# 	else: return False
# tags['tag63'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip63(tag)]
# 
# njetslist = ['5','6','7','8','9','10p']
# tags['tag54'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip63(tag)]
# 
# njetslist = ['6','7','8','9','10p']
# tags['tag45'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip63(tag)]
# 
# njetslist = ['7','8','9','10p']
# tags['tag36'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip63(tag)]
# 
# njetslist = ['7','8','9p']
# tags['tag27'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip63(tag)]
# 
# nttaglist = ['0p']
# nWtaglist = ['0p']
# njetslist = ['6','7','8','9','10p']
# tags['noTW15'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]
# 
# nWtaglist = ['0','1p']
# njetslist = ['6','7','8','9','10p']
# tags['onlyW30'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]
# 
# nttaglist = ['0','1p']
# nWtaglist = ['0p']
# njetslist = ['6','7','8','9','10p']
# tags['onlyT30'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]
# 
# nttaglist = ['0p']
# nWtaglist = ['0p']
# njetslist = ['5','6','7','8','9','10p']
# tags['noTW18'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]
# 
# nWtaglist = ['0','1p']
# njetslist = ['5','6','7','8','9','10p']
# tags['onlyW36'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]
# 
# nttaglist = ['0','1p']
# nWtaglist = ['0p']
# njetslist = ['5','6','7','8','9','10p']
# tags['onlyT36'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist))]
# 
# nttaglist = ['0','1','2p']
# nWtaglist = ['0','1','1p','2p']
# nbtaglist = ['2','3','3p','4p']
# njetslist = ['5','6','7','8','9','10p']
# def skip120(cat):
# 	if (cat[0]=='0') and (cat[1]=='1p' or cat[2]=='3p'): return True
# 	elif (cat[0]=='1') and (cat[1]=='1' or cat[1]=='2p' or cat[2]=='3p'): return True
# 	elif (cat[0]=='2p') and (cat[1]=='1' or cat[1]=='2p'): return True
# 	elif (cat[0]=='2p' and cat[1]=='0') and (cat[2]=='3p'): return True
# 	elif (cat[0]=='2p' and cat[1]=='1p') and (cat[2]=='3' or cat[2]=='4p'): return True
# 	else: return False
# tags['tag120'] = ['_nT'+tag[0]+'_nW'+tag[1]+'_nB'+tag[2]+'_nJ'+tag[3]+'_' for tag in list(itertools.product(nttaglist,nWtaglist,nbtaglist,njetslist)) if not skip120(tag)]

#print len(tags['all']), len(tags['onlyT30']), len([tag for tag in tags['all'] if tag not in tags['onlyT30']])
#print len(tags['tag27']), tags['tag27']
