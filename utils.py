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

def poissonNormByBinWidth(tgae,hist):
	alpha = 1. - 0.6827
	for ibin in range(0,tgae.GetN()):
		width = float(hist.GetBinWidth(ibin+1))
		X = tgae.GetX()[ibin]
		N = tgae.GetY()[ibin]
		L = 0
		if N != 0: L = Math.gamma_quantile(alpha/2.,N,1.)
		U = Math.gamma_quantile_c(alpha/2.,N+1,1)
		tgae.SetPoint(ibin,X,N/width)
		tgae.SetPointEYlow(ibin,(N-L)/width)
		tgae.SetPointEYhigh(ibin,(U-N)/width)

def poissonErrors(tgae):
	alpha = 1. - 0.6827
	for ibin in range(0,tgae.GetN()):
		N = tgae.GetY()[ibin]
		L = 0
		if N != 0: L = Math.gamma_quantile(alpha/2.,N,1.)
		U = Math.gamma_quantile_c(alpha/2.,N+1,1)
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
	for iBin in range(0,h.GetNbinsX()+2):
		if h.GetBinContent(iBin)<0: 
			h.SetBinContent(iBin,0)
			h.SetBinError(iBin,0)
	if h.Integral()!=0 and norm0>0: h.Scale(norm0/h.Integral())

def overflow(h):
	nBinsX=h.GetXaxis().GetNbins()
	content=h.GetBinContent(nBinsX)+h.GetBinContent(nBinsX+1)
	error=math.sqrt(h.GetBinError(nBinsX)**2+h.GetBinError(nBinsX+1)**2)
	h.SetBinContent(nBinsX,content)
	h.SetBinError(nBinsX,error)
	h.SetBinContent(nBinsX+1,0)
	h.SetBinError(nBinsX+1,0)

def underflow(h):
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
