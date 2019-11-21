import ROOT

legendPosition = (0.8,0.6,0.95,0.9)
histogramEntries = {
    'jetFakes':'Jet Fakes',
    'ZT':'Z #rightarrow #tau#tau',
    'ZL':'Z #rightarrow #ell #ell',
    'Top':'t#bar{t}',
    'Other':'Others',
    'Higgs':'Higgs Signal (#times 20)'
    }
histogramFormats = {
    'jetFakes':'f',
    'ZT':'f',
    'ZL':'f',
    'Top':'f',
    'Other':'f',
    'Higgs':'l',
    }

def CreateLegend(histogramDictionary):
    theLegend = ROOT.TLegend(legendPosition[0],legendPosition[1],legendPosition[2],legendPosition[3])
    for entry in histogramDictionary:
        AppendToLegend(theLegend,histogramDictionary[entry],entry)
    return theLegend

def AppendToLegend(theLegend,histogram,entry):
    try:
        theLegend.AddEntry(histogram,histogramEntries[entry],histogramFormats[entry])
    except KeyError:
        print("Failed to properly make entry for: "+str(entry))
