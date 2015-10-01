import os
import sys
from Functions_MeasureAlphaSigma import *
import time; 

#One config file correspond to one job
configFiles=[ 
    ['Config6_Toys.boost', 4, 2, '']
    ]

inputC = [ 0.01 ]
inputStat = [ 100000 ]
nIteration = 1000
outName = 'TreeToyTemplates_' + str( int( time.time()%(2600*24*365*3) ) )
counter =0
nUseEl=3
fitPerJob= 5

plotPath='/sps/atlas/c/cgoudet/Calibration/PreRec/'

for vInput in  inputC  :
    for vStat in inputStat :

        print( vInput, vStat )

        if vStat == 0 :
            fitPerJob=1
            nUseEl = 10

        for iIteration in range( 0, nIteration, fitPerJob ) :
            
            configFiles[0][3] = outName + str( counter ) + '.root'
            optionLine = ' --inputC ' + str( vInput ) + ' --inputStat ' + str( vStat ) + ' --nIteration ' + str( min( nIteration-iIteration, fitPerJob ) ) \
                + ' --nUseEl ' + str( nUseEl ) + " --indepTemplates 1 --indepDistorded 1 "
            logPath="Log/"
            launcherFile=CreateLauncher( configFiles[0], 1, optionLine, 0 )
            launchLine='~/sub28.sh ' + StripName( configFiles[0][3] ) + ' ' \
                + plotPath + logPath  + StripName( configFiles[0][3] ) + '.log ' \
                + plotPath + logPath  + StripName( configFiles[0][3] ) + '.err ' \
                + launcherFile

#            print launchLine
            os.system( launchLine )
            counter+=1
