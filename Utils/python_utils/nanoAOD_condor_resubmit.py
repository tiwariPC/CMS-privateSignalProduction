import os
import shutil
import subprocess
from optparse import OptionParser
import ROOT
from ROOT import TFile

DEBUG = False


def files_to_remove(files, directory):
    filelist_to_remove = []

    for file in files:
        tfile = None
        try:
            tfile = TFile.Open(file)
        except Exception:
            pass

        if tfile and not tfile.IsZombie():
            tfile.Close()
        else:
            print("File could not be opened or is zombie:", file)
            filelist_to_remove.append(file)

    if DEBUG:
        print(filelist_to_remove)

    return filelist_to_remove


def list_files(file_name):
    file_list = []
    with open(file_name) as f:
        for line in f:
            if "USER_" in line:
                start_pt = line.find("output")
                end_pt = line.find(".root", start_pt + 1)
                res = line[start_pt:end_pt + 5]

                if "/" in res:
                    res = res[res.find("/") + 1:]

                file_list.append(res)

    return file_list


def get_files_from_submit(path_submit):
    import re
    with open(path_submit) as myfile:
        content = myfile.read()

    return re.findall(r"[a-zA-Z0-9-]+\.root", content)


def list_root(directory):
    flist = []
    flistWithPath = []

    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".root"):
                flist.append(filename.replace("_SkimHadd", ""))
                flistWithPath.append(os.path.join(root, filename))

    return flist, flistWithPath


def submit_missing(InputSubmitFile, resubmit=True):
    bashCommand = ["condor_submit", InputSubmitFile]

    if resubmit:
        print("Resubmitting now!")
        subprocess.run(bashCommand)
    else:
        print("Ready to resubmit. Set resubmit=True to proceed:")
        print(" ".join(bashCommand))


def prepare_runJobs_missing(FailedJobRootFile, InputSubmitFile, CondorLogDir, EOSDir, Resubmit_no):

    if DEBUG:
        print("FailedJobRootFile:", FailedJobRootFile)
        print("InputSubmitFile:", InputSubmitFile)
        print("CondorLogDir:", CondorLogDir)
        print("EOSDir:", EOSDir)

    shutil.copy2(InputSubmitFile, f"original_{InputSubmitFile}")

    outsubmit_fileName = InputSubmitFile.replace(".submit", "") + f"_resubmit_{Resubmit_no}.submit"

    with open(InputSubmitFile) as myfile:
        head = [next(myfile) for _ in range(7)]  # FIXED (no xrange)

    with open(outsubmit_fileName, "w") as outsubmit_file:
        for lines in head:
            outsubmit_file.write(lines)

        for RootFiles in FailedJobRootFile:

            grep_cmd = f"grep {RootFiles.replace('.root','')} {CondorLogDir}/*.stdout"
            grep_stdout_files = subprocess.run(grep_cmd.split(), capture_output=True, text=True).stdout

            OldRefFile = ""

            if grep_stdout_files.strip():
                base = grep_stdout_files.strip().split(':')[0].replace('.stdout', '')

                parts = base.split('_')
                if len(parts) > 2 and parts[-2] == "resubmit":
                    OldRefFile = parts[-4]
                else:
                    OldRefFile = parts[-1]

            grep_submit_cmd = f'grep -A1 -B3 "{RootFiles}" {InputSubmitFile}'
            grep_condor_submit_part = subprocess.run(grep_submit_cmd.split(), capture_output=True, text=True).stdout

            updateString = grep_condor_submit_part.replace(
                '$(Process)',
                OldRefFile + '_$(Process)_resubmit_' + Resubmit_no
            )

            outsubmit_file.write(updateString)

    return outsubmit_fileName


def main():
    parser = OptionParser()

    parser.add_option("-d", "--dir", dest="dir",
                      default="task_config.json", help="directory")

    parser.add_option("-s", "--stage-dest", dest="stage_dest",
                      help="directory output files were staged to")

    parser.add_option("-i", "--input", dest="input",
                      default="all_root.submit", help="input submit file")

    parser.add_option("-r", "--resubmit", action="store_false",
                      dest="resubmit", default=True, help="resubmit")

    parser.add_option("-n", "--resubmit_no", dest="resubmit_no",
                      default=1, help="resubmit counter")

    (options, args) = parser.parse_args()

    stageDir = os.path.abspath(options.stage_dest) if options.stage_dest else os.getcwd()

    full_output = get_files_from_submit(options.input)
    present_output, present_output_WithPath = list_root(stageDir)

    print("length(submit file):", len(full_output))
    print("Length(output root file):", len(present_output))

    not_finished = list(set(full_output) - set(present_output))

    corrupted_files = files_to_remove(present_output_WithPath, stageDir)
    not_finished += corrupted_files

    print("Missing files:", not_finished)
    print("Number missing:", len(not_finished))

    submitfile = prepare_runJobs_missing(
        not_finished,
        options.input,
        options.dir,
        stageDir,
        str(options.resubmit_no)
    )

    print("Submitting:", submitfile)
    submit_missing(submitfile, options.resubmit)


if __name__ == "__main__":
    main()