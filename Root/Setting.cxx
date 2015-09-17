#include "Template/Setting.h"
#include <iostream>
#include <fstream>
#include <cstdlib>
#include "TTree.h"
#include <boost/program_options.hpp>
#include "PlotFunctions/SideFunctions.h"

namespace po = boost::program_options;
using std::ifstream;

using std::cout;
using std::endl;
using std::string;
using std::vector;
using std::stringstream;

//######## CONSTRUCTORS
Setting::Setting() : m_mode("1VAR"), m_var1( "eta" ), m_var2( "pt" ), m_ZMassMin(80), m_ZMassMax(100), m_ZMassNBins(40),
		     m_doScale(false), m_alphaMin(-1e-2), m_alphaMax(1e-2), m_alphaNBins(10),
		     m_doSmearing(false), m_sigmaMin(0), m_sigmaMax(0.1), m_sigmaNBins(10),
		     m_selection(0), m_nEventMC(0), m_nEventData(0), m_nUseEvent(0),
		     m_debug( true ), m_doSimulation( false ), m_MCName(""), m_dataName(""),
		     m_optimizeRanges( 10 ), m_fitMethod( 3 ), m_nUseEl(1), m_nEventCut(500), m_thresholdMass( 70 ),
		     m_indepDistorded( false ), m_indepTemplates( false ), m_inversionMethod(0)
{
  m_etaBins.clear();
  m_ptBins.clear();
  m_constVarFit = "SIGMA";
}

//########### SETTER
void Setting::SetConstVarFit( string constVarFit ) { 
  if ( constVarFit == "ALPHA" || constVarFit == "SIGMA" ) m_constVarFit = constVarFit; 
  else cout << constVarFit << " is not ALPHA or SIGMA" << endl;
}


//############METHODS
int Setting::Configure( const string &configFile ) {
  if ( m_debug )  cout << "Setting : Configure( " << configFile << " )" << endl;
  string etaBins, ptBins, alphaSimEta, alphaSimPt, sigmaSimEta, sigmaSimPt;
  int debug, doSmearing, doScale,  symBin;

  po::options_description configOptions("configOptions");
  configOptions.add_options()
    ( "ZMassMin", po::value<double>(&m_ZMassMin), "")
    ( "ZMassMax", po::value<double>(&m_ZMassMax), "")
    ( "ZMassNBins", po::value<unsigned int>(&m_ZMassNBins), "" )
    ( "mode", po::value<string>(&m_mode), "" )
    ( "var1", po::value<string>(&m_var1), "" )
    ( "var2", po::value<string>(&m_var2), "" )
    ( "doScale", po::value<int>(&doScale), "" )
    ( "alphaMin", po::value<double>(&m_alphaMin), "")
    ( "alphaMax", po::value<double>(&m_alphaMax), "")
    ( "alphaNBins", po::value<int>(&m_alphaNBins), "" )
    ( "doSmearing", po::value<int>(&doSmearing), "" )
    ( "sigmaMin", po::value<double>(&m_sigmaMin), "")
    ( "sigmaMax", po::value<double>(&m_sigmaMax), "")
    ( "sigmaNBins", po::value<int>(&m_sigmaNBins), "" )
    ( "debug", po::value<int>(&debug), "" )
    ( "constVarFit", po::value<string>(&m_constVarFit), "" )
    ( "selection", po::value<int>(&m_selection), "" )
    ( "doSimulation", po::value<bool>(&m_doSimulation), "" )
    ( "optimizeRanges", po::value<double>(&m_optimizeRanges), "" )
    ( "etaBins", po::value<string>(&etaBins), "" )
    ( "ptBins", po::value<string>(&ptBins), "" )
    ( "alphaSimEta", po::value<string>(&alphaSimEta), "" )
    ( "alphaSimPt", po::value<string>(&alphaSimPt), "" )
    ( "sigmaSimEta", po::value<string>(&sigmaSimEta), "" )
    ( "sigmaSimPt", po::value<string>(&sigmaSimPt), "" )
    ( "symBin", po::value<int>(&symBin), "" )
    ( "fitMethod", po::value<unsigned int>(&m_fitMethod), "" )
    ( "nUseEl",    po::value<unsigned int>(&m_nUseEl), "" )
    ( "nUseEvent", po::value<unsigned int>(&m_nUseEvent), "" )
    ( "nEventCut", po::value<unsigned int>(&m_nEventCut), "" )
    ( "thresholdMass", po::value<double>(&m_thresholdMass), "" )
    ( "indepDistorded", po::value<bool>(&m_indepDistorded), "" )
    ( "indepTemplates", po::value<bool>(&m_indepTemplates), "" )
    ( "inversionMethod", po::value<unsigned int>(&m_inversionMethod), "" )
    ;
  
  po::variables_map vm;
  ifstream ifs( configFile, ifstream::in );
  po::store(po::parse_config_file(ifs, configOptions), vm);
  po::notify( vm );
  

  m_doSmearing = (bool) doSmearing;
  m_doScale = (bool) doScale;
  m_debug = (bool) debug;
  m_symBin = (bool) symBin;

  ParseVector( etaBins, m_etaBins );
  ParseVector( ptBins, m_ptBins );
  ParseVector( alphaSimEta, m_alphaSimEta );
  ParseVector( alphaSimPt, m_alphaSimPt );
  ParseVector( sigmaSimEta, m_sigmaSimEta );
  ParseVector( sigmaSimPt, m_sigmaSimPt );

  if ( m_symBin ) {
    Symmetrize( m_etaBins );
    Symmetrize( m_ptBins );
    SymmetrizedSim( m_alphaSimEta );
    SymmetrizedSim( m_sigmaSimEta );
    SymmetrizedSim( m_alphaSimPt );
    SymmetrizedSim( m_sigmaSimPt );
  }

  std::sort( m_etaBins.begin(), m_etaBins.end() );
  m_etaBins.erase( unique( m_etaBins.begin(), m_etaBins.end() ), m_etaBins.end() );
  std::sort( m_ptBins.begin(), m_ptBins.end() );
  m_ptBins.erase( unique( m_ptBins.begin(), m_ptBins.end() ), m_ptBins.end() );  

  //=====
  if ( !m_nUseEl ) m_nUseEl=1;
  if ( m_mode != "1VAR" && m_mode != "2VAR" ) return 1;
  if ( m_doSimulation ) { //Make checks for vector sizes in simulation
    if ( m_etaBins.size() && m_alphaSimEta.size() != m_etaBins.size() - 1 ) return 2;
    if ( m_ptBins.size() && m_alphaSimPt.size() != m_ptBins.size() - 1 ) return 2;
    if ( m_etaBins.size() && m_sigmaSimEta.size() != m_etaBins.size() - 1 ) return 2;
    if ( m_ptBins.size() && m_sigmaSimPt.size() != m_ptBins.size() - 1 ) return 2;
    if ( m_constVarFit != "ALPHA" && m_constVarFit != "SIGMA" ) return 3;
    if ( m_alphaMin > m_alphaMax ) return 4;
    if ( m_sigmaMin > m_sigmaMax ) return 4;
  }

  if ( !m_doScale && !m_doSmearing ) return 5;

  if ( m_debug )  cout << "Setting : Configure " << configFile << " ) Done" << endl; 
   return 0;
}

//====================================================
int Setting::Save( TFile *outFile ) {
  if ( m_debug ) cout << "Setting::Save" << endl;

  if ( !outFile ) {
    cout << "TFile is a 0 pointer" << endl;
    return 1;}

  if ( !outFile->IsOpen() ) {
    cout << "TFile is not opened" << endl;
    return 2;
  }

  outFile->cd();

  TTree *infoTree = new TTree( "InfoTree", "InfoTree" );
  
 //properties for templates
  infoTree->Branch( "alphaNBins", &m_alphaNBins  );
  infoTree->Branch( "alphaMin", &m_alphaMin );
  infoTree->Branch( "alphaMax", &m_alphaMax );
  infoTree->Branch( "sigmaNBins", &m_sigmaNBins );
  infoTree->Branch( "sigmaMin", &m_sigmaMin );
  infoTree->Branch( "sigmaMax", &m_sigmaMax );
  infoTree->Branch( "MCName", &m_MCName );

  //propeerties of detector
  infoTree->Branch( "etaBins", &m_etaBins );
  infoTree->Branch( "ptBins", &m_ptBins );
  infoTree->Branch( "mode", &m_mode );
  infoTree->Branch( "symBin", &m_symBin );
  infoTree->Branch( "fitMethod", &m_fitMethod );
  
  //properties of extraction
  infoTree->Branch( "doScale", &m_doScale );
  infoTree->Branch( "doSmearing", &m_doSmearing );
  infoTree->Branch( "dataName", &m_dataName );
  
  //Simulation properties
  infoTree->Branch( "doSimulation", &m_doSimulation );
  infoTree->Branch( "alphaSimEta", &m_alphaSimEta );
  infoTree->Branch( "sigmaSimEta", &m_sigmaSimEta );
  infoTree->Branch( "alphaSimPt", &m_alphaSimPt );
  infoTree->Branch( "sigmaSimPt", &m_sigmaSimPt );
  infoTree->Branch( "indepDistorded", &m_indepDistorded );
  infoTree->Branch( "indepTemplates",&m_indepTemplates );

  //Mass distribution properties
  infoTree->Branch( "ZMassNBins", &m_ZMassNBins );  
  infoTree->Branch( "ZMassMin", &m_ZMassMin );
  infoTree->Branch( "ZMassMax", &m_ZMassMax );

  infoTree->Branch( "constVarFit", &m_constVarFit );
  infoTree->Branch( "nUseEl", &m_nUseEl );
  infoTree->Branch( "selection", &m_selection );
  infoTree->Branch( "inversionMethod", &m_inversionMethod );
  // infoTree->Branch( "nEventMC", &m_nEventMC );
  // infoTree->Branch( "nEventData", &m_nEventData );
  infoTree->Branch( "nEventCut", &m_nEventCut );
  infoTree->Branch( "thresholdMass", &m_thresholdMass );
  infoTree->Fill();
  infoTree->Write( "", TObject::kOverwrite );


  if ( m_debug ) cout << "Setting::Save Done" << endl;
  return 0;
}

//======================================================
int Setting::Load( const string &inFileName, bool justTemplate ) {
  if ( m_debug ) cout << "Setting::Load" << endl;

  TFile *inFile = TFile::Open( inFileName.c_str() );
  if ( !inFile ) {
    cout << "input file not found" << endl;
    return 1;
  }

  TTree *infoTree = (TTree* ) inFile->Get( "InfoTree" );
  if ( !infoTree ) {
    cout << "InfoTree  not found" << endl;
    return 2;
  }

  infoTree->SetBranchStatus( "*", 1 );

 //properties for templates
  infoTree->SetBranchAddress( "alphaNBins", &m_alphaNBins  );
  infoTree->SetBranchAddress( "alphaMin", &m_alphaMin );
  infoTree->SetBranchAddress( "alphaMax", &m_alphaMax );
  infoTree->SetBranchAddress( "sigmaNBins", &m_sigmaNBins );
  infoTree->SetBranchAddress( "sigmaMin", &m_sigmaMin );
  infoTree->SetBranchAddress( "sigmaMax", &m_sigmaMax );
  infoTree->SetBranchAddress( "symBin", &m_symBin );

    //Mass distribution properties
  infoTree->SetBranchAddress( "ZMassNBins", &m_ZMassNBins );  
  infoTree->SetBranchAddress( "ZMassMin", &m_ZMassMin );
  infoTree->SetBranchAddress( "ZMassMax", &m_ZMassMax );

  infoTree->SetBranchAddress( "selection", &m_selection );
  infoTree->SetBranchAddress( "nEventMC", &m_nEventMC );
  infoTree->SetBranchAddress( "nEventCut", &m_nEventCut );
  infoTree->SetBranchAddress( "thresholdMass", &m_thresholdMass );
  infoTree->SetBranchAddress( "nUseEl", &m_nUseEl );

  
  if ( !justTemplate ) {
    //properties of extraction
    infoTree->SetBranchAddress( "doScale", &m_doScale );
    infoTree->SetBranchAddress( "doSmearing", &m_doSmearing );
    infoTree->SetBranchAddress( "fitMethod", &m_fitMethod );
    infoTree->SetBranchAddress( "inversionMethod", &m_inversionMethod );

    //Simulation properties
    infoTree->SetBranchAddress( "doSimulation", &m_doSimulation );
    infoTree->SetBranchAddress( "indepDistorded", &m_indepDistorded );
    infoTree->SetBranchAddress( "indepTemplates", &m_indepTemplates );

    infoTree->SetBranchAddress( "nEventData", &m_nEventData );
  }
  infoTree->GetEntry(0);  
  
  //Load all vectors
  infoTree->LoadTree( 0 );
  
  TBranch *branchAlphaSimEta = 0, *branchAlphaSimPt = 0, *branchSigmaSimEta = 0, *branchSigmaSimPt = 0, *branchEtaBin = 0, *branchPtBin = 0, *branchMode = 0, *branchConstVarFit = 0, *branchMCName = 0, *branchDataName = 0;
  vector< double > *alphaSimEta = 0, *alphaSimPt = 0, *sigmaSimEta = 0, *sigmaSimPt = 0, *etaBin = 0, *ptBin = 0;
  string *mode = 0, *constVarFit = 0, *MCName = 0, *dataName = 0;
  
  infoTree->SetBranchAddress( "etaBins", &etaBin, &branchEtaBin );
  infoTree->SetBranchAddress( "ptBins", &ptBin, &branchPtBin );
  infoTree->SetBranchAddress( "mode", &mode, &branchMode );
  infoTree->SetBranchAddress( "MCName", &MCName, &branchMCName );
  
  branchEtaBin->GetEntry( 0 );
  branchPtBin->GetEntry( 0 );
  branchMode->GetEntry(0);
  branchMCName->GetEntry(0);

  m_etaBins = *etaBin;
  m_ptBins = *ptBin;
  m_mode =  *mode ;
  m_MCName = *MCName;
  
  if ( !justTemplate ) {
    infoTree->SetBranchAddress( "alphaSimEta", &alphaSimEta, &branchAlphaSimEta );
    infoTree->SetBranchAddress( "alphaSimPt", &alphaSimPt, &branchAlphaSimPt );
    infoTree->SetBranchAddress( "sigmaSimEta", &sigmaSimEta, &branchSigmaSimEta );
    infoTree->SetBranchAddress( "sigmaSimPt", &sigmaSimPt, &branchSigmaSimPt );
    infoTree->SetBranchAddress( "constVarFit", &constVarFit, &branchConstVarFit );
    infoTree->SetBranchAddress( "dataName", &dataName, &branchDataName );
    
    branchAlphaSimEta->GetEntry( 0 );
    branchAlphaSimPt->GetEntry( 0 );
    branchSigmaSimEta->GetEntry( 0 );
    branchSigmaSimPt->GetEntry( 0 );
    branchConstVarFit->GetEntry( 0 );
    branchDataName->GetEntry( 0 );
    
    m_alphaSimEta = *alphaSimEta;
    m_alphaSimPt = *alphaSimPt;
    m_sigmaSimEta = *sigmaSimEta;
    m_sigmaSimPt = *sigmaSimPt;
    m_constVarFit = *constVarFit;
    m_dataName = *dataName;
  }
  
  //Some checks to do if loeading only templates
  if ( justTemplate && m_doSimulation) {
    if ( m_alphaSimEta.size() != m_etaBins.size() - 1
	 || ( m_ptBins.size() && m_alphaSimPt.size() != m_ptBins.size() - 1 )
	 || m_sigmaSimEta.size() != m_etaBins.size() - 1
	 || ( m_ptBins.size() && m_sigmaSimPt.size() != m_ptBins.size() - 1 )) {
      cout << "Detector binning and simulation binning do not match" << endl;
      return 3;
    }    
  } 
 
  if ( m_debug ) cout << "Setting::Load Done" << endl;
  return 0;
}

//=========================================
int Setting::Symmetrize( vector<double> &outVector ) {

  for ( vector<double>::iterator vec = outVector.begin(); vec != outVector.end(); vec++ ) {
    *vec = fabs( *vec );
  }
  return 0;
}

//==========================================
int Setting::SymmetrizedSim( vector<double> &outVector ) {

  vector< double > vecResult;
  for ( unsigned int i = outVector.size() /2; i< outVector.size(); i++ ) {
    vecResult.push_back( outVector[ i ] );
  }

  outVector.clear();
  outVector = vecResult;

  return 0;
}

//=================================
void Setting::Print() {

  cout << "m_mode : "<< m_mode << endl << endl;
  cout << "m_var1 : " << m_var1 << endl;
  cout << "m_var2 : " << m_var2 << endl;
  cout << "m_ZMassMin : " << m_ZMassMin << endl;
  cout << "m_ZMassMax : " << m_ZMassMax << endl;
  cout << "m_ZMassNBins : " << m_ZMassNBins << endl;
  cout << "m_doScale : " << m_doScale << endl;
  cout << "m_alphaMin : " << m_alphaMin << endl;
  cout << "m_alphaMax : " << m_alphaMax << endl;
  cout << "m_alphaNBins : " << m_alphaNBins << endl;
  cout << "m_doSmearing : " << m_doSmearing << endl;
  cout << "m_sigmaMin : " << m_sigmaMin << endl;
  cout << "m_sigmaMax : " << m_sigmaMax << endl;
  cout << "m_sigmaNBins : " << m_sigmaNBins << endl;
  cout << "m_constVarFit : " << m_constVarFit << endl;
  cout << "m_selection : " << m_selection << endl;
  cout << "m_nEventMC : " << m_nEventMC << endl;
  cout << "m_nEventData : " << m_nEventData << endl;
  cout << "m_nUseEvent : " << m_nUseEvent << endl;
  cout << "m_debug : " << m_debug << endl;
  cout << "m_doSimulation : "<< m_doSimulation << endl;
  cout << "m_MCName : " << m_MCName << endl;
  cout << "m_dataName : " << m_dataName << endl;
  cout << "m_symBin : " << m_symBin << endl;
  cout << "m_fitMethod : " << m_fitMethod << endl;
  cout << "m_inversionMethod : " << m_inversionMethod << endl;
  cout << "m_nUseEl : " << m_nUseEl << endl;
  cout << "m_nEventCut : " << m_nEventCut << endl;
  cout << "m_thresholMass : " << m_thresholdMass << endl;
  cout << "m_indepDistorded : " << m_indepDistorded << endl;
  cout << "m_indepTemplates : " << m_indepTemplates << endl;
  cout << "m_etaBins : ";
  PrintVector( m_etaBins );

  cout << "m_ptBins";
  PrintVector( m_ptBins );

}

void Setting::PrintVector( vector<double> vector ) {
  for ( unsigned int i = 0; i < vector.size(); i++ ) {
    cout << vector[i] << " ";
  }
  cout << endl;
}
