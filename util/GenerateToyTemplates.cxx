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


  unsigned int nIteration, makePlot;
  vector< double > inputValues;
  vector< unsigned int > inputStat;

  vector<string> dataFileNames, MCTreeNames, MCFileNames, dataTreeNames;
  vector<double> dataWeights, MCWeights;
  string  outFileName, configFile;
  //define all options in the program
  desc.add_options()
    ("help", "Display this help message")
    ("dataFileName", po::value<vector<string>>(&dataFileNames)->multitoken(), "1 : Input data file name")
    ("dataTreeName", po::value<vector<string>>(&dataTreeNames)->multitoken(), "Input Data Tree Name" )
    ("dataWeights", po::value<vector<double>>(&dataWeights)->multitoken(), "Input Data Weights" )
    ("MCFileName", po::value<vector<string>>(&MCFileNames)->multitoken(), "1 : Input MC file name")
    ("MCTreeName", po::value<vector<string>>(&MCTreeNames)->multitoken(), "Input MC Tree Name" )
    ("MCWeights", po::value<vector<double>>(&MCWeights)->multitoken(), "Input MC Weights" )
    ("outFileName", po::value<string>(&outFileName)->default_value("ConfigurationsCTree.root"), "Output file name")
    ("configFile", po::value<string>(&configFile), "Select the configuration file")
    ("nIteration", po::value<unsigned int>(&nIteration)->default_value(1), "" )   
    ("inputC", po::value<vector<double>>(&inputValues)->multitoken(), "" )
    ("inputStat", po::value<vector<unsigned int>>(&inputStat)->multitoken(), "" )
    ("makePlot", po::value<unsigned int>(&makePlot)->default_value(0)->implicit_value(1), "" ) 
   ;


  // Create a map vm that contains options and all arguments of options       
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv).options(desc).style(po::command_line_style::unix_style ^ po::command_line_style::allow_short).run(), vm);
  po::notify(vm);
  
  if (vm.count("help")) {cout << desc; return 0;}
  //===================================================
  Style_Christophe();
  int err = 0;

  double sigma, errSigma, inputC, rms;
  unsigned int iConf, jConf, statConf, statTree, runNumber, nBins, fitMethod, bootstrap, indepDistorded, indepTemplates, inversionMethod;
  double nOptim;

  cout << "Opening " << outFileName << endl;
  TFile *outFile = new TFile( outFileName.c_str(), "RECREATE" );

  TTree *outTree = new TTree( "ConfigurationsCTree","ConfigurationsCTree" );
  outTree->SetDirectory( 0 );
  outTree->Branch( "sigma", &sigma );
  outTree->Branch( "errSigma", &errSigma );
  outTree->Branch( "inputC", &inputC );
  outTree->Branch( "iConf", &iConf );
  outTree->Branch( "jConf", &jConf );
  outTree->Branch( "statConf", &statConf );
  outTree->Branch( "statTree", &statTree );
  outTree->Branch( "indepDistorded", &indepDistorded );
  outTree->Branch( "indepTemplates", &indepTemplates );
  outTree->Branch( "dataRMS", &rms );
  outTree->Branch( "runNumber", &runNumber );
  outTree->Branch( "nBins", &nBins );
  outTree->Branch( "nOptim", &nOptim );
  outTree->Branch( "bootstrap", &bootstrap );
  outTree->Branch( "fitMethod", &fitMethod );

  TTree *scalesTree = new TTree( "scalesTree", "scalesTree" );
  scalesTree->SetDirectory( 0 );
  scalesTree->Branch( "sigma", &sigma );
  scalesTree->Branch( "errSigma", &errSigma );
  scalesTree->Branch( "inputC", &inputC );
  scalesTree->Branch( "iBin", &iConf );
  scalesTree->Branch( "statTree", &statTree );
  scalesTree->Branch( "indepDistorded", &indepDistorded );
  scalesTree->Branch( "indepTemplates", &indepTemplates );
  scalesTree->Branch( "dataRMS", &rms );
  scalesTree->Branch( "runNumber", &runNumber );
  scalesTree->Branch( "nBins", &nBins );
  scalesTree->Branch( "nOptim", &nOptim );
  scalesTree->Branch( "bootstrap", &bootstrap );
  scalesTree->Branch( "fitMethod", &fitMethod );
  scalesTree->Branch( "inversionMethod", &inversionMethod );

  for ( unsigned int iInput = 0; iInput < inputValues.size(); iInput++ ) {
    for ( unsigned int iStat = 0; iStat < inputStat.size(); iStat++ ) {
      for ( unsigned int iIteration = 0; iIteration < nIteration; iIteration++ ) {
	cout << endl << "===================================================" << endl;;	
	cout << "New loop : " << iIteration << endl;
	cout << "iStat : " << inputStat[iStat] << endl;
	cout << "iInput : " << inputValues[iInput] << endl;
	if ( true ) { //Only to free memory	
	  Template TempDistorded( "", configFile, {}, {}, {}, dataFileNames, dataTreeNames, dataWeights );
	  Setting &settingDistorded = TempDistorded.GetSetting();
	  settingDistorded.SetDebug( 0 );
	  settingDistorded.SetSigmaSimEta( vector<double>( settingDistorded.GetEtaBins().size()-1, inputValues[iInput] ) );
	  settingDistorded.SetAlphaSimEta( vector<double>( settingDistorded.GetEtaBins().size()-1, 0 ) );
	  inputC = inputValues[iInput];
	  //	  statTree = inputStat[iStat];

	  settingDistorded.Print();
	  TempDistorded.CreateDistordedTree( "MC_distorded.root" );
	}

	Template TempMeasure( "", configFile, {"MC_distorded.root"}, {""}, {1}, MCFileNames, MCTreeNames, MCWeights  );
	Setting &settingMeasure = TempMeasure.GetSetting();
	settingMeasure.SetDebug( 1 );
	//This part is usefull for deviation sigma plots if needed later
	settingMeasure.SetSigmaSimEta( vector<double>( settingMeasure.GetEtaBins().size()-1, inputValues[iInput] ) );
	settingMeasure.SetAlphaSimEta( vector<double>( settingMeasure.GetEtaBins().size()-1, 0 ) );

	settingMeasure.SetNUseEvent( inputStat[iStat] );

	err = TempMeasure.CreateTemplate();
	if ( err ) {
	  cout << "Template::CreateTemplate failed : " << err << endl;
	  return 6;
	}
	
	err = TempMeasure.ExtractFactors( );
	if ( err ) {
	  cout << "Template::Extraction failed : " << err << endl;
	  return 1;
	}

	if ( makePlot ) TempMeasure.MakePlot();
	statTree=settingMeasure.GetNEventData();
	string dumString = outFileName.substr( 0, outFileName.find_last_of( "." ) );
	dumString = dumString.substr( dumString.find_last_of( "/" )+1 );
	cout << "latex file : " << dumString + ".tex" << endl;
	
	runNumber = std::stol( dumString.substr( dumString.find_last_of( "_") +1 ) );
	TMatrixD *combinSigma = TempMeasure.GetMatrix( "sigma" );
	TMatrixD* combinErrSigma = TempMeasure.GetMatrix( "errSigma" );

	nBins = settingMeasure.GetEtaBins().size()-1;
	nOptim = settingMeasure.GetOptimizeRanges();
	bootstrap = settingMeasure.GetBootstrap();
	fitMethod = settingMeasure.GetFitMethod();
	indepDistorded = settingMeasure.GetIndepDistorded();
	indepTemplates = settingMeasure.GetIndepTemplates();
	inversionMethod = settingMeasure.GetInversionMethod();

	cout << "filling confTree" << endl;
	for ( unsigned int i1 = 0; i1 < nBins; i1++ ) {
	  for ( unsigned int i2 = 0; i2 <=i1; i2++ ) {
	    sigma = (*combinSigma)(i1, i2);
	    errSigma = (*combinErrSigma)(i1,i2);
	    if ( errSigma == 100 ) continue;
	    iConf = i1;
	    jConf = i2;
	    ChiMatrix *chiMatrix = TempMeasure.GetChiMatrix( i1, i2 );
	    if ( !chiMatrix ) continue;
	    statConf = chiMatrix->GetStat();
	    rms = chiMatrix->GetDataRMS();
	    if ( !statConf ) continue;

	    outTree->Fill();
	  }
	}

	cout << "filling binTree" << endl;
	TH1D* sigmaResult = (TH1D*) TempMeasure.GetResults( "sigma" );
	for ( unsigned int iBin = 0; iBin < nBins; iBin++ ) {
	  iConf = iBin;
	  sigma = sigmaResult->GetBinContent(iBin+1);
	  if ( sigma < 0 ) { 
	    string negativeName = string( TString::Format( "Note_%u", runNumber ) );
	    TempMeasure.MakePlot("", negativeName + ".tex" );
	    TempMeasure.Save( negativeName + ".root" );
	  }
	    
	  errSigma = sigmaResult->GetBinError(iBin+1);
	  scalesTree->Fill();
	}

	cout << outFile << " " << outTree << " " << scalesTree << " " << endl;
	outFile->cd();
	outTree->Write("", TObject::kOverwrite);
	scalesTree->Write("", TObject::kOverwrite);
	outFile->ls();
	outFile->SaveSelf();
      }
    }
  }
  //  system( "ll -h" );  
  cout << "return" << endl;
  return 0;

}
