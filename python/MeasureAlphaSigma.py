import os
import sys
from Functions_MeasureAlphaSigma import *


#One config file correspond to one job
configFiles=[]
switch=0

if switch==0 :
        configFiles=[ 
		#Mesure des scales
		['DataOff_25ns.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', [] ],
		['DataOff_25ns_dataScaled.root', 'Data_13TeV_Zee_25ns_Lkh1_scaled', 'MC_13TeV_Zee_25ns_Lkh1', [] ],
		#mesure avec electron tight
		['DataOff_25ns_tight.root', 'Data_13TeV_Zee_25ns_Lkh2', 'MC_13TeV_Zee_25ns_Lkh2', [] ],
		#mesure sans pileup
		['DataOff_25ns_noPileup.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1',[] ],
		#mesure avec masse sueil Off0
		['DataOff_25ns_thresholdMass.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', []],
		#mesure avec fenetre masse plus faible
		['DataOff_25ns_massWindow.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', [] ],
		#mesure globale avec pt seuil
#		['Data1_25ns.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', ['etaBins=ETA6'] ],
		['DataOff_25ns_pt30.root', 'Data_13TeV_Zee_25ns_Lkh1_pt30', 'MC_13TeV_Zee_25ns_Lkh1_pt30', [] ],
		['DataOff_25ns_pt35.root', 'Data_13TeV_Zee_25ns_Lkh1_pt35', 'MC_13TeV_Zee_25ns_Lkh1_pt35', []],
		]
	
elif switch == 1 :
	command = 'cat ' + '/afs/in2p3.fr/home/c/cgoudet/private/eGammaScaleFactors/DatasetList/Data_13TeV_Zee_25ns.csv' 
	inFileRun = os.popen( command ).read().split( '\n' )
	for line  in inFileRun :
		if line == '' or '#' in line :
			continue
		run = int( line.split('.')[1] )

		configFiles.append( 
			['Data6_' + str(run) + '.root', 
			 'Data_13TeV_Zee_25ns_Lkh1_scaled',
			 'MC_13TeV_Zee_25ns_Lkh1', 
			 ['etaBins=ETA6', 'selection=runNumber=='+ str(run), 'debug=1', 'applySelection=1'] ] )
	
		# configFiles.append( ['MC1_PairEvents.root', 'MC_distordedRejPair', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel', ['etaBins=ETA1'], 0] )
		# configFiles.append( ['Config1_noSigma.boost', 'MC_distordedRejPair', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel','MC1_PairEvents_noSigma.root', 0] )
#		configFiles.append( ['Config1_noAlpha.boost', 'Data_13TeV_Zee_50ns_Lkh1', 'MC_13TeV_Zee_50ns_Lkh1', 'Data1_50ns_noAlpha.root', 0, '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noSigma.root', 'measScale_alpha'] )
#		configFiles.append( ['Config1_noSigma.boost', 'Data_13TeV_Zee_50ns_Lkh1', 'MC_13TeV_Zee_50ns_Lkh1', 'Data1_50ns_noSigma_it2.root', 0, '', '', '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noAlpha.root', 'measScale_c'] )
#		configFiles.append( ['Config1_noSigma.boost', 'Data_13TeV_Zee_50ns_Lkh1', 'MC_13TeV_Zee_50ns_Lkh1', 'Data1_50ns_noSigma_itTest.root', 0, '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noSigma.root', 'measScale_alpha', '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noAlpha.root', 'measScale_c'] )



spsPath="/sps/atlas/c/cgoudet/Calibration/PreRec/"
logPath="Log/"

for confFile in range( 0, len( configFiles ) ) :

    launcherFile=CreateLauncher( configFiles[confFile], 0, "" )

    logFile = StripName( configFiles[confFile][0] )
    
    launchLine='~/sub28.sh ' + logFile + ' ' \
        + spsPath + logPath + logFile + '.log ' \
        + spsPath + logPath + logFile + '.err ' \
        + launcherFile

    os.system( launchLine )
