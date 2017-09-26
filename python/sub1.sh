#! /bin/bash

#path=`pwd`/

qsub -P P_atlas -m e -M guerguichon@lal.in2p3.fr -l ct=10:00:00 -l vmem=16G -l sps=1 -N $1 -o ${path}$2 -e ${path}$3 $4

# $1 -job name
# ${path}$2 -log file
# echo ${path}$3 -err file
# echo $4 -.sh file

