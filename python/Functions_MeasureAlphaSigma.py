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
MCFILESETS['MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0_PairEvents_PassSel.root']
MCWEIGHTSET={}
MCWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1']       =[ 1, 1]
MCWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1_scaled']=[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_25ns_Lkh1']       =[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_25ns_Lkh2']       =[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_25ns_Lkh1_scaled']=[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1_0']     =[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_25ns_Lkh1_pt35']  =[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_25ns_Lkh1_pt30']  =[ 1, 1] 
MCWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel']  =[ 1, 1] 


#    [ 0.2923, 0.2923, 0.2923, 0.32194 ],
DATAFILESETS={}
DATAFILESETS['Data_13TeV_Zee_50ns_Lkh1']       =[ PREFIXDATASETS + 'Data_13TeV_Zee_50ns_Lkh1/Data_13TeV_Zee_50ns_Lkh1_0.root']
DATAFILESETS['Data_13TeV_Zee_50ns_Lkh1_scaled']=[ PREFIXDATASETS + 'Data_13TeV_Zee_50ns_Lkh1_scaled/Data_13TeV_Zee_50ns_Lkh1_scaled_0.root']
DATAFILESETS['Data_13TeV_Zee_25ns_Lkh1']       =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1/Data_13TeV_Zee_25ns_Lkh1_0.root']
DATAFILESETS['Data_13TeV_Zee_25ns_Lkh1_pt30']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_pt30/Data_13TeV_Zee_25ns_Lkh1_pt30_0.root']
DATAFILESETS['Data_13TeV_Zee_25ns_Lkh1_pt35']  =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_pt35/Data_13TeV_Zee_25ns_Lkh1_pt35_0.root']
DATAFILESETS['Data_13TeV_Zee_25ns_Lkh1_scaled']=[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh1_scaled/Data_13TeV_Zee_25ns_Lkh1_scaled_0.root']
DATAFILESETS['MC_13TeV_Zee_50ns_Lkh1_1']       =[ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_1.root' ]
DATAFILESETS['Data_13TeV_Zee_25ns_Lkh2']       =[ PREFIXDATASETS + 'Data_13TeV_Zee_25ns_Lkh2/Data_13TeV_Zee_25ns_Lkh2_0.root']
DATAFILESETS['MC_13TeV_Zee_50ns_Lkh1_PairEvents_RejSel'] = [ PREFIXDATASETS + 'MC_13TeV_Zee_50ns_Lkh1_0_PairEvents_RejSel.root']
DATAFILESETS['MC_distordedRejPair']       =[ PREFIXDATASETS + '../Test/MC_distordedRejPair.root' ]

DATAWEIGHTSET={}
DATAWEIGHTSET['Data_13TeV_Zee_50ns_Lkh1']       =[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_50ns_Lkh1_scaled']=[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_25ns_Lkh1']       =[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_25ns_Lkh1_scaled']=[ 1 ]
DATAWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1_1']       =[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_25ns_Lkh1_pt30']  =[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_25ns_Lkh1_pt35']  =[ 1 ]
DATAWEIGHTSET['Data_13TeV_Zee_25ns_Lkh2']       =[ 1 ]
DATAWEIGHTSET['MC_13TeV_Zee_50ns_Lkh1_PairEvents_RejSel'] = [ 1 ]
DATAWEIGHTSET['MC_distordedRejPair'] = [ 1 ]

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

    configName = PREFIXPATH + configPath + StripName( outNameFile ) + '.boost' 
    CreateConfig( configName, configOptions )

    fileName = PREFIXPATH + batchPath + StripName( outNameFile ) + '.sh'


    with open( fileName, 'w+') as batch:
#Configure the server
        batch.write('server=`pwd`\n' 
                    + 'cd ${server} \n'
                    + 'ulimit -S -s 100000 \n'
                    + 'LD_LIBRARY_PATH=/afs/in2p3.fr/home/c/cgoudet/private/Codes/RootCoreBin/lib:/afs/in2p3.fr/home/c/cgoudet/private/Codes/RootCoreBin/bin:$LD_LIBRARY_PATH \n'
                    + 'cd /afs/in2p3.fr/home/c/cgoudet/private/Codes/RootCoreBin/ \n'
                    + 'source local_setup.sh \n'
                    + 'cd ${server} \n'
                    + 'cp -v /afs/in2p3.fr/home/c/cgoudet/private/Codes/RootCoreBin/obj/x86_64-slc6-gcc48-opt/Template/bin/MeasureScale . \n'
                    )
        
#Copy the configuration file to the server
        batch.write( 'cp ' + configName + ' . \n' )
        
#copy the data files to the server and prepare the command line
        dataLine=""
        for iFile in range( 0, len( dataFiles ) ) :
            batch.write( 'cp -v ' + dataFiles[iFile] + ' . \n' )
            dataLine+=" --dataFileName " + StripName( dataFiles[iFile], 1, 0 ) + ' --dataWeight ' + str( dataWeights[iFile] ) 
        
#copy the MC files to the server and prepare command line
        MCLine=""
        for iFile in range( 0, len( MCFiles ) ) :
            batch.write( 'cp -v ' + MCFiles[iFile] + ' . \n' )
            MCLine+=" --MCFileName " + StripName( MCFiles[iFile], 1, 0 ) + ' --MCWeight ' + str( MCWeights[iFile] )

#If correction Alpha
#Check the size of the vector
#copy the file on the server
#prepare the command line
        correctionLine=""
        if len( inVector ) > 6 and inVector[5] != "" and inVector[6] != "" :
            correctionLine +=' --correctAlphaFileName ' + inVector[5] + ' --correctAlphaHistName ' + inVector[6]
            batch.write( 'cp ' + PREFIXPATH + inVector[5] + ' . \n')

        if len( inVector ) > 8 and inVector[7] != "" and inVector[8] != "" :
            correctionLine +=' --correctSigmaFileName ' + inVector[7] + ' --correctSigmaHistName ' + inVector[8]
            batch.write( 'cp ' + PREFIXPATH + inVector[7] + ' . \n')

#Create an outName
        if outNameFile != "" :
            outNameFile = ' --outFileName ' + outNameFile

#Fill the command line
            if mode==0 :
                if doDistorded==0 :
                        batch.write( 'MeasureScale --configFile ' + StripName(configName, 1, 0)
                                 + dataLine + MCLine + correctionLine + outNameFile + ' --makePlot\n')
                else : 
                    batch.write( 'MeasureScale --configFile ' + StripName(configName, 1, 0) 
                                 + dataLine.replace( '--dataFileName', '--MCFileName' ) +  correctionLine + outNameFile + ' --createDistorded MC_distorded.root \n')
                    batch.write( 'MeasureScale --configFile ' + StripName(configName, 1, 0 )
                                 + ' --dataFileName MC_distorded.root ' + MCLine + correctionLine + outNameFile + ' --makePlot\n')

#Copy the output pdf and root file to result folder
#                batch.write( 'cp *.tex ' + PREFIXPATH + resultPath + '. \n' )
                batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
                batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`*.root ' + PREFIXPATH + resultPath + '. \n' ) 

                

            else :
                batch.write( 'GenerateToyTemplates --configFile ' + StripName(configName, 1, 0)
                             + dataLine + MCLine + optionLine + outNameFile +' \n' )
#                batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
                batch.write( 'cp -v ' + inVector[0] + ' ' + PREFIXPATH + resultPath + '. \n' )
                # batch.write( 'cp Note*.root ' + PREFIXPATH + plotPath + '. \n' ) 
                # batch.write( 'cp Note*.pdf ' + PREFIXPATH + plotPath + '. \n' ) 

        batch.write( 'ls -lh \n' ) 
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

    options = {}
    options['ZMassMin'] = 80
    options['ZMassMax'] = 100
    options['ZMassNBins'] = 20
    options['mode'] = "1VAR"
    options['var1'] = "ETA_CALO"
    options['var2'] = ""
    options['doScale'] = 1
    options['alphaMin']=-0.1
    options['alphaMax']=0.1
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
    options['fitMethod']=1
    options['nUseEl']=1
    options['nUseEvent']=0
    options['nEventCut']=10
    options['thresholdMass']=70
    options['indepDistorded']=0
    options['indepTemplates']=0
    options['inversionMethod']=1
    options['bootstrap']=0
    options['doPileup']=1
    options['doWeight']=1
    options['etaBins']=defaultBinning['ETA24']
    options['ptBins']=''
    options['applySelection']=0

    for inOpt in inOptions :
        optKey = inOpt.split('=')[0]
        optValue= inOpt[inOpt.find('=')+1:]

        if optKey in options.keys() :
            options[optKey]=optValue

        if ( optKey=='ptBins' and 'PT' in optValue ) or ( optKey=='etaBins' and 'ETA' in optValue ) :
            options[optKey]=defaultBinning[optValue]

    with open( configName, 'w' ) as batch:
        for iLabel in options.keys() :
            batch.write( iLabel  + '=' + str( options[iLabel] ) + '\n' )
        
