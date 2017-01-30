import os


os.system('MeasureScale --configFile /sps/atlas/a/aguerguichon/Calibration/PreRec/Config/Scales_eos_1516.boost --dataFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/data15_Zee.root --dataFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/data16_Zee.root  --MCFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/mc_Zee.root --outFileName test.root --MCTreeName CollectionTree --dataTreeName CollectionTree --dataTreeName CollectionTree')

#os.system('MeasureScale --configFile /sps/atlas/a/aguerguichon/Calibration/PreRec/Config/AlphaOff_15.boost --dataFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/Data15_13TeV_Zee_noGain_Lkh1/Data15_13TeV_Zee_noGain_Lkh1.root   --MCFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/MC15c_13TeV_Zee_2015_noGain_Lkh1/MC15c_13TeV_Zee_2015_noGain_Lkh1.root --outFileName test2.root ')
