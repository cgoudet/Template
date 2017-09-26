#include <iostream>
#include <istream>
#include <fstream>
#include <map>
#include <vector>
#include <string>
#include "boost/multi_array.hpp"
#include "TH1.h"
#include "TMatrixD.h"
#include "RooDataSet.h"
#include "RooGaussian.h"

using namespace RooFit;

/**\brief The BiasAnalysis class allows to analyze the toys generated with the GenerateToyTemplates routine.
 */						\

class BiasAnalysis
{

public:
  BiasAnalysis(std::string configFileName);
  ~BiasAnalysis();

  /**\brief Retrieve the injected value in a given configuration from the injected value in each bin of the configuration.
   */
  double GetInput(TH1D *h, unsigned int iBin, unsigned int jBin);

  /**\brief Retrieve the injected value in a given bin.
   */
  double GetInput(TH1D *h, unsigned int iBin);

  /**\brief Select the variable to analyze:
     - read files, link tree branches to local variables and sorting variables according to the ones selected.                                                                                 - compute bias
     - fill the map m_mapHist with unique histogramms for each combination of all possible values of each variable.                                                                        
 */ 
  void SelectVariables (std::vector <std::string> dataFiles, bool isAlpha=0);

  /**\brief Get mean, RMS and mean from each histogram of the map m_mapHist in 3 different ways:
     - method=0 : exact computation 
     - method=1 (default): get stat with ROOT methods (GetMean()...)
     - method 3 : Gauss RooFit. Idea was to be able in the future to fit the distribution with asymetric gaussians...
   */
  std::vector<double> GetBiasStat( TH1* hist, std::string histName, unsigned int method=1);

  /**\brief Save some information (name of histogram, number of entries, mean, RMS and error on mean) from the map m_mapHist in a root file and a csv file.
   */
  void SaveBiasInfo (std::string outName);
  
  /**\brief Draw bias distribution plots and save them into a pdf file.			     
   */
  void MakeBiasPlots (std::string path, std::string latexFileName, std::string comment=" ");

  void MakePdf (std::string latexFileName, std::vector <std::string> vectHistNames ,std::string comment=" ");

  /**\brief Remove empty extremal bins. 
   */
  void RemoveExtremalBins(TH1D* &hist);

 private:
  std::vector <std::string> m_variablesBias;
  std::vector <unsigned int> m_variablesStats;

  std::map <std::string, TH1D*> m_mapHist;
  std::map <std::string, double> m_mapSumX;
  std::map <std::string, double> m_mapSumXM;
  std::map <std::string, std::vector<double> > m_mapStatHist;
  std::map <std::string, RooRealVar*> m_mapRooVar;
  std::map <std::string, RooDataSet*> m_mapRooDataSet;
  std::map <std::string, RooGaussian*> m_mapRooGauss;
  std::map <unsigned long long, TMatrixD> m_mapCij;
  std::map <unsigned long long, TMatrixD> m_mapErrCij;
  std::map <unsigned long long, TMatrixD> m_mapCi;
  std::map <unsigned long long, TMatrixD> m_mapErrCi;

  std::string m_inTreeName;

  unsigned int m_nBins;
  unsigned int m_methodStats;
  double m_minX, m_maxX;
};
