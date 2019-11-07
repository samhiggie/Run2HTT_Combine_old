#!/usr/bin/env python
import ROOT
import argparse

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gStyle.SetOptStat(0)

def add_lumi(year):
    lowX=0.60
    lowY=0.9
    lumi  = ROOT.TPaveText(lowX, lowY+0.0, lowX+0.30, lowY+0.1, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.04)
    lumi.SetTextFont (   42 )
    if year=="2016":
       lumi.AddText("2016, 35.9 fb^{-1} (13 TeV)")
    elif year=="2017":
       lumi.AddText("2017, 41.5 fb^{-1} (13 TeV)")
    elif year=="2018":
       lumi.AddText("2018, 59.5 fb^{-1} (13 TeV)")
    elif year=="all":
       lumi.AddText("139.9 fb^{-1} (13 TeV)")
    return lumi

def add_channel(channel):
    lowX=0.45
    lowY=0.9
    lumi  = ROOT.TPaveText(lowX, lowY+0.0, lowX+0.30, lowY+0.1, "NDC")
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.SetTextSize(0.04)
    lumi.SetTextFont (   42 )
    if channel=="mt":
       lumi.AddText("#mu#tau_{h}")
    if channel=="et":
       lumi.AddText("e#tau_{h}")
    if channel=="em":
       lumi.AddText("e#mu")
    if channel=="tt":
       lumi.AddText("#tau_{h}#tau_{h}")
    if channel == "all":
        lumi.AddText("")

    return lumi

def add_CMS():
    lowX=0.05
    lowY=0.9
    lumi  = ROOT.TPaveText(lowX, lowY+0.0, lowX+0.15, lowY+0.1, "NDC")
    lumi.SetTextFont(61)
    lumi.SetTextSize(0.045)
    lumi.SetBorderSize(   0 )
    lumi.SetFillStyle(    0 )
    lumi.SetTextAlign(   12 )
    lumi.SetTextColor(    1 )
    lumi.AddText("CMS Preliminary")
    return lumi


def translate_categ(i):
   if "ggH_PTH_0_200_0J_PTH_0_10_htt125" in i: return "ggH-0j/pT[0,10]"
   elif "ggH_PTH_0_200_0J_PTH_10_200_htt125" in i: return "ggH-0j/pT[10-200]"
   elif "ggH_PTH_0_200_1J_PTH_60_120_htt125" in i: return "ggH-1j/pT[60-120]"
   elif "ggH_PTH_0_200_1J_PTH_0_60_htt125" in i: return "ggH-1j/pT[0-60]"
   elif "ggH_PTH_0_200_1J_PTH_120_200_htt125" in i: return "ggH-1j/pT[120-200]"
   elif "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125" in i: return "ggH-2j/mJJ<350/pT[60,120]"
   elif "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125" in i: return "ggH-2j/mJJ<350/pT[0,60]"
   elif "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125" in i: return "ggH-2j/mJJ<350/pT[120,200]"
   elif "ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125" in i: return "ggH-2j/mJJ[350,700]/pTHJJ[0,25]"
   elif "ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125" in i: return "ggH-2j/mJJ[350,700]/pTHJJ>25"
   elif "ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125" in i: return "ggH-2j/mJJ>700/pTHJJ><5"
   elif "ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125" in i: return "ggH-2j/mJJ>700/pTHJJ>25"
   elif "ggH_PTH_0_200_GE2J_MJJ_GE350" in i: return "ggH-2j/mJJ>350"
   elif "ggH_PTH_GE200_htt125" in i: return "ggH/pT>200"
   elif "qqH_0J_htt125" in i: return "qqH/0j"
   elif "qqH_1J_htt125" in i: return "qqH/1j"
   elif "qqH_LT2J" in i: return "qqH/<2j"
   elif "qqH_GE2J_MJJ_0_60_htt125" in i: return "qqH-2j/mJJ[0,60]"
   elif "qqH_GE2J_MJJ_60_120_htt125" in i: return "qqH-2j/mJJ[60,120]"
   elif "qqH_GE2J_MJJ_120_350_htt125" in i: return "qqH-2j/mJJ[120,350]"
   elif "qqH_GE2J_MJJ_0_350" in i: return "qqH-2j/mJJ<350"
   elif "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125" in i: return "ggH-2j/mJJ[350,700]/pTHJJ<25"
   elif "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125" in i: return "ggH-2j/mJJ[350,700]/pTHJJ>25"
   elif "qqH_GE2J_MJJ_350_700_PTH_0_200" in i: return "qqH-2j/350<mJJ<700"
   elif "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125" in i: return "qqH-2j/mJJ>700/pTHJJ<25"
   elif "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125" in i: return "qqH-2j/mJJ>700/ptHJJ>25"
   elif "qqH_GE2J_MJJ_GE700_PTH_0_200" in i: return "qqH-2j/mJJ>700"
   elif "qqH_GE2J_MJJ_GE350_PTH_GE200_htt125" in i: return "qqH-2j/mJJ>350/pT>200"
   elif "WH" in i: return "WH"
   elif "ZH" in i: return "ZH"
   elif "ggH" in i: return "ggH"
   elif "qqH" in i: return "qqH"
   else: return ""

def is_included(mycat,type):
    included=0
    if type=="stage0" and (translate_categ(mycat)=="WH" or translate_categ(mycat)=="ZH" or translate_categ(mycat)=="qqH" or translate_categ(mycat)=="ggH"): 
       included=1
    if type=="stage1-all" and not (translate_categ(mycat)=="WH" or translate_categ(mycat)=="ZH" or translate_categ(mycat)=="qqH" or translate_categ(mycat)=="ggH"):
       included=1
    if type=="stage1-select" and not (translate_categ(mycat)=="WH" or translate_categ(mycat)=="ZH" or translate_categ(mycat)=="qqH" or translate_categ(mycat)=="ggH") and not "_25" in mycat and not "qqH_0J" in mycat and not "qqH_1J" in mycat and not "GE25" in mycat and not "qqH_GE2J_MJJ_0_60" in mycat and not "qqH_GE2J_MJJ_60_120" in mycat and not "qqH_GE2J_MJJ_120_350" in mycat:
       included=1
    return included

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', default=None, help='Output name')
parser.add_argument('--channel', '-c', default=None, help='Output name')
parser.add_argument('--year', '-y', default=None, help='Output name')
parser.add_argument('--output', '-o', default=None, help='Output name')
parser.add_argument('--type', '-t', default="stage0", help='stage0, stage1-select, stage1-all')

args = parser.parse_args()

# Canvas and pads
canv = ROOT.TCanvas(args.output, args.output,600,600)
canv.cd()
canv.SetLeftMargin(0.5)

f = open(args.input, "r")

nlines=0

k=0
for x in f:
  if ":" in x:
    mycat=""
    if k>0:
       mycat=x.split("r_")[1].split(" ")[0]
    print mycat,is_included(mycat,args.type)
    if is_included(mycat,args.type):
       nlines=nlines+1
    k=k+1

print nlines

f.seek(0)

axis = ROOT.TH2F('axis', '', 1, 0., 10, 10, 0.01, nlines)
axis.GetXaxis().SetTitle("#mu")
axis.GetYaxis().SetLabelSize(0)
axis.GetYaxis().SetTickLength(0)
axis.Draw()

y_pos = float(nlines)-0.5
x_text = 1.85

f.seek(0)

gr = ROOT.TGraphAsymmErrors(nlines-1)
gr.SetMarkerStyle(20)
combineMu=0
lowBnad=0
highBand=0
i=0
ii=0
categ=[]
result=[]

for x in f:
  if ":" in x:
    mean=round(1.0, 2)
    if "N/A" in x:
        up=24.0
        down=-26.0
    else:
        up= round(float(x.split("+")[1][:5]),2)
        down=round(float(x.split("-")[1].split("/")[0]),2)

    mycat=""
    mycat2=""
    if ii>0:
       mycat=translate_categ(x.split("r_")[1].split(" ")[0])
       mycat2=x.split("r_")[1].split(" ")[0]

    if ii>0 and is_included(mycat2,args.type):
      gr.SetPoint(i, mean, y_pos)
      gr.SetPointError(i,down ,up, 0, 0)

    elif ii==0:
      combineMu= mean; lowBnad=down; highBand=up;

    myresult=str(mean)+" -"+str(down)+"/-"+str(up)

    print mycat2,is_included(mycat2,args.type)
    if is_included(mycat2,args.type):

      if args.type=="stage0":
         categ.append( ROOT.TPaveText(0.01, 0.90-(i+1)*(0.905-0.105)/nlines+0.5*(0.905-0.105)/nlines, 0.25, 0.90+0.01-(i+1)*(0.905-0.105)/nlines+0.5*(0.905-0.105)/nlines, "NDC"))
      else:
         categ.append( ROOT.TPaveText(0.01, 0.90-(i+1)*(0.905-0.105)/nlines+0.5*(0.905-0.105)/nlines, 0.35, 0.90+0.01-(i+1)*(0.905-0.105)/nlines+0.5*(0.905-0.105)/nlines, "NDC"))
      categ[i].SetBorderSize(   0 )
      categ[i].SetFillStyle(    0 )
      categ[i].SetTextAlign(   32 )
      categ[i].SetTextSize ( 0.023 )
      if args.type=="stage0":
         categ[i].SetTextSize ( 0.04 )
      categ[i].SetTextColor(    1 )
      categ[i].SetTextFont (   42 )
      categ[i].AddText(mycat)
      if ii>0:
         categ[i].Draw("same")

      if args.type=="stage0":
         result.append( ROOT.TPaveText(0.25, 0.90-(i+1)*(0.905-0.105)/nlines+0.5*(0.905-0.105)/nlines, 0.49, 0.90+0.01-(i+1)*(0.905-0.105)/nlines+0.5*(0.905-0.105)/nlines, "NDC"))
      else:
         result.append( ROOT.TPaveText(0.35, 0.90-(i+1)*(0.905-0.105)/nlines+0.5*(0.905-0.105)/nlines, 0.49, 0.90+0.01-(i+1)*(0.905-0.105)/nlines+0.5*(0.905-0.105)/nlines, "NDC"))
      result[i].SetBorderSize(   0 )
      result[i].SetFillStyle(    0 )
      result[i].SetTextAlign(   12 )
      result[i].SetTextSize ( 0.02 )
      if args.type=="stage0":
         result[i].SetTextSize ( 0.04 )
      result[i].SetTextColor(    1 )
      result[i].SetTextFont (   42 )
      result[i].AddText(myresult)
      if ii>0:
         result[i].Draw("same")

      i += 1
      y_pos -= 1.
    ii+=1

gr.Draw('P')

theory_band = ROOT.TBox(combineMu-lowBnad,0,combineMu+highBand,nlines-0.1)
theory_band.SetFillColor(ROOT.kYellow)
theory_band.Draw('same')

l=ROOT.TLine(combineMu,0,combineMu,nlines)
l.SetLineColor(ROOT.kOrange)
l.Draw('sameL')

gr.Draw('SAMEP')

lumi1=add_lumi(args.year)
lumi2=add_CMS()
lumi3=add_channel(args.channel)
lumi1.Draw("same")
lumi2.Draw("same")
lumi3.Draw("same")

#legend = ROOT.TLegend(0.18, 0.13, 0.45, 0.22, '', 'NBNDC')
#legend.Draw()


# Go back and tidy up the axes and frame
canv.cd()
#canv.GetFrame().Draw("same")
canv.RedrawAxis()

# ... and we're done
canv.Print('.png')
canv.Print('.pdf')

