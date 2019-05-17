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
  TFile* TheFile = new TFile((aux_shapes+"smh2018mt.root").c_str());
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
  cb.AddObservations({"*"}, {"smh2018"}, {"13TeV"}, {"mt"}, cats);

  vector<string> bkg_procs = {"ZT","VVT","TTT","jetFakes","ZL","VVL","TTL"};
  cb.AddProcesses({"*"}, {"smh2018"}, {"13TeV"}, {"mt"}, bkg_procs, cats, false);

  vector<string> ggH_STXS = {"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125",
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
			     "ggH_PTH_GE200_htt125"};
  
  vector<string> qqH_STXS = {"qqH_0J_htt125",
			     "qqH_1J_htt125",
			     "qqH_GE2J_MJJ_0_60_htt125",
			     "qqH_GE2J_MJJ_60_120_htt125",
			     "qqH_GE2J_MJJ_120_350_htt125",
			     "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125",
			     "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125",
			     "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125",
			     "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125",
			     "qqH_GE2J_MJJ_GE350_PTH_GE200_htt125"};

  vector<string> sig_procs = ch::JoinStr({ggH_STXS,qqH_STXS,{"ZH_htt125","WH_htt125"}});
  
  cb.AddProcesses(masses, {"smh2018"}, {"13TeV"}, {"mt"}, sig_procs, cats, true);    

  //! [part4]

  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;
  using ch::JoinStr;

  //start with lnN errors
  //********************************************************************************************************************************
  
  //What are these: Present in 18-032 Data cards.
  cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));
  cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
  cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_THU", "lnN", SystMap<>::init(1.017));  

  // these 4 have been replaced with one overarching tau ID efficiency uncertainty
  //Quadrature addition of CMS_eff_mc__t and CMS_eff_mc_t_Run2017
  //cb.cp().process({"ZT","TTT","VVT","ZL","TTL","VVL","WH_htt125","ZH_htt125","ggH_htt125","qqH_htt125"}).AddSyst(cb,"CMS_eff_mc_t","lnN",SystMap<>::init(1.019));
  //Quadrature addition of CMS_eff_mc_t_mt and CMS_eff_mc_t_mt_Run2017
  //cb.cp().process({"ZT","TTT","VVT","ZL","TTL","VVL","WH_htt125","ZH_htt125","ggH_htt125","qqH_htt125"}).AddSyst(cb,"CMS_eff_mc_t_mt","lnN",SystMap<>::init(1.0084));
  //Quadrature addition of CMS_eff_t and CMS_eff_t_Run2017
  //cb.cp().process({"ZT","TTT","VVT","ZL","TTL","VVL","WH_htt125","ZH_htt125","ggH_htt125","qqH_htt125"}).AddSyst(cb,"CMS_eff_t","lnN",SystMap<>::init(1.019));
  //Quadrature addition of CMS_eff_tmt and CMS_eff_t_mt_Run2017
  //cb.cp().process({"ZT","TTT","VVT","ZL","TTL","VVL","WH_htt125","ZH_htt125","ggH_htt125","qqH_htt125"}).AddSyst(cb,"CMS_eff_t_mt","lnN",SystMap<>::init(1.0084));
  
  //this is what it was replaced with
  //Tau ID uncertainty: applied to genuine tau contributions.
  cb.cp().process(JoinStr({{"ZT","TTT","VVT"},sig_procs})).AddSyst(cb,"CMS_t_ID_eff","lnN",SystMap<>::init(1.02));

  //Muon ID efficiency: Decorollated in 18-032 datacards.
  cb.cp().process(JoinStr({{"ZT","TTT","VVT","ZL","TTL","VVL"},sig_procs})).AddSyst(cb,"CMS_eff_m","lnN",SystMap<>::init(1.014));
  cb.cp().process(JoinStr({{"ZT","TTT","VVT","ZL","TTL","VVL"},sig_procs})).AddSyst(cb,"CMS_eff_mc_m","lnN",SystMap<>::init(1.014));

  //lnN Fake Factor Uncertainties: Values from 18-032 data cards.
  cb.cp().process({"jetFakes"}).AddSyst(cb, "CMS_ff_norm_stat_mt_mt_qqh_unrolled_Run2018","lnN",SystMap<>::init(1.048));
  //Quadrature addition of CMS_ff_norm_syst_mt and CMS_ff_norm_syst_mt_Run2018
  cb.cp().process({"jetFakes"}).AddSyst(cb, "CMS_ff_norm_syst_mt","lnN",SystMap<>::init(1.058));
  //Quadrature addition of CMS_ff_sub_syst_mt_mt_qqh_unrolled and CMS_ff_sub_syst_mt_mt_qqh_unrolled_Run2018
  cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_sub_syst_mt_mt_qqh_unrolled", "lnN",SystMap<>::init(1.04));

  // b-tagging efficiency: Changed into lnN.
  //5% in ttbar and 0.5% otherwise.
  cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_htt_eff_b_TTL","lnN",SystMap<>::init(1.05));
  cb.cp().process(JoinStr({{"ZT","VVT","ZL","VVL"},sig_procs})).AddSyst(cb,"CMS_htt_eff_b","lnN",SystMap<>::init(1.005));

  // TTbar XSection Uncertainty
  cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_htt_tjXsec", "lnN", SystMap<>::init(1.06));

  // Diboson XSection Uncertainty
  cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_htt_vvXsec", "lnN", SystMap<>::init(1.05));
  //DY XSection Uncertainty
  cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_htt_zjXsec", "lnN", SystMap<>::init(1.04));
  //Muon Fake Rate Uncertainty
  cb.cp().process({"ZL"}).AddSyst(cb, "CMS_mFakeTau", "lnN",SystMap<>::init(1.26));

  //Quadrature addition of CMS_Scale_mc_t_1prong and CMS_Scale_mc_t_1prong_Run2018
  cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN", ch::syst::SystMapAsymm<>::init(0.99349,1.00655));
  cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN",ch::syst::SystMapAsymm<>::init(0.9779,1.02244));
  cb.cp().process({"WH_htt125"}).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN",ch::syst::SystMapAsymm<>::init(0.99758,1.00242));
  cb.cp().process({"ZH_htt125"}).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN",ch::syst::SystMapAsymm<>::init(0.9922,1.00785));
  cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN",ch::syst::SystMapAsymm<>::init(0.99717,1.00283));
  cb.cp().process(ggH_STXS).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN",ch::syst::SystMapAsymm<>::init(0.99339,1.00665));
  cb.cp().process(qqH_STXS).AddSyst(cb,"CMS_Scale_mc_t_1prong","lnN",ch::syst::SystMapAsymm<>::init(0.99602,1.004));

  //Quadrature addition of CMS_scale_mc_t_1prong1pizero and CMS_scale_mc_t_1prong1pizero_Run2018
  cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.985821,1.014325));
  cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.997992,1.014325));
  cb.cp().process({"WH_htt125"}).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.99655,1.00345));
  cb.cp().process({"ZH_htt125"}).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.99238,1.00767));
  cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.991626,1.00843));
  cb.cp().process(ggH_STXS).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.99259,1.00744));
  cb.cp().process(qqH_STXS).AddSyst(cb,"CMS_scale_mc_t_1prongpizero","lnN",ch::syst::SystMapAsymm<>::init(0.9941,1.00594));
  
  //Quadrature addition of CMS_scale_mc_t_3prong and CMS_Scale_mc_t_3prong_Run2018
  cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.996,1.004));
  cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.994713,1.0053));
  cb.cp().process({"WH_htt125"}).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.9947,1.0053));
  cb.cp().process({"ZH_htt125"}).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.9945,1.00549));
  cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.9966,1.0034));
  cb.cp().process(ggH_STXS).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.997,1.0029));
  cb.cp().process(qqH_STXS).AddSyst(cb,"CMS_scale_mc_t_3prong","lnN",ch::syst::SystMapAsymm<>::init(0.9972,1.00283));

  ////cb.cp().process({"VVL","TTL"}).AddSyst(cb,"CMS_scale_met_unclustered", "shape", SystMap<>::init(1.00));
  cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_scale_met_unclustered","lnN",ch::syst::SystMapAsymm<>::init(0.999559,1.00044));
  cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_scale_met_unclustered","lnN",ch::syst::SystMapAsymm<>::init(0.983288,1.017));
  cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_scale_met_unclustered","lnN",ch::syst::SystMapAsymm<>::init(0.976299,1.02428));
  
  cb.cp().process({"WH_htt125"}).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.008));
  cb.cp().process({"ZH_htt125"}).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.009));
  cb.cp().process(qqH_STXS).AddSyst(cb, "QCDScale_qqH", "lnN", SystMap<>::init(1.005));

  //Luminosity Uncertainty
  cb.cp().process(JoinStr({sig_procs,{"VVL","ZL","TTL"}})).AddSyst(cb, "lumi_Run2018", "lnN", SystMap<>::init(1.023));

  //??? present in HIG 18-032
  cb.cp().process({"WH_htt125"}).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.018));
  cb.cp().process({"ZH_htt125"}).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.013));
  cb.cp().process(ggH_STXS).AddSyst(cb, "pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
  cb.cp().process(qqH_STXS).AddSyst(cb, "pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));  
  //********************************************************************************************************************************

  //shape uncertainties
  //********************************************************************************************************************************
  if(not Input.OptionExists("-s"))
    {
      cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_ZLShape_mt_1prong_Run2018","shape",SystMap<>::init(1.00));
      cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_ZLShape_mt_1prong1pizero_Run2018","shape",SystMap<>::init(1.00));      
      
      //Fake factor shapes: taken from 18-032 data cards.
      cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_qcd_mt_syst", "shape", SystMap<>::init(1.00));
      cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_qcd_njet0_mt_stat", "shape", SystMap<>::init(1.00));
      cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_qcd_njet1_mt_stat", "shape", SystMap<>::init(1.00));  
      cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_tt_njet1_stat","shape",SystMap<>::init(1.00));
      cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_tt_syst","shape",SystMap<>::init(1.00));
      cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_w_njet0_mt_stat","shape",SystMap<>::init(1.00));
      cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_w_njet1_mt_stat","shape",SystMap<>::init(1.00));
      cb.cp().process({"jetFakes"}).AddSyst(cb,"CMS_ff_w_syst","shape",SystMap<>::init(1.00));  

      //Recoil Shapes:
      cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_htt_boson_reso_met", "shape", SystMap<>::init(1.00));
      cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_htt_boson_scale_met", "shape", SystMap<>::init(1.00));  

      //ZPT Reweighting Shapes:
      cb.cp().process({"ZT","ZL"}).AddSyst(cb,"CMS_htt_dyShape", "shape", SystMap<>::init(1.00));

      //Top Pt Reweighting
      cb.cp().process({"TTL"}).AddSyst(cb,"CMS_htt_ttbarShape", "shape", SystMap<>::init(1.00));
  
      //TES Uncertainty
      cb.cp().process({"ZT","ggH_htt125","qqH_htt125","WH_htt125","ZH_htt125","VVL","ZL","TTL"}).AddSyst(cb,"CMS_scale_t_1prong", "shape", SystMap<>::init(1.00));
      cb.cp().process({"ZT","ggH_htt125","qqH_htt125","WH_htt125","ZH_htt125","VVL","ZL","TTL"}).AddSyst(cb,"CMS_scale_t_3prong", "shape", SystMap<>::init(1.00));
      cb.cp().process({"ZT","ggH_htt125","qqH_htt125","WH_htt125","ZH_htt125","VVL","ZL","TTL"}).AddSyst(cb,"CMS_scale_t_1prong1pizero", "shape", SystMap<>::init(1.00));

      // Jet Energy Scale Uncertainties
      cb.cp().process(JoinStr({sig_procs, {"ZT","ggH_htt125","qqH_htt125","WH_htt125","ZH_htt125","VVL","ZL","TTL"}})).AddSyst(cb,"CMS_JetRelativeBal", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({sig_procs, {"ZT","ggH_htt125","qqH_htt125","WH_htt125","ZH_htt125","VVL","ZL","TTL"}})).AddSyst(cb,"CMS_JetEta3to5", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({sig_procs, {"ZT","ggH_htt125","qqH_htt125","WH_htt125","ZH_htt125","VVL","ZL","TTL"}})).AddSyst(cb,"CMS_JetEta0to5", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({sig_procs, {"ZT","ggH_htt125","qqH_htt125","WH_htt125","ZH_htt125","VVL","ZL","TTL"}})).AddSyst(cb,"CMS_JetEta0to3", "shape", SystMap<>::init(1.00));
      cb.cp().process(JoinStr({sig_procs, {"ZT","ggH_htt125","qqH_htt125","WH_htt125","ZH_htt125","VVL","ZL","TTL"}})).AddSyst(cb,"CMS_JetRelativeSample", "shape", SystMap<>::init(1.00));

      //ggH theory uncertainties
      cb.cp().process({"ggH_htt125"}).AddSyst(cb,"THU_ggH_Mu", "shape", SystMap<>::init(1.00));
      cb.cp().process({"ggH_htt125"}).AddSyst(cb,"THU_ggH_Res", "shape", SystMap<>::init(1.00));
      cb.cp().process({"ggH_htt125"}).AddSyst(cb,"THU_ggH_Mig01", "shape", SystMap<>::init(1.00));
      cb.cp().process({"ggH_htt125"}).AddSyst(cb,"THU_ggH_Mig12", "shape", SystMap<>::init(1.00));
      cb.cp().process({"ggH_htt125"}).AddSyst(cb,"THU_ggH_VBF2j", "shape", SystMap<>::init(1.00));
      cb.cp().process({"ggH_htt125"}).AddSyst(cb,"THU_ggH_VBF3j", "shape", SystMap<>::init(1.00));
      cb.cp().process({"ggH_htt125"}).AddSyst(cb,"THU_ggH_qmtop", "shape", SystMap<>::init(1.00));
      cb.cp().process({"ggH_htt125"}).AddSyst(cb,"THU_ggH_PT60", "shape", SystMap<>::init(1.00));
      cb.cp().process({"ggH_htt125"}).AddSyst(cb,"THU_ggH_PT120", "shape", SystMap<>::init(1.00));
    }
  //********************************************************************************************************************************


  //embedded uncertainties. No embedded avaialable for 2018 yet.
  //********************************************************************************************************************************
  if(not Input.OptionExists("-e"))
    {
      //Quadrature addition of CMS_eff_emb_t and CMS_eff_emb_t_Run2018
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_emb_t", "lnN", SystMap<>::init(1.019));
  
      //Quadrature addition of CMS_eff_emb_t_mt and CMS_eff_emt_t_mt_Run2018
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_emb_t_mt","lnN",SystMap<>::init(1.0084));

      //These were changed from shapes to lnN
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_1ProngPi0Eff","lnN",ch::syst::SystMapAsymm<>::init(0.9934,1.011));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_3ProngEff","lnN",ch::syst::SystMapAsymm<>::init(0.969,1.005));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_emb_m","lnN",SystMap<>::init(1.014));

      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_htt_doublemutrg", "lnN", SystMap<>::init(1.04));

      // TTBar Contamination
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_htt_emb_ttbar", "shape", SystMap<>::init(1.00));

      //TES uncertainty
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_1prong", "shape", SystMap<>::init(1.00));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_1prong1pizero", "shape", SystMap<>::init(1.00));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_3prong", "shape", SystMap<>::init(1.00));
    }
  //********************************************************************************************************************************                          

  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + "smh2018mt.root",
      "$BIN/$PROCESS",
      "$BIN/$PROCESS_$SYSTEMATIC");
  cb.cp().signals().ExtractShapes(
      aux_shapes + "smh2018mt.root",
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
  TFile output("smh2018_mt.input.root", "RECREATE");

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
