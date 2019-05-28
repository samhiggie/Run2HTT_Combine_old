import os
import argparse
import ROOT
import logging

logging.basicConfig(filename="CombineHistory.log",filemode="w",level=logging.INFO,format='%(asctime)s %(message)s')

parser = argparse.ArgumentParser(description="Centralized script for running combine fits on dynamically changing analysis categories.")
parser.add_argument('--years',nargs="+",choices=['2016','2017','2018'],help="Specify the year(s) to run the fit for",required=True)
parser.add_argument('--channels',nargs="+",choices=['mt','et','tt'],help="specify the channels to create data cards for",required=True)
parser.add_argument('--RunShapeless',help="Run combine model without using any shape uncertainties",action="store_true")
parser.add_argument('--RunBinByBinLess',help="Run combine model without using bin-by-bin uncertainties",action="store_true")
#Currently bugged. No visible effect.
#parser.add_argument('--RunWithAutoMCStats',help="Run with auto mc stats command appended to data cards",action="store_true")

args = parser.parse_args() 

DataCardCreationCommand = ""

ChannelCards = []

for year in args.years:
    DataCardCreationCommand="SMHTT"+year
    for channel in args.channels:
        DataCardCreationCommand+="_"+channel
        if args.RunShapeless:
            DataCardCreationCommand+=" -s"
        if args.RunBinByBinLess:
            DataCardCreationCommand+=" -b"
        logging.info("Data Card Creation Command:")
        logging.info('\n\n'+DataCardCreationCommand+'\n')
        os.system(DataCardCreationCommand)        

        TheFile = ROOT.TFile(os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+".root")        
        CardCombiningCommand = "combineCards.py"
        CardNum = 1
        for Directory in TheFile.GetListOfKeys():
            CardCombiningCommand += " "+Directory.GetName()+"=smh"+year+"_"+channel+"_"+str(CardNum)+"_13TeV_.txt "
            CardNum+=1
        CombinedChannelName = channel.upper()+year+"DataCard.txt"
        CardCombiningCommand += ("> "+CombinedChannelName)
        logging.info("Channel Combining Command:")
        logging.info('\n\n'+CardCombiningCommand+'\n')
        os.system(CardCombiningCommand)        
        ChannelCards.append(CombinedChannelName)
        
#combine all cards together
CardCombiningCommand = "combineCards.py"
for CombinedChannelCard in ChannelCards:
    CardCombiningCommand+=" "+CombinedChannelCard[:6]+"="+CombinedChannelCard
CombinedCardName = "FinalCard.txt"
CardCombiningCommand += ("> "+CombinedCardName)
logging.info("Final Card Combining Command:")
logging.info('\n\n'+CardCombiningCommand+'\n')
os.system(CardCombiningCommand)

#Currently bugged. No visible effect.
#if args.RunWithAutoMCStats:
#    CardFile = open(CombinedCardName,"a+")
#    CardFile.write(" autoMCStats 0")

#per signal card workspace set up
PerSignalWorkspaceCommand = "text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel "
PerSignalWorkspaceCommand+= "--PO 'map=.*/ggH.*:r_ggH[1,-25,25]' "
PerSignalWorkspaceCommand+= "--PO 'map=.*/qqH.*:r_qqH[1,-25,25]' "
PerSignalWorkspaceCommand+= "--PO 'map=.*/WH.*:r_WH[1,-25,25]' "
PerSignalWorkspaceCommand+= "--PO 'map=.*/ZH.*:r_ZH[1,-25,25]' "
PerSignalWorkspaceCommand+= CombinedCardName +" -o workspace_per_signal_breakdown_2018_cmb.root -m 125"

logging.info("Per Signal Workspace Command:")
logging.info('\n\n'+PerSignalWorkspaceCommand+'\n')
os.system(PerSignalWorkspaceCommand)

#per category
PerCategoryWorkspaceCommand = "text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel "
CategorySignalNames=[]
for Directory in TheFile.GetListOfKeys():
    CategorySignalNames.append("r"+Directory.GetName()[2:])
    PerCategoryWorkspaceCommand += "--PO 'map=.*"+Directory.GetName()+".*/.*_htt.*:"+"r"+Directory.GetName()[2:]+"[1,-25,25]' "
PerCategoryWorkspaceCommand+=CombinedCardName+" -o workspace_per_cat_breakdown_2018_cmb.root -m 125"

logging.info("Per Category Workspace Command: ")
logging.info('\n\n'+PerCategoryWorkspaceCommand+'\n')
os.system(PerCategoryWorkspaceCommand)

#Set up the possible STXS bins list
STXSBins = ["ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125",
            "ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125",
            "ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125",
            "ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125",
            "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125",
            "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125",
            "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125",
            "ggH_PTH_0_200_1J_PTH_120_200_htt125",
            "ggH_PTH_0_200_1J_PTH_60_120_htt125",
            "ggH_PTH_0_200_1J_PTH_0_60_htt125",
            "ggH_PTH_0_200_0J_PTH_10_200_htt125",
            "ggH_PTH_0_200_0J_PTH_0_10_htt125",
            "ggH_PTH_GE200_htt125",
            "qqH_0J_htt125",
            "qqH_1J_htt125",
            "qqH_GE2J_MJJ_0_60_htt125",
            "qqH_GE2J_MJJ_60_120_htt125",
            "qqH_GE2J_MJJ_120_350_htt125",
            "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125",
            "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125",
            "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125",
            "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125",
            "qqH_GE2J_MJJ_GE350_PTH_GE200_htt125"]
PerSTXSBinsWorkSpaceCommand = "text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel "
STXSSignalNames=[]
for Bin in STXSBins:
    STXSSignalNames.append("r_"+Bin)
    PerSTXSBinsWorkSpaceCommand += "--PO 'map=.*/"+Bin+":"+"r_"+Bin+"[1,-25,25]' "
PerSTXSBinsWorkSpaceCommand += CombinedCardName+" -o workspace_per_STXS_breakdown_2018_cmb.root -m 125"

logging.info("Per STXS Bins Work Space Command")
logging.info('\n\n'+PerSTXSBinsWorkSpaceCommand+'\n')
os.system(PerSTXSBinsWorkSpaceCommand)

#add in the merged ones
PerMergedBinWorkSpaceCommand = "text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel "
MergedSignalNames=[]
#qqH, less than 2 Jets
MergedSignalNames.append("qqH_LT2J")
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/qqH_0J_htt125:r_qqH_LT2J[1,-25,25]' "
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/qqH_1J_htt125:r_qqH_LT2J[1,-25,25]' "
#qqH mjj 0-350
MergedSignalNames.append("qqH_GE2J_MJJ_0_350")
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/qqH_GE2J_MJJ_0_60_htt125:r_qqH_GE2J_MJJ_0_350[1,-25,25]' "
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/qqH_GE2J_MJJ_60_120_htt125:r_qqH_GE2J_MJJ_0_350[1,-25,25]' "
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/qqH_GE2J_MJJ_120_350_htt125:r_qqH_GE2J_MJJ_0_350[1,-25,25]' "
#qqH mjj 350-700, all PtH
MergedSignalNames.append("qqH_GE2J_MJJ_350_700_PTH_0_200")
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125:r_qqH_GE2J_MJJ_350_700_PTH_0_200[1,-25,25]' "
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125:r_qqH_GE2J_MJJ_350_700_PTH_0_200[1,-25,25]' "
#qqH mjj 700+, all PtH
MergedSignalNames.append("qqH_GE2J_MJJ_GE700_PTH_0_200")
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125:r_qqH_GE2J_MJJ_GE700_PTH_0_200[1,-25,25]' "
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125:r_qqH_GE2J_MJJ_GE700_PTH_0_200[1,-25,25]' "
#ggH 2Jets, mjj 350+
MergedSignalNames.append("ggH_PTH_0_200_GE2J_MJJ_GE350")
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125:r_ggH_PTH_0_200_GE2J_MJJ_GE350[1,-25,25]' "
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125:r_ggH_PTH_0_200_GE2J_MJJ_GE350[1,-25,25]' " 
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125:r_ggH_PTH_0_200_GE2J_MJJ_GE350[1,-25,25]' "
PerMergedBinWorkSpaceCommand += "--PO 'map=.*/ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125:r_ggH_PTH_0_200_GE2J_MJJ_GE350[1,-25,25]' " 
PerMergedBinWorkSpaceCommand += CombinedCardName+" -o workspace_per_Merged_breakdown_2018_cmb.root -m 125"

logging.info("Per Meged Bin Work Space Command")
logging.info('\n\n'+PerMergedBinWorkSpaceCommand+'\n')
os.system(PerMergedBinWorkSpaceCommand)

TextWorkspaceCommand = "text2workspace.py "+CombinedCardName
logging.info("Text 2 Worskpace Command:")
logging.info('\n\n'+TextWorkspaceCommand+'\n')
os.system(TextWorkspaceCommand)

#run the inclusive
CombinedWorkspaceName = CombinedCardName[:len(CombinedCardName)-3]+"root"
InclusiveCommand="combine -M MultiDimFit "+CombinedWorkspaceName+" --robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --expectSignal=1 -t -1 --algo=singles --cl=0.68"
logging.info("Inclusive combine command:")
logging.info('\n\n'+InclusiveCommand+'\n')
os.system(InclusiveCommand)

#run the per categories
for SignalName in CategorySignalNames:
    CombineCommand = "combine -M MultiDimFit workspace_per_cat_breakdown_2018_cmb.root --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --robustFit=1 --algo=singles --cl=0.68 -t -1 --setParameters r_0jet_PTH_0_10=1,r_0jet_PTH_GE10=1,r_boosted_1J=1,r_boosted_GE2J=1,r_vbf_PTH_0_200=1,r_vbf_PTH_GE_200=1 -P "+SignalName+" --floatOtherPOIs=1"
    logging.info("Category Signal Command: ")
    logging.info('\n\n'+CombineCommand+'\n')    
    os.system(CombineCommand)

#run the signal samples
for SignalName in ["r_ggH","r_qqH","r_WH","r_ZH"]:
    CombineCommand = "combine -M MultiDimFit workspace_per_signal_breakdown_2018_cmb.root --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --robustFit=1 --algo=singles --cl=0.68 -t -1 --setParameters r_ggH=1,r_qqH=1,r_WH=1,r_ZH=1 -P "+SignalName+" --floatOtherPOIs=1" 
    logging.info("Signal Sample Signal Command: ")
    logging.info('\n\n'+CombineCommand+'\n')
    os.system(CombineCommand)

# run the STXS bins
for STXSBin in STXSBins:
    CombineCommand = "combine -M MultiDimFit workspace_per_STXS_breakdown_2018_cmb.root --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --robustFit=1 --algo=singles --cl=0.68 -t -1 --setParameters "
    for BinName in STXSBins:
        CombineCommand+=("r_"+BinName+"=1,")
    CombineCommand[:len(CombineCommand)-1]
    CombineCommand+=" -P r_"+STXSBin+" --floatOtherPOIs=1"
    logging.info("STXS Combine Command:")
    logging.info('\n\n'+CombineCommand+'\n')    
    os.system(CombineCommand)

#run the merged bins
for MergedBin in MergedSignalNames:
    CombineCommand = "combine -M MultiDimFit workspace_per_Merged_breakdown_2018_cmb.root --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --X-rtd FITTER_BOUND --robustFit=1 --algo=singles --cl=0.68 -t -1 --setParameters "
    for BinName in MergedSignalNames:
        CombineCommand+=("r_"+BinName+"=1,")
    CombineCommand+=" -P r_"+MergedBin+" --floatOtherPOIs=1"
    logging.info("Merged Bin Combine Command:")
    logging.info('\n\n'+CombineCommand+'\n')
    os.system(CombineCommand)
