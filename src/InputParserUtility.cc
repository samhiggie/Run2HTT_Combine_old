#include "TROOT.h"
#include <string>
#include "CombineHarvester/Run2HTT_Combine/interface/InputParserUtility.h"
#include <iostream>

InputParserUtility::InputParserUtility(int &argc, char **argv)
{
  for(int i=1; i < argc; ++i)
    {
      this->tokens.push_back(std::string(argv[i]));
    }
}

bool InputParserUtility::OptionExists(const std::string &Option)
{
  for(auto it = this->tokens.begin(); it != this->tokens.end(); ++it)
    {
      if(*it == Option) return true;
    }
  return false;  
}

std::string InputParserUtility::ReturnToken(int TokenNum)
{
  return this->tokens[TokenNum];
}

std::vector<std::string> InputParserUtility::GetAllArguments(const std::string &Option)
{
  std::vector<std::string> Arguments = {};
  for(auto it = this->tokens.begin(); it != this->tokens.end(); ++it)
    {      
      if(*it == Option)
	{	  
	  for (auto argit = it+1; argit != tokens.end() && ((std::string) *argit).front() != '-'; ++argit)
	    {	      
	      Arguments.push_back(*argit);
	    }
	}
    }
  return Arguments;
}
