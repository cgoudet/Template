PREFIXPATH="/sps/atlas/c/cgoudet/Calibration/PreRec/"
PREFIXDATASETS="/sps/atlas/c/cgoudet/Calibration/DataxAOD/"

MCFILESETS={}
MCFILESETS['MC_13TeV_Zee_50ns_Lkh1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1/MC_13TeV_Zee_50ns_Lkh1_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1/MC_13TeV_Zee_50ns_Lkh1_1.root' ]
MCFILESETS['MC_13TeV_Zee_50ns_Lkh1_scaled']=[ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_scaled/MC_13TeV_Zee_50ns_Lkh1_scaled_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_scaled/MC_13TeV_Zee_50ns_Lkh1_scaled_0.root']
MCFILESETS['MC_13TeV_Zee_25ns_Lkh1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1/MC_13TeV_Zee_25ns_Lkh1_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1/MC_13TeV_Zee_25ns_Lkh1_1.root' ]
MCFILESETS['MC_13TeV_Zee_25ns_Lkh2']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh2/MC_13TeV_Zee_25ns_Lkh2_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh2/MC_13TeV_Zee_25ns_Lkh2_1.root' ]
MCFILESETS['MC_13TeV_Zee_25ns_Lkh1_scaled']=[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_scaled/MC_13TeV_Zee_25ns_Lkh1_scaled_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_scaled/MC_13TeV_Zee_25ns_Lkh1_scaled_0.root']
MCFILESETS['MC_13TeV_Zee_50ns_Lkh1_0']     =[ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0.root' ]
MCFILESETS['MC_13TeV_Zee_25ns_Lkh1_pt35']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt35/MC_13TeV_Zee_25ns_Lkh1_pt35_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt35/MC_13TeV_Zee_25ns_Lkh1_pt35_1.root' ]
MCFILESETS['MC_13TeV_Zee_25ns_Lkh1_pt30']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt30/MC_13TeV_Zee_25ns_Lkh1_pt30_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt30/MC_13TeV_Zee_25ns_Lkh1_pt30_1.root' ]
MCFILESETS['MC_13TeV_Zee_25ns_Lkh1_pt20']  =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt20/MC_13TeV_Zee_25ns_Lkh1_pt20_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1_pt20/MC_13TeV_Zee_25ns_Lkh1_pt20_1.root' ]
MCFILESETS['MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0_PairEvents_PassSel.root']
MCFILESETS['MC_8TeV_Zee_Lkh1']     =[ PREFIXDATASETS + 'MC_8TeV_Zee_1Lepton_Lkh1/MC_8TeV_Zee_1Lepton_Lkh1_0.root', PREFIXDATASETS + 'MC_8TeV_Zee_DiLepton_Lkh1/MC_8TeV_Zee_DiLepton_Lkh1_0.root', PREFIXDATASETS + 'MC_8TeV_Zee_DiLepton_Lkh1/MC_8TeV_Zee_DiLepton_Lkh1_1.root', PREFIXDATASETS + 'MC_8TeV_Zee_DiLepton_Lkh1/MC_8TeV_Zee_DiLepton_Lkh1_2.root' ]

MCFILESETS['ClosureMC'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0_PairEvents_RejSel.root' ]
MCWEIGHTSET={}
MCWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1']       =[ 1, 1]
MCWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1_scaled']=[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_25ns_Lkh1']       =[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_25ns_Lkh2']       =[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_25ns_Lkh1_scaled']=[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1_0']     =[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_25ns_Lkh1_pt35']  =[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_25ns_Lkh1_pt30']  =[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_25ns_Lkh1_pt20']  =[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel']  =[ 1, 1] 
MCWEIGHTSET['MC_8TeV_Zee_Lkh1']     =[ 0.32194, 0.2923, 0.2923, 0.2923 ]
MCWEIGHTSET['ClosureMC'] = [1]

#    [ 0.2923, 0.2923, 0.2923, 0.32194 ],
DATAFILESETS={}
DATAFILESETS['Data_13TeV_Zee_50ns_Lkh1']       =[ PREFIXDATASETS + 'Data_13TeV_Zee_50ns_Lkh1/Data_13TeV_Zee_50ns_Lkh1_0.root']
DATAFILESETS['Data_13TeV_Zee_50ns_Lkh1_scaled']=[ PREFIXDATASETS + 'Data_13TeV_Zee_50ns_Lkh1_scaled/Data_13TeV_Zee_50ns_Lkh1_scaled_0.root']
DATAFILESETS['Data_13TeV_Zee_25ns_Lkh1']       =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1/Data_13TeV_Zee_25ns_Lkh1_0.root']
DATAFILESETS['Data_13TeV_Zee_25ns_Lkh1_pt30']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_pt30/Data_13TeV_Zee_25ns_Lkh1_pt30_0.root']
DATAFILESETS['Data_13TeV_Zee_25ns_Lkh1_pt20']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_pt20/Data_13TeV_Zee_25ns_Lkh1_pt20_0.root']
DATAFILESETS['Data_13TeV_Zee_25ns_Lkh1_pt35']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_pt35/Data_13TeV_Zee_25ns_Lkh1_pt35_0.root']
DATAFILESETS['Data_13TeV_Zee_25ns_Lkh1_scaled']=[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_scaled/Data_13TeV_Zee_25ns_Lkh1_scaled_0.root']
DATAFILESETS['MC_13TeV_Zee_50ns_Lkh1_1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_1.root' ]
DATAFILESETS['Data_13TeV_Zee_25ns_Lkh2']       =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh2/Data_13TeV_Zee_25ns_Lkh2_0.root']
DATAFILESETS['MC_13TeV_Zee_50ns_Lkh1_PairEvents_RejSel'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0_PairEvents_RejSel.root']
DATAFILESETS['MC_distordedRejPair']       =[ PREFIXDATASETS + '../Test/MC_distordedRejPair.root' ]
DATAFILESETS['ClosureData'] = ['/sps/atlas/c/cgoudet/Calibration/Closure/MC24_PassSel_distorded.root' ]
DATAFILESETS['Data_8TeV_Zee_Lkh1'] = [ PREFIXDATASETS + 'Data_8TeV_Zee_Lkh1/Data_8TeV_Zee_Lkh1_0.root', PREFIXDATASETS + 'Data_8TeV_Zee_Lkh1/Data_8TeV_Zee_Lkh1_1.root' ]
DATAFILESETS['Data_8TeV_Zee_Lkh1_scaled'] = [ PREFIXDATASETS + 'Data_8TeV_Zee_Lkh1_scaled/Data_8TeV_Zee_Lkh1_scaled_0.root', PREFIXDATASETS + 'Data_8TeV_Zee_Lkh1_scaled/Data_8TeV_Zee_Lkh1_scaled_0.root' ]
DATAFILESETS['MC_13TeV_Zee_25ns_Lkh1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1/MC_13TeV_Zee_25ns_Lkh1_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_25ns_Lkh1/MC_13TeV_Zee_25ns_Lkh1_1.root' ]
DATAFILESETS['MC_13TeV_Zee_25ns_geo02_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo02_Lkh1/MC_13TeV_Zee_25ns_geo02_Lkh1_0.root' ]
DATAFILESETS['MC_13TeV_Zee_25ns_geo11_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo11_Lkh1/MC_13TeV_Zee_25ns_geo11_Lkh1_0.root' ]
DATAFILESETS['MC_13TeV_Zee_25ns_geo12_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo12_Lkh1/MC_13TeV_Zee_25ns_geo12_Lkh1_0.root' ]
DATAFILESETS['MC_13TeV_Zee_25ns_geo13_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo13_Lkh1/MC_13TeV_Zee_25ns_geo13_Lkh1_0.root' ]
DATAFILESETS['MC_13TeV_Zee_25ns_geo14_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo14_Lkh1/MC_13TeV_Zee_25ns_geo14_Lkh1_0.root' ]
DATAFILESETS['MC_13TeV_Zee_25ns_geo15_Lkh1'] =[ PREFIXDATASETS + 'MC_13TeV_Zee_25ns_geo15_Lkh1/MC_13TeV_Zee_25ns_geo15_Lkh1_0.root' ]

DATAWEIGHTSET={}
DATAWEIGHTSET['Data_13TeV_Zee_50ns_Lkh1']       =[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_50ns_Lkh1_scaled']=[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_25ns_Lkh1']       =[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_25ns_Lkh1_scaled']=[ 1 ]
DATAWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1_1']       =[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_25ns_Lkh1_pt30']  =[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_25ns_Lkh1_pt20']  =[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_25ns_Lkh1_pt35']  =[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_25ns_Lkh2']       =[ 1 ]
DATAWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1_PairEvents_RejSel'] = [ 1 ]
DATAWEIGHTSET['MC_distordedRejPair'] = [ 1 ]
DATAWEIGHTSET['ClosureData'] = [1]
DATAWEIGHTSET['Data_8TeV_Zee_Lkh1'] = [ 1, 1 ]
DATAWEIGHTSET['Data_8TeV_Zee_Lkh1_scaled'] = [ 1, 1 ]
DATAWEIGHTSET['MC_13TeV_Zee_25ns_Lkh1'] = [ 1, 1 ]
DATAWEIGHTSET['MC_13TeV_Zee_25ns_geo02_Lkh1'] = [ 1 ]
DATAWEIGHTSET['MC_13TeV_Zee_25ns_geo11_Lkh1'] = [ 1 ]
DATAWEIGHTSET['MC_13TeV_Zee_25ns_geo12_Lkh1'] = [ 1 ]
DATAWEIGHTSET['MC_13TeV_Zee_25ns_geo13_Lkh1'] = [ 1 ]
DATAWEIGHTSET['MC_13TeV_Zee_25ns_geo14_Lkh1'] = [ 1 ]
DATAWEIGHTSET['MC_13TeV_Zee_25ns_geo15_Lkh1'] = [ 1 ]


def CreateLauncher( inVector, mode = 0,optionLine=""  ) :

#mode 
    # 0 MeasureScale
    # 1 GenerateToyTemplates
    
    global PREFIXPATH
    global MCFILESETS
    global DATAFILESETS

    if len( inVector ) < 4  :
        print 'In vector does not have the right length,  the attributes must be : '
        print 'ConfigFile DataFiles MCFiles outNameFile'
        exit(1)


    configOptions=inVector[3]
    dataFiles=DATAFILESETS[ inVector[1] ]
    dataWeights=DATAWEIGHTSET[ inVector[1] ]  
    MCFiles=MCFILESETS[ inVector[2] ]
    MCWeights=MCWEIGHTSET[ inVector[2] ]
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
#                batch.write( 'cp *.tex ' + PREFIXPATH + resultPath + '. \n' )
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
            batch.write( 'GenerateToyTemplates --configFile ' + StripName(configName, 1, 0)
                         + dataLine + MCLine + optionLine + outNameFile + ' \n' )
            batch.write( 'cp *distorded* ' + PREFIXPATH + resultPath + '. \n' )
            batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
            batch.write( 'cp -v *.pdf ' + PREFIXPATH + plotPath + '. \n' )
            batch.write( 'cp -v ' + inVector[0] + ' ' + PREFIXPATH + resultPath + '. \n' )
            batch.write( 'ls -lh \n ' ) 
            # batch.write( 'cp Note*.root ' + PREFIXPATH + plotPath + '. \n' ) 
                # batch.write( 'cp Note*.pdf ' + PREFIXPATH + plotPath + '. \n' ) 

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
    options['nUseEl']=1
    options['nUseEvent']=0
    options['nEventCut']=10
    options['thresholdMass']=70
    options['indepDistorded']=0
    options['indepTemplates']=0
    options['inversionMethod']=11
    options['bootstrap']=0
    options['doPileup']=1
    options['doWeight']=1
    options['etaBins']=defaultBinning['ETA24']
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
        
