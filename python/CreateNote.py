import os
import sys
from Functions_MeasureAlphaSigma import *

for option in sys.argv:
    if option == 'CreateNote.py' : continue


    dumFile = '/sps/atlas/c/cgoudet/dum/'
    os.system( 'mkdir ' + dumFile )
    os.chdir( dumFile  )
    commandLine = ( 'MeasureScale --config /sps/atlas/c/cgoudet/Calibration/Closure/Config24.boost '
                    + ' --loadFull ' + option 
                    + ' --noExtraction '
                    + ' --outFileName ' + StripName( option, 1, 0 )
                    + ' --makePlot ' 
                )
    os.system( commandLine )
    os.system( 'cp ' + StripName( option ) + '.pdf /sps/atlas/c/cgoudet/Plots/.' )
    os.system( 'rm -r ' + dumFile ) 
