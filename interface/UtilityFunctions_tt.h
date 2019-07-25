//Andrew Loeliger
//File just includes utility functions for use in data card production
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

using namespace std;

//Add a given vector of shapes to a given vector of distributions
//takes: a vector of strings for shape names
//a vector of strings for the distributions to add it to
//a pointer ot the combine harvester instance
//a pointer to the tfile that the distributions are in
void AddShapesIfNotEmpty(std::vector<string> Shapes,
			   std::vector<string> Distributions,
			   ch::CombineHarvester * cb,
			   TFile* TheFile)
{
  //loop over all of the analysis categories
  for(int i = 0; i<TheFile->GetListOfKeys()->GetEntries();++i)
    {
      string DirectoryName = TheFile->GetListOfKeys()->At(i)->GetName();
      cout << "*** " << DirectoryName << " ***" << endl;
      TDirectory* TheDirectory = (TDirectory*) TheFile->Get(DirectoryName.c_str());
      for(std::vector<string>::iterator it = Distributions.begin(); it != Distributions.end(); ++it)
	{
          TH1F* NominalHisto = (TH1F*) TheDirectory->Get((*it).c_str());
          Float_t NominalIntegral = NominalHisto->Integral();
          TH1F* UpHisto;
          TH1F* DownHisto;
	  Float_t UpIntegral=0.0, DownIntegral=0.0;
          //now loop over all the uncertainties
          for(std::vector<string>::iterator Unc_it = Shapes.begin();Unc_it != Shapes.end(); ++Unc_it)
	    {
	      TheDirectory->cd();
	      //shape histogram exist
	      //std::cout << "\n["+*it+"_"+*Unc_it+"Up]" << std::endl;
	      if (TheDirectory->Get((*it+"_"+*Unc_it+"Up").c_str()))
		{
		  UpHisto = (TH1F*) TheDirectory->Get((*it+"_"+*Unc_it+"Up").c_str());
		  DownHisto = (TH1F*) TheDirectory->Get((*it+"_"+*Unc_it+"Down").c_str());
		  UpIntegral = UpHisto->Integral();
		  DownIntegral = DownHisto->Integral();
		  if (UpIntegral != 0.0 && DownIntegral != 0.0) {
		    cb->cp().bin({TheDirectory->GetName()}).process({*it})
		      .AddSyst(*cb,*Unc_it,"shape",ch::syst::SystMap<>::init(1.00));
		    //std::cout<<"Adding Uncertainty:"<<*Unc_it<<" for "<<*it<<" in category: "<<DirectoryName<<std::endl;
		    std::cout << "\033[1;32m[ >>ADD<< ]\033[0m  "+*it+"_"+*Unc_it+"Up/Down" << std::endl;
		  }
                }
	      else if (( NominalIntegral == 0.0 || UpIntegral==0.0 || DownIntegral==0.0) && TheDirectory->Get((*it+"_"+*Unc_it+"Up").c_str()))	
		std::cout << "\033[1;33m[0Integral]\033[0m  "+*it+"_"+*Unc_it+"Up/Down\t\t" << NominalIntegral << "\t" << UpIntegral << "\t" << DownIntegral << "\t" << std::endl;
	      else std::cout << "\033[1;31m[Not Ready]\033[0m  "+*it+"_"+*Unc_it+"Up/Down\t\t" << NominalIntegral << std::endl;
            }
        }
    }
}
