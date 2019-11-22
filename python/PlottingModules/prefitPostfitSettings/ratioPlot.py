import ROOT
from .. import Utilities
from array import array

YBounds = (0.7,1.3)

ratioMarkerStyle = 20
ratioYAxisTitle = 'Data/Predicted'
ratioYAxisTitleSize = 0.1
ratioYAxisTitleOffset = 0.22
ratioYAxisLabelSize = 0.10
ratioYAxisNDivisions = (6,0,0)

errorFillStyle = 3001
errorFillColor = 15

def MakeRatioPlot(theStack,theData):
    nBins,binBoundaries = Utilities.GetHistogramAxisInfo(theData)
    binBoundaryArray = array('f',binBoundaries)

    ratioHist = ROOT.TH1F('Ratio',
                          'Ratio',
                          nBins,
                          binBoundaryArray)

    ratioHist.Sumw2()
    ratioHist.Add(theData)

    denominatorHistos = ROOT.TH1F('denominatorHistos',
                                  'denominatorHistos',
                                  nBins,
                                  binBoundaryArray)
    listOfStackHistograms = theStack.GetHists()
    for i in range(theStack.GetNhists()):
        denominatorHistos.Add(theStack.GetHists().At(i))
    ratioHist.Divide(denominatorHistos)
    for i in range(1,ratioHist.GetNbinsX()+1):
        try:
            ratioHist.SetBinError(i,(theData.GetBinError(i)/theData.GetBinContent(i))*ratioHist.GetBinContent(i))
        except ZeroDivisionError:
            ratioHist.SetBinError(i,0)
        

    ratioHist.SetMarkerStyle(ratioMarkerStyle)
    
    ratioHist.GetYaxis().SetTitle(ratioYAxisTitle)
    ratioHist.GetYaxis().SetTitleSize(ratioYAxisTitleSize)
    ratioHist.GetYaxis().SetTitleOffset(ratioYAxisTitleOffset)
    ratioHist.GetYaxis().CenterTitle()
    ratioHist.GetYaxis().SetLabelSize(ratioYAxisLabelSize)
    ratioHist.GetYaxis().SetNdivisions(ratioYAxisNDivisions[0],
                                       ratioYAxisNDivisions[1],
                                       ratioYAxisNDivisions[2])
    ratioHist.GetYaxis().SetRangeUser(YBounds[0],YBounds[1])

    MCErrors = ROOT.TH1F("MCErrors","MCErrors",
                         nBins,
                         binBoundaryArray)
    for i in range (1,MCErrors.GetNbinsX()+1):
        MCErrors.SetBinContent(i,1.0)
        try:
            MCErrors.SetBinError(i,denominatorHistos.GetBinError(i)/denominatorHistos.GetBinContent(i))
        except:
            MCErrors.SetBinError(i,0)
    MCErrors.SetFillStyle(errorFillStyle)
    MCErrors.SetFillColor(errorFillColor)
    MCErrors.SetMarkerStyle(1)

    return ratioHist,MCErrors
