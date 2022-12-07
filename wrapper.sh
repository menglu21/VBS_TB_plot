#!/bin/bash -e 
echo "TEST FIRST" 
echo "copy input root file"
eoscp dummyroot ./INPUT
PWD=`pwd`
HOME=$PWD
echo $HOME 
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scramv1 project CMSSW CMSSW_10_6_29`
cd $PWD/CMSSW_10_6_29
ls -lrth
eval `scramv1 runtime -sh`

cd #PWD
echo "TEST DIR"

python make_hists.py -i INPUT -r REGION -c CATEGORY
printf "end!!!"
ls -lrth
rm -rf CMSSW_10_6_29
ls *.root | grep -v "output.root" |xargs rm
ls -lrth
