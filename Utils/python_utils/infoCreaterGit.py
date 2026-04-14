import os
import subprocess


class BasicInfoCreater:
    """Creates git + CMSSW summary logs and patches."""

    GITPATCH = "gitDiff.patch"

    def __init__(self, logFileName="summary.dat", optionalString=""):
        self.CMSSWDirPath = os.environ.get("CMSSW_BASE", "")
        self.CMSSWRel = self.CMSSWDirPath.split("/")[-1] if self.CMSSWDirPath else ""
        self.logFileName = logFileName
        self.optionalString = optionalString

    # -----------------------------
    def GenerateGitLog(self):
        with open(self.logFileName, "w") as outScript:
            outScript.write(f"CMSSW Version used: {self.CMSSWRel}\n")
            outScript.write(f"Current directory path: {self.CMSSWDirPath}\n")
            outScript.write(f"Summary for current setup: {self.optionalString}\n")

        with open(self.logFileName, "a") as f:
            subprocess.run(
                'echo -e "\n\n============\n== Latest commit summary\n\n"',
                shell=True,
                stdout=f
            )

            subprocess.run(
                "git log -1 --pretty=tformat:' Commit: %h %n Date: %ad %n Relative time: %ar %n Commit Message: %s'",
                shell=True,
                stdout=f
            )

            subprocess.run('echo -e "\n\n============\n"', shell=True, stdout=f)

            subprocess.run(
                'git log -1 --format="SHA: %H"',
                shell=True,
                stdout=f
            )

    # -----------------------------
    def GenerateGitPatch(self):
        subprocess.run(["git", "diff"], stdout=open(self.GITPATCH, "w"))

    # -----------------------------
    def GenerateGitPatchAndLog(self):
        self.GenerateGitPatch()

        with open(self.logFileName, "w") as outScript:
            outScript.write(f"\nCMSSW Version used: {self.CMSSWRel}\n")
            outScript.write(f"\nCurrent directory path: {self.CMSSWDirPath}\n")
            outScript.write(f"\nSummary for current setup: {self.optionalString}\n")

        with open(self.logFileName, "a") as f:
            subprocess.run(
                'echo -e "\n\n============\n== Latest commit summary\n\n"',
                shell=True,
                stdout=f
            )

            subprocess.run(
                "git log -1 --pretty=tformat:' Commit: %h %n Date: %ad %n Relative time: %ar %n Commit Message: %s'",
                shell=True,
                stdout=f
            )

            subprocess.run('echo -e "\n\n============\n"', shell=True, stdout=f)

            subprocess.run(
                'git log -1 --format="SHA: %H"',
                shell=True,
                stdout=f
            )

    # -----------------------------
    def SendGitLogAndPatchToEos(self, outputFolder):
        print(f"\nCopying {self.logFileName} to: {outputFolder}")
        subprocess.run([
            "xrdcp", "-f",
            self.logFileName,
            f"root://cmseos.fnal.gov/{outputFolder}/{self.logFileName}"
        ])

        print(f"\nCopying {self.GITPATCH} to: {outputFolder}")
        subprocess.run([
            "xrdcp", "-f",
            self.GITPATCH,
            f"root://cmseos.fnal.gov/{outputFolder}/{self.GITPATCH}"
        ])