import os
import argparse
import ROOT
import logging
import datetime
import string
import random
import CategoryConfigurations as cfg
from EmbeddedConfiguration import EmbeddedConfiguration as embedded_cfg
from CombineHarvester.Run2HTT_Combine.SplitUncertainty import UncertaintySplitter

def RandomStringTag(size=6,chars=string.ascii_uppercase+string.ascii_lowercase+string.digits):
    return ''.join(random.choice(chars) for x in range(size))

parser = argparse.ArgumentParser(description="Centralized script for running combine fits on dynamically changing analysis categories.")
parser.add_argument('--years',nargs="+",choices=['2016','2017','2018'],help="Specify the year(s) to run the fit for",required=True)
parser.add_argument('--channels',nargs="+",choices=['mt','et','tt','em'],help="specify the channels to create data cards for",required=True)
parser.add_argument('--RunShapeless',help="Run combine model without using any shape uncertainties",action="store_true")
parser.add_argument('--RunWithBinByBin',help="Run combine model without using bin-by-bin uncertainties",action="store_true")
parser.add_argument('--RunWithoutAutoMCStats',help="Run with auto mc stats command appended to data cards",action="store_true")
parser.add_argument('--RunInclusiveggH',help="Run using an inclusive ggH distribution (no STXS bins), using either this or the the inclusive qqH will cancel STXS bin measurements",action="store_true")
parser.add_argument('--RunInclusiveqqH',help="Run using an inclusive qqH distribution (no STXS bins), using either this or the inclusive ggH will cancel STXS bin measurements.",action="store_true")
parser.add_argument('--ComputeSignificance',help="Compute expected significances instead of expected POIs",action="store_true")
parser.add_argument('--ComputeImpacts',help="Compute expected impacts on Inclusive POI",action="store_true")
parser.add_argument('--DisableCategoryFits',help="Disable category card creation and fits",action="store_true")
parser.add_argument('--Timeout', help="Timeout after 3min", action="store_true")
parser.add_argument('--SplitUncertainties', help="Create groups for helping to split the measurements",action="store_true")
parser.add_argument('--SplitInclusive',help="Split the inclusive measurements into component pieces. REQUIRES --SplitUncertainties",action="store_true")
parser.add_argument('--SplitSignals',help="Split signal measurements into component pieces. REQUIRES --SplitUncertainties",action="store_true")
parser.add_argument('--SplitSTXS',help="Split STXS measurements into component pieces. REQUIRES --SplitUncertainties",action="store_true")
parser.add_argument('--RunParallel',help='Run all fits in parallel using condor',action="store_true")
print("Parsing command line arguments.")
args = parser.parse_args() 

if (args.SplitInclusive or args.SplitSignals or args.SplitSTXS) and not (args.SplitUncertainties):
    parser.error("Tried to split a measurement without calling --SplitUncertainties!")

DateTag = datetime.datetime.now().strftime("%d%m%y_")+RandomStringTag()
print ''
print "*********************************************"
print("This session is run under tag: "+DateTag)
print "*********************************************"
print ''
#check if we have an output directory
if args.RunParallel:
    print("Running jobs on condor. Creating the ouput on hdfs instead...")
    if not os.path.isdir("/hdfs/store/user/"+os.environ['USER']+"/HTT_Output"):
        os.mkdir("/hdfs/store/user/"+os.environ['USER']+"/HTT_Output")
    OutputDir = "/hdfs/store/user/"+os.environ['USER']+"/HTT_Output/Output_"+DateTag+"/"
    os.mkdir(OutputDir)
else:    
    if not os.path.isdir(os.environ['CMSSW_BASE']+"/src/CombineHarvester/Run2HTT_Combine/HTT_Output"):
        os.mkdir(os.environ['CMSSW_BASE']+"/src/CombineHarvester/Run2HTT_Combine/HTT_Output")
    OutputDir = os.environ['CMSSW_BASE']+"/src/CombineHarvester/Run2HTT_Combine/HTT_Output/Output_"+DateTag+"/"
    os.mkdir(OutputDir)
print("Output directory is: "+OutputDir)

logging.basicConfig(filename=OutputDir+"CombineHistory_"+DateTag+".log",filemode="w",level=logging.INFO,format='%(asctime)s %(message)s')

DataCardCreationCommand = ""

ChannelCards = []

for year in args.years:    
    for channel in args.channels:
        DataCardCreationCommand="SMHTT"+year
        DataCardCreationCommand+="_"+channel+" "+OutputDir
        if args.RunShapeless:
            DataCardCreationCommand+=" -s"
        if not args.RunWithBinByBin:
            DataCardCreationCommand+=" -b"
        #if args.RunEmbeddedLess:
        if not embedded_cfg[str(year)+str(channel)]: #load from config. If false, run embedded less
            DataCardCreationCommand+=" -e"
        if args.RunInclusiveggH:
            DataCardCreationCommand+=" -g"
        if args.RunInclusiveqqH:
            DataCardCreationCommand+=" -q"
        DataCardCreationCommand+=" --Categories"
        for Category in cfg.Categories[channel]:
            DataCardCreationCommand+=" "+cfg.Categories[channel][Category]
        print("Creating data cards")
        logging.info("Data Card Creation Command:")
        logging.info('\n\n'+DataCardCreationCommand+'\n')
        os.system(DataCardCreationCommand)        
        

#cobmine all cards together
#we can't do this the old way of first mashing all channels together and then mashing those into a final card
#messes with paths somewhere
#we have to do this in one fell swoop.
CombinedCardName = OutputDir+"FinalCard_"+DateTag+".txt"
CardCombiningCommand = "combineCards.py"
if args.SplitUncertainties:
    Splitter = UncertaintySplitter()
for year in args.years:
    for channel in args.channels:
        CardNum = 1
        TheFile = ROOT.TFile(os.environ['CMSSW_BASE']+"/src/auxiliaries/shapes/smh"+year+channel+".root")
        for Directory in TheFile.GetListOfKeys():
            if Directory.GetName() in cfg.Categories[channel].values():
                if not args.RunWithoutAutoMCStats:
                    CardFile = open(OutputDir+"smh"+year+"_"+channel+"_"+str(CardNum)+"_13TeV_.txt","a+")
                    CardFile.write("* autoMCStats 0.0\n")
                    CardFile.close()                
                if args.SplitUncertainties:                    
                    Splitter.FindAndTagGroups(OutputDir+"smh"+year+"_"+channel+"_"+str(CardNum)+"_13TeV_.txt")
                CardCombiningCommand += " "+Directory.GetName()+"_"+year+"="+OutputDir+"smh"+year+"_"+channel+"_"+str(CardNum)+"_13TeV_.txt "
                CardNum+=1
CardCombiningCommand+= " > "+CombinedCardName
logging.info("Final Card Combining Command:")
logging.info('\n\n'+CardCombiningCommand+'\n')
os.system(CardCombiningCommand)


#per signal card workspace set up
print("Setting up per signal workspace")
PerSignalName = OutputDir+"Workspace_per_signal_breakdown_cmb_"+DateTag+".root"
PerSignalWorkspaceCommand = "text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel "
PerSignalWorkspaceCommand+= "--PO 'map=.*/ggH.*:r_ggH[1,-25,25]' "
PerSignalWorkspaceCommand+= "--PO 'map=.*/qqH.*:r_qqH[1,-25,25]' "
PerSignalWorkspaceCommand+= "--PO 'map=.*/WH.*:r_WH[1,-25,25]' "
PerSignalWorkspaceCommand+= "--PO 'map=.*/ZH.*:r_ZH[1,-25,25]' "
PerSignalWorkspaceCommand+= CombinedCardName +" -o "+PerSignalName+" -m 125"

logging.info("Per Signal Workspace Command:")
logging.info('\n\n'+PerSignalWorkspaceCommand+'\n')
os.system(PerSignalWorkspaceCommand)

#per category
if not args.DisableCategoryFits:
    print("Setting up per category command.")
    PerCategoryName = OutputDir+"workspace_per_cat_breakdown_cmb_"+DateTag+".root"
    PerCategoryWorkspaceCommand = "text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel "
    CategorySignalNames=[]
    for Directory in TheFile.GetListOfKeys():
        CategorySignalNames.append("r"+Directory.GetName()[2:])
        PerCategoryWorkspaceCommand += "--PO 'map=.*"+Directory.GetName()+".*/.*_htt.*:"+"r"+Directory.GetName()[2:]+"[1,-25,25]' "
    PerCategoryWorkspaceCommand+=CombinedCardName+" -o "+PerCategoryName+" -m 125"

    logging.info("Per Category Workspace Command: ")
    logging.info('\n\n'+PerCategoryWorkspaceCommand+'\n')
    os.system(PerCategoryWorkspaceCommand)

#Set up the possible STXS bins list
if not (args.RunInclusiveggH or args.RunInclusiveqqH):
    print("Setting up STXS commands")
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
    PerSTXSName = OutputDir+"workspace_per_STXS_breakdown_cmb_"+DateTag+".root"
    PerSTXSBinsWorkSpaceCommand = "text2workspace.py -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel "
    STXSSignalNames=[]
    for Bin in STXSBins:
        STXSSignalNames.append("r_"+Bin)
        PerSTXSBinsWorkSpaceCommand += "--PO 'map=.*/"+Bin+":"+"r_"+Bin+"[1,-25,25]' "
    PerSTXSBinsWorkSpaceCommand += CombinedCardName+" -o "+PerSTXSName+" -m 125"

    logging.info("Per STXS Bins Work Space Command")
    logging.info('\n\n'+PerSTXSBinsWorkSpaceCommand+'\n')
    os.system(PerSTXSBinsWorkSpaceCommand)

    #add in the merged ones
    PerMergedBinName = OutputDir+"workspace_per_Merged_breakdown_cmb_"+DateTag+".root"
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
    PerMergedBinWorkSpaceCommand += CombinedCardName+" -o "+PerMergedBinName+" -m 125"

    logging.info("Per Merged Bin Work Space Command")
    logging.info('\n\n'+PerMergedBinWorkSpaceCommand+'\n')
    os.system(PerMergedBinWorkSpaceCommand)

TextWorkspaceCommand = "text2workspace.py "+CombinedCardName+" -m 125"
logging.info("Text 2 Worskpace Command:")
logging.info('\n\n'+TextWorkspaceCommand+'\n')
os.system(TextWorkspaceCommand)

PhysModel = 'MultiDimFit'
ExtraCombineOptions = '--robustFit=1 --preFitValue=1. --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --algo=singles --cl=0.68'
if args.ComputeSignificance:
    PhysModel = 'Significance'
    ExtraCombineOptions = '--X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP --cl=0.68'

#run the inclusive
CombinedWorkspaceName = CombinedCardName[:len(CombinedCardName)-3]+"root"
InclusiveCommand="combineTool.py -M "+PhysModel+" "+CombinedWorkspaceName+" "+ExtraCombineOptions+" --expectSignal=1 -t -1"
if args.RunParallel:
    InclusiveCommand+=" --job-mode condor --sub-opts=\""
    InclusiveCommand+="+JobFlavor = \"tomorrow\"\n"
    InclusiveCommand+="RequestCpus = 4\n"
    InclusiveCommand+="output = "+OutputDir+"r_joboutput.txt\n"
    InclusiveCommand+="error="+OutputDir+"r_joberror.txt\n"
    InclusiveCommand+="log="+OutputDir+"joblog.log \""
    InclusiveCommand+=" --task-name htt_Fit_r_"+DateTag
if args.Timeout is True:
    InclusiveCommand = "timeout 180s " + InclusiveCommand
logging.info("Inclusive combine command:")
logging.info('\n\n'+InclusiveCommand+'\n')
os.system(InclusiveCommand)
if args.SplitInclusive:
    Splitter.SplitMeasurement(InclusiveCommand,OutputDir)

if not args.ComputeSignificance:
    #run the signal samples
    for SignalName in ["r_ggH","r_qqH","r_WH","r_ZH"]:
        CombineCommand = "combineTool.py -M "+PhysModel+" "+PerSignalName+" "+ExtraCombineOptions+" -t -1 --setParameters r_ggH=1,r_qqH=1,r_WH=1,r_ZH=1 -P "+SignalName+" --floatOtherPOIs=1" 
        if args.Timeout is True:
            CombineCommand = "timeout 180s " + CombineCommand
        if args.RunParallel:
            if args.RunParallel:
                CombineCommand+=" --job-mode condor --sub-opts=\""
                CombineCommand+="+JobFlavor = \"tomorrow\"\n"
                CombineCommand+="RequestCpus = 4\n"
                CombineCommand+="output = "+OutputDir+SignalName+"_joboutput.txt\n"
                CombineCommand+="error="+OutputDir+SignalName+"_joberror.txt\n"
                CombineCommand+="log="+OutputDir+SignalName+"_joblog.log \""
                CombineCommand+=" --task-name htt_Fit_"+SignalName+DateTag
                CombineCommand+=" --dry-run"
        logging.info("Signal Sample Signal Command: ")
        logging.info('\n\n'+CombineCommand+'\n')
        os.system(CombineCommand)
        if args.SplitSignals:
            Splitter.SplitMeasurement(CombineCommand,OutputDir)

    #run the per categories
    if not args.DisableCategoryFits:
        for SignalName in CategorySignalNames:
            CombineCommand = "combineTool.py -M "+PhysModel+" "+PerCategoryName+" "+ExtraCombineOptions+" -t -1 --setParameters r_0jet_PTH_0_10=1,r_0jet_PTH_GE10=1,r_boosted_1J=1,r_boosted_GE2J=1,r_vbf_PTH_0_200=1,r_vbf_PTH_GE_200=1 -P "+SignalName+" --floatOtherPOIs=1"
            if args.Timeout is True:
                CombineCommand = "timeout 180s " + CombineCommand
            if args.RunParallel:
                CombineCommand+=" --job-mode condor --sub-opts=\"+JobFlavor = \"tomorrow\"\nRequestCpus = 4 \" --task-name htt_Fit_"+SignalName+"_"+DateTag+" --dry-run"
            logging.info("Category Signal Command: ")
            logging.info('\n\n'+CombineCommand+'\n')    
            os.system(CombineCommand)

# run the STXS bins
if not (args.RunInclusiveggH or args.RunInclusiveqqH or args.ComputeSignificance):
    for STXSBin in STXSBins:
        CombineCommand = "combineTool.py -M "+PhysModel+" "+PerSTXSName+" "+ExtraCombineOptions+" -t -1 --setParameters "
        for BinName in STXSBins:
            CombineCommand+=("r_"+BinName+"=1,")        
        CombineCommand+=" -P r_"+STXSBin+" --floatOtherPOIs=1"
        if args.Timeout is True:
            CombineCommand = "timeout 180s " + CombineCommand
        if args.RunParallel:
            CombineCommand+=" --job-mode condor --sub-opts=\""
            CombineCommand+="+JobFlavor = \"tomorrow\"\n"
            CombineCommand+="RequestCpus = 4\n"
            CombineCommand+="output = "+OutputDir+"r_"+SignalName+"_joboutput.txt\n"
            CombineCommand+="error="+OutputDir+"r_"+SignalName+"_joberror.txt\n"
            CombineCommand+="log="+OutputDir+"r_"+SignalName+"_joblog.log \""
            CombineCommand+=" --task-name htt_Fit_r_"+SignalName+DateTag
            CombineCommand+=" --dry-run"
        logging.info("STXS Combine Command:")
        logging.info('\n\n'+CombineCommand+'\n')    
        os.system(CombineCommand)
        if args.SplitSTXS:
            Splitter.SplitMeasurement(CombineCommand,OutputDir)
    #run the merged bins
    for MergedBin in MergedSignalNames:
        CombineCommand = "combineTool.py -M "+PhysModel+" "+PerMergedBinName+" "+ExtraCombineOptions+" -t -1 --setParameters "
        for BinName in MergedSignalNames:
            CombineCommand+=("r_"+BinName+"=1,")
        CombineCommand+=" -P r_"+MergedBin+" --floatOtherPOIs=1"
        if args.Timeout is True:
            CombineCommand = "timeout 180s " + CombineCommand
        if args.RunParallel:
            CombineCommand+=" --job-mode condor --sub-opts=\""
            CombineCommand+="+JobFlavor = \"tomorrow\"\n"
            CombineCommand+="RequestCpus = 4\n"
            CombineCommand+="output = "+OutputDir+"r_"+SignalName+"_joboutput.txt\n"
            CombineCommand+="error="+OutputDir+"r_"+SignalName+"_joberror.txt\n"
            CombineCommand+="log="+OutputDir+"r_"+SignalName+"_joblog.log \""
            CombineCommand+=" --task-name htt_Fit_r_"+SignalName+DateTag
            CombineCommand+=" --dry-run"
        logging.info("Merged Bin Combine Command:")
        logging.info('\n\n'+CombineCommand+'\n')
        os.system(CombineCommand)

#run impact fitting
if args.ComputeImpacts:
    os.chdir(OutputDir)
    print("\nCalculating Impacts, this may take a while...\n")
    print("Initial fit")
    ImpactCommand = "combineTool.py -M Impacts -d "+CombinedWorkspaceName+" -m 125 --doInitialFit --robustFit 1 --expectSignal=1 -t -1 --parallel 8 "
    logging.info("Initial Fit Impact Command:")
    logging.info('\n\n'+ImpactCommand+'\n')
    os.system(ImpactCommand)
        
    print("Full fit")
    ImpactCommand = "combineTool.py -M Impacts -d "+CombinedWorkspaceName+" -m 125 --robustFit 1 --doFits --expectSignal=1 -t -1 --parallel 8 --X-rtd FITTER_NEW_CROSSING_ALGO --X-rtd FITTER_NEVER_GIVE_UP "
    logging.info("Full Fit Impact Command:")
    logging.info('\n\n'+ImpactCommand+'\n')
    os.system(ImpactCommand)

    print("json-ifying")
    ImpactJsonName = "impacts_final_"+DateTag+".json"
    ImpactCommand = "combineTool.py -M Impacts -d "+CombinedWorkspaceName+" -m 125 -o "+ImpactJsonName
    logging.info("JSON Output Impact Command:")
    logging.info('\n\n'+ImpactCommand+'\n')
    os.system(ImpactCommand)

    print("final impact plot")
    FinalImpactName = "impacts_final_"+DateTag
    ImpactCommand = "plotImpacts.py -i "+ImpactJsonName+" -o "+FinalImpactName
    logging.info("Plotting Impact Command:")
    logging.info('\n\n'+ImpactCommand+'\n')
    os.system(ImpactCommand)

    os.chdir("../../")
