#include "TROOT.h"
#include <string>
#include <vector>

class InputParserUtility
{
 private:  
  std::vector <std::string> tokens;
  
 public: 
  InputParserUtility(int &argc, char **argv);
  bool OptionExists(const std::string &Option);
  std::string ReturnToken(int TokenNum);
  std::vector<std::string> GetAllArguments(const std::string &Option);
};
