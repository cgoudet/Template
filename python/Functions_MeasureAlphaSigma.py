import os
PREFIXPATH="/sps/atlas/c/cgoudet/Calibration/PreRec/"
PREFIXDATASETS="/sps/atlas/c/cgoudet/Calibration/DataxAOD/"

FILESETS={}
FILESETS['MC_13TeV_Zee_50ns_Lkh1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1/'] 
FILESETS['MC_13TeV_Zee_50ns_Lkh1_scaled']=[ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_scaled/']
FILESETS['MC_13TeV_Zee_25ns_Lkh1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1/']
FILESETS['MC_13TeV_bkg_25ns_Lkh1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1/', PREFIXDATASETS + 'MC_13TeV_Ztautau_25ns_Lkh1/', PREFIXDATASETS + 'MC_13TeV_Zttbar_25ns_Lkh1/' ]
FILESETS['MC_13TeV_Zee_25nsb_Lkh1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1/archive/MC_13TeV_Zee_25nsb_Lkh1_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1/archive/MC_13TeV_Zee_25nsb_Lkh1_1.root']
FILESETS['MC_13TeV_Zee_25nsb_Lkh1_scaled']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_scaled/archive/MC_13TeV_Zee_25nsb_Lkh1_scaled_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_scaled/archive/MC_13TeV_Zee_25nsb_Lkh1_scaled_1.root']
FILESETS['MC_13TeV_Zee_25ns_Lkh2']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh2/'] 
FILESETS['MC_13TeV_Zee_25ns_Lkh1_scaled']=[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_scaled' ]
FILESETS['MC_13TeV_Zee_50ns_Lkh1_0']     =[ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0.root' ]
FILESETS['MC_13TeV_Zee_25ns_Lkh1_pt35']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt35/' ]
FILESETS['MC_13TeV_Zee_25ns_Lkh1_pt30']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt30' ]
FILESETS['MC_13TeV_Zee_25ns_Lkh1_pt20']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt20/']
FILESETS['MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0_PairEvents_PassSel.root']
FILESETS['MC_8TeV_Zee_Lkh1']     =[ PREFIXDATASETS + 'MC_8TeV_Zee_1Lepton_Lkh1/']
FILESETS['MC_13TeV_Zee_25ns_Lkh1_fBrem30'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_fBrem30/']
FILESETS['MC_13TeV_Zee_25ns_Lkh1_IDSyst']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_IDSyst']
FILESETS['MC_13TeV_Zee_25ns_Lkh1_recoSyst']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_recoSyst']

FILESETS['ClosureMC'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0_PairEvents_RejSel.root' ]
#    [ 0.2923, 0.2923, 0.2923, 0.32194 ],

FILESETS['Data_13TeV_Zee_50ns_Lkh1']       =[ PREFIXDATASETS + 'Data_13TeV_Zee_50ns_Lkh1']
FILESETS['Data_13TeV_Zee_50ns_Lkh1_scaled']=[ PREFIXDATASETS + 'Data_13TeV_Zee_50ns_Lkh1_scaled']
FILESETS['Data_13TeV_Zee_25ns_Lkh1']       =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1']
FILESETS['Data_13TeV_Zee_25ns_Lkh1_pt30']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_pt30/']
FILESETS['Data_13TeV_Zee_25ns_Lkh1_pt20']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_pt20/']
FILESETS['Data_13TeV_Zee_25ns_Lkh1_fBrem30']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_fBrem30']
FILESETS['Data_13TeV_Zee_25ns_Lkh1_IDSyst']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_IDSyst']
FILESETS['Data_13TeV_Zee_25ns_Lkh1_recoSyst']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_recoSyst']
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

def CreateLauncher( inVector, mode = 4,optionLine=""  ) :

#mode 
    # 0 MeasureScale
    # 2 GenerateToyTemplates
    
    global PREFIXPATH
    global FILESETS

    if len( inVector ) < 4  :
        print 'In vector does not have the right length,  the attributes must be : '
        print 'ConfigFile DataFiles MCFiles outNameFile'
        exit(1)


    configOptions=inVector[3]
    dataFiles=[]
    for dataset in FILESETS[ inVector[1] ] : 
        if '.root' in dataset : dataFiles.append( dataset ); continue
        dataFiles += os.popen( 'ls ' + dataset      + ( '/' if dataset[:-1] != '/' else '' ) + ( 'MC_' if 'MC_' in dataset else 'Data_' ) + '*.root' ).read().split()
    MCFiles=[]
    for dataset in FILESETS[ inVector[2] ] : 
        if '.root' in dataset : MCFiles.append( dataset ); continue
        MCFiles += os.popen( 'ls ' + dataset      + ( '/' if dataset[:-1] != '/' else '' ) + ( 'MC_' if 'MC_' in dataset else 'Data_' ) + '*.root' ).read().split()

    outNameFile=inVector[0]
    doDistorded = 0
    if  len( inVector ) > 4 :
        doDistorded = inVector[4]


    configPath="Config/"
    batchPath="Batch/"
    resultPath="Results/"
    plotPath="Plots/"

    configName = []
    if mode == 1 :
        configName.append( PREFIXPATH + configPath + StripName( outNameFile ) + '_alpha.boost' )
        configName.append( PREFIXPATH + configPath + StripName( outNameFile ) + '_c.boost' )
    elif mode == 3 or mode == 4 :
        configName.append( PREFIXPATH + configPath + StripName( outNameFile ) + '.boost' )
        configName.append( PREFIXPATH + configPath + StripName( outNameFile ) + '_c24.boost' )
    else :
        configName.append( PREFIXPATH + configPath + StripName( outNameFile ) + '.boost' )


    fileName = PREFIXPATH + batchPath + StripName( outNameFile ) + '.sh' 


    with open( fileName, 'w+') as batch:
#Configure the server
        batch.write('server=`pwd`\n' 
                    + 'cd ${server} \n'
                    + 'ulimit -S -s 100000 \n'
                    + 'LD_LIBRARY_PATH=/afs/in2p3.fr/home/c/cgoudet/private/Calibration/RootCoreBin/lib:/afs/in2p3.fr/home/c/cgoudet/private/Calibration/RootCoreBin/bin:$LD_LIBRARY_PATH \n'
                    + 'cd /afs/in2p3.fr/home/c/cgoudet/private/Calibration/RootCoreBin/ \n'
                    + 'source local_setup.sh \n'
                    + 'cd ${server} \n'
                    + 'cp -v /afs/in2p3.fr/home/c/cgoudet/private/Calibration/RootCoreBin/obj/x86_64-slc6-gcc48-opt/Template/bin/MeasureScale . \n'
                    )    
    
#Copy the configuration file to the server
        for confName in configName :
            batch.write( 'cp ' + confName + ' . \n' )
        
#copy the data files to the server and prepare the command line
        dataLine=""
        for iFile in range( 0, len( dataFiles ) ) :
            batch.write( 'cp -v ' + dataFiles[iFile] + ' . \n' )
            dataLine+=" --dataFileName " + StripName( dataFiles[iFile], 1, 0 )  
        
#copy the MC files to the server and prepare command line
        MCLine=""
        for iFile in range( 0, len( MCFiles ) ) :
            batch.write( 'cp -v ' + MCFiles[iFile] + ' . \n' )
            MCLine+=" --MCFileName " + StripName( MCFiles[iFile], 1, 0 ) 

#Fill the command line
#Modes  description
# 0 Normal
# 1 Corrects alpha and c

        if mode==0 :
            CreateConfig( configName[0] ,configOptions )
            batch.write( 'cp -v ' + configName[0] + ' . \n' )
            outNameFile = ' --outFileName ' + StripName( configName[0] ) + '.root '
            if doDistorded==0 :
                batch.write( 'MeasureScale --configFile ' + StripName(configName[0], 1, 0)
                             + dataLine + MCLine + outNameFile + ' --makePlot\n')
            else : 
                batch.write( 'MeasureScale --configFile ' + StripName(configName[0], 1, 0) 
                             + dataLine.replace( '--dataFileName', '--MCFileName' ) + outNameFile + ' --createDistorded MC_distorded.root \n')
                batch.write( 'MeasureScale --configFile ' + StripName(configName[0], 1, 0 )
                             + ' --dataFileName MC_distorded.root ' + MCLine + outNameFile + ' --makePlot \n')
                
#Copy the output pdf and root file to result folder
            batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
            batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`*.root ' + PREFIXPATH + resultPath + '. \n' ) 

        elif mode == 1 :
            configOptionsTemp = configOptions[:]
            configOptionsTemp.append( "doSmearing=0" )
            CreateConfig( configName[0], configOptionsTemp )
            batch.write( 'cp -v ' + configName[0] + ' . \n' )
            outNameFile = ' --outFileName ' + StripName( configName[0] ) + '.root '
            
            batch.write( 'MeasureScale --configFile ' + StripName(configName[0], 1, 0)
                         + dataLine + MCLine + outNameFile + ' --makePlot\n')
            
            configOptionsTemp = configOptions
            configOptionsTemp.append( "doScale=0" )
            CreateConfig( configName[1], configOptionsTemp )
            batch.write( 'cp -v ' + configName[1] + ' . \n' )
            outNameFile = ' --outFileName ' + StripName( configName[1] ) + '.root '
            batch.write( 'MeasureScale --configFile ' + StripName(configName[1], 1, 0)
                         + dataLine + MCLine + outNameFile + ' --correctAlphaFileName ' + StripName( configName[0] ) + '.root --correctAlphaHistName measScale_alpha ' 
                         + ' --makePlot\n')


            batch.write( 'cp -v ' + StripName( configName[0] ) + '.root ' + PREFIXPATH + resultPath + '. \n' ) 
            batch.write( 'cp -v ' + StripName( configName[0] ) + '.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
            batch.write( 'cp -v ' + StripName( configName[1] ) + '.root ' + PREFIXPATH + resultPath + '. \n' ) 
            batch.write( 'cp -v ' + StripName( configName[1] ) + '.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
                
        elif mode == 2:
            CreateConfig( configName[0] ,configOptions )
            batch.write( 'GenerateToyTemplates --configFile ' + StripName(configName[0], 1, 0)
                         + dataLine + MCLine + optionLine + ' --outFileName ' + outNameFile + ' --makePlot \n' )
            batch.write( 'cp *distorded* ' + PREFIXPATH + resultPath + '. \n' )
            batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
            batch.write( 'cp -v *.pdf ' + PREFIXPATH + plotPath + '. \n' )
            batch.write( 'cp -v ' + inVector[0] + ' ' + PREFIXPATH + resultPath + '. \n' )
            # batch.write( 'cp Note*.root ' + PREFIXPATH + plotPath + '. \n' ) 
                # batch.write( 'cp Note*.pdf ' + PREFIXPATH + plotPath + '. \n' ) 

        elif mode == 3 or mode == 4:
            configOptionsTemp = configOptions[:]
            if mode == 4 : configOptionsTemp.append( "doSmearing=0" )
            CreateConfig( configName[0], configOptions )
            batch.write( 'cp -v ' + configName[0] + ' . \n' )
            outNameFile = ' --outFileName ' + StripName( configName[0] ) + '.root '
            batch.write( 'MeasureScale --configFile ' + StripName(configName[0], 1, 0)
                         + dataLine + MCLine + outNameFile + ' --makePlot\n')
            
            configOptionsTemp = configOptions
            configOptionsTemp.append( "doScale=0" )
            configOptionsTemp.append( "etaBins=ETA24" )
            CreateConfig( configName[1], configOptionsTemp )
            batch.write( 'cp -v ' + configName[1] + ' . \n' )
            outNameFile = ' --outFileName ' + StripName( configName[1] ) + '.root '
            batch.write( 'MeasureScale --configFile ' + StripName(configName[1], 1, 0)
                         + dataLine + MCLine + outNameFile + ' --correctAlphaFileName ' + StripName( configName[0] ) + '.root --correctAlphaHistName measScale_alpha ' 
                         + ' --makePlot\n')

            batch.write( 'cp -v ' + StripName( configName[0] ) + '.root ' + PREFIXPATH + resultPath + '. \n' ) 
            batch.write( 'cp -v ' + StripName( configName[0] ) + '.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
            batch.write( 'cp -v ' + StripName( configName[1] ) + '.root ' + PREFIXPATH + resultPath + '. \n' ) 
            batch.write( 'cp -v ' + StripName( configName[1] ) + '.pdf ' + PREFIXPATH + plotPath + '. \n' ) 


    return fileName





def StripName( line, doPrefix = 1, doSuffix = 1 ) :
    if ( line.rfind( '.' ) != -1 and doSuffix ) : 
        line = line[0:line.rfind( '.' )]

    if ( line.rfind( '/' ) != -1 and doPrefix ) :
        line = line[line.rfind( '/' )+1:len( line )]

    return line


def CreateConfig( configName, inOptions = [] ) :

    defaultBinning={}
    defaultBinning['ETA1']='-2.47 2.47'
    defaultBinning['ETA6']='-2.47 -1.55 -1.37 0 1.37 1.55 2.47'
    defaultBinning['SIMSIGMAETA6']='0.007 0.007 0.007 0.007 0.007 0.007'
    defaultBinning['ETA24']='-2.47 -2.3 -2 -1.80 -1.55 -1.37 -1.2 -1 -0.8 -0.6 -0.4 -0.2 0 0.2 0.4 0.6 0.8 1 1.2 1.37 1.55 1.8 2 2.3 2.47'
    defaultBinning['SIMALPHAETA24']=' -2e-2 0 -1.5e-2 1e-2 -2e-2 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -2e-2 1e-2 -1.5e-2 0 -2e-2'
    defaultBinning['SIMSIGMAETA24']='2e-2 2e-2 5e-3 1.5e-2 1.5e-2 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3  8e-3 8e-3 1.5e-2 1.5e-2 5e-3 2e-2 2e-2'
    defaultBinning['ETA68'] = '-2.47 -2.425 -2.4 -2.35 -2.3 -2.2 -2.1 -2.05 -2 -1.9 -1.8 -1.7625 -1.725 -1.6775 -1.63 -1.59 -1.55 -1.51 -1.47 -1.42 -1.37 -1.285 -1.2 -1.1 -1 -0.9 -0.8 -0.7 -0.6 -0.5 -0.4 -0.3 -0.2 -0.1 0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1 1.1 1.2 1.285 1.37 1.42 1.47 1.51 1.55 1.59 1.63 1.6775 1.725 1.7625 1.8 1.9 2 2.05 2.1 2.2 2.3 2.35 2.4 2.435 2.47'

    options = {}
    options['ZMassMin'] = 80
    options['ZMassMax'] = 100
    options['ZMassNBins'] = 20
    options['mode'] = "1VAR"
    options['var1'] = "ETA_CALO"
    options['var2'] = ""
    options['doScale'] = 1
    options['alphaMin']=-0.08
    options['alphaMax']=0.08
    options['alphaNBins']=20
    options['doSmearing']=1
    options['sigmaMin']=0
    options['sigmaMax']=0.1
    options['sigmaNBins']=20
    options['debug']=0
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
    options['nUseEl']=5
    options['nUseEvent']=0
    options['nEventCut']=10
    options['thresholdMass']=70
    options['indepDistorded']=0
    options['indepTemplates']=0
    options['inversionMethod']=11
    options['bootstrap']=0
    options['doPileup']=1
    options['doWeight']=1
    options['etaBins']=defaultBinning['ETA68']
    options['ptBins']=''
    options['applySelection']=0
    options['branchVarNames']={}
    options['branchVarNames']['ETA_CALO_1']='eta_calo_1'
    options['branchVarNames']['ETA_CALO_2']='eta_calo_2' 
    options['branchVarNames']['PHI_1']='phi_1' 
    options['branchVarNames']['PHI_2']='phi_2' 
    options['branchVarNames']['ETA_TRK_1']='eta_1'
    options['branchVarNames']['ETA_TRK_2']='eta_2'
    options['branchVarNames']['PT_1']='pt_1'
    options['branchVarNames']['PT_2']='pt_2'
    options['branchVarNames']['MASS']='m12'
    options['dataBranchWeightName']='weight'
    options['MCBranchWeightName']='weight'


    for inOpt in inOptions :
        optKey = inOpt.split('=')[0]
        optValue= inOpt[inOpt.find('=')+1:]

        if optKey in options.keys() :
            if optKey == 'branchVarNames' :
                optValue.split( ' ' )
                options[optKey][optValue[0]] = optValue[1]
                pass
            else : options[optKey]=optValue

#select a predefined binnin
        if ( optKey=='ptBins' and 'PT' in optValue ) or ( optKey=='etaBins' and 'ETA' in optValue ) :
            options[optKey]=defaultBinning[optValue]
            pass

    with open( configName, 'w' ) as batch:
        for iLabel in options.keys() :
            if iLabel == 'branchVarNames' :
                for var in options[iLabel].keys() :
                    batch.write( iLabel + '=' + var + ' ' + options[iLabel][var] + '\n' )
                    pass
                pass
            else : batch.write( iLabel  + '=' + str( options[iLabel] ) + '\n' )
        
