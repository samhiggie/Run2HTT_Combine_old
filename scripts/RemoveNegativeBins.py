import ROOT
import argparse
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for removing negative bins from shapes")
    parser.add_argument("FileIn",help="File to remove the negative bins from")
    
    args = parser.parse_args()
    
    TheFile = ROOT.TFile(args.FileIn,"UPDATE")

    for i in range(TheFile.GetListOfKeys().GetEntries()):
        TheDirectory = TheFile.Get(TheFile.GetListOfKeys().At(i).GetName())
        for j in range(TheDirectory.GetListOfKeys().GetEntries()):
            if re.search("(Up|Down)",TheDirectory.GetListOfKeys().At(j).GetName()):
                HasNegativeBins=False
                TheHisto = TheDirectory.Get(TheDirectory.GetListOfKeys().At(j).GetName()).Clone()
                for k in range(1,TheHisto.GetNbinsX()):
                    if TheHisto.GetBinContent(k) < 0.0:
                        HasNegativeBins=True
                        TheHisto.SetBinContent(k,0.0)
                if HasNegativeBins:
                    TheDirectory.cd()
                    TheHisto.Write()
                        
                
