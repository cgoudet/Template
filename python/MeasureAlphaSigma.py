import os
import sys
from Functions_MeasureAlphaSigma import *


#One config file correspond to one job
configFiles=[]

if 1 :
    configFiles=[ 
        # ['Config6.boost', 0, 0, 'Data6_50ns.root'],
        # ['Config6.boost', 1, 0, 'Data6_50ns_dataScaled.root'],
        # ['Config1.boost', 0, 0, 'Data1_50ns.root'],
        ['Config6.boost', 2, 5, 'Data6_25ns.root'],
        ['Config6.boost', 3, 5, 'Data6_25ns_dataScaled.root'],
        ['Config1.boost', 2, 5, 'Data1_25ns.root']
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
        + spsPath + logPath + logFile + '.err ' \
        + launcherFile

    os.system( launchLine )
