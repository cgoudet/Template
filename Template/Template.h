#ifndef TEMPLATE_H
#define TEMPLATE_H
#include "PlotFunctions/MapBranches.h"
#include "Setting.h"
#include "TTree.h"
#include "TH2F.h"
#include "ChiMatrix.h"
#include "TFile.h"
#include "TMatrixD.h"
#include "TRandom3.h"
#include <vector>
#include <map>
#include "boost/multi_array.hpp"
#include <sstream>

using std::stringstream;
using boost::multi_array;
using std::vector;
using std::string;
using std::map;

namespace TemplateMethod {
  /**\brief Main Class

     Central class that perform the measurement.
     To use it :
     - Create an instance with a configuration file ( examples given in ConfigFiles ), MC and DataNtuples.
     One can also just use MC ntuple to perform a closure. Input value and closure switch are modified within configuration file.
     - Call Template.ApplyCorrection to apply initial scale factors
     - Call Template.CreateTemplate to create MC templates in each configuration
     - Call Template.ExtractFactor To perform the measurement

     Results will be put into an histogram measScale_alpha(c) containing scale as input and scale statistical uncertainty as bin error.
     Scales and their uncertainty at configuration level are available in a TMatrixD combin(Err)Alpha.

     One can save the templates and/or final results and load them back.

     Binning for any variable as long as it is included in mapVar and in Template.LinkTree NOT TESTED

     Binning with two different variables DOES NOT YET WORK
  */
  class Template
  {

  public : 

    Template();


    /**\brief Constructor with input files
       \param outFileName Name of the file containing all objects of the Template
       \param configFile Path for the configuration file to load
       \param dataFileNames vector of all root files which will contain data Ntuple (all Ntuple will be merged)
       \param dataTreeNames vector if all TTree names. If not given, a default TTree will be looked for in the TFile.
       \param dataWeight vector of global weights to apply to each data Ntuple
       \param MCFileNames vector of all root files which will contain MC Ntuple (all Ntuple will be merged)
       \param MCTreeNames vector if all TTree names. If not given, a default TTree will be looked for in the TFile.
       \param MCWeight vector of global weights to apply to each MC Ntuple

       - Call Template( const string &outFileName, const string &configFile ) \n
       - If no Ntuple is given, the program exits. \n
       - Accept one missing Ntuple, cases dealt with at template creation.
    */
    Template( const string &outFileName, const string &configFile,  
	      vector<string> dataFileNames, vector<string> dataTreeNames,
	      vector<string> MCFileNames, vector<string> MCTreeNames );

    /**\brief Destructor
     */
    ~Template();

    Setting& GetSetting()  { return m_setting; }
    TMatrixD *GetMatrix( string matrixName );
    TH1 *GetResults( string resultName );
    ChiMatrix* GetChiMatrix( unsigned int iMatrix, unsigned int jMatrix );
    string GetName() const { return m_name; };

    /**\brief Read a boost configuration file
       \param configFile Name of the configuration file
       \return 0 OK
       \return i Error code of Setting.Configure()

       Examples of configuration files given in configFiles directory
    */
    int Configure( const string &configFile );

    /**\brief Compute alpha_ij and sigma_ij
       \return 0 OK
       \return 1 No templates and no MCNtuple to create them

       - Call Template.CreateTemplate() if no tempaltes loaded.
       - Perform the measurement in each configuration and fill the combined result matrix
       - Call InvertMatrix() and fill result histogram.

       If the measurement fails in a configuration, the program will continue and remove it from the combined inversion : setting alpha=0 and errAlpha=100.
    */
    int  ExtractFactors( );

    /**\brief Load Templates from a root file
       \param inFileName Name of the input file
       \param justTemplate switch to load templates or full results.

       \return 0 OK
       \return 1 InputFile does not exist
       \return 2 Setting.Load() failed. Error code of Setting.Load() displayed in error message
       \return 3 ChiMatrix.Load() failed. Error code and coordinates of failure in error message
       \return 4 One of the alpha/sigma matrices/histograms have not been found
       \return 5 Error while inverting matrix. Error code in message.
       \return 6 Did not found tree containig chiMatrix ranges.
       \return 7 Empty bin in m_chiMatrix

       - Change the templates related variables of Setting, see Setting::Load() \n
       - Create an upper triangular matrix of ChiMatrix and calls ChiMatrix.Load().\n
       - Each ChiMatrix wil have the name ChiMatrix_i_j with i,j its coordinates in m_chiMatrix \n
       - If justTemplate, reset all factor matrices an histograms to 0 pointers else load them. \n
       - Call ChiMatrix::ExtractFactors() for each chiMatrix
       - Fill factor matrices with extracted values
    */
    int Load( const string &inFileName, bool justTemplate = false );

    /**\brief Create the matrices of templates

       - Create a ChiMatrix object for all bin in pt and eta
       - Call Template.FillDistrib() for MC
       - Create pseudo-data if needed
       - Call Template.FillDistrib() for data
       - Call ChiMatrix.CreateTemplate for each configuration

    */
    int CreateTemplate();

    /**\brief Save The results in logFile
       \param outFileName Name of the file to write the objects on
       \param justTemplate Wether to save only templates related variables

       \return 0 OK
       \return 1 Templates need to be saved but they do not exist
       \return 2 Setting::Save() failed. Error code in error message
       \return 3 ChiMatrix::Save() failed. Error code and coordinates in error messge

       - Save the full Setting of the objects.\n
       - Calls ChiMatrix.Save(). for each configuration\n

       Do not save informations from bad configurations.
    */
    int Save( bool saveChiMatrix=0 );


    /**\brief Create a pdf note with all the fits (may be heavy in case of high configuration number
       \param path directory path where to save the plots
       \param latexFileName name of the .tex file which whil create a .pdf file

       To call preferably after Template::Save() because changes colors, etc...\n
       - Calls ChiMatrix::MakePlot() : \n
    */
    void MakePlot( string path = "", string latexFileName = "" );

    /**\brief Apply scale factors to MC and data Ntuples
       \param correctionAlpha histogram containing corrections of energy scale factor.
       \param correctionSigma histogram containing constant term correction.

       The variable which bin the detector are automatically taken from the x axis title. 
       This title must me among a predefined list : ETA_TRK, ETA_CALO, ETA_CLUSTER, PHI, PT
    */
    int ApplyCorrection( TH1D* correctionAlpha = 0, TH1D *correctionSigma = 0);


    /**\brief Create distorded pseudo-data from MC Ntuple
       \param outfileName root file name in which the distorded Ntuple will be saved.

       - Generate a random seed if needed by measuring time at nanosecond level.
       - Apply scales given Setting to the MC Ntuple
       - replace data file name with with new one.

       I locally have issue when saving heavy root file. Saving the distorded merging of heavy file have NOT BEEN TESTED.
    */
    void CreateDistordedTree( string outFileName = "");


  private :
    /**\brief Change the electrons pt and Z mass with scales
     */
    void RescaleMapVar( double factor1, double factor2 );

    /**\brief Properly delete 2D vectors of pointers to ChiMatrix
     */
    void ClearChiMatrix();

    /**\brief delete histograms in m_histVec
       \param iVar index of the histogram to delete (-1 remove all histograms)
    */
    void CleanHistVect( int jVar = -1 );

    /**\brief delete matrics in m_histMatrix
       \param iVar index of the matrix to delete (-1 remove all)
    */
    void CleanMatrixVect( int jVar = -1 );


    /**\brief Get color to use for printing in latex file
       \param inputVal theoretical value
       \param experimental value
       \param uncertVal uncertainty on experimental value

       \return string of the latex color to use

       Used only in Template.MakePlot. Will print in the note the experimental value with a color depending on its consistency with expected value.
       - black : <1sigma
       - blue : < 3 sigma
       - red : >3 sigma
    */
    string GetColorTabular( double inputVal, double measVal, double uncertVal );

    /**\brief Generate histogram name
       \param objName name of the object we want to create
       \param iVar Tells if the object is created for alpha (iVar=0) or for C (iVar=1)
    */
    static string CreateHistMatName( string objName, unsigned int iVar ) { return objName + ( iVar ? "_c" : "_alpha" ); }

    /**\brief Find the configuration to put an event into
       \return 0 OK

       Bin numbers of the configuration are put into i_eta and j_eta.
    */
    int FindBin( unsigned int &i_eta, unsigned int &j_eta, bool swapEl=0 );

    /**\brief Fill a ZMass distributions
       \param isData Tell wich role has the input tree

       Calls ChiMatrix::FillDistrib()
     
       When binning with only one variable, the electron with the highest value of the variable will be labeled as first electron.
     
       In case of binning in pt and eta, the event is used twice with a weight of 0.5 whith the selection on 1 electron
    */
    void FillDistrib( bool isData );
  
    /**\brief Class containing all configuration attributes
     */
    Setting m_setting;

    /**\brief Class which perform the template fit
     */
    vector< vector< ChiMatrix* > > m_chiMatrix;

    /**\brief Input Ntuple with Data role
     */
    vector<string> m_dataFileNames;
    vector<string> m_dataTreeNames;

    vector<string> m_MCFileNames;
    vector<string> m_MCTreeNames;

    /**\brief Random generator for creation of distorded tree
     */
    TRandom3 m_rand;

    ChrisLib::MapBranches m_mapBranches;
    string m_name;

    /**\brief 2D vector containing usefull histograms for alpha and c
       Dim 2 :
       0 : TH2D of deviation of alpha_ij compare to expected value in #Sigma
       1 : TH1D for inputvalues
       2 : TH1D for final values of alpha

       Dim 1 :
       0 : alpha
       1 : C 
    */
    multi_array<TH1*, 2> m_vectHist;
    vector<string> m_histNames;

    /**\brief 2D vector containing usefull matrices for alpha and c
       Dim 2 :
       0 : TH2D of alpha_ij
       1 : TH2D of alphaErr_ij

       Dim 1 :
       0 : alpha
       1 : C
    */
    multi_array< TMatrixD*, 2> m_vectMatrix;
    vector<string> m_matrixNames;
    stringstream m_sStream;

    double GetWeight( bool isData );
  };
}
//#########################################

#endif


