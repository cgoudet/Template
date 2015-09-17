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
  Style_Christophe();

  string path = "/sps/atlas/c/cgoudet/Calibration/PreRec/Results/";

  //Choose the files that contains central values
  // ROOTFILE HISTNAME OUTHISTNAME
  vector< vector< string > > centralValues = {
    { "Data68.root", "alpha", "alpha68" },
    { "Data24Sigma_NUseEl15.root", "sigma", "sigma24" }
  };

  //Choose which systematics are to be added
  //BASEROOTFILE SYSTROOTFILE OUTHISTNAME
  vector<string> systDifAlpha = {
    "Data68.root"
  };
  vector< string > systDifSigma = {
    "Data24Sigma_NUseEl15.root"
  };

  vector<string> systAloneAlpha = {
  "Data68_MC13.root"
  };
  
  vector<string> systAloneSigma = {
    "Data24Sigma_NUseEl15_MC13.root"
  };
  
  bool doSyst68_34Bins = true;
  vector<string> filesSyst68_34Bins = { "Data68.root", "Data34_NUseEl15.root" };


//Copying the recommandations to the common file
  TFile *outFile = new TFile( TString(path) + "ElectronEnergyScaleFactor.root", "RECREATE" );
  vector<TH1D *> systAlpha;
  vector<TH1D *> systSigma;
  for ( unsigned int iFile = 0; iFile < centralValues.size(); iFile++ ) {
    TFile *rootFile = new TFile( TString( path + centralValues[iFile][0] ) );
    if ( !rootFile ) {
      cout << "Error : file " << path + centralValues[iFile][0] << " not found."  << endl;
      exit(1);
    }
    TH1D *scale = (TH1D*) rootFile->Get( centralValues[iFile][1].c_str() );
    if ( !scale ) {
      cout << "Error : hist " << centralValues[iFile][1] << " not found." << endl;
      exit( 1 );
    }
    outFile->cd();
    scale->Write( centralValues[iFile][2].c_str(), TObject::kOverwrite );
  }
  cout << "Scale factors saved" << endl;


  //Making systematics from result differences
  for (unsigned int iVar =0; iVar < 2; iVar++ ) {
    if ( iVar && !systDifSigma.size() ) continue;
    if ( !iVar && !systDifAlpha.size() ) continue;

    TFile *fileBase = new TFile( TString( path) + (iVar ? systDifSigma[0].c_str() : systDifAlpha[0].c_str()) );
    TH1D *alphaBase = (TH1D*) fileBase->Get( iVar ? "sigma" : "alpha" );

    for ( unsigned int iSyst = 1; iSyst < ( iVar ? systDifAlpha.size() : systDifAlpha.size()); iSyst++ ) {
      string title = path + ( iVar ? systDifSigma[iSyst] : systDifAlpha[iSyst] );
      TFile *fileSyst = new TFile( title.c_str() );
      TH1D* alphaSyst = ( TH1D*) fileSyst->Get( iVar ? "sigma" : "alpha" );
      StripString( title );

      TH1D *histSyst = 0;
      if ( iVar ) {
      systAlpha.push_back( 0 );
      systAlpha.back() = new TH1D( systDifAlpha[iSyst].c_str(), systDifAlpha[iSyst].c_str(), alphaBase->GetNbinsX(), alphaBase->GetXaxis()->GetXbins()->GetArray() );
      histSyst = systAlpha.back();
      }
      else {
      systSigma.push_back( 0 );
      systSigma.back() = new TH1D( systDifSigma[iSyst].c_str(), systDifSigma[iSyst].c_str(), alphaBase->GetNbinsX(), alphaBase->GetXaxis()->GetXbins()->GetArray() );
      histSyst = systSigma.back();
      }      

      histSyst->SetName( TString( title ) + "_" + histSyst->GetTitle() );
      histSyst->SetTitle( histSyst->GetName() );
      systAlpha.back()->GetXaxis()->SetTitle( alphaSyst->GetXaxis()->GetTitle() );
      systAlpha.back()->GetYaxis()->SetTitle( alphaSyst->GetYaxis()->GetTitle() );

      for ( int iBin = 1; iBin <= alphaBase->GetNbinsX(); iBin++ ) {
	double syst = fabs( alphaBase->GetBinContent( iBin ) - alphaSyst->GetBinContent(iBin) );
	histSyst->SetBinContent( iBin, syst );
      }
      cout << "Systematic " << ( iVar ? "sigma" : "alpha" ) << " " << systDifAlpha[iSyst][2] << " done" << endl;
    }
  }

  //Make standalone systematics
  for (unsigned int iVar =0; iVar < 2; iVar++ ) {
    if ( iVar && !systAloneSigma.size() ) continue;
    if ( !iVar && !systAloneAlpha.size() ) continue;

    for ( unsigned int iFile = 0; iFile < ( iVar ? systAloneSigma.size() : systAloneAlpha.size() ); iFile++ ) {
      string title = path +  (iVar ?  systAloneSigma[iFile] : systAloneAlpha[iFile]);
      TFile *inFile = new TFile( title.c_str() );
      StripString( title );
      TH1D* inHist = (TH1D*) inFile->Get( iVar ? "sigma" : "alpha" )->Clone();
      inHist->SetName( TString( title ) + "_" + inHist->GetTitle() );
      inHist->SetTitle( inHist->GetName() );

      if ( iVar ) systSigma.push_back( inHist );
      else systAlpha.push_back( inHist );
    }

  }

  //Make systematic 68bin vs 34 bin
  if ( doSyst68_34Bins ) {
    //The systematic is the difference between the value of 34 bin and the average of the 2 sub-bins
    TFile *file68 = new TFile( TString( path + filesSyst68_34Bins[0] ) );
    TH1D *alpha68 = (TH1D*) file68->Get( "alpha" );
    TFile *file34 = new TFile( TString( path + filesSyst68_34Bins[1] ) );
    TH1D *alpha34 = (TH1D*) file34->Get( "alpha" );
    systAlpha.push_back(0);
    systAlpha.back() = new TH1D( "syst68_34Bins_alpha", "syst68_34Bins_alpha", alpha68->GetNbinsX(), alpha68->GetXaxis()->GetXbins()->GetArray() );
    systAlpha.back()->GetXaxis()->SetTitle( alpha68->GetXaxis()->GetTitle() );
    systAlpha.back()->GetYaxis()->SetTitle( alpha68->GetYaxis()->GetTitle() );
    

    for ( int iBin = 1; iBin <= alpha34->GetNbinsX(); iBin++ ) {
      double syst = fabs( (alpha68->GetBinContent( 2*iBin ) + alpha68->GetBinContent( 2*iBin-1 ))/2 - alpha34->GetBinContent(iBin) );
      systAlpha.back()->SetBinContent( 2*iBin -1, syst );
      systAlpha.back()->SetBinContent( 2*iBin, syst );
    }


    cout << "Sytematic 68/34 bins done" << endl;
  }




  //Saving all Systematics
  outFile->cd();
  TH1D *fullSystAlpha = 0, *fullSystSigma=0;
  for ( unsigned int iVar = 0; iVar < 2; iVar++ ) {
    if ( iVar && !systSigma.size() ) continue;
    if ( !iVar && !systAlpha.size() ) continue;

    if ( iVar ) fullSystSigma = new TH1D( "systSigma", "systSigma", systSigma.front()->GetNbinsX(), systSigma.front()->GetXaxis()->GetXbins()->GetArray() );
    else fullSystAlpha = new TH1D( "systAlpha", "systAlpha", systAlpha.front()->GetNbinsX(), systAlpha.front()->GetXaxis()->GetXbins()->GetArray() );

    TH1D *fullSystHist = iVar ? fullSystSigma : fullSystAlpha;
    cout <<  "systAlphasize : " << systAlpha.size() << endl;
    for ( unsigned int iSyst = 0; iSyst < ( iVar ? systSigma.size() : systAlpha.size() ); iSyst++ ) {

      TH1D *histSyst =  iVar ? systSigma[iSyst] : systAlpha[iSyst];
      histSyst->Write( "", TObject::kOverwrite );

      for ( int iBin = 1; iBin <= histSyst->GetNbinsX(); iBin++ ) {
	double systVal = fullSystHist->GetBinContent( iBin )*fullSystHist->GetBinContent( iBin ) + histSyst->GetBinContent( iBin )*histSyst->GetBinContent( iBin );
	fullSystHist->SetBinContent( iBin, systVal );
      }
    }
    cout << "Added syst" << endl;    
    for ( int iBin = 1; iBin <= fullSystHist->GetNbinsX(); iBin++ ) {
      fullSystHist->SetBinContent( iBin, sqrt( fullSystHist->GetBinContent( iBin ) ) );
    }
    cout << "test" << endl;
    outFile->ls();
    cout << "writting" << endl;
    fullSystHist->Write( "", TObject::kOverwrite );
  }


  cout << "Histograms saved" << endl;
  outFile->Close();
  return 0;
}
