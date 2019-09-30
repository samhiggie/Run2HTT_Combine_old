import ROOT
import argparse
import re
from array import array
import math

def MakeRatioPlot(TheCanvas,TheStack,TheData,XAxisLabel,YBoundDown,YBoundUp):
    PlotPad = ROOT.TPad("pad1","plot",0.,0.20,1.,1.)
    PlotPad.Draw()
    RatioPad = ROOT.TPad("pad2","ratio",0.,0.,1.,0.25)
    RatioPad.Draw()

    PlotPad.cd()
    RatioPad.SetTopMargin(0.0)
    RatioPad.SetBottomMargin(0.08)
    RatioPad.SetGridy()

    nBins,BinBoundaries = GetHistogramAxisInfo(TheData)
    BinBoundaryArray=array('f',BinBoundaries)

    RatioHist = ROOT.TH1F("Ratio","",
                          nBins,
                          BinBoundaryArray)
    RatioHist.Sumw2()
    RatioHist.Add(TheData)

    DenominatorHistos = ROOT.TH1F("DenominatorHistos","DenominatorHistos",
                                  nBins,
                                  BinBoundaryArray)
    
    ListOfStackHistograms = TheStack.GetHists()
    for i in range(TheStack.GetNhists()):
        DenominatorHistos.Add(TheStack.GetHists().At(i))
    RatioHist.Divide(DenominatorHistos)
    FinalRatioHist = ROOT.TH1F("FinalRatio","",
                               nBins,
                               BinBoundaryArray)

    for i in range(1,FinalRatioHist.GetNbinsX()+1):
        FinalRatioHist.SetBinContent(i,RatioHist.GetBinContent(i))
        try:
            FinalRatioHist.SetBinError(i,(TheData.GetBinError(i)/TheData.GetBinContent(i))*RatioHist.GetBinContent(i))
        except ZeroDivisionError:
            #print("Division By zero in ratio bin errors.")
            #print("Setting bin: "+str(i)+" to zero")
            FinalRatioHist.SetBinError(i,0)
    
    FinalRatioHist.SetMarkerStyle(20)
    
    FinalRatioHist.GetYaxis().SetTitle("Data/Predicted")
    FinalRatioHist.GetYaxis().SetTitleSize(0.1)
    FinalRatioHist.GetYaxis().SetTitleOffset(0.32)
    FinalRatioHist.GetYaxis().CenterTitle()
    FinalRatioHist.GetYaxis().SetLabelSize(0.10)
    FinalRatioHist.GetYaxis().SetNdivisions(6,0,0)
    FinalRatioHist.GetYaxis().SetRangeUser(YBoundDown*0.95,YBoundUp*1.05)

    FinalRatioHist.GetXaxis().SetLabelSize(0.10)
    
    FinalRatioHist.GetXaxis().SetTitle(XAxisLabel)
    FinalRatioHist.GetXaxis().SetTitleSize(0.14)

    MCErrors = ROOT.TH1F("MCErrors","MCErrors",
                         nBins,
                         BinBoundaryArray)
    for i in range (1,MCErrors.GetNbinsX()+1):
        MCErrors.SetBinContent(i,1.0)
        try:
            MCErrors.SetBinError(i,DenominatorHistos.GetBinError(i)/DenominatorHistos.GetBinContent(i))
        except:
            #print("No background predicted in ratio plot errors for bin: "+str(i))
            #print("Setting it to zero")
            MCErrors.SetBinError(i,0)

    MCErrors.SetFillStyle(3001)
    MCErrors.SetFillColor(15)    

    #RatioPad.cd()
    #FinalRatioHist.Draw("ex0")
    #MCErrors.Draw("SAME e2")
    #FinalRatioHist.Draw("SAME ex0")    
    #RatioPad.Draw()
    #PlotPad.cd()

    #RatioPad.ls()
    #FinalRatioHist.Print()
    #MCErrors.Print()
    #raw_input("Done Drawing Ratio. Press Enter...")

    return PlotPad,RatioPad,FinalRatioHist,MCErrors

def MakeStackErrors(TheStack):
    nBins,BinBoundaries = GetHistogramAxisInfo(TheStack.GetHists().At(0))
    BinBoundaryArray = array('f',BinBoundaries)
    DenominatorHistos = ROOT.TH1F("DenominatorHistos","DenominatorHistos",
                                  nBins,
                                  BinBoundaryArray)
    for i in range(TheStack.GetNhists()):
        DenominatorHistos.Add(TheStack.GetHists().At(i))
    TheErrorHisto = ROOT.TH1F("TheErrorHisto","",
                              nBins,
                              BinBoundaryArray)

    for i in range(1,DenominatorHistos.GetNbinsX()+1):
        TheErrorHisto.SetBinContent(i,DenominatorHistos.GetBinContent(i))
        TheErrorHisto.SetBinError(i,DenominatorHistos.GetBinError(i))
    TheErrorHisto.SetLineColor(0)
    TheErrorHisto.SetLineWidth(0)
    TheErrorHisto.SetMarkerSize(0)
    TheErrorHisto.SetFillStyle(3001)
    TheErrorHisto.SetFillColor(15)
    return TheErrorHisto

#verification function that dumps all histograms to a drawn canvas
def DumpContentsToScreen(NominalHistograms,AllHistograms):
    ROOT.gStyle.SetOptStat(0)

    TheCanvas = ROOT.TCanvas("TheCanvas","TheCanvas")

    HistogramDictionary= {}
    for Histogram in NominalHistograms:
        HistogramDictionary[Histogram.GetName()]=Histogram.Clone()
    for Histogram in AllHistograms:
        if Histogram.GetName()=="data_obs":
            HistogramDictionary["data_obs"]=Histogram.Clone()
    TT=HistogramDictionary["TTL"].Clone()
    TT.Add(HistogramDictionary["TTT"])
    TT.SetNameTitle("TT","TT")
    HistogramDictionary["TT"]=TT
    Other=HistogramDictionary["VVT"].Clone()
    Other.Add(HistogramDictionary["VVL"])
    Other.Add(HistogramDictionary["qqH_htt125"])
    Other.Add(HistogramDictionary["ggH_htt125"])
    Other.Add(HistogramDictionary["WH_htt125"])
    Other.Add(HistogramDictionary["ZH_htt125"])
    Other.SetNameTitle("Other","Other")
    HistogramDictionary["Other"]=Other
    HiggsUpscale = HistogramDictionary["qqH_htt125"].Clone()
    HiggsUpscale.Add(HistogramDictionary["ggH_htt125"])
    HiggsUpscale.Add(HistogramDictionary["WH_htt125"])
    HiggsUpscale.Add(HistogramDictionary["ZH_htt125"])
    Signal = HiggsUpscale.Clone()
    HiggsUpscale.Scale(30.0)
    HistogramDictionary["HiggsUpscale"]=HiggsUpscale
    
    HistogramDictionary["data_obs"].SetMarkerStyle(20)
    HistogramDictionary["jetFakes"].SetFillColor(ROOT.TColor.GetColor("#ffccff"))
    HistogramDictionary["ZT"].SetFillColor(ROOT.TColor.GetColor("#ffcc66"))
    HistogramDictionary["ZL"].SetFillColor(ROOT.TColor.GetColor("#ffccff"))
    HistogramDictionary["TT"].SetFillColor(ROOT.TColor.GetColor("#9999cc"))
    HistogramDictionary["Other"].SetFillColor(ROOT.TColor.GetColor("#12cadd"))
    HistogramDictionary["HiggsUpscale"].SetLineColor(ROOT.kRed)
    HistogramDictionary["HiggsUpscale"].SetLineWidth(2)

    #blind ourselves
    for i in range(1,HistogramDictionary["data_obs"].GetNbinsX()+1):
        SignalContribution = Signal.GetBinContent(i)
        NonHiggsOtherContribution = HistogramDictionary["Other"].GetBinContent(i)-SignalContribution
        TotalBackgroundContribution = NonHiggsOtherContribution+HistogramDictionary["jetFakes"].GetBinContent(i)+ HistogramDictionary["ZT"].GetBinContent(i)+HistogramDictionary["ZL"].GetBinContent(i)+HistogramDictionary["TT"].GetBinContent(i)
        try:
            if SignalContribution/math.sqrt(TotalBackgroundContribution) > 0.5:
                HistogramDictionary["data_obs"].SetBinContent(i,-1.0)
        except ZeroDivisionError:
            print("No background contribution predicted in bin: "+str(i))
            print("Not blinding this bin???")
        except ValueError:
            print("Negative Background in this bin.")
            print("Not blinding this bin.")
    BackgroundStack = ROOT.THStack("BackgroundStack","BackgroundStack")
    BackgroundStack.Add(HistogramDictionary["Other"],"HIST")
    BackgroundStack.Add(HistogramDictionary["TT"],"HIST")
    BackgroundStack.Add(HistogramDictionary["ZL"],"HIST")
    BackgroundStack.Add(HistogramDictionary["jetFakes"],"HIST")
    BackgroundStack.Add(HistogramDictionary["ZT"],"HIST")

    TheErrors = MakeStackErrors(BackgroundStack)

    ThePlotPad,TheRatioPad,TheRatioHist,TheRatioErrors = MakeRatioPlot(TheCanvas,BackgroundStack,HistogramDictionary["data_obs"],"mass bin",0.7,1.3)

    TheRatioPad.cd()
    TheRatioHist.Draw("ex0")
    TheRatioErrors.Draw("SAME e2")
    TheRatioHist.Draw("SAME ex0")
    TheRatioPad.Draw()

    ThePlotPad.cd()
    ThePlotPad.SetTickx()
    ThePlotPad.SetTicky()
    ThePlotPad.SetGridx()
    ThePlotPad.SetLogy()
    
    #RatioPad = TheCanvas.FindObject("pad2")
    #RatioPad.ls()
    #RatioHist = RatioPad.FindObject("FinalRatio")
    #RatioHist.Print()

    BackgroundStack.SetMaximum(max(BackgroundStack.GetMaximum(),HistogramDictionary["data_obs"].GetMaximum())*1.1)
    BackgroundStack.SetMinimum(1.0)

    BackgroundStack.Draw()
    TheErrors.Draw("SAME e2")
    BackgroundStack.SetTitle(TheDirectory.GetName())
    HistogramDictionary["data_obs"].Draw("SAME e1")
    HistogramDictionary["HiggsUpscale"].Draw("SAME HIST")
    BackgroundStack.GetYaxis().SetTitle("Events")
    BackgroundStack.GetYaxis().SetTitleOffset(1.58)
    BackgroundStack.GetXaxis().SetLabelSize(0.0)

    TheLegend = ROOT.TLegend(0.9,0.6,1.0,0.9)
    TheLegend.AddEntry(HistogramDictionary["data_obs"],"Observed","pe")
    TheLegend.AddEntry(HistogramDictionary["ZT"],"DY #rightarrow #tau#tau","f")
    TheLegend.AddEntry(HistogramDictionary["Other"],"Other","f")
    TheLegend.AddEntry(HistogramDictionary["ZL"],"DY #rightarrow ll","f")
    TheLegend.AddEntry(HistogramDictionary["TT"],"t#bar{t}","f")
    TheLegend.AddEntry(HistogramDictionary["jetFakes"],"Fakes","f")
    TheLegend.AddEntry(HistogramDictionary["HiggsUpscale"],"All Higgs (#times 30)","l")
    TheLegend.Draw()

    TheCanvas.Draw()

    #create grid divisions
    numCategories = int((BackgroundStack.GetHistogram().GetXaxis().GetXmax()-BackgroundStack.GetHistogram().GetXaxis().GetXmin()))/11
    BackgroundStack.GetXaxis().SetNdivisions(-500-numCategories)

    lumiText="?"

    latex = ROOT.TLatex()
    latex.SetNDC()
    latex.SetTextAngle(0)
    latex.SetTextColor(ROOT.kBlack)
    latex.SetTextFont(42)
    latex.SetTextAlign(31)
    latex.SetTextSize(0.6*ThePlotPad.GetTopMargin())
    latex.DrawLatex(1.0-ThePlotPad.GetRightMargin(),1.01-ThePlotPad.GetTopMargin(),lumiText)

    latex.SetTextFont(61)
    latex.SetTextSize(0.75*ThePlotPad.GetTopMargin())
    latex.DrawLatex(0.18,1.01-ThePlotPad.GetTopMargin(),"CMS")

    latex.SetTextFont(52)
    latex.SetTextSize(0.76*0.75*ThePlotPad.GetTopMargin())
    latex.DrawLatex(0.33,1.01-ThePlotPad.GetTopMargin(),"Preliminary")

    ThePlotPad.Draw()

    #NominalErrorHisto = GetErrors(NominalHistograms)
    #AnotherCanvas = ROOT.TCanvas("AnotherCanvas")
    #NominalErrorHisto.SetMaximum(1.3)
    #NominalErrorHisto.SetMinimum(0.7)
    #NominalErrorHisto.SetFillStyle(3001)
    #NominalErrorHisto.SetFillColor(15)
    #NominalErrorHisto.Draw("e2")

    raw_input("Press Enter to Continue...")

#here's another of the magic functions, 
#this actually creates the new histograms with the merged bins
def MergeBin(FirstBin,SecondBin,NominalHistos,AllHistos):
    if FirstBin > SecondBin:
        FirstBin,SecondBin = SecondBin,FirstBin
    BinBoundaryToRemove = FirstBin #The boundary number is equivalent to the bin number of the smallest bin
    nBins,BinBoundaries = GetHistogramAxisInfo(NominalHistos[0])
    BinBoundaries.pop(BinBoundaryToRemove)
    nBins-=1
    BinBoundaryArray = array('f',BinBoundaries)
    #go through and create new histograms with the merged bins present
    #print("Merging Nominal Bins")
    for i in range(len(NominalHistos)):
        NewName = NominalHistos[i].GetName()
        NewTitle = NominalHistos[i].GetTitle()
        NewHisto = ROOT.TH1F("Temp",
                             "Temp",
                             nBins,
                             BinBoundaryArray)
        for j in range(1,NominalHistos[i].GetNbinsX()+1):#This needs to be the full range of the histogram
            #print("Filling bin: "+str(j))
            if j < FirstBin:
                #print("j<FirstBin, Content: "+str(NominalHistos[i].GetBinContent(j)))
                NewHisto.SetBinContent(j,NominalHistos[i].GetBinContent(j))
                NewHisto.SetBinError(j,NominalHistos[i].GetBinError(j))
            elif j == FirstBin:                
                #print("j=FirstBin, Content: "+str(NominalHistos[i].GetBinContent(j)+NominalHistos[i].GetBinContent(j+1)))
                NewHisto.SetBinContent(j,NominalHistos[i].GetBinContent(j)+NominalHistos[i].GetBinContent(j+1))#j+1 SHOULD be equivalent to second bin
                NewHisto.SetBinError(j,math.sqrt(NominalHistos[i].GetBinError(j)*NominalHistos[i].GetBinError(j)+NominalHistos[i].GetBinError(j+1)*NominalHistos[i].GetBinError(j+1)))#j+1 again SHOULD be equivalent to second bin
            elif j > FirstBin:
                #print("j>FirstBin, Content: "+str(NominalHistos[i].GetBinContent(j+1)))
                NewHisto.SetBinContent(j,NominalHistos[i].GetBinContent(j+1))
                NewHisto.SetBinError(j,NominalHistos[i].GetBinError(j+1))
        NominalHistos[i]=NewHisto
        NominalHistos[i].SetNameTitle(NewName,NewTitle)
    #print("Merging All Histograms")
    for i in range(len(AllHistos)):
        NewName = AllHistos[i].GetName()
        NewTitle = AllHistos[i].GetTitle()
        NewHisto = ROOT.TH1F("Temp",
                             "Temp",
                             nBins,
                             BinBoundaryArray)
        for j in range(1,AllHistos[i].GetNbinsX()+1): #this needs to be the full range of the histogram
            #print("Filling bin: "+str(j))
            if j < FirstBin:
                #print("j<FirstBin, Content: "+str(AllHistos[i].GetBinContent(j)))
                NewHisto.SetBinContent(j,AllHistos[i].GetBinContent(j))
                NewHisto.SetBinError(j,AllHistos[i].GetBinError(j))
            elif j == FirstBin:                
                #print("MergeBin error: "+str(math.sqrt(AllHistos[i].GetBinError(j)*AllHistos[i].GetBinError(j)+AllHistos[i].GetBinError(j+1)*AllHistos[i].GetBinError(j+1))))
                #print("j=FirstBin, Content: "+str(AllHistos[i].GetBinContent(j)+AllHistos[i].GetBinContent(j+1)))
                NewHisto.SetBinContent(j,AllHistos[i].GetBinContent(j)+AllHistos[i].GetBinContent(j+1))#j+1 SHOULD be equivalent to second bin
                NewHisto.SetBinError(j,math.sqrt(AllHistos[i].GetBinError(j)*AllHistos[i].GetBinError(j)+AllHistos[i].GetBinError(j+1)*AllHistos[i].GetBinError(j+1)))#j+1 again SHOULD be equivalent to second bin
            elif j > FirstBin:
                #print("j>FirstBin, Content: "+str(AllHistos[i].GetBinContent(j+1)))
                NewHisto.SetBinContent(j,AllHistos[i].GetBinContent(j+1))
                NewHisto.SetBinError(j,AllHistos[i].GetBinError(j+1))
        AllHistos[i]=NewHisto
        AllHistos[i].SetNameTitle(NewName,NewTitle)

def GetFirstBinNeedingMerge(StartBin,StopBin,ErrorHisto,NominalHistos):
    for i in range(StartBin,StopBin+1):
        if ErrorHisto.GetBinError(i) >= 0.30:
            print("Error: "+str(ErrorHisto.GetBinError(i)))
            return i
    return -1

#okay, here's a brief function to describe whether the bin we've selected is 
#a mergeable bin. Currently unused but planned for upgrade.
def IsMergeableBin(BinNum,StartBin,StopBin,ErrorHisto,NominalHistos):
    #if the bin we've selected is the Overflow bin, it is not mergeable.
    if BinNum == StopBin:
        return False
    #if the bin has S/root(B) > 0.1, it is not mergeable
    Signal = 0.0
    Background = 0.0
    for Histogram in NominalHistos:
        if re.search("ggH|qqH|ZH|WH",Histogram.GetName()):
            Signal+=Histogram.GetBinContent(BinNum)
        else:
            Background+=Histogram.GetBinContent(BinNum)
    if Signal/math.sqrt(Background) >= 0.1:
        return False
    #if we have an error on the prediction greater than 30% we 
    #have a potentially mergeable bin.
    elif ErrorHisto.GetBinError(BinNum) > 0.3:                        
        return True
    return False
#Okay, here's one of the magic functions
#examine the errors inside slice
#if we find a bin that has more than 30% error in the bin
#then for each histogram we have, we take that bin
#and we merge it into the bin beside it that has the least stats (no merging across slices)
#then we call the function on this slice again
#if we have only one bin, or there is nothing to merge, we simply stop merging bins
def MergeSlice(StartBin,StopBin,NominalHistos,AllHistos):
    #if we only have one bin in the slice, we're done. No more merging to be done here
    #print("Slice span: "+str(StartBin)+","+str(StopBin))
    if StopBin-StartBin == 0:
        print("Only one bin left, nothing to merge.")
        return
    Errors = GetErrors(NominalHistos)
    AddedHistos = GetNominalStack(NominalHistos)
    BinToMerge = GetFirstBinNeedingMerge(StartBin,StopBin,Errors,NominalHistos)
    #print("Merge Bin: "+str(BinToMerge))
    if(BinToMerge == StartBin):
        print("Merging first bin in slice right")
        MergeBin(BinToMerge,BinToMerge+1,NominalHistos,AllHistos)
        #DumpContentsToScreen(NominalHistos,AllHistos)
        MergeSlice(StartBin,StopBin-1,NominalHistos,AllHistos)
    elif(BinToMerge == StopBin):
        print("Merging last bin in slice left")
        MergeBin(BinToMerge,BinToMerge-1,NominalHistos,AllHistos)
        #DumpContentsToScreen(NominalHistos,AllHistos)
        MergeSlice(StartBin,StopBin-1,NominalHistos,AllHistos)
    elif(BinToMerge > 0):
        #print("Performing merge of middle bin")
        if AddedHistos.GetBinContent(BinToMerge-1) < AddedHistos.GetBinContent(BinToMerge+1): #fewer stats to the left
            print("Merging bin #"+str(BinToMerge)+" left")
            MergeBin(BinToMerge,BinToMerge-1,NominalHistos,AllHistos)
            #DumpContentsToScreen(NominalHistos,AllHistos)
        elif AddedHistos.GetBinContent(BinToMerge-1) >= AddedHistos.GetBinContent(BinToMerge+1):
            print("Merging bin #"+str(BinToMerge)+" right")
            MergeBin(BinToMerge,BinToMerge+1,NominalHistos,AllHistos)
            #DumpContentsToScreen(NominalHistos,AllHistos)
        MergeSlice(StartBin,StopBin-1,NominalHistos,AllHistos)
    else: #there are no bins in need of merging. We're done here
        print("No bins in need of merge.")
        return

#function to split the histograms up into compnent slices, then call the merging function on each 
#in right to left order!
def DivideSlicesForMerging(NominalBinsPerSlice,NominalHistograms,AllHistograms):
    NumberOfSlices = NominalHistograms[0].GetNbinsX()/NominalBinsPerSlice
    for i in range(NumberOfSlices):
        print("Merging slice #"+str(i+1))
        StartOfSlice = (NumberOfSlices-i-1)*NominalBinsPerSlice+1
        EndOfSlice = (NumberOfSlices-i)*NominalBinsPerSlice
        MergeSlice(StartOfSlice,EndOfSlice,NominalHistograms,AllHistograms)
        #DumpContentsToScreen(NominalHistograms,AllHistograms)
    DumpContentsToScreen(NominalHistograms,AllHistograms)

#helper function to get the bin boundaries and number of bins from a histogram
def GetHistogramAxisInfo(TheHistogram):
    BinBoundaries = []
    for i in range(1,TheHistogram.GetNbinsX()+1):
        BinBoundaries.append(TheHistogram.GetBinLowEdge(i))
    BinBoundaries.append(TheHistogram.GetXaxis().GetXmax())
    Nbins = len(BinBoundaries)-1
    return Nbins,BinBoundaries

def GetNominalStack(NominalHistograms):
    Nbins,BinBoundaries=GetHistogramAxisInfo(NominalHistograms[0])
    BinBoundaryArray= array('f',BinBoundaries)
    MCHistos = ROOT.TH1F("MCHistos","MCHistos",
                         Nbins,
                         BinBoundaryArray)
    for Histogram in NominalHistograms:
        MCHistos.Add(Histogram)
    return MCHistos

#function to generate the error ratio as seen in a ratio plot
def GetErrors(NominalHistograms):
    #we need to create an array with the bin edges
    Nbins,BinBoundaries=GetHistogramAxisInfo(NominalHistograms[0])    
    BinBoundaryArray= array('f',BinBoundaries)
    MCHistos = GetNominalStack(NominalHistograms)
    MCErrors = ROOT.TH1F("MCErrors","MCErrors",
                         Nbins,
                         BinBoundaryArray)
    for i in range(1,NominalHistograms[0].GetNbinsX()+1):
        #print("Filling bin "+str(i))
        #print("Abs error "+str(MCHistos.GetBinError(i)))
        #print("BinContent "+str(MCHistos.GetBinContent(i)))
        #gprint("Error "+str(MCHistos.GetBinError(i)/MCHistos.GetBinContent(i)))
        MCErrors.SetBinContent(i,1.0)
        MCErrors.SetBinError(i,MCHistos.GetBinError(i)/MCHistos.GetBinContent(i))
    return MCErrors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for merging low stats bins together.")
    parser.add_argument("FileIn",help="File to merge bins in")
    parser.add_argument("--BinsPerSlice",type=int,nargs="?",help="# of bins in a slice",required=True)
    parser.add_argument("--OutputFile",nargs="?",help="Name of the output file",default="MergedFile.root")

    args = parser.parse_args()
    
    TheFile = ROOT.TFile(args.FileIn)
    NewFile = ROOT.TFile(args.OutputFile,"RECREATE")

    for i in range(TheFile.GetListOfKeys().GetEntries()):
        TheDirectory = TheFile.Get(TheFile.GetListOfKeys().At(i).GetName())
        print(TheDirectory.GetName())
        NewFileDir = NewFile.mkdir(TheDirectory.GetName())
        NewFileDir.cd()
        NominalList = []
        HistogramList = []
        for j in range(TheDirectory.GetListOfKeys().GetEntries()):
            HistogramList.append(TheDirectory.Get(TheDirectory.GetListOfKeys().At(j).GetName()).Clone())
            NominalMatch = re.search("(ggH_htt125|qqH_htt125|^(?!ggH)(?!qqH)(?!data).+)$(?<!Up)(?<!Down)",TheDirectory.GetListOfKeys().At(j).GetName())
            if NominalMatch:                
                NominalList.append(TheDirectory.Get(TheDirectory.GetListOfKeys().At(j).GetName()).Clone())
        DumpContentsToScreen(NominalList,HistogramList)
        DivideSlicesForMerging(args.BinsPerSlice,NominalList,HistogramList)
        NewFileDir.cd()
        for Histogram in HistogramList:
            Histogram.Write()
    NewFile.Write()
    NewFile.Close()
        
        
        
                
            
        
    
