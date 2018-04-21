#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_89/x86_64-slc6-gcc62-opt/setup.sh
cd ~/www/pw/cadiTool
nohup python2.7 -u cadiDeltaLogger.py > deltaLogger.log 2>&1
