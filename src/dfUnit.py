import sys
from .utils import *

def get_filename_from_fgzlistitem(string):
    string = string.strip().split(";")[:-1]
    for i in range(9):
        dummy = string.pop(-1)
    filename = ";".join(string)
    return filename


class dfUnit:
    def __init__(self,hash):
        self.hash   = hash  # typically hash_top + "#" + hash_bottom
        self.flist  = []    # list of _ls files with the same hash
        self.fsize  = -1    # size of each file
        self.ndup   = -1    # files in flist with same size, but different inode (they already have the same hash)
        self.size_set   = set()    # set of unique sizes ... if len(size_set) then split is required
        self.uid_list   = []        # list of uids of files added
        self.inode_list = []        # list of inodes of files added
        self.oldest_inode   = -1    # oldest_ ... is for the file which is NOT the duplicate
        self.oldest_index   = -1
        self.oldest_age     = -1
        self.oldest_uid     = -1

    
    def add_fd(self,fd):
        # add the file to flist
        self.flist.append(fd)
        # add size if not already present
        self.size_set.add(fd.size)
        # add uid
        self.uid_list.append(fd.uid)
        # add inode
        self.inode_list.append(fd.inode)
        # update oldest file
        if fd.mtime > self.oldest_age: # current file is older than known oldest
            self.oldest_age     = fd.mtime
            self.oldest_index   = len(self.flist) - 1 # oldest_index is the index of the item last added
            self.oldest_uid     = fd.uid
            self.oldest_inode   = fd.inode

    def filter_flist_by_uid(self,uid):
        for i,f in enumerate(self.flist):
            if f.uid == uid : self.keep.append(i)
                
    def compute(self,hashhashsplits,split_required): # 1. move oldest to the first position 2. find ndup 3. find size 4. filter by uid 5. get depth folder
        # check if spliting is required
        if len(self.size_set) > 1: # more than 1 size in this hash
            split_required = True
            for i,size in enumerate(self.size_set):
                tophash, bottomhash = self.hash.split("#")
                bottomhash += "_" + str(i)
                newhash = "#".join([tophash,bottomhash])        # this is the newhash for this size
                hashhashsplits[newhash] = dfUnit(newhash)
                for fd in self.flist:
                    if fd.size == size:
                        hashhashsplits[newhash].add_fd(fd)
        else: # there only 1 size ... no splits required
            self.ndup   = len(self.inode_list) - 1  #ndup is zero if same size and only 1 inode
            self.fsize  = self.flist[0].size
    
    def get_user_file_index(self,uid):
        uid_file_index = []
        if not uid in self.uid_list:
            if uid == 0: uid_file_index = list(range(0,len(self.flist)))
            return uid_file_index
        else:
            for i,j in enumerate(self.flist):
                if j.uid == uid: uid_file_index.append(i)
            return uid_file_index


    
    def __str__(self):
        return "{0} : {1} {2} {3}".format(self.hash, self.ndup, self.fsize,"##".join(map(lambda x:str(x),self.flist)))
        
    def str_with_name(self,uid2uname, gid2gname,findex):
        return "{0} : {1} {2} {3}".format(self.hash, self.ndup, self.fsize,"##".join(map(lambda x:x.str_with_name(uid2uname,gid2gname),[self.flist[i] for i in findex])))


class fgz: # used by grubber
    def __init__(self):
        self.hash = ""
        self.ndup = -1
        self.filesize = -1
        self.totalsize = -1
        self.fds = []
    
    def __lt__(self,other):
        return self.totalsize > other.totalsize
    
    def __str__(self):
        outstring=[]
        outstring.append(str(self.hash))
        outstring.append(str(self.ndup))
        outstring.append(get_human_readable_size(self.totalsize))
        outstring.append(get_human_readable_size(self.filesize))
        outstring.append(";".join(map(lambda x:get_filename_from_fgzlistitem(x),self.fds)))
        return "\t".join(outstring)
        # return "{0} {1} {2} {3} {4}".format(self.hash,self.ndup,get_human_readable_size(self.totalsize), get_human_readable_size(self.filesize), ";".join(map(lambda x:get_filename_from_fgzlistitem(x),self.fds)))
        # return "{0} {1} {2} {3} {4}".format(self.hash,self.ndup,self.totalsize, self.filesize, ";".join(map(lambda x:get_filename_from_fgzlistitem(x),self.fds)))

# 09f9599cff76f6c82a96b042d67f81ff#09f9599cff76f6c82a96b042d67f81ff : 158 1348 "/data/CCBR/projects/ccbr583/Pipeliner/.git/hooks/pre-push.sample";1348;41;8081532070425347857;1;1552;35069;57786;jailwalapa;CCBR;##"/data/CCBR/projects/ccbr785/FREEC/.git/hooks/pre-push.sample";1348;41;11610558684702129747;1;1629;35069;57786;jailwalapa;CCBR;##"/data/CCBR/projects/ccbr785/citup/pypeliner/.git/hooks/pre-push.sample";1348;41;9306919632329364056;1;1624;35069;57786;jailwalapa;CCBR;##"/data/CCBR/projects/ccbr785/titan_workflow/.git/hooks/pre-push.sample";1348;41;7658100918611057517;1;1628;35069;57786;jailwalapa;CCBR;##"/data/CCBR/rawdata/ccbr1016/batch1/fastq/scratch/example/Pipeliner/.git/hooks/pre-push.sample";1348;41;328973360624494807;1;1253;35069;57786;jailwalapa;CCBR;##"/data/CCBR/rawdata/ccbr1040/Seq2n3n4n5_GEXnHTO/Pipeliner/.git/hooks/pre-push.sample";1348;41;16190385205193530167;1;1093;35069;57786;jailwalapa;CCBR;##"/data/CCBR/rawdata/ccbr1044/Pipeliner/.git/hooks/pre-push.sample";1348;41;10429578581567757002;1;1110;35069;57786;jailwalapa;CCBR;    
    def set(self,inputline):
        original_line = inputline
        try:
            inputline = inputline.strip().split(" ")
            if len(inputline) < 5:
                raise Exception("Less than 5 items in the line.")
            self.hash = inputline.pop(0)
            dummy = inputline.pop(0)
            total_ndup = int(inputline.pop(0))
            if total_ndup == 0: # may be finddup was run to output all files .. not just dups
                return False
            self.filesize = int(inputline.pop(0))
            full_fds = " ".join(inputline)
            fds = full_fds.split("##")
            self.ndup = len(fds) # these are user number of duplicates/files
            if self.ndup == (total_ndup + 1): # one file is the original ... other are all duplicates
                dummy = fds.pop(0)
                self.ndup -= 1
            self.fds = fds
            self.totalsize = self.ndup * self.filesize
            return True
        except:
            sys.stderr.write("spacesavers2:{0}:files.gz Do not understand line:{1} with {2} elements.\n".format(self.__class__.__name__,original_line,len(inputline)))
            # exit()            
            return False


class FileDetails2:
    def __init__(self):
        self.apath = ""
        self.size = -1
        self.dev = -1
        self.inode = -1
        self.nlink = -1
        self.mtime = -1
        self.uid = -1
        self.gid = -1
        self.uname = ""
        self.gname = ""
    
    def set(self,fgzline):
        original_fgzline=fgzline
        # print(ls_line)
        try:
            fgzline         = fgzline.strip().replace("\"","").split(";")[:-1]
            if len(fgzline) < 10:
                raise Exception("Less than 10 items in the line.")
            self.gname      = fgzline.pop(-1)
            self.uname      = fgzline.pop(-1)
            self.gid        = int(fgzline.pop(-1))
            self.uid        = int(fgzline.pop(-1))
            self.mtime      = int(fgzline.pop(-1)) 
            self.nlink      = int(fgzline.pop(-1))
            self.inode      = int(fgzline.pop(-1))
            self.dev        = int(fgzline.pop(-1))
            self.size       = int(fgzline.pop(-1))
            apath           = ";".join(fgzline)
            apath           = apath.strip("\"")
            self.apath      = Path(apath)         # sometimes filename have ";" in them ... hence this!
            return True
        except:
            sys.stderr.write("spacesavers2:{0}:catalog Do not understand line:\"{1}\" with {2} elements.\n".format(self.__class__.__name__,original_fgzline,len(fgzline)))
            # exit()            
            return False        

class fgzblamer: # used by blamematrix
    def __init__(self):
        self.hash = ""
        self.ndup = -1
        self.users = set()
        self.folders = set()
        self.bm = dict()
        self.fds = []
    
    def set(self,inputline,depth):
        original_line = inputline
        try:
            inputline = inputline.strip().split(" ")
            if len(inputline) < 5:
                raise Exception("Less than 5 items in the line.")
            self.hash = inputline.pop(0)
            dummy = inputline.pop(0)
            self.ndup = int(inputline.pop(0))
            if self.ndup == 0 or self.ndup == 1: return False                       
            self.filesize = int(inputline.pop(0))
            full_fds = " ".join(inputline)
            fds = full_fds.split("##")
            for f in fds:
                fd = FileDetails2()
                fd.set(f)
                self.users.add(fd.uname)
                fad=get_folder_at_depth(fd.apath,depth)
                self.folders.add(fad)
                if not fd.uname in self.bm:
                    self.bm[fd.uname] = dict()
                if not fad in self.bm[fd.uname]:
                    self.bm[fd.uname][fad] = 0
                self.bm[fd.uname][fad] += self.filesize
            self.fds = []
            return True
        except:
            sys.stderr.write("spacesavers2:{0}:files.gz Do not understand line:{1} with {2} elements.\n".format(self.__class__.__name__,original_line,len(inputline)))
            # exit()            
            return False
