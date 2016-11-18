/**

\mainpage


# Templates

**_In the different mentionned files, be careful to change the paths_**  

**An example is given at each step for 2015 data. It will be wrapped within a block quote as follows:**

> Here is the example.  


___


Templates is a package designed in the ROOT Analysis framework allowing to:
- measure the in-situ scale factors
- build the systematics model for the scale factors
- generate toys

The different measurements are performed as jobs running on the Centre de Calcul de Lyon (CCIN2P3) via a command called "sub1.sh" (personal bash script containing the line commands). It can be easily changed or run in interactive (scale factors measurement takes about 2h).


Download and setup
------------------

The Templates package depends on the PlotFunctions one, meaning that you have to download both packages in the same directory from git@github.com:aguerguichon/. A RootCore will have to be setup in this directory.

```
mkdir Calibration
git clone git@github.com:aguerguichon/Template.git
git clone git@github.com:aguerguichon/PlotFunctions.git
cd Template
rcSetup -r //to check the latest version of RootCore available  
rcSetup Base,2.4.X  
rc find_packages  
rc compile  
```


Measuring scale factors
-----------------------

Scale factors are measured from a Ntuple. To generate a smaller Ntuple from DxAOD, see the eGammaScaleFactors package.

- In python/Functions_MeasureAlphaSigma.py, the FILESETS map collects the keys corresponding to the Ntuple files you want to use to perform your measurement.

>     FILESETS['Data15_13TeV_Zee_Lkh1'] = [ PREFIXDATASETS + 'Data15_13TeV_Zee_Lkh1/']  
>     FILESETS['MC15c_13TeV_Zee_Lkh1'] = [ PREFIXDATASETS + 'MC15c_13TeV_Zee_Lkh1/'] 

- In python/MeasureAlphaSigma.py, each "line" (i.e. entry of the configFiles list) corresponds to one job
