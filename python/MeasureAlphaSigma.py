import os
import sys
from Functions_MeasureAlphaSigma import *


#One config file correspond to one job
configFiles=[]
switch=0

if switch==0 :
        configFiles=[ 
		#Mesure des scales
		['DataOff_13TeV_25ns.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', ['nUseEl=2'] ],
		#		['DataOff_13TeV_25ns_dataScaled.root', 'Data_13TeV_Zee_25ns_Lkh1_scaled', 'MC_13TeV_Zee_25ns_Lkh1', ['nUseEl=2'] ],
		# #mesure avec electron tight
		# ['DataOff_13TeV_25ns_tight.root', 'Data_13TeV_Zee_25ns_Lkh2', 'MC_13TeV_Zee_25ns_Lkh2', ['nUseEl=2'] ],
		# #mesure sans pileup
		# ['DataOff_13TeV_25ns_noPileup.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1',['MCBranchWeightName=vertexWeight SFWeight_1 SFWeight_2','nUseEl=2'] ],
		# #mesure avec masse sueil Off0
		# ['DataOff_13TeV_25ns_thresholdMass.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', ['nUseEl=2','thresholdMass=75']],
		# #mesure avec fenetre masse plus faible
		# ['DataOff_13TeV_25ns_massWindow.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', ['nUseEl=2', 'ZMassMin=82.5', 'ZMassMax=97.5'] ],
		# #mesure globale avec pt seuil
		# ['Data6_13TeV_25ns.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', ['etaBins=ETA6','nUseEl=2'] ],
		# ['Data6_13TeV_25ns_pt20.root', 'Data_13TeV_Zee_25ns_Lkh1_pt20', 'MC_13TeV_Zee_25ns_Lkh1_pt20', ['etaBins=ETA6','nUseEl=2'] ],
		# ['Data6_13TeV_25ns_pt30.root', 'Data_13TeV_Zee_25ns_Lkh1_pt30', 'MC_13TeV_Zee_25ns_Lkh1_pt30', ['etaBins=ETA6','nUseEl=2'] ],
		# ['Data6_13TeV_25ns_pt35.root', 'Data_13TeV_Zee_25ns_Lkh1_pt35', 'MC_13TeV_Zee_25ns_Lkh1_pt35', ['etaBins=ETA6','nUseEl=2']],
		# #Mesure avec les geometries modifiees
		# ['DataOff_13TeV_25ns_geo02.root', 'MC_13TeV_Zee_25ns_geo02_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1',['nUseEl=2'] ],
		# ['DataOff_13TeV_25ns_geo11.root', 'MC_13TeV_Zee_25ns_geo11_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1',['nUseEl=2'] ],
		# ['DataOff_13TeV_25ns_geo12.root', 'MC_13TeV_Zee_25ns_geo12_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1',['nUseEl=2'] ],
		# ['DataOff_13TeV_25ns_geo13.root', 'MC_13TeV_Zee_25ns_geo13_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1',['nUseEl=2'] ],
		# ['DataOff_13TeV_25ns_geo14.root', 'MC_13TeV_Zee_25ns_geo14_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1',['nUseEl=2'] ],
		# ['DataOff_13TeV_25ns_geo15.root', 'MC_13TeV_Zee_25ns_geo15_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1',['nUseEl=2'] ],
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
	
		# 

#		configFiles.append( ['Config1_noAlpha.boost', 'Data_13TeV_Zee_50ns_Lkh1', 'MC_13TeV_Zee_50ns_Lkh1', 'Data1_50ns_noAlpha.root', 0, '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noSigma.root', 'measScale_alpha'] )
#		configFiles.append( ['Config1_noSigma.boost', 'Data_13TeV_Zee_50ns_Lkh1', 'MC_13TeV_Zee_50ns_Lkh1', 'Data1_50ns_noSigma_it2.root', 0, '', '', '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noAlpha.root', 'measScale_c'] )
#		configFiles.append( ['Config1_noSigma.boost', 'Data_13TeV_Zee_50ns_Lkh1', 'MC_13TeV_Zee_50ns_Lkh1', 'Data1_50ns_noSigma_itTest.root', 0, '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noSigma.root', 'measScale_alpha', '/sps/atlas/c/cgoudet/Calibration/PreRec/Results/Data1_50ns_noAlpha.root', 'measScale_c'] )

elif switch == 2 :
	# configFiles.append( ['MC6_nUseEl15.root', 'ClosureData', 'ClosureMC', ['nUseEl=15', 'etaBins=ETA6' ]] )
	# configFiles.append( ['MC6_nUseEl15_fit1.root', 'ClosureData', 'ClosureMC', ['nUseEl=15', 'etaBins=ETA6', 'fitMethod1' ]] )
	# configFiles.append( ['MC6_nUseEl10.root', 'ClosureData', 'ClosureMC', ['nUseEl=10', 'etaBins=ETA6' ]] )
	configFiles.append( ['MC6_nUseEl5.root', 'ClosureData', 'ClosureMC', ['nUseEl=5', 'etaBins=ETA6' ]] )
	configFiles.append( ['MC6_nUseEl1.root',  'ClosureData', 'ClosureMC', ['nUseEl=1', 'etaBins=ETA6' ]] )

elif switch == 3 :
	configFiles.append( ['Data_8TeV.root', 'Data_8TeV_Zee_Lkh1', 'MC_8TeV_Zee_Lkh1', ['nUseEl=15', 'etaBins=ETA68'] ] )


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
