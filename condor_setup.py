import subprocess
import os
import sys

sys.path.append("Utils/python_utils/")
import gridpackList

from color_style import style

"""Fields changed by user"""
StringToChange = "2024"
nEvents = 200  # number of output events per job
gs_efficiency = 0.8  # GS filter efficiency
nEventsInput = int(nEvents / gs_efficiency)  # input events for GS step
condor_file_name = 'privateSignalProduction'
storeAreaPath = "/eos/cms/store/group/phys_susy/sus-23-008/run3_2HDMa_typeII_bbdm_PrivateSamples"
storeAreaPathForlogs = "."

"""Create log files"""
import infoCreaterGit

# SumamryOfCurrentSubmission = input("\n\nWrite summary for current job submission: ")
SumamryOfCurrentSubmission = "\n\nWrite summary for current job submission: "
infoLogFiles = infoCreaterGit.BasicInfoCreater(
    "summary.dat", SumamryOfCurrentSubmission
)
infoLogFiles.GenerateGitPatchAndLog()

"""Create directories for storing log files and output files at EOS."""
import fileshelper

dirsToCreate = fileshelper.FileHelper(
    "condor_logs/" + StringToChange, storeAreaPathForlogs
)
output_log_path = dirsToCreate.CreateLogDirWithDate()
dirTag = dirsToCreate.dirName
"""Create directories for different models at EOS"""
for key in gridpackList.models:
    if key == "radion":
        for gridpack in gridpackList.models[key]:
            DirName = gridpack.split("/")[-1].split("_")
            DirName = (
                DirName[0] + "_" + DirName[1] + "_" + DirName[2] + "_" + DirName[3]
            )
            storeDir = dirsToCreate.createStoreDirWithDate(StringToChange, DirName)
            print('storeDir',storeDir)
            infoLogFiles.SendGitLogAndPatchToEos(storeDir)


import condorJobHelper

if not os.path.exists("dummyFile"):
    open("dummyFile", "w").close()

listOfFilesToTransfer = "NPS-BBDM-RunIII2024Summer24GS_1_cfg.py, NPS-BBDM-RunIII2024Summer24DRPremix_1_cfg.py, NPS-BBDM-RunIII2024Summer24DRPremix_2_cfg.py, NPS-BBDM-RunIII2024Summer24MiniAODv6_1_cfg.py, NPS-BBDM-RunIII2024Summer24NanoAODv15_1_cfg.py, dummyFile"
condorJobHelper = condorJobHelper.condorJobHelper(
    condor_file_name,
    listOfFilesToTransfer,
    12000,  # request_memory 12000
    8,  # request_cpus 8
    output_log_path,
    "test",  # logFileName
    "",  # Arguments
    2,  # Queue
)
submitFile = condorJobHelper.submitFileHeaderCreater()
print("===> Condor executable file: ", condor_file_name + ".sh")
print("===> Condor submit file: ", submitFile)
print("===> Eos Outdir: ", "root://eoscms.cern.ch/" + storeAreaPath + os.sep + StringToChange)
print("===> Log files directory: ", output_log_path)
print()

for key in gridpackList.models:
    if key == "bbdm":
        for gridpack in gridpackList.models[key]:
            DirName = gridpack.split("/")[-1].split("_")
            DirName = ( DirName[0]+ "_" + DirName[1] + "_" + DirName[2] + "_" + DirName[3] + "_" + DirName[4] + "_" + DirName[5])
            condorJobHelper.logFileName = DirName
            condorJobHelper.Arguments = ( "NPS-BBDM-RunIII2024Summer24GS_1_cfg.py " + DirName + os.sep + dirTag + "  " + gridpack.replace("/", "\\/"))

condorJobHelper.submitJobsWriter()

outScript = open(condor_file_name + ".sh", "w")

outScript.write("#!/bin/bash")
outScript.write("\n" + 'echo "Starting job on " `date`')
outScript.write("\n" + 'echo "Running on: `uname -a`"')
outScript.write("\n" + 'echo "System software: `cat /etc/redhat-release`"')
outScript.write("\n" + "source /cvmfs/cms.cern.ch/cmsset_default.sh")
outScript.write("\n" + 'echo "' + "#" * 51 + '"')
outScript.write("\n" + 'echo "#    List of Input Arguments: "')
outScript.write("\n" + 'echo "' + "#" * 51 + '"')
outScript.write("\n" + 'echo "Input Arguments: $1"')
outScript.write("\n" + 'echo "Input Arguments: $2"')
outScript.write("\n" + 'echo "Input Arguments: $3"')
outScript.write("\n" + 'echo "Input Arguments: $4"')
outScript.write("\n" + 'echo "Input Arguments: $5"')
outScript.write("\n" + 'echo "' + "#" * 51 + '"')
outScript.write("\n" + "")
outScript.write("\n" + "OUTDIR=root://eoscms.cern.ch/" + storeAreaPath + os.sep + StringToChange + "/")
outScript.write("\n" + "")
outScript.write("\n" + "export SCRAM_ARCH=el8_amd64_gcc12")
outScript.write("\n" + "echo $PWD")
outScript.write("\n" + "eval $(scramv1 project CMSSW CMSSW_14_0_22_patch1)")
outScript.write("\n" + "cd CMSSW_14_0_22_patch1/src/")
outScript.write("\n" + "eval $(scram runtime -sh)")
outScript.write("\n" + "cd -")
outScript.write("\n" + 'echo "+=============================="')
# outScript.write("\n"+ 'sed -i "s/args = cms.vstring.*/args = cms.vstring(\\"${5}\\"),/g" NPS-BBDM_GEN-Run3Summer22wmLHEGS_1_cfg.py')
# outScript.write("\n" + f'sed -i "s/nEvents = cms.untracked.uint32.*/nEvents = cms.untracked.uint32({nEvents}),/g" NPS-BBDM_GEN-Run3Summer22wmLHEGS_1_cfg.py')
outScript.write("\n" + f'sed -i "s/input = cms.untracked.int32.*/input = cms.untracked.int32({nEventsInput}),/g" NPS-BBDM-RunIII2024Summer24GS_1_cfg.py')
outScript.write("\n" + f'sed -i "s/output = cms.untracked.int32.*/output = cms.untracked.int32({nEvents})/g" NPS-BBDM-RunIII2024Summer24GS_1_cfg.py')
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + 'echo "cmsRun NPS-BBDM-RunIII2024Summer24GS_1_cfg.py"')
outScript.write("\n" + "cmsRun NPS-BBDM-RunIII2024Summer24GS_1_cfg.py ")
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + 'echo "List all root files = "')
outScript.write("\n" + "ls *.root")
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + 'echo "Loading CMSSW env for DRPremix step"')
outScript.write("\n" + "eval $(scram unsetenv -sh)")
outScript.write("\n" + "source /cvmfs/cms.cern.ch/cmsset_default.sh")
outScript.write("\n" + "export SCRAM_ARCH=el8_amd64_gcc12")
outScript.write("\n" + "eval $(scramv1 project CMSSW CMSSW_14_0_21)")
outScript.write("\n" + "cd CMSSW_14_0_21/src/")
outScript.write("\n" + "eval $(scram runtime -sh)")
outScript.write("\n" + "cd -")
outScript.write("\n" + 'echo "==> cmsRun NPS-BBDM-RunIII2024Summer24DRPremix_1_cfg.py" ')
outScript.write("\n" + "cmsRun NPS-BBDM-RunIII2024Summer24DRPremix_1_cfg.py  ")
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + 'echo "List all root files = "')
outScript.write("\n" + "ls *.root")
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + 'echo "==> cmsRun NPS-BBDM-RunIII2024Summer24DRPremix_2_cfg.py"')
outScript.write("\n" + "cmsRun NPS-BBDM-RunIII2024Summer24DRPremix_2_cfg.py ")
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + 'echo "List all root files = "')
outScript.write("\n" + "ls *.root")
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + 'echo "Loading CMSSW env for MiniAOD+NanoAOD step"')
outScript.write("\n" + "eval $(scram unsetenv -sh)")
outScript.write("\n" + "source /cvmfs/cms.cern.ch/cmsset_default.sh")
outScript.write("\n" + "export SCRAM_ARCH=el8_amd64_gcc12")
outScript.write("\n" + "eval $(scramv1 project CMSSW CMSSW_15_0_4)")
outScript.write("\n" + "cd CMSSW_15_0_4/src/")
outScript.write("\n" + "eval $(scram runtime -sh)")
outScript.write("\n" + "cd -")
outScript.write("\n" + 'echo "==> cmsRun NPS-BBDM-RunIII2024Summer24MiniAODv6_1_cfg.py"')
outScript.write("\n" + "cmsRun NPS-BBDM-RunIII2024Summer24MiniAODv6_1_cfg.py")
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + 'echo "List all root files = "')
outScript.write("\n" + "ls *.root")
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + 'echo "==> cmsRun NPS-BBDM-RunIII2024Summer24NanoAODv15_1_cfg.py"')
outScript.write("\n" + "cmsRun NPS-BBDM-RunIII2024Summer24NanoAODv15_1_cfg.py")
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + 'echo "List all root files = "')
outScript.write("\n" + "ls *.root")
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + "mv NPS-BBDM-RunIII2024Summer24NanoAODv15.root  BBDM-2HDMa-fullsim_Par-LO-5f_TuneCP5_13p6TeV_madgraph-pythia8_RunIII2024Summer24NanoAODv15_${1}_${2}.root")
outScript.write("\n" + 'echo "Do xrdcp output for condor"')
outScript.write("\n" + 'outfile="BBDM-2HDMa-fullsim_Par-LO-5f_TuneCP5_13p6TeV_madgraph-pythia8_RunIII2024Summer24NanoAODv15_${1}_${2}.root"')
outScript.write("\n" + 'if [[ ! -f "$outfile" || ! -s "$outfile" ]]; then')
outScript.write("\n" + '    echo "ERROR: $outfile missing or empty (zombie), skipping xrdcp"; exit 1')
outScript.write("\n" + 'fi')
outScript.write("\n" + 'echo "Copying $outfile to EOS"')
outScript.write("\n" + 'until xrdcp -f "$outfile" ${OUTDIR}/"$outfile"; do')
outScript.write("\n" + '    sleep 60')
outScript.write("\n" + '    echo "Retrying"')
outScript.write("\n" + 'done')
outScript.write("\n" + 'echo "+=============================="')
outScript.write("\n" + 'echo "Done. Data Production Completed on $(date)"')
outScript.write("\n" + 'echo "+=============================="')
outScript.close()
os.chmod(condor_file_name + ".sh", 0o777)
print("===> Condor Executable File Created.")
print("===> Condor Submit File Created.")
print("===> Set Proxy Using:")
print("\tvoms-proxy-init --rfc --voms cms --valid 192:00")
print('\t"condor_submit ' + condor_file_name + '.submit" to submit')
