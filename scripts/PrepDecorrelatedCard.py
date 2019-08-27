import ROOT
import argparse
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a copy of the specified data card with duplicated shape histograms for correllating/decorrelating uncertainties")
    parser.add_argument('year',nargs="?",choices={"2016","2017","2018"},help="data card year.")
    parser.add_argument('DataCard',help="Specify the data card")
    parser.add_argument('--OutputFileName',nargs="?",help="Name of the result data card.")
    parser.add_argument('--TrimYears',action="store_true",help="Instead of adding years to histogram names, trim them off instead")

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
            if re.search("(Up|Down)",Histogram.GetName()):                
                #if we're trimming years, but this histogram doesn't even have a year
                #then we don't really need to do anything.
                if args.TrimYears and not re.search(args.year+"(Up|Down)$",Histogram.GetName()):
                    continue
                CopyHisto = TheDirectory.Get(Histogram.GetName()).Clone()
                #we need to add a way to add in the year before the "up/down"
                if re.search("Up",CopyHisto.GetName()):
                    if args.TrimYears:
                        NewNameTitle = CopyHisto.GetName()[:len(CopyHisto.GetName())-7]+"Up"
                    else:
                        NewNameTitle = CopyHisto.GetName()[:len(CopyHisto.GetName())-2]+"_"+args.year+"Up"
                elif re.search("Down",CopyHisto.GetName()):
                    if args.TrimYears:
                        NewNameTitle = CopyHisto.GetName()[:len(CopyHisto.GetName())-9]+"Down"
                    else:
                        NewNameTitle = CopyHisto.GetName()[:len(CopyHisto.GetName())-4]+"_"+args.year+"Down"
                else:
                    raise RuntimeError("Something fell through the RE")
                CopyHisto.SetNameTitle(NewNameTitle,NewNameTitle)
                CopyHisto.Write()
    NewDataCardFile.Write()
    NewDataCardFile.Close()
    DataCardFile.Close()
                
                
