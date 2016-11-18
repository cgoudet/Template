import subprocess as sub
import os
import sys
import ROOT
sys.path.append(os.path.abspath("/afs/in2p3.fr/home/a/aguergui/public/Calibration/PlotFunctions/python"))
from SideFunction import *
from ROOT import *

configFile=open("/sps/atlas/a/aguerguichon/Calibration/Test/StabilityMC.boost","w")
configFile.write("inputType=8\n")

path=("/sps/atlas/a/aguerguichon/Calibration/DataxAOD/")
configFile.write("loadFiles="+path+"MC15c_13TeV_Zee_Lkh1/MC15c_13TeV_Zee_Lkh1.boost\n"+"varName=muPU m12 \nselectionCut= m12>=80 && m12<=100 \n")
configFile.write("varMin=0 \nvarMax=30 \nplotDirectory=/sps/atlas/a/aguerguichon/Calibration/Test/\n")

mean=0
counter=0

for dataset in listFiles(path+"MC15c_13TeV_Zee_Lkh1/MC15c*root"):
    histName=dataset.rsplit('/',1)[1]
    rootFile=TFile.Open(dataset)
    #print histName.split('.',1)[0]
    mean+=rootFile.Get(histName.split('.',1)[0]+"_ZMass").GetMean()
    counter+=1

mean=mean/counter
print (mean)
configFile.write("line="+str(mean)+"\n")

configFile.write("rangeUserY= 90 90.2 \n")
configFile.close()
