#!/usr/bin/python

import sys,math
from ROOT import *

def isEqual(a, b):
    try:
        return a.upper() == b.upper()
    except AttributeError:
        return a == b

def contains(a, b):
    try:
        return b.upper() in a.upper()
    except AttributeError:
        return b in a

##############################################################################

def skip_nominal(cat):
	#return False
	if (cat[3]=='1' or cat[3]=='2p') and not (cat[1]=='0' and cat[2]=='0'): return True
	elif (cat[1]=='1p') and (cat[2]=='1p' or cat[3]=='1p') and (cat[5]=='4'): return True
	else: return False

def skip_90cats(cat):
	if (cat[1]=='0p' or cat[2]=='0p' or cat[3]=='1' or cat[3]=='2p' or cat[4]=='3p' or cat[5]=='4' or cat[5]=='9p'): return True
	if (cat[1]=='1p' and cat[3]!='0p'): return True
	elif (cat[1]=='0' and cat[2]=='1p' and cat[3]!='0p'): return True
	elif (cat[1]=='0' and cat[2]=='0' and cat[3]=='0p'): return True
	else: return False
	
def skip_75cats(cat):
	if (cat[1]=='0p' or cat[2]=='0p' or cat[3]=='1' or cat[3]=='2p' or cat[4]=='3p' or cat[5]=='4' or cat[5]=='5' or cat[5]=='9p'): return True
	if (cat[1]=='1p' and cat[3]!='0p'): return True
	elif (cat[1]=='0' and cat[2]=='1p' and cat[3]!='0p'): return True
	elif (cat[1]=='0' and cat[2]=='0' and cat[3]=='0p'): return True
	else: return False
	
def skip_noHOTtW_OR_onlyHOTtW(cat):
	if (cat[1]=='0p' and cat[2]=='0p' and cat[3]=='0p'): return False
	if (cat[1]!='0p' and cat[2]=='0p' and cat[3]=='0p'): return False
	if (cat[1]=='0p' and cat[2]!='0p' and cat[3]=='0p'): return False
	if (cat[1]=='0p' and cat[2]=='0p' and cat[3]!='0p'): return False
	return True
	
def skip(cat):
	if cat[1]=='0p' and cat[2]=='0p' and cat[3]=='0p' and cat[4]=='2p' and cat[5]=='4p': return False #preselection plots
	#return skip_75cats(cat)
	#return skip_noHOTtW_OR_onlyHOTtW(cat)
	return False

##############################################################################
		
def smoothShape(hNm,hUp,hDn,algo='lowess',symmetrize=True):
	hName = hNm.GetName()
	grinUp = TGraphErrors()
	grinDn = TGraphErrors()
	groutUp = TGraphErrors()
	groutDn = TGraphErrors()
	gsUp = TGraphSmooth(hName+'_up_lowess')
	gsDn = TGraphSmooth(hName+'_dn_lowess')
	hsUp = hNm.Clone(hName+'__'+algo+hUp.GetName().replace(hName,'')[2:])
	hsDn = hNm.Clone(hName+'__'+algo+hDn.GetName().replace(hName,'')[2:])
	#hsUp.Reset()
	#hsDn.Reset()
	hUp_ = hUp.Clone(hName+'_up')
	hDn_ = hDn.Clone(hName+'_dn')
	hUp_.Divide(hNm)
	hDn_.Divide(hNm)
	for ibin in range(1,hNm.GetNbinsX()+1):
		p = ibin-1
		x = (hUp_.GetBinLowEdge(ibin)+hUp_.GetBinLowEdge(ibin+1))/2
		yup = hUp_.GetBinContent(ibin)
		ydn = hDn_.GetBinContent(ibin)
		if symmetrize:
			grinUp.SetPoint(p, x, 1+(yup-ydn)/2)
			grinDn.SetPoint(p, x, 1-(yup-ydn)/2)
		else:
			grinUp.SetPoint(p, x, yup)
			grinDn.SetPoint(p, x, ydn)
	if algo=='super':
		groutUp = gsUp.SmoothSuper(grinUp,"",9,0)
		groutDn = gsDn.SmoothSuper(grinDn,"",9,0)
	elif algo=='kern':
		groutUp = gsUp.SmoothKern(grinUp,"normal",5.0)
		groutDn = gsDn.SmoothKern(grinDn,"normal",5.0)
	else:
		groutUp = gsUp.SmoothLowess(grinUp,"",0.9)
		groutDn = gsDn.SmoothLowess(grinDn,"",0.9)

	for ibin in range(1,hNm.GetNbinsX()+1):
		hsUp.SetBinContent(ibin, hNm.GetBinContent(ibin)*groutUp.GetY()[ibin-1])
		hsDn.SetBinContent(ibin, hNm.GetBinContent(ibin)*groutDn.GetY()[ibin-1])
	return hsUp,hsDn
		
##############################################################################
		
def poissonNormByBinWidth(tgae,hist):
	confLevel = 0.6827 #1sigma
	alpha = 1. - confLevel
	for ibin in range(0,tgae.GetN()):
		width = float(hist.GetBinWidth(ibin+1))
		X = tgae.GetX()[ibin]
		N = tgae.GetY()[ibin]
		L = 0
		if N != 0: L = Math.gamma_quantile(alpha/2.,N,1.)
		U = Math.gamma_quantile_c(alpha/2.,N+1,1.)
		tgae.SetPoint(ibin,X,N/width)
		tgae.SetPointEYlow(ibin,(N-L)/width)
		tgae.SetPointEYhigh(ibin,(U-N)/width)

def poissonErrors(tgae):
	confLevel = 0.6827 #1sigma
	alpha = 1. - confLevel
	for ibin in range(0,tgae.GetN()):
		N = tgae.GetY()[ibin]
		L = 0
		if N != 0: L = Math.gamma_quantile(alpha/2.,N,1.)
		U = Math.gamma_quantile_c(alpha/2.,N+1,1.)
		tgae.SetPointEYlow(ibin,N-L)
		tgae.SetPointEYhigh(ibin,U-N)

def normByBinWidth(h):
	h.SetBinContent(0,0)
	h.SetBinContent(h.GetNbinsX()+1,0)
	h.SetBinError(0,0)
	h.SetBinError(h.GetNbinsX()+1,0)
	
	for bin in range(1,h.GetNbinsX()+1):
		width=h.GetBinWidth(bin)
		content=h.GetBinContent(bin)
		error=h.GetBinError(bin)
		
		h.SetBinContent(bin, content/width)
		h.SetBinError(bin, error/width)

def negBinCorrection(h): #set negative bin contents to zero and adjust the normalization
	norm0=h.Integral()
	if h.GetNbinsY()>1: #2D histogram
		for xBin in range(0,h.GetNbinsX()+2):
			for yBin in range(0,h.GetNbinsY()+2):
				if h.GetBinContent(xBin,yBin)<0: 
					h.SetBinContent(xBin,yBin,0)
					h.SetBinError(xBin,yBin,0)
	else: #1D histogram
		for iBin in range(0,h.GetNbinsX()+2):
			if h.GetBinContent(iBin)<0: 
				h.SetBinContent(iBin,0)
				h.SetBinError(iBin,0)
	if h.Integral()!=0 and norm0>0: h.Scale(norm0/h.Integral())

def overflow(h):
	nBinsX=h.GetXaxis().GetNbins()
	nBinsY=h.GetYaxis().GetNbins()
	if nBinsY>1: #2D histogram
		for xBin in range(0,nBinsX+2):
			content=h.GetBinContent(xBin,nBinsY)+h.GetBinContent(xBin,nBinsY+1)
			error=math.sqrt(h.GetBinError(xBin,nBinsY)**2+h.GetBinError(xBin,nBinsY+1)**2)
			h.SetBinContent(xBin,nBinsY,content)
			h.SetBinError(xBin,nBinsY,error)
			h.SetBinContent(xBin,nBinsY+1,0)
			h.SetBinError(xBin,nBinsY+1,0)
		for yBin in range(0,nBinsY+2):
			content=h.GetBinContent(nBinsX,yBin)+h.GetBinContent(nBinsX+1,yBin)
			error=math.sqrt(h.GetBinError(nBinsX,yBin)**2+h.GetBinError(nBinsX+1,yBin)**2)
			h.SetBinContent(nBinsX,yBin,content)
			h.SetBinError(nBinsX,yBin,error)
			h.SetBinContent(nBinsX+1,yBin,0)
			h.SetBinError(nBinsX+1,yBin,0)
	else: #1D histogram
		content=h.GetBinContent(nBinsX)+h.GetBinContent(nBinsX+1)
		error=math.sqrt(h.GetBinError(nBinsX)**2+h.GetBinError(nBinsX+1)**2)
		h.SetBinContent(nBinsX,content)
		h.SetBinError(nBinsX,error)
		h.SetBinContent(nBinsX+1,0)
		h.SetBinError(nBinsX+1,0)
		
def underflow(h):
	nBinsX=h.GetXaxis().GetNbins()
	nBinsY=h.GetYaxis().GetNbins()
	if nBinsY>1: #2D histogram
		for xBin in range(0,nBinsX+2):
			content=h.GetBinContent(xBin,1)+h.GetBinContent(xBin,0)
			error=math.sqrt(h.GetBinError(xBin,1)**2+h.GetBinError(xBin,0)**2)
			h.SetBinContent(xBin,1,content)
			h.SetBinError(xBin,1,error)
			h.SetBinContent(xBin,0,0)
			h.SetBinError(xBin,0,0)
		for yBin in range(0,nBinsY+2):
			content=h.GetBinContent(1,yBin)+h.GetBinContent(0,yBin)
			error=math.sqrt(h.GetBinError(1,yBin)**2+h.GetBinError(0,yBin)**2)
			h.SetBinContent(1,yBin,content)
			h.SetBinError(1,yBin,error)
			h.SetBinContent(0,yBin,0)
			h.SetBinError(0,yBin,0)
	else: #1D histogram
		content=h.GetBinContent(1)+h.GetBinContent(0)
		error=math.sqrt(h.GetBinError(1)**2+h.GetBinError(0)**2)
		h.SetBinContent(1,content)
		h.SetBinError(1,error)
		h.SetBinContent(0,0)
		h.SetBinError(0,0)
			    
##############################################################################
#Printing tables

from math import log10, floor, ceil

def round_sig(x, sig):
    if x==0: return 0

    result=round(x, sig-int(floor(log10(x)))-1)
    if ceil(log10(x)) >= sig: result=int(result)
    return result

def format(number):
    return str(number)
    
def getMaxWidth(table, index):
    #Get the maximum width of the given column index
    max=0
    for row in table:
        try:
            n=len(format(row[index]))
            if n>max: max=n
        except: pass
    return max

def printTable(table,out=sys.stdout):
    """Prints out a table of data, padded for alignment
    @param out: Output stream (file-like object)
    @param table: The table to print. A list of lists.
    Each row must have the same number of columns. """
    col_paddings = []

    maxColumns=0
    for row in table:
        if len(row)>maxColumns: maxColumns=len(row)

    for i in range(maxColumns):
        col_paddings.append(getMaxWidth(table, i))
        
    for row in table:
        # left col
        if row[0]=='break': row[0]='-'*(sum(col_paddings)+(2*len(col_paddings)))
        print >> out, format(row[0]).ljust(col_paddings[0] + 1),
        # rest of the cols
        for i in range(1, len(row)):
            col = format(row[i]).ljust(col_paddings[i] + 2)
            print >> out, col,
        print >> out

##############################################################################

if __name__=='__main__':

    table=[["A","B","C"],[1,2,3],[4,5],[6],['break'],['a long string','short',7,8]]
    printTable(table)
