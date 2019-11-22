#!/usr/bin/env python
import argparse
import ROOT
import os
import CombineHarvester.Run2HTT_Combine.PlottingModules.prefitPostfitSettings as prefitPostfitSettings
import CombineHarvester.Run2HTT_Combine.PlottingModules.Utilities as Utils
import CombineHarvester.Run2HTT_Combine.PlottingModules.globalSettings as globalSettings

def MakePrefitPlots(tag,years,channels,DontPerformCalculation = False):
    globalSettings.style.setTDRStyle()
    ROOT.gROOT.SetStyle('tdrStyle')

    theDirectory = os.environ['CMSSW_BASE']+"/src/CombineHarvester/Run2HTT_Combine/HTT_Output/Output_"+tag+"/"
    if not os.path.isdir(theDirectory):
        raise RuntimeError("Couldn't find the output directory. Check the tag to make sure you have the right one.")
    os.chdir(theDirectory)
    
    fileName = "fitDiagnostics.Test.root"
    if not os.path.exists(fileName):
        raise RuntimeError("Coudn't find the output file. Are you sure you have the right directory and ran the option to store plots?")

    #let's go find the final card
    finalCardName = 'FinalCard_'+tag+'.root'
    finalTextCardName = 'FinalCard_'+tag+'.txt'
    if not os.path.exists(finalCardName) or not os.path.exists(finalTextCardName):
        raise RuntimeError("Failed to find the one of the original workspace cards (root/txt). Are you sure the fit all the way through?")

    #first things first, we need to make the actual prefit and post-fit shapes    
    prefitPostfitFile = 'FitHistos.root'
    if not DontPerformCalculation:
        prefitPostfitResult = os.system('PostFitShapesFromWorkspace -o '+prefitPostfitFile+' -m 125 -f '+fileName+':fit_s --postfit --sampling --print -d '+finalTextCardName+' -w '+finalCardName)
        assert prefitPostfitResult == 0, "There was an error while creating the prefits and postfits..."
        
    plotFile = ROOT.TFile(prefitPostfitFile)    
    histograms = prefitPostfitSettings.RetrievePlots.RetrievePlotsFromAllDirectories(channels,plotFile,years)

    for channel in channels:
        for year in years:
            for category in histograms[channel][year]:
                for prefitOrPostfit in ['prefit','postfit']:
                    #retrieve original data
                    print("Retrieving data")
                    dataCard = ROOT.TFile(prefitPostfitSettings.RetrievePlots.RetrieveOriginalDatacardPath(channel,year))
                    dataHistogram = dataCard.Get(category).Get("data_obs")
                    histograms[channel][year][category][prefitOrPostfit]['Data']={'data_obs':dataHistogram}
                    prefitPostfitSettings.dataSettings.ApplyDataSettings(histograms[channel][year][category][prefitOrPostfit]['Data']['data_obs'])
                    
                    #perform blinding
                    print("blinding...")
                    prefitPostfitSettings.blinding.BlindDataPoints(
                        histograms[channel][year][category][prefitOrPostfit]['Signals'],
                        histograms[channel][year][category][prefitOrPostfit]['Full'],
                        histograms[channel][year][category][prefitOrPostfit]['Data']
                    )
                    
                    #Create the canvas and pads needed
                    theCanvas = ROOT.TCanvas(prefitOrPostfit+"_"+category,prefitOrPostfit+"_"+category)
                    print("Performing pad set-up...")
                    prefitPostfitSettings.plotPad.SetupPad(theCanvas)
                    
                    #color in any distributions
                    print("Creating colors...")
                    prefitPostfitSettings.colors.ColorizePrefitDistribution(histograms[channel][year][category][prefitOrPostfit]['Slimmed'] )
                    prefitPostfitSettings.colors.ColorizePrefitDistribution(histograms[channel][year][category][prefitOrPostfit]['Signals'])                
                    
                    #upscale the higgs distribution
                    histograms[channel][year][category][prefitOrPostfit]['Signals']['Higgs'].Scale(20.0)                
                    
                    #make the stack and errors
                    print("Making stack...")
                    backgroundStack = Utils.StackDictionary(histograms[channel][year][category][prefitOrPostfit]['Slimmed'])                
                    print("Making stack errors...")
                    backgroundStackErrors = Utils.MakeStackErrors(backgroundStack)
                    
                    #create the legend
                    print("Creating legend...")
                    theLegend = prefitPostfitSettings.legend.CreateLegend(histograms[channel][year][category][prefitOrPostfit]['Slimmed'])
                    prefitPostfitSettings.legend.AppendToLegend(theLegend,histograms[channel][year][category][prefitOrPostfit]['Signals']['Higgs'],'Higgs')
                    prefitPostfitSettings.legend.AppendToLegend(theLegend,histograms[channel][year][category][prefitOrPostfit]['Data']['data_obs'],'data_obs')
                    prefitPostfitSettings.legend.AppendToLegend(theLegend,backgroundStackErrors,'background_error')
                    
                    #draw everything
                    print("Drawing...")
                    backgroundStack.SetMinimum(0.1)
                    backgroundStack.Draw()
                    backgroundStackErrors.Draw("SAME e2")
                    histograms[channel][year][category][prefitOrPostfit]['Signals']['Higgs'].Draw("SAME HIST")
                    histograms[channel][year][category][prefitOrPostfit]['Data']['data_obs'].Draw("SAME e1")
                    theLegend.Draw()                
                
                    raw_input("Press enter to continue...")
                    
    if len(channels) > 1:
        print("Make Category Combination Plots Here!")
    if len(years) > 1:
        print("Make Year Combination Plots Here!")
    if len(channels) > 1 and len(years) > 1:
        print("Make Year and Category Combination Plots Here")
    
    
    #for year in years:
    #    for channel in channels

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Create prefit plots from a fit diagnostic output file")
    parser.add_argument('--tag',nargs = "?",help="Tag of the output directory to create plots for",required=True)
    parser.add_argument('--years',nargs="+",choices=['2016','2017','2018'],help="year of results to run.",required=True)
    parser.add_argument('--channels',nargs="+",choices=['mt','tt','et','em'],help="specify the channels to run",required=True)
    parser.add_argument('--DontRecalculate',help="Dont preform the PostfitShapesFromWorkspace step again.",action = 'store_true')

    args = parser.parse_args()
    MakePrefitPlots(args.tag,args.year,args.channels,args.DontRecalculate)
