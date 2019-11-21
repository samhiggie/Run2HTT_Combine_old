import ROOT
from array import array

#quick utility function to make a TH1 Stack out of histograms in a dictionary.
def StackDictionary(histogramDictionary):
    theStack = ROOT.THStack("Predictions","Predictions")
    for entry in histogramDictionary:
        theStack.Add(histogramDictionary[entry],"HIST")
    return theStack

#quick utility function for making a histogram that has the errors of a stack
#some of these settings should probably be offloaded to other modules.
def MakeStackErrors(TheStack):
    nBins,BinBoundaries = GetHistogramAxisInfo(TheStack.GetHists().At(0))    
    BinBoundaryArray = array('f',BinBoundaries)
    DenominatorHistos = ROOT.TH1F("DenominatorHistos","DenominatorHistos",
                                  nBins,
                                  BinBoundaryArray)
    for i in range(TheStack.GetNhists()):        
        newNBins,newBinBoundaries = GetHistogramAxisInfo(TheStack.GetHists().At(i))
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

def GetHistogramAxisInfo(TheHistogram):
    BinBoundaries = []
    for i in range(1,TheHistogram.GetNbinsX()+1):
        BinBoundaries.append(TheHistogram.GetBinLowEdge(i))
    BinBoundaries.append(TheHistogram.GetXaxis().GetXmax())
    Nbins = len(BinBoundaries)-1
    return Nbins,BinBoundaries
