import ROOT

fillColoringScheme = {
        'jetFakes':"#ffccff",
        'ZT':"#ffcc66",
        'ZL':'#4496c8',
        'Top':'#9999cc',
        'Other':'#12cadd',
        }

lineColoringScheme = {
        'Higgs': ROOT.kRed,
        'jetFakes':ROOT.kBlack,
        'ZT':ROOT.kBlack,
        'ZL':ROOT.kBlack,
        'Top':ROOT.kBlack,
        'Other':ROOT.kBlack,
        }

def ColorizePrefitDistribution(histogramDictionary):            
    for entry in histogramDictionary:
        try:
            histogramDictionary[entry].SetFillColor(ROOT.TColor.GetColor(fillColoringScheme[entry]))
        except KeyError:
            print("Failed to colorize the fill of distribution: "+str(entry))
        except AttributeError:
            print("Histogram does not seem to properly exist: "+str(entry))
    for entry in histogramDictionary:
        try:            
            histogramDictionary[entry].SetLineColor(lineColoringScheme[entry])
        except KeyError:
            print("Failed to colorize the line of distribution: "+str(entry))
        except AttributeError:
            print("Histogram does not seem to properly exist: "+str(entry))
