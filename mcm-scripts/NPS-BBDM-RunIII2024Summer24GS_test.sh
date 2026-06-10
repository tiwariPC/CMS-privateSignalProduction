#!/bin/bash

export SCRAM_ARCH=el8_amd64_gcc12

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_14_0_22_patch1/src ] ; then
  echo release CMSSW_14_0_22_patch1 already exists
else
  scram p CMSSW CMSSW_14_0_22_patch1
fi
cd CMSSW_14_0_22_patch1/src
eval `scram runtime -sh`

mv ../../Configuration .
scram b
cd ../..

# Maximum validation runtime: 28800s
# Minimum validation runtime: 600s
# Output events to run for the validation job (from application's setting): 100
# Event efficiency: Computed using the request efficiency and its error.
# Event efficiency: `efficiency - (2 * efficiency_error)`: `1 - (2 * 0.1)` = 0.8
# Input events: `int(output_events / event_efficiency)`: `int(100 / 0.8)` = 125
# Time per event (s): Computed adding all the time_per_event values on every sequence
# Time per event (s): 9.98
# Target input events: 125
# Target output events: 100
# This validation will be computed based on the target output events!
EVENTS=100


# cmsDriver command
cmsDriver.py Configuration/GenProduction/python/NPS-BBDM-RunIII2024Summer24GS-fragment.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions 140X_mcRun3_2024_realistic_v26 --beamspot DBrealistic --customise_commands "process.source.numberEventsInLuminosityBlock = cms.untracked.uint32(1)" --step GEN,SIM --geometry DB:Extended --era Run3_2024 --python_filename NPS-BBDM-RunIII2024Summer24GS_1_cfg.py --fileout file:NPS-BBDM-RunIII2024Summer24GS.root --number 100 --number_out 100 --no_exec --mc || exit $? ;

# End of NPS-BBDM-RunIII2024Summer24GS_test.sh file
