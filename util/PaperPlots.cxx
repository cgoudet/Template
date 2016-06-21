#include <iostream>
#include "Template/Template.h"
#include "Template/ChiMatrix.h"
#include "TFile.h"
#include "TCanvas.h"
#include "PlotFunctions/SideFunctions.h"
#include <boost/program_options.hpp>
#include <fstream>
#include "TProfile.h"

using std::cout;
using std::endl;
using std::vector;
namespace po = boost::program_options;
using std::ifstream;




int main( int argc, char* argv[] ) {
  po::options_description desc("LikelihoodProfiel Usage");

  //define all options in the program
  vector<string> MCFiles, dataFiles;
  desc.add_options()
    ("help", "Display this help message")
    ( "MCFiles", po::value< vector<string> >( &MCFiles )->multitoken(), "" )
    ( "dataFiles", po::value< vector<string> >( &dataFiles )->multitoken(), "" )
;

  // Create a map vm that contains options and all arguments of options       
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv).options(desc).style(po::command_line_style::unix_style ^ po::command_line_style::allow_short).run(), vm);
  po::notify(vm);
  
  if (vm.count("help")) {cout << desc; return 0;}
  //########################################

  TH1D*  DoMeeVsMu( vector<string> &datasets );


  return 0;
}


TH1*  DoMeeVsMu( vector<string> &datasetNames ) {

  TProfile *profile = new TProfile( "profile", "profile", 100, -0.5, 99.5 );
  double meanMass=0;
  MapBranches mapBranch;
  unsigned int totEntries=0;

  for ( auto vDatasetName : datasetNames ) {
    TFile *inFile = new TFile( vDatasetName.c_str() );
    TTree *inTree = (TTree*) inFile->Get( FindDefaultTree( inFile, "TTree" ).c_str() );
    mapBranch.LinkTreeBranches( inTree, 0 );

    unsigned int nentries = inTree->GetEntries();
    totEntries+=nentries;
    for ( unsigned int iEntry = 0; iEntry<nentries; iEntry++ ) {
      meanMass += mapBranch.GetVal("m12");
      profile->Fill( mapBranch.GetVal("mu"), mapBranch.GetVal("m12"), mapBranch.GetVal("weight") );
    }
  }

  meanMass/=totEntries;

  return 0;
}
