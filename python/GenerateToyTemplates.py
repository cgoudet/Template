import os
import sys
from Functions_MeasureAlphaSigma import *
import time; 

#One config file correspond to one job
configFiles=[ 
    ['', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_RejSel', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel', ['indepDistorded=2', 'indepTemplates=2', 'bootstrap=0', 'etaBins=ETA6', 'doScale=0', 'doSimulation=1'], 0, 1 ]
    ]

inputC = [ 0.007 ]
inputStat = [ 100000 ]
nIteration = 3
outName = 'TreeToyTemplates_' + str( int( time.time()%(2600*24*365*3) ) )
counter =0
nUseEl= 1
fitPerJob= 2

plotPath='/sps/atlas/c/cgoudet/Calibration/PreRec/'

for vInput in  inputC  :
    for vStat in inputStat :

        print( vInput, vStat )
        for iIteration in range( 0, nIteration, fitPerJob ) :
            
            configFiles[0][0] = outName + str( counter ) + '.root'


            optionLine = ' --inputC ' + str( vInput ) + ' --inputStat ' + str( vStat ) + ' --nIteration ' + str( min( nIteration-iIteration, fitPerJob ) ) + ' --toyNumber '+ str( iIteration )+' '
            if nUseEl != 1 :
                configFiles[0][3].append( 'nUseEl=' + str( nUseEl ) )
            logPath="Log/"
            launcherFile=CreateLauncher( configFiles[0], 2, optionLine )
            launchLine='~/sub1.sh ' + StripName( configFiles[0][0] ) + ' ' \
                + plotPath + logPath  + StripName( configFiles[0][0] ) + '.log ' \
                + plotPath + logPath  + StripName( configFiles[0][0] ) + '.err ' \
                + launcherFile

#            print launchLine
            os.system( launchLine )
            counter+=1
