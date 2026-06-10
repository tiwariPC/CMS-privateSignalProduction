# MiniAOD + NanoAOD step
eval $(scram unsetenv -sh)
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el8_amd64_gcc12
eval $(scramv1 project CMSSW CMSSW_15_0_4)
cd CMSSW_15_0_4/src/
eval $(scram runtime -sh)
cd -
cmsRun NPS-BBDM-RunIII2024Summer24MiniAODv6_1_cfg.py
cmsRun NPS-BBDM-RunIII2024Summer24NanoAODv15_1_cfg.py
