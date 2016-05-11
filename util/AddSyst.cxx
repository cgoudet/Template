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

  vector<string> inputFile;

  //define all options in the program
  desc.add_options()
    ("help", "Display this help message")
    ( "inputFile", po::value< vector<string> >( &inputFile )->multitoken(), "" )
    ;


  // create a map vm that contains options and all arguments of options       
  po::positional_options_description p;
  p.add("inputFile", -1);

  // create a map vm that contains options and all arguments of options              
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv).options(desc).positional(p).style(po::command_line_style::unix_style ^ po::command_line_style::allow_short).run(), vm);
  po::notify(vm);
  
  if (vm.count("help")) {cout << desc; return 0;}
  //########################################
  //  Style_Christophe();

  cout << "nFile : " << inputFile.size() << endl;
  for ( unsigned int iFile = 0; iFile<inputFile.size(); iFile++ ) {
    cout << iFile << " : " << inputFile[iFile] << endl;
    DiffSystematics( inputFile[iFile], 0, iFile );
  }
  //Diphoton model
  // //  DiffSystematics( "/afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/Input/systematics_alpha.txt", 0, 0 );
  // DiffSystematics( "/afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/Input/systematics_c.txt", 20, 0 );
  // //material
  // DiffSystematics( "/afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/Input/systematics_c_Moriond0.txt", 20, 1 );
  // //inversion
  // DiffSystematics( "/afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/Input/systematics_c_Moriond2.txt", 20, 1 );
  // //run1
  // DiffSystematics( "/afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/Input/systematics_c_Moriond3.txt", 10, 1 );
  // DiffSystematics( "/afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/Input/systematics_c_Moriond4.txt", 0, 1 );
  // DiffSystematics( "/afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/Input/systematics_c_Moriond1.txt", 1, 1 );


  // DiffSystematics( "/afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/Input/systematics_alpha.txt", 0, 0 );
  // DiffSystematics( "/afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/Input/systematics_c.txt", 0, 1 );


  // VarOverTime( "/afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/Input/ScalesOverTime_alpha.txt", 1);
  // VarOverTime( "/afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/Input/ScalesOverTime_c.txt",  1);

  return 0;
}
