import os
from pathlib import Path
import shlex
import subprocess

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

def get_username_groupname(id):
    if id == 0: return "allusers"
    # x = subprocess.run(shlex.split("id -nu {}".format(uid)),capture_output=True,shell=False,text=True)
    x = subprocess.run(shlex.split("getent group {}".format(id)),capture_output=True,shell=False,text=True)
    x = x.stdout.strip().split(":")[0]
    return x

def get_folder_depth(path):
    return len(list(path.parents))

def get_file_depth(path):
    return len(list(path.parents))-1

