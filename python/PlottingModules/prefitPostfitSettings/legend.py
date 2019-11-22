import ROOT

legendPosition = (0.7,0.82,0.95,0.97)
histogramEntries = {
    'jetFakes':'Jet Fakes',
    'ZT':'Z #rightarrow #tau#tau',
    'ZL':'Z #rightarrow #ell #ell',
    'Top':'t#bar{t}',
    'Other':'Others',
    'Higgs':'Higgs Signal (#times 20)',
    'data_obs':'Data',
    'background_error':'Prediction uncertainty',
    }
histogramFormats = {
    'jetFakes':'f',
    'ZT':'f',
    'ZL':'f',
    'Top':'f',
    'Other':'f',
    'Higgs':'l',
    'data_obs':'pe',
    'background_error':'f',
    }

def CreateLegend(histogramDictionary):
    theLegend = ROOT.TLegend(legendPosition[0],legendPosition[1],legendPosition[2],legendPosition[3])
    
    theLegend.SetNColumns(2)

    for entry in histogramDictionary:
        AppendToLegend(theLegend,histogramDictionary[entry],entry)
    return theLegend

def AppendToLegend(theLegend,histogram,entry):
    try:
        theLegend.AddEntry(histogram,histogramEntries[entry],histogramFormats[entry])
    except KeyError:
        print("Failed to properly make entry for: "+str(entry))
