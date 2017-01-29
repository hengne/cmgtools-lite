#!/usr/bin/env python

from ROOT import *
from array import array
from math import *

pu_list=[61000, 61100, 61200, 61300, 61400, 61500, 61600, 61700, 61800, 61900, 62000, 62100, 62200, 62300, 62400, 62500, 62600, 62700, 62800, 62900, 63000]
#pu_list=[57500, 58000, 58500, 59000, 59500, 60000, 60500, 61000, 61500, 62000, 62500, 63000, 63500, 64000, 64500, 65000, 65500, 66000, 66500, 67000, 67500, 68000, 68500, 69000, 69500, 70000, 70500, 71000, 71500, 72000, 72500, 73000, 73500, 74000, 74500, 75000, 75500, 76000, 76500, 77000, 77500]
#pu_list=[69100, 69200, 69300, 69400, 69500, 69600, 69700, 69800, 69900, 70000, 70100, 70200, 70300, 70400, 70500]


inputdir='/dataf/heli/XZZ/80X_20160711_LinksForPUScan'


outtag='scan_pu_pass2_smp'
#outtag='scan_pu_pass2_b2g'

DataHLT="DblLepHLT"
#DataHLT="SglLepHLT"

outtag += '_'+DataHLT


dtfileName='SingleEMU_Run2016BC_PromptReco.root'
#mcfileName='DYJetsToLL_M50_PUScan.root'
mcfileName='DYJetsToLL_M50_PUScanV2.root'

lumiTag = 'CMS 13 TeV 2016 L=6.26 fb^{-1}'

cuts_b2g_z='(((abs(llnunu_l1_l1_pdgId)==13&&llnunu_l1_l1_pt>50&&abs(llnunu_l1_l1_eta)<2.1&&llnunu_l1_l2_pt>20&&abs(llnunu_l1_l2_eta)<2.4)||(abs(llnunu_l1_l1_pdgId)==11&&llnunu_l1_l1_pt>115&&abs(llnunu_l1_l1_eta)<2.5&&llnunu_l1_l2_pt>35&&abs(llnunu_l1_l2_eta)<2.5))&&(llnunu_l1_mass>70&&llnunu_l1_mass<110))'

cuts_smp_z='(((abs(llnunu_l1_l1_pdgId)==13&&abs(llnunu_l1_l2_pdgId)==13&&llnunu_l1_l1_pfMuonId&&llnunu_l1_l2_pfMuonId&&llnunu_l1_l1_pt>25&&abs(llnunu_l1_l1_eta)<2.4&&llnunu_l1_l2_pt>25&&abs(llnunu_l1_l2_eta)<2.4)'
cuts_smp_z+='||(abs(llnunu_l1_l1_pdgId)==11&&abs(llnunu_l1_l2_pdgId)==11&&llnunu_l1_l1_pt>25&&abs(llnunu_l1_l1_eta)<2.5&&llnunu_l1_l2_pt>25&&abs(llnunu_l1_l2_eta)<2.5))&&(llnunu_l1_mass>70&&llnunu_l1_mass<110))'

cuts=cuts_b2g_z
#cuts=cuts_smp_z


gROOT.ProcessLine('.x tdrstyle.C')

dtfile = TFile(inputdir+'/'+dtfileName)
mcfile = TFile(inputdir+'/'+mcfileName)
dttree=dtfile.Get('tree')
mctree=mcfile.Get('tree')



fout = TFile(outtag+'.root','recreate')

plots = TCanvas('plots','plots',600,800)
plots.SetLeftMargin(0.15)
plots.SetBottomMargin(0.15)


lumipt = TPaveText(0.45,0.8,0.9,0.9,"brNDC")
lumipt.SetBorderSize(0)
lumipt.SetTextAlign(12)
lumipt.SetFillStyle(0)
lumipt.SetTextFont(42)
lumipt.SetTextSize(0.045)
lumipt.AddText(0.15,0.15, lumiTag)

plots.Print(outtag+'.ps[')


ress = array('d', 50*[0.0])

hs_dt = []
hs_mc = []
hs_res = []
lg_dtmc = []
chi2ndf_pu = []
pvalue_pu = []


for pu in pu_list:
    print 'Scanning MB xsec = '+str(pu)+' ub'
    hdt = TH1D("hdt","hdt_"+str(pu),50,0,50)    
    hmc = TH1D("hmc","hmc_"+str(pu),50,0,50)    
    hdt.SetName('hdt_'+str(pu))
    hmc.SetName('hmc_'+str(pu))
    hdt.SetTitle('nVert: MB xsec= {pu:n} ub {lumitag:s}'.format(pu=pu,lumitag=lumiTag))
    hdt.Sumw2()
    hmc.Sumw2()
    if DataHLT=="DblLepHLT" :
        dttree.Draw('nVert>>hdt_'+str(pu), '('+cuts+'&&((HLT_MUMU&&!HLT_ELEL)||(HLT_ELEL)))', 'e')
    elif DataHLT=="SglLepHLT" :
        dttree.Draw('nVert>>hdt_'+str(pu), '('+cuts+'&&((HLT_MU&&!HLT_ELE)||(HLT_ELE)))', 'e')
    else: 
        dttree.Draw('nVert>>hdt_'+str(pu), '('+cuts+')', 'e')
    mctree.Draw('nVert>>hmc_'+str(pu), '(('+cuts+')*(genWeight*puWeight'+str(pu)+'))', 'e')
    hmc.Scale(hdt.Integral()/hmc.Integral())
    hdt.GetXaxis().SetTitle('N vertices')
    hmc.GetXaxis().SetTitle('N vertices')
    hdt.GetYaxis().SetTitle('Events')
    hmc.GetYaxis().SetTitle('Events')
    hdt.SetMarkerStyle(20)
    hmc.SetLineColor(4)
    hmc.SetMarkerColor(4)
    ymax = max(hdt.GetMaximum(),hmc.GetMaximum())*1.2
    hdt.GetYaxis().SetRangeUser(0,ymax)
    hmc.GetYaxis().SetRangeUser(0,ymax)

    pv = hdt.Chi2Test(hmc, "UW P", ress)
    #print 'p-value pu '+str(pu)+' : '+str(pv)
    pvalue_pu.append(pv)
    chi2ndf = hdt.Chi2Test(hmc, "UW P CHI2/NDF", ress)
    chi2ndf_pu.append(chi2ndf)
    hres = TH1D("hres_"+str(pu),"hres_"+str(pu), 50,0, 50)
    hres.Sumw2()
    for ib in range(hres.GetNbinsX()):
        hres.SetBinContent(ib+1, ress[ib])
        hres.SetBinError(ib+1, 1.0)
    hres.SetMarkerStyle(20)  
    hres.SetMarkerColor(2)
    hres.GetXaxis().SetTitle('N vertices')
    hres.GetYaxis().SetTitle('Normalized Residual (Pull)')
    hres.SetTitle('Pull: MB xsec= {pu:n} ub , Chi2/Ndf= {chi2ndf:.2f}, P-value= {pv:.3E}'.format(pu=pu,chi2ndf=chi2ndf,pv=pv))

    plots.Clear()
    plots.Divide(1,2)
    pad1=plots.cd(1)
    pad1.SetTopMargin(0.10)
    pad1.SetBottomMargin(0.15)
    pad1.SetLeftMargin(0.15)
    hdt.Draw()
    hmc.Draw('hist same')
    lumipt.Draw()
    pad2=plots.cd(2)
    pad2.SetTopMargin(0.10)
    pad2.SetBottomMargin(0.15)
    pad2.SetLeftMargin(0.15)
    hres.Draw()
    lumipt.Draw()
    plots.Print(outtag+'.ps')
    plots.Clear()

    hs_dt.append(hdt)
    hs_mc.append(hmc)
    hs_res.append(hres)
  
    fout.cd()
    hdt.Write()
    hmc.Write()
    hres.Write() 
    plots.Write('plots_'+str(pu))


gr_pvalue_pu = TGraph()
for i in range(len(pu_list)):
  gr_pvalue_pu.SetPoint(i,pu_list[i]*0.001,pvalue_pu[i])
gr_pvalue_pu.SetName('gr_pvalue_pu')
gr_pvalue_pu.SetTitle('Pileup Data/MC matching p-value vs. MB xsec')
gr_pvalue_pu.SetMarkerStyle(20)
gr_pvalue_pu.GetXaxis().SetTitle('MB xsec (mb)')
gr_pvalue_pu.GetYaxis().SetTitle('p-value')
gr_pvalue_pu.GetXaxis().SetRangeUser(min(pu_list)*0.001*0.9,max(pu_list)*0.001*1.1)
gr_pvalue_pu.GetYaxis().SetRangeUser(min(pvalue_pu)*1e-10,max(pvalue_pu)*1e20)
gr_pvalue_pu.Sort()

#fc_pvalue_pu = TF1("fc_pvalue_pu", "pol2", min(pu_list)*0.1*0.9, max(pu_list)*0.1*1.1)
#gr_pvalue_pu.Fit(fc_pvalue_pu)
#x_maxpvalue=fc_pvalue_pu.GetMaximumX()
#gr_pvalue_pu.SetTitle('Pileup Data/MC matching p-value vs. MB xsec, max at {xm:.3f} mb'.format(xm=x_maxpvalue))


gr_chi2ndf_pu = TGraph()
for i in range(len(pu_list)):
  gr_chi2ndf_pu.SetPoint(i,pu_list[i]*0.001,chi2ndf_pu[i])
gr_chi2ndf_pu.SetName('gr_chi2ndf_pu')
gr_chi2ndf_pu.SetTitle('Pileup Data/MC matching Chi2/Ndf vs. MB xsec')
gr_chi2ndf_pu.SetMarkerStyle(20)
gr_chi2ndf_pu.GetXaxis().SetTitle('MB xsec (mb)')
gr_chi2ndf_pu.GetYaxis().SetTitle('Chi2/Ndf')
gr_chi2ndf_pu.GetXaxis().SetRangeUser(min(pu_list)*0.001*0.9,max(pu_list)*0.001*1.1)
gr_chi2ndf_pu.GetYaxis().SetRangeUser(min(chi2ndf_pu)*0.98,max(chi2ndf_pu)*1.1)
gr_chi2ndf_pu.Sort()

fc_chi2ndf_pu = TF1("fc_chi2ndf_pu", "pol2", min(pu_list)*0.001*0.9, max(pu_list)*0.001*1.1)
gr_chi2ndf_pu.Fit(fc_chi2ndf_pu)
x_minchi2ndf=fc_chi2ndf_pu.GetMinimumX()
#calculate minimum and uncertainty
b=fc_chi2ndf_pu.GetParameter(1);
c=fc_chi2ndf_pu.GetParameter(2);
br=fc_chi2ndf_pu.GetParError(1);
cr=fc_chi2ndf_pu.GetParError(2);
xmin=-b/2./c;
xminerr=sqrt(1./2/2/c/c*br*br+b*b/2/2/c/c/c/c*cr*cr)
gr_chi2ndf_pu.SetTitle('Pileup Data/MC matching Chi2/Ndf vs. MB xsec, min at {xm:.3f}#pm{xmr:.3f} mb'.format(xm=xmin, xmr=xminerr))

print '#########################################################################'
print ' Pileup MB xsec fitresults: best MB xsec = {xm:.3f}#pm{xmr:.3f} mb'.format(xm=xmin, xmr=xminerr)
print '#########################################################################'

plots.Clear()
plots.Divide(1,2)
pad1=plots.cd(1)
pad1.SetTopMargin(0.10)
pad1.SetBottomMargin(0.15)
pad1.SetLeftMargin(0.15)
pad1.SetLogy(1)
gr_pvalue_pu.Draw("apl")
lumipt.Draw()
pad2=plots.cd(2)
pad2.SetTopMargin(0.10)
pad2.SetBottomMargin(0.15)
pad2.SetLeftMargin(0.15)
gr_chi2ndf_pu.Draw("apl")
lumipt.Draw()
plots.Print(outtag+'.ps')
pad1.SetLogy(0)
plots.Clear()

fout.cd()
gr_pvalue_pu.Write()
gr_chi2ndf_pu.Write()
plots.Write('plots_gr_pvalue_chi2ndf_pu')


plots.Print(outtag+'.ps]')

gROOT.ProcessLine('.! ps2pdf '+outtag+'.ps')

fout.Close()