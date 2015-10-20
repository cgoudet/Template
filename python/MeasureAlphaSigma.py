import os
import sys
from Functions_MeasureAlphaSigma import *


#One config file correspond to one job
configFiles=[]
fullSyst=0

if fullSyst :
        configFiles=[ 
		#Mesure des scales
		['ConfigOff.boost', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', 'Data6_25ns.root'],
		['ConfigOff.boost', 'Data_13TeV_Zee_25ns_Lkh1_scaled', 'MC_13TeV_Zee_25ns_Lkh1', 'Data6_25ns_dataScaled.root'],
		#mesure avec electron tight
		['ConfigOff.boost', 'Data_13TeV_Zee_25ns_Lkh2', 'MC_13TeV_Zee_25ns_Lkh2', 'Data6_25ns_tight.root'],
		#mesure sans pileup
		['ConfigOff_noPileup.boost', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', 'Data6_25ns_noPileup.root'],
		#mesure avec masse sueil 60
		['ConfigOff_thresholdMass.boost', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', 'Data6_25ns_thresholdMass.root'],
		#mesure avec fenetre masse plus faible
		['ConfigOff_massWindow.boost', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', 'Data6_25ns_massWindow.root'],
		#mesure globale avec pt seuil
		['Config1.boost', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', 'Data1_25ns.root'],
		['Config1.boost', 'Data_13TeV_Zee_25ns_Lkh1_pt30', 'MC_13TeV_Zee_25ns_Lkh1_pt30', 'Data1_25ns_pt30.root'],
		['Config1.boost', 'Data_13TeV_Zee_25ns_Lkh1_pt35', 'MC_13TeV_Zee_25ns_Lkh1_pt35', 'Data1_25ns_pt35.root'],
		]
	
else :
	if 1 :
		configFiles.append( ['Config1.boost', 'MC_distordedRejPair', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel', 'MC1_PairEvents.root', 0] )
		configFiles.append( ['Config1_noSigma.boost', 'MC_distordedRejPair', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel','MC1_PairEvents_noSigma.root', 0] )
#		configFiles.append( ['Config1_noAlpha.boost', 'Data_13TeV_Zee_50ns_Lkh1', 'MC_13TeV_Zee_50ns_Lkh1', 'Data1_50ns_noAlpha.root', 0, '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noSigma.root', 'measScale_alpha'] )
#		configFiles.append( ['Config1_noSigma.boost', 'Data_13TeV_Zee_50ns_Lkh1', 'MC_13TeV_Zee_50ns_Lkh1', 'Data1_50ns_noSigma_it2.root', 0, '', '', '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noAlpha.root', 'measScale_c'] )
#		configFiles.append( ['Config1_noSigma.boost', 'Data_13TeV_Zee_50ns_Lkh1', 'MC_13TeV_Zee_50ns_Lkh1', 'Data1_50ns_noSigma_itTest.root', 0, '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noSigma.root', 'measScale_alpha', '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noAlpha.root', 'measScale_c'] )

					
		
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
