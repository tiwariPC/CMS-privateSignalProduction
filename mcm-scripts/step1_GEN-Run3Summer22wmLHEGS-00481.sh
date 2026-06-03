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

cd /afs/cern.ch/cms/PPD/PdmV/work/McM/submit/GEN-Run3Summer22wmLHEGS-00481/

# Make voms proxy
voms-proxy-init --voms cms --out $(pwd)/voms_proxy.txt --hours 4
export X509_USER_PROXY=$(pwd)/voms_proxy.txt

# Download fragment from McM
curl -s -k https://cms-pdmv-prod.web.cern.ch/mcm/public/restapi/requests/get_fragment/GEN-Run3Summer22wmLHEGS-00481 --retry 3 --create-dirs -o Configuration/GenProduction/python/GEN-Run3Summer22wmLHEGS-00481-fragment.py
[ -s Configuration/GenProduction/python/GEN-Run3Summer22wmLHEGS-00481-fragment.py ] || exit $?;

# install -D mcm-scripts/bbDM_fragment.py Configuration/GenProduction/python/GEN-Run3Summer22wmLHEGS-00481-fragment.py

# Dump actual test code to a GEN-Run3Summer22wmLHEGS-00481_test.sh file that can be run in Singularity
cat <<'EndOfTestFile' > GEN-Run3Summer22wmLHEGS-00481_test.sh
#!/bin/bash

export SCRAM_ARCH=el8_amd64_gcc10

source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_12_4_14_patch3/src ] ; then
  echo release CMSSW_12_4_14_patch3 already exists
else
  scram p CMSSW CMSSW_12_4_14_patch3
fi
cd CMSSW_12_4_14_patch3/src
eval `scram runtime -sh`

mv ../../Configuration .
scram b
cd ../..

# Maximum validation runtime: 28800s
# Minimum validation runtime: 600s
# Output events to run for the validation job (from application's setting): 100
# Event efficiency: Computed using the request efficiency and its error.
# Event efficiency: `efficiency - (2 * efficiency_error)`: `0.08 - (2 * 0)` = 0.08
# Input events: `int(output_events / event_efficiency)`: `int(100 / 0.08)` = 1250
# Time per event (s): Computed adding all the time_per_event values on every sequence
# Time per event (s): 3.38
# Target input events: 1250
# Target output events: 100
# This validation will be computed based on the target output events!
EVENTS=100

# Random seed between 1 and 100 for externalLHEProducer
SEED=$(($(date +%s) % 100 + 1))


# cmsDriver command
# cmsDriver.py Configuration/GenProduction/python/GEN-Run3Summer22wmLHEGS-00481-fragment.py --eventcontent RAWSIM,LHE --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM,LHE --conditions 124X_mcRun3_2022_realistic_v12 --beamspot Realistic25ns13p6TeVEarly2022Collision --customise_commands process.RandomNumberGeneratorService.externalLHEProducer.initialSeed="int(${SEED})" --step LHE,GEN,SIM --geometry DB:Extended --era Run3 --python_filename GEN-Run3Summer22wmLHEGS-00481_1_cfg.py --fileout file:GEN-Run3Summer22wmLHEGS-00481.root --number 1250 --number_out 100 --no_exec --mc || exit $? ;

cmsDriver.py Configuration/GenProduction/python/GEN-Run3Summer22wmLHEGS-00481-fragment.py --eventcontent RAWSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier GEN-SIM --conditions 124X_mcRun3_2022_realistic_v12 --beamspot Realistic25ns13p6TeVEarly2022Collision --customise_commands "process.source.numberEventsInLuminosityBlock = cms.untracked.uint32(25)" --step GEN,SIM --geometry DB:Extended --era Run3 --python_filename GEN-Run3Summer22wmLHEGS_1_cfg.py --fileout file:GEN-Run3Summer22wmLHEGS-00481.root --number 100 --number_out 100 --no_exec --mc || exit $? ;

# End of GEN-Run3Summer22wmLHEGS-00481_test.sh file
EndOfTestFile

# Make file executable
chmod +x GEN-Run3Summer22wmLHEGS-00481_test.sh

if [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:amd64" ]; then
  CONTAINER_NAME="el8:amd64"
elif [ -e "/cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/el8:x86_64" ]; then
  CONTAINER_NAME="el8:x86_64"
else
  echo "Could not find amd64 or x86_64 for el8"
  exit 1
fi
export SINGULARITY_CACHEDIR="/tmp/$(whoami)/singularity"
singularity run --no-home /cvmfs/unpacked.cern.ch/registry.hub.docker.com/cmssw/$CONTAINER_NAME $(echo $(pwd)/GEN-Run3Summer22wmLHEGS-00481_test.sh)
