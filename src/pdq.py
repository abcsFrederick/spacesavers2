from pathlib import Path
import sys

def get_type(p): # copy paste from FileDetails
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

class pdq:
    def __init__(self):
        self.inode  = -1
        self.fld    = "u" # u or f or l or d
        self.size   = -1
        self.uid    = 0
    def set(self,p,st_block_byte_size=512):
        p           = Path(p).absolute()
        try:
            st          = p.stat(follow_symlinks=False)
            self.size   = st.st_blocks * st_block_byte_size
            self.inode 	= st.st_ino
            self.uid	= st.st_uid
            self.fld	= get_type(p)
        except:
            print(f"spacesavers2_pdq: {p} File not found!")
    def get_uid(self):
        return self.uid
    def get_fld(self):
        return self.fld
    def is_file(self):
        if self.fld == "f": return True
        return False
    def get_inode(self):
        return self.inode
    def get_size(self):
        return self.size