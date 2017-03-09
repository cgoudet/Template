import os



#os.system('MeasureScale --noExtraction --correctAlphaFileName /sps/atlas/a/aguerguichon/Calibration/PreRec/Results/CorrectedData/Deltaeos.root --correctAlphaHistName delta_eos_Window --dataFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/data15_Zee.root --configFile /sps/atlas/a/aguerguichon/Calibration/PreRec/Config/Scales_eos_15_Window.boost --dataTreeName CollectionTree')

os.system('GenerateToyTemplates --configFile /sps/atlas/a/aguerguichon/Calibration/Bias/Toys/Config/TreeToyTemplates_540046800.boost --dataFileName /sps/atlas/a/aguerguichon/Calibration/Test/MC15c_13TeV_Zee_noGain_Lkh1_evenEvents.root --MCFileName /sps/atlas/a/aguerguichon/Calibration/Test/MC15c_13TeV_Zee_noGain_Lkh1_oddEvents.root --inputC 0.007 --inputStat 1000000 --nIteration 2 --toyNumber 0  --outFileName test.root')

