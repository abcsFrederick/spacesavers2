import os
from pathlib import Path

def which(program):
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def check_writeable_folder(folder):
    try:
        Path(folder).mkdir(parents=True,exist_ok=True)
    except PermissionError:
        exit("ERROR: {} folder cannot be created! Check your permissions!".format(folder))
    if not os.access(folder,os.W_OK):
        exit("ERROR: {} folder exists but cannot be written to".format(folder))

def check_readable_file(file):
    return os.access(file,os.R_OK)

