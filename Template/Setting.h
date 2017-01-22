#ifndef SETTING_H
#define SETTING_H

#include <string>
#include <vector>
#include "TFile.h"
#include <map>


namespace TemplateMethod {
  /**\brief Class to store the settings of the Template method

     The Setting class is filled through a configuration file in the boost format.
     The list of options and their meaning is described below.

     Variable definition :
     - selection=<string> : Define a selection to apply on the inputs.
     - applySelection=<int> (default 0 ) : Define which input must undergo the selection : data (0 or 1) and/or MC (0 or 2 ).

     Options related to categorization :
     - mode={ 1VAR (default), 2VAR } : Chooses the categorization. 
     1VAR adds an event in a configuration (ETA_CALO_1, ETA_CALO_2).
     2VAR adds an event in both configurations ( ETA_CALO_1, PT_1 ) and (ETA_CALO_2, PT_2 ) with half its weight.
     - etaBins= <double> <double> ... : Defines the binning for the variable in ETA_CALO_1 and ETA_CALO_2. 
     Extremal values defines the domain of definition.

     Options related to the template method : 
     - doScale=<int(bool)> ( default 0) : Allows the measurement of scale factor
     - doSmearing=<int(bool)> ( default 0) : Allows the measurement of smearing factor
     - ZMassMin=<double> (default 80) : Low limit for variable of interest value
     - ZMassMax=<double> (default 100) : High limit for variable of interest value
     - ZMassNBins=<int> (default 20) : Number of bins to compute chi2
     - alphaNBins=<int> (default 20) : Number of tested scale values
     - sigmaNBins=<int> (default 20) : Number of tested smearing values

     The framework allows for an easy procedure to perform closures. 
     The options to perform a closure are detailed here :
     - doSimulation=<int(bool)> : Switches the closure mode.
     
     When testing exreme values of scale factors, it is possible to change dramatically the shape of the distribution.
     Optionnal variables are defined to set a range for the tested of scale factors.
     - alphaMin=<double> (default -0.10)
     - alphaMax=<double> (default 0.10)
     - sigmaMin=<double> (default 0)
     - sigmaMin=<double> (default 0.10)

     Other options : 
     - debug=<int(bool)> (default 0)
     - constVarFit={ ALPHA, SIGMA (default) } : Selects the factor which remains constant while the other is scanned.
     - optimizeRange=<int> ( default 5 ) : Defines how the final interval of tested scales values is computed. 
     An optimization code looks for having an interval such as the maximum difference in chi2 is optimizeRanges**2.
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
    void Configure( const std::string &configFile  );
  
  
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
    std::string GetMode()            const { return m_mode;           };
    bool   GetDebug()           const { return m_debug;          };
    bool   GetDoSmearing()      const { return m_doSmearing;     };
    bool   GetDoScale()         const { return m_doScale;        };
    bool   GetDoSimulation()    const { return m_doSimulation;   };
    std::string GetConstVarFit()     const { return m_constVarFit;    };
    std::string    GetSelection()       const { return m_selection;      };
    std::string GetMCName()          const { return m_MCName;         };
    std::string GetDataName()        const { return m_dataName;       };
    bool   GetDoSymBin()        const { return m_symBin;         };
    unsigned int GetFitMethod() const { return m_fitMethod;      };
    unsigned int GetNUseEl()    const { return m_nUseEl;         };
    unsigned int GetNEventCut() const { return m_nEventCut;      };
    double GetThresholdMass() const { return m_thresholdMass; };
    unsigned long GetIndepDistorded() const { return m_indepDistorded; };
    unsigned long GetIndepTemplates() const { return m_indepTemplates; };
    unsigned int GetInversionMethod() const { return m_inversionMethod; }
    unsigned long GetBootstrap() const { return m_bootstrap; }
    unsigned int GetApplySelection() const { return m_applySelection; }
 
    double GetOptimizeRanges()  const { return m_optimizeRanges; };
    std::vector< double > const &GetEtaBins()     const { return m_etaBins;     };
    std::vector< double > const &GetPtBins()      const { return m_ptBins;      };
    std::vector< double > const &GetAlphaSimEta() const { return m_alphaSimEta; };
    std::vector< double > const &GetSigmaSimEta() const { return m_sigmaSimEta; }; 
    std::vector< double > const &GetAlphaSimPt()  const { return m_alphaSimPt;  }; 
    std::vector< double > const &GetSigmaSimPt()  const { return m_sigmaSimPt;  };
    std::vector< std::string > const &GetDataBranchWeightNames() const { return m_dataBranchWeightNames; }
    std::vector< std::string > const &GetMCBranchWeightNames() const { return m_MCBranchWeightNames; }
    std::map< std::string, std::string> const &GetDataBranchVarNames() const { return m_dataBranchVarNames;}
    std::map< std::string, std::string> const &GetMCBranchVarNames() const { return m_MCBranchVarNames;}

    void SetInversionMethod( unsigned int inversionMethod ) { m_inversionMethod = inversionMethod; }
    void SetDebug( bool debug )               { m_debug = debug; };
    void SetDoSmearing( bool smearing )       { m_doSmearing = smearing; };
    void SetDoScale( bool scale )             { m_doScale = scale; };
    void SetSelection( std::string selection )        { m_selection = selection; };
    void SetNEventMC(  long int nEventMC = -1 )     { ( nEventMC != -1 ) ?  m_nEventMC = (unsigned long int ) nEventMC : m_nEventMC++; };
    void SetNEventData( long int nEventData = -1 ) { ( nEventData != -1 ) ? m_nEventData = (unsigned long int ) nEventData : m_nEventData++;};
    void SetMCName( std::string MCName )           { m_MCName = MCName; };
    void SetDataName( std::string DataName )       { m_dataName = DataName; };
    void SetConstVarFit( std::string constVarFit = "SIGMA" );
    void SetSigmaSimEta( const std::vector<double> &sigmaSimEta );
    void SetAlphaSimEta( const std::vector<double> &alphaSimEta );
    void SetNUseEvent( unsigned int nUseEvent ) { m_nUseEvent = nUseEvent; }
    void SetNUseEl( unsigned int nUseEl ) { m_nUseEl = nUseEl; }
    void SetIndepDistorded( unsigned long indepDistorded ) { m_indepDistorded = indepDistorded; }
    void SetIndepTemplates( unsigned long indepTemplates ) { m_indepTemplates = indepTemplates; }
    void SetBootstrap( unsigned long bootstrap ) {m_bootstrap = bootstrap;}

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
    int Load( const std::string &inFileName, bool justTemplate = false ); 

    void Print();

  private : 

    void PrintVector( std::vector<double> vect );
    int Symmetrize( std::vector<double> &outVector );
    int SymmetrizedSim( std::vector<double> &outVector );
    void TestBranches( const std::vector<std::string> &inVect, const std::vector<std::string> constraint, const bool isData );

    /**\brief Define the mode of the run

       We can choose either : \n
       - 1VAR : Electrons are separated in eta bins
       - 2VAR : Electrons are separated in eta and pt bins
    */
    std::string  m_mode;
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
    std::vector< double > m_etaBins;

    /**\brief Vector with pt frontiers
     
       Do not contain extremal pts
    */
    std::vector< double > m_ptBins;

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
    std::vector< double > m_alphaSimEta;

    /**\brief Matrix of simulated sigma in Eta bins
     */
    std::vector< double > m_sigmaSimEta;

    /**\brief Matrix of simulated alpha in Pt bins
     */
    std::vector< double > m_alphaSimPt;

    /**\brief Matrix of simulated bpt in Pt bins
     */
    std::vector< double > m_sigmaSimPt;

    /**\brief Decide which variable remains constant for the first round of fit
     */
    std::string m_constVarFit;



    std::string m_selection;
    unsigned int m_applySelection;//0 both, 1 data only, 2 MC only
    unsigned long int m_nEventMC;
    unsigned long int m_nEventData;
    unsigned int m_nUseEvent;
    /**\brief Switch debug mode
     */
    bool m_debug;

    /**\brief Switch simulation Mode
     */
    bool  m_doSimulation;

    std::string m_MCName;
    std::string m_dataName;

    double m_optimizeRanges;
    bool m_symBin;

    /** Chosse wich fit formula to use
	0 : quadratic fit, uncertainties from the fit parameters
	1 : cubic fit, uncertainties from the fit parameters
	2 : cubic Fit, uncertainty obtained by dichotomy
	3 : qudratic fit only on the right of the minimum
	4 : look for the minimum of the distribution within 2sigma of the fitted minimum

    */
    unsigned int m_fitMethod;
    unsigned int m_nUseEl;
    unsigned int m_nEventCut;
    double m_thresholdMass;
    unsigned long m_indepDistorded;
    unsigned long m_indepTemplates;
    unsigned int m_inversionMethod;
    unsigned long m_bootstrap;

    std::map<std::string,std::string> m_dataBranchVarNames;
    std::map<std::string,std::string> m_MCBranchVarNames;
    std::vector< std::string > m_dataBranchWeightNames;
    std::vector< std::string > m_MCBranchWeightNames;
  };
}

#endif
