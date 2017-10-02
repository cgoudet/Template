#include <iostream>
#include "TFile.h"
#include "TCanvas.h"
#include "TColor.h"
#include "PlotFunctions/SideFunctions.h"
#include <boost/program_options.hpp>
#include <fstream>
#include "PlotFunctions/AtlasStyle.h"
#include "PlotFunctions/AtlasUtils.h"
#include "PlotFunctions/AtlasLabels.h"


using std::cout;
using std::endl;
using std::vector;
namespace po = boost::program_options;
using std::ifstream;


int main( int argc, char* argv[] ) {
  po::options_description desc("LikelihoodProfiel Usage");
  string year;
  //define all options in the program
  desc.add_options()
    ("help", "Display this help message")
    //    ("year", po::value<string>(&year)->default_value("15"))
    ;

  // Create a map vm that contains options and all arguments of options       
  po::variables_map vm;
  po::store(po::command_line_parser(argc, argv).options(desc).style(po::command_line_style::unix_style ^ po::command_line_style::allow_short).run(), vm);
  po::notify(vm);
  
  if (vm.count("help")) {cout << desc; return 0;}
  //########################################
  SetAtlasStyle();
  vector<double> frameUp = { -2.7, 2.7, 0, 0};
  vector<double> frameDown = { frameUp[0], frameUp[1], 0, 0};
  vector <TH1D*> vectHistScale;
  vector <TH1D*> vectHistStat;
  vector <TH1D*> vectHistSystFill;
  vector <int> vectColor= {600, 632};//600=kBlue, 632=kRed
  vector <string> vectYear;
  string var;
  TH1D *histSyst=0; 

  TFile *inFile = TFile::Open( "/sps/atlas/a/aguerguichon/Calibration/ScaleResults/170608/EnergyScaleFactors.root" );
  TFile *systFile = TFile::Open( "/sps/atlas/a/aguerguichon/Calibration/ScaleResults/170601/EnergyScaleFactors.root" );

  TH1::AddDirectory(kFALSE);
  bool doReduce = 0;

  for ( unsigned int iScale =0; iScale < 2; iScale++ ) {
    if (iScale) vectYear={"1516"};
    else vectYear={"15", "16"};

    vectHistScale.clear();
    vectHistStat.clear();
    vectHistSystFill.clear();

    for (unsigned int iHist=0; iHist<vectYear.size(); iHist++){
      var = iScale? "c_"+vectYear[iHist] : "alpha_"+vectYear[iHist];
      TH1D *histScale = (TH1D*) inFile->Get( ("centVal_"+var).c_str() );
   
      histScale->SetLineColor( vectColor[iHist] );
      histScale->SetMarkerColor( vectColor[iHist] );
      histScale->SetMarkerStyle(20);
      
      TH1D* histStat = (TH1D*) histScale->Clone();
      histStat->ResetAttLine();
      histStat->ResetAttMarker();
      histStat->SetLineWidth(1.5);
      histStat->SetLineColor( kRed );

      var = iScale ?  "c" : "alpha";
      histSyst = (TH1D*) systFile->Get( ("totSyst_"+var).c_str() );

      TH1D *histScaleTot = (TH1D*) histScale->Clone();
      histScaleTot->SetFillColor( vectColor[iHist]-9 );
 
      for ( int iBin = 1; iBin<histStat->GetNbinsX()+1; iBin++ ) {
	histStat->SetBinContent( iBin, histScale->GetBinError( iBin ) );
	histStat->SetBinError( iBin, 0 );
	histScaleTot->SetBinError( iBin, histSyst->GetBinContent(iBin) );
      }
      vectHistScale.push_back( histScale );
      vectHistStat.push_back( histStat );
      vectHistSystFill.push_back( histScaleTot );
    } //end iHist
    
    histSyst->SetLineColor( kBlack );
    histSyst->SetLineWidth( 2.5 );
    histSyst->SetMarkerColor( kBlack );
    histSyst->SetMarkerStyle(20);
    
    // if ( doReduce )  {
    //   const TArrayD *binning = histScale->GetXaxis()->GetXbins();
    //   vector<double> vectBin;
    //   for ( int i=1; i<binning->GetSize(); i++ ) vectBin.push_back( binning->GetAt(i) );
    //   vectBin.pop_back();

    //   TH1D *dumScale = new TH1D( "dumScale", "dumScale", vectBin.size()-1, &vectBin[0] );
    //   TH1D *dumSyst = new TH1D( "dumSyst", "dumSyst", vectBin.size()-1, &vectBin[0] );

    //   for ( int i = 1; i<=dumScale->GetNbinsX(); ++i ) {
    // 	dumScale->SetBinContent( i, histScale->GetBinContent(i+1) );
    // 	dumSyst->SetBinContent( i, histSyst->GetBinContent(i+1) );
    // 	dumScale->SetBinError( i, histScale->GetBinError(i+1) );
    // 	dumSyst->SetBinError( i, histSyst->GetBinError(i+1) );
    //   }

    //   histScale=dumScale;
    //   histSyst = dumSyst;
    // }

    frameUp[2]   = iScale ? 0     : -0.03;
    frameUp[3]   = iScale ? 0.065 : ( doReduce ? 0.06 : 0.1 );
    frameDown[3] = iScale ? 6 : ( !doReduce ? 8e-2: 6 );
    frameDown[2] = ( !iScale && !doReduce ) ? 5e-5 : 0;

    TCanvas *canvas = new TCanvas();
    TPad padUp( "padUp", "padUp", 0, 0.32, 1, 1 );
    padUp.SetBottomMargin( 0.03 );
    padUp.Draw();
    padUp.cd();
    TH1F* dumUp = padUp.DrawFrame( frameUp[0], frameUp[2], frameUp[1], frameUp[3] );
    if (iScale){
    dumUp->GetYaxis()->SetTitleSize( 0.07);   
    dumUp->GetYaxis()->SetTitleOffset( 0.7);
    }
    else{
    dumUp->GetYaxis()->SetTitleSize( 0.085);   
    dumUp->GetYaxis()->SetTitleOffset( 0.6);
    }
    dumUp->GetYaxis()->SetLabelSize( 0.05);   
    dumUp->GetXaxis()->SetLabelSize( 0 );
    string legendVar = iScale ? "Additional constant term, c'" : "#alpha";
    dumUp->GetYaxis()->SetTitle( legendVar.c_str() );   
    TPad padDown( "padDown", "padDown", 0, 0, 1, 0.32 );
    padDown.SetTopMargin( 0.04 );
    padDown.SetBottomMargin( 0.35 );
    canvas->cd();
    padDown.Draw();
    padDown.cd();
    TH1F* dumDown = padDown.DrawFrame( frameDown[0], frameDown[2], frameDown[1], frameDown[3] );
    dumDown->GetYaxis()->SetLabelSize( 0.09 );
    dumDown->GetYaxis()->SetTitleSize( 0.15 );
    dumDown->GetYaxis()->SetTitleOffset( 0.35 );
    //xAxis
    //dumDown->GetXaxis()->SetTitle( "#eta_{CALO}" );
    dumDown->GetXaxis()->SetTitle( "#eta" );
    dumDown->GetXaxis()->SetTitleSize( 0.15 );
    dumDown->GetXaxis()->SetLabelSize( 0.15 );
    dumDown->GetXaxis()->SetTitleOffset( 1 );
    legendVar = "#delta"+legendVar;
    if ( frameDown[3] > 1 ) legendVar= "#deltac' (10^{-3})";
    dumDown->GetYaxis()->SetTitle( legendVar.c_str() );
    dumDown->GetYaxis()->CenterTitle();
    
    double x = 0.35;
    double y = 0.65;
    double s = 0.06;
    double lsize = 0.03;

    //padUp
    padUp.cd();
    for (unsigned int iHist=0; iHist<vectYear.size(); iHist++){
      vectHistSystFill[iHist]->Draw("E2, same");
      myBoxText( x, y-iHist*0.1,  vectHistSystFill[iHist]->GetFillColor(), "", s, lsize );
      myLineText( x, y-iHist*0.1, vectHistScale[iHist]->GetLineColor(), vectHistScale[iHist]->GetLineStyle(), "", s, vectHistScale[iHist]->GetLineWidth(), lsize ); 
      if (iScale) myMarkerText( x, y-iHist*0.1, vectHistScale[iHist]->GetMarkerColor(), vectHistScale[iHist]->GetMarkerStyle(), "Electrons from Z#rightarrowee", s, vectHistScale[iHist]->GetMarkerSize(), lsize ); 
      else  myMarkerText( x, y-iHist*0.1, vectHistScale[iHist]->GetMarkerColor(), vectHistScale[iHist]->GetMarkerStyle(), ("Electrons from Z#rightarrowee, 20"+vectYear[iHist]+" data").c_str(), s, vectHistScale[iHist]->GetMarkerSize(), lsize ); 
    }
    for (unsigned int iHist=0; iHist<vectYear.size(); iHist++) vectHistScale[iHist]->Draw("SAME");


    //padDown
    padDown.cd();
    histSyst->Draw("same");
    for (unsigned int iHist=0; iHist<vectYear.size(); iHist++){
      if ( iScale || doReduce ) {
	histSyst->Scale( 1e3 );
	vectHistStat[iHist]->Scale( 1e3 );
      }    
      vectHistStat[iHist]->SetLineColor(vectColor[iHist]);
      vectHistStat[iHist]->Draw("same");
      if (iScale) myLineText( 0.48, 0.75-iHist*0.1, vectHistStat[iHist]->GetLineColor(), vectHistStat[iHist]->GetLineStyle(), "Stat.", 0.11, vectHistStat[iHist]->GetLineWidth() ); 
      else myLineText( 0.48, 0.75-iHist*0.1, vectHistStat[iHist]->GetLineColor(), vectHistStat[iHist]->GetLineStyle(), ("Stat. (20"+vectYear[iHist]+" data)").c_str(), 0.11, vectHistStat[iHist]->GetLineWidth() ); 
    }
    if ( !iScale && !doReduce ) padDown.SetLogy(1);
    myLineText( 0.48, 0.85, histSyst->GetLineColor(), histSyst->GetLineStyle(), "Syst." ,0.11, histSyst->GetLineWidth() ); 

    canvas->cd();

    ATLASLabel( 0.3, 0.9, "Internal", 1, 0.052 );
    myText( 0.3, 0.84, 1, "#sqrt{s} = 13 TeV, L = 3.2 (2015) + 32.9 (2016) fb^{-1}", 0.042 );

    string suffix = doReduce ? "_reduced" : "";
    canvas->SaveAs( ("/sps/atlas/a/aguerguichon/Calibration/Plots/CS_"+var+"Off.eps").c_str() );
    canvas->SaveAs( ("/sps/atlas/a/aguerguichon/Calibration/Plots/CS_"+var+"Off.png").c_str() );
  }//end iScale

  return 0;

}
