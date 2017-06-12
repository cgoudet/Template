#include "Template/Template.h"
#include "PlotFunctions/Foncteurs.h"
#include "PlotFunctions/SideFunctions.h"
#include "PlotFunctions/SideFunctionsTpp.h"
#include "PlotFunctions/DrawOptions.h"
#include "PlotFunctions/InvertMatrix.h"

#include "TCanvas.h"
#include "TLorentzVector.h"
#include "TError.h"
#include "TROOT.h"

#include <iterator>
#include <iostream>
#include <fstream>
#include "time.h"
#include "TKey.h"
#include "time.h"
#include <chrono>
#include <algorithm>
#include <stdexcept>

using std::invalid_argument;
using std::swap;
using boost::extents;
using std::cout;
using std::endl;
using std::vector;
using std::fstream;
using TMath::Power;
using std::to_string;
using std::find;
using namespace std::chrono;
using namespace ChrisLib;
using namespace TemplateMethod;
using std::runtime_error;
using std::cerr;

//########## CONSTRUCTOR
TemplateMethod::Template::Template() : m_setting(), m_rand(), m_mapBranches(), m_name()
{
  TH1::AddDirectory( false );
  gErrorIgnoreLevel = kError;
  m_chiMatrix.clear();
  m_dataFileNames.clear();
  m_dataTreeNames.clear();
  m_MCFileNames.clear();
  m_MCTreeNames.clear();

  m_mapBranches.SetVal("WEIGHT", 1. );
  m_histNames = { "measScale", "inputScale", "deviation" };
  m_vectHist.resize( extents[2][m_histNames.size()] );

  m_matrixNames = { "combin", "combinErr"  };
  m_vectMatrix.resize( extents[2][m_matrixNames.size()] );

}

TemplateMethod::Template::Template( const string &outFileName, const string &configFile,
                    vector<string> dataFileNames, vector<string> dataTreeNames,
                    vector<string> MCFileNames, vector<string> MCTreeNames )
  : Template()
{
  //Setup the setting attribute
  Configure( configFile );


  for ( unsigned int iType = 0; iType < 2; iType++ ) {
    if ( !iType && !dataFileNames.size() ) continue;
    if ( iType && !MCFileNames.size() ) continue;
    FillBranchesToLink( !iType );
    vector<string> &fileNames = iType ? MCFileNames : dataFileNames;
    vector<string> &treeNames = iType ? MCTreeNames : dataTreeNames;

    for ( unsigned int iFile = 0; iFile < fileNames.size(); iFile++ ) {
      TFile *dumFile = new TFile( fileNames[iFile].c_str() );
      if ( !dumFile ) throw invalid_argument( "Template::Template : Unknown input file.");

      if ( treeNames.size() < iFile+1 ) treeNames.push_back( "" );

      if ( treeNames[iFile] == "" ) treeNames[iFile] = FindDefaultTree( dumFile, "TTree", "selectionTree" );
      TTree *dumTree = static_cast<TTree*>(dumFile->Get(treeNames[iFile].c_str()));
      if ( !dumTree ) throw runtime_error( "TempalteMethod::Template::Configure : "+treeNames[iFile] + " in " + fileNames[iFile] + " does not exist." );

      delete dumTree; dumTree=0;
      dumFile->Close("R");
      delete dumFile; dumFile=0;
    }
    if ( !iType ) {
      m_setting.SetDataName( dataFileNames.front() );
      m_dataFileNames = dataFileNames;
      m_dataTreeNames = dataTreeNames;
    }
    else {
      m_setting.SetMCName( MCFileNames.front() );
      m_MCFileNames = MCFileNames;
      m_MCTreeNames = MCTreeNames;
    }
  }

  m_name = outFileName == ""  ? "TemplateDefault" : TString(outFileName).ReplaceAll(".root", "" );
  //  m_saveTemplateFileName =   TString( m_saveFileName ).ReplaceAll( ".root", "_template.root" ).Data();

  if ( m_setting.GetDebug() )  cout << "Template : Constructor Done" << endl;
}

TemplateMethod::Template::~Template() {
  //Clear the ChiMatrix vector
  ClearChiMatrix();
  CleanHistVect();
  CleanMatrixVect();
}


//######## METHODS
void TemplateMethod::Template::Configure( const string &configFile ) {
  if ( m_setting.GetDebug() )  cout << "Template : Configure( " << configFile << " )" << endl;
  m_setting.Configure( configFile );
  if ( m_setting.GetDebug() )  cout << "Template : Configure( " << configFile << " ) Done" << endl;
}

//######################==
int  TemplateMethod::Template::Load( const string &inFileName, bool justTemplate ) {
  if ( m_setting.GetDebug() ) cout << "Template::LoadTemplate"<< endl;

  TFile *inFile = TFile::Open( inFileName.c_str() );
  if ( !inFile ) throw runtime_error( "TemplateMethod::Template::Load : Input file not found : " + inFileName );

  //Get the proper information from saved configuration file
  int err = m_setting.Load( inFileName, justTemplate );
  if ( err ) throw runtime_error( "TemplateMethod::Template::Load : Setting Loading failed : " + err );

  //Decide which variables to extract and how to cut the detector
  vector<double> etaBins = m_setting.GetEtaBins();
  vector<double> ptBins = m_setting.GetPtBins();

  //Clean m_chiMatrix if not empty
  //ClearChiMatrix();

  //Open the tree into which alpha ranges values for each chiMatrix are stored
  int i_eta=-99, j_eta=-99;
  TTree *treeChiMatrixRanges = (TTree* ) inFile->Get( "chiMatrixRanges" );
  if ( !treeChiMatrixRanges ) {
    cout << "chiMatrixRanges not found" << endl;
    return 6;
  }
  else {
    //Link alpha rane tree to corresonding variables

    double alphaMin=0, alphaMax=0, sigmaMin=0, sigmaMax=0;
    treeChiMatrixRanges->SetBranchStatus( "*", 1);
    treeChiMatrixRanges->SetBranchAddress( "i_eta", &i_eta);
    treeChiMatrixRanges->SetBranchAddress( "j_eta", &j_eta );
    treeChiMatrixRanges->SetBranchAddress( "alphaMin" , &alphaMin );
    treeChiMatrixRanges->SetBranchAddress( "sigmaMin", &sigmaMin );
    treeChiMatrixRanges->SetBranchAddress( "alphaMax", &alphaMax );
    treeChiMatrixRanges->SetBranchAddress( "sigmaMax", &sigmaMax );

    //Make sure m_ChiMtrix is empty before loading
    // ClearChiMatrix();

    for ( int entry = 0; entry < treeChiMatrixRanges->GetEntries() ; entry++ ) {
      treeChiMatrixRanges->GetEntry( entry );

      //If the coordinates of the loaded chiMatrix are off the vector, extend the vector
      while ( i_eta >= (int) m_chiMatrix.size() )  m_chiMatrix.push_back( vector< ChiMatrix * >() );
      while ( j_eta >= (int) m_chiMatrix[i_eta].size() ) m_chiMatrix[i_eta].push_back( 0 );

      //Create a new chiMatrix at the right coordinates which the loaded ranges values
      if ( !m_chiMatrix[i_eta][j_eta] ) m_chiMatrix[i_eta][j_eta] = new ChiMatrix( string( TString::Format( "ChiMatrix_%i_%i", i_eta, j_eta )), m_setting );
      m_chiMatrix[i_eta][j_eta]->SetAlphaMin( alphaMin );
      m_chiMatrix[i_eta][j_eta]->SetAlphaMax( alphaMax );
      m_chiMatrix[i_eta][j_eta]->SetSigmaMin( sigmaMin );
      m_chiMatrix[i_eta][j_eta]->SetSigmaMax( sigmaMax );

    }
    delete treeChiMatrixRanges; treeChiMatrixRanges=0;
  }
  //Perform test on the structure on m_chiMatrix and load templates
  for ( i_eta = 0; i_eta < (int) m_chiMatrix.size(); i_eta++ ) {
    for ( j_eta = 0; j_eta < (int) m_chiMatrix[i_eta].size(); j_eta++ ) {

      if ( !m_chiMatrix[i_eta][j_eta] ) {
        cout << "m_chiMatrix has an empty bin" << endl;
        return 7;}

      //Load the templates
      err = m_chiMatrix[i_eta][j_eta]->Load( inFile, justTemplate );
      if ( err ) {
        cout << "Loading alpha/sigma Templates failed : i=" << i_eta << " j=" << j_eta << " err=" << err << endl;
        return 3;}

    }}
  //If pointers factors are not empty, reset them to 0 after a cleaning
  if ( justTemplate ) cout << endl;//CleanHistVect();
  else {
    //Load histograms
    for ( unsigned int iVar = 0; iVar < m_vectHist.size(); iVar++ ) {
      for ( unsigned int iHist = 0; iHist < m_vectHist[0].size(); iHist++ ) {
        string titleHist = CreateHistMatName( m_histNames[iHist], iVar );
        m_vectHist[iVar][iHist] = (TH1*) inFile->Get( titleHist.c_str() );

        if ( !m_vectHist[iVar][iHist] ) {
          cout << "Histogram not found : " << titleHist << endl;
          //      return 4;
        }
        else m_vectHist[iVar][iHist]->SetDirectory(0);
      }
      //Load Matrices
      for ( unsigned int iMat = 0; iMat < m_vectMatrix[0].size(); iMat++ ) {
        m_vectMatrix[iVar][iMat] = (TMatrixD*) inFile->Get( CreateHistMatName( m_matrixNames[iMat], iVar ).c_str() );
        if ( !m_vectMatrix[iVar][iMat] ) {
          cout << "Matrix not found : " << CreateHistMatName( m_matrixNames[iMat], iVar ) << endl;
          return 4;
        }
      }

    }
  }

  inFile->Close("R");
  delete inFile; inFile=0;
  if ( m_setting.GetDebug() ) cout << "Template::LoadTemplate Done" << endl;
  return 0;
}

//######################==
int TemplateMethod::Template::Save( bool saveChiMatrix ) {
  if ( m_setting.GetDebug() ) cout << "Template::Save()" << endl;

  //create the output TFile
  string saveFileName = m_name + ".root";
  TFile *outFile = new TFile( saveFileName.c_str(), "UPDATE");
  cout << "saving file : " << outFile->GetName() << endl;

  //Saving properties of TemplateClass
  for ( unsigned int iVar = 0; iVar < m_vectHist.size(); iVar++ ) {
    for ( unsigned int iHist = 0; iHist < m_vectHist[0].size(); iHist++ )
      if ( m_vectHist[iVar][iHist] ) m_vectHist[iVar][iHist]->Write( CreateHistMatName( m_histNames[iHist], iVar ).c_str(), TObject::kOverwrite );
    for ( unsigned int iMat = 0; iMat < m_vectMatrix[0].size(); iMat++ )
      if ( m_vectMatrix[iVar][iMat] ) m_vectMatrix[iVar][iMat]->Write( CreateHistMatName( m_matrixNames[iMat], iVar ).c_str(), TObject::kOverwrite );
  }

  //Save Setting variables
  //  err = m_setting.Save( outFile );
  // if ( err ) {
  //   cout << "Setting::Save() failed : " << err << endl;
  //   return 2;
  // }

  // if ( saveChiMatrix ) {
  //   for ( auto vChiMatrixLine : m_chiMatrix ) {
  //     for ( auto vChiMatrix : vChiMatrixLine ) {
  //       vChiMatrix->Save(outFile, 1);
  //       vChiMatrix->Save(outFile, 0);
  //     }
  //   }
  // }

  outFile->Close();
  delete outFile;
  outFile = 0;

  if ( m_setting.GetDebug() ) cout << "Template::Save Done" << endl;
  return 0;
}

//######################=
int TemplateMethod::Template::CreateTemplate() {
  if ( m_setting.GetDebug() ) cout << "Template::CreateTemplate" << endl;
  //Decide which variables to extract and how to cut the detector
  vector<double> etaBins = m_setting.GetEtaBins();
  vector<double> ptBins = m_setting.GetPtBins();
  //In case of pt bins, there will be one more bin than ptBins, hence i_eta must reach ptBins.size()
  int eta1Max = (int) etaBins.size()-1;
  int eta2Max = 0;

  //Setup ChiMatrix
  for ( int i_eta = 0; i_eta < eta1Max; i_eta++ ) {
    m_chiMatrix.push_back( vector< ChiMatrix * >() );

    //If only eta binning : we do a tringular matrix
    //else we do a full matrix
    eta2Max = ( m_setting.GetMode() == "1VAR" ) ? i_eta+1 : (int) ptBins.size()-1;


    //Create default ChiMatrix object
    for ( int j_eta = 0; j_eta < eta2Max; j_eta++ ) {
      m_chiMatrix.back().push_back( 0 );
      m_chiMatrix.back().back() = new ChiMatrix( string( TString::Format( "ChiMatrix_%i_%i", i_eta, j_eta )), m_setting );
    }}

  //Fill MC events into templates and check execution time
  FillDistrib( false );
  //If there is no data input, create pseudo data
  // Checks are made at the crettion of the Class : if there is no data, there MUST be a MC to create pseudo data
  if ( !m_dataFileNames.size() ) {
    if ( m_setting.GetDoSimulation() ) CreateDistordedTree();
    else {
      cout << "Error : No data and simulation off" << endl;
      return 2;
    }
    cout << "create distorded" << endl;
  }
  //If data events haven't been filled
  else  FillDistrib( true );

  //Create templates for each configuration
  for ( unsigned int i_eta = 0; i_eta < m_chiMatrix.size(); i_eta++ ) {
    for ( unsigned int j_eta = 0; j_eta < m_chiMatrix[i_eta].size(); j_eta++ ) {
      //if (i_eta!=38 || j_eta!=5) continue;
      m_chiMatrix[i_eta][j_eta]->CreateTemplates();
    }}

  if ( m_setting.GetDebug() ) cout << "Template::CreateTemplate Done" << endl;
  return 0;
}

//############################
int TemplateMethod::Template::ExtractFactors() {
  if ( m_setting.GetDebug() )  cout << "Template : ExtractFactors" << endl;

  if ( ! m_chiMatrix.size() ) {
    //Create templates if they haven't been loaded
    if ( m_MCFileNames.size() ) CreateTemplate();
    else throw runtime_error( "TemplateMethod::Template::ExtractFactors : No MCNtuple and no loaded templates" );
  }

  if ( !m_setting.GetNEventData() ) FillDistrib( true );
  //Checks that all factors matrices are empty

  CleanMatrixVect();

  //Decide which variables to extract and how to cut the detector
  vector<double> etaBins = m_setting.GetEtaBins();
  vector<double> ptBins = m_setting.GetPtBins();
  vector<double> alphaSimEta = m_setting.GetAlphaSimEta();
  vector<double> alphaSimPt  = m_setting.GetAlphaSimPt();
  vector<double> sigmaSimEta = m_setting.GetSigmaSimEta();
  vector<double> sigmaSimPt  = m_setting.GetSigmaSimPt();

  string xVar = m_setting.GetMCBranchVarNames().at( "ETA_CALO_1" );
  ReplaceString( "_1" )( xVar );
  bool isChi2Done = false;
  for ( unsigned int iVar = 0; iVar < m_vectHist.size(); iVar++ ) {

    bool isMeasuredVar =  (m_setting.GetDoScale() && !iVar) || (iVar && m_setting.GetDoSmearing() );
    if ( !isMeasuredVar ) continue;

    //In case of pt bins, there will be one more bin than ptBins, hence i_eta must reach ptBins.size()
    int eta1Max = static_cast<int>(etaBins.size() -1);
    int eta2Max = ( m_setting.GetMode() == "1VAR" ) ? eta1Max : static_cast<int>(ptBins.size())-1;

    unsigned int histDevBin = SearchVectorBin( string("deviation"), m_histNames );
    unsigned int matCombinBin = SearchVectorBin( string("combin"), m_matrixNames );
    unsigned int matErrBin = SearchVectorBin( string("combinErr"), m_matrixNames );
    unsigned int histMeasBin = SearchVectorBin( string("measScale"), m_histNames );

    //Create an histogram of inputs in case of closure
    if ( m_setting.GetMode() == "1VAR" && ((!m_dataFileNames.size() && m_setting.GetDoSimulation() ) || TString(m_setting.GetDataName()).Contains("distorded") )) {
      if ( isMeasuredVar ) {
        unsigned int histBin = SearchVectorBin( string("inputScale"), m_histNames );
        string histName = CreateHistMatName( m_histNames[histBin], iVar );
        m_vectHist[iVar][histBin] = new TH1D( histName.c_str(), histName.c_str(), etaBins.size()-1, (double*) &etaBins[0] );
        m_vectHist[iVar][histBin]->GetXaxis()->SetTitle( xVar.c_str() );
        m_vectHist[iVar][histBin]->GetYaxis()->SetTitle( iVar ? "C" : "#alpha" );
        for ( int i = 0; i < static_cast<int>(alphaSimEta.size()); i++ ) {
          m_vectHist[iVar][histBin]->SetBinContent( i+1, iVar ? sigmaSimEta[i] : alphaSimEta[i] );
          m_vectHist[iVar][histBin]->SetBinError( i+1, 0);
        }

        histName = CreateHistMatName( m_histNames[histDevBin], iVar );
        m_vectHist[iVar][histDevBin] = new TH2F( histName.c_str(), histName.c_str(), eta1Max , -0.5, eta1Max-0.5, eta2Max, -0.5, eta2Max - 0.5);
      }
    }


    //Create combined factor matrices
    for ( unsigned int iMat = 0; iMat < m_matrixNames.size(); iMat++ )
      m_vectMatrix[iVar][iMat] = new TMatrixD( eta1Max, eta2Max  );

    //Run over all chiMatrices
    for ( int i_eta = 0; i_eta < eta1Max; i_eta++ ) {
      if ( m_setting.GetMode() == "1VAR" ) eta2Max =  (int) i_eta+1;

      for ( int j_eta = 0; j_eta < eta2Max; j_eta++ ) {
        if ( !isChi2Done )  m_chiMatrix[i_eta][j_eta]->FitChi2();
        // Make symmetric matrices of combined alpha and their values in order to apply the formulae
        (*m_vectMatrix[iVar][matCombinBin])(i_eta, j_eta) =  ( !m_chiMatrix[i_eta][j_eta]->GetQuality() ) ? m_chiMatrix[i_eta][j_eta]->GetScale(iVar) : 0;
        (*m_vectMatrix[iVar][matErrBin])(i_eta, j_eta) =  ( !m_chiMatrix[i_eta][j_eta]->GetQuality() ) ? m_chiMatrix[i_eta][j_eta]->GetErrScale(iVar) : 100;

        if ( m_setting.GetMode() == "1VAR" ) {
          //Symetrize coimbinMatrix if only 1VAR
          (*m_vectMatrix[iVar][matCombinBin])(j_eta, i_eta) = (*m_vectMatrix[iVar][matCombinBin])(i_eta, j_eta);
          (*m_vectMatrix[iVar][matErrBin])(j_eta, i_eta) = (*m_vectMatrix[iVar][matErrBin])(i_eta, j_eta);
        }

        if ( m_vectHist[iVar][histDevBin] && !m_chiMatrix[i_eta][j_eta]->GetQuality() ) {
          double alphaTh =  ( m_setting.GetMode() == "1VAR" ) ?
            ( !iVar ? (alphaSimEta[i_eta] + alphaSimEta[j_eta])/2.
              : sqrt((sigmaSimEta[i_eta]*sigmaSimEta[i_eta] + sigmaSimEta[j_eta]*sigmaSimEta[j_eta])/2.) )
            : ( !iVar ? (alphaSimPt[i_eta] + alphaSimEta[j_eta])/2.
                : sqrt((sigmaSimPt[i_eta]*sigmaSimPt[i_eta]+sigmaSimEta[j_eta]*sigmaSimEta[j_eta])/2.) );
          m_vectHist[iVar][histDevBin]->SetBinContent( i_eta+1, j_eta+1,  ((*m_vectMatrix[iVar][matCombinBin])(i_eta, j_eta) - alphaTh ) / (*m_vectMatrix[iVar][matErrBin])(i_eta, j_eta) );
        }
      }
    } //end loop on chiMatrix

    if ( isMeasuredVar  ) {
      bool is2Var = m_setting.GetMode() == "2VAR" ;
      TMatrixD resultMatrix( eta1Max, is2Var ? eta2Max : 1 );
      TMatrixD resultErrMatrix( eta1Max, is2Var ? eta2Max : 1  );
      unsigned int inversionMethod = is2Var ? 13 : (iVar ? m_setting.GetInversionMethod() : 0);
      if ( is2Var ) {
        inversionMethod = iVar ? 14 : 13;
        resultMatrix = *m_vectMatrix[iVar][matCombinBin];
        resultErrMatrix = *m_vectMatrix[iVar][matErrBin];
      }
      else InvertMatrix( *m_vectMatrix[iVar][matCombinBin], *m_vectMatrix[iVar][matErrBin], resultMatrix, resultErrMatrix, inversionMethod );
      string histName = CreateHistMatName( m_histNames[histMeasBin], iVar );
      if ( is2Var ) m_vectHist[iVar][histMeasBin] = new TH2D( histName.c_str(), histName.c_str(), etaBins.size()-1, (double*) &etaBins[0], ptBins.size()-1, (double*) &ptBins[0] );
      else m_vectHist[iVar][histMeasBin] = new TH1D( histName.c_str(), histName.c_str(), etaBins.size()-1, (double*) &etaBins[0] );

      m_vectHist[iVar][histMeasBin]->GetXaxis()->SetTitle( xVar.c_str() );
      string yTitle = ( iVar ? "C" : "#alpha");
      if ( is2Var ) yTitle = ReplaceString("_2")( m_setting.GetMCBranchVarNames().at( "ETA_CALO_2" ) );
      m_vectHist[iVar][histMeasBin]->GetYaxis()->SetTitle( yTitle.c_str() );

      for ( int iBin = 0; iBin < resultMatrix.GetNrows(); iBin++ ) {
        for ( int jBin = 0; jBin < resultMatrix.GetNcols(); jBin++ ) {
          if ( is2Var ) {
            m_vectHist[iVar][histMeasBin]->SetBinContent( iBin+1, jBin+1, resultMatrix(iBin,jBin) );
            m_vectHist[iVar][histMeasBin]->SetBinError( iBin+1, jBin+1,  resultErrMatrix(iBin,jBin) );
          }
          else {
            m_vectHist[iVar][histMeasBin]->SetBinContent( iBin+1, resultMatrix(iBin,0) );
            m_vectHist[iVar][histMeasBin]->SetBinError( iBin+1, resultErrMatrix(iBin,0) );
          }
        }
      }
    }//end isMeasured
    isChi2Done = true;
   }//end loop iVar

  if ( m_setting.GetDebug() )  cout << "Template : ExtractFactors Done" << endl;
  return 0;
  }

//###########################################==
void TemplateMethod::Template::FillDistrib( bool isData ) {
  if ( m_setting.GetDebug() )  cout << "Template : FillDistrib " << isData << endl;
  //  clock_t tStart = clock();

  if ( isData ) m_setting.SetNEventData(0);
  else m_setting.SetNEventMC(0);

  double weight=1;
  unsigned int nEntry = ( isData && m_setting.GetNUseEvent() ) ? m_setting.GetNUseEvent() : 0;
  unsigned int nFiles = ( isData ) ? m_dataFileNames.size() : m_MCFileNames.size();
  unsigned long int counterEntry = 0;

  const map<string, string> &mapBranchNames = isData ? m_setting.GetDataBranchVarNames() : m_setting.GetMCBranchVarNames();
  FillBranchesToLink( isData );

  vector<string> requiredBranches = { "RUNNUMER", "PHI_CALO_1", "PHI_CALO_2"};
  bool doRemoveHV = 1;
  for ( auto &s : requiredBranches )
    if ( mapBranchNames.find(s) == mapBranchNames.end() ) doRemoveHV=0;

  for ( unsigned int iFile = 0; iFile < nFiles; iFile++ ) {

    TFile *inputFile = new TFile( isData  ? m_dataFileNames[iFile].c_str() : m_MCFileNames[iFile].c_str() );
    TTree *inputTree = static_cast<TTree*>(inputFile->Get( ( isData ) ? m_dataTreeNames[iFile].c_str() : m_MCTreeNames[iFile].c_str() ));

    if ( m_setting.GetSelection() != "" &&
         ( !m_setting.GetApplySelection()
           || ( m_setting.GetApplySelection()==1 &&  isData )
           || ( m_setting.GetApplySelection()==2 && !isData ) )
           ) {
      TTree* dumTree = inputTree->CopyTree( m_setting.GetSelection().c_str() );
      if ( !dumTree->GetEntries() ) throw runtime_error( "Template::FillDistrib : The desired selection leads to no events" );
    }

    //inputTree->SetDirectory( 0 );
    m_mapBranches.LinkTreeBranches( inputTree, 0, m_branchesToLink );

    for ( unsigned int iEvent = 0; iEvent < inputTree->GetEntries(); iEvent++ ) {
      if ( nEntry && counterEntry== nEntry ) { cout << "returning : " << counterEntry << endl;return;}

      inputTree->GetEntry( iEvent );
      if ( doRemoveHV && !RemoveHVDeadZones( m_mapBranches, isData ) ) continue;

      double mass = m_mapBranches.GetDouble(mapBranchNames.at("MASS"));
      weight = GetWeight(isData);
      //##############################
      if ( isData ) m_setting.SetNEventData();
      else m_setting.SetNEventMC();

      unsigned int i_eta = 0, j_eta = 0;
      if ( m_setting.GetMode() == "1VAR" ) {
        int foundBin = FindBin( i_eta, j_eta, 0, mapBranchNames );
        if ( !foundBin ) m_chiMatrix[i_eta][j_eta]->FillDistrib( mass, isData,  weight );
      }
      else {
        if ( FindBin( i_eta, j_eta, 0, mapBranchNames ) || FindBin( i_eta, j_eta, 1, mapBranchNames ) ) continue;
        FindBin( i_eta, j_eta, 0, mapBranchNames );
        m_chiMatrix[i_eta][j_eta]->FillDistrib( mass, isData, weight/2. );
        FindBin( i_eta, j_eta, 1, mapBranchNames );
        m_chiMatrix[i_eta][j_eta]->FillDistrib( mass, isData, weight/2. );
      }
      counterEntry++;
    }//end loop iEvent
     delete inputTree; inputTree = 0;
    inputFile->Close("R");
    delete inputFile; inputFile = 0;
  }//end loop iFile

  if ( m_setting.GetDebug() )  cout << "Template : FillDistrib Done" << endl;

}
//###############################==
void TemplateMethod::Template::CreateDistordedTree( string outFileName ) {
  cout << "Template::CreateDistordedTree" << endl;

  const vector< double > &alphaSimEta = m_setting.GetAlphaSimEta();
  const vector< double > &alphaSimPt = m_setting.GetAlphaSimPt();
  const vector< double > &sigmaSimEta = m_setting.GetSigmaSimEta();
  const vector< double > &sigmaSimPt = m_setting.GetSigmaSimPt();

  vector< TTree* > vectorTree;

  TTree *MCTree {0};
  TTree *bootTree {0};
  TFile *distorded {0};
  TTree *dataTree {0};
  TFile *MCFile {0};

  if ( alphaSimEta.size()!= sigmaSimEta.size()
       || ( m_setting.GetEtaBins().size() && ( alphaSimEta.size() != m_setting.GetEtaBins().size()-1) )
       || alphaSimPt.size() != sigmaSimPt.size()
       || ( m_setting.GetPtBins().size() && (sigmaSimPt.size() !=  m_setting.GetPtBins().size()-1) )
       ) {
    cout << (alphaSimEta.size()!= sigmaSimEta.size()) << " " << alphaSimEta.size() << " " << sigmaSimEta.size() << endl ;
    cout << ( m_setting.GetEtaBins().size() && ( alphaSimEta.size() != m_setting.GetEtaBins().size()-1) ) << endl ;
    cout << (alphaSimPt.size() != sigmaSimPt.size()) << " " << alphaSimPt.size() << " " << sigmaSimPt.size() << endl ;
    cout << ( m_setting.GetPtBins().size() && (sigmaSimPt.size() !=  m_setting.GetPtBins().size()-1) ) << endl;
    throw invalid_argument( "Template::CreateDistordedTree Simulation vector sizes do not match" );
  }

  if ( m_setting.GetIndepDistorded() == 1 ) {
    high_resolution_clock::time_point t1 = high_resolution_clock::now();
    m_rand.SetSeed( t1.time_since_epoch().count() );
  }
  else if ( m_setting.GetIndepDistorded() ) m_rand.SetSeed(  m_setting.GetIndepDistorded() );

  if ( m_setting.GetBootstrap() ) {
    TFile *inFile {0};
    TFile *distordedFile {0};

    for ( unsigned int iFile = 0; iFile < m_MCFileNames.size(); ++iFile ) {
      inFile =TFile::Open( m_MCFileNames[iFile].c_str() );
      MCTree = static_cast<TTree*>(inFile->Get( m_MCTreeNames[iFile].c_str() ));
      vectorTree.push_back(MCTree);
    }

    distordedFile=new TFile( string( StripString( m_MCFileNames.front() )+ "_bootstrap.root").c_str(), "RECREATE" );
    bootTree = Bootstrap( vectorTree, m_setting.GetNUseEvent(), m_setting.GetBootstrap(), 1);
    bootTree->Write( "", TObject::kOverwrite );
    m_MCFileNames = { distordedFile->GetName() };
    m_MCTreeNames = { bootTree->GetName() };

    DeleteContainer( vectorTree );

    distordedFile->Close();
    delete distordedFile; distordedFile = 0;
    inFile->Close();
    delete inFile; inFile = 0;
  }//end bootstrap


  if ( outFileName=="" ) outFileName= m_name + "_distorted.root";
  cout << "outDistordedFileName : " << outFileName << endl;
  string treeName = StripString(outFileName);
  distorded = new TFile( outFileName.c_str(), "RECREATE" );
  dataTree = new TTree( treeName.c_str(), treeName.c_str() );
  m_setting.SetDataName( dataTree->GetName() );

  const map<string,string> &mapBranchNames = m_setting.GetMCBranchVarNames();

  for ( unsigned int iFile = 0; iFile < m_MCFileNames.size(); iFile++ ) {
    MCFile = new TFile( m_MCFileNames[iFile].c_str() );
    MCTree = static_cast<TTree*>(MCFile->Get( m_MCTreeNames[iFile].c_str() ));
    m_mapBranches.LinkTreeBranches( MCTree, dataTree, m_branchesToLink );
    for ( unsigned int iEvent = 0; iEvent < MCTree->GetEntries(); ++iEvent ) {
      MCTree->GetEntry( iEvent );

      unsigned int i_eta = 0, j_eta = 0;
      if ( FindBin( i_eta, j_eta, 0, mapBranchNames ) ) continue;
      if ( m_setting.GetMode() == "2VAR" && FindBin( i_eta, j_eta, 1, mapBranchNames ) ) continue;

      double factor1=1, factor2=1;
      for ( unsigned int iSwap = 0; iSwap < (m_setting.GetMode()=="2VAR" ? 2 : 1); iSwap++ ){
        FindBin( i_eta, j_eta, iSwap, mapBranchNames );
        factor1 *= ( 1 + alphaSimEta[i_eta] ) * ( 1 + m_rand.Gaus(0,1)*sigmaSimEta[i_eta] );
        factor2 *= ( 1 + alphaSimEta[j_eta] ) * ( 1 + m_rand.Gaus(0,1)*sigmaSimEta[j_eta] );
      }

      RescaleMapVar( factor1, factor2, mapBranchNames.at("MASS") );
      dataTree->Fill();
      if (iEvent%100000==0) cout<<iEvent<<" factor1 "<<factor1<<endl;
    }
  }

  cout << "tree entries : " << dataTree->GetEntries() << endl;
  cout << "Writting in : " << outFileName.c_str() << endl;

  distorded->cd();
  dataTree->Write( "", TObject::kOverwrite );

  m_dataFileNames = { distorded->GetName() };
  m_dataTreeNames = { dataTree->GetName() };

  MCFile->Close();
  delete MCFile; MCFile = 0;
  distorded->Close();
  delete distorded; distorded = 0;

  if ( m_setting.GetDebug() )  cout << "Template : CreateDistordedTree Done " << endl;
}

//####################################################==
void TemplateMethod::Template::MakePlot( string path, string latexFileName ) {

  if ( m_setting.GetDebug() )  cout << "Template::MakePlot" << endl;
  if ( path.back() != '/' && path != "" ) path += "/";

  if ( latexFileName == "" ) {
    if ( m_name != "" ) latexFileName = m_name + ".tex";
    else latexFileName = "latex.tex";
  }

  if ( m_setting.GetDebug() ) cout << "latexFile : " << path << "/" << latexFileName << endl;

  unsigned int histMeasBin = SearchVectorBin( string("measScale"), m_histNames );
  unsigned int histInputBin = SearchVectorBin( string("inputScale"), m_histNames );
  const string var1Name = m_setting.GetMCBranchVarNames().at( "ETA_CALO_1" );;
  const string var2Name = m_setting.GetMode() != "1VAR" ? m_setting.GetMCBranchVarNames().at( "ETA_CALO_2" ) : "";
  //Prepare a latex file to store plots
  fstream latex;
  TString dumName;
  latex.open( path + latexFileName, fstream::out | fstream::trunc );
  WriteLatexHeader( latex, "Antinea Guerguichon" );
  //Give the main info about the analysis
  latex << "Mass Distribution : " << m_setting.GetZMassNBins() << " " << m_setting.GetZMassMin() << " " << m_setting.GetZMassMax() << "\\newline" << endl;
  dumName = m_setting.GetMCName();
  dumName.ReplaceAll("_", "\\_");
  latex << "Template : " << dumName << "\\newline" << endl;
  latex << "Events : " << m_setting.GetNEventMC() << "\\newline" << endl;
  dumName = m_setting.GetDataName();
  dumName.ReplaceAll("_", "\\_");
  latex << "Data : " << dumName << "\\newline" << endl;
  latex << "Events : " << m_setting.GetNEventData() << "\\newline" << endl;
  dumName = var1Name;
  dumName.ReplaceAll("_", "\\_");
  latex << "Variable1 : " << dumName << " \\newline" << endl;
  if ( m_setting.GetMode() != "1VAR" )  {
    dumName = m_setting.GetMCBranchVarNames().at( "ETA_CALO_2" );
    dumName.ReplaceAll("_", "\\_");
    latex << "Variable2 : " << dumName << endl;
  }
  latex << "Fit Method : " << m_setting.GetFitMethod() << "\\newline" << endl;
  latex << "nUseEl : " << m_setting.GetNUseEl() << "\\newline" << endl;
  latex << "nEventCut : " << m_setting.GetNEventCut() << "\\newline" << endl;
  latex << "Selection : " << m_setting.GetSelection() << "\\newline" << endl;
  latex << "\\tableofcontents\\clearpage" << endl;

  latex << "\\section{Results}" << endl;

  //Create the result pdf in case of bining in eta only
  //  if ( m_setting.GetMode() == "1VAR"  ) {
  bool is2Var = m_setting.GetMode() == "2VAR" ;
  bool isClosure = TString(m_setting.GetDataName()).Contains("_distorded");

  TString tabularPattern = TString( 'l', 2 + (2 + isClosure ) *(m_setting.GetDoScale() + m_setting.GetDoSmearing() ) + ( is2Var ? 2 : 0 ) );
  latex << "\\begin{center}" << endl;
  latex << "\\begin{tabular}{|" << tabularPattern << "|}" << endl;
  latex << "\\hline" << endl;
  latex << "$" << var1Name << "$& bin &";
  if ( is2Var ) latex << "$" + var2Name + "$&bin&" ;
  if ( m_setting.GetDoScale() ) {
    if ( isClosure ) latex << "$\\alpha_{input}$ & ";
    latex << "$\\alpha$ & $\\Delta\\alpha$ " ;
    if ( m_setting.GetDoSmearing() ) latex << " & ";
  }

  if ( m_setting.GetDoSmearing() ) {
    if ( isClosure ) latex << "$\\sigma_{input}$ & ";
    latex << "$\\sigma$ & $\\Delta\\sigma$" ;
  }
  latex << "\\\\" << endl;
  latex << "\\hline " << endl;

  vector< double > etaBins = m_setting.GetEtaBins();
  vector< double > ptBins;
  vector< double > alphaSimPt = m_setting.GetAlphaSimPt();
  vector< double > sigmaSimPt = m_setting.GetSigmaSimPt();
  if ( is2Var ) {
    ptBins = m_setting.GetPtBins();
  }

  vector< double > alphaSimEta = m_setting.GetAlphaSimEta();
  vector< double > sigmaSimEta = m_setting.GetSigmaSimEta();

  //fill the tabuilar with measured values
  for ( int i_bin = 0; i_bin < (int) etaBins.size()-1; i_bin++ ) {
    unsigned int jMax =  is2Var ? ptBins.size()-1 : 1;
    for ( unsigned int jBin=0; jBin<jMax; jBin++ ) {
      //Deal with bin description
      latex  << "$] " << etaBins[i_bin] << " , " << etaBins[i_bin+1] << " ]$ & " << i_bin ;
      if ( is2Var ) latex << "&$] " << ptBins[jBin] << " , " << ptBins[jBin+1] << " ]$ & " << jBin ;

      if ( isClosure ) {
        string color = "";
        double inputValue = 0;
        if ( m_setting.GetDoScale() ) {
          inputValue = is2Var ? (1+alphaSimEta[i_bin])*(1+alphaSimPt[jBin])-1 : alphaSimEta[i_bin];
          color = GetColorTabular( inputValue, m_vectHist[0][histMeasBin]->GetBinContent( i_bin+1 ), m_vectHist[0][histMeasBin]->GetBinError( i_bin+1 ) );
          latex << " & " << inputValue;
          latex << " & \\textcolor{" << color << "}{"<< m_vectHist[0][histMeasBin]->GetBinContent( i_bin +1 ) << "} & \\textcolor{" << color << "}{" << m_vectHist[0][histMeasBin]->GetBinError( i_bin +1) << "}";
        }
        if ( m_setting.GetDoSmearing() ) {
          inputValue = is2Var ? sqrt(sigmaSimEta[i_bin]*sigmaSimEta[i_bin] + sigmaSimPt[jBin]*sigmaSimPt[jBin] ) : sigmaSimEta[i_bin];
          color = GetColorTabular( inputValue, m_vectHist[1][histMeasBin]->GetBinContent( i_bin+1 ), m_vectHist[1][histMeasBin]->GetBinError( i_bin + 1 ) );
          latex << " & " << inputValue;
          latex << " & \\textcolor{" << color << "}{"<< m_vectHist[1][histMeasBin]->GetBinContent( i_bin +1 ) << "} & \\textcolor{" << color << "}{" << m_vectHist[1][histMeasBin]->GetBinError( i_bin +1) << "}";
        }
      }
      else {
        if ( m_setting.GetDoScale() ) latex << " & " << m_vectHist[0][histMeasBin]->GetBinContent( i_bin +1) << " & " << m_vectHist[0][histMeasBin]->GetBinError( i_bin +1) ;
        if ( m_setting.GetDoSmearing() ) latex << " & " << m_vectHist[1][histMeasBin]->GetBinContent( i_bin +1) << " & " << m_vectHist[1][histMeasBin]->GetBinError( i_bin +1);
      }
      latex << "\\\\" << endl;
    }
  }//end iBin

  latex << "\\hline";
  latex << "\\end{tabular}" << endl;
  latex << "\\end{center}" << endl;

  vector< string > plotNames;
  unsigned int histDevBin = SearchVectorBin( string("deviation"), m_histNames );
  DrawOptions drawOpt;

  for ( unsigned int iVar = 0; iVar< m_vectHist.size(); iVar++ ) {
    for ( unsigned int iHist = 0; iHist< m_vectHist[0].size(); iHist++ ) {
      if ( iHist != histMeasBin && iHist != histDevBin ) continue;
      if ( m_vectHist[iVar][iHist] ) {
        string plotName = path + m_vectHist[iVar][iHist]->GetName();
        vector<TH1*> histPlot = { m_vectHist[iVar][iHist] };
        if ( m_vectHist[iVar][histInputBin] && iHist==histMeasBin ) histPlot.insert( histPlot.begin(), m_vectHist[iVar][histInputBin] );
        drawOpt.AddOption( "outName", plotName );
        if ( isClosure ) drawOpt.AddOption( "doRatio", "2");
        drawOpt.Draw( histPlot );
        plotNames.push_back( plotName );
      }
    }
  }
  WriteLatexMinipage( latex, plotNames, 2 );
  // }//end 1VAR

  for ( unsigned int i_eta = 0; i_eta < m_chiMatrix.size(); i_eta++ ) {
    for ( unsigned int j_eta = 0; j_eta < m_chiMatrix[i_eta].size(); j_eta++ ) {
      m_chiMatrix[i_eta][j_eta]->MakePlot( m_sStream );
    }
  }


  latex << "\\clearpage" << endl;
  latex << m_sStream.str() << endl;
  latex << "\\end{document}" << endl;
  latex.close();

  string commandLine = "pdflatex -interaction=batchmode " + path + latexFileName;
  //string commandLine = "pdflatex " + path + latexFileName;

  cout << "latexFileName : " << commandLine << endl;
  int err = system( commandLine.c_str() );
  err = system( commandLine.c_str() );
  err = system( commandLine.c_str() );
  cout << "isPdfCompiled : " << !err << endl;

  if ( m_setting.GetDebug() )  cout << "Template::MakePlot Done" << endl;
}
//#################################################=
 int TemplateMethod::Template::FindBin( unsigned int &i_eta, unsigned int &j_eta, const bool swapEl, const map<string,string> &mapBranchNames ) {
  vector< double > etaBins = m_setting.GetEtaBins();
  vector< double > ptBins = m_setting.GetPtBins();

  i_eta = 0;
  j_eta = 0;

  string varName =  "ETA_CALO_" + to_string( 1 + (m_setting.GetMode() == "2VAR" && swapEl));
  double eta1 = m_mapBranches.GetDouble( mapBranchNames.at(varName));

  varName = ( m_setting.GetMode() == "2VAR" ) ? "PT_" + to_string( 1 + swapEl) : "ETA_CALO_2";
  double eta2 = m_mapBranches.GetDouble( mapBranchNames.at(varName) );

  if ( m_setting.GetDoSymBin() ) {
    eta1 = fabs(eta1);
    eta2 = fabs(eta2);
  }

  if ( m_setting.GetMode() == "1VAR" && eta1 < eta2 ) swap( eta1, eta2 );

  if ( eta1 <= etaBins[0] || eta1 > etaBins.back() ) return 1;
  while ( i_eta <  etaBins.size()-1 && eta1 > etaBins[i_eta+1] ) i_eta++;

  if ( m_setting.GetMode() == "1VAR" ) {
    if ( eta2 <= etaBins[0] || eta2 > etaBins.back() ) return 2;
    while ( j_eta <  etaBins.size()-1 && eta2 >  etaBins[j_eta+1] )  j_eta++;
  }
  else {
    if ( eta2 < -10 ) {
      cout << "eta2 : " << eta2 << endl;
      cout << "ptBins : " << ptBins[0] << endl;
      cout << "passSell : " << ( eta2<=ptBins[0] ) << endl;
    }
    if ( eta2 <= ptBins[0] || eta2 > ptBins.back() ) return 3;
    while ( j_eta <  ptBins.size() && eta2 >  ptBins[j_eta+1] )  j_eta++;
  }


  return 0;
}

//#################################################
void TemplateMethod::Template::ClearChiMatrix() {
  while ( m_chiMatrix.size() ) {
    while ( m_chiMatrix.back().size() ) {
      if ( m_chiMatrix.back().back() ) delete m_chiMatrix.back().back();
      m_chiMatrix.back().back()=0;
      m_chiMatrix.back().pop_back();
    }
    m_chiMatrix.pop_back();
  }
}

//###################################################"
string TemplateMethod::Template::GetColorTabular( double inputVal, double measVal, double uncertVal ) {

  double nSigma = fabs( inputVal - measVal ) / uncertVal;

  if ( nSigma > 3 ) return "red";
  else if ( nSigma > 1 ) return "blue";
  else return "black";

}

//######################################################
void TemplateMethod::Template::RescaleMapVar( double factor1, double factor2, const string &key ) {
  double valD{m_mapBranches.GetDouble(key)*sqrt(factor2*factor1)};
  float valF = valD;
  if ( m_mapBranches.IsFloat(key) ) m_mapBranches.SetVal( key, valF );
  else m_mapBranches.SetVal( key, valD );
}
//######################################################
int TemplateMethod::Template::ApplyCorrection( TH1D* correctionAlpha, TH1D *correctionSigma ) {
  if ( m_setting.GetDebug() )cout<< "Template::ApplyCorrection"<<endl;

  if ( !correctionAlpha && !correctionSigma ) return 0;

  string dumString="";
  TString outFileName = "";

  for ( unsigned int iCorrection = 0; iCorrection < 2; iCorrection++ ) {

    if (  iCorrection && !correctionSigma ) continue;
    if ( !iCorrection && !correctionAlpha ) continue;
    const map<string, string> &mapBranchNames = iCorrection ? m_setting.GetMCBranchVarNames() : m_setting.GetDataBranchVarNames();
    if ( m_setting.GetDebug() )cout << "correcting : " << iCorrection << endl;
    unsigned int nFile = ( iCorrection ) ? m_MCFileNames.size() : m_dataFileNames.size() ;
    cout << "nFile : " << nFile << endl;

    for ( unsigned int iFile = 0; iFile < nFile; iFile++ ) {

      dumString = ( iCorrection ) ? m_MCFileNames[iFile] : m_dataFileNames[iFile];
      cout << "correcting : " << dumString << endl;
      TFile *dataFile = new TFile( dumString.c_str() );

      dumString = ( iCorrection ) ? m_MCTreeNames[iFile] : m_dataTreeNames[iFile];
      TTree *dataTree = (TTree*) dataFile->Get( dumString.c_str() );

      outFileName = ( iCorrection ) ? m_MCFileNames[iFile] : m_dataFileNames[iFile];
      outFileName.ReplaceAll( ".root", "_corrected.root" );
      TFile *distorded = new TFile( outFileName, "RECREATE" );

      dumString = ( iCorrection ) ? "correctedMC" : "correctedData";
      TTree *dumTree = new TTree( dumString.c_str(), dumString.c_str() );


      m_mapBranches.LinkTreeBranches( dataTree, dumTree, m_branchesToLink );

      for ( unsigned int iEvent = 0; iEvent < dataTree->GetEntries(); iEvent++ ) {
        dataTree->GetEntry( iEvent );

        vector<double> factors(2);
        for ( unsigned i=0; i<factors.size(); ++i ) {
          TH1 *hist = iCorrection ? correctionSigma : correctionAlpha;
          //string varName = string( hist->GetXaxis()->GetTitle() );// + "_" + to_string(i+1);
          string varName = "ETA_CALO_" + to_string(i+1);
          double scale = hist->GetBinContent( hist->FindFixBin( m_mapBranches.GetDouble( mapBranchNames.at(varName) ) ) );
          //double scale = hist->GetBinContent( hist->FindFixBin( m_mapBranches.GetDouble( varName ) ) );
          if ( iCorrection ) scale*=m_rand.Gaus();
          factors[i] = 1 - scale;
        }

        RescaleMapVar( factors.front(), factors.back(), mapBranchNames.at("MASS") );
        dumTree->Fill();
      }
      delete dataTree;
      dataFile->Close("R");
      delete dataFile;


      cout << "saving : " << outFileName << endl;
      dumTree->Write( "", TObject::kOverwrite );

      if ( iCorrection ) {
        m_MCFileNames[iFile] = outFileName;
        m_MCTreeNames[iFile] = dumTree->GetName();
      }
      else {
        m_dataFileNames[iFile] = distorded->GetName();
        m_dataTreeNames[iFile] = dumTree->GetName();
     }
      distorded->Close();
      delete distorded;

    }//end iFile

  }//end if correctionAlpha
  if ( m_setting.GetDebug() )  cout << "Template : ApplyCorrection Done" << endl;
  return 0;
}

// //######################################"
TMatrixD* TemplateMethod::Template::GetMatrix( string matrixName ) {
  if ( matrixName == "alpha" ) return m_vectMatrix[0][SearchVectorBin( string("combin"), m_matrixNames )];
  else if ( matrixName == "sigma" ) return m_vectMatrix[1][SearchVectorBin( string("combin"), m_matrixNames )];
  else if ( matrixName == "errAlpha" ) return m_vectMatrix[0][SearchVectorBin( string("combinErr"), m_matrixNames )];
  else if ( matrixName == "errSigma" ) return m_vectMatrix[1][SearchVectorBin( string("combinErr"), m_matrixNames )];
  return 0;
}

///###########################################
ChiMatrix* TemplateMethod::Template::GetChiMatrix( unsigned int iMatrix, unsigned int jMatrix ) {
  if ( iMatrix < m_chiMatrix.size() && jMatrix < m_chiMatrix[iMatrix].size() ) return m_chiMatrix[iMatrix][jMatrix];
  else return 0;
}

//##########################################
TH1 *TemplateMethod::Template::GetResults( string resultName ) {
  if ( resultName == "alpha" ) return m_vectHist[0][SearchVectorBin( string("measScale"), m_histNames )];
  else if ( resultName == "sigma" ) return m_vectHist[1][SearchVectorBin( string("measScale"), m_histNames )];
  else return 0;
}


//##############################################
void TemplateMethod::Template::CleanHistVect( int jVar ) {
  for ( unsigned int iVar = 0; iVar < m_vectHist.size(); iVar++ ) {
    if ( jVar != -1 && jVar != (int) iVar ) continue;
    for ( unsigned int iHist = 0; iHist < m_vectHist[0].size(); iHist++ ) {
      if ( m_vectHist[iVar][iHist] ) delete m_vectHist[iVar][iHist];
      m_vectHist[iVar][iHist] = 0;
    }}
}

//###################################################"
void TemplateMethod::Template::CleanMatrixVect( int jVar) {
  for ( unsigned int iVar = 0; iVar < m_vectMatrix.size(); iVar++ ) {
    if ( jVar != -1 && jVar != (int) iVar ) continue;
    for ( unsigned int iHist = 0; iHist < m_vectMatrix[iVar].size(); iHist++ ) {

      if ( m_vectMatrix[iVar][iHist] ) delete m_vectMatrix[iVar][iHist];
      m_vectMatrix[iVar][iHist] = 0;
    }}
}

//#############################
double TemplateMethod::Template::GetWeight( bool isData ) {
  double weight=1;
  vector<string> dumVect = isData ? m_setting.GetDataBranchWeightNames() : m_setting.GetMCBranchWeightNames();
  for ( unsigned int iName = 0; iName < dumVect.size(); iName++ ) {
    weight *= m_mapBranches.GetDouble( dumVect[iName] );
  }
  return weight;
}
//==============================
void TemplateMethod::Template::FillBranchesToLink( const bool isData ) {
  m_branchesToLink.clear();
  const map<string, string> &mapBranchNames = isData ? m_setting.GetDataBranchVarNames() : m_setting.GetMCBranchVarNames();
  for ( auto it=mapBranchNames.begin(); it!=mapBranchNames.end(); ++it )
    m_branchesToLink.push_back( it->second );

  const vector<string> weightNames = isData ? m_setting.GetDataBranchWeightNames() : m_setting.GetMCBranchWeightNames();
  for ( auto it=weightNames.begin(); it!=weightNames.end(); ++it )
    m_branchesToLink.push_back( *it );


  m_branchesToLink.sort();
  m_branchesToLink.erase( unique( m_branchesToLink.begin(), m_branchesToLink.end()), m_branchesToLink.end() );

}
//=======================================
bool TemplateMethod::Template::RemoveHVDeadZones( ChrisLib::MapBranches &event, bool isData ) {

  const map<string, string> &mapBranchNames = isData ? m_setting.GetDataBranchVarNames() : m_setting.GetMCBranchVarNames();
  double runnumber = event.GetDouble( mapBranchNames.at("RUNNUMBER"));

  for ( int iEl=1; iEl<=2; ++iEl ) {
    double eta_calo = event.GetDouble( mapBranchNames.at("PHI_CALO_"+to_string(iEl)));
    double phi_calo = event.GetDouble( mapBranchNames.at("PHI_CALO_"+to_string(iEl)));

    if ((runnumber>=296938.5 && runnumber<298966.5) ||
        (runnumber>=299143.5 && runnumber<300278.5)){
      if (   eta_calo > - 1.825
             && eta_calo < -1.5
             && phi_calo > -1.104921
             && phi_calo < -0.956748){
        return false;
      }
    }

    if ((runnumber>=298966.5 && runnumber<299143.5 ) ||
        (runnumber>=300278.5 && runnumber< 305290.5)){
      if (eta_calo > - 1.825
          && eta_calo < -1.5
          && phi_calo > -1.104921
          && phi_calo < -0.956748){
        return false;
      }

      if (eta_calo> - 1.825
          && eta_calo < -1.5
          && phi_calo > 1.054922
          && phi_calo < 1.203097){
        return false;
      }
    }
  }

  return true;

}
