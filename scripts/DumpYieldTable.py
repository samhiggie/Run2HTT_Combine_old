import CombineHarvester.CombineTools.ch as ch
import ROOT
import math
import argparse

def PrintTables(cmb,uargs):    
    BinList = cmb.cp().bin_set()    
    print(BinList)
    ProcessList = cmb.cp().process_set()
    print(ProcessList)
    for BinEntry in BinList:
        print(BinEntry)
        Bin_cmb = cmb.cp().bin([BinEntry])
        print r"""
\begin{tabular}{|l|r@{$ \,\,\pm\,\, $}l|}
\hline
Process & \multicolumn{2}{c|}{Normalization}  \\
\hline
\hline"""
        for Process in ProcessList:            
            print r' '+Process+'                                           & $%.1f$ & $%.1f$  \\\\' % (
                                                                                                     
                Bin_cmb.cp().process([Process]).GetRate(), Bin_cmb.cp().process([Process]).GetUncertainty(*uargs)),"\n",
        print r"""\hline
\end{tabular}"""
    print("Inclusive: ")
    print r"""
\begin{tabular}{|l|r@{$ \,\,\pm\,\, $}l|}
\hline
Process & \multicolumn{2}{c|}{Normalization}  \\
\hline
\hline"""
    for Process in ProcessList:
        print r' '+Process+'                                           & $%.1f$ & $%.1f$  \\\\' % (
                                                                                                     
            cmb.cp().process([Process]).GetRate(), cmb.cp().process([Process]).GetUncertainty(*uargs)),"\n",
    print r"""\hline
\end{tabular}"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script for dumping yields to table")
    parser.add_argument("Workspace",help="File to dump everything out of")

    args = parser.parse_args()
    
    TheFile = ROOT.TFile(args.Workspace)

    wsp = TheFile.Get('w')

    cmb = ch.CombineHarvester()
    cmb.SetFlag("workspaces-use-clone",True)
    ch.ParseCombineWorkspace(cmb,wsp, 'ModelConfig', 'data_obs', False)
    
    PrintTables(cmb,tuple())
