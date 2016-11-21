/**

\mainpage


# Templates

**_In the different mentionned files, be careful to change the paths._**  

**An example is given at each step for 2015 data. It will be wrapped within a block quote as follows:**

> Here is the example.  


___


Templates is a package designed in the ROOT Analysis framework allowing to:
- measure the in-situ scale factors
- build the systematics model for the scale factors
- generate toys

The different measurements are performed as jobs running on the Centre de Calcul de Lyon (CCIN2P3) via a command called "sub1.sh" (personal bash script containing the line commands). It can be easily changed or run in interactive mode (scale factors measurement takes about 2h).


Download and setup
------------------

The Template package depends on the PlotFunctions one, meaning that you have to download both packages in the same directory from git@github.com:aguerguichon. A RootCore will have to be setup in this directory.

```
git clone git@github.com:aguerguichon/Template.git
git clone git@github.com:aguerguichon/PlotFunctions.git
rcSetup -r //to check the latest version of RootCore available  
rcSetup Base,2.4.X  
rc find_packages  
rc compile  
```

Make sure that in Template/cmt/Makefile.RootCore the PlotFunctions dependency is added in PACKAGE_DEP.  

Measuring scale factors
-----------------------

Scale factors are measured from a Ntuple. To generate a smaller Ntuple from DxAOD, see the eGammaScaleFactors package.  

The MeasureScale.cxx macro allows to perform the measurement. The Functions_MeasureAlphaSigma.py script sets the configuration needed and the job is submitted to the CCIN2P3 through the MeasureAlphaSigma.py script.  

To run the program, call:
```
MeasureScale --configFile yourConfFile --dataFileName yourDataFile1 --dataFileName yourDataFile2 --MCFileName yourMCFile1 --outFileName yourOutputFile <other options>
```  
Different options are supported by MeasureScale and are displayed/described in MeasureScale.cxx.

The configuration file is a boost file containing all the options needed for the measurement (number of bins, Z mass fit range...). The list of the options with their default values can be found in Functions_MeasureAlphaSigma in CreateConfig.  

The Template framework allows to automatically generate those configuration files depending on the type of measurement you need to perform (nominal, different systematics, geometries, number of bins...).  

###Configuring your measurement  

- In python/Functions_MeasureAlphaSigma.py, the FILESETS map collects the keys corresponding to the Ntuple files you want to use to perform your measurement.

>     FILESETS['Data15_13TeV_Zee_Lkh1'] = [ PREFIXDATASETS + 'Data15_13TeV_Zee_Lkh1/']  
>     FILESETS['MC15c_13TeV_Zee_Lkh1'] = [ PREFIXDATASETS + 'MC15c_13TeV_Zee_Lkh1/'] 

- In python/MeasureAlphaSigma.py, each "line" (i.e. entry of the configFiles list) corresponds to one job.

```
['outputFileName', 'dataKey', 'MCKey', [optionsList], mode]
```

>     ['DataOff_13TeV_15.root', 'Data15_13TeV_Zee_Lkh1', 'MC15c_13TeV_Zee_Lkh1',[]]
>     ['DataOff_13TeV_Window.root', 'Data1615_13TeV_Zee_Lkh1', 'MC15c_13TeV_Zee_Lkh1', ['ZMassMin=82.5', 'ZMassMax=97.5'] ]   
> The 1st line corresponds to the nominal measurement, the second line to the measurement reducing the Z mass fit range for the window systematic.  

More information on the different modes can be found in Functions_MeasureAlphaSigma in CreateLauncher def. The default mode is 3, which is the one to be used for the scale factors measurement.    


###Submitting the job

For that you just need to run:
```
python MeasureAlphaSigma.py
```

