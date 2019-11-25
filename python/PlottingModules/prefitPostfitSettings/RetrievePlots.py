import ROOT
import os
import CombineHarvester.Run2HTT_Combine.CategoryConfigurations as CategoryConfigurations

#given the exact directory path we can try to retrive all plots we know and care about.
#takes as arguments a TDirectory
def RetrievePlotsFromDirectory(directory):
    jetFakes = directory.Get("jetFakes")
    ZT = directory.Get("embedded")
    ZL = directory.Get("ZL")
    TTL = directory.Get("TTL")
    TTT = directory.Get("TTT")
    VVL = directory.Get("VVL")
    VVT = directory.Get("VVT")
    STL = directory.Get("STL")
    STT = directory.Get("STT")
    ggH = directory.Get("ggH_htt125")
    qqH = directory.Get("qqH_htt125")
    WH = directory.Get("WH_htt125")
    ZH = directory.Get("ZH_htt125")
    ggH_PTH_0_200_0J_PTH_0_10_htt125 = directory.Get('ggH_PTH_0_200_0J_PTH_0_10_htt125')
    ggH_PTH_0_200_0J_PTH_10_200_htt125 = directory.Get('ggH_PTH_0_200_0J_PTH_10_200_htt125')
    ggH_PTH_0_200_1J_PTH_0_60_htt125 = directory.Get('ggH_PTH_0_200_1J_PTH_0_60_htt125')
    ggH_PTH_0_200_1J_PTH_120_200_htt125 = directory.Get('ggH_PTH_0_200_1J_PTH_120_200_htt125')
    ggH_PTH_0_200_1J_PTH_60_120_htt125 = directory.Get('ggH_PTH_0_200_1J_PTH_60_120_htt125')
    ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125 = directory.Get('ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125')
    ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125 = directory.Get('ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125')
    ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125 = directory.Get('ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125')    
    ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125 = directory.Get('ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125')
    ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125 = directory.Get('ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125')
    ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125 = directory.Get('ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125')
    ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125 = directory.Get('ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125')
    ggH_PTH_GE200_htt125 = directory.Get('ggH_PTH_GE200_htt125')
    qqH_0J_htt125 = directory.Get('qqH_0J_htt125')
    qqH_1J_htt125 = directory.Get('qqH_1J_htt125')
    qqH_GE2J_MJJ_0_60_htt125 = directory.Get('qqH_GE2J_MJJ_0_60_htt125')
    qqH_GE2J_MJJ_120_350_htt125 = directory.Get('qqH_GE2J_MJJ_120_350_htt125')
    qqH_GE2J_MJJ_60_120_htt125 = directory.Get('qqH_GE2J_MJJ_60_120_htt125')
    qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125 = directory.Get('qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125')
    qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125 = directory.Get('qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125')
    qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125 = directory.Get('qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125')
    qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125 = directory.Get('qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125')
    qqH_GE2J_MJJ_GE350_PTH_GE200_htt125 = directory.Get('qqH_GE2J_MJJ_GE350_PTH_GE200_htt125')

    TT = TTL.Clone()
    TT.SetNameTitle("TT","TT")
    TT.Add(TTT)
    
    VV = VVL.Clone()
    VV.SetNameTitle("VV","VV")
    VV.Add(VVT)

    ST = STL.Clone()
    ST.SetNameTitle("ST","ST")
    ST.Add(STT)

    Top = TT.Clone()
    Top.SetNameTitle("Top","Top")
    Top.Add(ST)

    Higgs = ggH.Clone()
    Higgs.SetNameTitle("Higgs","Higgs")
    Higgs.Add(qqH)
    Higgs.Add(WH)
    Higgs.Add(ZH)

    Other = VV.Clone()
    Other.SetNameTitle("Other","Other")
    Other.Add(Higgs)    

    #create the Full histogram list
    fullDictionary = {
        'jetFakes':jetFakes,
        'ZT':ZT,
        'ZL':ZL,
        'TTL':TTL,
        'TTT':TTT,
        'VVL':VVL,
        'VVT':VVT,
        'STL':STL,
        'STT':STT,
        'ggH':ggH,
        'qqH':qqH,
        'WH':WH,
        'ZH':ZH,
        }
    slimmedDictionary = {
        'jetFakes':jetFakes,
        'ZT':ZT,
        'ZL':ZL,
        'Top':Top,        
        'Other':Other
        }

    signalDictionary = {
        'Higgs':Higgs,
        'ggH':ggH,
        'qqH':qqH,
        'WH':WH,
        'ZH':ZH,
        'ggH_PTH_0_200_0J_PTH_0_10_htt125':ggH_PTH_0_200_0J_PTH_0_10_htt125,
        'ggH_PTH_0_200_0J_PTH_10_200_htt125':ggH_PTH_0_200_0J_PTH_10_200_htt125,
        'ggH_PTH_0_200_1J_PTH_0_60_htt125':ggH_PTH_0_200_1J_PTH_0_60_htt125,
        'ggH_PTH_0_200_1J_PTH_120_200_htt125':ggH_PTH_0_200_1J_PTH_120_200_htt125,
        'ggH_PTH_0_200_1J_PTH_60_120_htt125':ggH_PTH_0_200_1J_PTH_60_120_htt125,
        'ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125':ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125,
        'ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125':ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125,
        'ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125':ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125,
        'ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125': ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125,
        'ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125': ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125,
        'ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125':ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125,
        'ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125':ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125,
        'ggH_PTH_GE200_htt125':ggH_PTH_GE200_htt125,
        'qqH_0J_htt125':qqH_0J_htt125,
        'qqH_1J_htt125':qqH_1J_htt125,
        'qqH_GE2J_MJJ_0_60_htt125':qqH_GE2J_MJJ_0_60_htt125,
        'qqH_GE2J_MJJ_120_350_htt125':qqH_GE2J_MJJ_120_350_htt125,
        'qqH_GE2J_MJJ_60_120_htt125': qqH_GE2J_MJJ_60_120_htt125,
        'qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125':qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125,
        'qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125':qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125,
        'qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125':qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125,
        'qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125':qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125,
        'qqH_GE2J_MJJ_GE350_PTH_GE200_htt125':qqH_GE2J_MJJ_GE350_PTH_GE200_htt125,
        
    }

    #create the slimmed histogram list with the plots common to most plotting schemes
    return {'Full':fullDictionary,'Slimmed':slimmedDictionary,'Signals':signalDictionary}

def RetrieveOriginalDatacardPath(channel,year):
    datacardPath = os.environ['CMSSW_BASE']+'/src/auxiliaries/shapes/'
    datacardName = 'smh'+year+channel+'.root'
    return datacardPath+datacardName

#retrieve all plots conforming to current category configuration specs.
#takes as arguments a list of channels from ['tt','mt','et','em']
#and a TFile or TDirectory.
#the years of the plot to be retrieved
def RetrievePlotsFromAllDirectories(channels,location,years,withYears = True):
    location.ls()
    histograms = {}
    for channel in channels:
        histograms[channel] = {}        
        for year in years:
            histograms[channel][year]={}
            for categoryName in CategoryConfigurations.Categories[channel]:
                histograms[channel][year][categoryName] = {}
                for prefitOrPostfit in ['prefit','postfit']:                    
                    directoryName = categoryName+'_'+year+'_'+prefitOrPostfit
                    candidateDirectory = location.Get(directoryName)
                    if candidateDirectory == None:
                        print("Could not load all histograms from the files because it was missing a directory: "+directoryName)
                        continue
                    else:
                        print("loading plots from : "+directoryName)
                        histograms[channel][year][categoryName][prefitOrPostfit] = RetrievePlotsFromDirectory(candidateDirectory)                    
    return histograms
