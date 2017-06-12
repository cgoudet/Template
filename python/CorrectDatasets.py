import os

path='/sps/atlas/a/aguerguichon/Calibration/PreRec/'
dataPath='/sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/'

# data15 = os.popen( 'ls /sps/atlas/a/aguerguichon/Calibration/DataxAOD/Data_13TeV_Zee_25ns_Lkh1_scaled/Data_*.root' ).read().split()
# dataFiles = os.popen( 'ls /sps/atlas/a/aguerguichon/Calibration/DataxAOD/Data_13TeV_Zee_25ns_Lkh1/Data_*.root' ).read().split()
# MCScaledFiles = os.popen( 'ls /sps/atlas/a/aguerguichon/Calibration/DataxAOD/MC_13TeV_Zee_25ns_Lkh1_scaled/MC_*.root' ).read().split()
# MCFiles = os.popen( 'ls /sps/atlas/a/aguerguichon/Calibration/DataxAOD/MC_13TeV_Zee_25ns_Lkh1/MC_*.root' ).read().split()
# dataCorrectedFiles = os.popen( 'ls ' + path + 'Data_*corrected.root | grep -v scaled' ).read().split()


#print ' --dataFileName '.join( dataFiles )
#command= 'MeasureScale --configFile ~/private/Calibration/Template/python/Config25_noAlpha.boost --noExtraction '

command= 'MeasureScale --noExtraction --correctAlphaFileName '+path+'Results/CorrectedData/DeltaSummer.root'

#nominal
os.system( command
           + ' --configFile '+path+'Config/AlphaOffSummer_15_noDeadCells.boost'
           + ' --dataFileName '+dataPath+'Latest/data15.root'
           + ' --dataTreeName CollectionTree'
           + ' --correctAlphaHistName delta_Nom_noDead'
           )
os.system( 'mv '+dataPath+'NominalZeeSelection/data15*corrected.root '+path+'Results/CorrectedData/data15_noDead_corrected.root' )

# #EW
# os.system( command
#            + ' --configFile '+path+'Config/AlphaOffSummer_15.boost'
#            + ' --dataFileName '+dataPath+'NominalZeeSelection/data15.root'
#            + ' --dataTreeName CollectionTree'
#            + ' --correctAlphaHistName delta_EW'
#            )
# os.system( 'mv '+dataPath+'NominalZeeSelection/data15*corrected.root '+path+'Results/CorrectedData/data15_EW_corrected.root' )

# #noIsoCut
# os.system( command
#            + ' --configFile '+path+'Config/AlphaOffSummer_15_noIsoCut.boost'
#            + ' --dataFileName '+dataPath+'NoElectronIsolationCut/data15_noIsoCut.root'
#            + ' --dataTreeName CollectionTree'
#            + ' --correctAlphaHistName delta_noIsoCut'
#            )
# os.system( 'mv '+dataPath+'NoElectronIsolationCut/data15*corrected.root '+path+'Results/CorrectedData/.')

# #tightID
# os.system( command
#            + ' --configFile '+path+'Config/AlphaOffSummer_15_tightID.boost'
#            + ' --dataFileName '+dataPath+'TightElectronID/data15_tightID.root'
#            + ' --dataTreeName CollectionTree'
#            + ' --correctAlphaHistName delta_tightID'
#            )
# os.system( 'mv '+dataPath+'TightElectronID/data15*corrected.root '+path+'Results/CorrectedData/.')

# #Threshold
# os.system( command
#            + ' --configFile '+path+'Config/AlphaOffSummer_15_Threshold.boost'
#            + ' --dataFileName '+dataPath+'NominalZeeSelection/data15.root'
#            + ' --dataTreeName CollectionTree'
#            + ' --correctAlphaHistName delta_Threshold'
#            )
# os.system( 'mv '+dataPath+'NominalZeeSelection/data15_corrected.root '+path+'Results/CorrectedData/data15_Threshold_corrected.root' )

# #Window
# os.system( command
#            + ' --configFile '+path+'Config/AlphaOffSummer_15_Window.boost'
#            + ' --dataFileName '+dataPath+'NominalZeeSelection/data15.root'
#            + ' --dataTreeName CollectionTree'
#            + ' --correctAlphaHistName delta_Window'
#            )
# os.system( 'mv '+dataPath+'NominalZeeSelection/data15_corrected.root '+path+'Results/CorrectedData/data15_Window_corrected.root' )

# #fBrem
# os.system( command
#            + ' --configFile '+path+'Config/AlphaOffSummer_15_fBrem50.boost'
#            + ' --dataFileName '+dataPath+'NominalZeeSelection/data15_fBrem.root'
#            + ' --dataTreeName PassSelTree'
#            + ' --correctAlphaHistName delta_fBrem'
#            )
# os.system( 'mv '+dataPath+'NominalZeeSelection/data15*corrected.root '+path+'Results/CorrectedData/.' )

