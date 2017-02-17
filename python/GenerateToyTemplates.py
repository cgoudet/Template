import os
import sys
from math import *
from Functions_MeasureAlphaSigma import *
import time;
 
isAntinea=1
#One config file correspond to one job

configFiles=[ 
    ['', 'MC15c_evenEvents', 'MC15c_oddEvents', ['indepDistorded=2', 'indepTemplates=2', 'bootstrap=2', 'etaBins=ETA6', 'doScale=0']]
    ]

inputC = [ 0.007 ]
inputStat = [ 1000000 ]
nIteration = 10 #total number of jobs
outName = 'TreeToyTemplates_' + str( int( time.time()%(2600*24*365*3) ) )
counter =0
nUseEl= 1
fitPerJob= 3 # number of toys per command "GenerateToyTemplate"
commandPerJob=2 # number of commands per job
#nJobs= nIteration/ (fitPerJob*commandPerJob) if nIteration%(fitPerJob*commandPerJob)==0 else (nIteration/ (fitPerJob*commandPerJob)) +1
nJobs= nIteration/ float((fitPerJob*commandPerJob))

nJobs=int(ceil(nJobs))

print(nJobs)
toyNumber=0

plotPath= '/sps/atlas/a/aguerguichon/Calibration/Bias/Toys/' if isAntinea else '/sps/atlas/c/cgoudet/Calibration/PreRec/'
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
            print(optionLine, configFiles[0][0]) 
            logPath="Log/"
            launcherFile=CreateLauncher( configFiles[0], 2, optionLine )
            launchLine='~/sub1.sh ' + StripString( configFiles[0][0] ) + ' ' \
                + plotPath + logPath  + StripString( configFiles[0][0] ) + '.log ' \
                + plotPath + logPath  + StripString( configFiles[0][0] ) + '.err ' \
                + launcherFile


            #os.system( launchLine )



