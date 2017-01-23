import os

path='/sps/atlas/a/aguerguichon/Calibration/PreRec/'
dataPath='/sps/atlas/a/aguerguichon/Calibration/DataxAOD/'
dataset='Data15_13TeV_Zee_noGain_Lkh1'

# data15 = os.popen( 'ls /sps/atlas/a/aguerguichon/Calibration/DataxAOD/Data_13TeV_Zee_25ns_Lkh1_scaled/Data_*.root' ).read().split()
# dataFiles = os.popen( 'ls /sps/atlas/a/aguerguichon/Calibration/DataxAOD/Data_13TeV_Zee_25ns_Lkh1/Data_*.root' ).read().split()
# MCScaledFiles = os.popen( 'ls /sps/atlas/a/aguerguichon/Calibration/DataxAOD/MC_13TeV_Zee_25ns_Lkh1_scaled/MC_*.root' ).read().split()
# MCFiles = os.popen( 'ls /sps/atlas/a/aguerguichon/Calibration/DataxAOD/MC_13TeV_Zee_25ns_Lkh1/MC_*.root' ).read().split()
# dataCorrectedFiles = os.popen( 'ls ' + path + 'Data_*corrected.root | grep -v scaled' ).read().split()


#print ' --dataFileName '.join( dataFiles )
#command= 'MeasureScale --configFile ~/private/Calibration/Template/python/Config25_noAlpha.boost --noExtraction '
command= 'MeasureScale --noExtraction --correctAlphaFileName '+path+'Results/CorrectedData/Delta.root '


# os.system( command
#            + ' --configFile '+path+'Config/AlphaOff_15.boost'
#            + ' --dataFileName '+dataPath+dataset+'/Data15*.root'
#            + ' --correctAlphaHistName delta_Nom'
#            )
# os.system( 'mv '+dataPath+dataset+'/Data15*corrected.root '+path+'Results/CorrectedData/' )

# os.system( command
#            + ' --configFile '+path+'Config/AlphaOff_15_ID.boost'
#            + ' --dataFileName '+dataPath+dataset.replace('Lkh1','Lkh2')+'/Data15*.root'
#            + ' --correctAlphaHistName delta_ID'
#            )
# os.system( 'mv '+dataPath+dataset.replace('Lkh1', 'Lkh2')+'/Data15*corrected.root '+path+'Results/CorrectedData/' )

# os.system( command
#            + ' --configFile '+path+'Config/AlphaOff_15_Threshold.boost'
#            + ' --dataFileName '+dataPath+dataset+'/Data15*.root'
#            + ' --correctAlphaHistName delta_Threshold'
#            )
# os.system( 'mv '+dataPath+dataset+'/Data15*corrected.root '+path+'Results/CorrectedData/'+dataset+'_Threshold_corrected.root' )

# os.system( command
#            + ' --configFile '+path+'Config/AlphaOff_15_Window.boost'
#            + ' --dataFileName '+dataPath+dataset+'/Data15*.root'
#            + ' --correctAlphaHistName delta_Window'
#            )
# os.system( 'mv '+dataPath+dataset+'/Data15*corrected.root '+path+'Results/CorrectedData/'+dataset+'_Window_corrected.root' )

# os.system( command
#            + ' --configFile '+path+'Config/AlphaOff_15_noIso.boost'
#            + ' --dataFileName '+dataPath+dataset+'_doIso0/Data15*.root'
#            + ' --correctAlphaHistName delta_doIso0'
#            )
# os.system( 'mv '+dataPath+dataset+'_doIso0/Data15*corrected.root '+path+'Results/CorrectedData/')

os.system( command
           + ' --configFile '+path+'Config/AlphaOff_15_fBrem.boost'
           + ' --dataFileName '+dataPath+dataset+'_fBrem70/Data15*.root'
           + ' --correctAlphaHistName delta_fBrem70'
           )
os.system( 'mv '+dataPath+dataset+'_fBrem70/Data15*corrected.root '+path+'Results/CorrectedData/')
#os.system( 'mv '+dataPath+dataset+'_fBrem70/Data15*corrected.root .')

         
# execution = ( command + ' --dataFileName ' + ' --dataFileName '.join( dataFiles ) 
#               + ' --MCFileName ' + ' --MCFileName '.join( MCFiles ) 
#               + ' --correctAlphaFileName ' + path + 'DataOff_13TeV_25ns.root --correctAlphaHistName measScale_alpha '
#               + ' --correctSigmaFileName ' + path + 'DataOff_13TeV_25ns_c24.root --correctSigmaHistName measScale_c '
#               + '\n'
#               + 'mv ' + ' '.join( [ x.replace( '.root', '_corrected.root' ) for x in dataFiles ] ) + ' '
#               + ' '.join( [ x.replace( '.root', '_corrected.root' ) for x in MCFiles ] ) + ' '
#               + path + '. \n'
#               + command  + ' --dataFileName ' + ' --dataFileName '.join( data15 ) 
#               + ' --MCFileName ' + ' --MCFileName '.join( MCScaledFiles ) 
#               + ' --correctAlphaFileName ' + path + 'DataOff_13TeV_25ns_dataScaled.root --correctAlphaHistName measScale_alpha '
#               + ' --correctSigmaFileName ' + path + 'DataOff_13TeV_25ns_dataScaled_c24.root --correctSigmaHistName measScale_c '
#               + '\n'
#               + 'mv ' + ' '.join( [ x.replace( '.root', '_corrected.root' ) for x in data15 ] ) + ' '
#               + ' '.join( [ x.replace( '.root', '_corrected.root' ) for x in MCScaledFiles ] ) + ' '
#               + path + '. \n'
#               + '\n' )

              
# print execution
# os.system( execution )

