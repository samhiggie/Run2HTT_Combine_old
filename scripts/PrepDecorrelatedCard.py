#!/usr/bin/env python
import ROOT
import argparse
import re

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a copy of the specified data card with duplicated shape histograms for correllating/decorrelating uncertainties")
    parser.add_argument('--year',nargs="?",choices={"2016","2017","2018"},help="data card year.")
    parser.add_argument('--DataCard',help="Specify the data card")
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
		    # For the embedded sample, duplicate the tau ES for partial correlation
		    if "CMS_scale_emb_t" in CopyHisto.GetName():
			if args.TrimYears:
			   CopyHisto2 = TheDirectory.Get(Histogram.GetName()).Clone()
			   NewNameTitle2 = CopyHisto.GetName().replace('_emb','')[:len(CopyHisto.GetName())-11]+"Up"
                	   CopyHisto2.SetNameTitle(NewNameTitle2,NewNameTitle2)
			   CopyHisto2.Write()
                           CopyHisto3 = TheDirectory.Get(Histogram.GetName()).Clone()
                           NewNameTitle3 = CopyHisto.GetName().replace('_emb','')
                           CopyHisto3.SetNameTitle(NewNameTitle3,NewNameTitle3)
                           CopyHisto3.Write()
			else:
                           CopyHisto2 = TheDirectory.Get(Histogram.GetName()).Clone()                           
                           #NewNameTitle2 = CopyHisto.GetName().replace('_emb','')[:len(CopyHisto.GetName())-2]+"_"+args.year+"Up"
                           NewNameTitle2 = CopyHisto.GetName().replace('_emb','')
                           NewNameTitle2 = NewNameTitle2[:len(NewNameTitle2)-2]
                           NewNameTitle2+="_"+args.year+"Up"
                           CopyHisto2.SetNameTitle(NewNameTitle2,NewNameTitle2)
                           CopyHisto2.Write()
                           CopyHisto3 = TheDirectory.Get(Histogram.GetName()).Clone()
                           NewNameTitle3 = CopyHisto.GetName().replace('_emb','')
                           CopyHisto3.SetNameTitle(NewNameTitle3,NewNameTitle3)
                           CopyHisto3.Write()

                elif re.search("Down",CopyHisto.GetName()):
                    if args.TrimYears:
                        NewNameTitle = CopyHisto.GetName()[:len(CopyHisto.GetName())-9]+"Down"
                    else:
                        NewNameTitle = CopyHisto.GetName()[:len(CopyHisto.GetName())-4]+"_"+args.year+"Down"
                    if "CMS_scale_emb_t" in CopyHisto.GetName():
                        if args.TrimYears:
                           CopyHisto2 = TheDirectory.Get(Histogram.GetName()).Clone()
                           NewNameTitle2 = CopyHisto.GetName().replace("_emb","")[:len(CopyHisto.GetName())-13]+"Down"
                           CopyHisto2.SetNameTitle(NewNameTitle2,NewNameTitle2)
                           CopyHisto2.Write()
                           CopyHisto3 = TheDirectory.Get(Histogram.GetName()).Clone()
                           NewNameTitle3 = CopyHisto.GetName().replace("_emb","")
                           CopyHisto3.SetNameTitle(NewNameTitle3,NewNameTitle3)
                           CopyHisto3.Write()
                        else:
                           CopyHisto2 = TheDirectory.Get(Histogram.GetName()).Clone()
                           #NewNameTitle2 = CopyHisto.GetName().replace("_emb","")[:len(CopyHisto.GetName())-4]+"_"+args.year+"Down"
                           NewNameTitle2 = CopyHisto.GetName().replace("_emb","")
                           NewNameTitle2 = NewNameTitle2[:len(NewNameTitle2)-4 ]
                           NewNameTitle2+="_"+args.year+"Down"
                           CopyHisto2.SetNameTitle(NewNameTitle2,NewNameTitle2)
                           CopyHisto2.Write()
                           CopyHisto3 = TheDirectory.Get(Histogram.GetName()).Clone()
                           NewNameTitle3 = CopyHisto.GetName().replace("_emb","")
                           CopyHisto3.SetNameTitle(NewNameTitle3,NewNameTitle3)
                           CopyHisto3.Write()

                else:
                    raise RuntimeError("Something fell through the RE")
                CopyHisto.SetNameTitle(NewNameTitle,NewNameTitle)
                CopyHisto.Write()
    NewDataCardFile.Write()
    NewDataCardFile.Close()
    DataCardFile.Close()
                
                
