#!/usr/bin/env python

from math import sqrt

hname2023_f = lambda hname: "highest_emtf2023_" + hname[13:]

donotdelete = []

# Functions
def make_ptcut(h):
  use_overflow = True
  binsum = 0
  binerr2 = 0
  for ib in xrange(h.GetNbinsX()+2-1, 0-1, -1):
    if (not use_overflow) and (ib == 0 or ib == h.GetNbinsX()+1):
      continue
    binsum += h.GetBinContent(ib)
    binerr2 += h.GetBinError(ib)**2
    h.SetBinContent(ib, binsum)
    h.SetBinError(ib, sqrt(binerr2))
  return

def make_rate(h, nevents):
  orbitFreq = 11246.
  nCollBunches = 2808
  nZeroBiasEvents = nevents
  convFactorToHz = orbitFreq * nCollBunches / nZeroBiasEvents
  h.Scale(convFactorToHz / 1000.)
  return



# ______________________________________________________________________________
if __name__ == '__main__':
  from ROOT import gROOT, gPad, gStyle, TFile, TCanvas, TH1F, TH2F, TPolyLine, TLatex, TColor, TEfficiency, TLine, TGraph

  # ____________________________________________________________________________
  # Setup basic drawer
  gROOT.LoadMacro("tdrstyle.C")
  gROOT.ProcessLine("setTDRStyle();")
  #gROOT.SetBatch(True)
  gStyle.SetMarkerStyle(1)
  gStyle.SetEndErrorSize(0)
  gStyle.SetPadGridX(True)
  gStyle.SetPadGridY(True)
  gROOT.ForceStyle()

  infile = "histos_tbb_add.20.root"
  tfile = TFile.Open(infile)

  h_nevents = tfile.Get("nevents")
  assert h_nevents != None, "Cannot get nevents"
  nevents = h_nevents.GetBinContent(2)

  tline = TLine()
  tline.SetLineColor(920+2)  # kGray+2
  tline.SetLineStyle(2)


  # ____________________________________________________________________________
  # highest_emtf_absEtaMin0_absEtaMax2.5_qmin12_pt

  hname_pairs = [
    ("highest_emtf_absEtaMin1.24_absEtaMax2.4_qmin12_pt", "emtf2023_rate_reduction"),
    ("highest_emtf_absEtaMin1.24_absEtaMax1.65_qmin12_pt", "emtf2023_rate_reduction_1"),
    ("highest_emtf_absEtaMin1.65_absEtaMax2.15_qmin12_pt", "emtf2023_rate_reduction_2"),
    ("highest_emtf_absEtaMin2.15_absEtaMax2.4_qmin12_pt", "emtf2023_rate_reduction_3"),
  ]

  for hname, imgname in hname_pairs:
    h = tfile.Get(hname)
    h = h.Clone(h.GetName() + "_clone")
    h.Sumw2()
    x0 = h.Integral()
    x1 = h.Integral(h.FindBin(20), h.FindBin(100))
    make_ptcut(h)
    make_rate(h, nevents)
    x2 = h.GetBinContent(h.FindBin(20))
    h.SetFillColor(632)  # kRed
    h.SetFillStyle(3003)
    h.SetLineColor(632)  # kRed
    h.SetLineWidth(2)
    h.GetXaxis().SetTitle("p_{T} threshold [GeV]")
    h.GetYaxis().SetTitle("Trigger rate [kHz]")
    h.GetYaxis().SetTitleOffset(1.3)
    denom = h.Clone("denom")
    denom.SetMaximum(1.2e4)
    denom.SetMinimum(1e-1)

    h = tfile.Get(hname2023_f(hname))
    h = h.Clone(h.GetName() + "_clone")
    h.Sumw2()
    x3 = h.Integral()
    x4 = h.Integral(h.FindBin(20), h.FindBin(100))
    make_ptcut(h)
    make_rate(h, nevents)
    x5 = h.GetBinContent(h.FindBin(20))
    h.SetFillColor(600)  # kBlue
    h.SetFillStyle(3003)
    h.SetLineColor(600)  # kBlue
    h.SetLineWidth(2)
    h.GetXaxis().SetTitle("p_{T} threshold [GeV]")
    h.GetYaxis().SetTitle("Trigger rate [kHz]")
    h.GetYaxis().SetTitleOffset(1.3)
    numer = h.Clone("numer")

    ratio = numer.Clone("ratio")
    ratio.Divide(numer, denom, 1, 1, "")
    x6 = ratio.GetBinContent(ratio.FindBin(20))
    ratio.SetMinimum(0)
    ratio.SetMaximum(2)
    ratio.GetYaxis().SetTitle("ratio")
    print (x0, x1, x2), (x3, x4, x5), x6

    # ____________________________________________________________________________
    # rate reduction
    cc1 = TCanvas("cc1", "cc1", 600, 700)
    cc1.Divide(1,2)
    cc1_1 = cc1.GetPad(1)
    cc1_1.SetPad(0.01,0.25,0.99,0.99)
    cc1_1.SetBottomMargin(0.01)
    cc1_1.SetGrid()
    cc1_1.SetLogy()
    cc1_2 = cc1.GetPad(2)
    cc1_2.SetPad(0.01,0.01,0.99,0.25)
    cc1_2.SetTopMargin(0.01)
    cc1_2.SetBottomMargin(0.43)
    cc1_2.SetGrid()

    denom.SetLabelSize(0.0);
    denom.GetXaxis().SetTitleSize(0.00)
    denom.GetYaxis().SetLabelSize(0.05)
    denom.GetYaxis().SetTitleSize(0.06)
    denom.GetYaxis().SetTitleOffset(1.10)
    ratio.GetXaxis().SetLabelSize(0.15)
    ratio.GetXaxis().SetTitleSize(0.18)
    ratio.GetXaxis().SetTitleOffset(1.10)
    ratio.GetYaxis().SetLabelSize(0.14)
    ratio.GetYaxis().SetTitleSize(0.18)
    ratio.GetYaxis().SetTitleOffset(0.37)
    ratio.GetYaxis().SetNdivisions(502)
    ratio.GetYaxis().SetLabelOffset(0.01)
    draw_option = "hist"
    draw_err_option = "e3"

    cc1_1.cd()
    denom.SetStats(0)
    denom.Draw(draw_err_option)
    numer.Draw(draw_err_option + " same")

    denom_no_fill = denom.Clone("denom_no_fill")
    denom_no_fill.SetFillStyle(0)
    denom_no_fill.Draw(draw_option + " same")
    numer_no_fill = numer.Clone("numer_no_fill")
    numer_no_fill.SetFillStyle(0)
    numer_no_fill.Draw(draw_option + " same")


    cc1_2.cd()
    ratio.SetStats(0)
    ratio.Draw(draw_err_option)
    xmin, xmax = ratio.GetXaxis().GetXmin(), ratio.GetXaxis().GetXmax()
    tline.DrawLine(xmin, 1.0, xmax, 1.0)

    ratio_no_fill = ratio.Clone("ratio_no_fill")
    ratio_no_fill.SetFillStyle(0)
    ratio_no_fill.Draw(draw_option + " same")

    cc1.cd()
    gPad.Print("figures_winter/" + imgname + ".png")


    if imgname == "emtf2023_rate_reduction":
      outfile = TFile.Open("figures_winter/" + imgname + ".root", "RECREATE")
      for obj in [denom, numer, ratio, cc1]:
        obj.Write()
      outfile.Close()

  # ____________________________________________________________________________
  # PU dependence

  if False:
    gr10 = TGraph(3)
    gr10.SetPoint(0, 0, 0)
    gr10.SetPoint(1, 140, 51.4486)
    gr10.SetPoint(2, 200, 70.1479)

    gr20 = TGraph(3)
    gr20.SetPoint(0, 0, 0)
    gr20.SetPoint(1, 140, 8.37764)
    gr20.SetPoint(2, 200, 10.9988)

    gr10a = TGraph(3)
    gr10a.SetPoint(0, 0, 0)
    gr10a.SetPoint(1, 140, 51.4486)
    gr10a.SetPoint(2, 200, 51.4486*200/140)

    gr20a = TGraph(3)
    gr20a.SetPoint(0, 0, 0)
    gr20a.SetPoint(1, 140, 8.37764)
    gr20a.SetPoint(2, 200, 8.37764*200/140)

    palette = ("#333333", "#377eb8", "#e41a1c", "#984ea3", "#ff7f00", "#4daf4a")
    palette = map(lambda x: TColor.GetColor(x), palette)

    gr10.SetMarkerStyle(20)
    gr10.SetMarkerSize(1)
    gr10.SetMarkerColor(palette[1])
    gr20.SetMarkerStyle(20)
    gr20.SetMarkerSize(1)
    gr20.SetMarkerColor(palette[2])

    gr10a.SetLineStyle(2)
    gr10a.SetLineColor(palette[1])
    gr20a.SetLineStyle(2)
    gr20a.SetLineColor(palette[2])

    gr10.Draw("AP")
    gr20.Draw("P")

    gr10a.Draw("C")
    gr20a.Draw("C")

    gr10.GetHistogram().GetXaxis().SetTitle("PU")
    gr10.GetHistogram().GetYaxis().SetTitle("Trigger rate [kHz]")
    imgname = "rate_pu_dependence"
    gPad.Print("figures_winter/" + imgname + ".png")
