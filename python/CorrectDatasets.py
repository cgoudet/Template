import os

path='/sps/atlas/c/cgoudet/Calibration/ScaleResults/160213/'

dataScaledFiles = os.popen( 'ls /sps/atlas/c/cgoudet/Calibration/DataxAOD/Data_13TeV_Zee_25ns_Lkh1_scaled/Data_*.root' ).read().split()
dataFiles = os.popen( 'ls /sps/atlas/c/cgoudet/Calibration/DataxAOD/Data_13TeV_Zee_25ns_Lkh1/Data_*.root' ).read().split()
MCScaledFiles = os.popen( 'ls /sps/atlas/c/cgoudet/Calibration/DataxAOD/MC_13TeV_Zee_25ns_Lkh1_scaled/MC_*.root' ).read().split()
MCFiles = os.popen( 'ls /sps/atlas/c/cgoudet/Calibration/DataxAOD/MC_13TeV_Zee_25ns_Lkh1/MC_*.root' ).read().split()


#print ' --dataFileName '.join( dataFiles )
command='MeasureScale --configFile ~/private/Calibration/Template/ConfigFiles/Config6.boost --noExtraction '


execution = ( command + ' --dataFileName ' + ' --dataFileName '.join( dataFiles ) 
              + ' --MCFileName ' + ' --MCFileName '.join( MCFiles ) 
              + ' --correctAlphaFileName ' + path + 'DataOff_13TeV_25ns_68Bins.root --correctAlphaHistName measScale_alpha '
              + ' --correctSigmaFileName ' + path + 'DataOff_13TeV_25ns_68Bins.root --correctSigmaHistName measScale_c '
              + '\n'
              + 'mv ' + ' '.join( [ x.replace( '.root', '_corrected.root' ) for x in dataFiles ] ) + ' '
              + ' '.join( [ x.replace( '.root', '_corrected.root' ) for x in MCFiles ] ) + ' '
              + path + '. \n'
              + command + ' --dataFileName ' + ' --dataFileName '.join( dataScaledFiles ) 
              + ' --MCFileName ' + ' --MCFileName '.join( MCScaledFiles ) 
              + ' --correctAlphaFileName ' + path + 'DataOff_13TeV_25ns_dataScaled.root --correctAlphaHistName measScale_alpha '
              + ' --correctSigmaFileName ' + path + 'DataOff_13TeV_25ns_dataScaled.root --correctSigmaHistName measScale_c '
              + '\n'
              + 'mv ' + ' '.join( [ x.replace( '.root', '_corrected.root' ) for x in dataScaledFiles ] ) + ' '
              + ' '.join( [ x.replace( '.root', '_corrected.root' ) for x in MCScaledFiles ] ) + ' '
              + path + '. \n'
              + '\n' )
print execution
os.system( execution )

