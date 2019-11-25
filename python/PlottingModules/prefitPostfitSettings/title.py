import ROOT
import CombineHarvester.Run2HTT_Combine.CategoryConfigurations as catConfig

#histogramTitleSize = 0.1

Title2016 = '2016 prefit'
Title2017 = '2017 prefit'
Title2018 = '2018 prefit'
TitleRun2 = 'Run 2 prefit' 

ZeroJetTitle = 'Zero Jet'
ZeroJetLowTitle = 'Zero Jet Low'
ZeroJetHighTitle = 'Zero Jet High'

BoostedTitle = 'Boosted'
BoostedOneJetTitle = 'Boosted One Jet'
BoostedTwoJetTitle = 'Boosted More than One Jet'

VBFTitle = 'VBF'
VBFLowTitle = 'VBF Low PTH'
VBFHighTitle = 'VBF High PTH'

ttChannelTitle = '#tau#tau Channel'
mtChannelTitle = '#mu#tau Channel'
etChannelTitle = 'e#tau Channel'
emChannelTitle = 'e#mu Channel'
allChannelsTitle = 'All Final States'

def CreateTitle(year,channel,category,histogram):
    title = '' 
    if channel == 'tt':
        title += ttChannelTitle
    elif channel == 'mt':
        title += mtChannelTitle
    elif channel == 'et':
        title += etChannelTitle
    elif channel == 'em':
        title += emChannelTitle
    title += ', '

    if year == '2016':
        title += Title2016
    elif year == '2017':
        title += Title2017
    elif channel == '2018':
        title += Title2018
    elif year == 'Run2':
        title += TitleRun2
    title += ', '

    if (category == catConfig.mt_0jet_low_category
        or category == catConfig.et_0jet_low_category
        or category == catConfig.em_0jet_low_category):
        title += ZeroJetLowTitle
    elif (category == catConfig.mt_0jet_high_category
          or category == catConfig.et_0jet_high_category
          or category == catConfig.em_0jet_high_category):
        title += ZeroJetHighTitle
    elif (category == catConfig.tt_0jet_category
          or category == 'ZeroJet'):
        title += ZeroJetTitle
    elif (category == catConfig.tt_boosted_1J_category
          or category == catConfig.mt_boosted_1J_category
          or category == catConfig.et_boosted_1J_category
          or category == catConfig.em_boosted_1J_category):
        title += BoostedOneJetTitle
    elif (category == catConfig.tt_boosted_GE2J_category
          or category == catConfig.mt_boosted_GE2J_category
          or category == catConfig.et_boosted_GE2J_category
          or category == catConfig.em_boosted_GE2J_category):
        title += BoostedTwoJetTitle
    elif (category == 'Boosted'):
        title += BoostedTitle
    elif (category == catConfig.tt_vbf_low_category
          or category == catConfig.mt_vbf_low_category
          or category == catConfig.et_vbf_low_category
          or category == catConfig.em_vbf_low_category):
        title += VBFLowTitle
    elif(category == catConfig.tt_vbf_high_category
         or category == catConfig.mt_vbf_high_category
         or category == catConfig.et_vbf_high_category
         or category == catConfig.em_vbf_high_category):
        title += VBFHighTitle
    elif (category == 'VBF'):
        title += VBFTitle        

    print(title)
    #histogram.SetTitleSize(histogramTitleSize)
    histogram.SetTitle(title)
