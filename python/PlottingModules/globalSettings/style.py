import ROOT

tdrStyle = ROOT.TStyle('tdrStyle','Style for P-TDR')

def tdrGrid(gridOn):
    tdrStyle.SetPadGridX(gridOn)
    tdrStyle.SetPadGridY(gridOn)

def fixOverlay():
    ROOT>gPad.RedrawAxis()

def setTDRStyle():
    #Canvas Settings
    tdrStyle.SetCanvasBorderMode(0)
    tdrStyle.SetCanvasDefH(600)
    tdrStyle.SetCanvasDefW(600)
    tdrStyle.SetCanvasDefX(0)
    tdrStyle.SetCanvasDefY(0)

    #Pad Settings
    tdrStyle.SetPadBorderMode(0)
    
    tdrStyle.SetPadColor(ROOT.kWhite)
    tdrStyle.SetPadGridX(False)
    tdrStyle.SetPadGridY(False)
    tdrStyle.SetGridColor(0)
    tdrStlye.SetGridStyle(3)
    tdrStyle.SetGridWidth(1)

    #Frame Settings
    tdrStyle.SetFrameBorderMode(0)
    tdrStyle.SetFrameBorderSize(1)
    tdrStyle.SetFrameFillColor(0)
    tdrStyle.SetFrameFillStyle(0)
    tdrStyle.SetFrameLineColor(1)
    tdrStyle.SetFrameLineStyle(1)
    tdrStyle.SetFrameLineWidth(1)

    #Histogram Settings
    tdrStyle.SetHistLineColor(1)
    tdrStyle.SetHistLineStyle(0)
    tdrStyle.SetHistLineWidth(1)

    tdrStyle.SetEndErrorSize(2)

    tdrStyle.SetMarkerStyle(20)

    #Fit Settings
    tdrStyle.SetOptFit(1)
    tdrStyle.SetFitFormat("5.4g")
    tdrStyle.SetFuncColor(2)
    tdrStyle.SetFuncStyle(1)
    tdrStyle.SetFuncWidth(1)

    #For the date:
    tdrStyle.SetOptDate(0)

    #For the statistics box:
    tdrStyle.SetOptFile(0)
    tdrStyle.SetOptStat(0) # To display the mean and RMS:   SetOptStat("mr")
    tdrStyle.SetStatColor(kWhite)
    tdrStyle.SetStatFont(42)
    tdrStyle.SetStatFontSize(0.025)
    tdrStyle.SetStatTextColor(1)
    tdrStyle.SetStatFormat("6.4g")
    tdrStyle.SetStatBorderSize(1)
    tdrStyle.SetStatH(0.1)
    tdrStyle.SetStatW(0.15)

    # Margins:
    tdrStyle.SetPadTopMargin(0.05)
    tdrStyle.SetPadBottomMargin(0.13)
    tdrStyle.SetPadLeftMargin(0.16)
    tdrStyle.SetPadRightMargin(0.02)

    # For the Global title:
    tdrStyle.SetOptTitle(0)
    tdrStyle.SetTitleFont(42)
    tdrStyle.SetTitleColor(1)
    tdrStyle.SetTitleTextColor(1)
    tdrStyle.SetTitleFillColor(10)
    tdrStyle.SetTitleFontSize(0.05)
    # tdrStyle.SetTitleH(0) # Set the height of the title box
    # tdrStyle.SetTitleW(0) # Set the width of the title box
    # tdrStyle.SetTitleX(0) # Set the position of the title box
    # tdrStyle.SetTitleY(0.985) # Set the position of the title box
    # tdrStyle.SetTitleStyle(Style_t style = 1001)
    # tdrStyle.SetTitleBorderSize(2)

    # For the axis titles:
    
    tdrStyle.SetTitleColor(1, "XYZ")
    tdrStyle.SetTitleFont(42, "XYZ")
    tdrStyle.SetTitleSize(0.06, "XYZ")
    # tdrStyle.SetTitleXSize(Float_t size = 0.02) # Another way to set the size?
    # tdrStyle.SetTitleYSize(Float_t size = 0.02)
    tdrStyle.SetTitleXOffset(0.9)
    tdrStyle.SetTitleYOffset(1.25)
    # tdrStyle.SetTitleOffset(1.1, "Y") # Another way to set the Offset
    
    # For the axis labels:
    
    tdrStyle.SetLabelColor(1, "XYZ")
    tdrStyle.SetLabelFont(42, "XYZ")
    tdrStyle.SetLabelOffset(0.007, "XYZ")
    tdrStyle.SetLabelSize(0.05, "XYZ")
    
    # For the axis:
    
    tdrStyle.SetAxisColor(1, "XYZ")
    tdrStyle.SetStripDecimals(kTRUE)
    tdrStyle.SetTickLength(0.03, "XYZ")
    tdrStyle.SetNdivisions(510, "XYZ")
    tdrStyle.SetPadTickX(1)  # To get tick marks on the opposite side of the frame
    tdrStyle.SetPadTickY(1)
    
    # Change for log plots:
    tdrStyle.SetOptLogx(0)
    tdrStyle.SetOptLogy(0)
    tdrStyle.SetOptLogz(0)
    
    # Postscript options:
    tdrStyle.SetPaperSize(20.,20.)
