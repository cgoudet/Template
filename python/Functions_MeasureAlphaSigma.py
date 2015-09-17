PREFIXPATH="/sps/atlas/c/cgoudet/Calibration/PreRec/"
PREFIXDATASETS="/sps/atlas/c/cgoudet/Calibration/"

MCFILESETS=[
    [ PREFIXDATASETS + 'MC_13TeV_Zee_Lkh1_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_Lkh1_1.root' ],
    [ PREFIXDATASETS + 'MC_13TeV_Zee_Lkh1_scaled_0.root', PREFIXDATASETS + 'MC_13TeV_Zee_Lkh1_scaled_1.root'], 
    [ PREFIXDATASETS + 'MC_8TeV_ZeeDiLepton_scaled_Lkh1_0.root', PREFIXDATASETS + 'MC_8TeV_ZeeDiLepton_scaled_Lkh1_1.root', PREFIXDATASETS + 'MC_8TeV_ZeeDiLepton_scaled_Lkh1_2.root', PREFIXDATASETS + 'MC_8TeV_Zee1Lepton_scaled_Lkh1_0.root'],
    [ PREFIXDATASETS + 'DataxAOD/MC13/MC_13TeV_Zee_Lkh1_0.root' ],
    [ PREFIXDATASETS + 'testKirill/150830/data/MC_stand.root' ],
    [ PREFIXDATASETS + 'testKirill/150830/data/MC_dw.root' ]
    ]

MCWEIGHTSET=[ 
    [ 1, 1 ],
    [ 1, 1, 1],
    [ 0.2923, 0.2923, 0.2923, 0.32194 ],
    [1],
    [1],
    [1]
    ]

DATAFILESETS=[
    [ PREFIXDATASETS + 'DataxAOD/Data13_50ns/Data_13TeV_Zee_50ns_Lkh1_0.root'],
    [ PREFIXDATASETS + 'DataxAOD/Data13_50ns_scaled/Data_13TeV_Zee_50ns_Lkh1_scaled_0.root'],
    [ PREFIXDATASETS + 'DataxAOD/DATA8/Data_8TeV_ZeeLkh1_0.root'],
    [ PREFIXDATASETS + 'DataxAOD/EGAM1_DATA15/Data_13TeV_PA_Zee_Lkh1_scaled_0.root' ],
    [ PREFIXDATASETS + 'DataxAOD/EGAM1_DATA15/Data_13TeV_PC_Zee_Lkh1_scaled_0.root' ],
    [ PREFIXDATASETS + 'DataxAOD/MC13/MC_13TeV_Zee_Lkh1_1.root' ],
    [ PREFIXDATASETS + 'testKirill/150830/data/Data_stand.root' ],
    [ PREFIXDATASETS + 'testKirill/150830/data/Data_dw.root' ],
    [ PREFIXDATASETS + 'DataxAOD/Data13_50ns/Data_13TeV_Zee_50ns_276731_id43130364_0.root'],
    [ PREFIXDATASETS + 'DataxAOD/Data13_50ns/Data_13TeV_Zee_50ns_periodAC_0.root']
    ]

DATAWEIGHTSET=[
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1],
    [1]
    ]


def CreateLauncher( inVector, mode = 0, optionLine="" , doDistorded=0 ) :

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

    configFile=inVector[0]
    dataFiles=DATAFILESETS[ inVector[1] ]
    dataWeights=DATAWEIGHTSET[ inVector[1] ]  
    MCFiles=MCFILESETS[ inVector[2] ]
    MCWeights=MCWEIGHTSET[ inVector[2] ]
    outNameFile=inVector[3]



    configPath="Config/"
    batchPath="Batch/"
    resultPath="Results/"
    plotPath="Plots/"
    fileName = batchPath + StripName( outNameFile ) + '.sh'

    with open( fileName, 'w+') as batch:
#Configure the server
        batch.write('server=`pwd`\n' 
                    # + 'cp  /afs/in2p3.fr/home/c/cgoudet/private/Template/* -r . \n'
                    # + 'export ATLAS_LOCAL_ROOT_BASE=/cvmfs/atlas.cern.ch/repo/ATLASLocalRootBase \n'
                    # + 'source ${ATLAS_LOCAL_ROOT_BASE}/user/atlasLocalSetup.sh \n'
                    # + 'rcSetup Base,2.3.25 \n rc clean \n rc find_packages \n rc compile \n'
                 #    + 'cd /afs/cern.ch/atlas/project/HSG7/root/root_v5-34-19/x86_64-slc6-gcc47/ \n' 
                 # + 'source bin/thisroot.sh \n'
                    + 'cd ${server} \n'
                    + 'ulimit -S -s 100000 \n'
                    + 'LD_LIBRARY_PATH=/afs/in2p3.fr/home/c/cgoudet/private/Template/RootCoreBin/lib:/afs/in2p3.fr/home/c/cgoudet/private/Template/RootCoreBin/bin:$LD_LIBRARY_PATH \n'
                    + 'cd /afs/in2p3.fr/home/c/cgoudet/private/Template/RootCoreBin/ \n'
                    + 'source local_setup.sh \n'
                    + 'cd ${server} \n'
                    + 'cp -v /afs/in2p3.fr/home/c/cgoudet/private/Template/RootCoreBin/obj/x86_64-slc6-gcc48-opt/Template/bin/MeasureScale . \n'
                    )
        
#Copy the configuration file to the server
        batch.write( 'cp ' + PREFIXPATH + configPath + configFile + ' . \n' )
        
#copy the data files to the server and prepare the command line
        dataLine=""
        for iFile in range( 0, len( dataFiles ) ) :
            batch.write( 'cp ' + dataFiles[iFile] + ' . \n' )
            dataLine+=" --dataFileName " + StripName( dataFiles[iFile], 1, 0 ) + ' --dataWeight ' + str( dataWeights[iFile] ) 
        
#copy the MC files to the server and prepare command line
        MCLine=""
        for iFile in range( 0, len( MCFiles ) ) :
            batch.write( 'cp ' + MCFiles[iFile] + ' . \n' )
            MCLine+=" --MCFileName " + StripName( MCFiles[iFile], 1, 0 ) + ' --MCWeight ' + str( MCWeights[iFile] )

#If correction Alpha
#Check the size of the vector
#copy the file on the server
#prepare the command line
        correctionLine=""
        if len( inVector ) >= 6 and inVector[4] != "" and inVector[5] != "" :
            correctionLine +=' --correctAlphaFileName ' + inVector[4] + ' --correctAlphaHistName ' + inVector[5]
            batch.write( 'cp ' + PREFIXPATH + inVector[4] + ' . \n')

        if len( inVector ) >= 8 and inVector[6] != "" and inVector[7] != "" :
            correctionLine +=' --correctSigmaFileName ' + inVector[6] + ' --correctSigmaHistName ' + inVector[7]
            batch.write( 'cp ' + PREFIXPATH + inVector[6] + ' . \n')

#Create an outName
        if outNameFile != "" :
            outNameFile = ' --outFileName ' + outNameFile

#Fill the command line
            if mode==0 :
                if doDistorded==0 :
                        batch.write( 'MeasureScale --configFile ' + StripName(configFile, 1, 0)
                                 + dataLine + MCLine + correctionLine + outNameFile + ' --makePlot\n')
                else : 
                    batch.write( 'MeasureScale --configFile ' + StripName(configFile, 1, 0) 
                                 + dataLine.replace( '--dataFileName', '--MCFileName' ) +  correctionLine + outNameFile + ' --createDistorded MC_distorded.root \n')
                    batch.write( 'MeasureScale --configFile ' + StripName(configFile, 1, 0 )
                                 + ' --dataFileName MC_distorded.root ' + MCLine + correctionLine + outNameFile + ' --makePlot\n')

#Copy the output pdf and root file to result folder
                batch.write( 'cp *.tex ' + PREFIXPATH + resultPath + '. \n' )
                batch.write( 'cp `ls *.tex | awk -F "." \'{print $1 }\'`.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
                batch.write( 'cp `ls *.tex | awk -F "." \'{print $1 }\'`*.root ' + PREFIXPATH + resultPath + '. \n' ) 

                

            else :
                batch.write( 'GenerateToyTemplates --configFile ' + StripName(configFile, 1, 0)
                             + dataLine + MCLine + optionLine + outNameFile +' \n' )
#                batch.write( 'cp -v `ls *.tex | awk -F "." \'{print $1 }\'`.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
                batch.write( 'cp -v ' + inVector[3] + ' ' + PREFIXPATH + resultPath + '. \n' )
                batch.write( 'cp Note*.root ' + PREFIXPATH + plotPath + '. \n' ) 
                batch.write( 'cp Note*.pdf ' + PREFIXPATH + plotPath + '. \n' ) 
        return fileName





def StripName( line, doPrefix = 1, doSuffix = 1 ) :
    if ( line.rfind( '.' ) != -1 and doSuffix ) : 
        line = line[0:line.rfind( '.' )]

    if ( line.rfind( '/' ) != -1 and doPrefix ) :
        line = line[line.rfind( '/' )+1:len( line )]

    return line
