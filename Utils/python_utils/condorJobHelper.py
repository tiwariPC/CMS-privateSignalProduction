import os
import sys

class condorJobHelper(object):
    """docstring for condorJobHelper"""
    def __init__(self, fileName="test",
                 listOfFilesToTransfer="",
                 request_memory=0,
                 request_cpus=0,
                 logFilePath = 'test',
                 logFileName = 'test',
                 Arguments="",
                 Queue=1):
        self.fileName = fileName
        self.listOfFilesToTransfer = listOfFilesToTransfer
        self.request_memory = request_memory
        self.request_cpus = request_cpus
        self.logFilePath = logFilePath
        self.logFileName = logFileName
        self.Arguments = Arguments
        self.Queue = Queue

    def submitFileHeaderCreater(self):
        outSubmit = open(self.fileName+'.submit','w')
        outSubmit.write('Executable = '+self.fileName+'.sh')
        outSubmit.write('\n'+'Universe = vanilla')
        outSubmit.write('\n'+'Notification = ERROR')
        outSubmit.write('\n'+'Should_Transfer_Files = YES')
        outSubmit.write('\n'+'WhenToTransferOutput = ON_EXIT')
        outSubmit.write('\n'+'Transfer_Input_Files = '+self.fileName+'.sh, ' + self.listOfFilesToTransfer)
        outSubmit.write('\n'+'Transfer_Output_Files = dummyFile')
        outSubmit.write('\n'+'use_x509userproxy = True')
        outSubmit.write('\n'+'+SingularityImage = "/cvmfs/singularity.opensciencegrid.org/cmssw/cms:rhel7"') ##for uscms
        if self.request_memory != 0: outSubmit.write('\n'+'request_memory = '+str(self.request_memory))
        if self.request_cpus != 0: outSubmit.write('\n'+'request_cpus = '+ str(self.request_cpus))
        return self.fileName+'.submit'

    def submitFileAppendLogInfo(self):
        outSubmit = open(self.fileName+'.submit','a')
        outSubmit.write('\n'+'Output = '+self.logFilePath+os.sep+self.logFileName+'_$(Cluster)_$(Process).stdout')
        outSubmit.write('\n'+'Error  = '+self.logFilePath+os.sep+self.logFileName+'_$(Cluster)_$(Process).stderr')
        outSubmit.write('\n'+'Log  = '+self.logFilePath+os.sep+self.logFileName+'_$(Cluster)_$(Process).log')
        outSubmit.write('\n'+'Arguments = $(Cluster) $(Process) '+self.Arguments)
        outSubmit.write('\n'+'Queue '+str(self.Queue))
        outSubmit.close()

    def shFileHeaderCreater(self):
        outScript = open(self.fileName+".sh","w");
        outScript.write('#!/bin/bash')
        outScript.write('\n'+'echo "Starting job on " `date`')
        outScript.write('\n'+'echo "Running on: `uname -a`"')
        outScript.write('\n'+'echo "System software: `cat /etc/redhat-release`"')
        outScript.write('\n'+'source /cvmfs/cms.cern.ch/cmsset_default.sh')
        outScript.write('\n'+'echo "'+'#'*51+'"')
        outScript.write('\n'+'echo "#    List of Input Arguments: "')
        outScript.write('\n'+'echo "'+'#'*51+'"')
        outScript.write('\n'+'echo "Input Arguments (CluserID): $1" ')
        outScript.write('\n'+'echo "Input Arguments (ProcessID): $2" ')
        for x in range(3,len(self.Arguments)+3):
            outScript.write('\n'+'echo "Input Arguments: $'+str(x)+'" ')
        outScript.write('\n'+'echo "'+'#'*51+'"')
        outScript.write('\n'+'')
        outScript.close()
        return self.fileName+'.sh'

    def submitAndShFileCreater(self):
        submitFile = self.submitFileHeaderCreater()
        submitFile = self.submitFileAppendLogInfo()
        shFile = self.shFileCreater()
        return submitFile, shFile
