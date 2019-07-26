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
			 float Value,
			 TFile* TheFile,
			 std::vector<std::string> Categories)
{
  //loop over all of the analysis categories
  for(auto CategoryIt = Categories.begin(); CategoryIt != Categories.end(); ++CategoryIt)
    {
      string DirectoryName = *CategoryIt;
      TDirectory* TheDirectory = (TDirectory*) TheFile->Get(DirectoryName.c_str());
      if(TheDirectory == NULL)
	{
	  std::cout<<"Bad Directory: "+DirectoryName<<std::endl;
	  throw;
	}
      for(std::vector<string>::iterator it = Distributions.begin(); it != Distributions.end(); ++it)
	{
          TH1F* NominalHisto = (TH1F*) TheDirectory->Get((*it).c_str());
          Float_t NominalIntegral = NominalHisto->Integral();
          TH1F* UpHisto;
          TH1F* DownHisto;
	  if (NominalHisto==NULL)
	    {
	      std::cout<<"Bad Histogram: "+*it<<std::endl;
	      throw;
	    }
          //now loop over all the uncertainties
          for(std::vector<string>::iterator Unc_it = Shapes.begin();Unc_it != Shapes.end(); ++Unc_it)
	    {
              UpHisto = (TH1F*) TheDirectory->Get((*it+"_"+*Unc_it+"Up").c_str());
              DownHisto = (TH1F*) TheDirectory->Get((*it+"_"+*Unc_it+"Down").c_str());
	      Float_t UpIntegral = 0.0;
	      Float_t DownIntegral = 0.0;	     
	      if(UpHisto==NULL)
		{
		  std::cout<<"Bad Up Histogram: "+(string)(*it+"_"+*Unc_it+"Up")<<std::endl;
		  std::cout<<"Directory: "+DirectoryName<<std::endl;

		  throw;
		}
	      if(DownHisto==NULL)
		{
		  std::cout<<"Bad Down Histogram: "+(string)(*it+"_"+*Unc_it+"Down")<<std::endl;
		  std::cout<<"Directory: "+DirectoryName<<std::endl;
		  throw;
		}
	      UpIntegral = UpHisto->Integral();
	      DownIntegral = DownHisto->Integral();
              if(NominalIntegral != 0.0 and UpIntegral != 0.0 and DownIntegral != 0.0)
		{
                  cb->cp().bin({TheDirectory->GetName()}).process({*it})
                    .AddSyst(*cb,*Unc_it,"shape",ch::syst::SystMap<>::init(Value));
                }
              else
		{
                  std::cout<<"Skipping Uncertainty:"<<*Unc_it<<" for "<<*it<<" in category: "<<DirectoryName<<std::endl;
                }
            }
        }
    }
}
