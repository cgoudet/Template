#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
import argparse
import subprocess as sub
import os
import sys
sys.path.append(os.path.abspath("/afs/in2p3.fr/home/a/aguergui/public/Calibration/PlotFunctions/python"))
from SideFunction import *

"""
Argument parser script example. 
Much more details at https://docs.python.org/2/howto/argparse.html
and at https://github.com/paris-swc/python-packaging
"""

class Systematic :
    def __init__( self, name, inFile ) :
        self.m_inFile = inFile
        self.m_name = name

        self.m_nomFile = 'DataOff_13TeV_25ns'
        self.m_nomSuffixes = {'alpha' : '', 'c' : '_c'}
        self.m_systModel = { 'alpha' : 20, 'c' : 20 }
        self.m_plotOptions = []
        self.m_suffixes = {'alpha' : '', 'c' : '_c'}
        self.m_histNames = { 'alpha' : 'measScale_alpha', 'c' : 'measScale_c' }

    def GetNomFile( self ) : return self.m_nomFile
    def GetInFile( self ) : return self.m_inFile
    def GetName( self ) : return self.m_name
    def GetSystModel( self ) : return self.m_systModel
    def GetPlotOptions( self ) : return self.m_plotOptions
    def GetSuffixes( self ) : return self.m_suffixes
    def GetNomSuffixes( self ) : return self.m_suffixes
    def GetHistNames( self ) : return self.m_histNames

    def SetNomFile( self, nomFile ) :  self.m_nomFile = nomFile
    def SetSystModel( self, systModel ) : self.m_systModel = systModel
    def SetPlotOptions( self, plotOptions ) : self.m_plotOptions = plotOptions
    def SetSuffixes( self, dictSuffix ) : self.m_suffixes = dictSuffix
    def SetHistNames( self, dictHists ) : self.m_histNames = dictHists

#Define all systematics
systematics = []
systematics.append( Systematic( 'Window', 'DataOff_13TeV_25ns_Window' ) )
systematics.append( Systematic( 'fBrem', 'DataOff_13TeV_25ns_fBrem' ) )
systematics.append( Systematic( 'Threshold', 'DataOff_13TeV_25ns_Threshold') )
systematics.append( Systematic( 'ID', 'DataOff_13TeV_25ns_ID') )
systematics.append( Systematic( 'recoEff', 'DataOff_13TeV_25ns_recoEff') )
systematics.append( Systematic( 'isoEff', 'DataOff_13TeV_25ns_isoEff') )
systematics.append( Systematic( 'IDEff', 'DataOff_13TeV_25ns_IDEff') )
systematics.append( Systematic( 'noIso', 'DataOff_13TeV_25ns_noIso') )

systematics.append( Systematic( 'Inv', 'InversionStudy') )
systematics[-1].SetSuffixes( {'c' : '_c' } )

systematics.append( Systematic( 'Mat', 'DataOff_13TeV_25ns_rel201_IBL') )
systematics[-1].SetNomFile( 'DataOff_13TeV_25ns_rel201' )

systematics.append( Systematic( 'Clos', '/sps/atlas/a/aguerguichon/Calibration/Run1/EnergyScaleFactors') )
systematics[-1].SetSuffixes( { 'alpha' : '', 'c' : '' } ) 
systematics[-1].SetSystModel( { 'alpha' : 10, 'c' : 10 } ) 
systematics[-1].SetHistNames( { 'alpha' : 'Run1/alphaErrZee_run1_Clos', 'c' : 'Run1/ctErrZee_run1_Clos' } ) 
systematics[-1].SetNomFile( '' )

systematics.append( Systematic( 'Meth', '/sps/atlas/a/aguerguichon/Calibration/Run1/EnergyScaleFactors') )
systematics[-1].SetSuffixes( { 'alpha' : '', 'c' : '' } ) 
systematics[-1].SetSystModel( { 'alpha' : 10, 'c' : 10 } ) 
systematics[-1].SetHistNames( { 'alpha' : 'Run1/alphaErrZee_run1_Meth', 'c' : 'Run1/ctErrZee_run1_MethMod' } ) 
systematics[-1].SetNomFile( '' )

systematics.append( Systematic( 'EW', '/sps/atlas/a/aguerguichon/Calibration/Run1/EnergyScaleFactors') )
systematics[-1].SetSuffixes( { 'alpha' : '', 'c' : '' } ) 
systematics[-1].SetSystModel( { 'alpha' : 10, 'c' : 10 } ) 
systematics[-1].SetHistNames( { 'alpha' : 'Run1/alphaErrZee_run1_EW', 'c' : 'Run1/ctErrZee_run1_EW' } ) 
systematics[-1].SetNomFile( '' )

specialID = [ 'fBrem', 'reweighting', 'cutFlow', 'nominal', 'residual', 'totSyst', 'correction', 'run1Syst' ]

def InversionStudy( directory ) :
    print('create inversion systematic' )
    commandLines = [ 'InversionStudy --inFileName ' + directory + 'DataOff_13TeV_25ns_c.root'
                     + ' --outFileName ' + directory + 'InversionStudy_c.root'
                     + ' --inputType ' + str(var) + ' --mode 12 '
                     for var in range(1,2) ]
    os.system( '\n'.join( commandLines ) )


#===============================================================
def applyCorrection( directory ) :

#    commandLine = 'MeasureScale --configFile /afs/in2p3.fr/home/a/aguergui/public/Calibration/Template/python/DataOff_13TeV_25ns.boost --noExtraction '
    commandLine = 'MeasureScale --configFile /sps/atlas/a/aguerguichon/Calibration/PreRec/Config/DataOff_13TeV_25ns.boost --noExtraction '
    commandLine += ' --dataFileName '.join( [''] + listFiles( '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/Data_13TeV_Zee_25ns_Lkh1/Data*.root' ) )
    commandLine += ' --MCFileName '.join( [''] + listFiles( '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/MC_13TeV_Zee_25ns_Lkh1/MC*.root' ) )
    commandLine += ' --correctAlphaHistName measScale_alpha --correctSigmaHistName measScale_c '
    commandLine += ' --correctAlphaFileName ' + directory + 'DataOff_13TeV_25ns.root'
    commandLine += ' --correctSigmaFileName ' + directory + 'DataOff_13TeV_25ns_c.root'

    os.chdir( directory )
    
    os.system( commandLine )
    content = listFiles( '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/Data_13TeV_Zee_25ns_Lkh1/Data*.root' ) + listFiles( '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/MC_13TeV_Zee_25ns_Lkh1/MC*.root' )
    content = [ (f if 'corrected' in f else '' ) for f in content ]
    
    commandLine= 'mv ' + ' '.join( content ) + ' ' + directory  

    os.system( commandLine )
    

#===========================================
def getSyst( mode = 0) :
    output=[]
    for syst in systematics :

        if syst.GetNomFile()=='' and mode/100==1 : continue
        if syst.GetNomFile()!='' and mode/100==2 : continue
        tmpMode = mode % 100
#get rid of 
        if int(tmpMode /10) == 1 and 'alpha' not in syst.GetSuffixes() : continue
        if int(tmpMode /10) == 2 and 'alpha' in syst.GetSuffixes() : continue

        tmpMode = mode % 10
        if tmpMode == 1 and 'c' not in syst.GetSuffixes() : continue
        if tmpMode == 2 and 'c' in syst.GetSuffixes() : continue

        output.append( syst.GetName() )
    return output

#===============================================
def createSingleFile( directory, var, systList, suffix='' ) :
    if not len(systList) : return

    outFile = directory + 'systematics_' + var + suffix + '.txt'
    systFile = open( outFile, 'w' )
    systFile.write( directory + 'EnergyScaleFactors.root totSyst_' + var + ' dum 0\n' )

    if systList[0].GetNomFile() != '' : 
        systFile.write( ( directory if '/' not in systList[0].GetNomFile() else '' ) + systList[0].GetNomFile() + systList[0].GetNomSuffixes()[var] + '.root measScale_' + var + ( ' centVal_'+var if systList[0].GetNomFile()== 'DataOff_13TeV_25ns' else ' dum' ) + ' 0\n' )
    
    systFile.write( '\n'.join( [ 
                ( directory if '/' not in syst.GetInFile() else '' ) 
                + syst.GetInFile() + syst.GetSuffixes()[var] + '.root ' + ' '.join( [ syst.GetHistNames()[var], syst.GetName()+ '_' + var, str( syst.GetSystModel()[var] ) ] ) 
                for syst in systList if var in syst.GetSuffixes() ] )
                    + '\n' )
    systFile.close()
    return outFile
#===============================================
def createSystematicFiles( directory, systList ) :

    dispatchSystByNom = {}
    nominalFiles = []
    for syst in systList : 
        nomFile = syst.GetNomFile()
        if not nomFile in dispatchSystByNom : dispatchSystByNom[nomFile]=[]
        if not nomFile in nominalFiles : nominalFiles.append( nomFile )
        dispatchSystByNom[nomFile].append( syst )

    print( nominalFiles )

    output = [ createSingleFile( directory, var, dispatchSystByNom[systs], '_'+str(nominalFiles.index( systs )) ) for systs in dispatchSystByNom for var in ['alpha', 'c'] ]
    output.sort()

    return output

#=============================================
def createLatex( directory, introFiles=[], concluFiles=[], mode=1 ) :
    latexFileName = directory + 'latex.tex'
    print( 'latexFileName : ', latexFileName )
    latex = open( latexFileName, "w" )

    latex.write( LatexHeader( 'Central electron energy scale factors and resolution constant term', 'Electron scale factors', mode ) )

    for input in introFiles : 
        with open( input ) as intro :
            for line in intro : latex.write( line  )

    systs = getSyst()
    slideText = {}
    for name in systs+specialID : slideText[name]=''
    slideText['nominal'] = ( 'Scales are measured with 2015 13TeV data at 25ns : \n'
                             + '\\begin{itemize}\item Data are {\\bf not} corrected with energy scale from pre-recommandations, '
                             + '\\item MC is {\\bf not }smeared with pre-rec.\\end{itemize}'
                             )
    slideText['residual'] = ( 'Scales are measured with 2015 13TeV data at 25ns : \n'
                             + '\\begin{itemize}\item Data are corrected with energy scale from pre-recommandations + temperature, '
                             + '\\item MC is {\\bf not }smeared with pre-rec.\\end{itemize}'
                             )
    slideText['correction'] = ( 'The lineshape of the $Z$ is compared after application of 2015 corrections between data and MC.\n' )
    slideText['totSyst'] = ( 'Sources of uncertainty and their contribution in the total systematic uncertainty.\n For statistical reasons, uncertainties are symetrized along $\eta_{calo}$\n' )
    slideText['WindowSyst'] = 'Systematic defined as the difference between nominal measurement and reducing $Z$ mass range from $[80-100]$~GeV to $[82.5-97.5]$~GeV.\n'
    slideText['noIsoSyst'] = 'Systematic defined as the difference between nominal measurement and removing the isolation cut.\n'
    slideText['run1Syst'] = 'Comparison between current systematic model and run1 total systematic uncertainty\n.'
    slideText['IDSyst'] = 'Systematic defined as the difference between nominal measurement and Tight identification selection\n'
    slideText['fBremSyst' ] = 'Systematic defined as the difference between nominal measurement and an additional cut removing electrons with fBrem$>0.7$.\n'

    effSyst = [ syst for syst in systs if 'Eff' in syst ]
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
            ) )               

    latex.write( '\n' )
    latex.write( drawMinipage( ['correction_m12.pdf'], 'Correction', slideText['correction'] ) )


    latex.write( drawMinipage([ 'totSyst'+var+'.pdf' for var in ['_alpha', '_c'] ], 'Experimental Uncertaities', slideText['totSyst'] ) )
    if mode : latex.write( ' '.join( [drawTabular([ 'totSyst'+var+'.csv' for var in ['_alpha', '_c'] ], 'Experimental Uncertainties breakdown : $\\alpha$ \\& $c$ ' )  ] ) )
#Systematics that come from a difference : alpha and c
    latex.write( '\n'.join( 
            [drawMinipage([plotName+plotType+var+'.pdf'  for plotType in [ '', '_syst' ] for var in ['_alpha', '_c'] ] , plotName[0].upper() + plotName[1:], slideText[plotName] ) 
             for plotName in [ s for s in getSyst(111) ] ]  
            ) )
    #systematic that come directly from histogram : alpha and c
    latex.write( '\n'.join( 
            [drawMinipage([plotName+"_syst_"+var+'.pdf' for var in ['alpha', 'c'] ] , plotName[0].upper() + plotName[1:], slideText[plotName] )
             for plotName in [ s for s in getSyst(211) ] ]
            )
                 )

# systematic from difference c only
    latex.write( '\n'.join( 
            [drawMinipage([plotName+plotType+'_c.pdf' for plotType in [ '', '_syst' ] ] , plotName[0].upper() + plotName[1:], slideText[plotName])
                          for plotName in [ s for s in getSyst(121) ] ]
             )
            )

    # systematic directly from histogram : c only
    latex.write( '\n'.join( 
            [drawMinipage([plotName+'_syst_c.pdf' for plotName in [ s for s in getSyst(221) ] ], "Systematics", '' )
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
def createSystBoost( directory, syst, var, mode ) :
    if syst.GetNomFile()=='' and not mode : return ''
    if not var in syst.GetSuffixes() : return ''

    output = directory + syst.GetName() + ( '_syst' if mode else '' ) + '_' + var + '.boost'

    boostFile = open( output, 'w+' )
    boostFile.write( 'inputType=0\n' )
    if not mode :
        boostFile.write( 'rootFileName=' + ( directory if '/' not in syst.GetNomFile() else '' ) + syst.GetNomFile() + syst.GetNomSuffixes()[var] + '.root\n' 
                         + 'rootFileName=' + ( directory if '/' not in syst.GetInFile() else '' ) + syst.GetInFile() + syst.GetSuffixes()[var] + '.root\n' 
                         + ('objName=measScale_' + var + '\n')*2
                         + 'legend=Nominal\nlegend='+syst.GetName()+'\n'
                         + 'doRatio=2\n'
                         )
        if var=='c' : boostFile.write( 'rangeUserY=0 0.99\n' )
        
    else : 
        boostFile.write( 'rootFileName=' +  directory + 'EnergyScaleFactors.root\n'
                         + 'objName=syst_'+syst.GetName()+'_'+var+'\n'
                         + 'legend='+syst.GetName()+'\n'
                         + 'line=0\n'
                         )

    boostFile.write( '\n'.join( syst.GetPlotOptions() ) +'\n' )
    boostFile.write( 'plotDirectory='+directory+'\n')
    boostFile.write( 'loadFiles='+directory+'Label.txt\n')

    boostFile.close()
    
    return output

#================================================
def createRestBoost( directory, ID, var ) :
    fileSuffix = '_c' if var=='c' else ''

#Defining variables used in the boost files
    boostFile= directory + ID + '_' + var + '.boost'
    print( 'ID=', ID )
    options = {}

    if ID=='residual' and var!='c':
        options['rootFileName'] = [ directory+"DataOff_13TeV_25ns_dataScaled.root" ]

    else:
        options['rootFileName'] = [ directory+systematics[0].GetNomFile()+fileSuffix+'.root' ]
    options['objName'] = []
    options['loadFiles'] = [ directory + 'Label.txt']
    options['legend']=[]

    optionsUnique = {}
    optionsUnique['inputType']=0
    optionsUnique['plotDirectory']=directory

    if ID =='residual' : #PreRec
        varName = 'ctZee' if var=='c' else 'alpha0'
        options['rootFileName'] += ['/sps/atlas/a/aguerguichon/Calibration/Run1/EnergyScaleFactors.root' ]*(2 if var =="c" else 1)
        options['rootFileName'].reverse()
        options['objName'].append( 'PreRecommandations/' + varName + '_prerec_errSyst' )
        options['legend'] .append('Pre-recommandations, syst. unc. __FILL __NOPOINT' )
        optionsUnique['yTitle']='__HASHTAGalpha'
        if var=='c' : 
            options['objName'].append( 'PreRecommandations/ctZee_prerec_errStat' )
            options['legend'].append( 'Pre-recommandations, stat. unc.' )
            optionsUnique['shiftColor']=-1

        else :
            optionsUnique['line']='0'
            pass
        optionsUnique['legendPos'] = '0.55 0.9'
        options['legend'].append( 'Run2' )
        if var=='c' : optionsUnique['rangeUserY'] = '0 0.99'

    elif ID=='nominal' :
        print('nominal')
        varName = 'ctZee' if var=='c' else 'alphaTot'
        options['rootFileName'] += ['/sps/atlas/a/aguerguichon/Calibration/Run1/EnergyScaleFactors.root' ]*2
        options['rootFileName'].reverse()
        options['objName'] += ['PreRecommandations/'+varName+'_prerec_errSyst', 'PreRecommandations/'+varName+'_prerec_errStat' ]
        options['legend']= [ 'Pre-recommandations, syst. unc. __FILL __NOPOINT', 'Pre-recommandations, stat. unc.', 'Run2' ]
        optionsUnique['yTitle']='__HASHTAGalpha'
        optionsUnique['shiftColor']=-1
        optionsUnique['legendPos'] = '0.55 0.9'
        if var=='c' : optionsUnique['rangeUserY'] = '0 0.99'
        
    elif ID == 'totSyst' :
        systs = getSyst( 10 if var=='alpha' else 1 )

        options['rootFileName'] =  [directory + 'EnergyScaleFactors.root']*(len( systs )+ 1 ) 
        options['objName'].append( 'totSyst_' + var )
        options['legend'].append( 'totSyst' )
        options['objName'] += [ 'syst_' + plotName.replace('Syst', '' ) + '_' + var for plotName in systs ]
        options['legend'] += [ plotName.replace('Syst', '' ) for plotName in systs ]
        optionsUnique['doTabular']=1

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
        optionsUnique['rangeUserY'] = '0 0.99'

    elif ID == 'run1Syst' :
        options['rootFileName'] = ['/sps/atlas/a/aguerguichon/Calibration/Run1/EnergyScaleFactors.root', directory+'EnergyScaleFactors.root']
        options['objName'] = [ 'Run1/' + ( 'ct' if var=='c' else 'alpha' ) + 'ErrZee_run1_totSyst', 'totSyst_' + var ]
        options['legend']= [ 'Run1', 'Run2' ]
        optionsUnique['rangeUserY'] = '0 0.99'

    elif ID == 'cutFlow' : 
        boostFile= directory + ID + '.boost'
        options['rootFileName'] = [ ' '.join([ dataset for dataset in listFiles('/sps/atlas/a/aguerguichon/Calibration/DataxAOD/' + datasetType + '/', datasetType+'*.root' ) ] )
                                    for datasetType in [ 'Data_13TeV_Zee_2015_Lkh1', 'MC_13TeV_Zee_2015b_Lkh1' ] 
                                     ] 
        options['objName'] = [ ' '.join( [ StripString(objName)+'_cutFlow' for objName in rootFile.split(' ') ] )
                                for rootFile in options['rootFileName'] ]
        options['legend']= [ 'Data', 'MC' ]
        optionsUnique['rangeUserY'] = '0 0.99'

    elif ID == 'reweighting' :
        optionsUnique['inputType']=1        
        options['rootFileName']=[]
        boostFile= directory + ID + '.boost'
        options['varWeight'] = ['X', 'SFID', 'SFIso', 'SFReco', 'puWeight', 'weight' ]
        options['loadFiles'] = [ '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/MC_13TeV_Zee_25ns_Lkh1/MC_13TeV_Zee_25ns_Lkh1.boost' ]*len(options['varWeight'])
        options['legend']= options['varWeight']
        options['varName']=['m12']
        options['varMin'] = ['80']
        options['varMax'] = ['100']
        options['nComparedEvents'] = ['20']
        optionsUnique['rangeUserY'] = '0 0.99'
        optionsUnique['doRatio']=1
        optionsUnique['normalize']=1

    elif ID == 'fBrem' :
        optionsUnique['inputType']=1        
        options['rootFileName']=[]
        boostFile= directory + ID + '.boost'
        options['varWeight'] = ['weight' ]
        options['loadFiles'] = [ '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/Data_13TeV_Zee_2015_Lkh1/Data_13TeV_Zee_2015_Lkh1_0.boost', '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/MC_13TeV_Zee_2015b_Lkh1/MC_13TeV_Zee_2015b_Lkh1.boost' ]
        options['legend']= ['MC', 'Data' ]
        options['varName']=['fBrem_1 fBrem_2']
        options['varMin'] = ['-0.5 -0.5']
        options['varMax'] = ['1 1']
        options['nComparedEvents'] = ['30']
        optionsUnique['rangeUserY'] = '0 0.99'
        optionsUnique['doRatio']=1
        optionsUnique['normalize']=1
        

#Defining default cases of options if not defined
    if len( options['objName'] ) < len( options['rootFileName'] ) : options['objName'] += [ 'measScale_' + var  ]*(len(options['rootFileName']) - len(options['objName']))


    print('Print in file : ',boostFile )
    with open( boostFile, 'w+') as boost: 
        boost.write( '\n'.join( [ opt + '=' + it for opt in options for it in options[opt] ] ) + '\n' )
        boost.write( '\n'.join( [ opt + '=' + str(optionsUnique[opt]) for opt in optionsUnique] ) + '\n' )
    return boostFile
    
#=========================================
def createBoost( directory, systList ):

    boostFiles = [ createSystBoost( directory, syst, var, mode ) for var in ['alpha', 'c'] for syst in systList for mode in range(0,2) ]
    boostFiles += [ createRestBoost( directory, ID, var ) for var in ['alpha', 'c'] for ID in specialID ]

    boostFiles = [ x for x in boostFiles if x!='' ]
    return boostFiles


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
        default=1, type=int )
    parser.add_argument(
        '--doLatex', help='Tag for recreating plots',
        default=1, type=int )
    parser.add_argument(
        '--doSyst', help='Tag for recreating systematics histos and plots',
        default=1, type=int )
    parser.add_argument(
        '--doCorrection', help='Tag for recreating systematics histos and plots',
        default=1, type=int )

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

    if not '/' in args.directory : args.directory = '/sps/atlas/a/aguerguichon/Calibration/ScaleResults/' + args.directory + '/'



    if args.doCorrection :
        print('Doing correction')
        applyCorrection(args.directory)

    if args.doSyst :
        print('Creating Systematics')
        InversionStudy( args.directory )
        systematicsFiles = createSystematicFiles( args.directory, systematics ) 
        #print(systematics)
        os.system( 'AddSyst ' + ' '.join( systematicsFiles ) )

    if args.doPlot :
        print('Creating boost files')
        filesToPlot = createBoost( args.directory, systematics )
#        filesToPlot += [ createBoost( args.directory, var, 'run1Syst' ) for var in range(0,2) ]
        os.system( 'CompareHist ' + ' '.join( filesToPlot ) )



#    createLatex( args.directory )
    if args.doLatex :
        mode = 1
        os.chdir( args.directory )
        os.system('pwd')
        latexFileName = createLatex( args.directory, [ args.directory + 'intro.tex' ], [ args.directory + 'conclu.tex' ] , mode )
        if not mode : 
            for i in range(0, 3) : os.system( 'pdflatex ' + ( ' -interaction=batchmode ' if i else ' ' )  + latexFileName )
        os.system('pwd')

# The program entrance
if __name__ == '__main__':
    main()
