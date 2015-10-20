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

  string path = "/sps/atlas/c/cgoudet/Calibration/ScaleResults/279928/";

  //Choose the files that contains central values
  // ROOTFILE HISTNAME OUTHISTNAME
  vector< vector< string > > centralValues = {
    { "Data6_25ns.root", "measScale_alpha", "alphaOff" },
    { "Data6_25ns.root", "measScale_c", "sigmaOff" },
  };

  //Choose which systematics are to be added
  //SYSTROOTFILE OUTHISTNAME
  vector< vector<string> > systDifAlpha = {
    { "Data6_25ns_noPileup.root", "measScale_alpha", "pileUp" },
    { "Data6_25ns_massWindow.root", "measScale_alpha", "massWindow" },
    { "Data6_25ns_thresholdMass.root", "measScale_alpha", "thresholdMass" },
    { "Data6_25ns_tight.root", "measScale_alpha", "tight" }
  };
  vector< vector<string> > systDifSigma = {
    { "Data6_25ns_noPileup.root", "measScale_c", "pileUp" },
    { "Data6_25ns_massWindow.root", "measScale_c", "massWindow" },
    { "Data6_25ns_thresholdMass.root", "measScale_c", "thresholdMass" },
    { "Data6_25ns_tight.root", "measScale_c", "tight" }
  };

  vector<string> systAloneAlpha = {
  };
  
  vector<string> systAloneSigma = {
  };
  
  bool doSyst68_34Bins = false;
  vector<string> filesSyst68_34Bins = { "Data68.root", "Data34_NUseEl15.root" };


//Copying the recommandations to the common file
  TFile *outFile = new TFile( TString(path) + "ElectronEnergyScaleFactor.root", "RECREATE" );
  vector<TH1 *> systAlpha;
  vector<TH1 *> systSigma;
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
    scale->SetTitle( centralValues[iFile][2].c_str() );
    outFile->cd();
    scale->Write( centralValues[iFile][2].c_str(), TObject::kOverwrite );
    delete scale; scale = 0;
  }
  cout << "Scale factors saved" << endl;


  //Making systematics from result differences
  for (unsigned int iVar =0; iVar < 2; iVar++ ) {
    cout << "iVar : " << iVar << endl;
    if ( iVar && !systDifSigma.size() ) continue;
    if ( !iVar && !systDifAlpha.size() ) continue;
    vector< vector<string> > &currentVector = iVar ? systDifSigma : systDifAlpha;
    TH1D *alphaBase = (TH1D*) outFile->Get( centralValues[iVar][2].c_str() );
    cout << "currentVector.size() : " << currentVector.size() << endl;
    for ( unsigned int iSyst = 0; iSyst < currentVector.size(); iSyst++ ) {
      string title = path + currentVector[iSyst].front();
      TFile *fileSyst = new TFile( title.c_str() );
      string systName = "syst_" + currentVector[iSyst][2] + "_" + (iVar ? "sigma" : "alpha" );
      vector< TH1* > &systHist = iVar ? systSigma : systAlpha;
      systHist.push_back(0);
      cout << "systHistName : " << currentVector[iSyst][1] << endl;
      systHist.back() = ( TH1D*) fileSyst->Get( currentVector[iSyst][1].c_str() );
      systHist.back()->SetDirectory(0);
      systHist.back()->SetName( systName.c_str() );
      systHist.back()->SetTitle( systHist.back()->GetName() );
      systHist.back()->GetXaxis()->SetTitle( alphaBase->GetXaxis()->GetTitle() );
      systHist.back()->GetYaxis()->SetTitle( string( currentVector[iSyst][2] + "_syst" ).c_str() );

      cout << "systHist->GetName() : " << systHist.back()->GetName() << endl;
      cout << "alphaBaseName : " << alphaBase->GetName() << endl;

      for ( int iBin = 1; iBin <= alphaBase->GetNbinsX(); iBin++ ) {
      double syst = fabs( alphaBase->GetBinContent( iBin ) - systHist.back()->GetBinContent(iBin) );
	if ( iVar ) {
	  cout << alphaBase->GetBinContent( iBin ) << " " << systHist.back()->GetBinContent(iBin) << endl;
	  cout << syst << endl;
	}
      systHist.back()->SetBinContent( iBin, syst );
      }
           cout << "Systematic " << ( iVar ? "sigma" : "alpha" ) << " " << systDifAlpha[iSyst][2] << " done" << endl;
    }
  }

  // //Make standalone systematics
  // for (unsigned int iVar =0; iVar < 2; iVar++ ) {
  //   if ( iVar && !systAloneSigma.size() ) continue;
  //   if ( !iVar && !systAloneAlpha.size() ) continue;

  //   for ( unsigned int iFile = 0; iFile < ( iVar ? systAloneSigma.size() : systAloneAlpha.size() ); iFile++ ) {
  //     string title = path +  (iVar ?  systAloneSigma[iFile] : systAloneAlpha[iFile]);
  //     TFile *inFile = new TFile( title.c_str() );
  //     StripString( title );
  //     TH1D* inHist = (TH1D*) inFile->Get( iVar ? "sigma" : "alpha" )->Clone();
  //     inHist->SetName( TString( title ) + "_" + inHist->GetTitle() );
  //     inHist->SetTitle( inHist->GetName() );

  //     if ( iVar ) systSigma.push_back( inHist );
  //     else systAlpha.push_back( inHist );
  //   }

  // }

  // //Make systematic 68bin vs 34 bin
  // if ( doSyst68_34Bins ) {
  //   //The systematic is the difference between the value of 34 bin and the average of the 2 sub-bins
  //   TFile *file68 = new TFile( TString( path + filesSyst68_34Bins[0] ) );
  //   TH1D *alpha68 = (TH1D*) file68->Get( "alpha" );
  //   TFile *file34 = new TFile( TString( path + filesSyst68_34Bins[1] ) );
  //   TH1D *alpha34 = (TH1D*) file34->Get( "alpha" );
  //   systAlpha.push_back(0);
  //   systAlpha.back() = new TH1D( "syst68_34Bins_alpha", "syst68_34Bins_alpha", alpha68->GetNbinsX(), alpha68->GetXaxis()->GetXbins()->GetArray() );
  //   systAlpha.back()->GetXaxis()->SetTitle( alpha68->GetXaxis()->GetTitle() );
  //   systAlpha.back()->GetYaxis()->SetTitle( alpha68->GetYaxis()->GetTitle() );
    

  //   for ( int iBin = 1; iBin <= alpha34->GetNbinsX(); iBin++ ) {
  //     double syst = fabs( (alpha68->GetBinContent( 2*iBin ) + alpha68->GetBinContent( 2*iBin-1 ))/2 - alpha34->GetBinContent(iBin) );
  //     systAlpha.back()->SetBinContent( 2*iBin -1, syst );
  //     systAlpha.back()->SetBinContent( 2*iBin, syst );
  //   }


  //   cout << "Sytematic 68/34 bins done" << endl;
  // }




  //Saving all Systematics
  outFile->cd();
  //  TH1D *fullSyst = 0;
  for ( unsigned int iVar = 0; iVar < 2; iVar++ ) {
    if ( iVar && !systSigma.size() ) continue;
    if ( !iVar && !systAlpha.size() ) continue;

    vector<TH1 *> &systs = iVar ?  systSigma : systAlpha;

    string title = "syst" + string( iVar ? "Sigma" : "Alpha" );
    TH1D *fullSyst = new TH1D( title.c_str(), title.c_str(), systs.front()->GetNbinsX(), systs.front()->GetXaxis()->GetXbins()->GetArray() );

    cout <<  "systAlphasize : " << systAlpha.size() << endl;
    for ( unsigned int iSyst = 0; iSyst < systs.size(); iSyst++ ) {

      systs[iSyst]->Write( "", TObject::kOverwrite );

      for ( int iBin = 1; iBin <= fullSyst->GetNbinsX(); iBin++ ) {
  	double systVal = fullSyst->GetBinContent( iBin )*fullSyst->GetBinContent( iBin ) + systs[iSyst]->GetBinContent( iBin )*systs[iSyst]->GetBinContent( iBin );
  	fullSyst->SetBinContent( iBin, sqrt(systVal) );
      }
    }

    cout << "writting" << endl;
    fullSyst->Write( "", TObject::kOverwrite );
  }


  cout << "Histograms saved" << endl;
  outFile->Close();
  delete outFile;
  return 0;
}
