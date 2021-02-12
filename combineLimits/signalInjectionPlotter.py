import sys, subprocess, ROOT

limitdir = sys.argv[1]
mass = sys.argv[2]
rInj = int(sys.argv[3])

BR = 'bW0p5_tZ0p25_tH0p25'
if 'BB' in mass: BR = 'tW0p5_bZ0p25_bH0p25'
mass = mass.replace('BB','')

name = limitdir.replace('limits_templatesCR_Feb2021','').replace('limits_templatesSRCR_Feb2021','')+'InjR'+str(rInj)
path = limitdir+'/'+BR+'/cmb/'+mass


post_file = ROOT.TFile.Open(path+'/fitDiagnostics'+name+'.root')
tree_fit_sb = post_file.Get('tree_fit_sb')

# Final plotting
result_can = ROOT.TCanvas('sigpull_can','sigpull_can',800,700)

# fit_status>=0 just ensures you aren't including fits that failed
tree_fit_sb.Draw("(r-"+str(rInj)+")/(rHiErr*(r<"+str(rInj)+")+rLoErr*(r>"+str(rInj)+"))>>sigpull(20,-5,5)","fit_status>=0")
tree_fit_sb.Draw("(r-"+str(rInj)+")>>sigstrength(20,-1,1)","fit_status>=0")

hsigpull = ROOT.gDirectory.Get('sigpull')
hsignstrength = ROOT.gDirectory.Get('sigstrength')

ROOT.gStyle.SetOptFit(1)
hsigpull.Fit("gaus","L")
hsigpull.SetTitle(name)
hsigpull.GetXaxis().SetTitle('(r-'+str(rInj)+')/rErr')
result_can.cd()
hsigpull.Draw('pe')
result_can.Print(path+'/'+name+'_sigpull.png','png')

hsignstrength.Fit("gaus","L")
hsignstrength.SetTitle(name)
hsignstrength.GetXaxis().SetTitle('r-'+str(rInj))
result_can.cd()
hsignstrength.Draw('pe')
result_can.Print(path+'/'+name+'_sigstrength.png','png')
