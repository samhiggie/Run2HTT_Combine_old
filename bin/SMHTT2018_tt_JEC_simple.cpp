//Andrew Loeliger
//Input options: 
// -s disables shape uncertainties
// -e disables embedded
// -b disables bin-by-bin uncertainties
#include <string>
#include <map>
#include <set>
#include <iostream>
#include <utility>
#include <vector>
#include <cstdlib>
#include "CombineHarvester/CombineTools/interface/CombineHarvester.h"
#include "CombineHarvester/CombineTools/interface/Observation.h"
#include "CombineHarvester/CombineTools/interface/Process.h"
#include "CombineHarvester/CombineTools/interface/Utilities.h"
#include "CombineHarvester/CombineTools/interface/Systematics.h"
#include "CombineHarvester/CombineTools/interface/BinByBin.h"
#include "CombineHarvester/Run2HTT_Combine/interface/InputParserUtility.h"

using namespace std;

int main(int argc, char **argv) {
  InputParserUtility Input(argc,argv);

  //! [part1]
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  cout<<"test"<<endl;
  string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/";
  
  //Dynamic Category Loading
  TFile* TheFile = new TFile((aux_shapes+"smh2018tt_jec.root").c_str());
  std::vector<std::pair<int,std::string>> cats = {};
  for(int i = 0; i < TheFile->GetListOfKeys()->GetEntries(); ++i)
    {
      std::cout<<"Making category for: "<<i<<" "<<TheFile->GetListOfKeys()->At(i)->GetName()<<std::endl;
      cats.push_back({i+1,TheFile->GetListOfKeys()->At(i)->GetName()});
    }
  TheFile->Close();

  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  vector<string> masses = {""};;
  //! [part3]
  cb.AddObservations({"*"}, {"smh2018"}, {"13TeV"}, {"tt"}, cats);

  vector<string> bkg_procs = {"ZT","VVT","TTT","jetFakes","ZL","VVL","TTL"};
  cb.AddProcesses({"*"}, {"smh2018"}, {"13TeV"}, {"tt"}, bkg_procs, cats, false);

  //for later!!!
//  vector<string> "ggH125" = {"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125",
//			     "ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_GE25_htt125",
//			     "ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_GE25_htt125",
//			     "ggH_PTH_0_200_GE2J_MJJ_350_700_PTHJJ_0_25_htt125",
//			     "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_120_200_htt125",
//			     "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_60_120_htt125",
//			     "ggH_PTH_0_200_GE2J_MJJ_0_350_PTH_0_60_htt125",
//			     "ggH_PTH_0_200_1J_PTH_120_200_htt125",
//			     "ggH_PTH_0_200_1J_PTH_60_120_htt125",
//			     "ggH_PTH_0_200_1J_PTH_0_60_htt125",
//			     "ggH_PTH_0_200_0J_PTH_10_200_htt125",
//			     "ggH_PTH_0_200_0J_PTH_0_10_htt125",
//			     "ggH_PTH_GE200_htt125"};
//  
//  vector<string> "qqH125" = {"qqH_0J_htt125",
//			     "qqH_1J_htt125",
//			     "qqH_GE2J_MJJ_0_60_htt125",
//			     "qqH_GE2J_MJJ_60_120_htt125",
//			     "qqH_GE2J_MJJ_120_350_htt125",
//			     "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125",
//			     "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125",
//			     "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125",
//			     "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125",
//			     "qqH_GE2J_MJJ_GE350_PTH_GE200_htt125"};

//  vector<string> sig_procs = ch::JoinStr({"ggH125","qqH125",{"ZH125","WH125"}});
  vector<string> sig_procs = {""ggH125"",""qqH125"","ZH125","WH125"};
  
  cb.AddProcesses(masses, {"smh2018"}, {"13TeV"}, {"tt"}, sig_procs, cats, true);    

  //! [part4]

  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;
  using ch::JoinStr;

  //start with lnN errors
  //********************************************************************************************************************************
  
  //What are these: Present in 18-032 Data cards.
  //cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));
  //cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
  //cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_THU", "lnN", SystMap<>::init(1.017));  

  // these 4 have been replaced with one overarching tau ID efficiency uncertainty
  //Quadrature addition of CMS_eff_mc_t and CMS_eff_mc_t_Run2017
  //cb.cp().process({"ZT","TTT","VVT","ZL","TTL","VVL","WH125","ZH125","ggH_htt125","qqH_htt125"}).AddSyst(cb,"CMS_eff_mc_t","lnN",SystMap<>::init(1.019));
  //Quadrature addition of CMS_eff_mc_t_tt and CMS_eff_mc_t_tt_Run2017
  //cb.cp().process({"ZT","TTT","VVT","ZL","TTL","VVL","WH125","ZH125","ggH_htt125","qqH_htt125"}).AddSyst(cb,"CMS_eff_mc_t_tt","lnN",SystMap<>::init(1.0084));
  //Quadrature addition of CMS_eff_t and CMS_eff_t_Run2017
  //cb.cp().process({"ZT","TTT","VVT","ZL","TTL","VVL","WH125","ZH125","ggH_htt125","qqH_htt125"}).AddSyst(cb,"CMS_eff_t","lnN",SystMap<>::init(1.019));
  //Quadrature addition of CMS_eff_t_tt and CMS_eff_t_tt_Run2017
  //cb.cp().process({"ZT","TTT","VVT","ZL","TTL","VVL","WH125","ZH125","ggH_htt125","qqH_htt125"}).AddSyst(cb,"CMS_eff_t_tt","lnN",SystMap<>::init(1.0084));
  
  //this is what it was replaced with
  //Tau ID uncertainty: applied to genuine tau contributions.
  //cb.cp().process(JoinStr({{"ZT","TTT","VVT"},sig_procs})).AddSyst(cb,"CMS_t_ID_eff","lnN",SystMap<>::init(1.02));

  //DiTau Tirgger Efficiency Uncertainty. Value taken from HIG-18-032.
  //cb.cp().process(JoinStr({{"ZL","ZT","TTL","TTT","VVL","VVT"},sig_procs})).AddSyst(cb,"CMS_eff_trigger_tt","lnN",SystMap<>::init(1.1));

  //lnN Fake Factor Uncertainties: Taken from HIG-18-032
  cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_norm_stat_tt_tt_noniso_Run2017","lnN",SystMap<>::init(1.029));
  cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_norm_syst_tt","lnN",SystMap<>::init(1.098));
  cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_sub_syst_tt_tt_noniso","lnN",SystMap<>::init(1.020));

  // Recoil Uncertainties: treated as lnN/shape? (changed to lnN) in this channel in HIG-18-032
  //cb.cp().process({"ZL","ZT"}).AddSyst(cb,"CMS_htt_boson_reso_met_Run2017", "lnN",ch::syst::SystMapAsymm<>::init(1.10803,0.902503));
  //cb.cp().process({"WH125"}).AddSyst(cb,"CMS_htt_boson_reso_met_Run2017", "lnN",ch::syst::SystMapAsymm<>::init(1.00355 ,0.996464));
  //cb.cp().process({"ZH125"}).AddSyst(cb,"CMS_htt_boson_reso_met_Run2017", "lnN",ch::syst::SystMapAsymm<>::init(1.00719,0.992859));
  //cb.cp().process("ggH125").AddSyst(cb,"CMS_htt_boson_reso_met_Run2017", "lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  //cb.cp().process("qqH125").AddSyst(cb,"CMS_htt_boson_reso_met_Run2017", "lnN",ch::syst::SystMapAsymm<>::init(1.03034,0.970553));

  //cb.cp().process({"ZL","ZT"}).AddSyst(cb,"CMS_htt_boson_scale_met_Run2017", "lnN",ch::syst::SystMapAsymm<>::init(0.883488,1.13188));  
  //cb.cp().process({"WH125"}).AddSyst(cb,"CMS_htt_boson_scale_met_Run2017", "lnN",ch::syst::SystMapAsymm<>::init(0.985035,1.01519));  
  //cb.cp().process({"ZH125"}).AddSyst(cb,"CMS_htt_boson_scale_met_Run2017", "lnN",ch::syst::SystMapAsymm<>::init(0.98243,1.01788));  
  //cb.cp().process("ggH125").AddSyst(cb,"CMS_htt_boson_scale_met_Run2017", "lnN",ch::syst::SystMapAsymm<>::init(0.970232,1.03068));  
  //cb.cp().process("qqH125").AddSyst(cb,"CMS_htt_boson_scale_met_Run2017", "lnN",ch::syst::SystMapAsymm<>::init(0.975431,1.02519));  
  

  // b-tagging efficiency: Changed into lnN.
  //5% in ttbar and 0.5% otherwise.
  //cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_htt_eff_b_TTL","lnN",SystMap<>::init(1.05));
  //cb.cp().process(JoinStr({{"ZT","VVT","ZL","VVL"},sig_procs})).AddSyst(cb,"CMS_htt_eff_b","lnN",SystMap<>::init(1.005));

  // TTbar XSection Uncertainty
  //cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_htt_tjXsec", "lnN", SystMap<>::init(1.06));

  // Diboson XSection Uncertainty
  //cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_htt_vvXsec", "lnN", SystMap<>::init(1.05));
  //DY XSection Uncertainty
  //cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_htt_zjXsec", "lnN", SystMap<>::init(1.04));

  //JES uncertainty: treated as lnN in this channel. Value taken from HIG-18-032
  //looping through the systematics 
  std::vector<std::string> jetSysVec = {"Closure", "AbsoluteFlavMap", "AbsoluteMPFBias", "AbsoluteScale", "AbsoluteStat", "FlavorQCD", "Fragmentation", "PileUpDataMC", "PileUpPtBB", "PileUpPtEC1", "PileUpPtEC2", "PileUpPtHF", "PileUpPtRef", "RelativeBal", "RelativeFSR", "RelativeJEREC1", "RelativeJEREC2", "RelativeJERHF", "RelativePtBB", "RelativePtEC1", "RelativePtEC2", "RelativePtHF", "RelativeStatEC", "RelativeStatFSR", "RelativeStatHF", "SinglePionECAL", "SinglePionHCAL", "TimePtEta", "Total"};
  //for smoothing later needs to be prefilled??? 
  if(addSmoothing>0){
    TFile *fin = new TFile(argv[1],"READ");
    TDirectory *cat  = (TDirectory*) fin->Get("tt_inc");
    TList *k = cat->GetListOfKeys(); 
    for(auto hist: *k){
        TH1F* h = (TH1F*) hist->GetObject();
        TString name = h->GetName(); 
         
        std::vector<std::pair<string,std::vector<float>>> downvect = {std::make_pair("ZT_CMS_scale_j_UP",1.12)};
        std::vector<std::pair<string,std::vector<float>>> upvect;
        }
  }
  else{
    std::vector<std::pair<string,std::vector<float>>> downvect = {std::make_pair("ZT_CMS_scale_j_UP",1.12)};
    std::vector<std::pair<string,std::vector<float>>> upvect;
  } 
  
  for(auto jetSys : jetSysVec){
    std::string newSelectionUp=inputSelections;
    std::string newSelectionDown=inputSelections;
    ReplaceStringInPlace(newSelectionUp,   "njets", "njet_"   +jetSys+"Up");
    ReplaceStringInPlace(newSelectionUp,   "mjj"  , "vbfMass_"+jetSys+"Up");
    ReplaceStringInPlace(newSelectionDown, "njets", "njet_"   +jetSys+"Down");
    ReplaceStringInPlace(newSelectionDown, "mjj"  , "vbfMass_"+jetSys+"Down");
    cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_scale_j_"+jetSys+"_13TeV","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
    cb.cp().process({"TTL","TTT"}).AddSyst(cb,"CMS_scale_j_"+jetSys+"_13TeV","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
    cb.cp().process({"VVL","VVT"}).AddSyst(cb,"CMS_scale_j_"+jetSys+"_13TeV","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
    cb.cp().process({"WHH125"}).AddSyst(cb,"CMS_scale_j_"+jetSys+"_13TeV","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
    cb.cp().process({"ZHH125"}).AddSyst(cb,"CMS_scale_j_"+jetSys+"_13TeV","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
    cb.cp().process("ggH125").AddSyst(cb,"CMS_scale_j_"+jetSys+"_13TeV","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
    cb.cp().process("qqH125").AddSyst(cb,"CMS_scale_j_"+jetSys+"_13TeV","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  }

  cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_scale_j_RelativeSample","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  cb.cp().process({"TTL","TTT"}).AddSyst(cb,"CMS_scale_j_RelativeSample","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  cb.cp().process({"VVL","VVT"}).AddSyst(cb,"CMS_scale_j_RelativeSample","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  cb.cp().process({"WH125"}).AddSyst(cb,"CMS_scale_j_RelativeSample","lnN",ch::syst::SystMapAsymm<>::init(1.00086,0.999141));
  cb.cp().process({"ZH125"}).AddSyst(cb,"CMS_scale_j_RelativeSample","lnN",ch::syst::SystMapAsymm<>::init(0.993051,1.007));
  cb.cp().process("ggH125").AddSyst(cb,"CMS_scale_j_RelativeSample","lnN",ch::syst::SystMapAsymm<>::init(0.998394,1.00161));
  cb.cp().process("qqH125").AddSyst(cb,"CMS_scale_j_RelativeSample","lnN",ch::syst::SystMapAsymm<>::init(0.980391,1.02));

  cb.cp().process({"ZL","ZT"}).AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  cb.cp().process({"TTL","TTT"}).AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.062,0.94));
  cb.cp().process({"VVL","VVT"}).AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.15,0.865));
  cb.cp().process({"WH125"}).AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.002,0.998));
  cb.cp().process({"ZH125"}).AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.01,0.99));
  cb.cp().process("ggH125").AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.0027,0.997));
  cb.cp().process("qqH125").AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.036,0.964));

  cb.cp().process({"ZL","ZT"}).AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  cb.cp().process({"TTL","TTT"}).AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.062,0.94));
  cb.cp().process({"VVL","VVT"}).AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.15,0.865));
  cb.cp().process({"WH125"}).AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.002,0.998));
  cb.cp().process({"ZH125"}).AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.01,0.99));
  cb.cp().process("ggH125").AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.0027,0.997));
  cb.cp().process("qqH125").AddSyst(cb,"CMS_scale_j_eta0to3","lnN",ch::syst::SystMapAsymm<>::init(1.036,0.964));

  cb.cp().process({"ZL","ZT"}).AddSyst(cb,"CMS_scale_j_eta0to5","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  cb.cp().process({"TTL","TTT"}).AddSyst(cb,"CMS_scale_j_eta0to5","lnN",ch::syst::SystMapAsymm<>::init(1.14,0.871));
  cb.cp().process({"VVL","VVT"}).AddSyst(cb,"CMS_scale_j_eta0to5","lnN",ch::syst::SystMapAsymm<>::init(1.058,0.944));
  cb.cp().process({"WH125"}).AddSyst(cb,"CMS_scale_j_eta0to5","lnN",ch::syst::SystMapAsymm<>::init(1.0032,0.997));
  cb.cp().process({"ZH125"}).AddSyst(cb,"CMS_scale_j_eta0to5","lnN",ch::syst::SystMapAsymm<>::init(1.0081,0.992));
  cb.cp().process("ggH125").AddSyst(cb,"CMS_scale_j_eta0to5","lnN",ch::syst::SystMapAsymm<>::init(1.0029,0.997));
  cb.cp().process("qqH125").AddSyst(cb,"CMS_scale_j_eta0to5","lnN",ch::syst::SystMapAsymm<>::init(1.037,0.964));

  cb.cp().process({"ZL","ZT"}).AddSyst(cb,"CMS_scale_j_eta3to5","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  cb.cp().process({"TTL","TTT"}).AddSyst(cb,"CMS_scale_j_eta3to5","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.043));
  cb.cp().process({"VVL","VVT"}).AddSyst(cb,"CMS_scale_j_eta3to5","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.035));
  cb.cp().process({"WH125"}).AddSyst(cb,"CMS_scale_j_eta3to5","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0035));
  cb.cp().process({"ZH125"}).AddSyst(cb,"CMS_scale_j_eta3to5","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.01));
  cb.cp().process("ggH125").AddSyst(cb,"CMS_scale_j_eta3to5","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0016));
  cb.cp().process("qqH125").AddSyst(cb,"CMS_scale_j_eta3to5","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.015));

  //??? Values taken from HIG 18-032
  //Quadrature addition of CMS_Scale_mc_t_1prong and CMS_Scale_mc_t_1prong_Run2018
  // some listed as shapes? on ggH. Not included.
  //cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN", ch::syst::SystMapAsymm<>::init(0.959,1.043));
  //cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN",ch::syst::SystMapAsymm<>::init(0.958,1.043));
  //cb.cp().process({"WH125"}).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN",ch::syst::SystMapAsymm<>::init(0.983,1.0173));
  //cb.cp().process({"ZH125"}).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN",ch::syst::SystMapAsymm<>::init(0.995,1.0049));
  //cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN",ch::syst::SystMapAsymm<>::init(0.9996,1.0004));
  //cb.cp().process("qqH125").AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN",ch::syst::SystMapAsymm<>::init(0.964,1.0004));

  //Quadrature addition of CMS_scale_mc_t_1prong1pizero and CMS_scale_mc_t_1prong1pizero_Run2018
  //cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  //cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  //cb.cp().process({"WH125"}).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.991,1.0088));
  //cb.cp().process({"ZH125"}).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.986,1.014));
  //cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.9999,1.0001));
  //cb.cp().process("ggH125").AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.978,1.022));
  //cb.cp().process("qqH125").AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.967,1.0336));
  
  //Quadrature addition of CMS_scale_mc_t_3prong and CMS_Scale_mc_t_3prong_Run2018
  //cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  //cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  //cb.cp().process({"WH125"}).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.991,1.009));
  //cb.cp().process({"ZH125"}).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.986,1.0141));
  //cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.9999,1.0001));
  //cb.cp().process("ggH125").AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.978,1.0224));
  //cb.cp().process("qqH125").AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.967,1.034));

  ////cb.cp().process({"VVL","TTL"}).AddSyst(cb,"CMS_scale_met_unclustered", "shape", SystMap<>::init(1.00));
  //cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_scale_met_unclustered","lnN",ch::syst::SystMapAsymm<>::init(1.0,1.0));
  //cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_scale_met_unclustered","lnN",ch::syst::SystMapAsymm<>::init(0.978039,1.02245));
  //cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_scale_met_unclustered","lnN",ch::syst::SystMapAsymm<>::init(0.927533,1.07813));

  //TES treated as shape? in this channel?
  //HIG-18-032 Datacards have:
  //CMS_scale_mc_t_1prong: shape?, All but ZL (ZT)
  //CMS_scale_mc_t_1prong1pizero: shape?, All but ZL (ZT)
  //CMS_scale_mc_t_3prong: shape?, All but ZL (ZT)

  //??? Value taken from HIG-18-032
  cb.cp().process({"WH125"}).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.008));
  cb.cp().process({"ZH125"}).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.009));
  cb.cp().process("qqH125").AddSyst(cb, "QCDScale_qqH", "lnN", SystMap<>::init(1.005));

  //Luminosity Uncertainty: Value taken from HIG-18-032
  cb.cp().process(JoinStr({sig_procs,{"VVL","ZL","TTL"}})).AddSyst(cb, "lumi_Run2018", "lnN", SystMap<>::init(1.023));

  //??? present in HIG 18-032
  cb.cp().process({"WH125"}).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.018));
  cb.cp().process({"ZH125"}).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.013));
  cb.cp().process("ggH125").AddSyst(cb, "pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
  cb.cp().process("qqH125").AddSyst(cb, "pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));  
  //********************************************************************************************************************************

  //shape uncertainties
  //********************************************************************************************************************************
  if(not Input.OptionExists("-s"))
    {
      std::cout<<"Attempting to make shapes in tt channel 2018, but shapes is not implemented yet! Implement me!"<<std::endl;
    }
  //********************************************************************************************************************************


  //embedded uncertainties. No embedded avaialable for 2018 yet.
  //********************************************************************************************************************************
  if(not Input.OptionExists("-e"))
    {
      std::cout<<"Attempting to make embedded uncertainties in tt channel 2018, but embedded uncertainties not implemented yet! Implement me!"<<std::endl;
    }
  //********************************************************************************************************************************                          

  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + "smh2018tt.root",
      "$BIN/$PROCESS",
      "$BIN/$PROCESS_$SYSTEMATIC");
  cb.cp().signals().ExtractShapes(
      aux_shapes + "smh2018tt.root",
      "$BIN/$PROCESS$MASS",
      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
  //! [part7]

  //! [part8]

  //Commented out for speed.
  if (not Input.OptionExists("-b"))
    {
      auto bbb = ch::BinByBinFactory()
	.SetAddThreshold(0.05)
	.SetMergeThreshold(0.5)
	.SetFixNorm(false);
      bbb.MergeBinErrors(cb.cp().backgrounds());
      bbb.AddBinByBin(cb.cp().backgrounds(), cb);
      bbb.AddBinByBin(cb.cp().signals(), cb);
    }  

  /*auto bbb = ch::BinByBinFactory()
    .SetAddThreshold(0.0)
    .SetFixNorm(false);

  //bbb.AddBinByBin(cb.cp().backgrounds(), cb);
  bbb.AddBinByBin(cb.cp().signals(), cb);
  bbb.AddBinByBin(cb.cp().process({"TT"}), cb);
  bbb.AddBinByBin(cb.cp().process({"QCD"}), cb);
  bbb.AddBinByBin(cb.cp().process({"W"}), cb);
  bbb.AddBinByBin(cb.cp().process({"VV"}), cb);
  bbb.AddBinByBin(cb.cp().process({"ZTT"}), cb);
  bbb.AddBinByBin(cb.cp().process({"ZLL"}), cb);
*/
  // This function modifies every entry to have a standardised bin name of
  // the form: {analysis}_{channel}_{bin_id}_{era}
  // which is commonly used in the htt analyses
  ch::SetStandardBinNames(cb);
  //! [part8]

  //! [part9]
  // First we generate a set of bin names:
  set<string> bins = cb.bin_set();
  // This method will produce a set of unique bin names by considering all
  // Observation, Process and Systematic entries in the CombineHarvester
  // instance.

  // We create the output root file that will contain all the shapes.
  TFile output("smh2018_tt.input.root", "RECREATE");

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  for (auto b : bins) {
    for (auto m : masses) {
      cout << ">> Writing datacard for bin: " << b << " and mass: " << m
           << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must remember to include the "*" mass entry to get
      // all the data and backgrounds.
      cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(
          b + "_" + m + ".txt", output);
    }
  }
  //! [part9]

}
