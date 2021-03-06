#include <iostream>
#include "Template/Template.h"
#include "Template/ChiMatrix.h"
#include "TFile.h"
#include "TCanvas.h"
#include "PlotFunctions/SideFunctions.h"
#include <boost/program_options.hpp>
#include <fstream>

using namespace ChrisLib;
using namespace TemplateMethod;
using std::cout;
using std::endl;
using std::vector;
namespace po = boost::program_options;
using std::ifstream;

string FindDefaultTree( TFile* inFile );

int main( int argc, char* argv[] ) {
  po::options_description desc("LikelihoodProfiel Usage");


  unsigned int nIteration, makePlot;
  unsigned long long int toyNumber, toyNumberTmp;
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
    ("MCFileName", po::value<vector<string>>(&MCFileNames)->multitoken(), "1 : Input MC file name")
    ("MCTreeName", po::value<vector<string>>(&MCTreeNames)->multitoken(), "Input MC Tree Name" )
    ("outFileName", po::value<string>(&outFileName)->default_value("ConfigurationsCTree.root"), "Output file name")
    ("configFile", po::value<string>(&configFile), "Select the configuration file")
    ("nIteration", po::value<unsigned int>(&nIteration)->default_value(1), "" )   
    ("inputC", po::value<vector<double>>(&inputValues)->multitoken(), "" )
    ("inputStat", po::value<vector<unsigned int>>(&inputStat)->multitoken(), "" )
    ("makePlot", po::value<unsigned int>(&makePlot)->default_value(0)->implicit_value(1), "" ) 
    ("toyNumber", po::value<unsigned long long int>(&toyNumber), "")
   ;


  // Create a map vm that contains options and all arguments of options       
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv).options(desc).style(po::command_line_style::unix_style ^ po::command_line_style::allow_short).run(), vm);
  po::notify(vm);
  
  if (vm.count("help")) {cout << desc; return 0;}
  //===================================================
  int err{0};

  double scale, errScale, inputC, rms, meanDataZ;
  unsigned int iConf, jConf, statConf, statTree, nBins, fitMethod, bootstrap, indepDistorded, indepTemplates, inversionMethod;
  double nOptim;
  unsigned long long runNumber;
  cout << "Opening " << outFileName << endl;
  TFile *outFile = new TFile( outFileName.c_str(), "UPDATE" );

  TTree *outTree = new TTree( "ConfigurationsCTree","ConfigurationsCTree" );
  outTree->SetDirectory( 0 );
  outTree->Branch( "scale", &scale );
  outTree->Branch( "errScale", &errScale );
  outTree->Branch( "inputC", &inputC );
  outTree->Branch( "iConf", &iConf );
  outTree->Branch( "jConf", &jConf );
  outTree->Branch( "statConf", &statConf );
  outTree->Branch( "statTree", &statTree );
  outTree->Branch( "indepDistorded", &indepDistorded );
  outTree->Branch( "indepTemplates", &indepTemplates );
  outTree->Branch( "dataRMS", &rms );
  outTree->Branch( "meanDataZ", &meanDataZ );
  outTree->Branch( "runNumber", &runNumber );
  outTree->Branch( "nBins", &nBins );
  outTree->Branch( "nOptim", &nOptim );
  outTree->Branch( "bootstrap", &bootstrap );
  outTree->Branch( "fitMethod", &fitMethod );
  outTree->Branch( "toyNumber", &toyNumberTmp );

  TTree *scalesTree = new TTree( "scalesTree", "scalesTree" );
  scalesTree->SetDirectory( 0 );
  scalesTree->Branch( "scale", &scale );
  scalesTree->Branch( "errScale", &errScale );
  scalesTree->Branch( "inputC", &inputC );
  scalesTree->Branch( "iBin", &iConf );
  scalesTree->Branch( "statTree", &statTree );
  scalesTree->Branch( "indepDistorded", &indepDistorded );
  scalesTree->Branch( "indepTemplates", &indepTemplates );
  scalesTree->Branch( "dataRMS", &rms );
  scalesTree->Branch( "meanDataZ", &meanDataZ );
  scalesTree->Branch( "runNumber", &runNumber );
  scalesTree->Branch( "nBins", &nBins );
  scalesTree->Branch( "nOptim", &nOptim );
  scalesTree->Branch( "bootstrap", &bootstrap );
  scalesTree->Branch( "fitMethod", &fitMethod );
  scalesTree->Branch( "inversionMethod", &inversionMethod );
  scalesTree->Branch( "toyNumber", &toyNumberTmp );

  for ( unsigned int iInput = 0; iInput < inputValues.size(); iInput++ ) {
    for ( unsigned int iStat = 0; iStat < inputStat.size(); iStat++ ) {
      for ( unsigned int iIteration = 0; iIteration < nIteration; iIteration++ ) {
	cout << endl << "===================================================" << endl;	
	cout << "New loop : " << iIteration << endl;
	cout << "iStat : " << inputStat[iStat] << endl;
	cout << "iInput : " << inputValues[iInput] << endl;
	toyNumberTmp = toyNumber+iIteration;
	cout << "toyNumber : " << toyNumberTmp << endl;

	//	if ( true ) { //Only to free memory	
	//Pseudo-data  
	Template TempDistorded( "", configFile, {}, {}, dataFileNames, dataTreeNames );
	  Setting &settingDistorded = TempDistorded.GetSetting();
	  if ( settingDistorded.GetIndepDistorded()>1 ) settingDistorded.SetIndepDistorded( toyNumberTmp+2 );
	  if ( settingDistorded.GetBootstrap()>1 ) settingDistorded.SetBootstrap( 2*toyNumberTmp+3 );
	  bool isSmearing = settingDistorded.GetDoSmearing();
	  settingDistorded.SetDebug( 1 );

	  if (isSmearing) {
	    if (settingDistorded.GetSigmaSimEta().size()==0) settingDistorded.SetSigmaSimEta( vector<double>( settingDistorded.GetEtaBins().size()-1, inputValues[iInput] ) );
	    else settingDistorded.GetSigmaSimEta();
	    
	    settingDistorded.SetAlphaSimEta( vector<double>( settingDistorded.GetEtaBins().size()-1, 0 ) );
	  }
	  else {
	    settingDistorded.SetSigmaSimEta( vector<double>( settingDistorded.GetEtaBins().size()-1, 0 ) );
	    if (settingDistorded.GetAlphaSimEta().size()==0) settingDistorded.SetAlphaSimEta( vector<double>( settingDistorded.GetEtaBins().size()-1, inputValues[iInput]  ) );
	    else settingDistorded.GetAlphaSimEta();
	  }

	  inputC = inputValues[iInput];
	  TempDistorded.CreateDistordedTree( "MC_distorded.root" );
	  //}

	  //MC Templates
	  Template TempMeasure( StripString( outFileName ), configFile, {"MC_distorded.root"}, {""}, MCFileNames, MCTreeNames  );
	  cout << "template created" << endl;
	  Setting &settingMeasure = TempMeasure.GetSetting();
	  settingMeasure.SetDebug( 1 );
	  isSmearing = settingMeasure.GetDoSmearing();
       
	  //if (indepTemplates > 1 ) indepTemplates =2;
	  indepTemplates = settingMeasure.GetIndepTemplates();
	  if ( settingMeasure.GetIndepTemplates()>1 ) settingMeasure.SetIndepTemplates( 3*toyNumberTmp+4 );
	  if (isSmearing) {
	    if (settingMeasure.GetSigmaSimEta().size()==0) settingMeasure.SetSigmaSimEta( vector<double>( settingMeasure.GetEtaBins().size()-1, inputValues[iInput] ) );
	    else settingMeasure.GetSigmaSimEta();

	    settingMeasure.SetAlphaSimEta( vector<double>( settingMeasure.GetEtaBins().size()-1, 0 ) );
	  }
	  else {
	    settingMeasure.SetSigmaSimEta( vector<double>( settingMeasure.GetEtaBins().size()-1, 0 ) );
	    if (settingMeasure.GetAlphaSimEta().size()==0) settingMeasure.SetAlphaSimEta( vector<double>( settingMeasure.GetEtaBins().size()-1, inputValues[iInput]  ) );
	    else settingMeasure.GetAlphaSimEta();
	  }

	  settingMeasure.SetNUseEvent( inputStat[iStat] );
	  cout << "extracting" << endl;
   
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
	  TMatrixD *combinScale = isSmearing? TempMeasure.GetMatrix( "sigma" ) : TempMeasure.GetMatrix( "alpha" );
	  TMatrixD* combinErrScale = isSmearing? TempMeasure.GetMatrix( "errSigma" ) : TempMeasure.GetMatrix( "errAlpha" );

	  nBins = settingMeasure.GetEtaBins().size()-1;
	  nOptim = settingMeasure.GetOptimizeRanges();
	  fitMethod = settingMeasure.GetFitMethod();
	  bootstrap = settingMeasure.GetBootstrap();
	  indepDistorded = settingMeasure.GetIndepDistorded();
	  inversionMethod = settingMeasure.GetInversionMethod();

	  cout << "filling confTree" << endl;
	  for ( unsigned int i1 = 0; i1 < nBins; i1++ ) {
	    for ( unsigned int i2 = 0; i2 <=i1; i2++ ) {
	      scale = (*combinScale)(i1, i2);
	      errScale = (*combinErrScale)(i1,i2);
	      if ( errScale == 100 ) continue;
	      iConf = i1;
	      jConf = i2;
	      ChiMatrix *chiMatrix = TempMeasure.GetChiMatrix( i1, i2 );
	      if ( !chiMatrix ) continue;
	      statConf = chiMatrix->GetStat();
	      rms = chiMatrix->GetDataRMS();
	      meanDataZ = chiMatrix->GetDataMean();
	      if ( !statConf ) continue;
	      outTree->Fill();
	    }
	  }

	  cout << "filling binTree" << endl;
	  TH1D* scaleResult = isSmearing? (TH1D*) TempMeasure.GetResults( "sigma" ) : (TH1D*)  TempMeasure.GetResults( "alpha" );
	  TH1D *histInput = new TH1D ("histInput", "", nBins, 0, nBins);
	  for ( unsigned int iBin = 0; iBin < nBins; iBin++ ) {
	    iConf = iBin;
	    scale = scaleResult->GetBinContent(iBin+1);
	    errScale = scaleResult->GetBinError(iBin+1);
	    if ( settingMeasure.GetSigmaSimEta().size()!=0 || settingMeasure.GetAlphaSimEta().size()!=0 ) histInput->SetBinContent( iBin+1, isSmearing? settingMeasure.GetSigmaSimEta()[iBin] : settingMeasure.GetAlphaSimEta()[iBin] );
	    scalesTree->Fill();
	  }

	  outFile->cd();
	  outTree->Write("", TObject::kOverwrite);
	  scalesTree->Write("", TObject::kOverwrite);
	  histInput->Write("", TObject::kOverwrite);
	  outFile->ls();
	  outFile->SaveSelf();
      }
    }
  }

  cout << "return" << endl;
  return 0;

}
