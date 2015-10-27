#include <iostream>
#include <boost/program_options.hpp>
#include <vector>
#include <string>
#include "TFile.h"
#include "TString.h"
#include "TH1D.h"
#include "PlotFunctions/SideFunctions.h"


using std::string;
using std::cout;
using std::endl;
using std::vector;
namespace po = boost::program_options;

void Style_Christophe();

int main( int argc, char* argv[] ) {
  po::options_description desc("LikelihoodProfiel Usage");

  //define all options in the program
  desc.add_options()
    ("help", "Display this help message")
    ;
  // create a map vm that contains options and all arguments of options       
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv).options(desc).style(po::command_line_style::unix_style ^ po::command_line_style::allow_short).run(), vm);
  po::notify(vm);
  
  if (vm.count("help")) {cout << desc; return 0;}
  //########################################
  //  Style_Christophe();
  string outFileName = "/sps/atlas/c/cgoudet/Calibration/ScaleResults/280614/24Bins/EnergyScaleFactors.root";
  DiffSystematics( "/afs/in2p3.fr/home/c/cgoudet/private/Codes/Template/Input/systematics_alpha.txt", outFileName, "totSyst_alpha", 0 );
  DiffSystematics( "/afs/in2p3.fr/home/c/cgoudet/private/Codes/Template/Input/systematics_c.txt", outFileName, "totSyst_c", 1 );

  VarOverTime( "/afs/in2p3.fr/home/c/cgoudet/private/Codes/Template/Input/ScalesOverTime_alpha.txt", outFileName, 1);
  VarOverTime( "/afs/in2p3.fr/home/c/cgoudet/private/Codes/Template/Input/ScalesOverTime_c.txt", outFileName, 1);

  cout << "outFileName : " << outFileName << endl;
  return 0;
}
