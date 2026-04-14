#!/bin/bash
echo "Starting job on " `date`
echo "Running on: `uname -a`"
echo "System software: `cat /etc/redhat-release`"
source /cvmfs/cms.cern.ch/cmsset_default.sh
echo "###################################################"
echo "#    List of Input Arguments: "
echo "###################################################"
echo "Input Arguments: $1"
echo "Input Arguments: $2"
echo "Input Arguments: $3"
echo "Input Arguments: $4"
echo "Input Arguments: $5"
echo "###################################################"

OUTDIR=root://eoscms.cern.ch//eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_PrivateSamples//2022/${4}/

echo "======="
ls
echo "======"

export SCRAM_ARCH=el8_amd64_gcc10
echo $PWD
eval `scramv1 project CMSSW CMSSW_12_4_8`
cd CMSSW_12_4_14_patch3/src/
eval `scram runtime -sh`
cd -
echo "+=============================="
echo "==> Running LHE GEN SIM step"
sed -i "s/args = cms.vstring.*/args = cms.vstring(\"${5}\"),/g" NPS-BBDM_GEN-Run3Summer22wmLHEGS_1_cfg.py 
echo "+=============================="
cmsRun NPS-BBDM_GEN-Run3Summer22wmLHEGS_1_cfg.py 
echo "+=============================="
echo "List all root files = "
ls *.root
echo "List all files"
date
echo "+=============================="

echo "========================="
echo "==> List all files..."
echo "pwd : ${PWD}"
ls 
echo "+=============================="
echo "==> NPS-BBDM_GEN-Run3Summer22DRPremix_1_cfg.py" 
cmsRun NPS-BBDM_DIGIPremix_cfg.py  
eval `scramv1 project CMSSW CMSSW_12_4_14_patch3`
cd CMSSW_12_4_14_patch3/src/
# set cmssw environment
eval `scram runtime -sh`
cd -
echo "==> cmsRun NPS-BBDM_GEN-Run3Summer22DRPremix_2_cfg.py"
cmsRun NPS-BBDM_GEN-Run3Summer22DRPremix_2_cfg.py 
echo "Loading CMSSW env for RECO step"
eval `scramv1 project CMSSW CMSSW_13_0_13`
cd CMSSW_13_0_13/src/
# set cmssw environment
eval `scram runtime -sh`
cd -
echo "==> cmsRun NPS-BBDM_GEN-Run3Summer22MiniAODv4_1_cfg.py"
cmsRun NPS-BBDM_GEN-Run3Summer22MiniAODv4_1_cfg.py
echo "========================="
echo "==> List all files..."
echo "pwd : ${PWD}"
ls 
echo "+=============================="
echo "==> Running NanoAOD..."
eval `scramv1 project CMSSW CMSSW_13_0_13`
cd CMSSW_13_0_13/src
echo $PWD
eval `scram runtime -sh`
cd -
cmsRun NPS-BBDM_GEN-Run3Summer22NanoAODv12_1_cfg.py
echo "List all root files = "
ls *.root
echo "+=============================="
# To copy output to eos
mv NPS-BBDM_GEN-Run3Summer22NanoAODv12.root  NPS-BBDM_GEN-Run3Summer22NanoAODv12_${1}_${2}.root
echo "xrdcp output for condor"
echo "xrdcp -f NPS-BBDM_GEN-Run3Summer22NanoAODv12_${1}_${2}.root ${OUTDIR}/NPS-BBDM_GEN-Run3Summer22NanoAODv12_${1}_${2}.root"
echo "+=============================="
echo "Done."
date