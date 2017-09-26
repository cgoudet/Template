import os

 # os.system('MeasureScale --dataFileName /sps/atlas/a/aguerguichon/Calibration/Closure/pseudoData_distorted.root  --MCFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/mc_Zee.root --configFile /sps/atlas/a/aguerguichon/Calibration/PreRec/Config/Closure.boost --dataTreeName pseudoData_distorted --MCTreeName CollectionTree --outFileName /sps/atlas/a/aguerguichon/Calibration/Test/Closure.root')


os.system('MeasureScale --dataFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/Latest/data15.root  --MCFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/NominalZeeSelection/mcZee.root --configFile /sps/atlas/a/aguerguichon/Calibration/PreRec/Config/Test.boost --dataTreeName CollectionTree --MCTreeName CollectionTree  --outFileName /sps/atlas/a/aguerguichon/Calibration/Test/Test_noDeadCells.root')

#os.system('GenerateToyTemplates --configFile /sps/atlas/a/aguerguichon/Calibration/Bias/Toys/Config/TreeToyTemplates_577138850.boost --dataFileName /sps/atlas/a/aguerguichon/Calibration/Closure/mc_Zee_evenEvents.root --MCFileName /sps/atlas/a/aguerguichon/Calibration/Closure/mc_Zee_oddEvents.root --inputC 0 --inputStat 10000 --nIteration 1 --toyNumber 0  --outFileName /sps/atlas/a/aguerguichon/Calibration/test.root')
