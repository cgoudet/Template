#ifndef CHIMATRIX_H
#define CHIMATRIX_H

#include "TRandom.h"
#include "Setting.h"
#include "TH1D.h"
#include "TTree.h"
#include "TH2D.h"
#include "TLorentzVector.h"
#include "TFile.h"
#include <map>
#include <bitset>
#include <sstream>

using std::stringstream;
using std::bitset;
using std::map;

namespace TemplateMethod {
  class ChiMatrix
  {

  public:
    /**\brief Default Constructo
     */
    ChiMatrix();
 
    /**\brief Constructor which initialize m_name
     */
    ChiMatrix( string name );

    /** Overloaded Constructor
	\param name Name of the object
	\param configSetting Setting to be used
    */
    ChiMatrix( string name, Setting &configSetting );
    ~ChiMatrix();

    double GetScale( unsigned int iVar ) const { return iVar ? m_sigma : m_alpha; };
    double GetErrScale( unsigned int iVar ) const { return iVar ? m_errSigma : m_errAlpha; };
    double GetAlphaMin() const { return m_alphaMin; }
    double GetAlphaMax() const { return m_alphaMax; }
    double GetSigmaMin() const { return m_sigmaMin; }
    double GetSigmaMax() const { return m_sigmaMax; }
    unsigned int  GetQuality() const { return m_quality.to_ulong(); };
    unsigned int GetStat() const { return m_dataZMass ? m_dataZMass->GetEntries() : 0;}
    double GetDataRMS() const { return m_dataZMass->GetStdDev(); }
    double GetDataMean() const { return m_dataZMass->GetMean(); }

    void SetAlphaMin( double alphaMin ) { m_alphaMin = alphaMin; }
    void SetAlphaMax( double alphaMax ) { m_alphaMax = alphaMax; }
    void SetSigmaMin( double sigmaMin ) { m_sigmaMin = sigmaMin; }
    void SetSigmaMax( double sigmaMax ) { m_sigmaMax = sigmaMax; }
    void SetSetting( Setting& setting );

    /**\brief Measure scales factors for the configuration
       \return 0 OK
       \return 1 1VAR extraction with a 2D template which do not contains alpha=0. (sigma=0 always exists)

       - Normalize histograms
       - Compute chi2
       - Do Fit procedure
       - values of alpha_ij, sigma_ij and their errors are set into the dedicated variables
    */
    int ExtractFactor( );

    /**\brief Fill event in data histogram or in MC Ntuple
       \param e1 First electron
       \param e2 Second electron
       \param isData Is input event data
       \param weight Weight to apply to the event

       - if isData, fill the data mass distribution
       - id !isData, Create a temporary MC TTree to hold event variables ad fill it
    */
    void FillDistrib( TLorentzVector &e1, TLorentzVector &e2, bool isData, double weight = 1 );

    /**\brief Load templates
       \param inFileName input root file name
       \param justTemplate Whether to load templates related objects

       \return 0 OK
       \return 1 File can not be opened
       \return 2 One template can not be found. Details in error message
       \return 3 Some histograms can not be found. Details in error message

       - Variables not templates-related : m_chiMatrix, m_dataZMass, chi2FitConstVar, chi2FitNonConstVar
    */
    int Load( TFile *inFile, bool justTemplate = false );

    /**\brief Save the class
       \param outFile TFile in which to save
       \param justTemplate Save only templates related ojects

       \return 0 OK
       \return 1 TFile is a 0 pointer
       \return 2 TFile is not opened

       - Variables not templates-related : m_chiMatrix, m_dataZMass, chi2FitConstVar, chi2FitNonConstVar
    */
    int Save( TFile *outFile , bool justTemplate = false );


    /**\brief Create the content of the note for a configuration
       \param path directory path where to save the plots
       \param latexFileName latex file to write in 
    */
    void MakePlot( stringstream &ss, string path = "" );

    /*\brief Create the templates
      \return 0 OK
      \param nTemplates Number of bin in eta and sigma. If 0, these values are taken from m_setting.

      Call ChiMatrix.OptimizeRanges if needed.
      Create a 2D set of TH1D to hold template mass distribution
      Call FillTemplates();
      Call FillChiMatrix();
    */
    int CreateTemplates( int nTemplates = 0 );

    /**\brief Change local boundaries of alpha and sigma to m_alpha +/- X * m_errAlpha

       Create Template historams
       FillTemplate
       FillChiMatrix
       FitHist

       X can be chosen in the configuration file
    */
    void OptimizeRanges( );

    /**\brief Compute a chi2 between one chosen template and data histogram
       \param MCHist template to compare to data
       \param isIncreasedStat Should the MC errors should be corrected for additionnal smearing
       \return chi2/ndf

       When computing chi2 between data and MC of same number of events, we are sensitive to the statistical fluctuations induced by the smearing of the Template.  
       These fluctuations are purely created by the method and give unstability to the fit. 
       To correct that, MC events can be smeared several times independently and added. 
       The fluctuations will be smoothed but statistical uncertainties of MC will be artificially low. 
       isIncreasedStat is to switch on the error correction of the MC bin. 
       The number of added events will be taken from the configuration file.
    */
    double ComputeChi2( TH1D *MCHist, bool isIncreasedStat = false );

    /**\brief Fit an histogram 
       \param hist histogram to be fitted
       \param mode choice of fitting function to chose
       \param chiMinLow value of chi2 on left side to use to find fitting range low value
       \param chiMinUp value of chi2 on sight side to use to find fitting range high value
       \return TFitResultPtr pointer to the result of the fit

       FindFitBestRange()

       mode :
       - 0 : quadratic fit
       - 1 : cubic fit
    */
    TF1* FitHist( TH1D* hist, unsigned int mode, double chiMinLow=0, double chiMinUp=0 );

    /**\brief Create a local TTree to hold MC events of the configuration
     */
    void CreateMCTree( );

    /**\brief Find the minimum of the chi2 matrix

       Call FillChiMatrix()
       Create 1D histogram to fit
       Call ChiMatrix.FitHist()

       When doing scale and smearing, user can choose through config file which variable is first fitted. (default for doc ALPHA )
     
       User can choose the fitting method :

    */
    void FitChi2();

  private :

    /**\brief Create templates

       Run over all event in the MC TTree of the configuration.
       Scale each event with the set ot hypothesis scales and fill templates mass distribution. 
       Unit change from MeV to GeV is done here
       Mass is computed from pt, eta, phi and the electron mass. Total energy not used.
    */
    void FillTemplates();

    /**\brief Create the m_chiMatrix variable and fill it with chi2 computed between templates and data
     */
    int FillChiMatrix();

    /**\brief Link TTree branches to local variables
     */
    int LinkMCTree();

    /**\brief Fill m_alphaValues and m_sigmaValues with the alpha/sigma values corresponding to the templates
       \param define how many values will be computed between extremum. If 0, nTemplates taken from configuration file.


       N+1 values are computed according to the formula.
       m_alphaMin + ( m_alphaMax - m_alphaMin ) /  nTemplates * i_alpha
       If only one scale is measure, the value of the other one is just 0.   
    */
    void FillScaleValues( int nTemplates = 0 );


    /**\brief Properly delete all templates and clear the 2D vector
     */
    void ClearTemplates();

    /** \brief Quality cut of the configuration
	\return bitset integer with quality of the configuration. Good quality = 0

	Quality requirements are the followings :
	- MC and data event number higher than limit set in configuration file
	- Threshold mass of the configuration higher than limit set in the conf file. 
	When reconstructing the mass of the Z from both electron, the analysis cut on electron pt coupled with large eta separation will lead the lightest Z to be produced to be in our analysis range.
	This would lead to highly deformed ditributions. So we decide to remove all configuration whose lightest possible Z is above a limit set in the configuration file.
    */
    unsigned int IsGoodQuality();


    bool OptimizeVect( std::vector<double> &y, 
		       const std::vector<double> &x, 
		       const double allowedMaxRange,
		       double &width,
		       double &limit,
		       double &minChi );

    
    /** \brief Name og the object

	Each ChiMatrix object must have a different name in order for the histograms not to overwrite each other.
    */
    string m_name;

    /**\brief 2D matrix containing chi^2
     */
    TH2D *m_chiMatrix;

    /**\brief MC ZMass distributions
     */
    vector< vector< TH1D* > > m_MCZMass;

    /**\brief Data ZMass Distribution
     */
    TH1D* m_dataZMass;

    /**\brief Settings attriute
     */
    Setting* m_setting;

    /**\brief Value of alpha in this configuration
     */
    double m_alpha;

    /**\brief Value of sigma in this configuration
     */
    double m_sigma;

    TRandom m_rand;

    /**\brief Store the chi2 fits for the first non-const variable
     */
    vector< TH1D* > m_chi2FitNonConstVar;

    /**\brief Store chi2fit for the constant variable
     */
    TH1D *m_chi2FitConstVar;

    /**\brief Store correlation plot between the two variables
     */
    TH1D* m_corAngle;

    double m_errAlpha;
    double m_errSigma;

    /**\brief Values of scale factors for templates
     */
    vector< double > m_scaleValues;

    /**\brief Values of smearing factors for templates
     */
    vector< double > m_sigmaValues;

    /*\brief Local lower boundary for alpha
     */
    double m_alphaMin;
  
    /*\brief Local upper boundary for alpha
     */
    double m_alphaMax;

    /*\brief Local lower boundary for sigma
     */
    double m_sigmaMin;

    /*\brief Local upper boundary for sigma
     */
    double m_sigmaMax;

    bitset<8> m_quality;

    unsigned int  m_eta1Bin;
    unsigned int  m_eta2Bin;

    TTree *m_MCTree;
    map< string, double > m_mapVar1;
    map< string, double > m_mapVar2;
    map< string, double > m_mapVarEvent;

  };
}
#endif
