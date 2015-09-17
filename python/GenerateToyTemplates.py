import os
import sys
from Functions_MeasureAlphaSigma import *
import time; 

#One config file correspond to one job
configFiles=[ 
    ['Config6.boost', 5, 3, '']
    ]

#inputC = [ 0.007, 0.01, 0.015 ]
#inputStat = [ 50000, 100000, 200000, 300000, 500000, 1000000 ]
inputC = [ 0.01 ]
inputStat = [ 1000000 ]
nIteration = 2000
outName = 'TreeToyTemplates_' + str( int( time.time()%(2600*24*365*3) ) )
counter =0
nUseEl=1
fitPerJob= 10

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
                + logPath + StripName( configFiles[0][3] ) + '.log ' \
                + logPath + StripName( configFiles[0][3] ) + '.err ' \
                + launcherFile

            os.system( launchLine )
            counter+=1
