#!/usr/bin/env python

import optparse, os, sys
from ROOT import *


lumi=36.814



parser = optparse.OptionParser()
parser.add_option("-i","--input_tag",dest="intag", default='pileup_DATA_80x',help="input file tag")
parser.add_option("-o","--output_tag",dest="outtag", default='pileup_MC_80x',help="output files tag")
(options,args)=parser.parse_args()

gROOT.SetBatch(True)
gROOT.ProcessLine('.x tdrstyle.C')

# 2016_25ns_Moriond17MC_PoissonOOTPU
# https://github.com/cms-sw/cmssw/blob/CMSSW_8_0_20/SimGeneral/MixingModule/python/mix_2016_25ns_Moriond17MC_PoissonOOTPU_cfi.py

if (True): 

    intag = options.intag
    outtag = options.outtag

    pdf =[1.78653e-05 ,2.56602e-05 ,5.27857e-05 ,8.88954e-05 ,0.000109362 ,0.000140973 ,0.000240998 ,0.00071209 ,0.00130121 ,0.00245255 ,0.00502589 ,0.00919534 ,0.0146697 ,0.0204126 ,0.0267586 ,0.0337697 ,0.0401478 ,0.0450159 ,0.0490577 ,0.0524855 ,0.0548159 ,0.0559937 ,0.0554468 ,0.0537687 ,0.0512055 ,0.0476713 ,0.0435312 ,0.0393107 ,0.0349812 ,0.0307413 ,0.0272425 ,0.0237115 ,0.0208329 ,0.0182459 ,0.0160712 ,0.0142498 ,0.012804 ,0.011571 ,0.010547 ,0.00959489 ,0.00891718 ,0.00829292 ,0.0076195 ,0.0069806 ,0.0062025 ,0.00546581 ,0.00484127 ,0.00407168 ,0.00337681 ,0.00269893 ,0.00212473 ,0.00160208 ,0.00117884 ,0.000859662 ,0.000569085 ,0.000365431 ,0.000243565 ,0.00015688 ,9.88128e-05 ,6.53783e-05 ,3.73924e-05 ,2.61382e-05 ,2.0307e-05 ,1.73032e-05 ,1.435e-05 ,1.36486e-05 ,1.35555e-05 ,1.37491e-05 ,1.34255e-05 ,1.33987e-05 ,1.34061e-05 ,1.34211e-05 ,1.34177e-05 ,1.32959e-05 ,1.33287e-05]


    print "Summer16 PDF nbins: ",len(pdf)




    fdt=TFile(intag+'.root')
    pileup_dt = fdt.Get('pileup')
    nbins = pileup_dt.GetXaxis().GetNbins()
    xmin = pileup_dt.GetXaxis().GetBinLowEdge(1)
    xmax = pileup_dt.GetXaxis().GetBinUpEdge(nbins)
    pileup_dt.Scale(1.0/pileup_dt.Integral())
    fmc=TFile(outtag+'.root','recreate')
    pileup_mc=TH1F('pileup','pileup',nbins,xmin,xmax)
    pileup_mc.Sumw2()
    for i in range(nbins):
        if i< len(pdf): pileup_mc.SetBinContent(i+1,pdf[i])
        else: pileup_mc.SetBinContent(i+1, 0.0)

    pileup_mc.Scale(1.0/pileup_mc.Integral())
    gStyle.SetStatStyle(0)
    pileup_dt.SetStats(0)
    pileup_mc.SetStats(0)

    plotfile=outtag+"_puweight80x.pdf"

    plots = TCanvas("plots","plots",600,600)
    plots.SetLeftMargin(0.17)
    plots.SetBottomMargin(0.17)
   
    plots.Print(plotfile+"[")

    pileup_dt.SetLineColor(kRed)
    pileup_dt.SetMarkerColor(kRed)
    pileup_dt.SetMarkerStyle(20)
    pileup_dt.GetXaxis().SetTitle('N pileup')
    pileup_dt.GetYaxis().SetTitle('Norm.')
    pileup_mc.SetLineColor(kBlue)
    pileup_mc.SetMarkerColor(kBlue)
    pileup_mc.SetMarkerStyle(20)
    pileup_mc.SetLineWidth(2)
    pileup_mc.GetXaxis().SetTitle('N pileup')
    pileup_mc.GetYaxis().SetTitle('Norm.')

    pileup_mc.GetYaxis().SetTitleOffset(1.5)
    pileup_dt.GetYaxis().SetTitleOffset(1.5)
    lg = TLegend(0.6,0.7,0.85,0.85)
    lg.AddEntry(pileup_dt, "Data", "pl")
    lg.AddEntry(pileup_mc, "MC", "pl")

    pt = TPaveText(0.1577181,0.9562937,0.9580537,0.9947552,"brNDC")
    pt.SetBorderSize(0)
    pt.SetTextAlign(12)
    pt.SetFillStyle(0)
    pt.SetTextFont(42)
    pt.SetTextSize(0.03)
    text = pt.AddText(0.15,0.3,"CMS Preliminary")
    text = pt.AddText(0.55,0.3,"#sqrt{s} = 13 TeV, 2016, L = "+"{:.3}".format(float(lumi))+" fb^{-1}")


    pileup_dt.GetXaxis().SetRangeUser(0,100)
    pileup_mc.GetXaxis().SetRangeUser(0,100)
    pileup_mc.Draw()
    pileup_dt.Draw("SAME")
    lg.Draw("same")
    pt.Draw()

    plots.Print(plotfile)

    # log
    plots.SetLogy(1)
    plots.Print(plotfile)
    plots.SetLogy(0)

    # ratio
    puweight = pileup_dt.Clone("puweight")
    puweight.Divide(pileup_mc)
    puweight.GetXaxis().SetRangeUser(0,80)
    puweight.GetYaxis().SetTitle("PU Weight")
    lg1 = TLegend(0.65,0.7,0.9,0.9)
    lg1.AddEntry(puweight, "Data/MC", "pl")

    plots.Clear()
    puweight.Draw()
    lg1.Draw("same")
    pt.Draw()
    plots.Print(plotfile)

    # log
    plots.SetLogy(1)
    plots.Print(plotfile)
    plots.SetLogy(0)

    # print ratio 
    puwts = [puweight.GetBinContent(i+1) for i in range(50)]
    print puwts

    pileup_dt.Write('pileup_dt')
    pileup_mc.Write('pileup_mc')
    pileup_mc.Write('pileup')
    puweight.Write('puweight_dtmc')
    puweight.Write('puweight')
    fmc.Close()


    #close plot file
    plots.Print(plotfile+"]")


#if __name__ == "__main__":
#    makePURatio()


