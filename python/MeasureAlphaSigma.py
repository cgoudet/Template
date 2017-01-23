import os
import sys
from Functions_MeasureAlphaSigma import *
import sys
sys.path.append(os.path.abspath("/afs/in2p3.fr/home/a/aguergui/Calibration/PlotFunctions/python"))
from SideFunction import *


#One config file correspond to one job
configFiles=[]
switch=0


if switch==0 :
        configFiles=[ 
			
# 		Mesure des scales
		#['AlphaOff_16.root', 'Data16_13TeV_Zee_noGain_Lkh1', 'MC15c_13TeV_Zee_2016_noGain_Lkh1',[], 0 ], #nominal
		#['AlphaOff_15.root', 'Data15_13TeV_Zee_noGain_Lkh1', 'MC15c_13TeV_Zee_2015_noGain_Lkh1',[], 0 ], #nominal
		['ScalesOff_1516.root', 'CorrectedData', 'MC15c_13TeV_Zee_noGain_Lkh1',['nUseEl=3']], #nominal to compute systematics
		['ScalesGeom.root', 'MC_13TeV_Zee_NewGeom_Lkh1', 'MC15c_13TeV_Zee_2016_noGain_Lkh1',['MCBranchWeightName=weight', "nUseEl=3"] ], #nominal

		# ['Scales_eos_16.root', 'Data16_eos', 'MC15c_eos',['MCBranchWeightName=weight_16', 'etaBins='] ], #eosNtuples
		# ['Scales_eos_15.root', 'Data15_eos', 'MC15c_eos',['MCBranchWeightName=weight_15'] ], #eosNtuples
		
			       
#============Systematics
		#For residuals
 		# ['DataOff_13TeV_dataScaled.root', 'Data1615_13TeV_Zee_Lkh1_scaled', 'MC15c_13TeV_Zee_Lkh1', [] ],
		# Changing mass threshold from 70 to 75GeV
		#['AlphaOff_16_Threshold.root', 'Data16_13TeV_Zee_noGain_Lkh1', 'MC15c_13TeV_Zee_2016_noGain_Lkh1', ['thresholdMass=75'],0],
		#['AlphaOff_15_Threshold.root', 'Data15_13TeV_Zee_noGain_Lkh1', 'MC15c_13TeV_Zee_2015_noGain_Lkh1', ['thresholdMass=75'],0],
		['ScalesOff_1516_Threshold.root', 'CorrectedDataThreshold', 'MC15c_13TeV_Zee_noGain_Lkh1',['nUseEl=3', 'thresholdMass=75']],
		# Changing mass window of interest
		#['AlphaOff_16_Window.root', 'Data16_13TeV_Zee_noGain_Lkh1', 'MC15c_13TeV_Zee_2016_noGain_Lkh1',  ['ZMassMin=82.5', 'ZMassMax=97.5'],0],
		#['AlphaOff_15_Window.root', 'Data15_13TeV_Zee_noGain_Lkh1', 'MC15c_13TeV_Zee_2015_noGain_Lkh1',  ['ZMassMin=82.5', 'ZMassMax=97.5'],0], 
		['ScalesOff_1516_Window.root', 'CorrectedDataWindow', 'MC15c_13TeV_Zee_noGain_Lkh1',['nUseEl=3', 'ZMassMin=82.5', 'ZMassMax=97.5']],
		#  # Electron tight
		#['AlphaOff_16_ID.root', 'Data16_13TeV_Zee_noGain_Lkh2', 'MC15c_13TeV_Zee_2016_noGain_Lkh2', [], 0 ],
		#['AlphaOff_15_ID.root', 'Data15_13TeV_Zee_noGain_Lkh2', 'MC15c_13TeV_Zee_2015_noGain_Lkh2', [], 0 ],
		['ScalesOff_1516_ID.root', 'CorrectedDataID', 'MC15c_13TeV_Zee_noGain_Lkh2',['nUseEl=3']],
		#  #mesure avec fBrem
		#['AlphaOff_16_fBrem.root', 'Data16_13TeV_Zee_noGain_Lkh1_fBrem70', 'MC15c_13TeV_Zee_2016_noGain_Lkh1_fBrem70', [ ], 0],
		#['AlphaOff_15_fBrem.root', 'Data15_13TeV_Zee_noGain_Lkh1_fBrem70', 'MC15c_13TeV_Zee_2015_noGain_Lkh1_fBrem70', [ ], 0],
		['ScalesOff_1516_fBrem.root', 'CorrectedDatafBrem', 'MC15c_13TeV_Zee_noGain_Lkh1_fBrem70',['nUseEl=3'] ],

		# #Removing isolation 
		#['AlphaOff_16_noIso.root', 'Data16_13TeV_Zee_noGain_Lkh1_noIso', 'MC15c_13TeV_Zee_2016_noGain_Lkh1_noIso', [ ], 0],
		#['AlphaOff_15_noIso.root', 'Data15_13TeV_Zee_noGain_Lkh1_noIso', 'MC15c_13TeV_Zee_2015_noGain_Lkh1_noIso', [], 0],
		['ScalesOff_1516_noIso.root', 'CorrectedDataIso', 'MC15c_13TeV_Zee_noGain_Lkh1_noIso',['nUseEl=3'] ],


		# #Efficiencies
		['ScalesOff_1516_IDEff.root', 'CorrectedData', 'MC15c_13TeV_Zee_2015_noGain_Lkh1_IDSyst',['nUseEl=3'] ], 
		['ScalesOff_1516_recoEff.root', 'CorrectedData', 'MC15c_13TeV_Zee_2015_noGain_Lkh1_recoSyst',['nUseEl=3'] ], 
		['ScalesOff_1516_isoEff.root', 'CorrectedData', 'MC15c_13TeV_Zee_2015_noGain_Lkh1_isoSyst',['nUseEl=3']], 

		# #bkg
		# #['DataOff_13TeV_25ns_EW.root', 'Data1615_13TeV_Zee_Lkh1', 'MC_13TeV_bkg_25ns_Lkh1', [] ],
		
		#['DataOff_13TeV_2Steps.root', 'Data1615_13TeV_Zee_Lkh1', 'MC15c_13TeV_Zee_Lkh1', [], 1 ],
		##Syst matiere
		#['DataOff_13TeV_25ns_rel201_IBL.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_IBL_Lkh1', ['dataBranchWeightName=', 'MCBranchWeightName=puWeight SFID SFReco']],

		# #mesure globale avec pt seuil
		# ['Data6_13TeV_25ns.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', ['etaBins=ETA6',] ],
		# ['Data6_13TeV_25ns_pt20.root', 'Data_13TeV_Zee_25ns_Lkh1_pt20', 'MC_13TeV_Zee_25ns_Lkh1_pt20', ['etaBins=ETA6'] ],
		# ['Data6_13TeV_25ns_pt30.root', 'Data_13TeV_Zee_25ns_Lkh1_pt30', 'MC_13TeV_Zee_25ns_Lkh1_pt30', ['etaBins=ETA6'] ],
		# ['Data6_13TeV_25ns_pt35.root', 'Data_13TeV_Zee_25ns_Lkh1_pt35', 'MC_13TeV_Zee_25ns_Lkh1_pt35', ['etaBins=ETA6']],

#		Mesure avec les geometries modifiees
# 		['MCOff_13TeV_25ns_geo02.root', 'MC_13TeV_Zee_25ns_geo02_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1',['nUseEl=2', 'symBin=1', 'debug=1', 'etaBins=ETA24'] ],
# 		['MCOff_13TeV_25ns_geo11.root', 'MC_13TeV_Zee_25ns_geo11_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1',['nUseEl=2', 'symBin=1', 'debug=1', 'etaBins=ETA24'] ],
# 		['MCOff_13TeV_25ns_geo12.root', 'MC_13TeV_Zee_25ns_geo12_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1',['nUseEl=2', 'symBin=1', 'debug=1', 'etaBins=ETA24'] ],
# 		['MCOff_13TeV_25ns_geo13.root', 'MC_13TeV_Zee_25ns_geo13_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1',['nUseEl=2', 'symBin=1', 'debug=1', 'etaBins=ETA24'] ],
# 		['MCOff_13TeV_25ns_geo14.root', 'MC_13TeV_Zee_25ns_geo14_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1',['nUseEl=2', 'symBin=1', 'debug=1', 'etaBins=ETA24'] ],
# 		['MCOff_13TeV_25ns_geo15.root', 'MC_13TeV_Zee_25ns_geo15_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1',['nUseEl=2', 'symBin=1', 'debug=1', 'etaBins=ETA24'] ],
	]
elif switch == 1 :
        configFiles=[ 
		#Mesure des scales
#		['TestOptim.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1', ['dataBranchWeightName=' ], 3 ],
#		['DataOff_13TeV_25ns_rel201_IBL.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_IBL_Lkh1', ['dataBranchWeightName=', 'MCBranchWeightName=puWeight SFID SFReco'], 3 ],
#		['Test2VAR1.root', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_RejSel', ['dataBranchWeightName=', 'MCBranchWeightName=', 'alphaSimEta=0.005 0.005 0.005 0.005 0.005 0.005', 'alphaSimPt=0 0 0 0 0', 'sigmaSimAlpha=0 0 0 0 0', 'sigmaSimEta=0 0 0 0 0 0', 'sigmaSimPt=0 0 0 0 0', 'etaBins=ETA6', 'ptBins=0 50000 100000 150000 200000 1000000', "var2=PT", "mode=2VAR", 'doSmearing=0' ], 0, 1 ],
# 		['TestPT.root', '/sps/atlas/c/cgoudet/Calibration/ScaleResults/Data_13TeV_Zee_25ns_Lkh1_0_corrected.root', 'MC_2015cPRE_corr', ['etaBins=PT6', 'var1=pt', 'branchVarNames=pt_1 pt_1', 'branchVarNames=pt_2 pt_2', 'doSmearing=0'] ],
		# ['Closure_c.root', 'ClosureData', 'ClosureMC', ['etaBins=ETA6', 'sigmaSimEta=SIMSIGMAETA6', 'alphaSimEta=0 0 0 0 0 0', 'doScale=0', 'nUseEvent=100000',  'dataBranchWeightName=' ,'MCBranchWeightName='], 0 ]
		['Closure.root'  , 'ClosureData', 'ClosureMC', ['etaBins=ETA24', 'sigmaSimEta=2e-2 2e-2 5e-3 1.5e-2 1.5e-2 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3  8e-3 8e-3 1.5e-2 1.5e-2 5e-3 2e-2 2e-2', 'alphaSimEta= -2e-2 0 -1.5e-2 1e-2 -2e-2 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -2e-2 1e-2 -1.5e-2 0 -2e-2', 'dataBranchWeightName=' ,'MCBranchWeightName='], 0 ],
		['Closure_nUsel5.root', 'ClosureData', 'ClosureMC', ['etaBins=ETA24', 'sigmaSimEta=2e-2 2e-2 5e-3 1.5e-2 1.5e-2 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3  8e-3 8e-3 1.5e-2 1.5e-2 5e-3 2e-2 2e-2', 'alphaSimEta= -2e-2 0 -1.5e-2 1e-2 -2e-2 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -2e-2 1e-2 -1.5e-2 0 -2e-2', 'nUseEl=5', 'dataBranchWeightName=' ,'MCBranchWeightName='], 0 ],
		['Closure_nUsel10.root', 'ClosureData', 'ClosureMC', ['etaBins=ETA24', 'sigmaSimEta=2e-2 2e-2 5e-3 1.5e-2 1.5e-2 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3 8e-3  8e-3 8e-3 1.5e-2 1.5e-2 5e-3 2e-2 2e-2', 'alphaSimEta= -2e-2 0 -1.5e-2 1e-2 -2e-2 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -15e-3 -2e-2 1e-2 -1.5e-2 0 -2e-2', 'nUseEl=10', 'dataBranchWeightName=' ,'MCBranchWeightName='], 0 ]
		]	

spsPath="/sps/atlas/a/aguerguichon/Calibration/PreRec/"
logPath="Log/"

for confFile in range( 0, len( configFiles ) ) :
	if  len( configFiles[confFile] ) > 4 : mode = configFiles[confFile][4]
	else : mode = 3
	launcherFile=CreateLauncher( configFiles[confFile], mode, "" )
	
	logFile = StripString( configFiles[confFile][0] )
	
	launchLine='~/sub1.sh ' + logFile + ' ' \
	    + spsPath + logPath + logFile + '.log ' \
	    + spsPath + logPath + logFile + '.err ' \
	    + launcherFile
	#print(launchLine)

	os.system( launchLine )
