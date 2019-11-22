import ROOT

def SetupPad(thePad):
    thePad.SetTickx()
    thePad.SetTicky()
    #thePad.SetGridx()
    thePad.SetLogy()

def CreatePads(theCanvas):
    theCanvas.Divide(1,2)
    #PlotPad = ROOT.TPad("PlotPad","PlotPad",0.,0.20,1.,1.)
    plotPad = theCanvas.GetPrimitive(theCanvas.GetName()+'_1')
    plotPad.SetPad(0.,0.2,1.,1.)
    #RatioPad = ROOT.TPad("RatioPad","RatioPad",0.,0.,1.,0.25)    
    ratioPad = theCanvas.GetPrimitive(theCanvas.GetName()+'_2')
    ratioPad.SetPad(0.,0.,1.,0.25)

    return plotPad,ratioPad
