#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function

import subprocess as sub
import os
import sys
sys.path.append(os.path.abspath("/afs/in2p3.fr/home/c/cgoudet/private/Calibration/PlotFunctions/python"))
from SideFunction import *



#=============================================
def createLatex( directory, introFiles=[], concluFiles=[] ) :
    latexFileName = directory + 'latex.tex'
    # print( 'latexFileName : ', latexFileName )
    # latex = open( latexFileName, "w" )

    # latex.write( LatexHeader( 'Central electron energy scale factors and resolution constant term', 'Electron scale factors' ) )

    # for input in introFiles : 
    #     with open( input ) as intro :
    #         for line in intro : latex.write( line + '\n' )


    # slideText = {}
    # for name in plotID : slideText[name]=''
    # slideText['nominal'] = ( 'Scales are measured with 2015 13TeV data at 25ns : \n'
    #                          + '\\begin{itemize}\item Data are {\\bf not} corrected with energy scale from pre-recommandations, '
    #                          + '\\item MC is {\\bf not }smeared with pre-rec.\\end{itemize}'
    #                          )
    # slideText['residual'] = ( 'Scales are measured with 2015 13TeV data at 25ns : \n'
    #                          + '\\begin{itemize}\item Data are corrected with energy scale from pre-recommandations + tempetature, '
    #                          + '\\item MC is {\\bf not }smeared with pre-rec.\\end{itemize}'
    #                          )

    # orderedList = ['nominal', 'residual' ]
    # latex.write( '\n'.join( 
    #         [drawMinipage([plotName+var+'.pdf' for var in ['_alpha', '_c'] ], plotName[0].upper() + plotName[1:], slideText[plotName] )
    #          for plotName in orderedList
    #          ]
    #         )
    #              )

    # latex.write( '\n' )
    # latex.write( drawMinipage( ['correction_m12.pdf'], 'Correction', slideText['correction'] ) )


    # orderedList = ( ['totSyst'] if 'totSyst' in plotID else [] ) + getSyst()
    # latex.write( '\n'.join( 
    #         [drawMinipage([plotName+var+'.pdf' for var in ['_alpha', '_c'] ], plotName[0].upper() + plotName[1:], slideText[plotName] )
    #          for plotName in orderedList
    #          ]
    #         )
    #              )

    # for input in concluFiles : 
    #     with open( input ) as conclu :
    #         for line in conclu : latex.write( line + '\n' )

    # latex.write( '\\end{document}' )
    # latex.close()
    # return latexFileName




#=========================================
def createBoost( inFiles, var, ID, addOptions={} ):

#Defining variables used in the boost files
    options = {}
    options['rootFileName'] = inFiles
    options['objName'] = [ ID + '_' + ( 'c' if var else 'alpha' ) ]* len( options['rootFileName'] )
    options['legend'] = [ StripString( inFile ) for inFile in inFiles ]
    optionsUnique = {}
    optionsUnique['inputType']=0
    optionsUnique['plotDirectory'] = '/sps/atlas/c/cgoudet/Plots/'
    optionsUnique['doTabular'] = 1

    if 'combin' in ID : optionsUnique['inputType']=7 
        
#Defining default cases of options if not defined
    for opt in addOptions : optionsUnique[opt]=addOptions[opt]

    boostFile = ID + '_' + ( 'c' if var else 'alpha' ) + '.boost'
    print('Print in file : ', boostFile )
    with open( boostFile, 'w+') as boost: 
        boost.write( '\n'.join( [ opt + '=' + it for opt in options for it in options[opt] ] ) + '\n' )
        boost.write( '\n'.join( [ opt + '=' + str(optionsUnique[opt]) for opt in optionsUnique] ) + '\n' )

    return boostFile 

#========================================
def main():

    args = parseArgs()

    boostFiles = [ createBoost( args.inFiles, var, ID ) for var in range(0, 2) for ID in ['measScale', 'combin', 'combinErr' ] ]
    os.system( 'CompareHist ' + ' '.join( boostFiles ) )
    print( boostFiles )

# The program entrance
if __name__ == '__main__':
    main()
