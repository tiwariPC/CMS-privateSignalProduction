import os
import subprocess
from datetime import datetime


CURRENT_DATETIME = datetime.now()


class FileHelper:
    """Helper class to manage ROOT files and EOS directory mirroring."""

    def __init__(self, input_directory_path, output_directory_path, ifeos=False):
        self.ifeos = ifeos
        self.InputDirectoryPath = input_directory_path
        self.OutputDirectoryPath = output_directory_path

        self.AllSubDirectoryLists = []
        self.ListOfAllInputRootFiles = []
        self.ListOfAllOutputRootFiles = []

    def list_files(self):
        """Collect all .root files and subdirectories."""
        for root, directories, filenames in os.walk(self.InputDirectoryPath):
            self.AllSubDirectoryLists.append(root)

            for filename in filenames:
                if filename.endswith(".root"):
                    file_with_path = os.path.join(root, filename)
                    self.ListOfAllInputRootFiles.append(file_with_path)

    def CreateSameHirarcyDirsSameAsListFiles(self):
        """
        Recreate same directory hierarchy in output EOS area.
        """
        if self.InputDirectoryPath.endswith("/"):
            replace_string = self.InputDirectoryPath.split("/")[-2]
        else:
            replace_string = self.InputDirectoryPath.split("/")[-1]

        directory_path_to_replace = self.InputDirectoryPath.replace(replace_string, "")

        for directory in self.AllSubDirectoryLists:
            new_directory_name = directory.replace(
                directory_path_to_replace,
                self.OutputDirectoryPath.rstrip("/") + "/"
            )

            subprocess.run(["eos", "root://cmseos.fnal.gov", "mkdir", "-p", new_directory_name], check=True)

    def GetOutPutFileList(self):
        """
        Build output file paths corresponding to input ROOT files.
        """
        if self.InputDirectoryPath.endswith("/"):
            replace_string = self.InputDirectoryPath.split("/")[-2]
        else:
            replace_string = self.InputDirectoryPath.split("/")[-1]

        directory_path_to_replace = self.InputDirectoryPath.replace(replace_string, "").replace("//", "/")

        self.ListOfAllOutputRootFiles = [
            f.replace(
                directory_path_to_replace,
                self.OutputDirectoryPath.rstrip("/") + "/"
            )
            for f in self.ListOfAllInputRootFiles
        ]