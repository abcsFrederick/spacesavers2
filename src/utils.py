import os
from pathlib import Path
import shlex
import subprocess
import sys
import time
from .config import * 

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

def check_readable_file(filename):
    if os.access(filename,os.R_OK):
        return True
    else:
        exit("ERROR: Cannot read file:{}".format(filename))


def get_username_groupname(id):
    if id == 0: return "allusers"
    x = subprocess.run(shlex.split("getent group {}".format(id)),capture_output=True,shell=False,text=True)
    x = x.stdout.strip().split(":")[0]
    if x == "":
        y = subprocess.run(shlex.split("id -nu {}".format(id)),capture_output=True,shell=False,text=True)
        y = y.stdout.strip()
        if y == "":
            name = str(id)
        else:
            name = y
    else:
        name = x
    return name

def get_folder_depth(path):
    return len(list(path.parents))

def get_file_depth(path):
    try:
        return len(list(path.parents))-1
    except:
        print("get_file_depth error for file:\"{}\", type:{}".format(path,type(path)))
        exit()

def get_timestamp(start):
    e = time.time()
    return "%08.2fs"%(e-start)

def print_with_timestamp(start,string,scriptname=os.path.basename(__file__)):
    sys.stdout.write("{0}:{1}:{2}\n".format(scriptname,get_timestamp(start),string))

def get_human_readable_size(bytes):
    hr = str(bytes) + " B"
    kb = float(bytes)/1024.0
    if kb > 1024:
        mb = kb/1024.0
        if mb > 1024:
            gb = mb/1024.0
            if gb > 1024:
                    tb = gb/1024.0
                    hr = "{0:.2f} TiB".format(tb)
            else:
                hr = hr = "{0:.2f} GiB".format(gb)
        else:
            hr = hr = "{0:.2f} MiB".format(mb)
    else:
        hr = "{0:.2f} KiB".format(kb)
    return hr
