import os
import sys
from math import *
from Functions_MeasureAlphaSigma import *
import time;
 
#One config file correspond to one job

configFiles=[ 
    ['', 'MC15c_evenEvents', 'MC15c_oddEvents', ['indepDistorded=2', 'indepTemplates=2', 'bootstrap=2', 'etaBins=ETA68', 'doSmearing=0', 'doScale=1', 'alphaSimEta=SIMALPHAETA68', 'nUseEl=3']]
    ]

inputC = [ 0 ]
inputStat = [ 0 ]
nIteration = 1 #total number of jobs
outName = 'TreeToyTemplates_' + str( int( time.time()%(2600*24*365*3) ) )
counter =0
nUseEl= 1
fitPerJob= 1 # number of toys per command "GenerateToyTemplate"
commandPerJob=1 # number of commands per job

nJobs= nIteration/ float((fitPerJob*commandPerJob))

nJobs=int(ceil(nJobs))

toyNumber=0

plotPath= '/sps/atlas/a/aguerguichon/Calibration/Bias/Toys/'
commandCount=0
for vInput in  inputC  :
    for vStat in inputStat :
        print( vInput, vStat )
        for iJob in range( 0, nJobs) :
            optionLine=[]
            for iCommand in range (0, commandPerJob) :
                configFiles[0][0] = outName + str( counter ) + '.root'
                optionLine.append(   ' --inputC ' + str( vInput ) + ' --inputStat ' + str( vStat ) + ' --nIteration ' + str( min( nIteration-iJob, fitPerJob ) ) + ' --toyNumber '+ str( iCommand*fitPerJob +iJob*commandPerJob*fitPerJob  )+' ')

                counter+=1

            if nUseEl != 1 :
                configFiles[0][3].append( 'nUseEl=' + str( nUseEl ) )
            logPath="Log/"
            launcherFile=CreateLauncher( configFiles[0], 2, optionLine )
            launchLine='./sub1.sh ' + StripString( configFiles[0][0] ) + ' ' \
                + plotPath + logPath  + StripString( configFiles[0][0] ) + '.log ' \
                + plotPath + logPath  + StripString( configFiles[0][0] ) + '.err ' \
                + launcherFile

            os.system( launchLine )

