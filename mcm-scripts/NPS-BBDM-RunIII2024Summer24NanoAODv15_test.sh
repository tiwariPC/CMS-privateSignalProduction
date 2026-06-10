#!/bin/bash

export SCRAM_ARCH=el8_amd64_gcc12

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_15_0_4/src ] ; then
  echo release CMSSW_15_0_4 already exists
else
  scram p CMSSW CMSSW_15_0_4
fi
cd CMSSW_15_0_4/src
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
# Time per event (s): 0.3
# Initial target input events: 100
# Initial target output events: 100
# Validation runtime will not run for long enough than expected, extending the time
# Target input events changed to: `minimum_runtime / time_per_event * number_of_threads`: `600 / 0.3 * 1` = 2e+03
# Target output events changed to: `target_input_events * event_efficiency`: `2e+03 * 1` = 2e+03
# Final target input events: 2000
# Final target output events: 2000
# This validation will be computed based on the target output events!
EVENTS=2000


# cmsDriver command
cmsDriver.py  --scenario pp --era Run3_2024 --customise Configuration/DataProcessing/Utils.addMonitoring --step NANO --conditions 150X_mcRun3_2024_realistic_v2 --datatier NANOAODSIM --eventcontent NANOAODSIM1 --python_filename NPS-BBDM-RunIII2024Summer24NanoAODv15_1_cfg.py --fileout file:NPS-BBDM-RunIII2024Summer24NanoAODv15.root --filein file:NPS-BBDM-RunIII2024Summer24MiniAODv6.root --number 2000 --number_out 2000 --no_exec --mc || exit $? ;

# End of NPS-BBDM-RunIII2024Summer24NanoAODv15_test.sh file
