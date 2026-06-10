# GS step
export SCRAM_ARCH=el8_amd64_gcc12
eval $(scramv1 project CMSSW CMSSW_14_0_22_patch1)
cd CMSSW_14_0_22_patch1/src/
eval $(scram runtime -sh)
cd -
cmsRun NPS-BBDM-RunIII2024Summer24GS_1_cfg.py

# DRPremix step
eval $(scram unsetenv -sh)
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=el8_amd64_gcc12
eval $(scramv1 project CMSSW CMSSW_14_0_21)
cd CMSSW_14_0_21/src/
eval $(scram runtime -sh)
cd -
cmsRun NPS-BBDM-RunIII2024Summer24DRPremix_1_cfg.py
cmsRun NPS-BBDM-RunIII2024Summer24DRPremix_2_cfg.py