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
  return std::find(this->tokens.begin(),this->tokens.end(), Option) != this->tokens.end();
}
