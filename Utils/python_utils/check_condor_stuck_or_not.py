import subprocess
import sys

sys.path.append("Utils/python_utils/.")
from color_style import style

output = subprocess.run(['condor_q', '-submitter', 'rasharma'], capture_output=True, text=True).stdout

error_check_string = [ 'Server responded with an error',
                       'The remote file is not open']

#Oprint output.split("\t")
lpcschedd = ""
print(type(output))
for outputs in output.split('\n'):
  print(outputs)
  if outputs.find('Submitter') != -1:
    lpcschedd = outputs.split()[2].split('.')[0]
  if outputs.find('rasharma') != -1 and outputs.split()[5] == 'R':
    """This if condition checks the username and if the job is in
    Running (R) condition.
    """
    condor_tail = "condor_tail "+outputs.split()[0]+" -name "+lpcschedd

    print("\n","-"*51,"\n\n")
    print(style.GREEN + outputs+style.RESET+"\n\n")
    print("COMMAND: ",condor_tail)
    print("\n")
    output = subprocess.run(condor_tail.split(), capture_output=True, text=True).stdout

    foundOrNot = any(match in output for match in error_check_string)

    if foundOrNot:
        print(style.RED + "ERROR: Going to kill this job" + style.RESET)
        killCommand = "condor_rm "+outputs.split()[0]+" -name "+lpcschedd
        print(style.RED + "Running Command: " + killCommand + style.RESET)
        subprocess.run(killCommand.split(), check=True)
        print(style.RED + "Successfully killed." + style.RESET)
    else:
        print(output)
print("\n\n")