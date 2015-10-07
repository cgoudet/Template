import os
import sys
from Functions_MeasureAlphaSigma import *


#One config file correspond to one job
configFiles=[]
fullSyst=0

if fullSyst :
        configFiles=[ 
            #Mesure des scales
            ['ConfigOff.boost', 2, 3, 'Data6_25ns.root'],
            ['ConfigOff.boost', 3, 3, 'Data6_25ns_dataScaled.root'],
            #mesure avec electron tight
            ['ConfigOff.boost', X, Y, 'Data6_25ns_tight.root'],
            #mesure sans pileup
            ['ConfigOff_noPileup.boost', 2, 3, 'Data6_25ns_noPileup.root'],
            #mesure avec masse sueil 60
            ['ConfigOff_thresholdMass.boost', 2, 3, 'Data6_25ns_thresholdMass.root'],
            #mesure avec fenetre masse plus faible
            ['ConfigOff_massWindow.boost', 2, 3, 'Data6_25ns_massWindow.root'],
            #mesure global avec pt seuil
            ['Config1.boost', 2, 3, 'Data1_25ns.root'],
            ['Config1.boost', X, Y, 'Data1_25ns_pt30.root'],
            ['Config1.boost', X, Y, 'Data1_25ns_pt35.root'],
            ]

else :
    if 1 :
        configFiles=[ 
		['Config1_noSigma.boost', 'Data_13TeV_Zee_50ns_Lkh1', 'MC_13TeV_Zee_50ns_Lkh1', 'Data1_50ns_noSigma.root'],
#		['Config1_noWeight.boost', 'MC_13TeV_Zee_50ns_Lkh1_1', 'MC_13TeV_Zee_50ns_Lkh1_0', 'MC1_50ns.root', 1 ],
		#            ['Config6_noWeight.boost', 'MC_13TeV_Zee_50ns_Lkh1_1', 'MC_13TeV_Zee_50ns_Lkh1_0', 'MC6_50ns.root', 1 ]

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

    launcherFile=CreateLauncher( configFiles[confFile], 0, "" )

    if  configFiles[confFile][3] == "" :
        logFile = StripName( configFiles[confFile][0] )
    else :
        logFile = StripName( configFiles[confFile][3] )

    launchLine='~/sub28.sh ' + logFile + ' ' \
        + spsPath + logPath + logFile + '.log ' \
        + spsPath + logPath + logFile + '.err ' \
        + launcherFile

    os.system( launchLine )
