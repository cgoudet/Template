import os
import sys
from Functions_MeasureAlphaSigma import *
import sys
sys.path.append(os.path.abspath("/afs/in2p3.fr/home/c/cgoudet/private/Calibration/PlotFunctions/python"))
from SideFunction import *


#One config file correspond to one job
configFiles=[]
switch=1

if switch==0 :
        configFiles=[ 
# 		#Mesure des scales
 		['DataOff_13TeV_25ns_nominal.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', ['etaBins=ETA68'], 3 ],
 		['DataOff_13TeV_25ns_syst.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', ['debug=1'] ],
# 		['DataOff_13TeV_25ns_2Steps.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', [], 1 ],
 		['DataOff_13TeV_25ns_dataScaled.root', 'Data_13TeV_Zee_25ns_Lkh1_scaled', 'MC_13TeV_Zee_25ns_Lkh1', ['debug=1'] ],
		#mesure avec electron tight
		['DataOff_13TeV_25ns_ID.root', 'Data_13TeV_Zee_25ns_Lkh2', 'MC_13TeV_Zee_25ns_Lkh2', [] ],
		#bkg
#		['DataOff_13TeV_25ns_EW.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_bkg_25ns_Lkh1', [] ],
		#mesure avec masse sueil Off0
		['DataOff_13TeV_25ns_Threshold.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', ['thresholdMass=75']],
		#mesure avec fenetre masse plus faible
		['DataOff_13TeV_25ns_Window.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1', ['ZMassMin=82.5', 'ZMassMax=97.5'] ],
		#mesure avec fBrem
 		['DataOff_13TeV_25ns_fBrem.root', 'Data_13TeV_Zee_25ns_Lkh1_fBrem70', 'MC_13TeV_Zee_25ns_Lkh1_fBrem70', [ ]],
		#Mesure avec ID
		['DataOff_13TeV_25ns_IDEff.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1_IDSyst', []],
		['DataOff_13TeV_25ns_recoEff.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1_recoSyst', []],
		['DataOff_13TeV_25ns_isoEff.root', 'Data_13TeV_Zee_25ns_Lkh1', 'MC_13TeV_Zee_25ns_Lkh1_isoSyst', []],

		['DataOff_13TeV_25ns_noIso.root', 'Data_13TeV_Zee_25ns_Lkh1_noIso', 'MC_13TeV_Zee_25ns_Lkh1_noIso', []],

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
		# ['TestSame.root', 'MC_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1', ['etaBins=ETA6','doSmearing=0', 'optimizeRanges=0', 'alphaMin=0', 'alphaMax=0.05', 'nUseEl=1'], 0 ],
		# ['TestIBL.root', 'MC_13TeV_Zee_25nsb_IBL_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1', ['etaBins=ETA6','doSmearing=0', 'optimizeRanges=0', 'alphaMin=0', 'alphaMax=0.05', 'nUseEl=1'], 0 ],
	        # ['DataOff_13TeV_25ns_mat_6Bins.root', 'MC_13TeV_Zee_25nsb_IBL_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1', ['etaBins=ETA6','doSmearing=0'], 0 ],
	        # ['DataOff_13TeV_25ns_mat.root', 'MC_13TeV_Zee_25nsb_IBL_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1', ['doSmearing=0'], 0 ],
		# ['DataOff_13TeV_25ns_rel201_6Bins.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1', ['etaBins=ETA6'], 0 ],
		# ['DataOff_13TeV_25ns_rel201_IBL_6Bins.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_IBL_Lkh1', ['etaBins=ETA6'], 0 ],
		# ['DataOff_13TeV_25ns_rel201_24Bins.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1', ['etaBins=ETA24'], 0 ],
		# ['DataOff_13TeV_25ns_rel201_IBL_24Bins.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_IBL_Lkh1', ['etaBins=ETA24'], 0 ],
		['DataOff_13TeV_25ns_rel201.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1', [], 3 ],
		['DataOff_13TeV_25ns_rel201_IBL.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_IBL_Lkh1', [], 3 ],
		# ['DataOff_13TeV_25ns_rel201_2Steps.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1', [], 1 ],
		# ['DataOff_13TeV_25ns_rel201_IBL_2Steps.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_IBL_Lkh1', [], 1 ],
		# ['DataOff_13TeV_25ns_rel201_2Steps_24ins.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_Lkh1', ['etaBins=ETA24'], 1 ],
		# ['DataOff_13TeV_25ns_rel201_IBL_2Steps_24Bins.root', 'Data_13TeV_Zee_25nsb_Lkh1', 'MC_13TeV_Zee_25nsb_IBL_Lkh1', ['etaBins=ETA24'], 1 ],
#		['Test2VAR1.root', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_PassSel', 'MC_13TeV_Zee_50ns_Lkh1_PairEvents_RejSel', ['alphaSimEta=0.005 0.005 0.005 0.005 0.005 0.005', 'alphaSimPt=0 0 0 0 0', 'sigmaSimAlpha=0 0 0 0 0', 'sigmaSimEta=0 0 0 0 0 0', 'sigmaSimPt=0 0 0 0 0', 'etaBins=ETA6', 'doSmearing=0', 'ptBins=0 50000 100000 150000 200000 1000000', "var2=PT", "mode=2VAR", 'debug=1' ], 0, 1 ],
		]	

spsPath="/sps/atlas/c/cgoudet/Calibration/PreRec/"
logPath="Log/"

for confFile in range( 0, len( configFiles ) ) :
	if  len( configFiles[confFile] ) > 4 : mode = configFiles[confFile][4]
	else : mode = 0
	launcherFile=CreateLauncher( configFiles[confFile], mode, "" )
	
	logFile = StripString( configFiles[confFile][0] )
	
	launchLine='~/sub28.sh ' + logFile + ' ' \
	    + spsPath + logPath + logFile + '.log ' \
	    + spsPath + logPath + logFile + '.err ' \
	    + launcherFile

	os.system( launchLine )
