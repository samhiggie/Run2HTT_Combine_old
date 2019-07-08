#include "TROOT.h"
#include <string>
#include "CombineHarvester/Run2HTT_Combine/interface/InputParserUtility.h"

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
