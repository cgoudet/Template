#include <iostream>
#include <istream>
#include <fstream>
#include <map>
#include <vector>
#include <string>
#include <sstream>
#include <boost/program_options.hpp>
#include <boost/multi_array.hpp>

#include "TH1.h"
#include "TFile.h"
#include "TTree.h"
#include "TBranch.h"
#include "TCanvas.h"

#include "Template/BiasAnalysis.h"

using namespace std;
namespace po = boost::program_options;

int main(int argc, char *argv[])
{
  
  //=================
  //Define options to read name of files from the command line
  po::options_description desc("Input data files (.root)");
  vector<string> dataFiles;
  bool isConf{0};
  bool isAlpha{0};
  string fileName;

  desc.add_options()
    ("help", "Display this help message")
    ("dataFiles", po::value<vector <string> >(&dataFiles), "Absolute path of root files to analyze" )
    ("isConf", po::value<bool> (&isConf)->default_value(0), "Analyse of bin or configuration" )
    ("isAlpha", po::value<bool> (&isAlpha)->default_value(0), "Analyse of alpha or c" )
    ("fileName", po::value<string> (&fileName), "Name of the output file (pattern used)" )
    ;
                                   
  po::positional_options_description p;
  p.add("dataFiles", -1);

  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv).options(desc).positional(p).style(po::command_line_style::unix_style ^ po::command_line_style::allow_short).run(), vm);
  po::notify(vm);
  
  if (vm.count("help")) {cout << desc; return 0;}


  //================
  string BinOrConf;

  if (isConf) BinOrConf= "Conf";
  else BinOrConf="Bin";

  BiasAnalysis BA("/afs/in2p3.fr/home/a/aguergui/public/Calibration/Template/ConfigFile/Bias"+BinOrConf+".boost");

  string path= "/sps/atlas/a/aguerguichon/Calibration/Bias/";

  BA.SelectVariables(dataFiles, isAlpha);
  BA.SaveBiasInfo(path+"Plots/"+fileName);

  path+= "Plots/";
  
  BA.MakeBiasPlots(path, fileName, "Test");

  string commandLine = "mv ./"+fileName+".pdf "+path;
  system ( commandLine.c_str() );
  commandLine = "rm "+fileName+"*";
  system ( commandLine.c_str() );
  
  //================
  //End of program
  cout <<"End of programm."<<endl;
  return 0;
}
