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
plotID['correction']=''
plotID['totSyst'] = ''
plotID['fBremSyst'] = 'DataOff_13TeV_25ns_fBrem'
plotID['ThresholdSyst'] = 'DataOff_13TeV_25ns_Threshold'
plotID['WindowSyst'] = 'DataOff_13TeV_25ns_Window'
plotID['IDSyst'] = 'DataOff_13TeV_25ns_ID'
plotID['recoEffSyst'] = 'DataOff_13TeV_25ns_recoEff'
plotID['isoEffSyst'] = 'DataOff_13TeV_25ns_isoEff'
plotID['IDEffSyst'] = 'DataOff_13TeV_25ns_IDEff'
plotID['noIsoSyst'] = 'DataOff_13TeV_25ns_noIso'
plotID['matSyst'] = ''
#plotID['EWSyst'] = 'DataOff_13TeV_25ns_EW'

# Modes :
# 0 : central values only
# 1 : central values + systematics

def listFiles( directory ):
    output = sub.check_output( ['ls '+ directory ],  shell=1, stderr=sub.STDOUT ) 
    if '\n' in output : content = output.split() 
    else : content = [ output ]
    return content

#===============================================================
def applyCorrection( directory ) :

    commandLine = 'MeasureScale --configFile /afs/in2p3.fr/home/c/cgoudet/private/Calibration/Template/python/DataOff_13TeV_25ns.boost --noExtraction '
    commandLine += ' --dataFileName '.join( [''] + listFiles( '/sps/atlas/c/cgoudet/Calibration/DataxAOD/Data_13TeV_Zee_25ns_Lkh1/Data*.root' ) )
    commandLine += ' --MCFileName '.join( [''] + listFiles( '/sps/atlas/c/cgoudet/Calibration/DataxAOD/MC_13TeV_Zee_25ns_Lkh1/MC*.root' ) )
    commandLine += ' --correctAlphaHistName measScale_alpha --correctSigmaHistName measScale_c '
    commandLine += ' --correctAlphaFileName ' + directory + plotID['nominal'] + '.root'
    commandLine += ' --correctSigmaFileName ' + directory + plotID['nominal'] + '.root'
    os.chdir( directory )
     
    os.system( commandLine )
    content = listFiles( '/sps/atlas/c/cgoudet/Calibration/DataxAOD/Data_13TeV_Zee_25ns_Lkh1/Data*.root' ) + listFiles( '/sps/atlas/c/cgoudet/Calibration/DataxAOD/MC_13TeV_Zee_25ns_Lkh1/MC*.root' )
    content = [ (f if 'corrected' in f else '' ) for f in content ]
    os.system( 'mv ' + ' '.join( content ) + ' ' + directory )
 

#===========================================
def getSyst() :
    result = []
    for plotName in plotID :
        if not 'Syst' in plotName : continue
        if plotName == 'totSyst' : continue
        result.append(plotName)
    return result

#===============================================
def createSystematicFile( directory, var, model=0 ) :
    output = []

    specialSyst = [  'matSyst' ]
    nominalSyst = [ syst  for syst in getSyst() if syst not in specialSyst  ]

    suffix = '_c' if var else ''
    outFile = directory + 'systematics_' + ( 'c' if var else 'alpha' ) + '.txt'
    systFile = open( outFile, 'w' )
    systFile.write( directory + 'EnergyScaleFactors.root totSyst_' + ('c' if var else 'alpha') + ' dum 0\n' )
    systFile.write( directory + plotID['nominal'] + suffix + '.root measScale_' + ' centVal_'.join( [('c' if var else 'alpha')]*2 ) + ' 0\n' )

    systFile.write( '\n'.join( [ 
                directory + plotID[plotName] + suffix + '.root measScale_' + (' ' + plotName.replace('Syst', '_' )).join( [('c' if var else 'alpha')]*2 ) + ' ' + str( model ) 
                for plotName in nominalSyst ] )
                    + '\n' )
    output.append( outFile )

    datasets = {}
#    datasets['fBremSyst'] = [ 'DataOff_13TeV_25ns_24Bins.root', 'DataOff_13TeV_25ns_fBrem.root' ]
    datasets['matSyst'] = [ 'DataOff_13TeV_25ns_rel201' + ( '_c' if var else '' ) +'.root', 'DataOff_13TeV_25ns_rel201_IBL' + ( '_c' if var else '') +'.root', str(model) ]

    for syst in specialSyst : 
        if not syst in plotID : continue
        outFile = directory + 'systematics_' + syst + '_' + ( 'c' if var else 'alpha' ) + '.txt'
        systFile = open( outFile, 'w+' )
        systFile.write( directory + 'EnergyScaleFactors.root totSyst_' + ('c' if var else 'alpha') + ' dum 0 \n' )
        systFile.write( directory + datasets[syst][0]  + ' measScale_' + ('c' if var else 'alpha') + ' dum 0 \n' )
        systFile.write( directory + datasets[syst][1] + ' measScale_' + (' ' + syst.replace('Syst', '_' )).join( [('c' if var else 'alpha')]*2 ) + ' ' + datasets[syst][2] + '\n' ) 
        systFile.close()
        output.append( outFile )

    return output

#=============================================
def createLatex( directory, introFiles=[], concluFiles=[] ) :
    latexFileName = directory + 'latex.tex'
    print( 'latexFileName : ', latexFileName )
    latex = open( latexFileName, "w" )

    latex.write( LatexHeader( 'Central electron energy scale factors and resolution constant term', 'Electron scale factors', 1 ) )

    for input in introFiles : 
        with open( input ) as intro :
            for line in intro : latex.write( line  )


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
    slideText['correction'] = ( 'The lineshape of the $Z$ is compared after application of 2015 corrections between data and MC.\n' )
    slideText['totSyst'] = ( 'Sources of uncertainty and their contribution in the total systematic uncertainty.\n For statistical reasons, uncertainties are symetrized along $\eta_{calo}$\n' )
    slideText['WindowSyst'] = 'Systematic defined as the difference between nominal measurement and reducing $Z$ mass range from $[80-100]$~GeV to $[82.5-97.5]$~GeV.\n'
    slideText['noIsoSyst'] = 'Systematic defined as the difference between nominal measurement and removing the isolation cut.\n'
    slideText['run1Syst'] = 'Comparison between current systematic model and run1 total systematic uncertainty\n.'
    slideText['IDSyst'] = 'Systematic defined as the difference between nominal measurement and Tight identification selection\n'
    slideText['fBremSyst' ] = 'Systematic defined as the difference between nominal measurement and an additional cut removing electrons with fBrem$>0.7$.\n'

    effSyst = [ syst for syst in getSyst() if 'EffSyst' in syst ]
    for syst in effSyst :
        effName = ''
        if syst == 'IDEffSyst' : effName = ' identification '
        elif syst == 'recoEffSyst' : effName = ' reconstruction '
        elif syst == 'isoEffSyst ' : effName = ' isolation '
        slideText[syst] = ( syst + ' is defined as the difference between nominal measurement and pulling the weight of ' + effName + ' efficiency scale factors for each electron one sigma up.\n' )

    orderedList = ['nominal', 'residual' ]
    latex.write( '\n'.join( 
            [drawMinipage([plotName+var+'.pdf' for var in ['_alpha', '_c'] ], plotName[0].upper() + plotName[1:], slideText[plotName] )
             for plotName in orderedList
             ]
            )
                 )

    latex.write( '\n' )
    latex.write( drawMinipage( ['correction_m12.pdf'], 'Correction', slideText['correction'] ) )


    latex.write( drawMinipage([ 'totSyst'+var+'.pdf' for var in ['_alpha', '_c'] ], 'Experimental Uncertaities', slideText['totSyst'] ) )
    latex.write( ' '.join( [drawTabular([ 'totSyst'+var+'.csv' for var in ['_alpha', '_c'] ], 'Experimental Uncertainties breakdown : $\\alpha$ \\& $c$ ' )  ] ) )
    latex.write( '\n'.join( 
            [drawMinipage([plotName+var+'.pdf' for var in ['_alpha', '_c'] ], plotName[0].upper() + plotName[1:], slideText[plotName] )
             for plotName in getSyst()
             ]
            )
                 )

    latex.write( '\n'.join( 
            [drawMinipage(['run1Syst'+var+'.pdf' for var in ['_alpha', '_c'] ], 'Run1 systematics', slideText[plotName] )
             ]
            )
                 )

    for input in concluFiles : 
        with open( input ) as conclu :
            for line in conclu : latex.write( line  )

    latex.write( '\\end{document}' )
    latex.close()
    return latexFileName

#=========================================
def createBoost( directory, var, ID, options={} ):
#    content = sub.check_output( ['ls ' + directory ],  shell=1, stderr=sub.STDOUT )
#    print(content)
    fileSuffix = '_c' if var else ''

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
    optionsUnique['plotDirectory']=directory
    options['rootFileName'].append( directory+plotID[ID] + fileSuffix + '.root' if ID in plotID else '' )


    if ID =='residual' : #PreRec
        varName = 'ctZee' if var else 'alpha0'
        options['rootFileName'] += ['/sps/atlas/c/cgoudet/Calibration/Run1/EnergyScaleFactors.root' ]*(1+var)
        options['rootFileName'].reverse()
        options['objName'].append( 'PreRecommandations/' + varName + '_prerec_errSyst' )
        options['legend'] .append('Pre-recommandations, syst. unc. __FILL __NOPOINT' )

        if var : 
            options['objName'].append( 'PreRecommandations/ctZee_prerec_errStat' )
            options['legend'].append( 'Pre-recommandations, stat. unc.' )
            optionsUnique['shiftColor']=-1
            # print( options['rootFileName'] ) 
            # exit(0)
        else :
            optionsUnique['line']='0'
            pass
        optionsUnique['legendPos'] = '0.55 0.9'
        options['legend'].append( 'Run2' )

    elif ID=='nominal' :
        print('nominal')
        varName = 'ctZee' if var else 'alphaTot'
        options['rootFileName'] += ['/sps/atlas/c/cgoudet/Calibration/Run1/EnergyScaleFactors.root' ]*2
        options['rootFileName'].reverse()
        options['objName'] += ['PreRecommandations/'+varName+'_prerec_errSyst', 'PreRecommandations/'+varName+'_prerec_errStat' ]
        options['legend']= [ 'Pre-recommandations, syst. unc. __FILL __NOPOINT', 'Pre-recommandations, stat. unc.', 'Run2' ]
        optionsUnique['shiftColor']=-1
        optionsUnique['legendPos'] = '0.55 0.9'

    elif ID == 'totSyst' :
        systs = getSyst()
        options['rootFileName'] =  [directory + 'EnergyScaleFactors.root']*(len( systs )+1)
        options['objName'].append( 'totSyst_' + ( 'c' if var else 'alpha' ) )
        options['legend'].append( 'totSyst' )
        options['objName'] += [ 'syst_' + plotName.replace('Syst', '' ) + '_' + ( 'c' if var else 'alpha' ) for plotName in systs]
        options['legend'] += [ plotName.replace('Syst', '' ) for plotName in systs ]
        optionsUnique['doTabular']=1

    # elif ID == "fBremSyst" :
    #     options['rootFileName'] = [ directory+'DataOff_13TeV_25ns_24Bins.root', directory+'DataOff_13TeV_25ns_fBrem.root' ]
    #     options['legend']=['nominal 24Bins', ID.replace('Syst', '' ) ]
    #     optionsUnique['doRatio']=2
    elif ID in getSyst() :
        options['rootFileName'].append( directory+plotID['nominal'] + fileSuffix + '.root' )
        options['rootFileName'].reverse()
        options['legend']=['nominal', ID.replace('Syst', '' ) ]
        optionsUnique['doRatio']=2
        optionsUnique['extendUp']=0.4

    elif ID == 'correction' : 
        options['rootFileName']=[ ' '.join( listFiles( directory + varName + '_*corrected.root' ) ) for varName in ['MC','Data'] ] 
        options['objName'] = [ ( 'corrected'+ ( 'MC' if 'MC_' in option else 'Data' ) + ' ' ) * len( option.split(' ') ) for option in options['rootFileName']  ]
        options['legend'] = [ 'MC', 'Data' ]
        optionsUnique['inputType']=1   
        boostFile= directory +'correction.boost'
        options['varName'] = [ 'm12']
        options['varMin'] = [ '70' ]
        options['varMax'] = [ '110' ]
        optionsUnique['nComparedEvents'] = 40
        optionsUnique['normalize']=1
        optionsUnique['doRatio']=1
    elif ID == 'run1Syst' :
        options['rootFileName'] = ['/sps/atlas/c/cgoudet/Calibration/Run1/EnergyScaleFactors.root', directory+'EnergyScaleFactors.root']
        options['objName'] = [ 'Run1/' + ( 'ct' if var else 'alpha' ) + 'ErrZee_run1_totSyst', 'totSyst_' + ('c' if var else 'alpha') ]
        options['legend']= [ 'Run1', 'Run2' ]

#Defining default cases of options if not defined
    if len( options['objName'] ) < len( options['rootFileName'] ) : options['objName'] += [ 'measScale_' + ( 'alpha' if var==0 else 'c' )  ]*(len(options['rootFileName']) - len(options['objName']))


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
        '--doLatex', help='Tag for recreating plots',
        default=1, type=int )
    parser.add_argument(
        '--doSyst', help='Tag for recreating systematics histos and plots',
        default=1, type=int )
    parser.add_argument(
        '--doCorrection', help='Tag for recreating systematics histos and plots',
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

    if args.doCorrection :
        print('Doing correction')
        applyCorrection(args.directory)

    if args.doSyst :
        print('Creating Systematics')
        systematics = []
        for var in range( 0, 2 )  : systematics += createSystematicFile( args.directory, var, 20 ) 
        #print(systematics)
        os.system( 'AddSyst ' + ' '.join( systematics ) )

    if args.doPlot :
        print('Creating boost files')
        filesToPlot = list( set( [ createBoost( args.directory, var, key ) for var in range( 0, 2 ) for key in plotID ] ) )
        filesToPlot += [ createBoost( args.directory, var, 'run1Syst' ) for var in range(0,2) ]
        os.system( 'CompareHist ' + ' '.join( [ boost for boost in filesToPlot ] ) )



#    createLatex( args.directory )
    if args.doLatex :     
        os.chdir( args.directory )
        os.system('pwd')
        latexFileName = createLatex( args.directory, [ args.directory + 'intro.tex' ], [ args.directory + 'conclu.tex' ] )
#        for i in range(0, 3) : os.system( 'pdflatex ' + ( ' -interaction=batchmode ' if i else ' ' )  + latexFileName )
        os.system('pwd')

# The program entrance
if __name__ == '__main__':
    main()
