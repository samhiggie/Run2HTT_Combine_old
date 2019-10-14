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
#include "CombineHarvester/Run2HTT_Combine/interface/UtilityFunctions.h"

using namespace std;

int main(int argc, char **argv) 
{
  InputParserUtility Input(argc,argv);
  
  //! [part1]
  // First define the location of the "auxiliaries" directory where we can
  // source the input files containing the datacard shapes
  cout<<"test"<<endl;
  string aux_shapes = string(getenv("CMSSW_BASE")) + "/src/auxiliaries/shapes/";

  //keep a handle on the file, we need it to check if shapes are empty.
  TFile* TheFile = new TFile((aux_shapes+"smh2017et.root").c_str());  
    
  //categories loaded from configurations
  std::vector<std::pair<int,std::string>> cats = {};
  std::vector<std::string> CategoryArgs = Input.GetAllArguments("--Categories");
  int CatNum=1;
  for (auto it = CategoryArgs.begin(); it != CategoryArgs.end(); ++it)
    {					       
      std::cout<<"Making category for: "<<CatNum<<" "<<*it<<std::endl;
      cats.push_back({CatNum,(std::string)*it});
      CatNum++;
    }  

  // Create an empty CombineHarvester instance that will hold all of the
  // datacard configuration and histograms etc.
  ch::CombineHarvester cb;
  // Uncomment this next line to see a *lot* of debug information
  // cb.SetVerbosity(3);

  vector<string> masses = {""};;
  //! [part3]
  cb.AddObservations({"*"}, {"smh2017"}, {"13TeV"}, {"et"}, cats);

  vector<string> bkg_procs = {"VVT","STT","TTT","jetFakes","DYL","VVL","STL","TTL"};
  if(Input.OptionExists("-e")) 
    {
      bkg_procs.push_back("DYT");
    }
  else bkg_procs.push_back("embedded");
  cb.AddProcesses({"*"}, {"smh2017"}, {"13TeV"}, {"et"}, bkg_procs, cats, false);

  vector<string> ggH_STXS;
  if (Input.OptionExists("-g")) ggH_STXS = {"ggH_htt125"};
  else ggH_STXS = {"ggH_PTH_0_200_GE2J_MJJ_GE700_PTHJJ_0_25_htt125",
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
  
  vector<string> qqH_STXS; 
  if(Input.OptionExists("-q")) qqH_STXS = {"qqH_htt125"};
  else qqH_STXS = {"qqH_0J_htt125",
		   "qqH_1J_htt125",
		   "qqH_GE2J_MJJ_0_60_htt125",
		   "qqH_GE2J_MJJ_60_120_htt125",
		   "qqH_GE2J_MJJ_120_350_htt125",
		   "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_0_25_htt125",
		   "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_350_700_PTHJJ_GE25_htt125",
		   "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_0_25_htt125",
		   "qqH_GE2J_MJJ_GE350_PTH_0_200_MJJ_GE700_PTHJJ_GE25_htt125",
		   "qqH_GE2J_MJJ_GE350_PTH_GE200_htt125"};

  vector<string> sig_procs = ch::JoinStr({ggH_STXS,qqH_STXS,{"WH_htt125","ZH_htt125"}});
  cb.AddProcesses(masses, {"smh2017"}, {"13TeV"}, {"et"}, sig_procs, cats, true);

  //! [part4]

  using ch::syst::SystMap;
  using ch::syst::era;
  using ch::syst::bin_id;
  using ch::syst::process;
  using ch::JoinStr;

  //start with lnN errors
  //********************************************************************************************************************************
  
  //Theory uncerts
  cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_PU_alphas", "lnN", SystMap<>::init(1.0062));
  cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_PU_mq", "lnN", SystMap<>::init(1.0099));
  cb.cp().process(sig_procs).AddSyst(cb, "BR_htt_THU", "lnN", SystMap<>::init(1.017));  
  
  //Ele ID efficiency 
  cb.cp().process(JoinStr({{"DYT","TTT","VVT","STT","DYL","TTL","VVL","STL"},sig_procs})).AddSyst(cb,"CMS_eff_e_2017","lnN",SystMap<>::init(1.02));

  // b-tagging efficiency: 5% in ttbar and 0.5% otherwise.
  cb.cp().process({"TTT","TTL","STL","STT"}).AddSyst(cb,"CMS_htt_eff_b_TT_2017","lnN",SystMap<>::init(1.05));
  cb.cp().process(JoinStr({{"DYT","VVT","DYL","VVL"},sig_procs})).AddSyst(cb,"CMS_htt_eff_b_2017","lnN",SystMap<>::init(1.005));

  // TTbar XSection Uncertainty
  cb.cp().process({"TTT","TTL"}).AddSyst(cb,"CMS_htt_tjXsec", "lnN", SystMap<>::init(1.042));
  // Diboson XSection Uncertainty
  cb.cp().process({"VVT","VVL"}).AddSyst(cb,"CMS_htt_vvXsec", "lnN", SystMap<>::init(1.05));
  // Single top XSection Uncertainty
  cb.cp().process({"STT","STL"}).AddSyst(cb,"CMS_htt_stXsec", "lnN", SystMap<>::init(1.05));
  //DY XSection Uncertainty
  cb.cp().process({"DYT","DYL"}).AddSyst(cb,"CMS_htt_zjXsec", "lnN", SystMap<>::init(1.02));
  //Muon Fake Rate Uncertainty
  cb.cp().process({"DYL"}).AddSyst(cb, "CMS_eFakeTau_2017", "lnN",SystMap<>::init(1.15));    

  //theory uncerts present in HIG-18-032  
  cb.cp().process({"WH_htt125"}).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.008));
  cb.cp().process({"ZH_htt125"}).AddSyst(cb, "QCDScale_VH", "lnN", SystMap<>::init(1.009));
  cb.cp().process(qqH_STXS).AddSyst(cb, "QCDScale_qqH", "lnN", SystMap<>::init(1.005));

  //Luminosity Uncertainty
  cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","DYL","DYT","TTL","TTT"}})).AddSyst(cb, "lumi_Run2017", "lnN", SystMap<>::init(1.020));
  cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","DYL","DYT","TTL","TTT"}})).AddSyst(cb, "lumi_XYfactorization", "lnN", SystMap<>::init(1.008));
  cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","DYL","DYT","TTL","TTT"}})).AddSyst(cb, "lumi_lengthScale", "lnN", SystMap<>::init(1.003));
  cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","DYL","DYT","TTL","TTT"}})).AddSyst(cb, "lumi_beamBeamDeflection", "lnN", SystMap<>::init(1.004));
  cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","DYL","DYT","TTL","TTT"}})).AddSyst(cb, "lumi_dynamicBeta", "lnN", SystMap<>::init(1.005));
  cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","DYL","DYT","TTL","TTT"}})).AddSyst(cb, "lumi_beamCurrentCalibration", "lnN", SystMap<>::init(1.003));
  cb.cp().process(JoinStr({sig_procs,{"VVL","VVT","STT","STL","DYL","DYT","TTL","TTT"}})).AddSyst(cb, "lumi_ghostsAndSatellites", "lnN", SystMap<>::init(1.001));

  //theory uncerts present in HIG-18-032
  cb.cp().process({"WH_htt125"}).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.018));
  cb.cp().process({"ZH_htt125"}).AddSyst(cb, "pdf_Higgs_VH", "lnN", SystMap<>::init(1.013));
  cb.cp().process(ggH_STXS).AddSyst(cb, "pdf_Higgs_gg", "lnN", SystMap<>::init(1.032));
  cb.cp().process(qqH_STXS).AddSyst(cb, "pdf_Higgs_qq", "lnN", SystMap<>::init(1.021));  
  //********************************************************************************************************************************  
    
  //shape uncertainties
  //********************************************************************************************************************************
  if(not Input.OptionExists("-s"))
    {
      //uses custom defined utility function that only adds the shape if at least one shape inside is not empty.
 
      // Prefiring
      AddShapesIfNotEmpty({"CMS_prefiring"},
                          JoinStr({sig_procs,{"VVL","VVT","STT","STL","DYL","DYT","TTL","TTT"}}),
                          &cb,
                          1.00,
                          TheFile,CategoryArgs);

      // Tau ID eff in pt bins
      std::cout<<"Tau ID eff"<<std::endl;
      AddShapesIfNotEmpty({"CMS_tauideff_pt30to35_2017","CMS_tauideff_pt35to40_2017","CMS_tauideff_ptgt40_2017"},
                          JoinStr({ggH_STXS,qqH_STXS,{"VVT","STT","DYT","TTT","WH_htt125","ZH_htt125"}}),
                          &cb,
                          1.00,
                          TheFile,CategoryArgs);

      // Trg eff. It is a shape because the 2 triggers affect the ele pT spectrum differently
      std::cout<<"Trigger eff"<<std::endl;
      AddShapesIfNotEmpty({"CMS_singleeletrg_2017","CMS_eletautrg_2017"},
                          JoinStr({ggH_STXS,qqH_STXS,{"VVT","STT","DYT","TTT","WH_htt125","ZH_htt125"}}),
                          &cb,
                          1.00,
                          TheFile,CategoryArgs);

      
      //Mu to tau fake energy scale and e to tau energy fake scale            
      std::cout<<"Adding Shapes..."<<std::endl;
      AddShapesIfNotEmpty({"CMS_scale_efaket_1prong_2017","CMS_scale_efaket_1prong1pizero_2017"},
			  {"DYL"},
			  &cb,
			  1.00,
			  TheFile,CategoryArgs);

      AddShapesIfNotEmpty({"CMS_rawFF_et_qcd_0jet_unc1_2017","CMS_rawFF_et_qcd_0jet_unc2_2017","CMS_rawFF_et_qcd_1jet_unc1_2017","CMS_rawFF_et_qcd_1jet_unc2_2017","CMS_rawFF_et_w_0jet_unc1_2017","CMS_rawFF_et_w_0jet_unc2_2017","CMS_rawFF_et_w_1jet_unc1_2017","CMS_rawFF_et_w_1jet_unc2_2017","CMS_rawFF_et_tt_unc1_2017","CMS_rawFF_et_tt_unc2_2017","CMS_FF_closure_mvis_et_qcd_unc1_2017","CMS_FF_closure_mvis_et_qcd_unc2_2017","CMS_FF_closure_mvis_et_w_unc1_2017","CMS_FF_closure_mvis_et_w_unc2_2017","CMS_FF_closure_mvis_et_tt_unc1_2017","CMS_FF_closure_mvis_et_tt_unc2_2017","CMS_FF_closure_OSSS_mvis_et_qcd_unc1_2017","CMS_FF_closure_OSSS_mvis_et_qcd_unc2_2017","CMS_FF_closure_mt_et_w_unc1_2017","CMS_FF_closure_mt_et_w_unc2_2017"},
                          {"jetFakes"},
                          &cb,
                          1.00,
                          TheFile,CategoryArgs);
      
      //MET Unclustered Energy Scale      
      AddShapesIfNotEmpty({"CMS_scale_met_unclustered_2017"},
			  {"TTT","TTL","VVT","STT","VVL","STL"},
			  &cb,
			  1.00,
			  TheFile,CategoryArgs);

      //Recoil Shapes:                  
      //check which signal processes this should be applied to. If any.
      AddShapesIfNotEmpty({"CMS_htt_boson_reso_met_0jet_2017","CMS_htt_boson_scale_met_0jet_2017",
	    "CMS_htt_boson_reso_met_1jet_2017","CMS_htt_boson_scale_met_1jet_2017",
	    "CMS_htt_boson_reso_met_2jet_2017","CMS_htt_boson_scale_met_2jet_2017"},
	JoinStr({ggH_STXS,qqH_STXS,{"DYT","DYL"}}),
	&cb,
	1.00,
	TheFile,CategoryArgs);

      //ZPT Reweighting Shapes:      
      AddShapesIfNotEmpty({"CMS_htt_dyShape"},
			  {"DYT","DYL"},
			  &cb,
			  1.00,
			  TheFile,CategoryArgs);

      //Top Pt Reweighting      
      AddShapesIfNotEmpty({"CMS_htt_ttbarShape"},
			  {"TTL","TTT"},
			  &cb,
			  1.00,
			  TheFile,CategoryArgs);
  
      //TES Uncertainty                  
      AddShapesIfNotEmpty({"CMS_scale_t_1prong_2017","CMS_scale_t_3prong_2017","CMS_scale_t_1prong1pizero_2017"},
			  JoinStr({ggH_STXS,qqH_STXS,{"VVT","STT","DYT","TTT","WH_htt125","ZH_htt125"}}),
			  &cb,
			  1.00,
			  TheFile,CategoryArgs);

      // Jet Energy Scale Uncertainties            
      AddShapesIfNotEmpty({"CMS_JetRelativeBal_2017"},
	JoinStr({ggH_STXS,qqH_STXS,{"DYT","WH_htt125","ZH_htt125","VVL","STL","DYL","TTL","VVT","STT"}}),
	&cb,
	0.707,
	TheFile,CategoryArgs);
      /*AddShapesIfNotEmpty({"CMS_JetRelativeBal"},
	JoinStr({ggH_STXS,qqH_STXS,{"DYT","WH_htt125","ZH_htt125","VVL","STL","DYL","TTL","VVT","STT"}}),
	&cb,
	0.707,
	TheFile,CategoryArgs);*/
      AddShapesIfNotEmpty({"CMS_JetEta3to5_2017","CMS_JetEta0to5_2017",
	    "CMS_JetEta0to3_2017","CMS_JetRelativeSample_2017","CMS_JetEC2_2017"},
	JoinStr({ggH_STXS,qqH_STXS,{"DYT","WH_htt125","ZH_htt125","VVL","STL","DYL","TTL","VVT","STT"}}),
	&cb,
	1.00,
	TheFile,CategoryArgs);            

      //ggH Theory Uncertainties
      AddShapesIfNotEmpty({"THU_ggH_Mu","THU_ggH_Res","THU_ggH_Mig01","THU_ggH_Mig12","THU_ggH_VBF2j",
	    "THU_ggH_VBF3j","THU_ggH_qmtop","THU_ggH_PT60","THU_ggH_PT120"},
	ggH_STXS,
	&cb,
	1.00,
	TheFile,CategoryArgs);            

      //Muon Energy scale uncertainties
      AddShapesIfNotEmpty({"CMS_smear_e_2017","CMS_scale_e_2017"},
	JoinStr({ggH_STXS,qqH_STXS,{"DYT","VVT","STT","TTT","DYL","VVL","STL","TTL","WH_htt125","ZH_htt125"}}),
	&cb,
	1.00,
	TheFile,CategoryArgs);
    }
  //********************************************************************************************************************************

  //embedded uncertainties. No embedded avaialable for 2017 yet.
  //********************************************************************************************************************************
  if(not Input.OptionExists("-e"))
    {      
     
      //50% correlation with ID unc in MC
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_e_2017","lnN",SystMap<>::init(1.010));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_e_embedded_2017","lnN",SystMap<>::init(1.01732));

      //Tau ID eff
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_t_embedded_2017", "lnN", SystMap<>::init(1.020));
 
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_htt_doublemutrg", "lnN", SystMap<>::init(1.04));

      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_1ProngPi0Eff","lnN",ch::syst::SystMapAsymm<>::init(0.9934,1.011));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_3ProngEff","lnN",ch::syst::SystMapAsymm<>::init(0.969,1.005));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_eff_emb_m","lnN",SystMap<>::init(1.014));
      
      //ttbar contamination in embedded
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_htt_emb_ttbar_2017", "shape", SystMap<>::init(1.00));    

      //TES uncertainty
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_1prong_2017", "shape", SystMap<>::init(1.00));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_1prong1pizero_2017", "shape", SystMap<>::init(1.00));
      cb.cp().process({"embedded"}).AddSyst(cb,"CMS_scale_emb_t_3prong_2017", "shape", SystMap<>::init(1.00));
    }

  //********************************************************************************************************************************                          

  cb.cp().backgrounds().ExtractShapes(
      aux_shapes + "smh2017et.root",
      "$BIN/$PROCESS",
      "$BIN/$PROCESS_$SYSTEMATIC");
  cb.cp().signals().ExtractShapes(
      aux_shapes + "smh2017et.root",
      "$BIN/$PROCESS$MASS",
      "$BIN/$PROCESS$MASS_$SYSTEMATIC");
  //! [part7]

  //! [part8]
  
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
  bbb.AddBinByBin(cb.cp().process({"DYTT"}), cb);
  bbb.AddBinByBin(cb.cp().process({"DYLL"}), cb);
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
  TFile output((Input.ReturnToken(0)+"/"+"smh2017_et.input.root").c_str(), "RECREATE");

  // Finally we iterate through each bin,mass combination and write a
  // datacard.
  for (auto b : bins) {
    for (auto m : masses) {
      cout << ">> Writing datacard for bin: " << b << " and mass: " << m
           << "\n";
      // We need to filter on both the mass and the mass hypothesis,
      // where we must remember to include the "*" mass entry to get
      // all the data and backgrounds.
      cb.cp().bin({b}).mass({m, "*"}).WriteDatacard(Input.ReturnToken(0)+"/"+b + "_" + m + ".txt", output);
    }
  }
  //! [part9]

}
