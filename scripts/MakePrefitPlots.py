#!/usr/bin/env python
import argparse
import ROOT
import os
import CombineHarvester.Run2HTT_Combine.PlottingModules.prefitSettings as prefitSettings
import CombineHarvester.Run2HTT_Combine.PlottingModules.Utilities as Utils
import CombineHarvester.Run2HTT_Combine.PlottingModules.globalSettings as globalSettings

def MakePrefitPlots(tag,years,channels):
    globalSettings.style.setTDRStyle()

    theDirectory = os.environ['CMSSW_BASE']+"/src/CombineHarvester/Run2HTT_Combine/HTT_Output/Output_"+tag+"/"
    if not os.path.isdir(theDirectory):
        raise RuntimeError("Couldn't find the output directory. Check the tag to make sure you have the right one.")
    fileName = theDirectory+"fitDiagnostics.Test.root"
    if not os.path.exists(fileName):
        raise RuntimeError("Coudn't find the output file. Are you sure you have the right directory and ran the option to store plots?")
        
    plotFile = ROOT.TFile(fileName)
    prefitDirectory = plotFile.shapes_prefit
    histograms = prefitSettings.RetrievePlots.RetrievePlotsFromAllDirectories(channels,prefitDirectory,years)

    for channel in channels:
        for year in years:
            for category in histograms[channel][year]:
                #retrieve original data
                print("Retrieving data")
                dataCard = ROOT.TFile(prefitSettings.RetrievePlots.RetrieveOriginalDatacardPath(channel,year))
                dataHistogram = dataCard.Get(category).Get("data_obs")
                histograms[channel][year][category]['Data']={'data_obs':dataHistogram}
                theCanvas = ROOT.TCanvas("Prefit_"+category,"Prefit_"+category)
                print("blinding...")
                prefitSettings.blinding.BlindDataPoints(
                    histograms[channel][year][category]['Signals'],
                    histograms[channel][year][category]['Full'],
                    histograms[channel][year][category]['Data']
                )
                
                print("Performing pad set-up...")
                prefitSettings.plotPad.SetupPad(theCanvas)
                print("Creating colors...")
                prefitSettings.colors.ColorizePrefitDistribution(histograms[channel][year][category]['Slimmed'] )
                prefitSettings.colors.ColorizePrefitDistribution(histograms[channel][year][category]['Signals'])                
                #upscale the higgs distribution
                histograms[channel][year][category]['Signals']['Higgs'].Scale(20.0)                
                print("Making stack...")
                backgroundStack = Utils.StackDictionary(histograms[channel][year][category]['Slimmed'])                
                print("Making stack errors...")
                backgroundStackErrors = Utils.MakeStackErrors(backgroundStack)
                print("Creating legend...")
                theLegend = prefitSettings.legend.CreateLegend(histograms[channel][year][category]['Slimmed'])
                prefitSettings.legend.AppendToLegend(theLegend,histograms[channel][year][category]['Signals']['Higgs'],'Higgs')
                print("Drawing...")
                backgroundStack.Draw()
                backgroundStackErrors.Draw("SAME e2")
                histograms[channel][year][category]['Signals']['Higgs'].Draw("SAME")
                histograms[channel][year][category]['Data']['data_obs'].Draw("SAME E1")
                theLegend.Draw()                
                
                raw_input("Press enter to continue...")
    
    
    #for year in years:
    #    for channel in channels

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Create prefit plots from a fit diagnostic output file")
    parser.add_argument('--tag',nargs = "?",help="Tag of the output directory to create plots for",required=True)
    parser.add_argument('--year',nargs="+",choices=['2016','2017','2018'],help="year of results to run.",required=True)
    parser.add_argument('--channels',nargs="+",choices=['mt','tt','et','em'],help="specify the channels to run",required=True)

    args = parser.parse_args()
    MakePrefitPlots(args.tag,args.year,args.channels)
