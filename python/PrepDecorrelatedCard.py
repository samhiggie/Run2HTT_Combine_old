import ROOT
import argparse
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a copy of the specified data card with duplicated shape histograms for correllating/decorrelating uncertainties")
    parser.add_argument('year',nargs="?",choices={"2016","2017","2018"},help="data card year.")
    parser.add_argument('DataCard',help="Specify the data card")
    parser.add_argument('--OutputFileName',nargs="?",help="Name of the result data card.")

    args = parser.parse_args()        

    DataCardFile = ROOT.TFile(args.DataCard)

    if args.OutputFileName:
        NewDataCardName = args.OutputFileName
    else:
        NewDataCardName = args.DataCard.rsplit(".root")[0]+"_DC.root"

    NewDataCardFile = ROOT.TFile(NewDataCardName,"RECREATE")

    for Directory in DataCardFile.GetListOfKeys():
        TheDirectory = DataCardFile.Get(Directory.GetName())
        NewDirectory = NewDataCardFile.mkdir(Directory.GetName())
        NewDirectory.cd()
        for Histogram in TheDirectory.GetListOfKeys():
            TheDirectory.Get(Histogram.GetName()).Write()
            #if a shape, add it and a copy to the new file
            if re.search("(Up|Down)$",Histogram.GetName()):                
                CopyHisto = TheDirectory.Get(Histogram.GetName()).Clone()
                CopyHisto.SetNameTitle(Histogram.GetName()+"_"+args.year,Histogram.GetName()+"_"+args.year)
                CopyHisto.Write()
    NewDataCardFile.Write()
    NewDataCardFile.Close()
    DataCardFile.Close()
                
                
