import os
import sys
from Functions_MeasureAlphaSigma import *
import sys
sys.path.append(os.path.abspath("/afs/in2p3.fr/home/a/aguergui/Calibration/PlotFunctions/python/"))
from SideFunction import *


#One config file correspond to one job
configFiles=[]



configFiles=[ 
		
#=================Nominal
	#['AlphaOffSummer_16.root', 'Data16', 'MC15c',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_16', 'doSmearing=0',],0 ], #eosNtuples
	#['AlphaOffSummer_15.root', 'Data15', 'MC15c',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_15', 'doSmearing=0',],0 ], #eosNtuples
	#['ScalesOffSummer_1516.root', 'CorrectedData', 'MC15c',['nUseEl=3']], #nominal to compute systematics
	#['AlphaOffSummer_16_noDeadCells.root', 'Data16_xcheck', 'MC15c',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_16', 'doSmearing=0',],0 ], #eosNtuples
	#['AlphaOffSummer_15_noDeadCells.root', 'Data15_xcheck', 'MC15c',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_15', 'doSmearing=0',],0 ], #eosNtuples
    #['ScalesOffSummer_1516_noDeadCells.root', 'CorrectedData_noDeadCells', 'MC15c',['nUseEl=3', 'ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_1516']], #nominal to compute systematics

    ['Test.root', 'Data15_xcheck', 'MC15c',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_15'] ], #eosNtuples
	#['customSF.root', 'Data_Kirill', 'MC_Kirill',['nUseEl=3']], #nominal to compute systematics
	#['ScalesGeom.root', 'MC_13TeV_Zee_NewGeom_Lkh1', 'MC15c_13TeV_Zee_noGain_Lkh1',['MCBranchWeightName=weight', 'dataBranchWeightName=weight',"nUseEl=3"] ], #nominal

#================ Systematics
	#For residuals
	# ['DataOff_13TeV_dataScaled.root', 'Data1615_13TeV_Zee_Lkh1_scaled', 'MC15c_13TeV_Zee_Lkh1', [] ],

	# #EW
	 #['AlphaOffSummer_16_EW.root', 'Data16', 'MC15c_EWBkg',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_16 weightNorm_16', 'doSmearing=0',],0 ], #eosNtuples
#	 ['AlphaOffSummer_15_EW.root', 'Data15', 'MC15c_EWBkg',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_15 weightNorm_15', 'doSmearing=0',],0 ], #eosNtuples
	#['ScalesOffSummer_1516_EW.root', 'CorrectedData_EW', 'MC15c',['nUseEl=3', 'MCBranchWeightName=weight_1516 weightNorm_1516']], #nominal to compute systematics


	# #Removing isolation 
	 #['AlphaOffSummer_16_noIsoCut.root', 'Data16_noIsoCut', 'MC15c_noIsoCut',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_16', 'doSmearing=0',],0 ], #eosNtuples
	 #['AlphaOffSummer_15_noIsoCut.root', 'Data15_noIsoCut', 'MC15c_noIsoCut',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_15', 'doSmearing=0',],0 ], #eosNtuples
#	['ScalesOffSummer_1516_noIsoCut.root', 'CorrectedData_noIsoCut', 'MC15c_noIsoCut',['nUseEl=3']], #nominal to compute systematics

	# Changing mass threshold from 70 to 75GeV
	#['AlphaOffSummer_16_Threshold.root', 'Data16', 'MC15c', ['thresholdMass=75', 'MCBranchWeightName=weight_16', 'doSmearing=0'],0],
	#['AlphaOffSummer_15_Threshold.root', 'Data15', 'MC15c', ['thresholdMass=75', 'MCBranchWeightName=weight_15', 'doSmearing=0'],0],
	#['ScalesOffSummer_1516_Threshold.root', 'CorrectedData_Threshold', 'MC15c',['nUseEl=3', 'thresholdMass=75']],

	# Changing mass window of interest
	#['AlphaOffSummer_16_Window.root', 'Data16', 'MC15c',  ['ZMassMin=82500', 'ZMassMax=97500', 'MCBranchWeightName=weight_16', 'doSmearing=0'],0],
	#['AlphaOffSummer_15_Window.root', 'Data15', 'MC15c',  ['ZMassMin=82500', 'ZMassMax=97500', 'MCBranchWeightName=weight_15', 'doSmearing=0'],0], 
	#['ScalesOffSummer_1516_Window.root', 'CorrectedData_Window', 'MC15c',['nUseEl=3', 'ZMassMin=82500', 'ZMassMax=97500']],

	#  # Electron tight
#	['AlphaOffSummer_16_tightID.root', 'Data16_tightID', 'MC15c_tightID', ['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_16', 'doSmearing=0',],0 ],
#	['AlphaOffSummer_15_tightID.root', 'Data15_tightID', 'MC15c_tightID', ['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_15', 'doSmearing=0',],0 ],
	#['ScalesOffSummer_1516_tightID.root', 'CorrectedData_tightID', 'MC15c_tightID',['nUseEl=3']],

	#  #mesure avec fBrem
	#['AlphaOffSummer_16_fBrem50.root', 'Data16_fBrem', 'MC15c_fBrem', ['MCBranchWeightName=weight_16', 'doSmearing=0' ], 0],
	#['AlphaOffSummer_15_fBrem50.root', 'Data15_fBrem', 'MC15c_fBrem', ['MCBranchWeightName=weight_15', 'doSmearing=0' ], 0],
	#['ScalesOffSummer_1516_fBrem50.root', 'CorrectedData_fBrem', 'MC15c_fBrem',['nUseEl=3'] ],
	

	# #Efficiencies
	# ['ScalesOffSummer_1516_IDEff.root', 'CorrectedData', 'MC15c',['nUseEl=3', 'MCBranchWeightName= el2_trigger_SF el2_isEM_SFup el2_reconstruction_SF el2_isolation_SF weight_pileup_1516' ] ], 
	# ['ScalesOffSummer_1516_recoEff.root', 'CorrectedData', 'MC15c',['nUseEl=3', 'MCBranchWeightName= el2_trigger_SF el2_isEM_SF el2_reconstruction_SFup el2_isolation_SF weight_pileup_1516' ] ], 
	# ['ScalesOffSummer_1516_triggerEff.root', 'CorrectedData', 'MC15c',['nUseEl=3', 'MCBranchWeightName= el2_trigger_SFup el2_isEM_SF el2_reconstruction_SF el2_isolation_SF weight_pileup_1516' ] ], 
	# ['ScalesOffSummer_1516_isoEff.root', 'CorrectedData', 'MC15c',['nUseEl=3', 'MCBranchWeightName= el2_trigger_SF el2_isEM_SF el2_reconstruction_SF el2_isolation_SFup weight_pileup_1516' ] ], 



#================ Distorted
	# ['AlphaDistorted_s2763.root', 'Data16', 'Distorted_s2763', ['MCBranchWeightName=weight_16', 'dataBranchWeightName=',"nUseEl=20", 'doSmearing=0'], 0 ], #nominal 
	# ['AlphaDistorted_s2764.root', 'Data16', 'Distorted_s2764', ['MCBranchWeightName=weight_16', 'dataBranchWeightName=',"nUseEl=20", 'doSmearing=0'], 0 ], #nominal 
	# ['AlphaDistorted_s2765.root', 'Data16', 'Distorted_s2765', ['MCBranchWeightName=weight_16', 'dataBranchWeightName=',"nUseEl=20", 'doSmearing=0'], 0 ], #nominal
	# ['AlphaDistorted_s2766.root', 'Data16', 'Distorted_s2766', ['MCBranchWeightName=weight_16', 'dataBranchWeightName=',"nUseEl=20", 'doSmearing=0'], 0 ], #nominal
	# ['AlphaDistorted_s2767.root', 'Data16','Distorted_s2767', ['MCBranchWeightName=weight_16', 'dataBranchWeightName=',"nUseEl=20", 'doSmearing=0'], 0 ], #nominal
	# ['AlphaDistorted_s2768.root', 'Data16','Distorted_s2768', ['MCBranchWeightName=weight_16', 'dataBranchWeightName=',"nUseEl=20", 'doSmearing=0'], 0 ], #nominal


	#================ Closure
	#['Closure.root', 'pseudoData', 'MC15c_eos',['nUseEl=5', 'ZMassMin=80000', 'ZMassMax=100000'] ], #nominal
	#['Closure_Saskia.root', 'pseudoData_Saskia', 'MC_Saskia',['nUseEl=5'] ], #nominal
	#['Test24bins_16.root', 'Data16_eos', 'MC15c_eos',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_16', 'nUseEl=3', "etaBins=ETA24"] ], #eosNtuples
	
#	['Closure.root', 'MC15c_evenEvents', 'MC15c_oddEvents',['nUseEl=5', 'ZMassMin=80000', 'ZMassMax=100000', 'alphaSimEta=SIMALPHAETA68', 'sigmaSimEta=SIMZEROETA68'], 0, 1 ], #nominal

	#['DataOff_13TeV_2Steps.root', 'Data1615_13TeV_Zee_Lkh1', 'MC15c_13TeV_Zee_Lkh1', [], 1 ],
	##Syst matiere
	#['DataOff_13TeV_25ns_rel201_IBL.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_IBL_Lkh1', ['dataBranchWeightName=', 'MCBranchWeightName=puWeight SFID SFReco']],


	]


spsPath="/sps/atlas/a/aguerguichon/Calibration/PreRec/"
logPath="Log/"

# for confFile in range( 0, len( configFiles ) ) :
# 	if  len( configFiles[confFile] ) > 4 : mode = configFiles[confFile][4]
# 	else : mode = 3
# 	launcherFile=CreateLauncher( configFiles[confFile], mode, "" )
	
# 	logFile = StripString( configFiles[confFile][0] )
	
# 	launchLine='~/sub1.sh ' + logFile + ' ' \
# 	    + spsPath + logPath + logFile + '.log ' \
# 	    + spsPath + logPath + logFile + '.err ' \
# 	    + launcherFile


#	os.system( launchLine )


# 	os.system( launchLine )


	
[ LaunchBatchTemplate( c, spsPath+logPath ) for c in configFiles ]

