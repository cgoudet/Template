import os
import sys
from Functions_MeasureAlphaSigma import *
import time; 

#One config file correspond to one job
configFiles=[ 

    ['', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_RejSel', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel', ['indepDistorded=2', 'indepTemplates=2', 'bootstrap=2', 'etaBins=ETA6', 'doScale=0']]
    ]

inputC = [ 0.007 ]
inputStat = [ 100000 ]
nIteration = 1
outName = 'TreeToyTemplates_' + str( int( time.time()%(2600*24*365*3) ) )
counter =0
nUseEl= 1
fitPerJob= 1

plotPath='/sps/atlas/a/aguerguichon/Calibration/Bias/Toys/'

for vInput in  inputC  :
    for vStat in inputStat :

        print( vInput, vStat )
        for iIteration in range( 0, nIteration, fitPerJob ) :
            
            configFiles[0][0] = outName + str( counter ) + '.root'

            #optionLine = ' --inputC ' + str( vInput ) + ' --inputStat ' + str( vStat ) + ' --nIteration ' + str( min( nIteration-iIteration, fitPerJob ) ) + ' --toyNumber '+ str( iIteration )+' '

            optionLine = ' --inputC ' + str( vInput ) + ' --inputStat ' + str( vStat ) + ' --nIteration ' + str( min( nIteration-iIteration, fitPerJob ) ) + ' --toyNumber 99'

            if nUseEl != 1 :
                configFiles[0][3].append( 'nUseEl=' + str( nUseEl ) )
            logPath="Log/"
            launcherFile=CreateLauncher( configFiles[0], 2, optionLine )
            launchLine='~/sub1.sh ' + StripString( configFiles[0][0] ) + ' ' \
                + plotPath + logPath  + StripString( configFiles[0][0] ) + '.log ' \
                + plotPath + logPath  + StripString( configFiles[0][0] ) + '.err ' \
                + launcherFile

#            print launchLine
            os.system( launchLine )
            counter+=1
