import ROOT

lumiTextColor = ROOT.kBlack
lumiTextFont = 42
lumiTextAlignment = 31
lumiTextSize = 0.04
lumiTextPosition = (0.415,0.96)
lumi2016Text = '#sqrt{S}=13 TeV, 35.9 fb^{-1}'
lumi2017Text = '#sqrt{S}=13 TeV, 41.5 fb^{-1}'
lumi2018Text = '#sqrt{S}=13 TeV, 59.7 fb^{-1}'
lumiRun2Text = '#sqrt{S}=13 TeV, 137.1 fb^{-1}'

def CreateLumiText(year):
    lumiText = ROOT.TLatex()
    lumiText.SetNDC()
    lumiText.SetTextColor(lumiTextColor)
    lumiText.SetTextFont(lumiTextFont)
    lumiText.SetTextAlign(lumiTextAlignment)
    lumiText.SetTextSize(lumiTextSize)
    if year == '2016':
        lumiText.DrawLatex(lumiTextPosition[0],lumiTextPosition[1],lumi2016Text)
    elif year == '2017':
        lumiText.DrawLatex(lumiTextPosition[0],lumiTextPosition[1],lumi2017Text)
    elif year == '2018':
        lumiText.DrawLatex(lumiTextPosition[0],lumiTextPosition[1],lumi2018Text)
    elif year == 'Run2':
        lumiText.DrawLatex(lumiTextPosition[0],lumiTextPosition[1],lumiRun2Text)
    
