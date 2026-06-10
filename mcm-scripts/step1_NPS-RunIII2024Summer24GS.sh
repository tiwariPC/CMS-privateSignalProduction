#!/bin/bash

# Binds for singularity containers
# Mount /afs, /eos, /cvmfs, /etc/grid-security for xrootd
export APPTAINER_BINDPATH='/afs,/cvmfs,/cvmfs/grid.cern.ch/etc/grid-security:/etc/grid-security,/eos,/etc/pki/ca-trust,/run/user,/var/run/user'

#############################################################
#   This script is used by McM when it performs automatic   #
#  validation in HTCondor or submits requests to computing  #
#                                                           #
#      !!! THIS FILE IS NOT MEANT TO BE RUN BY YOU !!!      #
# If you want to run validation script yourself you need to #
#     get a "Get test" script which can be retrieved by     #
#  clicking a button next to one you just clicked. It will  #
# say "Get test command" when you hover your mouse over it  #
#      If you try to run this, you will have a bad time     #
#############################################################

cd /afs/cern.ch/cms/PPD/PdmV/work/McM/submit/NPS-BBDM-RunIII2024Summer24GS/

# Make voms proxy
voms-proxy-init --voms cms --out $(pwd)/voms_proxy.txt --hours 4
export X509_USER_PROXY=$(pwd)/voms_proxy.txt

# Download fragment from McM
# curl -s -k https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/NPS-BBDM-RunIII2024Summer24GS --retry 3 --create-dirs -o Configuration/GenProduction/python/NPS-BBDM-RunIII2024Summer24GS-fragment.py
# [ -s Configuration/GenProduction/python/NPS-BBDM-RunIII2024Summer24GS-fragment.py ] || exit $?;

install -D BBDM-2HDMa-fullsim_Par-LO-5f_TuneCP5_13p6TeV_madgraph-pythia8-fragment.py Configuration/GenProduction/python/NPS-BBDM-RunIII2024Summer24GS-fragment.py


# Dump actual test code to a NPS-BBDM-RunIII2024Summer24GS_test.sh file that can be run in Singularity
cat <<'EndOfTestFile' > NPS-BBDM-RunIII2024Summer24GS_test.sh
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
EndOfTestFile

# Make file executable
chmod +x NPS-BBDM-RunIII2024Summer24GS_test.sh

if [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:amd64" ]; then
  CONTAINER_NAME="el8:amd64"
elif [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:x86_64" ]; then
  CONTAINER_NAME="el8:x86_64"
else
  echo "Could not find amd64 or x86_64 for el8"
  exit 1
fi
export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"
singularity run --no-home /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/$CONTAINER_NAME $(echo $(pwd)/NPS-BBDM-RunIII2024Summer24GS_test.sh)
