#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
import argparse
import subprocess as sub
import os
import sys
sys.path.append(os.path.abspath("/afs/in2p3.fr/home/c/cgoudet/private/Calibration/PlotFunctions/python"))
from SideFunction import *

"""
Argument parser script example. 
Much more details at https://docs.python.org/2/howto/argparse.html
and at https://github.com/paris-swc/python-packaging
"""


plotID={}
plotID['nominal']='DataOff_13TeV_25ns'
plotID['residual']='DataOff_13TeV_25ns_dataScaled'
plotID['totSyst'] = ''
plotID['fBremSyst'] = 'DataOff_13TeV_25ns_fBrem'
plotID['ThresholdSyst'] = 'DataOff_13TeV_25ns_Threshold'
plotID['WindowSyst'] = 'DataOff_13TeV_25ns_Window'
plotID['IDSyst'] = 'DataOff_13TeV_25ns_ID'
plotID['EWSyst'] = 'DataOff_13TeV_25ns_EW'

# Modes :
# 0 : central values only
# 1 : central values + systematics

def getSyst() :
    result = []
    for plotName in plotID :
        if not 'Syst' in plotName : continue
        if plotName == 'totSyst' : continue
        result.append(plotName)
    return result

#===============================================
def createSystematicFile( directory, var, model=0 ) :
    outFile = directory + 'systematics_' + ( 'c' if var else 'alpha' ) + '.txt'
    systFile = open( outFile, 'w' )
    systFile.write( directory + 'EnergyScaleFactors.root totSyst_' + ('c' if var else 'alpha') + ' dum\n' )
    systFile.write( directory + plotID['nominal'] + ( '_c24' if var else '' ) + '.root measScale_' + ' centVal_'.join( [('c' if var else 'alpha')]*2 ) + '\n' )

    systFile.write( '\n'.join( [ 
                directory + plotID[plotName] + ( '_c24' if var else '' ) + '.root measScale_' + (' ' + plotName.replace('Syst', '_' )).join( [('c' if var else 'alpha')]*2 ) 
                for plotName in getSyst() ] )
                    + '\n' )

    return outFile

#=============================================
def createLatex( directory, introFiles=[], concluFiles=[] ) :
    latexFileName = directory + 'latex.tex'
    print( 'latexFileName : ', latexFileName )
    latex = open( latexFileName, "w" )

    latex.write( LatexHeader( 'Central electron energy scale factors and resolution constant term', 'Electron scale factors' ) )

    for input in introFiles : 
        with open( input ) as intro :
            for line in intro : latex.write( line + '\n' )


    slideText = {}
    for name in plotID : slideText[name]=''
    slideText['nominal'] = ( 'Scales are measured with 2015 13TeV data at 25ns : \n'
                             + '\\begin{itemize}\item Data are {\\bf not} corrected with energy scale from pre-recommandations, '
                             + '\\item MC is {\\bf not }smeared with pre-rec.\\end{itemize}'
                             )
    slideText['residual'] = ( 'Scales are measured with 2015 13TeV data at 25ns : \n'
                             + '\\begin{itemize}\item Data are corrected with energy scale from pre-recommandations + tempetature, '
                             + '\\item MC is {\\bf not }smeared with pre-rec.\\end{itemize}'
                             )

    orderedList = ['nominal', 'residual', 'totSyst' ] + getSyst()
    latex.write( '\n'.join( 
            [drawMinipage([plotName+var+'.pdf' for var in ['_alpha', '_c'] ], plotName[0].upper() + plotName[1:], slideText[plotName] )
             for plotName in orderedList
             ]
            )
                 )


    for input in concluFiles : 
        with open( input ) as conclu :
            for line in conclu : latex.write( line + '\n' )

    latex.write( '\\end{document}' )
    latex.close()
    return latexFileName

#=========================================
def createBoost( directory, var, ID, options={} ):
#    content = sub.check_output( ['ls ' + directory ],  shell=1, stderr=sub.STDOUT )
#    print(content)

#Defining variables used in the boost files
    boostFile= directory + ID + '_' + ( 'alpha' if var==0 else 'c' ) + '.boost'
    print( 'ID=', ID )
    options = {}
    options['rootFileName'] = []
    options['objName'] = []
    options['loadFiles'] = [ directory + 'Label.txt']
    options['legend']=[]

    optionsUnique = {}
    optionsUnique['inputType']=0

    options['rootFileName'].append(directory+plotID[ID] + ( '' if var==0 else '_c24' ) + '.root' )

    if ID =='residual' : #PreRec
        if not var : optionsUnique['line']='0'
    elif ID == 'totSyst' :
        systs = getSyst()
        options['rootFileName'] =  [directory + 'EnergyScaleFactors.root']*(len( systs )+1)
        options['objName'].append( 'totSyst_' + ( 'c' if var else 'alpha' ) )
        options['legend'].append( 'totSyst' )
        options['objName'] += [ 'syst_' + plotName.replace('Syst', '' ) + '_' + ( 'c' if var else 'alpha' ) for plotName in systs]
        options['legend'] += [ plotName.replace('Syst', '' ) for plotName in systs ]

    elif ID in getSyst() :
        options['rootFileName'].append( directory+plotID['nominal'] + ( '' if var==0 else '_c24' ) + '.root' )
        options['rootFileName'].reverse()
        options['legend']=['nominal', ID.replace('Syst', '' ) ]
        optionsUnique['doRatio']=1
        optionsUnique['extendUp']=0.4

#Defining default cases of options if not defined
    if not len( options['objName'] ) : options['objName'] = [ 'measScale_' + ( 'alpha' if var==0 else 'c' ) for dum in range(0, len( options['rootFileName'] ) ) ]


    print('Print in file : ',boostFile )
    with open( boostFile, 'w+') as boost: 
        boost.write( '\n'.join( [ opt + '=' + it for opt in options for it in options[opt] ] ) + '\n' )
        boost.write( '\n'.join( [ opt + '=' + str(optionsUnique[opt]) for opt in optionsUnique] ) + '\n' )

    return boostFile 


#==========================================
def parseArgs():
    """
    ArgumentParser.

    Return
    ------
        args: the parsed arguments.
    """
    # First create a parser with a short description of the program.
    # The parser will automatically handle the usual stuff like the --help messages.
    parser = argparse.ArgumentParser(
        description="This text will be displayed when the -h or --help option are given"
                    "It should contain a short description of what this program is doing.")

    # Retrieve the optionnal arguments. Optional argument should start with '-' or '--'
    # Simply give to the parser.add_argument() function the expected names 
    # (one short '-' and/or one long '--')

    # The parser can cast the given arguments to some usual types and will return 
    # standard error message if the given argument is not of the good type.

    # Integers
    # Here I give the short and the long argument name
    parser.add_argument(
        '--doPlot', help='Tag for recreating plots',
        default=0, type=int )
    parser.add_argument(
        '--doSyst', help='Tag for recreating systematics histos and plots',
        default=0, type=int )

    # Floats
    # Here I give only the long argument name

    # Choices
    # Here is illustrated the possibility of having to choose between several values
    # Again help and error messages are automatically built.
    # Moreover when you do not precise the dest= argument it choose in order of priority
    # the long name and the short name (if the long one does not exist)
    parser.add_argument("--verbosity", "-v", type=int, choices=[0, 1, 2],
                    help="increase output verbosity")

    # Add an argument to handle the output file.  If we use argparse.FileType it will
    # handle opening a writeable file (and ensuring we can write to it).
    # (Note: the str argument follow teh standard names 
    #   'w'=write, 'r'=read, 'r+'= read and write, 'a'=append,
    # For Windows there is a distinction between text and binary files: use the 'b' option
    #   'rb'=read binary, 'wb'=write binary, 'r+b'= read and write, etc)
    # Note that the argument name 'file' does not beging with a '-' or '--'; this indicates
    # to argparse that it is a *positional* argument
    # Whoa 2 new things in a single example ! This is crazy !
    # parser.add_argument('file', type=argparse.FileType('w'),
    #                     help='the name of the output file')

    parser.add_argument('directory', type=str, help="Directory where all inputs are stored" )
    # Now do your job and parse my command line !
    args = parser.parse_args()

    return args

#========================================
def main():
    """
    The main script
    """
    # Parsing the command line arguments
    args = parseArgs()
    # Now args is a argparse.NameSpace object
    # It is basically a dictionnary in which you can access its element 
    # as attributes instead of the quite heavy args['entry_name'] dict way.

 #   print( "Parsed : ")
#    for opt in args.__dict__: print(opt, getattr(args, opt))

    if not '/' in args.directory : args.directory = '/sps/atlas/c/cgoudet/Calibration/ScaleResults/' + args.directory + '/'

    if args.doSyst :
        print('Creating Systematics')
        systematics = [ createSystematicFile( args.directory, var ) for var in range( 0, 2 ) ]
        #print(systematics)
        os.system( 'AddSyst ' + ' '.join( systematics ) )

    if args.doPlot :
        print('Creating boost files')
        filesToPlot = [ createBoost( args.directory, var, key ) for var in range( 0, 2 ) for key in plotID ]
        for boost in filesToPlot : 
            print( 'Creating plot ', boost )
            os.system( 'CompareHist ' + boost )

#    createLatex( args.directory )
    
    os.chdir( args.directory )
    latexFileName = createLatex( args.directory, '', '' )
    for i in range(0, 3) : os.system( 'pdflatex ' + latexFileName )
    os.system('pwd')

# The program entrance
if __name__ == '__main__':
    main()
