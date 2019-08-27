import ROOT
import argparse
import re
from array import array
import math
import MergeStats

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Script for merging low stats bins together.")
    parser.add_argument("FileIn",help="File to merge bins in")
    parser.add_argument("OutputFile",nargs="?",help="Name of the output file",default="MergedFile.root")

    args = parser.parse_args()
    
    TheFile = ROOT.TFile(args.FileIn)
    NewFile = ROOT.TFile(args.OutputFile,"RECREATE")

    for i in range(TheFile.GetListOfKeys().GetEntries()):
        TheDirectory = TheFile.Get(TheFile.GetListOfKeys().At(i).GetName())
        print(TheDirectory.GetName())
        NewFileDir = NewFile.mkdir(TheDirectory.GetName())
        NewFileDir.cd()
        NominalList = []
        HistogramList = []
        for j in range(TheDirectory.GetListOfKeys().GetEntries()):
            HistogramList.append(TheDirectory.Get(TheDirectory.GetListOfKeys().At(j).GetName()).Clone())
            NominalMatch = re.search("(ggH_htt125|qqH_htt125|^(?!ggH)(?!qqH)(?!data).+)$(?<!Up)(?<!Down)",TheDirectory.GetListOfKeys().At(j).GetName())
            if NominalMatch:                
                NominalList.append(TheDirectory.Get(TheDirectory.GetListOfKeys().At(j).GetName()).Clone())
        if re.search("0jet.*PTH.*0.*10",TheDirectory.GetName()):
            #handle the sixth slice
            MergeStats.MergeBin(55+9,55+10,NominalList,HistogramList)
            MergeStats.MergeBin(55+7,55+8,NominalList,HistogramList)
            MergeStats.MergeBin(55+5,55+6,NominalList,HistogramList)
            MergeStats.MergeBin(55+3,55+4,NominalList,HistogramList)
            MergeStats.MergeBin(55+1,55+2,NominalList,HistogramList)            
            #handle the fifth slice
            MergeStats.MergeBin(44+9,44+10,NominalList,HistogramList)
            MergeStats.MergeBin(44+7,44+8,NominalList,HistogramList)
            MergeStats.MergeBin(44+5,44+6,NominalList,HistogramList)
            MergeStats.MergeBin(44+3,44+4,NominalList,HistogramList)
            MergeStats.MergeBin(44+1,44+2,NominalList,HistogramList)            
            #handle the fourth slice
            MergeStats.MergeBin(33+9,33+10,NominalList,HistogramList)            
            MergeStats.MergeBin(33+7,33+8,NominalList,HistogramList)            
            MergeStats.MergeBin(33+5,33+6,NominalList,HistogramList)            
            MergeStats.MergeBin(33+3,33+4,NominalList,HistogramList)            
            MergeStats.MergeBin(33+1,33+2,NominalList,HistogramList)
        elif re.search("vbf.*PTH.*GE.*200",TheDirectory.GetName()):
            #handle the 4th slice
            MergeStats.MergeBin(33+9,33+10,NominalList,HistogramList)
            MergeStats.MergeBin(33+7,33+8,NominalList,HistogramList)
            MergeStats.MergeBin(33+5,33+6,NominalList,HistogramList)
            MergeStats.MergeBin(33+3,33+4,NominalList,HistogramList)
            MergeStats.MergeBin(33+1,33+2,NominalList,HistogramList)            
        NewFileDir.cd()
        for Histogram in HistogramList:
            Histogram.Write()
    NewFile.Write()
    NewFile.Close()
