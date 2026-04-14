import os
import subprocess
from datetime import datetime


class FileHelper:
    """Helper class for creating local + EOS directories with timestamp."""

    def __init__(self, logPath, storeArea, ifeos=False):
        self.ifeos = ifeos
        self.logPath = logPath
        self.storeArea = storeArea

        now = datetime.now()

        self.dirName = (
            f"{str(now.year)[-2:]}"
            f"{now.month:02d}"
            f"{now.day:02d}_"
            f"{now.hour:02d}"
            f"{now.minute:02d}"
            f"{now.second:02d}"
        )

        self.eosString = "/eos/uscms"

        print("===> Time stamp:", self.dirName)

    # --------------------------------------------------

    def CreateLogDirWithDate(self):
        """Create local log directory."""
        logDirName = os.path.join(self.logPath, self.dirName)

        os.makedirs(logDirName, exist_ok=True)

        print("===> Created directory for log files:", logDirName)
        return logDirName

    # --------------------------------------------------

    def CreateSotreArea(self, path):
        """Create directory on EOS."""
        subprocess.run([
            "xrdfs",
            "root://cmseos.fnal.gov/",
            "mkdir",
            path
        ])

        print("===> Created EOS directory:", path)
        return path

    # --------------------------------------------------

    def createStoreDirWithDate(self,
                               additionalString1="",
                               additionalString2="",
                               additionalString3=""):
        """
        Create nested EOS store directories + timestamp folder.
        """

        path = self.CreateSotreArea(self.storeArea)

        if additionalString1:
            path = self.CreateSotreArea(os.path.join(path, additionalString1))

        if additionalString2:
            path = self.CreateSotreArea(os.path.join(path, additionalString2))

        if additionalString3:
            path = self.CreateSotreArea(os.path.join(path, additionalString3))

        # final timestamp folder
        path = self.CreateSotreArea(os.path.join(path, self.dirName))

        return path

    # --------------------------------------------------

    def CreateDirWithDate(self):
        """Create both local log + EOS store directories."""

        logDirName = os.path.join(self.logPath, self.dirName)

        storeAreaDirName1 = self.storeArea
        storeAreaDirName2 = os.path.join(self.storeArea, self.dirName)

        os.makedirs(logDirName, exist_ok=True)

        subprocess.run([
            "xrdfs",
            "root://cmseos.fnal.gov/",
            "mkdir",
            storeAreaDirName1
        ])

        subprocess.run([
            "xrdfs",
            "root://cmseos.fnal.gov/",
            "mkdir",
            storeAreaDirName2
        ])

        print("===> Created directory for log files:", logDirName)
        print("===> Created EOS directory:", storeAreaDirName2)

        return logDirName, storeAreaDirName2