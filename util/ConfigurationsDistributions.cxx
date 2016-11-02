#include <iostream>
#include <boost/program_options.hpp>
#include <vector>
#include <string>
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include <fstream>
#include "TCanvas.h"
#include <TROOT.h>
#include <TStyle.h>
#include "PlotFunctions/SideFunctions.h"
#include "PlotFunctions/SideFunctionsTpp.h"
#include "TProfile.h"
#include "TMath.h"
#include "TH2D.h"
#include "PlotFunctions/DrawPlot.h"
#include <map>

using std::map;
using std::fstream;
using std::string;
using std::cout;
using std::endl;
using std::vector;
using boost::multi_array;
using boost::extents;
namespace po = boost::program_options;
using namespace ChrisLib;
void Style_Christophe();

int main( int argc, char* argv[] ) {
  po::options_description desc("LikelihoodProfiel Usage");

  vector<string> inFiles;
  string outName;
  //define all options in the program
  desc.add_options()
    ("help", "Display this help message")
    ("inFiles", po::value<vector <string> >(&inFiles), "" )
    ("outName", po::value< string >( &outName )->default_value( "GenerateToyTemplates" ), "" )
     ;
  
  //Define options gathered by position                                                          
  po::positional_options_description p;
  p.add("inFiles", -1);

  // create a map vm that contains options and all arguments of options       
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv).options(desc).positional(p).style(po::command_line_style::unix_style ^ po::command_line_style::allow_short).run(), vm);
  po::notify(vm);
  
  if (vm.count("help")) {cout << desc; return 0;}
  //########################################
  Style_Christophe();
  /* CODED PLOTS
     - constant term sistribution in each configuration
     - constant term bias in each configuration
     - constant term distribution and bias in each 
   */


  //ConfigDistrib[nBins][stat][input][iConf][jConf][mode]
  multi_array<TH1D*, 6> configCDistrib;
  //binCDistrib[nBins][stat][input][iBin][model]
  multi_array< TH1D*, 5 > binCDistrib;
  //configProfileStat[nBins][input][iConf][jConf]
  multi_array< TProfile*, 5> configProfileStat;
  //fullBias[nBins][stat][input]
  multi_array< TH1D*, 3> fullBias;
  //configProfileRMS[nBin][stat][input]
  multi_array< TProfile*, 3 > configProfileRMS;
  //binMeanConfig[nBin][stat][input][iConf][2]
  multi_array< TH1D*, 4 > binMeanConfig;

  // nBins statTot iConf jConf
  multi_array< unsigned int, 4 > configStat;
  multi_array< unsigned int, 4 > configRMS;

  //nBins statTot IBin
  multi_array< unsigned int, 3 > binStat;
  multi_array< unsigned int, 3 > binRMS;
 
  vector< TH1* > saveHist;
  vector< double > inputVals;
  vector< unsigned int > inputStat, inputBins;
  double cVal, input, rms;
  unsigned int statConf, statTree, iConf, jConf, statBin, inputBin, binBin, nBins, maxBins=0;


  for ( unsigned int iFile = 0; iFile < inFiles.size(); iFile++ ) {
    //    cout << "File : " << iFile << endl;
    TFile *inFile = TFile::Open( inFiles[iFile].c_str() );
    if ( !inFile ) continue;
    //    inFile->ls();
    TTree *confTree = (TTree*) inFile->Get( "ConfigurationsCTree" );
    if ( !confTree ) {
      cout << inFile->GetName() << endl;
      continue;
    }

    confTree->SetBranchAddress( "sigma", &cVal );
    confTree->SetBranchAddress( "statTree", &statTree );
    confTree->SetBranchAddress( "statConf", &statConf );
    confTree->SetBranchAddress( "inputC", &input );
    confTree->SetBranchAddress( "iConf", &iConf );
    confTree->SetBranchAddress( "jConf", &jConf );
    confTree->SetBranchAddress( "nBins", &nBins );
    confTree->SetBranchAddress( "dataRMS", &rms );

    if ( !confTree ) {
      cout << inFile->GetName() << endl;
      continue;
    }
    
    TTree *binTree = (TTree*) inFile->Get( "scalesTree" );
    binTree->SetBranchAddress( "sigma", &cVal );
    binTree->SetBranchAddress( "statTree", &statTree );
    binTree->SetBranchAddress( "inputC", &input );
    binTree->SetBranchAddress( "iBin", &iConf );
    binTree->SetBranchAddress( "nBins", &nBins );
  
    //========================
    //Reading configariont TTree
    unsigned int nEntriesConf = confTree->GetEntries();
    for ( unsigned int iEntry = 0; iEntry< nEntriesConf; iEntry++ ) {
      confTree->GetEntry(iEntry);
      statBin = SearchVectorBin( statTree, inputStat );
      if ( statBin == inputStat.size() ) inputStat.push_back( statTree );
      inputBin = SearchVectorBin( input, inputVals );
      if ( inputBin == inputVals.size() ) inputVals.push_back( input );
      binBin = SearchVectorBin( nBins, inputBins );
      if ( binBin == inputBins.size() ) inputBins.push_back( nBins );
      if ( nBins > maxBins ) maxBins = nBins;
      TString titleConfig;

      configCDistrib.resize( extents[inputBins.size()][inputStat.size()][inputVals.size()][maxBins][maxBins][2] );
      if ( !configCDistrib[binBin][statBin][inputBin][iConf][jConf][0] ) {
      	titleConfig = TString::Format( "CValueConfig_%d_%d_%d_%d_%d", nBins, statTree, (int) floor( input*1e6), iConf, jConf );
      	configCDistrib[binBin][statBin][inputBin][iConf][jConf][0] = new TH1D( titleConfig, titleConfig, 400, 0, 0.02 );
	configCDistrib[binBin][statBin][inputBin][iConf][jConf][0]->Sumw2();
	configCDistrib[binBin][statBin][inputBin][iConf][jConf][0]->SetDirectory(0);
      	configCDistrib[binBin][statBin][inputBin][iConf][jConf][0]->GetXaxis()->SetTitle( "C^{meas}" );
      	configCDistrib[binBin][statBin][inputBin][iConf][jConf][0]->GetYaxis()->SetTitle( "# Event" );
	saveHist.push_back( configCDistrib[binBin][statBin][inputBin][iConf][jConf][0] );
      	titleConfig = TString::Format( "CBiasConfig_%d_%d_%d_%d_%d", nBins, statTree, (int) floor( input*1e6), iConf, jConf );
      	configCDistrib[binBin][statBin][inputBin][iConf][jConf][1] = new TH1D( titleConfig, titleConfig, 100, -0.01, 0.01 );
	configCDistrib[binBin][statBin][inputBin][iConf][jConf][1]->Sumw2();
	configCDistrib[binBin][statBin][inputBin][iConf][jConf][1]->SetDirectory(0);
      	configCDistrib[binBin][statBin][inputBin][iConf][jConf][1]->GetXaxis()->SetTitle( "C^{meas}-C^{in}" );
      	configCDistrib[binBin][statBin][inputBin][iConf][jConf][1]->GetYaxis()->SetTitle( "# Event" );
	saveHist.push_back( configCDistrib[binBin][statBin][inputBin][iConf][jConf][1] );
      }
      configCDistrib[binBin][statBin][inputBin][iConf][jConf][0]->Fill( cVal );
      configCDistrib[binBin][statBin][inputBin][iConf][jConf][1]->Fill( cVal - input );

      configProfileStat.resize( extents[inputBins.size()][inputVals.size()][maxBins][maxBins][2] );
      if ( !configProfileStat[binBin][inputBin][iConf][jConf][0] ) {
      	titleConfig = TString::Format( "CProfileStatConfig_%d_%d_%d_%d", nBins, (int) floor( input*1e6), iConf, jConf );
      	configProfileStat[binBin][inputBin][iConf][jConf][0] = new TProfile( titleConfig, titleConfig, 100, 1, 6 );
	configProfileStat[binBin][inputBin][iConf][jConf][0]->SetDirectory( 0 );
	configProfileStat[binBin][inputBin][iConf][jConf][0]->Sumw2();
      	configProfileStat[binBin][inputBin][iConf][jConf][0]->GetXaxis()->SetTitle( "log(confStat)" );
      	configProfileStat[binBin][inputBin][iConf][jConf][0]->GetYaxis()->SetTitle( "<C^{meas}-C^{in}>" );
	saveHist.push_back( configProfileStat[binBin][inputBin][iConf][jConf][0] );
      	titleConfig = TString::Format( "CProfileRmsStatConfig_%d_%d_%d_%d", nBins, (int) floor( input*1e6), iConf, jConf );
      	configProfileStat[binBin][inputBin][iConf][jConf][1] = new TProfile( titleConfig, titleConfig, 100, 1, 6 );
	configProfileStat[binBin][inputBin][iConf][jConf][1]->Sumw2();
	configProfileStat[binBin][inputBin][iConf][jConf][1]->SetDirectory( 0 );
      	configProfileStat[binBin][inputBin][iConf][jConf][1]->GetXaxis()->SetTitle( "log(confStat)" );
      	configProfileStat[binBin][inputBin][iConf][jConf][1]->GetYaxis()->SetTitle( "RMS" );
	saveHist.push_back( configProfileStat[binBin][inputBin][iConf][jConf][1] );
      }
      configProfileStat[binBin][inputBin][iConf][jConf][0]->Fill( TMath::Log10(statConf), cVal - input );
      configProfileStat[binBin][inputBin][iConf][jConf][1]->Fill( TMath::Log10(statConf), rms );

      configProfileRMS.resize( extents[inputBins.size()][inputStat.size()][inputVals.size()] );
      if ( !configProfileRMS[binBin][statBin][inputBin] ) {
      	titleConfig = TString::Format( "CProfileRmsConfig_%d_%d_%d", nBins, statTree, (int) floor( input*1e6) );
	configProfileRMS[binBin][statBin][inputBin] = new TProfile( titleConfig, titleConfig, 40, 3, 5 );
	configProfileRMS[binBin][statBin][inputBin]->SetDirectory( 0 );
	configProfileRMS[binBin][statBin][inputBin]->Sumw2();
	configProfileRMS[binBin][statBin][inputBin]->GetXaxis()->SetTitle( "config RMS" );
	configProfileRMS[binBin][statBin][inputBin]->GetYaxis()->SetTitle( "<C^{meas}-C^{in}>" );
	saveHist.push_back( configProfileRMS[binBin][statBin][inputBin] );
      }
      configProfileRMS[binBin][statBin][inputBin]->Fill( rms, cVal-input );

      binMeanConfig.resize( extents[inputBins.size()][inputStat.size()][inputVals.size()][maxBins] );
      if ( !binMeanConfig[binBin][statBin][inputBin][iConf] ) {
      	titleConfig = TString::Format( "BinMeanConfig_%d_%d_%d_%d", binBin, statBin, inputBin, iConf );
	binMeanConfig[binBin][statBin][inputBin][iConf] = new TH1D( titleConfig, titleConfig, 300, -0.03, 0.03 );
	binMeanConfig[binBin][statBin][inputBin][iConf]->SetDirectory( 0 );
	binMeanConfig[binBin][statBin][inputBin][iConf]->Sumw2();
	binMeanConfig[binBin][statBin][inputBin][iConf]->GetXaxis()->SetTitle( "<C_{ii}^{meas}-C^{in}>" );
	saveHist.push_back( binMeanConfig[binBin][statBin][inputBin][iConf] );
      }
      if ( iConf == jConf ) 	binMeanConfig[binBin][statBin][inputBin][iConf]->Fill( cVal-input );

      configStat.resize( extents[inputBins.size()][inputStat.size()][maxBins][maxBins] );
      if ( !configStat[binBin][statBin][iConf][jConf] ) configStat[binBin][statBin][iConf][jConf] = statConf;
    }//end nEntriesConf

  //===================================
    //  reading final result TTree
  unsigned int nEntriesBin = binTree->GetEntries();
  for ( unsigned int iEntry = 0; iEntry < nEntriesBin; iEntry++ ) {
    binTree->GetEntry( iEntry );
    statBin = SearchVectorBin( statTree, inputStat );
    if ( statBin == inputStat.size() ) inputStat.push_back( statTree );
    inputBin = SearchVectorBin( input, inputVals );
    if ( inputBin == inputVals.size() ) inputVals.push_back( input );
    binBin = SearchVectorBin( nBins, inputBins );
    if ( binBin == inputBins.size() ) inputBins.push_back( nBins );
    TString title;

    binCDistrib.resize( extents[inputBins.size()][inputStat.size()][inputVals.size()][maxBins][2] );
    if ( !binCDistrib[binBin][statBin][inputBin][iConf][0] ) {
      title = TString::Format( "CValueBin_%d_%d_%d_%d", nBins, statTree, (int) floor( input*1e6), iConf );
      binCDistrib[binBin][statBin][inputBin][iConf][0] = new TH1D( title, title, 400, 0, 0.02 );
      binCDistrib[binBin][statBin][inputBin][iConf][0]->SetDirectory(0);
      binCDistrib[binBin][statBin][inputBin][iConf][0]->Sumw2();
      binCDistrib[binBin][statBin][inputBin][iConf][0]->GetXaxis()->SetTitle( "C^{meas}" );
      binCDistrib[binBin][statBin][inputBin][iConf][0]->GetYaxis()->SetTitle( "# Event" );
      saveHist.push_back(binCDistrib[binBin][statBin][inputBin][iConf][0]);
      title = TString::Format( "BiasBin_%d_%d_%d_%d", nBins, statTree, (int) floor( input*1e6), iConf );
      binCDistrib[binBin][statBin][inputBin][iConf][1] = new TH1D( title, title, 71, -0.021, 0.05 );
      binCDistrib[binBin][statBin][inputBin][iConf][1]->SetDirectory(0);
      binCDistrib[binBin][statBin][inputBin][iConf][1]->Sumw2();
      binCDistrib[binBin][statBin][inputBin][iConf][1]->GetXaxis()->SetTitle( "C^{meas}-C^{in}" );
      binCDistrib[binBin][statBin][inputBin][iConf][1]->GetYaxis()->SetTitle( "# Event" );
      saveHist.push_back(binCDistrib[binBin][statBin][inputBin][iConf][1]);
    }
    binCDistrib[binBin][statBin][inputBin][iConf][0]->Fill( cVal );
    //    if ( cVal-input < -0.007 ) cout << cVal << " " << input << endl;
    binCDistrib[binBin][statBin][inputBin][iConf][1]->Fill( cVal - input );

    fullBias.resize( extents[inputBins.size()][inputStat.size()][inputVals.size()] );
    if ( !fullBias[binBin][statBin][inputBin] ) {
      title = TString::Format( "BiasFull_%d_%d_%d", nBins, statTree, (int) floor( input*1e6) );
      fullBias[binBin][statBin][inputBin] = new TH1D( title, title, 600, -0.02, 0.02 );
      fullBias[binBin][statBin][inputBin]->Sumw2();
      fullBias[binBin][statBin][inputBin]->SetDirectory( 0 );
      fullBias[binBin][statBin][inputBin]->GetXaxis()->SetTitle( "C^{meas}-C^{in}" );
      fullBias[binBin][statBin][inputBin]->GetYaxis()->SetTitle( "# Event" );
      saveHist.push_back( fullBias[binBin][statBin][inputBin] );
    }
    fullBias[binBin][statBin][inputBin]->Fill( cVal- input );

  }//end nEntrieBin


    delete confTree;
    delete binTree;
    inFile->Close( "R" );
    delete inFile;
}

  TFile *outFile = new TFile(  (outName + "_hist.root").c_str(), "RECREATE" );
  for ( unsigned int iHist = 0; iHist < saveHist.size(); iHist++ ) {
    saveHist[iHist]->Write( "", TObject::kOverwrite );
  }
  outFile->Close( "R" );

  return 0;
  //================================================
  //Prepare a latex file to store plots
  cout << "starting plots" << endl;
  string latexFileName = outName + ".tex";
  fstream latex;
  gStyle->SetOptStat( 1 );
  latex.open( latexFileName, fstream::out | fstream::trunc );
  latex << "\\documentclass[a4paper,12pt]{article}" << endl;
  latex << "\\usepackage{graphicx}" << endl;
  latex << "\\usepackage{xcolor}" << endl;
  latex << "\\usepackage[a4paper, textwidth=0.9\\paperwidth, textheight=0.9\\paperheight]{geometry}" << endl;
  latex << "\\usepackage[toc]{multitoc}" << endl;
  latex << "\\title{Measured C distributions}" << endl;
  latex << "\\author{Christophe Goudet}" << endl;
  latex << "\\date{\\today}" <<endl;
  latex << "\\begin{document}\\maketitle" << endl;

  latex << "\\tableofcontents\\clearpage" << endl;

  //-----------------------------------------------------
  // Configuration bias distribution for c=0.007 and stat = 200k events
  //chose which set of parameter will be the central ones
  double centralInput = 0.007;
  unsigned int centralStat = 100000, centralNBins=6;
  latex << "\\section{Configurations}" << endl;
  statBin = SearchVectorBin(  centralStat, inputStat );
  inputBin = SearchVectorBin( centralInput, inputVals );
  binBin = SearchVectorBin( centralNBins, inputBins );
  cout << "statBin : " << statBin << endl;
  cout << inputStat[0] << endl;
  map< string, vector<TH1*> > histVec;
  map< string, vector<string> > legendStringVec;
  map< string, string > latexStringVec;

  for ( unsigned int iIConf = 0; iIConf < maxBins; iIConf++ ) {

    for ( unsigned int iJConf = 0; iJConf < maxBins; iJConf++ ) {
      if ( iIConf < iJConf ) continue;
      //   if ( !(iIConf==2 && iJConf==2) && !(iIConf==1 && iJConf==1) && !(iIConf==0 && iJConf==0) ) continue;
      // if ( !(iIConf==1 && iJConf==1) ) continue;
      legendStringVec.clear();
      latexStringVec.clear();
      histVec.clear();


      for ( unsigned int iInput = 0; iInput < inputVals.size(); iInput++ ) {
      	if ( configCDistrib[binBin][statBin][iInput][iIConf][iJConf][1] ) {
	  latexStringVec["distribCompareInput"] =  string(configCDistrib[binBin][statBin][inputBin][iIConf][iJConf][1]->GetName()) + "_CompareInput" ;
	  histVec["distribCompareInput"].push_back( configCDistrib[binBin][statBin][iInput][iIConf][iJConf][1] );
	  legendStringVec["distribCompareInput"].push_back( string( TString::Format("C=%2.2f ", inputVals[iInput]*1e2) ) + "%");
	}
      	if ( configProfileStat[binBin][iInput][iIConf][iJConf][0] ) {
	  latexStringVec["profileCompareInput"] =  string(configProfileStat[binBin][inputBin][iIConf][iJConf][0]->GetName()) + "_CompareInput" ;
	  histVec["profileCompareInput"].push_back( configProfileStat[binBin][iInput][iIConf][iJConf][0] );
	  legendStringVec["profileCompareInput"].push_back( string( TString::Format("C=%2.2f ", inputVals[iInput]*1e2) ) + "%");
	  latexStringVec["profileRmsCompareInput"] =  string(configProfileStat[binBin][inputBin][iIConf][iJConf][1]->GetName()) + "_CompareInput" ;
	  histVec["profileRmsCompareInput"].push_back( configProfileStat[binBin][iInput][iIConf][iJConf][1] );
	  legendStringVec["profileRmsCompareInput"].push_back( string( TString::Format("C=%2.2f ", inputVals[iInput]*1e2) ) + "%");
	}

      }


      for ( unsigned int iStat = 0; iStat < inputStat.size(); iStat++ ) {
	if( configCDistrib[binBin][iStat][inputBin][iIConf][iJConf][1] ) {
	  latexStringVec["distribCompareStat"] = string(configCDistrib[binBin][statBin][inputBin][iIConf][iJConf][1]->GetName()) + "_CompareStat";
	  histVec["distribCompareStat"].push_back( configCDistrib[binBin][iStat][inputBin][iIConf][iJConf][1] );
	  legendStringVec["distribCompareStat"].push_back( string( TString::Format("evt=%d", inputStat[iStat]) ) );
	}
      }


      vector<string> dumVec;
      for ( auto it = histVec.begin(); it != histVec.end(); it++) {
	//	unsigned int doNorm = ( it->first == "profileCompareInput" || it->first=="profileRmsCompareInput") ? 0 : 1;
	if ( !histVec[it->first].size() ) continue;
	//	DrawPlot( histVec[it->first], latexStringVec[it->first], legendStringVec[it->first], 0, doNorm, 0, 1, vector<double>(), {0.1, 0.8, 0.4, 0.95} );
	dumVec.push_back( latexStringVec[it->first] );
       }
      if ( dumVec.size() ) {
	latex << "\\subsection{" << TString::Format( "Configuration : %d %d ", iIConf, iJConf ) << "}" << endl;
	WriteLatexMinipage( latex, dumVec, 2 );
      }
    }
  }
  cout << "end plotting configurations" << endl;

  //---------------------------------------------------
  // final bias distribution for 0.007 and 200k events
  latex << "\\section{Bin Result}" << endl;
  
  for ( unsigned int iBin = 0; iBin < maxBins; iBin++ ) {
    
    if ( iBin >= maxBins/2 ) continue;
    latexStringVec.clear();
    legendStringVec.clear();
    histVec.clear();

    latexStringVec["distribCompareInput"] =  string(binCDistrib[binBin][statBin][inputBin][iBin][1]->GetName()) + "_CompareInput" ;
    for ( unsigned int iInput = 0; iInput < inputVals.size(); iInput++ ) {
      if ( binCDistrib[binBin][statBin][iInput][iBin][1] ) {
      histVec["distribCompareInput"].push_back( binCDistrib[binBin][statBin][iInput][iBin][1] );
      legendStringVec["distribCompareInput"].push_back( string( TString::Format("C=%2.2f ", inputVals[iInput]*1e2) ) + "%");
      }
    }

    
    latexStringVec["distribCompareStat"] =  string(binCDistrib[binBin][statBin][inputBin][iBin][1]->GetName()) + "_CompareStat" ;
    latexStringVec["binMeanConf"] =  string(binMeanConfig[binBin][statBin][inputBin][iConf]->GetName() ) + "_compareStat";
    for ( unsigned int iStat = 0; iStat < inputStat.size(); iStat++ ) {
      if ( binCDistrib[binBin][iStat][inputBin][iBin][1] ) {
      histVec["distribCompareStat"].push_back( binCDistrib[binBin][iStat][inputBin][iBin][1] );
      legendStringVec["distribCompareStat"].push_back( string( TString::Format("evt=%d", inputStat[iStat]) ) );
    }
      if ( binMeanConfig[binBin][statBin][inputBin][iBin] ) {
      	histVec["binMeanConf"].push_back( binMeanConfig[binBin][statBin][inputBin][iBin] );
      	legendStringVec["binMeanConf"].push_back( string( TString::Format("evt=%d", inputStat[iStat]) ) );
      }
    }

    latex << "\\subsection{" << TString::Format( "Bin : %d ", iBin ) << "}" << endl;
    vector<string> dumVec;
    for ( auto it = histVec.begin(); it != histVec.end(); it++) {
      //      unsigned int doNorm = ( false ) ? 0 : 1;
      //      DrawPlot( histVec[it->first], latexStringVec[it->first], legendStringVec[it->first], 0, doNorm, 0, 1, vector<double>(), {0.1, 0.8, 0.4, 0.95} );
      dumVec.push_back( latexStringVec[it->first] );
    }
      WriteLatexMinipage( latex, dumVec, 2 );

  }//end plotting final results

  //---------------------------------------------
  latex << "\\section{General Result}" << endl;
  latexStringVec.clear();
  legendStringVec.clear();
  histVec.clear();
  latexStringVec["finalBiasCompareInput"] =  fullBias[binBin][statBin][inputBin]->GetName() + string( "_CompareInput" );
  latexStringVec["configProfileRmsCompareInput"] = configProfileRMS[binBin][statBin][inputBin]->GetName() + string( "_CompareInput" );
  for ( unsigned int iInput = 0; iInput < inputVals.size(); iInput++ ) {
    if ( fullBias[binBin][statBin][iInput] ) {
    histVec["finalBiasCompareInput"].push_back( fullBias[binBin][statBin][iInput] );
    legendStringVec["finalBiasCompareInput"].push_back( string( TString::Format("C=%2.2f ", inputVals[iInput]*1e2) ) + "%");
    }
    if ( configProfileRMS[binBin][statBin][iInput] ) {
      histVec["configProfileRmsCompareInput"].push_back( configProfileRMS[binBin][statBin][iInput] );
      legendStringVec["configProfileRmsCompareInput"].push_back( string( TString::Format("C=%2.2f ", inputVals[iInput]*1e2) ) + "%");
    }
  }

  latexStringVec["finalBiasCompareStat"] = string(fullBias[binBin][statBin][inputBin]->GetName()) + "_CompareStat" ;
  latexStringVec["configProfileRmsCompareStat"] = configProfileRMS[binBin][statBin][inputBin]->GetName() + string( "_CompareStat" );
  for ( unsigned int iStat = 0; iStat < inputStat.size(); iStat++ ) {
    if ( fullBias[binBin][iStat][inputBin] ) {
      histVec["finalBiasCompareStat"].push_back( fullBias[binBin][iStat][inputBin] );
      legendStringVec["finalBiasCompareStat"].push_back( string( TString::Format("evt=%d", inputStat[iStat]) ) );
    }
    if ( configProfileRMS[binBin][iStat][inputBin] ) {
      histVec["configProfileRmsCompareStat"].push_back( configProfileRMS[binBin][iStat][inputBin] );
      legendStringVec["configProfileRmsCompareStat"].push_back( string( TString::Format("evt=%d", inputStat[iStat]) ) );
    }

  }
    vector<string> dumVec;
    for ( auto it = histVec.begin(); it != histVec.end(); it++) {
      //      unsigned int doNorm = ( false ) ? 0 : 1;
      //      DrawPlot( histVec[it->first], latexStringVec[it->first], legendStringVec[it->first], 0, doNorm, 0, 1, vector<double>(), {0.1, 0.8, 0.4, 0.95} );
      dumVec.push_back( latexStringVec[it->first] );
    }
      WriteLatexMinipage( latex, dumVec, 2 );

  

  latex << "\\end{document}" << endl;
  //-interaction=batchmode
  string commandLine = "pdflatex -interaction=batchmode " + latexFileName;
  cout << "latexFileName : " << commandLine << endl;
  system( commandLine.c_str() );
  system( commandLine.c_str() );
  system( commandLine.c_str() );
  //system( "rm ConfigurationsDistributions_*.pdf" );

  cout << "The End" << endl;



  return 0;
}

