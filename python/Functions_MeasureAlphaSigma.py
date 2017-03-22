import os
import sys


isAntinea=0
isSaskia=1

user='a/aguergui/public' if isAntinea else 'c/cgoudet/private'
libPath= '/afs/in2p3.fr/home/' +user +'/Calibration/PlotFunctions/python'
sys.path.append(os.path.abspath(libPath))
from SideFunction import *

#PREFIXPATH='/sps/atlas/a/aguerguichon/Calibration/Bias/Toys/' if isAntinea else "/sps/atlas/c/cgoudet/Calibration/PreRec/"
PREFIXPATH='/sps/atlas/a/aguerguichon/Calibration/PreRec/' if isAntinea else "/sps/atlas/c/cgoudet/Calibration/PreRec/"
PREFIXDATASETS="/sps/atlas/a/aguerguichon/Calibration/DataxAOD/"

FILESETS={}


#======================= eos ===========================//
FILESETS['MC15c_eos']       =[ PREFIXDATASETS + 'eosNtuples/mc_Zee.root'] 
FILESETS['Data15_eos']       =[ PREFIXDATASETS + 'eosNtuples/data15_Zee.root'] 
FILESETS['Data16_eos']       =[ PREFIXDATASETS + 'eosNtuples/data16_Zee.root'] 
FILESETS['CorrectedData_eos']       =[ '/sps/atlas/a/aguerguichon/Calibration/PreRec/Results/CorrectedData/data15_Zee_corrected.root', PREFIXDATASETS + 'eosNtuples/data16_Zee.root'] 
FILESETS['CorrectedData_eos_Window']       =[ '/sps/atlas/a/aguerguichon/Calibration/PreRec/Results/CorrectedData/data15_Zee_corrected_Window.root', PREFIXDATASETS + 'eosNtuples/data16_Zee.root'] 
FILESETS['pseudoData'] = ['/sps/atlas/a/aguerguichon/Calibration/Closure/pseudoData_both_distorted.root']
FILESETS['pseudoData_Saskia'] = ['/sps/atlas/s/sfalke/CalibrationWork/PourAntinea/nTuple_data.root']
FILESETS['MC_Saskia'] = ['/sps/atlas/s/sfalke/CalibrationWork/PourAntinea/nTuple_MC.root']

#==============
FILESETS['CorrectedData']       =[ '/sps/atlas/a/aguerguichon/Calibration/PreRec/Results/CorrectedData/Data15_13TeV_Zee_noGain_Lkh1_corrected.root', PREFIXDATASETS + 'Data16_13TeV_Zee_noGain_Lkh1/']
FILESETS['CorrectedDataThreshold']       =[ '/sps/atlas/a/aguerguichon/Calibration/PreRec/Results/CorrectedData/Data15_13TeV_Zee_noGain_Lkh1_Threshold_corrected.root', PREFIXDATASETS + 'Data16_13TeV_Zee_noGain_Lkh1/']
FILESETS['CorrectedDataWindow']       =[ '/sps/atlas/a/aguerguichon/Calibration/PreRec/Results/CorrectedData/Data15_13TeV_Zee_noGain_Lkh1_Window_corrected.root', PREFIXDATASETS + 'Data16_13TeV_Zee_noGain_Lkh1/']
FILESETS['CorrectedDataID']       =[ '/sps/atlas/a/aguerguichon/Calibration/PreRec/Results/CorrectedData/Data15_13TeV_Zee_noGain_Lkh2_corrected.root', PREFIXDATASETS + 'Data16_13TeV_Zee_noGain_Lkh2/']
FILESETS['CorrectedDataIso']       =[ '/sps/atlas/a/aguerguichon/Calibration/PreRec/Results/CorrectedData/Data15_13TeV_Zee_noGain_Lkh1_doIso0_corrected.root', PREFIXDATASETS + 'Data16_13TeV_Zee_noGain_Lkh1_doIso0/']
FILESETS['CorrectedDatafBrem']       =[ '/sps/atlas/a/aguerguichon/Calibration/PreRec/Results/CorrectedData/Data15_13TeV_Zee_noGain_Lkh1_fBrem70_corrected.root', PREFIXDATASETS + 'Data16_13TeV_Zee_noGain_Lkh1_fBrem70/']

#======================== 2015 ========================//

FILESETS['MC15c_13TeV_Zee_2015_noGain_Lkh1']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2015_noGain_Lkh1/']#nominal
FILESETS['Data15_13TeV_Zee_noGain_Lkh1'] = [ PREFIXDATASETS + 'Data15_13TeV_Zee_noGain_Lkh1/']#nominal


FILESETS['MC15c_13TeV_Zee_2015_noGain_Lkh2']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2015_noGain_Lkh2/'] 
FILESETS['MC15c_13TeV_Zee_2015_noGain_Lkh1_IDSyst']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2015_noGain_Lkh1_IDSyst/'] 
FILESETS['MC15c_13TeV_Zee_2015_noGain_Lkh1_recoSyst']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2015_noGain_Lkh1_recoSyst/'] 
FILESETS['MC15c_13TeV_Zee_2015_noGain_Lkh1_isoSyst']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2015_noGain_Lkh1_isoSyst/']
FILESETS['MC15c_13TeV_Zee_2015_noGain_Lkh1_noIso']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2015_noGain_Lkh1_doIso0/']  
FILESETS['MC15c_13TeV_Zee_2015_noGain_Lkh1_fBrem70']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2015_noGain_Lkh1_fBrem70/']  


FILESETS['Data15_13TeV_Zee_noGain_Lkh1_noIso'] = [ PREFIXDATASETS + 'Data15_13TeV_Zee_noGain_Lkh1_doIso0/'] 
FILESETS['Data15_13TeV_Zee_noGain_Lkh1_fBrem70'] = [ PREFIXDATASETS + 'Data15_13TeV_Zee_noGain_Lkh1_fBrem70/'] 
FILESETS['Data15_13TeV_Zee_noGain_Lkh2'] = [ PREFIXDATASETS + 'Data15_13TeV_Zee_noGain_Lkh2/'] 


#======================== 2016 ===========================//

FILESETS['MC15c_13TeV_Zee_2016_noGain_Lkh1']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2016_noGain_Lkh1/']#nominal
FILESETS['Data16_13TeV_Zee_noGain_Lkh1'] = [ PREFIXDATASETS + 'Data16_13TeV_Zee_noGain_Lkh1/']#nominal

FILESETS['MC15c_13TeV_Zee_2016_noGain_Lkh2']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2016_noGain_Lkh2/'] 
FILESETS['MC15c_13TeV_Zee_2016_noGain_Lkh1_IDSyst']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2016_noGain_Lkh1_IDSyst/'] 
FILESETS['MC15c_13TeV_Zee_2016_noGain_Lkh1_recoSyst']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2016_noGain_Lkh1_recoSyst/'] 
FILESETS['MC15c_13TeV_Zee_2016_noGain_Lkh1_isoSyst']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2016_noGain_Lkh1_isoSyst/']
FILESETS['MC15c_13TeV_Zee_2016_noGain_Lkh1_noIso']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2016_noGain_Lkh1_doIso0/']  
FILESETS['MC15c_13TeV_Zee_2016_noGain_Lkh1_fBrem70']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_2016_noGain_Lkh1_fBrem70/']  

FILESETS['Data16_13TeV_Zee_noGain_Lkh1_noIso'] = [ PREFIXDATASETS + 'Data16_13TeV_Zee_noGain_Lkh1_doIso0/'] 
FILESETS['Data16_13TeV_Zee_noGain_Lkh1_fBrem70'] = [ PREFIXDATASETS + 'Data16_13TeV_Zee_noGain_Lkh1_fBrem70/'] 
FILESETS['Data16_13TeV_Zee_noGain_Lkh2'] = [ PREFIXDATASETS + 'Data16_13TeV_Zee_noGain_Lkh2/'] 


#====================== 2015 + 2016 ======================//

FILESETS['MC15c_13TeV_Zee_noGain_Lkh1']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_noGain_Lkh1/'] #nominal

FILESETS['MC15c_13TeV_Zee_noGain_Lkh2']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_noGain_Lkh2/'] 
FILESETS['MC15c_13TeV_Zee_noGain_Lkh1_IDSyst']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_noGain_Lkh1_IDSyst/'] 
FILESETS['MC15c_13TeV_Zee_noGain_Lkh1_recoSyst']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_noGain_Lkh1_recoSyst/'] 
FILESETS['MC15c_13TeV_Zee_noGain_Lkh1_isoSyst']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_noGain_Lkh1_isoSyst/']
FILESETS['MC15c_13TeV_Zee_noGain_Lkh1_noIso']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_noGain_Lkh1_doIso0/']  
FILESETS['MC15c_13TeV_Zee_noGain_Lkh1_fBrem70']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_noGain_Lkh1_fBrem70/']  

#====================== Test ===============================//

FILESETS['MC_13TeV_Zee_NewGeom_Lkh1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_NewGeom_Lkh1/']
FILESETS['Data_13TeV_Zee_25ns_Lkh1']       =[ PREFIXDATASETS + 'BackUp/Data_13TeV_Zee_25ns_Lkh1']
FILESETS['MC_13TeV_Zee_25ns_Lkh1']       =[ PREFIXDATASETS + 'BackUp/MC_13TeV_Zee_25ns_Lkh1/']

FILESETS['MC_Kirill']       =["/sps/atlas/g/grevtsov/Calibration/CalibrationStudies/FILES/inputs/customSF/v1_unShiftedWeights_noSmear_noScale/mc15c_wCal_v1.root" ]
FILESETS['Data_Kirill']       =["/sps/atlas/g/grevtsov/Calibration/CalibrationStudies/FILES/inputs/customSF/v1_unShiftedWeights_noSmear_noScale/data_16_wCal_v1.root" ]


#==================== Toys =====================
FILESETS['MC15c_evenEvents']       =['/sps/atlas/a/aguerguichon/Calibration/Test/MC15c_13TeV_Zee_noGain_Lkh1_evenEvents.root']
FILESETS['MC15c_oddEvents']       =['/sps/atlas/a/aguerguichon/Calibration/Test/MC15c_13TeV_Zee_noGain_Lkh1_oddEvents.root']

#================================================================
#FILESETS['MC_13TeV_bkg_25ns_Lkh1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1/', PREFIXDATASETS + 'MC_13TeV_Ztautau_25ns_Lkh1/', PREFIXDATASETS + 'MC_13TeV_Zttbar_25ns_Lkh1/' ]
FILESETS['MC_13TeV_Zee_25nsb_Lkh1']       =[ PREFIXDATASETS + 'Archive/MC_13TeV_Zee_25ns_rel201_0.root', PREFIXDATASETS + 'Archive/MC_13TeV_Zee_25ns_rel201_1.root']
FILESETS['MC_13TeV_Zee_25nsb_IBL_Lkh1']       =[ PREFIXDATASETS + 'Archive/MC_13TeV_Zee_25ns_rel201_IBL_0.root', PREFIXDATASETS + 'Archive/MC_13TeV_Zee_25ns_rel201_IBL_1.root']
FILESETS['MC_13TeV_Zee_25nsb_Lkh1_scaled']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_scaled/archive/MC_13TeV_Zee_25nsb_Lkh1_scaled_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_scaled/archive/MC_13TeV_Zee_25nsb_Lkh1_scaled_1.root']

FILESETS['ClosureMC'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0_PairEvents_RejSel.root' ]
FILESETS['ClosureData'] = [ '/sps/atlas/c/cgoudet/Calibration/Closure/MC_distorded.root' ]
#    [ 0.2923, 0.2923, 0.2923, 0.32194 ],

FILESETS['MC_13TeV_Zee_50ns_Lkh1_PairEvents_RejSel'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0_PairEvents_RejSel.root']
FILESETS['Data_8TeV_Zee_Lkh1'] = [ PREFIXDATASETS + 'Data_8TeV_Zee_Lkh1/' ]
FILESETS['Data_8TeV_Zee_Lkh1_scaled'] = [ PREFIXDATASETS + 'Data_8TeV_Zee_Lkh1_scaled' ]
FILESETS['MC_13TeV_Zee_25ns_geo02_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo02_Lkh1' ]
FILESETS['MC_13TeV_Zee_25ns_geo11_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo11_Lkh1' ]
FILESETS['MC_13TeV_Zee_25ns_geo12_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo12_Lkh1' ]
FILESETS['MC_13TeV_Zee_25ns_geo13_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo13_Lkh1' ]
FILESETS['MC_13TeV_Zee_25ns_geo14_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo14_Lkh1' ]
FILESETS['MC_13TeV_Zee_25ns_geo15_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo15_Lkh1' ]

FILESETS['MC_2015cPRE_corr']=['/sps/atlas/c/cgoudet/Calibration/ScaleResults/160519/MC_13TeV_Zee_25ns_Lkh1_0_corrected.root', '/sps/atlas/c/cgoudet/Calibration/ScaleResults/160519/MC_13TeV_Zee_25ns_Lkh1_1_corrected.root','/sps/atlas/c/cgoudet/Calibration/ScaleResults/160519/MC_13TeV_Zee_25ns_Lkh1_2_corrected.root']
def FillDatasetContainer( container, datasets ) :
    for dataset in datasets : 
        if '.root' in dataset : container.append( dataset )
        else : container += listFiles( AddSlash(dataset) + ( 'MC' if 'MC' in dataset else 'Data' ) + '*.root' )
    

def CreateLauncher( inVector, mode = 3,optionLine=[] ) :
    """
    mode  : 
    0 MeasureScale
    1 2Steps
    2 GenerateToyTemplates
    3 MeasureScale + sigmaOnly with correction -> default
    4 MeasureScale + alphaOnly with correction -> compare mode 3 to 0
    ? 5 AlphaOnly with lowaer ZMassMin+ MeasureScale corrected + sigmaOnly corrected ??
    to perform a closure: doDistorded=1 and any mode different from 2
    """
    print( "Mode: "+str(mode))

    global PREFIXPATH
    global FILESETS

    if len( inVector ) < 4  : print( 'In vector does not have the right length,  the attributes must be : \nConfigFile DataFiles MCFiles outNameFile'); exit(1)


    configOptions=inVector[3]
    dataFiles = []
    if inVector[1] in FILESETS : FillDatasetContainer( dataFiles, FILESETS[ inVector[1] ] )
    else : dataFiles+=inVector[1].split(',')

    MCFiles=[]
    if inVector[2] in FILESETS : FillDatasetContainer( MCFiles, FILESETS[ inVector[2] ] )
    else : MCFiles+=inVector[2].split(',')

    outNameFile=inVector[0]
    doDistorded = 0
    if  len( inVector ) > 5 :
        doDistorded = inVector[5]


    configPath="Config/"
    batchPath="Batch/"
    resultPath="Results/"
    plotPath="Plots/"

    configName = []
    if mode in [1, 4] : configName.append( PREFIXPATH + configPath + StripString( outNameFile ) + '_alpha.boost' )
    if mode in [0, 2, 3, 4] : configName.append( PREFIXPATH + configPath + StripString( outNameFile ) + '.boost' )
    if mode in [ 1, 3 ] : configName.append( PREFIXPATH + configPath + StripString( outNameFile ) + '_c.boost' )

    fileName = PREFIXPATH + batchPath + StripString( outNameFile ) + '.sh' 

    batch = open( fileName, 'w+')
#Configure the server

    batch.write('server=`pwd`\n' 
    
                + 'cd ${server} \n'
                + 'ulimit -S -s 100000 \n'
                + 'LD_LIBRARY_PATH=/afs/in2p3.fr/home/'+user+'/Calibration/RootCoreBin/lib:/afs/in2p3.fr/home/'+user+'/Calibration/RootCoreBin/bin:$LD_LIBRARY_PATH \n'
                + 'cd /afs/in2p3.fr/home/'+user+'/Calibration/RootCoreBin/ \n'
                + 'source local_setup.sh \n'
                + 'cd ${server} \n'
                + 'cp -v /afs/in2p3.fr/home/'+user+'/Calibration/RootCoreBin/obj/x86_64-slc6-gcc49-opt/Template/bin/MeasureScale . \n'
                )    


#Copy the configuration file to the server
    batch.write( '\n'.join( [ 'cp ' + confName + ' .' for confName in configName  ] ) + '\n' )
#copy the data files to the server and prepare the command line

    batch.write( '\n'.join( [ 'cp -v ' + dataFile + ' . ' for dataFile in dataFiles + MCFiles ] ) + '\n' )
    

    dataLine = ' '.join( [ (' --dataFileName ' 
                            + StripString( name, 1, 0 ) 
                            + ' --dataTreeName correctedData' )  if 'corrected' in name else (' --dataFileName ' + StripString( name, 1, 0 ) +(' --dataTreeName pseudoData_both_distorted' if isSaskia else '') ) for name in dataFiles ] ) 

    MCLine = ' '.join( [ ' --MCFileName ' + StripString( name, 1, 0 ) +(' --MCTreeName CollectionTree' if isSaskia else '') for name in MCFiles ] )

    # dataLine = ' '.join( [ (' --dataFileName ' 
    #                         + StripString( name, 1, 0 ) 
    #                         + ' --dataTreeName correctedData' )  if 'corrected' in name else (' --dataFileName ' + StripString( name, 1, 0 ) +(' --dataTreeName CollectionTree' if isSaskia else '') ) for name in dataFiles ] ) 

    # MCLine = ' '.join( [ ' --MCFileName ' + StripString( name, 1, 0 ) +(' --MCTreeName CollectionTree' if isSaskia else '') for name in MCFiles ] )




  #Fill the command line

#Perform a closure
    if doDistorded and mode != 2 : 
        batch.write( 'MeasureScale --configFile ' + StripString(configName[0], 1, 0) + dataLine.replace( '--dataFileName', '--MCFileName' ) + ' --outFileName ' + outNameFile + ' --createDistorded MC_distorded.root --noExtraction \n')
        dataLine = ' --dataFileName MC_distorded.root '


#Copy the output pdf and root file to result folder
        
    for name in configName :
        tmpOptions = configOptions[:]
        if '_alpha' in name : tmpOptions.append( 'doSmearing=0' )
        elif '_c' in name : tmpOptions+= [ 'doScale=0', 'etaBins=ETA24' ]
        CreateConfig( name, tmpOptions )


    for iFit in range( 0, len( configName ) ) :
        outNameFile = ' --outFileName ' + StripString( configName[iFit] )+ '.root '
        corrLine=''
        if iFit : corrLine = ' --correctAlphaHistName measScale_alpha --correctAlphaFileName ' + StripString(configName[iFit-1]) + '.root' 

        #if mode == 2 : batch.write( 'GenerateToyTemplates --configFile ' + StripString(configName[iFit], 1, 0)  + dataLine + MCLine + optionLine +  outNameFile + ' --makePlot \n' )
        if mode == 2 : 
            outNameFile = ' --outFileName ' + StripString( configName[iFit] ) +str(iFit)+ '.root '
            batch.write( '\n'.join( ['GenerateToyTemplates --configFile ' + StripString(configName[iFit], 1, 0)  + dataLine + MCLine + optionLine[i] +  ' --outFileName ' + StripString( configName[iFit] ) +str(i)+ '.root --makePlot ' for i in range(0, len (optionLine)) ]) +' \n') 


        else  :  batch.write( 'MeasureScale --configFile ' + StripString(configName[iFit], 1, 0 )  + dataLine + MCLine + outNameFile + corrLine + optionLine +' --makePlot \n')

   # if mode==2 : batch.write( 'cp -v *bootstrap* ' + PREFIXPATH + plotPath + '. \n rm *distorded* \n' )
    batch.write( 'rm -v ' + ' '.join( [ StripString(dataset, 1, 0) for dataset in dataFiles+MCFiles ] ) + '\n' )
    #batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`*.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
    #batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`*.root ' + PREFIXPATH + resultPath + '. \n' ) 
    for iFit in range( 0, len( configName ) ) :
        batch.write( 'cp -v '+ StripString( configName[iFit] ) +'*.root ' + PREFIXPATH + resultPath + '. \n')
        batch.write( 'cp -v '+StripString( configName[iFit] ) +'*.pdf ' + PREFIXPATH + plotPath + '. \n')
    batch.close()
    return fileName


#==================================
def CreateConfig( configName, inOptions = [] ) :

    defaultBinning={}
    defaultBinning['ETA1']='-2.47 2.47'
    defaultBinning['ETA6']='-2.47 -1.55 -1.37 0 1.37 1.55 2.47'
    defaultBinning['SIMSIGMAETA6']='0.007 0.007 0.007 0.007 0.007 0.007'
    defaultBinning['ETA24']='-2.47 -2.3 -2 -1.80 -1.55 -1.37 -1.2 -1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1 1.2 1.37 1.55 1.8 2 2.3 2.47'
    defaultBinning['SIMSIGMAETA24']='2e-2 2e-2 5e-3 1.5e-2 1.5e-2 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3  8e-3 8e-3 1.5e-2 1.5e-2 5e-3 2e-2 2e-2'
    defaultBinning['SIMALPHAETA24']=' -2e-2 0 -1.5e-2 1e-2 -2e-2 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -2e-2 1e-2 -1.5e-2 0 -2e-2'
    defaultBinning['ETA68'] = '-2.47 -2.435 -2.4 -2.35 -2.3 -2.2 -2.1 -2.05 -2 -1.9 -1.8 -1.7625 -1.725 -1.6775 -1.63 -1.59 -1.55 -1.51 -1.47 -1.42 -1.37 -1.285 -1.2 -1.1 -1 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.285 1.37 1.42 1.47 1.51 1.55 1.59 1.63 1.6775 1.725 1.7625 1.8 1.9 2 2.05 2.1 2.2 2.3 2.35 2.4 2.435 2.47'
    defaultBinning['SIMALPHAETA68'] = '1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 -1.5e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2 1e-2'

    defaultBinning['PT6'] = '0 100 200 300 400 500 1000'
    options = {}
    options['ZMassMin'] = 80
    options['ZMassMax'] = 100
    options['ZMassNBins'] = 20
    options['mode'] = "1VAR"
    options['doScale'] = 1
    options['alphaMin']=-0.1
    options['alphaMax']=0.1
    options['alphaNBins']=20
    options['doSmearing']=1
    options['sigmaMin']=0
    options['sigmaMax']=0.15
    options['sigmaNBins']=20
    options['debug']=1
    options['constVarFit']="SIGMA"
    options['selection']=''
    options['doSimulation']=0
    options['optimizeRanges']=5
    options['alphaSimEta']=''
    options['alphaSimPt']=''
    options['sigmaSimEta']=''
    options['sigmaSimPt']=''
    options['symBin']=0
    options['fitMethod']=2
    options['nUseEl']=1
    options['nUseEvent']=0
    options['nEventCut']=10
    options['thresholdMass']=70
    options['indepDistorded']=0
    options['indepTemplates']=0
    options['inversionMethod']=11
    options['bootstrap']=0
    options['etaBins']=defaultBinning['ETA68']
    options['ptBins']=''
    options['applySelection']=0
    options['dataBranchVarNames']={}
    options['MCBranchVarNames']={}

    if isSaskia:
        options['dataBranchVarNames']['ETA_CALO_1']='el1_etaCalo'
        options['dataBranchVarNames']['ETA_CALO_2']='el2_etaCalo' 
        options['dataBranchVarNames']['MASS']='m12'
        options['dataBranchWeightName']=''

        options['MCBranchVarNames']['ETA_CALO_1']='el1_etaCalo'
        options['MCBranchVarNames']['ETA_CALO_2']='el2_etaCalo' 
        options['MCBranchVarNames']['MASS']='m12'
        options['MCBranchWeightName']='weight_1516'


    else:
         options['dataBranchVarNames']['ETA_CALO_1']='eta_calo_1'
         options['dataBranchVarNames']['ETA_CALO_2']='eta_calo_2' 
         options['dataBranchVarNames']['MASS']='m12'
         options['dataBranchWeightName']=''

         options['MCBranchVarNames']['ETA_CALO_1']='eta_calo_1'
         options['MCBranchVarNames']['ETA_CALO_2']='eta_calo_2' 
         options['MCBranchVarNames']['MASS']='m12'
         options['MCBranchWeightName']='weight'
   


    for inOpt in inOptions :
        optKey = inOpt.split('=')[0]
        optValue= inOpt[inOpt.find('=')+1:]

        if optKey in options :
            if 'BranchVarNames' in optKey :
                optValue = optValue.split( ' ' )
                options[optKey][optValue[0]] = optValue[1]
                pass
            else : options[optKey]=optValue

#select a predefined binnin
        if ( optKey in ['ptBins', 'etaBins', 'sigmaSimEta', 'alphaSimEta' ] ) and (  'PT' in optValue or 'ETA' in optValue ) : options[optKey]=defaultBinning[optValue]

    with open( configName, 'w' ) as batch:
        for iLabel in options :
            if 'BranchVarNames' in iLabel : batch.write( '\n'.join( [ iLabel + '=' + var + ' ' + options[iLabel][var]  for var in options[iLabel] ] ) + '\n' )
            else : batch.write( iLabel  + '=' + str( options[iLabel] ) + '\n' )
        
    return


def LaunchBatchTemplate( configFile, path = '' ) :
    """
    Take an input with the right format and launch the template measuremetn with the corresponding options to the batch
    Format is a list 
    - 0 : Name of the job (and output file)
    - 1 : Directory of data
    - 2 : MC directory
    - 3 : harcoded options for the template method
    - 4 : modes for template measurement
    """
    path = AddSlash(path)
    mode = configFile[4]  if len( configFile ) > 4 else 3
    
    launcherFile=CreateLauncher( configFile, mode, "" )
    logFile = StripString( configFile[0] )
    
    launchLine='~/sub1.sh ' + logFile + ' ' \
	    + path + logFile + '.log ' \
	    + path + logFile + '.err ' \
	    + launcherFile
    
    os.system( launchLine )
