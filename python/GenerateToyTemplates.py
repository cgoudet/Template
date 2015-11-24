import os
import sys
from Functions_MeasureAlphaSigma import *
import time; 

#One config file correspond to one job
configFiles=[ 
    ['', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_RejSel', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel', ['indepDistorded=1', 'indepTemplates=1', 'bootstrap=1', 'etaBins=ETA6', 'debug=1', 'inversionMethod=11', 'optimizeRanges=5', 'doScale=0']]
    ]

inputC = [ 0.01 ]
inputStat = [ 1000000 ]
nIteration = 30
outName = 'TreeToyTemplates_' + str( int( time.time()%(2600*24*365*3) ) )
counter =0
nUseEl=1
fitPerJob= 3

plotPath='/sps/atlas/c/cgoudet/Calibration/PreRec/'

for vInput in  inputC  :
    for vStat in inputStat :

        print( vInput, vStat )


        for iIteration in range( 0, nIteration, fitPerJob ) :
            
            configFiles[0][0] = outName + str( counter ) + '.root'
            optionLine = ' --inputC ' + str( vInput ) + ' --inputStat ' + str( vStat ) + ' --nIteration ' + str( min( nIteration-iIteration, fitPerJob ) )
            if nUseEl != 1 :
                configFiles[0][3].append( 'nUseEl=' + str( nUseEl ) )
            logPath="Log/"
            launcherFile=CreateLauncher( configFiles[0], 1, optionLine )
            launchLine='~/sub28.sh ' + StripName( configFiles[0][0] ) + ' ' \
                + plotPath + logPath  + StripName( configFiles[0][0] ) + '.log ' \
                + plotPath + logPath  + StripName( configFiles[0][0] ) + '.err ' \
                + launcherFile

#            print launchLine
            os.system( launchLine )
            counter+=1
