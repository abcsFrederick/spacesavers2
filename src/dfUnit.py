import numpy

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
