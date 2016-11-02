#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

import subprocess as sub
import os
import sys
sys.path.append(os.path.abspath("/afs/in2p3.fr/home/a/aguergui/public/Calibration/PlotFunctions/python"))
from SideFunction import *

#=========================================
def createBoost( inFiles, var, ID, addOptions={} ):

#Defining variables used in the boost files
    options = {}
    options['rootFileName'] = inFiles
    options['objName'] = [ ID + '_' + var ]* len( options['rootFileName'] )
    options['legend'] = [ StripString( inFile ) for inFile in inFiles ]
    optionsUnique = {}
    optionsUnique['inputType']=0
    optionsUnique['plotDirectory'] = '/sps/atlas/a/aguerguichon/cgoudet/Plots/'
    optionsUnique['doTabular'] = 1
    optionsUnique['doRatio']=2

    if 'combin' in ID : 
        optionsUnique["yTitle"] = 'c' if var=='c' else '#alpha'
        optionsUnique['diagonalize']=1; 
        optionsUnique["clean"]= ( 100 if 'Err' in ID else 0 ); 
        optionsUnique['inputType']=7 
#Defining default cases of options if not defined
    for opt in addOptions : optionsUnique[opt]=addOptions[opt]

    boostFile = optionsUnique['plotDirectory'] + ID + '_' + var + '.boost'
    print('Print in file : ', boostFile )
    with open( boostFile, 'w+') as boost: 
        boost.write( '\n'.join( [ opt + '=' + it for opt in options for it in options[opt] ] ) + '\n' )
        boost.write( '\n'.join( [ opt + '=' + str(optionsUnique[opt]) for opt in optionsUnique] ) + '\n' )

    return boostFile 

#========================================
def main():

    args = parseArgs()

    boostFiles = [ createBoost( args.inFiles, var, ID ) for var in ['alpha', 'c'] for ID in ['measScale', 'combin', 'combinErr' ] ]
    os.system( 'CompareHist ' + ' '.join( boostFiles ) )
    print( boostFiles )

# The program entrance
if __name__ == '__main__':
    main()
