import os

os.system('MeasureScale --dataFileName /sps/atlas/a/aguerguichon/Calibration/Closure/pseudoData_both_distorted.root  --MCFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/mc_Zee.root --configFile /sps/atlas/a/aguerguichon/Calibration/PreRec/Config/Closure.boost --dataTreeName pseudoData_both_distorted --MCTreeName CollectionTree')

os.system('MeasureScale --dataFileName /sps/atlas/a/aguerguichon/Calibration/Closure/pseudoData_both_distorted.root  --MCFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/mc_Zee.root --configFile /sps/atlas/a/aguerguichon/Calibration/PreRec/Config/Closure_c.boost --dataTreeName pseudoData_both_distorted --MCTreeName CollectionTree --correctAlphaHistName measScale_alpha --correctAlphaFileName Closure.root')

#os.system('GenerateToyTemplates --configFile /sps/atlas/a/aguerguichon/Calibration/Bias/Toys/Config/TreeToyTemplates_545288104.boost --dataFileName /sps/atlas/a/aguerguichon/Calibration/Test/MC15c_13TeV_Zee_noGain_Lkh1_evenEvents.root --MCFileName /sps/atlas/a/aguerguichon/Calibration/Test/MC15c_13TeV_Zee_noGain_Lkh1_oddEvents.root --inputC 0 --inputStat 10000 --nIteration 1 --toyNumber 0  --outFileName test.root')

