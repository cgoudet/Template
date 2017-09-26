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
	['AlphaOffSummer_16.root', 'Data16', 'MC15c',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_16', 'doSmearing=0',],0 ], #eosNtuples
	['AlphaOffSummer_15.root', 'Data15', 'MC15c',['ZMassMin=80000', 'ZMassMax=100000', 'MCBranchWeightName=weight_15', 'doSmearing=0',],0 ], #eosNtuples
	['ScalesOffSummer_1516.root', 'CorrectedData', 'MC15c',['nUseEl=3']], #nominal to compute systematics
        ['ScalesRelease21_16.root', 'Data16_21', 'MC15c_21',['ZMassMin=80000', 'ZMassMax=100000'] ], #eosNtuples


#================ Systematics
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


	#================ Closure
	#['Closure.root', 'pseudoData', 'MC15c_eos',['nUseEl=5', 'ZMassMin=80000', 'ZMassMax=100000'] ], #nominal
#	['Closure.root', 'MC15c_evenEvents', 'MC15c_oddEvents',['nUseEl=5', 'ZMassMin=80000', 'ZMassMax=100000', 'alphaSimEta=SIMALPHAETA68', 'sigmaSimEta=SIMZEROETA68'], 0, 1 ], #nominal
	]


spsPath="/sps/atlas/a/aguerguichon/Calibration/PreRec/"
logPath="Log/"

	
[ LaunchBatchTemplate( c, spsPath+logPath ) for c in configFiles ]

