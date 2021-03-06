from ROOT import *
import numpy as np
filename =TFile( "ROOT/gammajet_sherpa.root")

varList = ["ntrk","bdt","c1","width"]



def myText(x,y,text,color=1):
    l = TLatex()
    l.SetTextSize(0.025)
    l.SetNDC()
    l.SetTextColor(color)
    l.DrawLatex(x,y,text)
    pass

bin = [0,50,100,150,200,300,400,500,600]

h1 = TH1F('quark','quark',500,0,60)
for i in range(len(bin)-1):
    min = bin[i]
    max = bin[i+1]
    c = TCanvas("c","c",500,500)
    c.SetGrid()
    grparams = []
    for d in range(0,4):
        var = varList[d]
        gamma_centralquark = filename.Get(str(min)+"_LeadingJet_Central_Quark_"+varList[d])
        gamma_centralgluon = filename.Get(str(min)+"_LeadingJet_Central_Gluon_"+varList[d])
        if(gamma_centralquark.Integral() != 0):
            gamma_centralquark.Scale(1./gamma_centralquark.Integral())
        if(gamma_centralgluon.Integral() != 0):
            gamma_centralgluon.Scale(1./gamma_centralgluon.Integral())
        
        x = np.empty(100)
        y = np.empty(100)
        for i in range(100):
            x[i] = gamma_centralquark.Integral(0,i)
            y[i] = 1 - gamma_centralgluon.Integral(0,i)
        
        grparams.append(x)
        grparams.append(y)

    p1 = np.array([0.01,0.99])
    p2 = np.array([0.99,0.01])
    
    gPad.SetTickx()
    gPad.SetTicky()
    gStyle.SetGridStyle(2)
    gStyle.SetGridColor(15)
    g1 = TGraph(100,grparams[0],grparams[1])
    g1.SetLineColor(8)

    g2 = TGraph(100,grparams[2],grparams[3])
    g2.SetLineColor(2)

    g3 = TGraph(100,grparams[4],grparams[5])
    g3.SetLineColor(4)

    g4 = TGraph(100,grparams[6],grparams[7])
    g4.SetLineColor(6)
    
    g5 = TGraph(2,p1,p2)
    g5.SetLineColor(1)
    g5.SetLineStyle(2)
    
    
   # g1.SetMarkerStyle(8)
   # g2.SetMarkerStyle(26)
   # g3.SetMarkerStyle(21)
   # g4.SetMarkerStyle(2)
    g5.GetXaxis().SetTitle("Quark Efficiency")
    g5.GetYaxis().SetTitle("Gluon Rejection")
    g5.SetTitle("") 
    g5.Draw("AL")
    g1.Draw("same C")
    g2.Draw("same C")
    g3.Draw("same C")
    g4.Draw("same C")
    myText(0.15,0.40,"#it{#bf{#scale[1.2]{#bf{ATLAS} Simulation Preliminary}}}")
    myText(0.15,0.36,"#bf{#scale[1.]{#sqrt{s} = 13 TeV}}")
    myText(0.15,0.32,"#bf{#scale[1.]{Anti-k_{t}, EM+JES R=0.4}}")
    myText(0.15,0.28,"#bf{#scale[1.]{|#eta| < 2.1}}")
    myText(0.15,0.24, str(min) + " #bf{#scale[0.8]{ < p_{T} <}} " + str(max) +" GeV" )    
    legend = TLegend(0.61,0.7,0.86,0.86)
    legend.SetTextFont(42)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetFillStyle(0)
    legend.SetNColumns(1)

    legend.AddEntry(g1,"N_{trk}","L")
    legend.AddEntry(g4,"Track width", "L")
    legend.AddEntry(g3,"C1","L")
    legend.AddEntry(g2,"qg-BDT","L")
  
    legend.Draw()  
    c.Print("./plots/gamma+/ROC_plots/ROC_"+str(min)+"-"+ str(max)+"_gamma.pdf")
