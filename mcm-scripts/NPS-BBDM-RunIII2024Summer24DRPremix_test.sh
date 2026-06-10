#!/bin/bash

export SCRAM_ARCH=el8_amd64_gcc12

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_14_0_21/src ] ; then
  echo release CMSSW_14_0_21 already exists
else
  scram p CMSSW CMSSW_14_0_21
fi
cd CMSSW_14_0_21/src
eval `scram runtime -sh`

mv ../../Configuration .
scram b
cd ../..

# Maximum validation runtime: 28800s
# Minimum validation runtime: 600s
# Output events to run for the validation job (from application's setting): 100
# Event efficiency: Computed using the request efficiency and its error.
# Event efficiency: `efficiency - (2 * efficiency_error)`: `1 - (2 * 0)` = 1
# Input events: `int(output_events / event_efficiency)`: `int(100 / 1)` = 100
# Time per event (s): Computed adding all the time_per_event values on every sequence
# Time per event (s): 36
# Target input events: 100
# Target output events: 100
# This validation will be computed based on the target output events!
EVENTS=100


# cmsDriver command
cmsDriver.py  --era Run3_2024 --customise Configuration/DataProcessing/Utils.addMonitoring --procModifiers premix_stage2 --datamix PreMix --step DIGI,DATAMIX,L1,DIGI2RAW,HLT:2024v14 --geometry DB:Extended --conditions 140X_mcRun3_2024_realistic_v26 --datatier GEN-SIM-RAW --eventcontent PREMIXRAW --python_filename NPS-BBDM-RunIII2024Summer24DRPremix_1_cfg.py --fileout file:NPS-BBDM-RunIII2024Summer24DRPremix_0.root --filein file:NPS-BBDM-RunIII2024Summer24GS.root --number 100 --number_out 100 --pileup_input "dbs:/Neutrino_E-10_gun/RunIIISummer24PrePremix-Premixlib2024_140X_mcRun3_2024_realistic_v26-v1/PREMIX" --no_exec --mc || exit $? ;

# cmsDriver command
cmsDriver.py  --era Run3_2024 --customise Configuration/DataProcessing/Utils.addMonitoring --step RAW2DIGI,L1Reco,RECO,RECOSIM --geometry DB:Extended --conditions 140X_mcRun3_2024_realistic_v26 --datatier AODSIM --eventcontent AODSIM --python_filename NPS-BBDM-RunIII2024Summer24DRPremix_2_cfg.py --fileout file:NPS-BBDM-RunIII2024Summer24DRPremix.root --filein file:NPS-BBDM-RunIII2024Summer24DRPremix_0.root --number 100 --number_out 100 --no_exec --mc || exit $? ;

# End of NPS-BBDM-RunIII2024Summer24DRPremix_test.sh file
