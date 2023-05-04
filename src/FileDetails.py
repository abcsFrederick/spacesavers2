import os
import time
import sys
from pathlib import Path

try:
    import xxhash
except ImportError:
    exit(f"{sys.argv[0]} requires xxhash module")

THRESHOLDSIZE = 1024 * 1024 * 1024
BUFFERSIZE  = 128 * 1024
TB = THRESHOLDSIZE+BUFFERSIZE
SEED = 20230502
MINDEPTH = 3

special_extensions=[".bam",".bai",".bigwig",".bw",".csi"]
SED = dict()                                # special extensions dict
for se in special_extensions:
    SED[se]=1

def convert_time_to_age(t):
    currenttime=int(time.time())
    return int((currenttime - t)/86400)+1 

class FileDetails:
    def __init__(self):
        self.apath 	= ""    # absolute path of file
        self.issyml	= False
        self.size 	= -1
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

    def initialize(self,f,thresholdsize=THRESHOLDSIZE, buffersize=BUFFERSIZE, tb=TB, sed=SED, bottomhash=False):
        self.apath  = Path(f).absolute()                         # path is of type PosixPath
        ext         = self.apath.suffix
        self.issyml	= self.apath.is_symlink()                   # is a symbolic link
        st		    = os.stat(self.apath)                       # gather all stats
        self.size 	= st.st_size                                # size in bytes
        self.dev 	= st.st_dev                                 # Device id
        self.inode 	= st.st_ino                                 # Inode
        self.nlink 	= st.st_nlink		                        # number of hardlinks
        self.atime	= convert_time_to_age(st.st_atime)          # access time
        self.mtime	= convert_time_to_age(st.st_mtime)          # modification time
        self.ctime	= convert_time_to_age(st.st_ctime)          # creation time
        self.uid	= st.st_uid                                 # user id
        self.gid	= st.st_gid                                 # group id
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
            sys.stderr.write("File cannot be read:{}\n".format(self.path))

    def set(self,ls_line):
        ls_line         = ls_line.strip().strip(";").replace("\"","").split(";")
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
        self.size       = int(ls_line.pop(-1))
        issyml = ls_line.pop(-1)
        self.issyml     = issyml == 'True'
        self.apath      = Path(";".join(ls_line))         # sometimes filename have ";" in them ... hence this!
                    
    
    def str_with_name(self,uid2uname,gid2gname):# method for printing output in finddup ... replace "xhash_top;xhash_bottom" with "username;groupname" at the end of the string
        return_str = "\"%s\";"%(self.apath)
        # return_str += "%s;"%(self.issyml)
        return_str += "%d;"%(self.size)
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

    def __str__(self):    
        return_str = "\"%s\";"%(self.apath)
        return_str += "%s;"%(self.issyml)
        return_str += "%d;"%(self.size)
        return_str += "%d;"%(self.dev)
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

    def get_path_at_depth(self,depth):
        abspath = str(self.apath).strip("/").split("/")
        maxd = len(abspath) - 1
        if depth > maxd:
            depth = maxd
        return "/"+"/".join(abspath[:depth])

    def get_paths_at_all_depths(self,maxdepth):
        paths = set()
        for i in range(MINDEPTH,maxdepth+1): 
            paths.add(self.get_path_at_depth(i))
        return paths

    def get_depth(self):
        return len(list(self.apath.parents)) - 1
    
    def get_path(self):
        return self.apath.parents[0]

