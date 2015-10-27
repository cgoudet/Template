import os
import sys
from Functions_MeasureAlphaSigma import *

directory='280614'

command = 'ls ' + '/sps/atlas/c/cgoudet/Calibration/ScaleResults/' + directory + '/Data6_2*.root' 
inFileRun = os.popen( command ).read().split( '\n' )

for iVar in range( 0, 2 ) :

    with open( '/afs/in2p3.fr/home/c/cgoudet/private/Codes/PlotFunctions/Inputs/Scales/ScalesOverTime_' + ( 'alpha' if iVar else 'c' ) + '.boost' , 'w') as plotFile :
        plotFile.write( 'inputType=6\n' )
        for file in inFileRun :
            if file == '' or 'Template' in file :
                continue
            plotFile.write( 'rootFileName=' + file + '\n' )
            plotFile.write( 'objName=measScale_' + ( 'alpha' if iVar else 'c' ) + '\n' )
            plotFile.write( 'legend=' + StripName( file ).split('.')[0].split('_')[1] + '\n' )
        plotFile.write( 'latex=Data 13TeV 25ns, with pre-rec \n latexOpt=0.15 0.15' )
