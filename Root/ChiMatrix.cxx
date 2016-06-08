#include "Template/ChiMatrix.h"
#include <string>
#include <iostream>
#include "TLorentzVector.h"
#include "PlotFunctions/SideFunctions.h"
#include "TCanvas.h"
#include "TF1.h"
#include "TFitResult.h"
#include "TLegend.h"
#include <fstream>
#include <chrono>
#include "PlotFunctions/DrawPlot.h"
#include "TAxis.h"
#include <sstream>

using std::stringstream;
using std::string;
using std::cout;
using std::endl;
using std::fstream;
using std::max;
using std::min;
using std::bitset;
using namespace std::chrono;

ChiMatrix::ChiMatrix() : m_alpha(-99), m_sigma(-99),
			 m_rand(),
			 m_errAlpha(-99), m_errSigma(-99),  
			 m_alphaMin( -0.5 ), m_alphaMax( 0 ), m_sigmaMin( 0 ), m_sigmaMax( 0.05 ), m_quality(), m_eta1Bin(0), m_eta2Bin(0)

{
  TH1::SetDefaultSumw2( true );
  m_setting = 0;
  m_chiMatrix = 0;
  m_MCZMass.clear();
  m_dataZMass = 0;
  m_chi2FitNonConstVar.clear();
  m_chi2FitConstVar = 0;
  m_corAngle = 0;
  m_scaleValues.clear();
  m_sigmaValues.clear();
  m_MCTree = 0;
}

ChiMatrix::ChiMatrix( string name ) : ChiMatrix()
{
  m_name = name;
  //Get the m_etaBin from the name
  name = m_name.substr( m_name.find_first_of("_")+1 );
  m_eta1Bin = atoi( name.substr( 0, name.find_first_of("_") ).c_str() );
  m_eta2Bin = atoi( name.substr(name.find_last_of("_") +1).c_str() );
  m_rand.SetSeed( m_eta1Bin*100+m_eta2Bin+1 );
  if ( m_name == "ChiMatrix_0_0" ) cout << "rand seed : " << m_rand.GetSeed() << endl;
}

ChiMatrix::ChiMatrix( string name, Setting &configSetting ) : ChiMatrix( name )
{
  m_setting = &configSetting;

  m_alphaMin = ( m_setting->GetDoScale() ) ? m_setting->GetAlphaMin() : - 0.5;
  m_alphaMax = ( m_setting->GetDoScale() ) ? m_setting->GetAlphaMax() : 0.5 ;
  m_sigmaMin  = ( m_setting->GetDoSmearing() ) ? m_setting->GetSigmaMin() : -0.5;
  m_sigmaMax  = ( m_setting->GetDoSmearing() ) ? m_setting->GetSigmaMax() : 0.5;

  m_dataZMass = new TH1D( TString( m_name + "_dataZMass"), "DataZMass", m_setting->GetZMassNBins(), m_setting->GetZMassMin(), m_setting->GetZMassMax() );    
  m_dataZMass->GetXaxis()->SetTitle( "M_{ee}" );

}

ChiMatrix::~ChiMatrix() {
  m_setting = 0;
  if ( m_chiMatrix ) delete m_chiMatrix; m_chiMatrix = 0;
  if ( m_dataZMass ) delete m_dataZMass; m_dataZMass = 0;

  while ( m_chi2FitNonConstVar.size() ) {
    if ( m_chi2FitNonConstVar.back() ) delete m_chi2FitNonConstVar.back();
    m_chi2FitNonConstVar.back() = 0;
    m_chi2FitNonConstVar.pop_back();
  }

  if ( m_chi2FitConstVar )  delete m_chi2FitConstVar; m_chi2FitConstVar = 0;
  if ( m_corAngle ) delete m_corAngle; m_corAngle = 0;
  if ( m_MCTree ) delete m_MCTree; m_MCTree = 0;
  ClearTemplates();
}

//############## SETTER
void ChiMatrix::SetSetting( Setting &setting ) {
  if ( m_setting->GetDebug() ) cout << "Setting::SetSetting" <<endl;

  if  ( m_setting && m_setting != &setting )  delete m_setting;
  m_setting = &setting;

  if ( m_setting->GetDebug() ) cout << "Setting::SetSetting Done" <<endl;
}

//############## METHOD
int ChiMatrix::Load( TFile *inFile, bool justTemplate ) {
  if ( m_setting->GetDebug() ) cout << "ChiMatrix::LoadTemplate : " << m_name<< endl;

  ClearTemplates();

  FillScaleValues();

  int alphaMaxBin = ( m_setting->GetDoScale() ) ? m_setting->GetAlphaNBins() : 0;
  int sigmaMaxBin = ( m_setting->GetDoSmearing() ) ? m_setting->GetSigmaNBins() : 0;

  if ( justTemplate ) {
    for ( int i_alpha = 0; i_alpha <= alphaMaxBin; i_alpha++ ) {
      m_MCZMass.push_back( vector< TH1D* > () );
      for ( int i_sigma = 0; i_sigma <= sigmaMaxBin; i_sigma++ ) {
	TString histName = TString::Format("%s_MCZMass_sc%i_sm%i", m_name.c_str(), (int) (m_scaleValues[i_alpha]*1e6),  (int) (m_sigmaValues[i_sigma]*1e6));
	m_MCZMass.back().push_back( 0 );
	m_MCZMass.back().back() = (TH1D* ) inFile->Get( histName );
	if ( ! m_MCZMass[i_alpha][i_sigma] ) {
	  m_quality.set( 1, 1 );
	  cout << "Bad configuration : " << histName << endl;
	  return 0;
	}
	m_MCZMass.back().back()->SetDirectory(0);   
      }}}

  if ( !justTemplate ) {
    
    if ( m_chiMatrix && inFile->Get( TString( m_name + "_chiMatrix" ) ) ) delete m_chiMatrix;
    m_chiMatrix = (TH2D*) inFile->Get( TString( m_name + "_chiMatrix" ) );
    if ( m_chiMatrix ) m_chiMatrix->SetDirectory(0);

    if ( m_dataZMass && inFile->Get( TString( m_name + "_dataZMass" )) ) delete m_dataZMass;
    m_dataZMass = (TH1D*) inFile->Get( TString( m_name + "_dataZMass" ) );
    if ( m_dataZMass ) m_dataZMass->SetDirectory(0);

    if ( m_chi2FitConstVar && inFile->Get( TString( m_name + "_chi2FitConstVar" ) ) ) delete m_chi2FitConstVar;
    m_chi2FitConstVar = (TH1D*) inFile->Get( TString( m_name + "_chi2FitConstVar" ) );
    if ( m_chi2FitConstVar ) m_chi2FitConstVar->SetDirectory(0);

    if ( m_corAngle && inFile->Get( TString( m_name + "_corAngle" ) ) ) delete m_corAngle;
    m_corAngle = (TH1D*) inFile->Get( TString( m_name + "_corAngle" ) );
    if ( m_corAngle ) m_corAngle->SetDirectory( 0 );

    TTree *infoTree = (TTree*) inFile->Get( TString( m_name + "_infoTree" ) );

    cout << "got all" << endl;
    if  (!m_chiMatrix || !m_dataZMass || !m_chi2FitConstVar || !m_corAngle || !infoTree) {
      if ( m_MCZMass.size() ) {
	cout << "Histogram could not be found :";
	cout << " m_chiMatrix:" << m_chiMatrix;
	cout << " m_dataZMass:" << m_dataZMass;
	cout << " m_chi2FitConstVar:" << m_chi2FitConstVar;
	cout << " m_corAngle:" << m_corAngle;
	cout << " infoTree:" << infoTree << endl;
	m_quality.set( 3, 1 );
	return 4;
      }
      else { 
	m_quality.set( 3, 1 );
	return 0;
      }
    }

    while ( m_chi2FitNonConstVar.size() ) {
      delete m_chi2FitNonConstVar.back();
      m_chi2FitNonConstVar.back() =0;
      m_chi2FitNonConstVar.pop_back();
    }
    while ( inFile->Get(  TString::Format( "%s_chi2FitNonConstVar_%i", m_name.c_str() , (int) m_chi2FitNonConstVar.size()+1 ) ) ) {
      m_chi2FitNonConstVar.push_back(0);
      m_chi2FitNonConstVar.back() = (TH1D*) inFile->Get( TString::Format( "%s_chi2FitNonConstVar_%i", m_name.c_str() , (int) m_chi2FitNonConstVar.size() ) );
      if ( m_chi2FitNonConstVar.back() ) m_chi2FitNonConstVar.back()->SetDirectory(0);
    }
    if ( !m_chi2FitNonConstVar.size() ) {
      cout << "No chi2FitNonConstVar have been found" << endl;
      return 4;
    }
    

  //Load values of alpha and sigma
    infoTree->SetBranchAddress( "alpha", &m_alpha );
    infoTree->SetBranchAddress( "sigma", &m_sigma );
    infoTree->SetBranchAddress( "errAlpha", &m_errAlpha );
    infoTree->SetBranchAddress( "errSigma", &m_errSigma );
    infoTree->GetEntry( 0 );
    delete infoTree;
    infoTree=0;
  }//justTemplate

  if ( m_setting->GetDebug() ) cout << "ChiMatrix::LoadTemplate Done" << endl;
  return 0;
}

//========================
int  ChiMatrix::Save( TFile *outFile, bool justTemplate ) {
  if ( m_setting->GetDebug() ) cout << m_name << "::Save" << endl;
  if ( m_quality.to_ulong() ) return 0;

  if ( !outFile ) {
    cout << "TFile is a 0 pointer" << endl;
    return 1;}

  if ( !outFile->IsOpen() ) {
    cout << "TFile is not opened" << endl;
    return 2;
  }

  outFile->cd();

  if ( justTemplate ) {
    for ( unsigned int i_alpha = 0; i_alpha <  m_MCZMass.size(); i_alpha++ ) {
      for ( unsigned int i_sigma = 0; i_sigma <  m_MCZMass.back().size(); i_sigma++ ) {
	m_MCZMass[i_alpha][i_sigma]->Write( "", TObject::kOverwrite );
      }}

  }
  else {
     if ( m_chiMatrix ) m_chiMatrix->Write( "", TObject::kOverwrite );
     if ( m_chi2FitConstVar ) m_chi2FitConstVar->Write( "", TObject::kOverwrite );
     if ( m_corAngle )        m_corAngle->Write( "", TObject::kOverwrite );
     for ( unsigned int i = 0; i < m_chi2FitNonConstVar.size() ; i++ ) {
       m_chi2FitNonConstVar[i]->Write( "", TObject::kOverwrite );
     }
    if ( m_dataZMass ) m_dataZMass->Write( "", TObject::kOverwrite );   

    string titleTree = m_name + "_infoTree";
    TTree *infoTree = new TTree( titleTree.c_str(), titleTree.c_str() );
    infoTree->Branch( "alpha", &m_alpha );
    infoTree->Branch( "sigma", &m_sigma );
    infoTree->Branch( "errAlpha", &m_errAlpha );
    infoTree->Branch( "errSigma", &m_errSigma );
    infoTree->Fill();
    infoTree->Write( "", TObject::kOverwrite );
    delete infoTree; infoTree=0;
  }


  if ( m_setting->GetDebug() ) cout << "ChiMatrix::Save Done" << endl;
  return 0;
}

//============
int ChiMatrix::FillChiMatrix(  ) {
  if ( m_setting->GetDebug() ) cout << m_name << " :FillChiMatrix" <<endl;

  if ( IsGoodQuality() )     return 0;
  
  int alphaMaxBin = ( m_setting->GetDoScale() ) ?  (int) m_MCZMass.size()-1 : 0;
  int sigmaMaxBin = ( m_setting->GetDoSmearing() ) ? (int) m_MCZMass.back().size()-1 : 0;

  double alphaWidth = ( alphaMaxBin ) ? ( m_alphaMax - m_alphaMin ) / alphaMaxBin : 0.5;
  double sigmaWidth =  ( sigmaMaxBin  ) ? ( m_sigmaMax - m_sigmaMin ) / sigmaMaxBin : 0.5;

  if ( m_chiMatrix ) delete m_chiMatrix; m_chiMatrix=0;
  m_chiMatrix = new TH2D( TString( m_name + "_chiMatrix" ), "ChiMatrix" , alphaMaxBin + 1, m_alphaMin - alphaWidth/2., m_alphaMax + alphaWidth/2., sigmaMaxBin + 1, m_sigmaMin - sigmaWidth/2., m_sigmaMax + sigmaWidth/2.);
  m_chiMatrix->GetXaxis()->SetTitle( "#alpha" );
  m_chiMatrix->GetYaxis()->SetTitle( "#sigma" );


  //Normalize data distribution
  //  m_dataZMass->Sumw2();
  if ( m_dataZMass->Integral() !=0 ) m_dataZMass->Scale( 1/ m_dataZMass->Integral() );
  else {
    cout << "null integral for dataZMass in fillChiMatrix " << endl;
    cout << "entries : " << m_dataZMass->GetEntries() << " " << m_dataZMass->Integral() << endl;
    exit(0);
  }
  

  //Fill the chi2 matrix
  for ( unsigned int i_alpha = 0; i_alpha < m_MCZMass.size(); i_alpha++ ) {

      int i_sigmaEnd   = ( m_setting->GetDoSmearing() ) ? (int) m_MCZMass[i_alpha].size() : 1;
    for ( int i_sigma = 0; i_sigma < i_sigmaEnd; i_sigma++ ) {
      //Normalize MC distribution
      //      m_MCZMass[i_alpha][i_sigma]->Sumw2();
      m_MCZMass[i_alpha][i_sigma]->Scale( 1/ m_MCZMass[i_alpha][i_sigma]->Integral() );

      double chi = ComputeChi2( m_MCZMass[i_alpha][i_sigma], m_setting->GetNUseEl() );
      m_chiMatrix->SetBinContent( i_alpha+1, i_sigma+1, chi );
      m_chiMatrix->SetBinError( i_alpha+1, i_sigma+1, 0.1);

    }
  }

  if ( m_setting->GetDebug() ) cout << m_name << " : FillChiMatrix Done" <<endl;  
  return 0;
}

//==========
void ChiMatrix::FillDistrib( TLorentzVector &e1, TLorentzVector &e2, bool isData, double weight ) {
  //if ( m_setting->GetDebug() ) cout << m_name << " : FillDistrib" <<endl;
  //  cout << "GetIndepTempaltes : " << m_setting->GetIndepTemplates() << endl;

  
  if ( isData ) {
    m_dataZMass->Fill( (e1+e2).M() / 1000., weight );
  }
  else {

    if ( !m_MCTree ) CreateMCTree();
    m_mapVar1["PT"] = e1.Pt();
    m_mapVar1["ETA_TRK"] = e1.Eta();
    m_mapVar1["PHI"] = e1.Phi();
    m_mapVar2["PT"] = e2.Pt();
    m_mapVar2["ETA_TRK"] = e2.Eta();
    m_mapVar2["PHI"] = e2.Phi();
    m_mapVarEvent["WEIGHT"]=weight;
    m_MCTree->Fill();
  }
}

//=======================================
void ChiMatrix::FillTemplates( ) {
  //  if ( m_setting->GetDebug() ) cout << "ChiMatrix::FillTemplates" << endl;
  if (! m_setting->GetIndepTemplates() ) m_rand.SetSeed( m_eta1Bin*100+m_eta2Bin+1 );  
  else if ( m_setting->GetIndepTemplates() == 1 ) {
    cout << "setting new Template seed ChiMatrix" << endl;
    high_resolution_clock::time_point t1 = high_resolution_clock::now();
    m_rand.SetSeed( t1.time_since_epoch().count() );
  }
  else m_rand.SetSeed( m_setting->GetIndepTemplates()+m_eta1Bin*100+m_eta2Bin+1 );  


  //cout<<"IndepTemplates Seed:  "<<m_rand.GetSeed()<<endl;

  LinkMCTree();
  unsigned int imax = m_setting->GetNUseEl();
  for ( unsigned int iEvent = 0; iEvent<m_MCTree->GetEntries(); iEvent++ ) {
    m_MCTree->GetEntry( iEvent );
    for ( unsigned int useEl = 0; useEl<imax; useEl++ ) {
      double randVal1 =  m_rand.Gaus();
      double randVal2 =  m_rand.Gaus();
      for ( int i_alpha = 0; i_alpha < (int) m_MCZMass.size(); i_alpha++ ) {	            
	for ( int i_sigma = 0; i_sigma < (int) m_MCZMass[i_alpha].size(); i_sigma++ ) {
	  	  
	  double factor1Alpha = 1 + ( m_MCZMass.size()==1 ? ( m_setting->GetDoScale() ? (m_alphaMax + m_alphaMin)/2. : 0.) : m_scaleValues[i_alpha] );
	  double factor2Alpha = 1 + ( m_MCZMass.size()==1 ? ( m_setting->GetDoScale() ? (m_alphaMax + m_alphaMin)/2. : 0.) :m_scaleValues[i_alpha]  );

	  double factor1Sigma = 1 + randVal1 *( m_MCZMass[i_alpha].size()!=1 ? m_sigmaValues[i_sigma] : 0 );
	  double factor2Sigma = 1 + randVal2 *( m_MCZMass[i_alpha].size()!=1 ? m_sigmaValues[i_sigma] : 0 );

	  double pt_1 = m_mapVar1["PT"] * factor1Alpha * factor1Sigma;
	  double pt_2 = m_mapVar2["PT"] * factor2Alpha * factor2Sigma;
	  TLorentzVector dum_el1, dum_el2;
	  dum_el1.SetPtEtaPhiM( pt_1, m_mapVar1["ETA_TRK"], m_mapVar1["PHI"], 0.511 );
	  dum_el2.SetPtEtaPhiM( pt_2, m_mapVar2["ETA_TRK"], m_mapVar2["PHI"], 0.511 );
	  TLorentzVector Z = dum_el1 + dum_el2;

	  if ( Z.M()/1000. < m_setting->GetZMassMin() || Z.M()/1000. > m_setting->GetZMassMax() ) continue;
	  m_MCZMass[i_alpha][i_sigma]->Fill( Z.M() /1000., m_mapVarEvent["WEIGHT"] );
	  
      }}}
  }
  //  if ( m_setting->GetDebug() ) cout << "ChiMatrix::FillTemplates Done" << endl;
}
	
//==========================================

void ChiMatrix::FitChi2() {
  if ( m_setting->GetDebug() ) cout << m_name << "::FitChi2()" << endl;

  if ( m_quality.to_ulong() ) {
    cout << m_name << " : bad quality (" << m_quality.to_ulong() << ") : returns " << endl;
    m_alpha = 0;
    m_errAlpha = 100;
    m_sigma = 0;
    m_errSigma = 100;
    return;
  }

  FillChiMatrix();

  TF1 *fittingFunction = 0;

  if ( m_setting->GetDoScale() && m_setting->GetDoSmearing()) {      

  //Get the informations for the histograms definition
    int constVarBins = ( m_setting->GetConstVarFit() == "ALPHA" ) ? m_chiMatrix->GetNbinsX() : ( ( m_setting->GetDoSmearing() ) ? m_chiMatrix->GetNbinsY() : 1 );
    double constVarMin = ( m_setting->GetConstVarFit() == "ALPHA" ) ? m_chiMatrix->GetXaxis()->GetXmin() : m_chiMatrix->GetYaxis()->GetXmin();
    double constVarMax = ( m_setting->GetConstVarFit() == "ALPHA" ) ? m_chiMatrix->GetXaxis()->GetXmax() : m_chiMatrix->GetYaxis()->GetXmax();
    string constVarLabel = ( m_setting->GetConstVarFit() == "ALPHA" ) ? "#alpha" : "c";
    string nConstVarLabel = ( m_setting->GetConstVarFit() != "ALPHA" ) ? "#alpha" : "c";
    
    //Create the histograms accrodingly to the parameters
    m_chi2FitConstVar = new TH1D( TString( m_name + "_chi2FitConstVar" ), "chi2FitConstVar",  constVarBins  , constVarMin, constVarMax );
    m_chi2FitConstVar->GetXaxis()->SetTitle( constVarLabel.c_str() );
    m_chi2FitConstVar->GetYaxis()->SetTitle( "#chi^{2}" );
    
    m_corAngle = new TH1D( TString( m_name + "_corAngle" ), "corAngle",  constVarBins , constVarMin, constVarMax );
    m_corAngle->GetXaxis()->SetTitle( constVarLabel.c_str() );
    m_corAngle->GetYaxis()->SetTitle( nConstVarLabel.c_str() );
    
    for ( int iConstVarBin = 1; iConstVarBin < constVarBins + 1; iConstVarBin++ ) {

      //Fill a 1D histogram to fit
      m_chi2FitNonConstVar.push_back( 0 );
      m_chi2FitNonConstVar.back() = ( m_setting->GetConstVarFit() == "SIGMA" ) ? m_chiMatrix->ProjectionX( TString::Format("%s_chi2FitNonConstVar_%d", m_name.c_str(), iConstVarBin ), iConstVarBin, iConstVarBin, "o")
	: m_chiMatrix->ProjectionY( TString::Format("%s_chi2FitNonConstVar_%d", m_name.c_str(), iConstVarBin ), iConstVarBin, iConstVarBin, "o");
      m_chi2FitNonConstVar.back()->GetXaxis()->SetTitle( nConstVarLabel.c_str() );
      m_chi2FitNonConstVar.back()->GetYaxis()->SetTitle( "#chi^{2}" );

      //Create the fit
      fittingFunction = FitHist( m_chi2FitNonConstVar.back(), m_setting->GetConstVarFit() == "SIGMA" ? 0 : m_setting->GetFitMethod(), 0, 0 );
      if ( fittingFunction ) {              
	double alphaMin = fittingFunction->GetParameter(2);
	double alphaErr = fittingFunction->GetParameter(1);
	double chi2Min  = fittingFunction->GetParameter(0);
	m_chi2FitConstVar->SetBinContent( iConstVarBin, chi2Min );
	m_chi2FitConstVar->SetBinError( iConstVarBin, 1e-3 );
	
	m_corAngle->SetBinContent( iConstVarBin, alphaMin );
	m_corAngle->SetBinError( iConstVarBin, alphaErr);
      }
      else cout << "fitHist failed" << endl;
      if ( fittingFunction ) delete fittingFunction; fittingFunction=0;
    }//End loop on constVar bins
  }//end if doScale && doSmearing
  else m_chi2FitConstVar =  ( m_setting->GetDoScale() ) ? m_chiMatrix->ProjectionX( TString::Format("%s_chi2FitConstVarFit", m_name.c_str() ), 1, 1, "o") : m_chiMatrix->ProjectionY( TString::Format("%s_chi2FitConstVarFit", m_name.c_str() ), 1, 1, "o");

  // Create a bool which will be used several times
  // Is sigma the variable into constVarFit?
  bool isSigmaConstVar = m_setting->GetDoSmearing() && ( !m_setting->GetDoScale() || (m_setting->GetDoScale() && m_setting->GetConstVarFit() == "SIGMA" ) );
  auto mode = ( m_setting->GetDoSmearing() && m_setting->GetConstVarFit() == "SIGMA") ?  m_setting->GetFitMethod() : 0;
  fittingFunction = FitHist( m_chi2FitConstVar , mode, 0, 0 );

  if ( fittingFunction ) {  
    if ( isSigmaConstVar ) {
      m_sigma = max( fittingFunction->GetParameter(2), 0.); 
      m_errSigma = fittingFunction->GetParameter(1);

      if ( m_setting->GetFitMethod() == 4 ) {
	//Find the minimum of the distribution within 2 sigma of the fit minimum
	double minChi = m_chi2FitConstVar->GetBinContent( m_chi2FitConstVar->FindBin( m_sigma) );
	for ( int bin = max( m_chi2FitConstVar->FindBin( m_sigma - 2*m_errSigma ), 1); bin <= min( m_chi2FitConstVar->FindBin( m_sigma +2*m_errSigma ), m_chi2FitConstVar->GetNbinsX() ); bin++ ) {
	  if ( m_chi2FitConstVar->GetBinContent( bin ) > minChi ) continue;
	  minChi = m_chi2FitConstVar->GetBinContent( bin );
	  m_sigma = max( 0., m_chi2FitConstVar->GetXaxis()->GetBinCenter( bin ) );
	}
      }
    }
    else {
      m_alpha = fittingFunction->GetParameter(2);
      m_errAlpha = fittingFunction->GetParameter(1);
    }

    delete fittingFunction; fittingFunction=0;
  }
  else m_quality.set( 0, 1 );
  
  if ( m_setting->GetDoScale() && m_setting->GetDoSmearing() ) {
    //We compute now m_alpha with the coreelationangle
    
    //Find the bin corresponding to sigma
    double constVarVal = ( isSigmaConstVar ) ? m_sigma : m_alpha;
    int constVarBin = min( max( 1, m_corAngle->FindFixBin( constVarVal ) ), m_corAngle->GetNbinsX() );
    TF1 *linearFit = new TF1( "linearFit", "[0]*(x-[1])+[2]", m_corAngle->GetXaxis()->GetBinLowEdge(constVarBin-1), m_corAngle->GetXaxis()->GetBinUpEdge(constVarBin+1) );
    linearFit->SetParameter( 0, 0 );
    linearFit->SetParameter( 1, constVarVal );
    linearFit->SetParLimits( 1, constVarVal, constVarVal ); 
    linearFit->SetParameter( 2, m_corAngle->GetBinContent( constVarBin ) );
    
    m_corAngle->Fit( linearFit , "Q", "Q",  m_corAngle->GetXaxis()->GetBinLowEdge( max( 1, constVarBin -2 ) ), m_corAngle->GetXaxis()->GetBinUpEdge( min( m_corAngle->GetNbinsX(), constVarBin+2 ) ));
    
    if ( !isSigmaConstVar ) {
      m_sigma = max( 0., linearFit->GetParameter( 2 )); 
      m_errSigma = m_corAngle->GetBinError( constVarBin );
    }
    else {
      m_alpha = linearFit->GetParameter( 2 ); 
      m_errAlpha = m_corAngle->GetBinError( constVarBin );
    }
    delete linearFit; linearFit=0;
  }
  cout << m_name << " scales : " << endl;
  cout << "alpha : " << m_alpha << " +- " << m_errAlpha << endl; 
  cout << "sigma : " << m_sigma << " +- " << m_errSigma << endl;
  if ( m_setting->GetDebug() ) cout << "ChiMatrix::FitChi2() done " << endl << endl;;
}
//====================================================
void ChiMatrix::MakePlot( stringstream &ss, string path ) {
  if ( m_setting->GetDebug() )  cout << "ChiMatrix::MakePlot " << m_name << endl;
  if ( m_quality.to_ulong() ) return;

  vector<string> plotNames, legends;
  string plotName;

  int bestAlpha = ( m_setting->GetDoScale() ) ? m_chiMatrix->GetXaxis()->FindFixBin( m_alpha )-1 : 0;
  int bestSigma = ( m_setting->GetDoSmearing() ) ?  m_chiMatrix->GetYaxis()->FindFixBin( m_sigma ) -1 : 0;
  if ( bestAlpha < 0 ) bestAlpha = 0;
  if ( bestAlpha > m_chiMatrix->GetNbinsX()-1 ) bestAlpha = m_chiMatrix->GetNbinsX()-1;
  if ( bestSigma < 0 ) bestSigma = 0;
  if ( bestSigma > m_chiMatrix->GetNbinsY()-1 ) bestSigma = m_chiMatrix->GetNbinsX()-1;

  TString dumName = m_name;
  dumName.ReplaceAll("_", "\\_");
  ss << "\\section{" << dumName << "}" << endl;

  vector<double> etaBins(m_setting->GetEtaBins());

  //Compute the expected values for alpha and c
  double expAlpha=0, expC=0;
  vector<double> alphaSimEta = m_setting->GetAlphaSimEta();
  vector<double> alphaSimPt = m_setting->GetAlphaSimPt();
  vector<double> sigmaSimEta = m_setting->GetSigmaSimEta();
  vector<double> sigmaSimPt = m_setting->GetSigmaSimPt();

  bool isClosure = TString(m_setting->GetDataName()).Contains("_distorded");

  if ( isClosure ) expAlpha = ( m_setting->GetMode() == "1VAR" ) ? (alphaSimEta[m_eta1Bin] + alphaSimEta[m_eta2Bin])/2. : (alphaSimEta[m_eta1Bin] + alphaSimPt[m_eta2Bin])/2. ;
  if ( isClosure ) expC = (   m_setting->GetMode() == "1VAR" ) ? sqrt((sigmaSimEta[m_eta1Bin]*sigmaSimEta[m_eta1Bin] + sigmaSimEta[m_eta2Bin]*sigmaSimEta[m_eta2Bin])/2.) : sqrt((sigmaSimEta[m_eta1Bin]*sigmaSimEta[m_eta1Bin] + sigmaSimPt[m_eta2Bin]*sigmaSimPt[m_eta2Bin])/2.); 
  ss << "\\begin{minipage}{0.49\\linewidth} Results \\newline" << endl;
  if ( m_MCZMass.size() && m_MCZMass.front().size() )  ss << "MCEvents : " << m_MCZMass.front().front()->GetEntries() << "\\newline" << endl;
  ss << "DataEvents : " << m_dataZMass->GetEntries() <<" \\newline" << endl;
  ss << "ThresholdMass : " << 27*sqrt(2*(TMath::CosH( (etaBins[m_eta1Bin+1]+etaBins[m_eta1Bin]-etaBins[m_eta2Bin+1]-etaBins[m_eta2Bin])/2.)+1)) << "\\\\" << endl;
  if ( m_setting->GetDoSimulation() || TString(m_setting->GetDataName()).Contains("distorded"))  ss << "$\\alpha_{ij}^{th}=" << expAlpha << "$     $c_{ij}^{th}=" << expC << "$" << endl;
  if ( m_setting->GetDoScale() )    ss << "$$\\alpha_{ij} = " << m_alpha << "\\pm " << m_errAlpha << "$$" << endl;
  if ( m_setting->GetDoSmearing() ) ss << "$$\\sigma_{ij} = " << m_sigma << "\\pm " << m_errSigma << "$$" << endl;
  ss << "\\end{minipage}\\hfill" << endl;
  plotName = path + m_name + "_chiMatrix";
  vector<TH1*> dumVect = {m_chiMatrix};
  DrawPlot( dumVect, plotName );
  WriteLatexMinipage( ss, {plotName}, 2 );

  // //Comparison data and extrmal alpha templates
  if ( m_MCZMass.size() && m_MCZMass.front().size() ) {
    if ( m_setting->GetDoScale() ) {
      legends.clear();
      legends.push_back( "legend=Data; m=__MEAN" );
      legends.push_back( string(TString::Format("legend=Template : alpha=%i; m=__MEAN",(int) ( m_scaleValues.front()*1e6)) ) );
      legends.push_back( string(TString::Format("legend=Template : alpha=%i", (int) (m_scaleValues.back()*1e6)) ) );
      legends.push_back("doRatio=1");
      plotName = TString( path + m_name + "_CompareAlpha" );
      dumVect = { m_dataZMass, m_MCZMass[0][bestSigma], m_MCZMass.back()[bestSigma]};
      DrawPlot( dumVect, plotName, legends );
      plotNames.push_back( plotName   );
    }
  
    if ( m_setting->GetDoSmearing() ) {
      legends.clear();
      legends.push_back( "legend=Data" );
      legends.push_back( string(TString::Format("legend=Template : sigma=%i",(int) ( m_sigmaValues.front()*1e6) ) ));
      legends.push_back( string(TString::Format("legend=Template : sigma=%i", (int) (m_sigmaValues.back()*1e6) )));
      plotName = path + m_name + "_CompareSigma";
      dumVect = { m_dataZMass, m_MCZMass[bestAlpha].front(), m_MCZMass[bestAlpha].back()};
      DrawPlot( dumVect, plotName, legends );
      plotNames.push_back( plotName );
    }
  }
  
  plotName = path + m_name + "_chi2FitConstVar";
  dumVect = { m_chi2FitConstVar };
  DrawPlot( dumVect, plotName );
  plotNames.push_back( plotName );

  if ( m_corAngle ) {
    plotName = path + m_name + "_corAngle";
    dumVect = { m_corAngle};
    DrawPlot( dumVect, plotName );
    plotNames.push_back( plotName );
  }
  WriteLatexMinipage( ss, plotNames, 2 );

  plotNames.clear();
  // for ( int i=0; i< (int) m_chi2FitNonConstVar.size(); i++ ) {
  //   plotName = path + m_chi2FitNonConstVar[i]->GetName();
  //   DrawPlot( { m_chi2FitNonConstVar[i] }, plotName );
  //   plotNames.push_back( plotName );
  // }
  // WriteLatexMinipage( ss, plotNames, 4 );

  if ( m_setting->GetDebug() )  cout << "ChiMatrix::MakePlot Done" << endl;
}


//=========================================
int ChiMatrix::CreateTemplates( int nTemplates ) {
  if ( m_setting->GetDebug() )  cout << m_name << "::CreateTemplate" << endl;

  if ( m_setting->GetOptimizeRanges() ) OptimizeRanges();
  ClearTemplates();
  if ( m_quality.to_ulong() ) return 0;

  int alphaMaxBin = ( m_setting->GetDoScale() ) ? ( nTemplates ) ? nTemplates : m_setting->GetAlphaNBins() : 0;
  int sigmaMaxBin = ( m_setting->GetDoSmearing() ) ? ( nTemplates ) ? nTemplates : m_setting->GetSigmaNBins() : 0;

  FillScaleValues( nTemplates );  
  for ( int i_alpha = 0; i_alpha <= alphaMaxBin; i_alpha++ ) {
    m_MCZMass.push_back( vector< TH1D* > () );
    for ( int i_sigma = 0; i_sigma <= sigmaMaxBin; i_sigma++ ) {
      m_MCZMass.back().push_back( 0 );
      m_MCZMass.back().back() = new TH1D( TString::Format( "%s_MCZMass_sc%d_sm%d", m_name.c_str() ,(int) (m_scaleValues[i_alpha]*1e6),  (int) (m_sigmaValues[i_sigma]*1e6) ), TString::Format( "MCZMass_sc%i_sm%d", (int) (m_scaleValues[i_alpha]*1e6), (int) (m_sigmaValues[i_sigma]*1e6) ), m_setting->GetZMassNBins(), m_setting->GetZMassMin(), m_setting->GetZMassMax() );  
      m_MCZMass.back().back()->GetXaxis()->SetTitle( "M_{ee}" );
    }}

  FillTemplates();
  FillChiMatrix();

  if ( m_setting->GetDebug() )  cout << "ChiMatrix::CreateTemplate Done" << endl;
  return 0;
}

//==============================
void ChiMatrix::FillScaleValues( int nTemplates ) {
  //  if ( m_setting->GetDebug() ) cout << "FillScaleValues" << endl;
  m_scaleValues.clear();
  m_sigmaValues.clear();

  int alphaMaxBin = ( m_setting->GetDoScale() ) ? ( nTemplates ) ? nTemplates : m_setting->GetAlphaNBins() : 0;
  int sigmaMaxBin = ( m_setting->GetDoSmearing() ) ? ( nTemplates ) ? nTemplates : m_setting->GetSigmaNBins() : 0;

  if ( !alphaMaxBin ) m_scaleValues.push_back( ( m_alphaMin != m_setting->GetAlphaMin() || m_alphaMax != m_setting->GetAlphaMax() ) ? (m_alphaMin + m_alphaMax)/2 : 0);
  else {
  for ( int i_alpha = 0; i_alpha <=alphaMaxBin; i_alpha++ ) {
    double scale = ( m_setting->GetDoScale() ) ? m_alphaMin + ( m_alphaMax - m_alphaMin ) /  alphaMaxBin * i_alpha : (m_alphaMax-m_alphaMin)/2.;
    m_scaleValues.push_back( scale );
  }}
    
  if ( !sigmaMaxBin ) m_sigmaValues.push_back( ( m_sigmaMin != m_setting->GetSigmaMin() || m_sigmaMax != m_setting->GetSigmaMax() ) ? (m_sigmaMin + m_sigmaMax)/2 : 0);
  else {
  for ( int i_sigma = 0; i_sigma <= sigmaMaxBin; i_sigma++ ) {
    double smear =  m_sigmaMin + ( m_sigmaMax - m_sigmaMin ) / sigmaMaxBin * i_sigma;
    m_sigmaValues.push_back( smear );
  }}

  //  if ( m_setting->GetDebug() ) cout << "FillScaleValues Done" << endl;
}


//===========================================
void ChiMatrix::OptimizeRanges( ) {
  if ( m_setting->GetDebug() ) cout << m_name << "::OptimizeRanges() " << m_name << endl;

  TH1D *histScale = 0;
  double chiOptim = m_setting->GetOptimizeRanges()*m_setting->GetOptimizeRanges();
  for ( unsigned int iScale = 0; iScale < 2; iScale++ ) {
    if ( (!m_setting->GetDoScale() && !iScale) || (!m_setting->GetDoSmearing() && iScale) ) continue;
    double &rangeMin = iScale ? m_sigmaMin : m_alphaMin;
    double &rangeMax = iScale ? m_sigmaMax : m_alphaMax;
    double allowedRangeMin = iScale ? max( 0., m_setting->GetSigmaMin()) : m_setting->GetAlphaMin();
    double allowedRangeMax = iScale ? m_setting->GetSigmaMax() : m_setting->GetAlphaMax();
    cout << allowedRangeMin << endl;
    //    double scaleMin = rangeMax;
    //    double chiMin = -99;

    int counter = -1;
    bitset<2> foundOptim;

    double upRightRange=allowedRangeMax, lowRightRange=allowedRangeMin, minVal=-99, upLeftRange=allowedRangeMin, lowLeftRange=allowedRangeMax;
    while ( true  ) {    
      if ( counter > 10 ) { cout << "reached 10 steps for optimization" << endl; exit(1); }
      foundOptim.reset();
      counter++;
      FillScaleValues( 10 );
      ClearTemplates();
      for ( int i_alpha = 0; i_alpha <= (iScale ? 0 : 10); i_alpha++ ) {
	m_MCZMass.push_back( vector< TH1D* > () );
	for ( int i_sigma = 0; i_sigma <= (iScale ? 10 : 0); i_sigma++ ) {
	  m_MCZMass.back().push_back( 0 );
	  m_MCZMass.back().back() = new TH1D( TString::Format( "%s_MCZMass_sc%d_sm%d", m_name.c_str() ,(int) (m_scaleValues[i_alpha]*1e6),  (int) (m_sigmaValues[i_sigma]*1e6) ), TString::Format( "MCZMass_sc%i_sm%d", (int) (m_scaleValues[i_alpha]*1e6), (int) (m_sigmaValues[i_sigma]*1e6) ), m_setting->GetZMassNBins(), m_setting->GetZMassMin(), m_setting->GetZMassMax() );  
	  m_MCZMass.back().back()->GetXaxis()->SetTitle( "M_{ee}" );
	}}
      FillTemplates( );
      
      if ( IsGoodQuality() ) {
	ClearTemplates();
	return ;
      }

      FillChiMatrix();
      if ( histScale ) delete histScale; histScale=0;
      histScale = iScale ? m_chiMatrix->ProjectionY( m_name.c_str() + TString("histSigma"), 1, 1, "o" )
	: m_chiMatrix->ProjectionX( m_name.c_str() + TString("histAlpha"), 1, 1, "o" );


      int minBin = histScale->GetMinimumBin();
      minVal = minVal==-99 ? histScale->GetBinContent(minBin) : min( minVal, histScale->GetBinContent(minBin) );
      int binUp=histScale->GetNbinsX(), binDown=1;
      while( histScale->GetBinContent(binUp-1) - histScale->GetBinContent(minBin) > chiOptim ) binUp--;
      while( histScale->GetBinContent(binDown+1) - histScale->GetBinContent(minBin) > chiOptim ) binDown++;

      cout << "binsUp : " << binDown << " " << minBin << " " << binUp << endl;
      cout << "values : " << histScale->GetBinContent(binDown) << " " << histScale->GetBinContent(binDown+1) << " " << minVal << " " << histScale->GetBinContent( binUp-1 ) << " " << histScale->GetBinContent( binUp )<< endl;
      cout << "centers : " << histScale->GetXaxis()->GetBinCenter(binDown) << " " << histScale->GetXaxis()->GetBinCenter(binDown+1) << " " << histScale->GetXaxis()->GetBinCenter(minBin) << " " << histScale->GetXaxis()->GetBinCenter(binUp-1) << " " << histScale->GetXaxis()->GetBinCenter(binUp) << endl;

      if ( binUp != histScale->GetNbinsX() ) {
	//The main dichotomy code suppose that once the dichotomy started, the optimized value of scale is between the last and before the last bin
	upRightRange = histScale->GetXaxis()->GetBinCenter( binUp );
	lowRightRange = histScale->GetXaxis()->GetBinCenter( binUp-1 ); 
      }

      if ( binUp==histScale->GetNbinsX() && minBin>=histScale->GetNbinsX()-1 && rangeMax>allowedRangeMax-1e-10 ) foundOptim.set(0);
      else if ( binUp == minBin+1 ) rangeMax = histScale->GetXaxis()->GetBinCenter(binUp);
      else if ( sqrt( histScale->GetBinContent(binUp) - minVal ) < m_setting->GetOptimizeRanges()+1
		&& sqrt( histScale->GetBinContent(binUp) - minVal ) > m_setting->GetOptimizeRanges()-1 ) {
	rangeMax = histScale->GetXaxis()->GetBinCenter( binUp );
	foundOptim.set(0);
      }
      else if ( sqrt( histScale->GetBinContent(binUp-1) - minVal ) < m_setting->GetOptimizeRanges()+1
		&& sqrt( histScale->GetBinContent(binUp-1) - minVal ) > m_setting->GetOptimizeRanges()-1 ) {
	rangeMax = histScale->GetXaxis()->GetBinCenter( binUp-1 );
	foundOptim.set(0);
      }
      else if ( sqrt( histScale->GetBinContent(binUp) - minVal ) < m_setting->GetOptimizeRanges()+1 && rangeMax > allowedRangeMax-1e-10 ) foundOptim.set(0);
      //The following case will always be the first case of dichotomy to happen.
      //It initialises upRightRange
      //lowRightRange initial value is set in such way that it will always be non-max at the first use of this case
      else if ( sqrt( histScale->GetBinContent(binUp) - minVal ) > m_setting->GetOptimizeRanges()+1 ) {
	upRightRange = histScale->GetXaxis()->GetBinCenter( binUp );
	//need to redefine lowRightRange as binUp-1 can have a more interesting centreal value than the previous iteration
	cout << "lowRightRange : " << lowRightRange << " " << histScale->GetXaxis()->GetBinCenter( binUp-1 ) << " " << max( lowRightRange, histScale->GetXaxis()->GetBinCenter( binUp-1 ) ) << endl;
	lowRightRange = max( lowRightRange, histScale->GetXaxis()->GetBinCenter( binUp-1 ) );
	rangeMax = ( lowRightRange + histScale->GetXaxis()->GetBinCenter( binUp ) ) /2;
      }
      else if ( sqrt( histScale->GetBinContent(binUp) - minVal ) < m_setting->GetOptimizeRanges()-1 ) {
	cout << "binUp too low : " << upRightRange << " " << histScale->GetXaxis()->GetBinCenter( binUp ) << " " << min( allowedRangeMax, ( upRightRange + histScale->GetXaxis()->GetBinCenter( binUp ) ) /2 ) << endl;
	rangeMax = min( allowedRangeMax, ( upRightRange + histScale->GetXaxis()->GetBinCenter( binUp ) ) /2 );
	lowRightRange = max( lowRightRange, histScale->GetXaxis()->GetBinCenter( binUp ) );
      }


      //===========================
      if ( binDown != 1 ) {
	//The main dichotomy code suppose that once the dichotomy started, the optimized value of scale is between the first and second bin
	upLeftRange = histScale->GetXaxis()->GetBinCenter( 1 );
	lowLeftRange = histScale->GetXaxis()->GetBinCenter( 2 ); 
      }

      if ( binDown == 1 && minBin<=2 && rangeMin < allowedRangeMin+ 1e-10 ) foundOptim.set(1);
      else if ( binDown == minBin-1 ) rangeMin = histScale->GetXaxis()->GetBinCenter(binDown);
      else if ( sqrt( histScale->GetBinContent(binDown) - minVal ) < m_setting->GetOptimizeRanges()+1
		&& sqrt( histScale->GetBinContent(binDown) - minVal ) > m_setting->GetOptimizeRanges()-1 ) {
	rangeMin = histScale->GetXaxis()->GetBinCenter( binDown );
	foundOptim.set(1);
      }
      else if ( sqrt( histScale->GetBinContent(binDown+1) - minVal ) < m_setting->GetOptimizeRanges()+1
		&& sqrt( histScale->GetBinContent(binDown+1) - minVal ) > m_setting->GetOptimizeRanges()-1 ) {
	rangeMin = histScale->GetXaxis()->GetBinCenter( binDown+1 );
	foundOptim.set(1);
      }
      else if ( sqrt( histScale->GetBinContent(binDown) - minVal ) < m_setting->GetOptimizeRanges()+1
		&& rangeMin<allowedRangeMin+1e-10 ) 	foundOptim.set(1);
      //The following case will always be the first case of dichotomy to happen.
      //It initialises upLeftRange
      //lowLeftRange initial value is set in such way that it will always be non-max at the first use of this case
      else if ( sqrt( histScale->GetBinContent(binDown) - minVal ) > m_setting->GetOptimizeRanges()+1 ) {
	cout << "reduce range : " << lowLeftRange << " " << histScale->GetXaxis()->GetBinCenter( binDown ) << endl;;
	upLeftRange = histScale->GetXaxis()->GetBinCenter( binDown );
	//need to redefine lowLeftRange as binDown-1 can have a more interesting centreal value than the previous iteration
	lowLeftRange = min( lowLeftRange, histScale->GetXaxis()->GetBinCenter( binDown+1 ) );
	rangeMin = ( lowLeftRange + histScale->GetXaxis()->GetBinCenter( binDown ) ) /2;
	cout << "reduce range : " << lowLeftRange << " " << histScale->GetXaxis()->GetBinCenter( binDown ) << endl;
      }
      else if ( sqrt( histScale->GetBinContent(binDown) - minVal ) < m_setting->GetOptimizeRanges()-1 ) {
	cout << "increase range : " << rangeMin << " " << upLeftRange + histScale->GetXaxis()->GetBinCenter( binDown ) /2 << endl;
	rangeMin = max( allowedRangeMin, upLeftRange + histScale->GetXaxis()->GetBinCenter( binDown ) /2 );
	cout << rangeMin << " " << lowLeftRange << endl;
	lowLeftRange = max( lowLeftRange, histScale->GetXaxis()->GetBinCenter( binDown ) );
	cout << lowLeftRange << endl;
      }
      cout << "leftRanges : " << lowLeftRange << " " << upLeftRange << endl;
      cout << "rightRanges : " << lowRightRange << " " << upRightRange << endl;
      cout << "ranges : " << rangeMin << " " << rangeMax << endl;
      cout << "foundOptim : " << foundOptim.to_ulong() << endl;
      if ( foundOptim.to_ulong() == 3 ) break;
      

	// //	cout << "minBin : "  << minBin << " " << histScale->GetBinCenter( histScale->GetMiXaxis()->GetXmin() << " " << histScale->GetXaxis()->GetXmax() << endl;
	// //Dealing with minimum bin too close to overflow
	// //if ( m_setting->GetDebug() ) cout << "minBin too high : " << minBin << " " << floor( histScale->GetNbinsX()*3./4 ) << " " << allowedRangeMax << " " << rangeMaxu << endl;
	// if ( minBin >= floor( histScale->GetNbinsX()*3./4 )   ) {
	//   if ( allowedRangeMax == rangeMax ) {
	//     m_quality.set(2, 1);
	//     delete histScale; histScale=0;
	//     ClearTemplates();
	//     delete m_chiMatrix; m_chiMatrix=0;
	//     return;
	//   } 
	//   else {
	//   rangeMax =  min( 2*rangeMax - rangeMin, allowedRangeMax );
	//   cout << "rangeMax : " << rangeMax << endl;
	//   continue;
	//   }
	// }
	
	// //Dealing with minimum bin too close to underflow
	// if ( minBin <= ceil( histScale->GetNbinsX()/4. ) && allowedRangeMin != rangeMin ) {
	//   rangeMin =  max( 2*rangeMin - rangeMax, allowedRangeMin );
	//   continue;
	// }

	// double sigmaUp = sqrt( histScale->GetBinContent(histScale->GetNbinsX()) - histScale->GetMinimum());
	// if ( histScale->GetMinimum() >= chiMin && chiMin != -99 && sigmaUp>m_setting->GetOptimizeRanges() ) {
	//   delete histScale; histScale=0;
	//   break;
	// }

	// if ( m_setting->GetDebug() ) {
	// cout << "counter : " << counter << endl;
	// cout << "start" << endl;
	// cout << "chiMin : " << chiMin << endl;
	// cout << "minimum : " << histScale->GetMinimum() << " " << minBin << endl;
	// cout << "scaleMin : " << scaleMin << endl;
	// cout << "rangeMin : " << rangeMin << " " << histScale->GetBinContent(1) << endl;
	// cout << "rangeMax : " << rangeMax << " " << histScale->GetBinContent( histScale->GetNbinsX() ) << endl;
	// }

	// chiMin = min( chiMin, histScale->GetMinimum() );
	// scaleMin = histScale->GetXaxis()->GetBinCenter( histScale->GetMinimumBin() );	

	// double sigmaDown = sqrt( histScale->GetBinContent(1) - histScale->GetMinimum());

	// if ( sigmaDown == 0 ) sigmaDown = m_setting->GetOptimizeRanges();
	// rangeMax = min( allowedRangeMax, scaleMin + (rangeMax-scaleMin)*m_setting->GetOptimizeRanges()/sigmaUp );
	// rangeMin = max ( allowedRangeMin, scaleMin + ( rangeMin-scaleMin)*m_setting->GetOptimizeRanges()/sigmaDown );


	// if ( histScale->GetMinimum() >= chiMin && chiMin != -99 ) {
	//   delete histScale; histScale=0;
	//   break;
	// }


	// if ( iScale && scaleMin<0 ) scaleMin=0;
	// chiMin = histScale->GetMinimum();

      //      }//end else counter

      if ( histScale ) delete histScale; histScale=0;
  }
    if ( m_setting->GetDebug() ) cout << "range " << (iScale ? "Sigma" : "Alpha" ) << " : " << rangeMin << " " << rangeMax << endl;	 
    //    if ( rangeMax == allowedRangeMax ) m_quality.set( 2, 1 );
  }

  if ( m_setting->GetDebug() ) cout << "ChiMatrix::OptimizeRanges() Done" << endl;
}

//==========================================
void ChiMatrix::ClearTemplates() {

 while( m_MCZMass.size() ) {
    while ( m_MCZMass.back().size() ) {    
      if ( m_MCZMass.back().back() ) delete m_MCZMass.back().back();
      m_MCZMass.back().back() = 0;
      m_MCZMass.back().pop_back();
    }
    m_MCZMass.pop_back();
  }

}
//==========
unsigned int ChiMatrix::IsGoodQuality() {
  //  cout << "ChiMatrix::IsGoodQuality" << endl;
  int nentries = (int) m_setting->GetNEventCut();
  //If m_quality already set to false put false again
  if ( m_quality.to_ulong() ) return false;

  vector< double > etaBins( m_setting->GetEtaBins());

  if ( !m_dataZMass || !m_MCZMass.front().front() ) m_quality.set( 3, 1 );
  if ( m_MCZMass.front().front()->GetEntries() < nentries ) m_quality.set( 4, 1 );
  if ( m_dataZMass->GetEntries() < nentries ) m_quality.set( 5, 1 );
  if ( m_setting->GetVar1() == "ETA_TRK" || m_setting->GetVar1() == "ETA_CALO" || m_setting->GetVar1() == "ETA_CLUSTER" ) {
    double mTh=27*sqrt(2*(TMath::CosH( (etaBins[m_eta1Bin]+etaBins[m_eta1Bin+1]-etaBins[m_eta2Bin+1]-etaBins[m_eta2Bin])/2.)+1)) ;
    if (  mTh > m_setting->GetThresholdMass() ) m_quality.set( 6, 1 );
  }

  return m_quality.to_ulong();
}


//==========================
double ChiMatrix::ComputeChi2( TH1D *MCHist, bool isIncreasedStat ) {

  if ( MCHist->GetNbinsX() != m_dataZMass->GetNbinsX() 
       || MCHist->GetXaxis()->GetXmin() != m_dataZMass->GetXaxis()->GetXmin() 
       || MCHist->GetXaxis()->GetXmax() != m_dataZMass->GetXaxis()->GetXmax() ) 
    {
      cout << "Histograms for chi do not match" << endl;
      exit(1);
    }
  
  double chi2 = 0;
  for ( int i = 0; i < MCHist->GetNbinsX(); i++ ) {
    if ( MCHist->GetBinError( i+1 )==0 || m_dataZMass->GetBinError( i+1 )==0 ) continue; 
    double valdif =  MCHist->GetBinContent( i+1 ) - m_dataZMass->GetBinContent( i+1 );
    double sigmaMC = MCHist->GetBinError( i+1 ) * ((isIncreasedStat) ? sqrt( m_setting->GetNUseEl() ) : 1 );
    double sigma2 =  sigmaMC*sigmaMC + m_dataZMass->GetBinError( i+1 ) * m_dataZMass->GetBinError( i+1 );
    chi2 += valdif * valdif / sigma2; 
  }
    
  return chi2;
}

//==============================
TF1* ChiMatrix::FitHist( TH1D* hist, unsigned int mode, double chiMinLow, double chiMinUp ) {
  TF1 *quadraticFit = new TF1( "quadraticFit", "[0] + (x-[2])*(x-[2])/[1]/[1]",-1, 1);
  TF1 *cubicFit = new TF1( "cubicFit", "[0] + (x-[2])*(x-[2])/[1]/[1]+[3]*(x-[2])*(x-[2])*(x-[2])/[1]/[1]/[1]",-1, 1);
  //TF1 *cubicFit = new TF1( "cubicFit", "[0] + (x-[2])*(x-[2])/[1]/[1]+[3]*TMath::Abs((x-[2]))*(x-[2])*(x-[2])/[1]/[1]/[1]",-1, 1);
  cubicFit->SetParLimits( 3, 0, 1e5 );
  TF1 *fittingFunction = 0;
  TFitResultPtr fitResult = 0;

  string options = string("S") + ( m_setting->GetDebug() ? "" : "Q" );
  int minBin = 1;
  int maxBin = hist->GetNbinsX();
  int centralBin = hist->GetMinimumBin();
  double minCentral = hist->GetXaxis()->GetBinLowEdge( minBin );
  if ( FindFitBestRange( hist, minBin, maxBin, chiMinLow, chiMinUp ) ) {
    delete quadraticFit; quadraticFit=0;
    delete cubicFit; cubicFit=0;
    return 0;
  }

  switch ( mode ) {
  case 1 :
    fittingFunction = cubicFit;
    minCentral=max( 0., hist->GetXaxis()->GetXmin() );
    break;
  case 2 :
    fittingFunction = cubicFit;
    minCentral=max( 0., hist->GetXaxis()->GetXmin() );
    break;
  case 3 :
    fittingFunction = quadraticFit;
    minCentral=max( 0., hist->GetXaxis()->GetXmin() );
    cout << "minBin : " << minBin;
    minBin = hist->GetMinimumBin();
    cout << " " << minBin << endl;
    break;
  case 4 :
    fittingFunction = cubicFit;
    minCentral=max( 0., hist->GetXaxis()->GetXmin() );
    break;
  default : //Fit alpha optimization
    fittingFunction = quadraticFit;
  }

  fittingFunction->SetParameter( 0, hist->GetMinimum() );
  fittingFunction->SetParLimits( 0, 0, hist->GetMaximum() );    


  fittingFunction->SetParameter( 2, hist->GetBinCenter( hist->GetMinimumBin()));
  fittingFunction->SetParLimits( 2, minCentral, hist->GetXaxis()->GetBinUpEdge( maxBin ) );


  int &extrBin = ( maxBin == centralBin ) ? minBin : maxBin;
  double sigma = ( hist->GetBinCenter( extrBin ) - hist->GetBinCenter( centralBin ) ) / sqrt(hist->GetBinContent( extrBin ) - hist->GetBinContent( hist->GetMinimumBin() ) );
  fittingFunction->SetParameter( 1, sigma );
  fittingFunction->SetParLimits( 1, 0, 1 );


  int nFits=5;
  do {
    //    fitResult = hist->Fit( fittingFunction, "SQ", "", hist->GetXaxis()->GetBinLowEdge( minBin ), hist->GetXaxis()->GetBinUpEdge( maxBin ) );
    //    if ( fitResult.Get() ) delete fitResult.Get();
    fitResult = hist->Fit( fittingFunction, options.c_str(), "", hist->GetXaxis()->GetBinLowEdge( minBin ), hist->GetXaxis()->GetBinUpEdge( maxBin ) );
    nFits --;
  }
  while( fitResult->Status() && nFits );

  if ( fitResult->Status() ) {
    while ( maxBin - minBin > 8 ) {
      minBin = min( minBin+1, hist->GetMinimumBin() );
      maxBin = max( maxBin-1, hist->GetMinimumBin() );
      nFits = 3;
      do {
	cout << "fit failed 3 times : try with another range" << endl;
	fittingFunction->SetParameter( 0, hist->GetMinimum() );
	fittingFunction->SetParameter( 2, hist->GetBinCenter( hist->GetMinimumBin()));
	sigma = ( hist->GetBinCenter( maxBin ) - hist->GetMinimum() ) / sqrt(hist->GetBinContent( maxBin ) - hist->GetBinContent( hist->GetMinimumBin() ) );
	fittingFunction->SetParameter( 1, sigma );
	//	if ( fitResult.Get() ) delete fitResult.Get();
	fitResult =   hist->Fit( fittingFunction, options.c_str(), "", hist->GetXaxis()->GetBinLowEdge( minBin ), hist->GetXaxis()->GetBinUpEdge( maxBin ) );
	nFits--;
      }
      while ( fitResult->Status() && nFits );
    }
  }
  
  if ( fitResult->Status() ) {
    cout << "fit failed" << endl;
    return 0;
  }


  if ( !fitResult->Status() && ( mode == 2 || mode == 4 ) ) { //solve the equation chi(C))=1 with dichotomy
    double minVal = fittingFunction->GetParameter(2);
    double currentValue = hist->GetXaxis()->GetXmax();
    double width = currentValue-minVal;
    double precision = 1e-3;
    while ( width > precision*(currentValue-minVal) ) {
      width/=2.;
      currentValue += ( (*fittingFunction)(currentValue) - (*fittingFunction)(minVal) < 1 ) ? width : -width;
    }
    double error = fabs(currentValue-minVal);
    fittingFunction->SetParameter( 1, error > 1e-7 ? error : 100  );

  }
  TF1* result = (TF1*) fittingFunction->Clone();
  result->SetName( "fittingFunction" );
  delete quadraticFit; quadraticFit=0;
  delete cubicFit; cubicFit=0;

 return result;
}


//===================================
void ChiMatrix::CreateMCTree() {
  //  if ( m_setting->GetDebug() ) cout << "ChiMatrix::CreateMCTree()" << endl;

  m_mapVar1["PT"] = 0;
  m_mapVar1["ETA_TRK"] = 0;
  m_mapVar1["PHI"] = 0;
  m_mapVar2["PT"] = 0;
  m_mapVar2["ETA_TRK"] = 0;
  m_mapVar2["PHI"] = 0;
  m_mapVarEvent["WEIGHT"]=1;
  
  if ( m_MCTree ) { delete m_MCTree; m_MCTree = 0; }
  m_MCTree = new TTree( m_name + TString("_MCTree" ), m_name + TString("_MCTree" ) );
  m_MCTree->SetDirectory(0);
  m_MCTree->Branch( "pt_1"  , &m_mapVar1["PT"] );
  m_MCTree->Branch( "eta_1" , &m_mapVar1["ETA_TRK"] );
  m_MCTree->Branch( "phi_1" , &m_mapVar1["PHI"] );
  m_MCTree->Branch( "pt_2"  , &m_mapVar2["PT"] );
  m_MCTree->Branch( "eta_2" , &m_mapVar2["ETA_TRK"] );
  m_MCTree->Branch( "phi_2" , &m_mapVar2["PHI"] );
  m_MCTree->Branch( "weight", &m_mapVarEvent["WEIGHT"] );
  // cout << m_MCTree << endl;
  // if ( m_setting->GetDebug() ) cout << "ChiMatrix::CreateMCTree() Done" << endl;
}

//====================================
int ChiMatrix::LinkMCTree( ) {
  //  if ( m_setting->GetDebug() ) cout << "Template::LinkTree" << endl;
  if ( !m_MCTree ) CreateMCTree();
  m_MCTree->SetBranchStatus( "*", 1);
  m_MCTree->SetBranchAddress( "pt_1"  , &m_mapVar1["PT"] );
  m_MCTree->SetBranchAddress( "eta_1" , &m_mapVar1["ETA_TRK"] );
  m_MCTree->SetBranchAddress( "phi_1" , &m_mapVar1["PHI"] );
  m_MCTree->SetBranchAddress( "pt_2"  , &m_mapVar2["PT"] );
  m_MCTree->SetBranchAddress( "eta_2" , &m_mapVar2["ETA_TRK"] );
  m_MCTree->SetBranchAddress( "phi_2" , &m_mapVar2["PHI"] );
  m_MCTree->SetBranchAddress( "weight", &m_mapVarEvent["WEIGHT"] );
  //  if ( m_setting->GetDebug() ) cout << "Template::LinkTree done" << endl;  
  return 0;
}


