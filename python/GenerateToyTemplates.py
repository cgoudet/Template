import os
import sys
from Functions_MeasureAlphaSigma import *
import time; 

#One config file correspond to one job
configFiles=[ 
    ['', 'MC_13TeV_Zee_50ns_Lkh1_1', 'MC_13TeV_Zee_50ns_Lkh1_0', ['indepDistorded=1', 'indepTemplates=1', 'bootstrap=1','debug=1']]
    ]

inputC = [ 0.01 ]
inputStat = [ 1000000 ]
nIteration = 1000
outName = 'TreeToyTemplates_' + str( int( time.time()%(2600*24*365*3) ) )
counter =0
nUseEl=1
fitPerJob= 20

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
