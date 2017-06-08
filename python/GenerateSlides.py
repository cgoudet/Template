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

        self.m_nomFile = 'ScalesOffSummer_1516'
        self.m_nomSuffixes = {'alpha' : '', 'c' : '_c'}
        self.m_systModel = { 'alpha' : 10, 'c' : 10 }
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
systematics.append( Systematic( 'Window', 'ScalesOffSummer_1516_Window' ) )
systematics.append( Systematic( 'fBrem', 'ScalesOffSummer_1516_fBrem50' ) )
systematics.append( Systematic( 'Threshold', 'ScalesOffSummer_1516_Threshold') )
systematics.append( Systematic( 'tightID', 'ScalesOffSummer_1516_tightID') )
systematics.append( Systematic( 'recoEff', 'ScalesOffSummer_1516_recoEff') )
systematics.append( Systematic( 'triggerEff', 'ScalesOffSummer_1516_triggerEff') )
systematics.append( Systematic( 'isoEff', 'ScalesOffSummer_1516_isoEff') )
systematics.append( Systematic( 'IDEff', 'ScalesOffSummer_1516_IDEff') )
systematics.append( Systematic( 'noIsoCut', 'ScalesOffSummer_1516_noIsoCut') )
systematics.append( Systematic( 'EW', 'ScalesOffSummer_1516_EW') )

systematics.append( Systematic( 'Inv', 'InversionStudy') )
systematics[-1].SetSuffixes( {'c' : '_c' } )

#systematics.append( Systematic( 'Mat', 'DataOff_13TeV_25ns_rel201_IBL') )
#systematics[-1].SetNomFile( 'DataOff_13TeV_25ns_rel201' )



systematics.append( Systematic( 'Clos', '/sps/atlas/a/aguerguichon/Calibration/Run1/EnergyScaleFactors') )
systematics[-1].SetSuffixes( { 'alpha' : '', 'c' : '' } ) 
systematics[-1].SetSystModel( { 'alpha' : 100, 'c' : 100 } ) 
systematics[-1].SetHistNames( { 'alpha' : 'Run1/alphaErrZee_run1_Clos', 'c' : 'Run1/ctErrZee_run1_Clos' } ) 
systematics[-1].SetNomFile( '' )

systematics.append( Systematic( 'Meth', '/sps/atlas/a/aguerguichon/Calibration/ScaleResults/170420/EnergyScaleFactors') )
systematics[-1].SetSuffixes( { 'alpha' : '', 'c' : '' } ) 
systematics[-1].SetSystModel( { 'alpha' : 100, 'c' : 100 } ) 
systematics[-1].SetHistNames( { 'alpha' : 'syst_Meth_alpha', 'c' : 'syst_Meth_c' } ) 
systematics[-1].SetNomFile( '' )

#specialID = [ 'fBrem', 'reweighting', 'cutFlow', 'nominal', 'residual', 'totSyst', 'correction', 'run1Syst' ]
specialID = [ 'totSyst', 'fBrem', 'run1Syst' ]


def InversionStudy( directory ) :
    print('create inversion systematic' )
    commandLines = [ 'InversionStudy --inFileName ' + directory + 'ScalesOffSummer_1516_c.root'
                     + ' --outFileName ' + directory + 'InversionStudy_c.root'
                     + ' --inputType ' + str(var) + ' --mode 12 '
                     for var in range(1,2) ]
    os.system( '\n'.join( commandLines ) )


#===============================================================
def applyCorrection( directory ) :

    os.chdir( directory )

    commandLine = 'MeasureScale --configFile /sps/atlas/a/aguerguichon/Calibration/PreRec/Config/AlphaOffSummer_15.boost --noExtraction'
    commandLine+= ' --dataFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/NominalZeeSelection/data15.root' 
    commandLine+= ' --correctAlphaHistName measScale_alpha --correctAlphaFileName /sps/atlas/a/aguerguichon/Calibration/ScaleResults/170125/AlphaOff_15.root \n'

    os.system( commandLine )
    os.system( commandLine.replace('15', '16') )


    commandLine = 'MeasureScale --configFile /sps/atlas/a/aguerguichon/Calibration/PreRec/Config/ScalesOffSummer_1516_c.boost --noExtraction '
    commandLine += ' --MCFileName /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/NominalZeeSelection/mcZee.root'
    commandLine += ' --correctSigmaHistName measScale_c '
    commandLine += ' --correctSigmaFileName /sps/atlas/a/aguerguichon/Calibration/ScaleResults/170125/ScalesOff_1516_c.root'

    os.system( commandLine )


    commandLine= 'mv /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/NominalZeeSelection/*corrected* ' + directory  

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
    systFile.write( 'outFileName='+directory + 'EnergyScaleFactors.root\ntotSystName=totSyst_' + var + '\n' )

    if systList[0].GetNomFile() != '' : 
        systFile.write('\n'.join( [ 
            ( 'rootFileName='+directory if '/' not in systList[0].GetNomFile() else '' ) + systList[0].GetNomFile() + systList[0].GetNomSuffixes()[var] + '.root', 
            'histName=measScale_' + var,
            ( 'systName=centVal_'+var+'_1516' if systList[0].GetNomFile()== 'ScalesOffSummer_1516' else '' ), 
            'mode=0'])
                       +'\n'
            )
    
    systFile.write( '\n'.join( [ 
                '\n'.join(['rootFileName='+( directory if '/' not in syst.GetInFile() else '' ) +syst.GetInFile() + syst.GetSuffixes()[var] + '.root', 
                'histName='+syst.GetHistNames()[var], 
                'systName=syst_'+syst.GetName()+ '_' + var, 
                'mode='+str( syst.GetSystModel()[var] )]) 
                for syst in systList if var in syst.GetSuffixes() ] )
                    +'\nupdate=1\n')
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
    slideText['Window'] = 'Systematic defined as the difference between nominal measurement and reducing $Z$ mass range from $[80-100]$~GeV to $[82.5-97.5]$~GeV.\n'
    slideText['noIsoCut'] = 'Systematic defined as the difference between nominal measurement and removing the isolation cut.\n'
    slideText['run1Syst'] = 'Comparison between current systematic model, Run 1, ICHEP 2016 and Moriond 2017 total systematic uncertainty.\n.'
    slideText['ID'] = 'Systematic defined as the difference between nominal measurement (medium) and tight identification selection..\n'
    slideText['fBrem' ] = 'Systematic defined as the difference between nominal measurement and an additional cut removing electrons with fBrem$>0.5$ (Run 1 0.3/ Moriond 0.7).\n'
    slideText['Meth' ] = 'Systematic \textcolor{red}{recomputed}: difference between nominal measurement and lineshape method (results from 20/04/17).\n'
    slideText['EW' ] = 'Systematic \textcolor{red}{recomputed}: difference between nominal measurement and measurement using MC produced including EW processes: diboson, t$\bar{t}$ and $Z\to\tau\tau$. \n'
    slideText['Inv' ] = "Systematic defined as the difference between nominal measurement with $c'_i>0$ and imposing $c'_i^2>0$ for the inversion procedure.\n"
    slideText['Clos' ] = 'Systematic \textcolor{red}{recomputed}: difference between values measured with the template method and values chosen as input when using a MC as pseudo-data (results from 20/04/17).\n'
    slideText['Threshold' ] = 'Systematic defined as the difference between nominal measurement and increasing the threshold mass $M_{th}$ from 70GeV to 75GeV, $M_{th}$ being the minimal $Z$ mass possible in a given ($\eta_{i}$,$\eta_{j}$) configuration for $p_{T, cut}=$27GeV.\n'

    effSyst = [ syst for syst in systs if 'Eff' in syst ]
    for syst in effSyst :
        effName = ''
        if syst == 'IDEffSyst' : effName = ' identification '
        elif syst == 'recoEffSyst' : effName = ' reconstruction '
        elif syst == 'isoEffSyst ' : effName = ' isolation '
        elif syst == 'triggerEffSyst ' : effName = ' trigger '
        slideText[syst] = ( syst + ' is defined as the difference between nominal measurement and pulling the weight of ' + effName + ' efficiency scale factors for each electron one sigma up.\n' )

    orderedList = ['nominal', 'residual' ]
    latex.write( '\n'.join( 
            [drawMinipage([plotName+var+'.eps' for var in ['_alpha', '_c'] ], plotName[0].upper() + plotName[1:], slideText[plotName] )
             for plotName in orderedList
             ]
            ) )               

    latex.write( '\n' )
    latex.write( drawMinipage( ['correction_m12.eps'], 'Correction', slideText['correction'] ) )


    latex.write( drawMinipage([ 'totSyst'+var+'.eps' for var in ['_alpha', '_c'] ], 'Experimental Uncertaities', slideText['totSyst'] ) )
    if mode : latex.write( ' '.join( [drawTabular([ 'totSyst'+var+'.csv' for var in ['_alpha', '_c'] ], 'Experimental Uncertainties breakdown : $\\alpha$ \\& $c$ ' )  ] ) )
#Systematics that come from a difference : alpha and c
    latex.write( '\n'.join( 
            [drawMinipage([plotName+plotType+var+'.eps'  for plotType in [ '', '_syst' ] for var in ['_alpha', '_c'] ] , plotName[0].upper() + plotName[1:], slideText[plotName] ) 
             for plotName in [ s for s in getSyst(111) ] ]  
            ) )
    #systematic that come directly from histogram : alpha and c
    latex.write( '\n'.join( 
            [drawMinipage([plotName+"_syst_"+var+'.eps' for var in ['alpha', 'c'] ] , plotName[0].upper() + plotName[1:], slideText[plotName] )
             for plotName in [ s for s in getSyst(211) ] ]
            )
                 )

# systematic from difference c only
    latex.write( '\n'.join( 
            [drawMinipage([plotName+plotType+'_c.eps' for plotType in [ '', '_syst' ] ] , plotName[0].upper() + plotName[1:], slideText[plotName])
                          for plotName in [ s for s in getSyst(121) ] ]
             )
            )

    # systematic directly from histogram : c only
    latex.write( '\n'.join( 
            [drawMinipage([plotName+'_syst_c.eps' for plotName in [ s for s in getSyst(221) ] ], "Systematics", '' )
             ]
            )
                 )
                 
    latex.write( '\n'.join( 
            [drawMinipage(['run1Syst'+var+'.eps' for var in ['_alpha', '_c'] ], 'Run1 systematics', slideText[plotName] )
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
    boostFile.write( 'extension=eps\n' )
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
                         + 'shiftColor=1 \n'
                         + 'line=0\n'
                         )

    boostFile.write( '\n'.join( syst.GetPlotOptions() ) +'\n' )
    boostFile.write( 'plotDirectory='+directory+'\n')
    boostFile.write( 'xTitle=__ETA_CALO\n')
    boostFile.write( 'loadFiles='+directory+'Label.txt\n' if syst.GetName() not in ['Clos', 'Meth'] else 'latex = __ATLAS Work in progress\nlatexOpt = 0.13 0.9')
    
#    boostFile.write( 'latex = __ATLAS Work in progress\nlatexOpt = 0.13 0.9')
    
    boostFile.close()
    
    return output

#================================================
def createRestBoost( directory, ID, var ) :
    fileSuffix = '_c' if var=='c' else ''

#Defining variables used in the boost files
    boostFile= directory + ID + '_' + var + '.boost'
    print( 'ID=', ID )
    options = {}

    if ID=='residual':
        if var=='c':options['rootFileName'] = [ directory+"ScalesOff_1516_dataScaled_c.root" ]
        else: options['rootFileName'] = [ directory+"ScalesOff_1516_dataScaled.root" ]

    else:
        options['rootFileName'] = [ directory+systematics[0].GetNomFile()+fileSuffix+'.root' ]
    options['objName'] = []
    options['loadFiles'] = [ directory + 'Label.txt']
    options['legend']=[]

    optionsUnique = {}
    optionsUnique['inputType']=0
    optionsUnique['plotDirectory']=directory
    optionsUnique['extension']="eps"

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
        options['rootFileName'] +=['/sps/atlas/c/cgoudet/Calibration/ScaleResults/160519/DataOff_13TeV_25ns_c.root'] if var == 'c' else ['/sps/atlas/c/cgoudet/Calibration/ScaleResults/160519/DataOff_13TeV_25ns.root']
        options['rootFileName'] += ['/sps/atlas/a/aguerguichon/Calibration/Run1/EnergyScaleFactors.root' ]*2
        options['rootFileName'].reverse()
        options['objName'] += ['PreRecommandations/'+varName+'_prerec_errSyst', 'PreRecommandations/'+varName+'_prerec_errStat' ]
        options['objName'] +=  ["measScale_c"] if var == 'c' else ["measScale_alpha"]
        options['legend']= [ 'Pre-recommandations, syst. unc. __FILL __NOPOINT', 'Pre-recommandations, stat. unc.', 'ICHEP results (3.2 fb^{-1}) ', '2015 + 2016' ]
        optionsUnique['yTitle']='__HASHTAGalpha'
        optionsUnique['shiftColor']=-1
        optionsUnique['legendPos'] = '0.62 0.9'
        if var=='c' : optionsUnique['rangeUserY'] = '0 0.99'
        
    elif ID == 'totSyst' :
        systs = getSyst( 10 if var=='alpha' else 1 )
        #systs = getSyst( 100 )

        options['rootFileName'] =  [directory + 'EnergyScaleFactors.root']*(len( systs )+ 1 ) 
        options['objName'].append( 'totSyst_' + var )
        options['legend'].append( 'totSyst' )
        options['objName'] += [ 'syst_' + plotName.replace('Syst', '' ) + '_' + var for plotName in systs ]
        options['legend'] += [ plotName.replace('Syst', '' ) for plotName in systs ]
        optionsUnique['doTabular']=1
        optionsUnique['xTitle']='__ETA_CALO'

    elif ID == 'correction' : 
        options['rootFileName']=[ '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/NominalZeeSelection/mcZee.root', '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/NominalZeeSelection/data15.root /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/NominalZeeSelection/data16.root' ] 
        options['objName'] = [ ( 'corrected'+ ( 'MC' if 'mc' in option else 'Data' ) + ' ' ) * len( option.split(' ') ) for option in options['rootFileName']  ]
        options['legend'] = [ 'MC', 'Data' ]
        optionsUnique['inputType']=1   
        boostFile= directory +'correction.boost'
        options['varName'] = [ 'm12']
        options['varMin'] = [ '80000' ]
        options['varMax'] = [ '100000' ]
        optionsUnique['nBins'] = 40
        optionsUnique['normalize']=1
        optionsUnique['doRatio']=1
        optionsUnique['rangeUserY'] = '0 0.99'

    elif ID == 'run1Syst' : 
        options['rootFileName'] = ['/sps/atlas/a/aguerguichon/Calibration/Run1/EnergyScaleFactors.root', '/sps/atlas/a/aguerguichon/Calibration/ScaleResults/ICHEP2016/EnergyScaleFactors.root', '/sps/atlas/a/aguerguichon/Calibration/ScaleResults/170125/EnergyScaleFactors.root', directory+'EnergyScaleFactors.root']
        options['objName'] = [ 'Run1/' + ( 'ct' if var=='c' else 'alpha' ) + 'ErrZee_run1_totSyst', 'totSyst_' + var,'totSyst_' + var, 'totSyst_' + var ]
        options['legend']= [ 'Run1', 'ICHEP recommandations', 'Moriond 2017', 'Current recommandations' ]
        optionsUnique['rangeUserY'] = '0 0.99'

    elif ID == 'cutFlow' : 
        boostFile= directory + ID + '.boost'
        #options['rootFileName'] = [ ' '.join([ dataset for dataset in listFiles('/sps/atlas/a/aguerguichon/Calibration/DataxAOD/Moriond2017/' + datasetType + '/', datasetType+'*.root' ) ] )
                                    #for datasetType in [ 'MC15c_13TeV_Zee_Lkh1' ] 
    #                                 ] 
        #options['objName'] = [ ' '.join( [ StripString(objName)+'_cutFlow' for objName in rootFile.split(' ') ] )
                                #for rootFile in options['rootFileName'] ]
        
        #options['loadFiles']=['Data1615_cutFlow.boost']
        options['rootFileName'] = [ ' '.join([ dataset for dataset in listFiles('/sps/atlas/a/aguerguichon/Calibration/DataxAOD/Moriond2017/' + datasetType + '/', datasetType+'*.root' ) ] )
                                    for datasetType in [ 'Data1*_13TeV_Zee_noGain_Lkh1','MC15c_13TeV_Zee_noGain_Lkh1' ] 
                                     ] 
        options['objName'] = [ 'Analysis_cutFlow Analysis_cutFlow', 'Analysis_cutFlow' ]
        
        options['legend']= [ 'Data', 'MC' ]
        optionsUnique['rangeUserY'] = '0 0.99'

    elif ID == 'reweighting' :
        optionsUnique['inputType']=1        
        options['rootFileName']=[]
        boostFile= directory + ID + '.boost'
        options['varWeight'] = ['X', 'SFID', 'SFIso', 'SFReco', 'puWeight', 'weight' ]
        options['loadFiles'] = [ '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/Moriond2017/MC15c_13TeV_Zee_noGain_Lkh1/MC15c_13TeV_Zee_noGain_Lkh1.boost' ]*len(options['varWeight'])
        options['legend']= options['varWeight']
        options['varName']=['m12']
        options['varMin'] = ['80000']
        options['varMax'] = ['100000']
        options['nBins'] = ['20']
        optionsUnique['rangeUserY'] = '0 0.99'
        optionsUnique['doRatio']=1
        optionsUnique['normalize']=1

    elif ID == 'fBrem' :
        optionsUnique['inputType']=1        
        options['rootFileName']=['/sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/NominalZeeSelection/data15.root /sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/NominalZeeSelection/data16.root', '/sps/atlas/a/aguerguichon/Calibration/DataxAOD/eosNtuples/NominalZeeSelection/mcZee.root']
        options['objName']=['CollectionTree CollectionTree', 'CollectionTree']
        boostFile= directory + ID + '.boost'
        options['varWeight'] = ['weight_1516' ]
        options['varName']=['el1_fBrem']
        options['varMin'] = ['0']
        options['varMax'] = ['1']
        options['xTitle'] = ['Fraction of momentum lost by bremsstrahlung (fBrem)']
        options['yTitle'] = ['Fraction of events']
        options['legend']= ['Data', 'MC' ]
        options['nBins'] = ['50']
        optionsUnique['rangeUserY'] = '0 0.09'
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
        default=0, type=int )
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
        os.system( 'Catalog --mode 1 ' + ' '.join( systematicsFiles ) )

    if args.doPlot :
        print('Creating boost files')
        filesToPlot = createBoost( args.directory, systematics )
#        filesToPlot += [ createBoost( args.directory, var, 'run1Syst' ) for var in range(0,2) ]
        os.system( 'PlotDist ' + ' '.join( filesToPlot ) )



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
