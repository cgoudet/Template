#ifndef SETTING_H
#define SETTING_H

//#include "yaml-cpp/yaml.h"
#include <string>
#include <vector>
#include "TFile.h"

using std::vector;
using std::string;

/**\brief Class to store the settings of the progra

   The class is meant to read a Yaml configuration file to setup the properties of the run.
 */
class Setting 
{

 public :

  Setting(); 

  /**\brief Read a configuration file in Yaml format
     \param configFile Input configuration file in Yaml format
     
     \return 0 OK
     \return 1 Bad stream from config file
     \return exception Bad check 

     - The attributes of the class are set according to the configuration file.
     - The mapping is made with the label of the attribute : adding a property in the config file, or changing orders of properties, will not perturb the reading.
     - Perform checks on read values : binFitRange, mode, vector sizes for simulation, 
*/
  int Configure( const string &configFile  );
  
  
  double GetAlphaMin()        const { return m_alphaMin;       };
  double GetAlphaMax()        const { return m_alphaMax;       };
  int    GetAlphaNBins()      const { return m_alphaNBins;     };
  unsigned long int GetNEventMC()        const { return m_nEventMC;       };
  unsigned long int GetNEventData()      const { return m_nEventData;     };
  int    GetNUseEvent()       const { return m_nUseEvent;      };
  double GetSigmaMin()        const { return m_sigmaMin;       };
  double GetSigmaMax()        const { return m_sigmaMax;       };
  int    GetSigmaNBins()      const { return m_sigmaNBins;     };
  double GetZMassMin()        const { return m_ZMassMin;       };
  double GetZMassMax()        const { return m_ZMassMax;       };
  int    GetZMassNBins()      const { return m_ZMassNBins;     };
  string GetMode()            const { return m_mode;           };
  bool   GetDebug()           const { return m_debug;          };
  bool   GetDoSmearing()      const { return m_doSmearing;     };
  bool   GetDoScale()         const { return m_doScale;        };
  bool   GetDoSimulation()    const { return m_doSimulation;   };
  string GetConstVarFit()     const { return m_constVarFit;    };
  int    GetSelection()       const { return m_selection;      };
  string GetMCName()          const { return m_MCName;         };
  string GetDataName()        const { return m_dataName;       };
  bool   GetDoSymBin()        const { return m_symBin;         };
  unsigned int GetFitMethod() const { return m_fitMethod;      };
  unsigned int GetNUseEl()    const { return m_nUseEl;         };
  unsigned int GetNEventCut() const { return m_nEventCut;      };
  string GetVar1() const { return m_var1; };
  string GetVar2() const { return m_var2; };
  double GetThresholdMass() const { return m_thresholdMass; };
  bool GetIndepDistorded() const { return m_indepDistorded; };
  bool GetIndepTemplates() const { return m_indepTemplates; };
  unsigned int GetInversionMethod() const { return m_inversionMethod; }
  bool GetBootstrap() const { return m_bootstrap; }
  bool GetDoPileup() const { return m_doPileup;}
  bool GetDoWeight() const { return m_doWeight; }

  double GetOptimizeRanges()  const { return m_optimizeRanges; };
  vector< double > const &GetEtaBins()     const { return m_etaBins;     };
  vector< double > const &GetPtBins()      const { return m_ptBins;      };
  vector< double > const &GetAlphaSimEta() const { return m_alphaSimEta; };
  vector< double > const &GetSigmaSimEta() const { return m_sigmaSimEta; }; 
  vector< double > const &GetAlphaSimPt()  const { return m_alphaSimPt;  }; 
  vector< double > const &GetSigmaSimPt()  const { return m_sigmaSimPt;  };

  void SetInversionMethod( unsigned int inversionMethod ) { m_inversionMethod = inversionMethod; }
  void SetDebug( bool debug )               { m_debug = debug; };
  void SetDoSmearing( bool smearing )       { m_doSmearing = smearing; };
  void SetDoScale( bool scale )             { m_doScale = scale; };
  void SetSelection( int selection )        { m_selection = selection; };
  void SetNEventMC(  long int nEventMC = -1 )     { ( nEventMC != -1 ) ?  m_nEventMC = (unsigned long int ) nEventMC : m_nEventMC++; };
  void SetNEventData( long int nEventData = -1 ) { ( nEventData != -1 ) ? m_nEventData = (unsigned long int ) nEventData : m_nEventData++;};
  void SetMCName( string MCName )           { m_MCName = MCName; };
  void SetDataName( string DataName )       { m_dataName = DataName; };
  void SetConstVarFit( string constVarFit = "SIGMA" );
  void SetSigmaSimEta( vector<double> sigmaSimEta ) { if ( sigmaSimEta.size() == m_sigmaSimEta.size() ) m_sigmaSimEta = sigmaSimEta; }
  void SetAlphaSimEta( vector<double> alphaSimEta ) { if ( alphaSimEta.size() == m_alphaSimEta.size() ) m_alphaSimEta = alphaSimEta; }
  void SetNUseEvent( unsigned int nUseEvent ) { m_nUseEvent = nUseEvent; }
  void SetNUseEl( unsigned int nUseEl ) { m_nUseEl = nUseEl; }
  void SetIndepDistorded( bool indepDistorded ) { m_indepDistorded = indepDistorded; }
  void SetIndepTemplates( bool indepTemplates ) { m_indepTemplates = indepTemplates; }
  void SetDoWeight( bool doWeight ) { m_doWeight = doWeight; };

  /**\brief Save the content into a file
     \param outFile output TFile

     \return 0 OK
     \return 1 TFile is a 0 pointer
     \return 2 TFile is not opened

     - Store all parameters into a TTree named InfoTree and write this tree
  */
  int Save( TFile *outFile ) ;

  /**\brief Load previously saved configuration file
     \param inFileName Name of the input root file
     \param justTemplate Load only templates related variables

     \return 0 OK
     \return 1 TFile can not be opened
     \return 2 InfoTree do not exist in inFileName
     \return 3 Detector binning and simulation binning do not match

     - Variables not loaded for template only : doScale, doSmearing, doSimulation, binFitRange, alphaSimEta, alphaSimPt, sigmaSimEta, sigmaSimPt, constVarFit
     - Perform a check on detector binning and simulation binning if justTemplate
  */
  int Load( const string &inFileName, bool justTemplate = false ); 

  void Print();

 private : 

  void PrintVector( vector<double> vect );
  int Symmetrize( vector<double> &outVector );
  int SymmetrizedSim( vector<double> &outVector );

  /**\brief Define the mode of the run

     We can choose either : \n
     - 1VAR : Electrons are separated in eta bins
     - 2VAR : Electrons are separated in eta and pt bins
   */
  string  m_mode;
  string m_var1;
  string m_var2;
  /**\brief Z mass lower bound
   */
  double m_ZMassMin;

  /**\brief Z mass upper bound
   */
  double m_ZMassMax;

  /**\brief Z mass number of bins
   */
  unsigned int m_ZMassNBins;

  /**\brief Vector with eta frontiers
     
     Do not contain extremal etas
  */
  vector< double > m_etaBins;

  /**\brief Vector with pt frontiers
     
     Do not contain extremal pts
  */
  vector< double > m_ptBins;

  /**\brief Setup the computation of scale factors
   */
  bool m_doScale;

  /**\brief Alpha lower limit
   */
  double  m_alphaMin;

  /**\brief Alpha upper limit
   */
  double m_alphaMax;

  /**\brief Alpha bin number

     m_alphaNBins represents the number of values of alpha different of 0. 
     The total bin number will be m_alphaNBins+1.
  */
  int m_alphaNBins;

  /**\brief Setup the computation of constant term
   */
  bool m_doSmearing;

  /**\brief Sigma lower limit
   */
  double m_sigmaMin;

  /**\brief Sigma upper limit
   */
  double m_sigmaMax;

  /**\brief Sigma bin number

     m_sigmaNBins represents the number of values of sigma different of 0. 
     The total bin number will be m_sigmaNBins+1.
   */
  int m_sigmaNBins;

  
  /**\brief Matrix of simulated alpha in Eta bins
   */
  vector< double > m_alphaSimEta;

  /**\brief Matrix of simulated sigma in Eta bins
   */
  vector< double > m_sigmaSimEta;

/**\brief Matrix of simulated alpha in Pt bins
   */
  vector< double > m_alphaSimPt;

  /**\brief Matrix of simulated bpt in Pt bins
   */
  vector< double > m_sigmaSimPt;

  /**\brief Decide which variable remains constant for the first round of fit
   */
  string m_constVarFit;



  int m_selection;

  unsigned long int m_nEventMC;
  unsigned long int m_nEventData;
  unsigned int m_nUseEvent;
  /**\brief Switch debug mode
   */
  bool m_debug;

  /**\brief Switch simulation Mode
   */
  bool  m_doSimulation;

  string m_MCName;
  string m_dataName;

  double m_optimizeRanges;
  bool m_symBin;

  unsigned int m_fitMethod;
  unsigned int m_nUseEl;
  unsigned int m_nEventCut;
  double m_thresholdMass;
  bool m_indepDistorded;
  bool m_indepTemplates;
  unsigned int m_inversionMethod;
  bool m_bootstrap;
  bool m_doPileup;
  bool m_doWeight;
};


#endif
