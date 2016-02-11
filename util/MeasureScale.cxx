#include <iostream>
#include "Template/Template.h"
#include "Template/ChiMatrix.h"
#include "TFile.h"
#include "TCanvas.h"
#include "PlotFunctions/SideFunctions.h"
#include <boost/program_options.hpp>
#include <fstream>


using std::cout;
using std::endl;
using std::vector;
namespace po = boost::program_options;
using std::ifstream;

string FindDefaultTree( TFile* inFile );
void Style_Christophe();

int main( int argc, char* argv[] ) {
  po::options_description desc("LikelihoodProfiel Usage");

  //define all options in the program
  vector<string> dataFileNames, MCTreeNames, MCFileNames, dataTreeNames;
  string  outFileName, constVarFit, configFile, distordedTreeName;
  string loadTemplateFileName, saveTemplateFileName, loadFullFileName;
  string correctAlphaFileName, correctAlphaHistName, correctSigmaFileName, correctSigmaHistName;

  desc.add_options()
    ("help", "Display this help message")
    ("dataFileName", po::value<vector<string>>(&dataFileNames)->multitoken(), "1 : Input data file name")
    ("dataTreeName", po::value<vector<string>>(&dataTreeNames)->multitoken(), "Input Data Tree Name" )
    ("MCFileName", po::value<vector<string>>(&MCFileNames)->multitoken(), "1 : Input MC file name")
    ("MCTreeName", po::value<vector<string>>(&MCTreeNames)->multitoken(), "Input MC Tree Name" )
    ("outFileName", po::value<string>(&outFileName)->default_value(""), "Output file name")
    ("saveTemplate", po::value<string>(&saveTemplateFileName)->default_value("")->implicit_value( "" ), "Root file for template saving" )
    ("loadTemplate", po::value<string>(&loadTemplateFileName), "In put template file name" )
    ("noExtraction", "Switch off extraction of scale factors")    
    ("configFile", po::value<string>(&configFile), "Select the configuration file")
    ("loadFull", po::value<string>(&loadFullFileName), "Name of te root file to load")
    ("makePlot", "Create the results plots" )
    ("correctAlphaFileName", po::value<string>(&correctAlphaFileName), "")
    ("correctAlphaHistName", po::value<string>(&correctAlphaHistName), "")
    ("correctSigmaFileName", po::value<string>(&correctSigmaFileName), "")
    ("correctSigmaHistName", po::value<string>(&correctSigmaHistName), "")
    ("createDistorded", po::value<string>(&distordedTreeName)->implicit_value( "" ), "" )
;

  // Create a map vm that contains options and all arguments of options       
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv).options(desc).style(po::command_line_style::unix_style ^ po::command_line_style::allow_short).run(), vm);
  po::notify(vm);
  
  if (vm.count("help")) {cout << desc; return 0;}
  //########################################
  Style_Christophe();
  int err = 0;
  //Simplifies execution line for Christophe

  TFile *correctAlphaFile=0, *correctSigmaFile=0;
  TH1D *correctAlphaHist=0, *correctSigmaHist=0;
  if ( vm.count( "correctAlphaFileName" ) && vm.count( "correctAlphaHistName" ) )  {
    correctAlphaFile = TFile::Open( correctAlphaFileName.c_str() );
    correctAlphaHist = (TH1D*) correctAlphaFile->Get( correctAlphaHistName.c_str() );
  }
  if ( vm.count( "correctSigmaFileName" ) && vm.count( "correctSigmaHistName" ) )  {
    correctSigmaFile = TFile::Open( correctSigmaFileName.c_str() );
    correctSigmaHist = (TH1D*) correctSigmaFile->Get( correctSigmaHistName.c_str() );
  }


  Template Temp( outFileName, configFile, dataFileNames, dataTreeNames, MCFileNames, MCTreeNames  );
  Temp.ApplyCorrection( correctAlphaHist, correctSigmaHist );
  if ( vm.count("createDistorded") ) { 
    Temp.CreateDistordedTree( distordedTreeName );
    return 0;
  }

  if ( vm.count("loadFull") ) {
    err = Temp.Load( loadFullFileName, false);
    if ( err ) {
      cout << "Template::LoadFull failed : " << err << endl;
      return 3;
    }}

  if ( vm.count( "loadTemplate" ) ) {
    err = Temp.Load( loadTemplateFileName, true );
    if ( err ) {
      cout << "Template::LoadTemplate failed : " << err << endl;
      return 4;
    }} 
  
  
  if ( !vm.count( "noExtraction" ) )  {
    err = Temp.ExtractFactors();
    if ( err ) {
      cout << "Template::Extraction failed : " << err << endl;
      return 1;
    }
    err = Temp.Save();
    // if ( err ) {
    //   cout << "Template::Save failed : " << err << endl;
    //   return 2;
    // }
  }
  if ( vm.count("makePlot") )  {
    string title = outFileName.substr( 0, outFileName.find_last_of( "." ) ) + ".tex";
    Temp.MakePlot( "", "" );
  }


  return 0;
}


