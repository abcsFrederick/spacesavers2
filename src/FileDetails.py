import os
import time
import sys
from pathlib import Path
from .utils import *

try:
    import xxhash
except ImportError:
    exit(f"{sys.argv[0]} requires xxhash module")

THRESHOLDSIZE = 1024 * 1024 * 1024  # 1 MiB
BUFFERSIZE  = 128 * 1024            # 128 KiB
TB = THRESHOLDSIZE+BUFFERSIZE
SEED = 20230502
MINDEPTH = 3

special_extensions=[".bam",".bai",".bigwig",".bw",".csi"]
SED = dict()                                # special extensions dict
for se in special_extensions:
    SED[se]=1

def convert_time_to_age(t):
    currenttime = int(time.time())
    age = int((currenttime - t)/86400)+1
    if age < 0: age = 0
    return age

def get_type(p):
    # input:
    # 1. PosixPath object
    # output:
    # 1. type of path
    #   u = unknown
    #   L = broken symlink
    #   l = symlink
    #   f = file
    #   d = folder or directory
    x = "u" # unknown
    try:
        if p.is_symlink():
            x = "l" # link or symlink
            try:
                p.exists()
            except:
                x = "L" # upper case L is broken symlink
                sys.stderr.write("spacesavers2:Broken symlink found:{}\n".format(p))
            return x
        if not p.exists():
            x = "a" # absent
            return x
        if p.is_dir():
            x = "d" # directory
            return x
        if p.is_file():
            x = "f" # file
            return x
    except: # mainly to catch PermissionError:
        sys.stderr.write("spacesavers2:File cannot be read:{}\n".format(p))
    return x

class FileDetails:
    def __init__(self):
        self.apath 	= ""    # absolute path of file
        self.fdl	= "u"   # is it file or directory or link or unknown or absent ... values are f d l u a
        self.size 	= -1
        self.calculated_size = -1
        self.calculated_size_human_readable = ""
        self.dev 	= -1
        self.inode 	= -1
        self.nlink 	= -1
        self.atime	= -1
        self.mtime	= -1
        self.ctime	= -1
        self.uid	= -1
        self.gid	= -1
        self.xhash_top      = ""
        self.xhash_bottom   = ""

    def initialize(self,f,thresholdsize=THRESHOLDSIZE, buffersize=BUFFERSIZE, tb=TB, sed=SED, bottomhash=False,st_block_byte_size=512):
        self.apath  = Path(f).absolute()                         # path is of type PosixPath
        ext         = self.apath.suffix
        self.fld	= get_type(self.apath)                      # get if it is a file or directory or link or unknown or absent
        st          = self.apath.stat(follow_symlinks=False)    # gather stat results
        self.size 	= st.st_size                                # size in bytes
        self.calculated_size    = st.st_blocks * st_block_byte_size            # st_blocks gives number of 512 bytes blocks used
        self.calculated_size_human_readable = get_human_readable_size(self.calculated_size)
        self.dev 	= st.st_dev                                 # Device id
        self.inode 	= st.st_ino                                 # Inode
        self.nlink 	= st.st_nlink		                        # number of hardlinks
        self.atime	= convert_time_to_age(st.st_atime)          # access time
        self.mtime	= convert_time_to_age(st.st_mtime)          # modification time
        self.ctime	= convert_time_to_age(st.st_ctime)          # change time
        self.uid	= st.st_uid                                 # user id
        self.gid	= st.st_gid                                 # group id
        if self.fld == "f":
            try:
                with open(self.apath,'rb') as fh:
                    if ext in sed:
                        if self.size > tb:
                            data = fh.read(thresholdsize)
                            data = fh.read(buffersize)
                            self.xhash_top = xxhash.xxh128(data,seed=SEED).hexdigest()
                            if bottomhash:
                                fh.seek(-1 * buffersize,2)
                                data = fh.read(buffersize)
                                self.xhash_bottom = xxhash.xxh128(data,seed=SEED).hexdigest()
                            else:
                                self.xhash_bottom = self.xhash_top
                        else:
                            data = fh.read()
                            self.xhash_top = xxhash.xxh128(data,seed=SEED).hexdigest()
                            self.xhash_bottom = self.xhash_top
                    else:
                        if self.size > buffersize:
                            data = fh.read(buffersize)
                            self.xhash_top = xxhash.xxh128(data,seed=SEED).hexdigest()
                            if bottomhash:
                                fh.seek(-1 * buffersize,2)
                                data = fh.read(buffersize)
                                self.xhash_bottom = xxhash.xxh128(data,seed=SEED).hexdigest()
                            else:
                                self.xhash_bottom = self.xhash_top
                        else:
                            data = fh.read()
                            self.xhash_top = xxhash.xxh128(data,seed=SEED).hexdigest()
                            self.xhash_bottom = self.xhash_top
            except:
                sys.stderr.write("spacesavers2:{}:File cannot be read:{}\n".format(self.__class__.__name__,str(self.apath)))

    def set(self,ls_line):
        original_ls_line=ls_line
        # print(ls_line)
        try:
            ls_line         = ls_line.strip().replace("\"","").split(";")[:-1]
            if len(ls_line) < 13:
                raise Exception("Less than 13 items in the line.")
            self.xhash_bottom   = ls_line.pop(-1)
            self.xhash_top      = ls_line.pop(-1)
            self.gid        = int(ls_line.pop(-1))
            self.uid        = int(ls_line.pop(-1))
            self.ctime      = int(ls_line.pop(-1))
            self.mtime      = int(ls_line.pop(-1)) 
            self.atime      = int(ls_line.pop(-1))
            self.nlink      = int(ls_line.pop(-1))
            self.inode      = int(ls_line.pop(-1))
            self.dev        = int(ls_line.pop(-1))
            self.calculated_size       = int(ls_line.pop(-1))
            self.size       = int(ls_line.pop(-1))
            self.fld        = ls_line.pop(-1)
            self.apath      = Path(";".join(ls_line))         # sometimes filename have ";" in them ... hence this!
            return True
        except:
            sys.stderr.write("spacesavers2:{0}:catalog Do not understand line:\"{1}\" with {2} elements.\n".format(self.__class__.__name__,original_ls_line,len(ls_line)))
            # exit()            
            return False
    
    def str_with_name(self,uid2uname,gid2gname):# method for printing output in mimeo ... replace "xhash_top;xhash_bottom" with "username;groupname" at the end of the string
        # return_str = "\"%s\";"%(self.apath)
        # path may have newline char which should not be interpretted as new line char
        return_str = "\"%s\";"%(str(self.apath).encode('unicode_escape').decode('utf-8'))
        return_str += "%s;"%(self.fld)
        return_str += "%d;"%(self.size)
        return_str += "%d;"%(self.calculated_size)
        return_str += "%d;"%(self.dev)
        return_str += "%d;"%(self.inode)
        return_str += "%d;"%(self.nlink)
        # return_str += "%d;"%(self.atime)
        return_str += "%d;"%(self.mtime)
        # return_str += "%d;"%(self.ctime)
        return_str += "%d;"%(self.uid)
        return_str += "%d;"%(self.gid)
        return_str += "%s;"%(uid2uname[self.uid])
        return_str += "%s;"%(gid2gname[self.gid])
        return return_str

    def get_filepath(self):
        return "\"%s\""%(str(self.apath).encode('unicode_escape').decode('utf-8'))

    def __str__(self):    
        # return_str = "\"%s\";"%(self.apath)
        # path may have newline char which should not be interpretted as new line char
        return_str = "\"%s\";"%(str(self.apath).encode('unicode_escape').decode('utf-8'))
        return_str += "%s;"%(self.fld)
        return_str += "%d;"%(self.size)
        return_str += "%d;"%(self.calculated_size)
        return_str += "%d;"%(self.dev) # device id
        return_str += "%d;"%(self.inode)
        return_str += "%d;"%(self.nlink)
        return_str += "%d;"%(self.atime)
        return_str += "%d;"%(self.mtime)
        return_str += "%d;"%(self.ctime)
        return_str += "%d;"%(self.uid)
        return_str += "%d;"%(self.gid)
        return_str += "%s;"%(self.xhash_top)
        return_str += "%s;"%(self.xhash_bottom)
        return return_str

    def get_paths_at_all_depths(self): # for files and folders
        p = self.apath
        paths = []
        if self.fld == "d":
            paths.append(p)
        paths.extend(p.parents[:-1])    # remove the last one ... which will be '/'
        return paths

    def get_paths(self,mindepth,maxdepth):
        paths = self.get_paths_at_all_depths()
        paths = list(filter(lambda x:get_folder_depth(x) <= maxdepth,paths))
        paths = list(filter(lambda x:get_folder_depth(x) >= mindepth,paths))
        return paths

    def get_depth(self):
        p = self.apath
        try:
            if p.is_dir(): # folder
                return len(list(p.parents))
            else: # file
                return len(list(p.parents)) - 1
        except:
            print('get_file_depth error for file:"{}", type:{}'.format(p, type(p)))
            return -1
    
    def get_type(self):
        return self.fld
    
    def get_userid(self):
        return self.uid

    def get_age(self):
        return self.mtime
    
    def get_size(self):
        return self.calculated_size
    
    def get_size_human_readable(self):
        return self.calculated_size_human_readable