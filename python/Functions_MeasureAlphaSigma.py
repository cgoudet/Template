import os
import sys

isAntinea=0
user='a/aguergui/public' if isAntinea else 'c/cgoudet/private'
libPath= '/afs/in2p3.fr/home/' +user +'/Calibration/PlotFunctions/python'
sys.path.append(os.path.abspath(libPath))
from SideFunction import *

#PREFIXPATH='/sps/atlas/a/aguerguichon/Calibration/Bias/Toys/' if isAntinea else "/sps/atlas/c/cgoudet/Calibration/PreRec/"
PREFIXPATH='/sps/atlas/a/aguerguichon/Calibration/PreRec/' if isAntinea else "/sps/atlas/c/cgoudet/Calibration/PreRec/"
PREFIXDATASETS="/sps/atlas/a/aguerguichon/Calibration/DataxAOD/"

FILESETS={}

FILESETS['MC15c_13TeV_Zee_Lkh1']       =[ PREFIXDATASETS + 'MC15c_13TeV_Zee_Lkh1/'] 
FILESETS['Data16_13TeV_Zee_Lkh1']       =[ PREFIXDATASETS + 'Data16_13TeV_Zee_Lkh1/'] 

FILESETS['Data1615_13TeV_Zee_Lkh1'] = [ PREFIXDATASETS + 'Data16_13TeV_Zee_Lkh1/', PREFIXDATASETS + 'Data15_13TeV_Zee_Lkh1/'] 

FILESETS['Data16_13TeV_Zee_Lkh1']       =[ PREFIXDATASETS + 'Data16_13TeV_Zee_Lkh1/'] 


#=======================Test

FILESETS['Data_13TeV_Zee_25ns_Lkh1']       =[ PREFIXDATASETS + 'BackUp/Data_13TeV_Zee_25ns_Lkh1']
FILESETS['MC_13TeV_Zee_25ns_Lkh1']       =[ PREFIXDATASETS + 'BackUp/MC_13TeV_Zee_25ns_Lkh1/']

#================================================================
FILESETS['MC_13TeV_Zee_50ns_Lkh1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1/'] 
FILESETS['MC_13TeV_Zee_50ns_Lkh1_scaled']=[ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_scaled/']
#FILESETS['MC_13TeV_bkg_25ns_Lkh1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1/', PREFIXDATASETS + 'MC_13TeV_Ztautau_25ns_Lkh1/', PREFIXDATASETS + 'MC_13TeV_Zttbar_25ns_Lkh1/' ]
FILESETS['MC_13TeV_Zee_25nsb_Lkh1']       =[ PREFIXDATASETS + 'Archive/MC_13TeV_Zee_25ns_rel201_0.root', PREFIXDATASETS + 'Archive/MC_13TeV_Zee_25ns_rel201_1.root']
FILESETS['MC_13TeV_Zee_25nsb_IBL_Lkh1']       =[ PREFIXDATASETS + 'Archive/MC_13TeV_Zee_25ns_rel201_IBL_0.root', PREFIXDATASETS + 'Archive/MC_13TeV_Zee_25ns_rel201_IBL_1.root']
FILESETS['MC_13TeV_Zee_25nsb_Lkh1_scaled']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_scaled/archive/MC_13TeV_Zee_25nsb_Lkh1_scaled_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_scaled/archive/MC_13TeV_Zee_25nsb_Lkh1_scaled_1.root']
FILESETS['MC_13TeV_Zee_25ns_Lkh2']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh2/'] 
FILESETS['MC_13TeV_Zee_25ns_Lkh1_scaled']=[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_scaled' ]
FILESETS['MC_13TeV_Zee_50ns_Lkh1_0']     =[ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0.root' ]
FILESETS['MC_13TeV_Zee_25ns_Lkh1_pt35']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt35/' ]
FILESETS['MC_13TeV_Zee_25ns_Lkh1_pt30']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt30' ]
FILESETS['MC_13TeV_Zee_25ns_Lkh1_pt20']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt20/']
FILESETS['MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0_PairEvents_PassSel.root']
FILESETS['MC_8TeV_Zee_Lkh1']     =[ PREFIXDATASETS + 'MC_8TeV_Zee_1Lepton_Lkh1/']
FILESETS['MC_13TeV_Zee_25ns_Lkh1_fBrem70'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_fBrem70/']
FILESETS['MC_13TeV_Zee_25ns_Lkh1_IDSyst']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_IDSyst/']
FILESETS['MC_13TeV_Zee_25ns_Lkh1_recoSyst']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_recoSyst']
FILESETS['MC_13TeV_Zee_25ns_Lkh1_isoSyst']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_isoSyst']

FILESETS['MC_13TeV_Zee_25ns_Lkh1_noIso']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_doIso0']
FILESETS['Data_13TeV_Zee_25ns_Lkh1_noIso']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_doIso0']

FILESETS['ClosureMC'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0_PairEvents_RejSel.root' ]
FILESETS['ClosureData'] = [ '/sps/atlas/c/cgoudet/Calibration/Closure/MC_distorded.root' ]
#    [ 0.2923, 0.2923, 0.2923, 0.32194 ],

FILESETS['Data_13TeV_Zee_50ns_Lkh1']       =[ PREFIXDATASETS + 'Data_13TeV_Zee_50ns_Lkh1']
FILESETS['Data_13TeV_Zee_50ns_Lkh1_scaled']=[ PREFIXDATASETS + 'Data_13TeV_Zee_50ns_Lkh1_scaled']
FILESETS['Data_13TeV_Zee_25nsb_Lkh1']       =[ '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/Archive/Data_13TeV_Zee_25ns_rel201_0.root']

FILESETS['Data_13TeV_Zee_25ns_Lkh1_pt30']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_pt30/']
FILESETS['Data_13TeV_Zee_25ns_Lkh1_pt20']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_pt20/']
FILESETS['Data_13TeV_Zee_25ns_Lkh1_fBrem70']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_fBrem70']
FILESETS['Data_13TeV_Zee_25ns_Lkh1_pt35']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_pt35/']
FILESETS['Data_13TeV_Zee_25ns_Lkh1_scaled']=[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_scaled']
FILESETS['Data_13TeV_Zee_25ns_Lkh2']       =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh2/']
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


FILESETS['photonsAllSyst_h013']=['/sps/atlas/c/cgoudet/Hgam/Inputs/MxAOD_h013_Full/ntuple/*.root']

def FillDatasetContainer( container, datasets ) :
    for dataset in datasets : 
        if '.root' in dataset : container.append( dataset )
        else : container += listFiles( addSlash(dataset) + ( 'MC' if 'MC' in dataset else 'Data' ) + '*.root' )
    

def CreateLauncher( inVector, mode = 3,optionLine=[] ) :

    print "Mode: "+str(mode)
#mode 
    # 0 MeasureScale
    # 1 2Steps
    # 2 GenerateToyTemplates
    # 3 MeasureScale + sigmaOnly with correction -> default
    # 4 MeasureScale + alphaOnly with correction -> compare mode 3 to 0
    #? 5 AlphaOnly with lowaer ZMassMin+ MeasureScale corrected + sigmaOnly corrected ??
    # to perform a closure: doDistorded=1 and any mode different from 2

    global PREFIXPATH
    global FILESETS

    if len( inVector ) < 4  : print 'In vector does not have the right length,  the attributes must be : \nConfigFile DataFiles MCFiles outNameFile'; exit(1)


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
    
    dataLine = ' '.join( [ ' --dataFileName ' + StripString( name, 1, 0 ) for name in dataFiles ] ) 
    MCLine = ' '.join( [ ' --MCFileName ' + StripString( name, 1, 0 ) for name in MCFiles ] )

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
        outNameFile = ' --outFileName ' + StripString( configName[iFit] ) + '.root '
        corrLine=''
        if iFit : corrLine = ' --correctAlphaHistName measScale_alpha --correctAlphaFileName ' + StripString(configName[iFit-1]) + '.root' 

#        if mode == 2 : batch.write( 'GenerateToyTemplates --configFile ' + StripString(configName[iFit], 1, 0)  + dataLine + MCLine + optionLine +  outNameFile + ' --makePlot \n' )
        if mode == 2 : batch.write( '\n'.join( ['GenerateToyTemplates --configFile ' + StripString(configName[iFit], 1, 0)  + dataLine + MCLine + optionLine[i] +  outNameFile for i in range(0, len (optionLine)) ]) +'\n') 


        else  :  batch.write( 'MeasureScale --configFile ' + StripString(configName[iFit], 1, 0 )  + dataLine + MCLine + outNameFile + corrLine + optionLine + ' \n')

    if mode==2 : batch.write( 'cp -v *bootstrap* ' + PREFIXPATH + plotPath + '. \n' )
    batch.write( 'rm *distorded* \n' )
    batch.write( '`ls *.tex | awk -F "." \'{print $1 }\'` \n' )
    batch.write( 'rm -v ' + ' '.join( [ StripString(dataset, 1, 0) for dataset in dataFiles+MCFiles ] ) + '\n' )
    batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
    batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`*.root ' + PREFIXPATH + resultPath + '. \n' ) 
    batch.close()
    return fileName


#==================================
def CreateConfig( configName, inOptions = [] ) :

    defaultBinning={}
    defaultBinning['ETA1']='-2.47 2.47'
    defaultBinning['ETA6']='-2.47 -1.55 -1.37 0 1.37 1.55 2.47'
    defaultBinning['SIMSIGMAETA6']='0.007 0.007 0.007 0.007 0.007 0.007'
    defaultBinning['ETA24']='-2.47 -2.3 -2 -1.80 -1.55 -1.37 -1.2 -1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1 1.2 1.37 1.55 1.8 2 2.3 2.47'
    defaultBinning['SIMALPHAETA24']=' -2e-2 0 -1.5e-2 1e-2 -2e-2 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -2e-2 1e-2 -1.5e-2 0 -2e-2'
    defaultBinning['SIMSIGMAETA24']='2e-2 2e-2 5e-3 1.5e-2 1.5e-2 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3  8e-3 8e-3 1.5e-2 1.5e-2 5e-3 2e-2 2e-2'
    defaultBinning['ETA68'] = '-2.47 -2.435 -2.4 -2.35 -2.3 -2.2 -2.1 -2.05 -2 -1.9 -1.8 -1.7625 -1.725 -1.6775 -1.63 -1.59 -1.55 -1.51 -1.47 -1.42 -1.37 -1.285 -1.2 -1.1 -1 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.285 1.37 1.42 1.47 1.51 1.55 1.59 1.63 1.6775 1.725 1.7625 1.8 1.9 2 2.05 2.1 2.2 2.3 2.35 2.4 2.435 2.47'
    defaultBinning['PT6'] = '0 100 200 300 400 500 1000'
    options = {}
    options['ZMassMin'] = 80
    options['ZMassMax'] = 100
    options['ZMassNBins'] = 20
    options['mode'] = "1VAR"
#    options['var1'] = "ETA_CALO"
#    options['var2'] = ""
    options['doScale'] = 1
    options['alphaMin']=-0.10
    options['alphaMax']=0.10
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
    options['thresholdMass']=0
    options['indepDistorded']=0
    options['indepTemplates']=0
    options['inversionMethod']=11
    options['bootstrap']=0
#    options['doWeight']=1
    options['etaBins']=defaultBinning['ETA68']
    options['ptBins']=''
    options['applySelection']=0
    options['dataBranchVarNames']={}
    options['dataBranchVarNames']['ETA_CALO_1']='eta_calo_1'
    options['dataBranchVarNames']['ETA_CALO_2']='eta_calo_2' 
    # options['branchVarNames']['PT_1']='pt_1'
    # options['branchVarNames']['PT_2']='pt_2'
    options['dataBranchVarNames']['MASS']='m12'
    options['dataBranchVarNames']['WEIGHT']='weight'
    options['dataBranchWeightName']='weight'
    options['MCBranchWeightName']='weight'

    options['MCBranchVarNames']={}
    options['MCBranchVarNames']['ETA_CALO_1']='eta_calo_1'
    options['MCBranchVarNames']['ETA_CALO_2']='eta_calo_2' 
    # options['branchVarNames']['PT_1']='pt_1'
    # options['branchVarNames']['PT_2']='pt_2'
    options['MCBranchVarNames']['MASS']='m12'
    options['MCBranchVarNames']['WEIGHT']='weight'


    for inOpt in inOptions :
        optKey = inOpt.split('=')[0]
        optValue= inOpt[inOpt.find('=')+1:]

        if optKey in options :
            if optKey in ['dataBranchVarNames', 'MCBranchVarNames' ]  :
                optValue = optValue.split( ' ' )
                options[optKey][optValue[0]] = optValue[1]
                pass
            else : options[optKey]=optValue

#select a predefined binnin
        if ( optKey in ['ptBins', 'etaBins', 'sigmaSimEta' ] ) and (  'PT' in optValue or 'ETA' in optValue ) : options[optKey]=defaultBinning[optValue]

    with open( configName, 'w' ) as batch:
        for iLabel in options :
            if 'BranchVarNames' in iLabel : batch.write( '\n'.join( [ iLabel + '=' + var + ' ' + options[iLabel][var]  for var in options[iLabel] ] ) + '\n' )
            else : batch.write( iLabel  + '=' + str( options[iLabel] ) + '\n' )
        
    return

#==================================
def LaunchNPScale( inputs ) :
    NPFile = open( '/sps/atlas/c/cgoudet/Hgam/FrameWork/PhotonSystematic/data/NPNames.txt' )
    commonOptions = [ 'thresholdMass=0', 'ZMassMin=105', 'ZMassMax=160', 'ZMassNBins=55', 
                      'doSemaring=1', 'doScale=1', 'fitMethod=2', 'etaBins=105 160' ]

    mandatoryVariables = [ 'ETA_CALO_1', 'ETA_CALO_2', 'MASS' ]
    
    for NP in NPFile :
        NP = NP.replace( '\n', '').replace('containerName=','').replace( 'HGamEventInfo_', '' )
        if NP=='' : continue
        isUp = '1up' in NP
        options = commonOptions
        nomOptions = [ ( 'data' if isUp else 'MC') + 'BranchVarNames=' + var + ' ' + NP + '_m_yy' for var in mandatoryVariables ]
        fluctOptions = [ ('data'if not isUp else 'MC') + 'BranchVarNames=' +var + ' m_yy' for var in mandatoryVariables ]
        options+=nomOptions+fluctOptions
        inputs.append( [ NP+'.root', 'photonsAllSyst_h013', 'photonsAllSyst_h013', options, 0 ] )
        return
