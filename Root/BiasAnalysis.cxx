#include <iostream>
#include <istream>
#include <fstream>
#include <map>
#include <vector>
#include <string>
#include <sstream>
#include <boost/program_options.hpp>
#include <boost/multi_array.hpp>
#include <iomanip>

#include "TMatrixD.h"
#include "TH1.h"
#include "TF1.h"
#include "TFile.h"
#include "TTree.h"
#include "TBranch.h"
#include "TCanvas.h"
#include "TString.h"
#include "TGraphErrors.h"

#include "RooDataSet.h"
#include "RooRealVar.h"
#include "RooArgSet.h"
#include "RooGaussian.h"

#include "Template/BiasAnalysis.h"
#include "PlotFunctions/DrawPlot.h"
#include "PlotFunctions/DrawOptions.h"
#include "PlotFunctions/SideFunctionsTpp.h"
#include "PlotFunctions/SideFunctions.h"
#include "PlotFunctions/MapBranches.h"
#include "PlotFunctions/InvertMatrix.h"
#include "PlotFunctions/Foncteurs.h"

using namespace ChrisLib;
using namespace std;
using namespace RooFit;
namespace po = boost::program_options;

using boost::extents;
using boost::multi_array;

using std::logic_error;
using std::runtime_error;
using std::invalid_argument;

//====================================================
//Read configuration options from a configuration file
BiasAnalysis::BiasAnalysis(string configFileName)
{  
  po::options_description configOptions("Configuration options");
  configOptions.add_options()
    ("help", "Display this help message")
    ("variablesBias", po::value<vector<string>>(&m_variablesBias)->multitoken(),"Variables to study bias")
    /*accepted variables for ConfugurationsCTree: 
      - double: sigma, errSigma, inputC, dataRMS, nOptim;
      - unsigned int: iConf, jConf, statConf, statTree, indepDistorded, indepTemplates, runNumber, nBins, bootstrap, fitMethod;
      accepted variables for scalesTree:
      - double: sigma, errSigma, inputC, dataRMS, nOptim;
      - unsigned int: iBin, statTree, indepDistorded, indepTemplates, runNumber, nBins, bootstrap, fitMethod, inversionMethod;
    */
    ("variablesStats", po::value<vector<unsigned int>>(&m_variablesStats)->multitoken(),"Variables for the csv file")
    /*0: mean, rms, errMean
     */
    ("methodStats", po::value<unsigned int>(&m_methodStats), "")
    /*0: compute mean and rms
      1: h->GetMean(), h->GetRMS()
      2: get mean given by the Gaussian fit of the histogram
      3: RooFit gauss
    */
    ("selectTree", po::value<string>(&m_inTreeName), "")
    /*ConfigurationsCTree or scalesTree
     */    
    // ("checkDistri", po::value<unsigned int>(&m_checkDistri)->default_value(0),"")
    // /*0= bias study
    //   1= errSigma distribution
    // */
    
    ("nBins", po::value<unsigned int>(&m_nBins),"")
    
    ;
    
  po::variables_map vm;
  ifstream ifs( configFileName, ifstream::in );
  po::store(po::parse_config_file(ifs, configOptions), vm);
  po::notify(vm);  

  cout<<"Configuration file "<<configFileName<<" loaded."<<endl;
}


//==================================================
//Clear attributes
BiasAnalysis::~BiasAnalysis()
{
  m_variablesBias.clear();
  m_variablesStats.clear();

  m_mapHist.clear();
  m_mapSumX.clear();
  m_mapSumXM.clear();
  m_mapStatHist.clear();
  m_mapRooVar.clear();
  m_mapRooDataSet.clear();
  m_mapRooGauss.clear();
  m_mapCij.clear();
  m_mapErrCij.clear();
  m_mapCi.clear();
  m_mapErrCi.clear();
 
  m_inTreeName.clear();
  
  m_methodStats=-999;
  m_nBins=-999;
  m_maxX=-999;
  m_minX=-999;

  cout<<"Attributes cleaned."<<endl;
}

//===================================================
double BiasAnalysis::GetInput(TH1D *h, unsigned int iBin, unsigned int jBin){ return sqrt( (pow(h->GetBinContent(iBin),2)+ pow(h->GetBinContent(jBin),2)) / 2 ); }
double BiasAnalysis::GetInput(TH1D *h, unsigned int iBin){ return h->GetBinContent(iBin); }

//===================================================
void BiasAnalysis::SelectVariables(vector <string> dataFiles, bool isAlpha)
{
  cout<<"BiasAnalysis::SelectVariables"<<endl;

  map <string, RooArgSet*> mapArgSet; 
  TTree *inTree{0};
  TFile *inFile{0};
  double bias{0};
  string histName, rooName, errSigma, value;

  TH1::AddDirectory(kFALSE);

  for ( unsigned int iFile=0; iFile <dataFiles.size(); iFile++ ) { 
    inFile= TFile::Open(dataFiles[iFile].c_str());
    if ( !inFile ) throw invalid_argument( "BiasAnalysis::SelectVariables: Unknown input file "+dataFiles[iFile] );

    inTree = (TTree*) inFile->Get(m_inTreeName.c_str());  
    if ( !inTree ) throw runtime_error( "BiasAnalysis::SelectVariables: "+m_inTreeName + " in " + dataFiles[iFile] + " does not exist." );
    MapBranches mapBranches; 
    mapBranches.LinkTreeBranches(inTree);

    TH1D *inputHist=(TH1D*)inFile->Get("histInput");

    for ( unsigned int iEntry=0; iEntry<inTree->GetEntries(); iEntry++ ) {
      inTree->GetEntry(iEntry);
      histName =""; 
      if ( mapBranches.GetUnsigned( "nBins" )!=m_nBins ) continue;

      if (m_inTreeName.find("Configuration")!=string::npos) bias = mapBranches.GetDouble( "scale" )- GetInput( inputHist,mapBranches.GetUnsigned( "iConf" )+1, mapBranches.GetUnsigned( "jConf" )+1 );
      else bias = mapBranches.GetDouble( "scale" )- GetInput( inputHist, mapBranches.GetUnsigned( "iBin" )+1 );

      //Combine all possible values of each variable
      for ( unsigned int iVar =0; iVar < m_variablesBias.size(); iVar++ ){
	value=mapBranches.GetLabel( m_variablesBias[iVar] );
	
	if (value.find("0.")!=string::npos) value=to_string( stoi(ReplaceString("0.", "")(value)) );
	
	if ( iVar == m_variablesBias.size()-1 ) {
	  histName+= m_variablesBias[iVar]+"_"+value; 
       	  if ( !m_mapHist.count(histName) ) {
	    if (isAlpha) m_mapHist[histName] = new TH1D( histName.c_str(), "", 1e6, -0.01, 0.01 );
	    else m_mapHist[histName] = new TH1D( histName.c_str(), "", 10000, -0.1, 0.1 );
	    m_mapHist[histName]->Sumw2();

	    //Create elements needed to fit using RooFit
	    rooName= "bias_"+histName;
	    m_mapRooVar[histName] = new RooRealVar( rooName.c_str(), "C^{meas}-C^{input}", -0.1, 0.1 );
	    rooName= "set_"+histName;
	    mapArgSet[histName] = new RooArgSet( rooName.c_str() );
	    rooName= "data_"+histName;
	    m_mapRooDataSet[histName] = new RooDataSet( rooName.c_str(), "data", *mapArgSet[histName] );
	  }
	  m_mapHist[histName]->Fill( bias );
	  m_mapRooVar[histName]->setVal( bias );
	  mapArgSet[histName]->add( *m_mapRooVar[histName] );
	  m_mapRooDataSet[histName]->add( *mapArgSet[histName] );
	}
	histName += m_variablesBias[iVar]+"_"+value+"_";   
      }//end iVar
    }//end iEntry

    delete inputHist; inputHist=0;
    inFile->Close(); //close file and delete tree
    delete inFile; inFile=0;
    
  }//end iFile

  cout<<"BiasAnalysis::SelectVariables Done"<<endl;
  return;
}

//====================================================
void BiasAnalysis::RemoveExtremalBins(TH1D* &hist)
{
  unsigned int lowBin = 1;
  unsigned int upBin = hist->GetNbinsX();
  m_minX=hist->GetXaxis()->GetXmin();
  m_maxX=hist->GetXaxis()->GetXmax();

  while ( hist->GetBinContent( lowBin ) == 0 && lowBin!=upBin ) lowBin++;
  while ( hist->GetBinContent( upBin ) ==0 && lowBin!=upBin ) upBin--;
  if ( lowBin != upBin ) {
    m_minX = hist->GetXaxis()->GetBinLowEdge( lowBin );
    m_maxX = hist->GetXaxis()->GetBinUpEdge( upBin );
  }
  hist->GetXaxis()->SetRangeUser( m_minX, m_maxX );
  cout<<"BiasAnalysis::RemoveExtremalBins Done"<<endl;
  return;
}

//====================================================
vector<double> BiasAnalysis::GetBiasStat( TH1* hist, string histName, unsigned int method)
{
  cout<<"BiasAnalysis::GetBiasStat"<<endl;

  double mean{0}, errMean{0}, rms{0};
  vector<double> vectStat;
  unsigned int nBins=hist->GetNbinsX();
  double xMin = hist->GetXaxis()->GetBinCenter(2);
  double xMax = hist->GetXaxis()->GetBinCenter(nBins-1);
  
  switch (method) {
    // case 0: {//compute mean and rms
    // 	mean= m_mapSumX[histName]/m_mapNEff[histName];
    // 	rms= sqrt( m_mapSumXM[histName]/m_mapNEff[histName] );
    // 	errMean= rms/sqrt(m_mapNEff[histName]);
    // 	break;
    // }

  case 1:{//get mean and rms from histogram
    mean= hist->GetMean();
    rms= hist->GetRMS();
    errMean= rms/sqrt( hist->GetEntries() );
    break;
  }

  case 2: {//get from gaussian fit
    TF1 *f0 = new TF1("f0", "gaus", xMin, xMax);
    hist->Fit("f0","R");
    mean = hist->GetFunction("f0")->GetParameter(1);
    rms = hist->GetFunction("f0")->GetParameter(2);
    if (mean-1.5*rms>=xMin) xMin= mean-1.5*rms;
    if (mean+1.5*rms<=xMax && mean+1.5*rms>xMin) xMax= mean+1.5*rms;
    TF1 *f1= new TF1("f1", "gaus", xMin, xMax);
    hist->Fit("f1","R");
      
    mean = hist->GetFunction("f1")->GetParameter(1);
    rms = hist->GetFunction("f1")->GetParameter(2);
    errMean = hist->GetFunction("f1")->GetParError(1); 
    
    delete f1; f1=0;
    delete f0; f0=0;
    break;
  }
  case 3: {//gauss RooFit
    RooRealVar* meanFit = new RooRealVar("meanFit", "mean", -1, 1);
    RooRealVar* sigmaFit= new RooRealVar("sigmaFit", "sigma",0, 1);
    m_mapRooGauss[histName]= new RooGaussian("gauss", "gauss", *m_mapRooVar[histName], *meanFit, *sigmaFit);    
    m_mapRooGauss[histName]->fitTo( *m_mapRooDataSet[histName], Range( xMin+(xMax-xMin)*0.02, xMax ) );
    rms= sigmaFit->getValV();
    mean= meanFit->getValV();
    m_mapRooGauss[histName]->fitTo( *m_mapRooDataSet[histName], Range( mean-1.5*rms, mean+1.5*rms) );
    delete meanFit; meanFit=0;
    delete sigmaFit; sigmaFit=0;
    break;
  }
  }//end switch

  vectStat.push_back(mean);
  vectStat.push_back(rms);
  vectStat.push_back(errMean);
  cout<<"BiasAnalysis::GetBiasStat Done"<<endl;
  return vectStat;
}

//=====================================================

void BiasAnalysis::SaveBiasInfo( string outName )
{
  cout<<"BiasAnalysis::SaveBiasInfo"<<endl;
  vector <string> vectInfo;
  vector <double> vectStat;
  unsigned int skip{0};
  TFile *outRootFile = new TFile( (outName+".root").c_str(), "RECREATE" );
  ofstream outputFile( (outName+".csv").c_str(), ios::out );

  for ( auto it=m_mapHist.begin(); it!=m_mapHist.end(); ++it )  {
    RemoveExtremalBins(it->second);
    it->second->Write(); 

    //writing the csv file
    if (!skip) {
      outputFile<<"HistogramName"<<" "<<"NumberEntries"<<" ";
      for ( unsigned int iVarBias=0; iVarBias<m_variablesBias.size(); iVarBias++ ) outputFile<<m_variablesBias[iVarBias]<<" ";
      outputFile<<"Mean"<<" "<<"RMS"<<" "<<"ErrorMean"<<"\n";
      }
    skip++;
    ParseVector(it->first, vectInfo, '_');
    outputFile<<it->first<<" "<<it->second->GetEntries()<<" ";
    for (unsigned int i=1; i<vectInfo.size(); i+=2) outputFile<<vectInfo[i]<<" ";
    vectInfo.clear();

    vectStat=GetBiasStat( it->second, it->first, m_methodStats );
    for (unsigned int i=0; i<vectStat.size(); i++) outputFile<<vectStat[i]<<" ";
    outputFile<<"\n";
    m_mapStatHist[it->first]=vectStat;
  }//end iteration over histograms

  outRootFile->Close();
  delete outRootFile; outRootFile=0;
  //  delete hist; hist=0;
  outputFile.close();
  cout<<"BiasAnalysis::SaveBiasInfo Done"<<endl;

  return;
}


//==================================================
void BiasAnalysis::MakeBiasPlots(string path, string latexFileName, string comment)
{
  cout<<"BiasAnalysis::MakeDistriPlots"<<endl;
  vector <string> vectStatNames, vectOpt, vectTmp, vectHistNames;
  string histName;
  string legLatex, line="";

  vectStatNames.push_back("Mean");
  vectStatNames.push_back("RMS");
  vectStatNames.push_back("Error mean");

  for ( auto it=m_mapHist.begin(); it!=m_mapHist.end(); ++it )  {
    histName = it->first;
    RemoveExtremalBins(it->second);
    DrawOptions drawOpt;

    for (unsigned int iStat=0; iStat<vectStatNames.size(); iStat++) { //Quote the mean, rms, errMean of the hist on the plot
      legLatex= "latex="+ vectStatNames[iStat]+ ": " + TString::Format("%.3e", m_mapStatHist[histName][iStat]);
      vectOpt.push_back(legLatex.c_str());
      legLatex= "latexOpt= 0.65 "+ TString::Format("%.3f", 0.9-iStat*0.05);
      vectOpt.push_back(legLatex.c_str());
    }

    ParseVector(histName, vectTmp, '_');
    for (unsigned int iInfo=0; iInfo<vectTmp.size()-1; iInfo+=2){
      legLatex= "latex="+vectTmp[iInfo]+": "+vectTmp[iInfo+1];
      vectOpt.push_back(legLatex.c_str());
      legLatex= "latexOpt= 0.15 "+ TString::Format("%f", 0.9-iInfo*0.025);;
      vectOpt.push_back(legLatex.c_str());
    }

    vectOpt.push_back("rangeUserX="+to_string(m_minX)+" "+to_string(m_maxX));
    vectOpt.push_back("yTitle=#Events");
    vectOpt.push_back("extendUp= 0.4");
    vectOpt.push_back("xTitle=C^{meas}-C^{input}");
    vector <TH1*> vectHistTmp={it->second};

    if (m_methodStats == 3)  DrawPlot(m_mapRooVar[histName], {m_mapRooDataSet[histName], m_mapRooGauss[histName]}, path+histName,{vectOpt} );
    else {
      drawOpt.FillOptions(vectOpt); 
      drawOpt.AddOption("outName", path+histName);
      drawOpt.Draw( vectHistTmp );
    }       
    vectHistNames.push_back(path+histName);
    vectTmp.clear();
    vectOpt.clear();
    vectHistTmp.clear();
  }

  MakePdf(path+latexFileName, vectHistNames, comment);
  cout<<"BiasAnalysis::MakeDistriPlots Done"<<endl;
  return;
}

//==============================================
void BiasAnalysis::MakePdf(string latexFileName, vector<string> vectHistNames, string comment)
{
  fstream stream;
  latexFileName+=".tex";
  stream.open( latexFileName.c_str(), fstream::out | fstream::trunc );
  WriteLatexHeader( stream, "Bias study" , "Antinea Guerguichon" );

  stream <<comment <<"\\newline"<<endl;
  stream << "\\indent Method to get stats: "<<m_methodStats<<"\\newline  "<< endl;  
  stream << "\\indent Tree: "<< m_inTreeName<<"\\newline  "<<endl;
  stream << "\\indent Variables: ";
  for (unsigned int iVar=0; iVar< m_variablesBias.size(); iVar++)    {
    if (iVar == m_variablesBias.size()-1) stream<<m_variablesBias[iVar] <<"\\newline  ";
    else  stream  << m_variablesBias[iVar] <<", ";
  }

  WriteLatexMinipage( stream, vectHistNames, 2);
  stream << "\\end{document}" << endl;
  string commandLine = "pdflatex  -interaction=batchmode " + latexFileName;
  system( commandLine.c_str() );
  system( commandLine.c_str() );
  system( commandLine.c_str() );
  stream.close();
  cout<<"BiasAnalysis::MakePdf "+latexFileName+"  Done"<<endl;
}
