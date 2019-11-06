#!/usr/bin/python

import os,sys,math,json

theDir = '/user_data/ssagir/fourtops_limits_2019/'
fileDir = 'templates_HT510lep50_2019_8_28'
fileName = 'templates_HT_4TM690_41p53fb_rebinned_stat0p3'

def readLim(thefile):
	try:
		f = open(thefile, 'rU')
		lines = f.readlines()
		f.close()
	except: 
		return None,None,None,None,None
# 	exp    = round(float(lines[1].strip().split()[1]),3)
# 	exp68L = round(float(lines[1].strip().split()[4]),3)
# 	exp68H = round(float(lines[1].strip().split()[5]),3)
# 	exp95L = round(float(lines[1].strip().split()[2]),3)
# 	exp95H = round(float(lines[1].strip().split()[3]),3)
	exp    = "{0:.3f}".format(float(lines[1].strip().split()[1]))
	exp68L = "{0:.3f}".format(float(lines[1].strip().split()[4]))
	exp68H = "{0:.3f}".format(float(lines[1].strip().split()[5]))
	exp95L = "{0:.3f}".format(float(lines[1].strip().split()[2]))
	exp95H = "{0:.3f}".format(float(lines[1].strip().split()[3]))
	print exp,exp68L,exp68H,exp95L,exp95H,

def readSig(thefile):
	with open(thefile, 'r') as f:
		dict = json.load(f)
	return dict[0][0]

#catList = ['tag63','tag54','tag45','tag36','tag27','noTW15','onlyT30','onlyW30','noTW18','onlyT36','onlyW36']
catList = ['165cats','144cats','102cats','90cats','75cats','60cats','45cats','noHOTtW15','onlyHOT30','onlyT30','onlyW30']
jobList = [fileDir+'_disc']
for cat in catList:
	print cat.ljust(7), '\t', 
	
	for job in jobList:
		try: 
			print "{0:.3f}".format(readSig(theDir+job+'/'+cat+'/'+fileName+'.json')),'\t',
		except: print "NONE",'\t',

	readLim(theDir+fileDir+'_lim/'+cat+'/limits_'+fileName+'_expected.txt')

	print

