import os
import sys
sys.path.insert(0, 'util')
from MeasureAlphaSigma_Functions import *


#One config file correspond to one job
configFiles=[]

if 0 :
    configFiles=[ 
        ['Config6.boost', 0, 0, 'Data6_50ns.root'],
        ['Config6.boost', 1, 0, 'Data6_50ns_dataScaled.root']
        ['Config6.boost', 8, 0, 'Data6_50ns_periodD.root'],
        ['Config6.boost', 9, 0, 'Data6_50ns_periodAC.root']
        # ['../../testKirill/150830/data/ConfigKirill.boost', 6, 4, "Data_stand.root"],
        # ['../../testKirill/150830/data/ConfigKirill.boost', 7, 5, "Data_dw.root"]
        ]

else :
    configFiles=[
        ['Config24_NUseEl15.boost', 0, 0, "Data24Sigma_invProc1.root" ],
        ['Config34_NUseEl15.boost', 0, 0, "Data34Sigma_invProc1.root" ],
        ]
spsPath="/sps/atlas/c/cgoudet/Calibration/PreRec/"
logPath="Log/"
for confFile in range( 0, len( configFiles ) ) :

    launcherFile=CreateLauncher( configFiles[confFile], 0, "" , 0)
    if  configFiles[confFile][3] == "" :
        logFile = StripName( configFiles[confFile][0] )
    else :
        logFile = StripName( configFiles[confFile][3] )

    launchLine='~/sub28.sh ' + logFile + ' ' \
        + spsPath + logPath + logFile + '.log ' \
        + spsPath + logFile + '.err ' \
        + launcherFile

    os.system( launchLine )
