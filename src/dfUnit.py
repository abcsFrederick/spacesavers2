
def delete_unwanted_indexes(lst,unwanted_index_lst):
    for ele in sorted(unwanted_index_lst, reverse = True):
        del lst[ele]

# Swap function
def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

class dfUnit:
    def __init__(self,hash):
        self.hash   = hash  # typically hash_top + "#" + hash_bottom
        self.flist  = []    # list of _ls files with the same has
        self.size   = -1    # total disk space occupied by all duplicates ... total size of (nfiles-symlinks-hardlinks)
        self.ndup   = -1    # files in flist with same size, but different inode (they already have the same hash)
        self.oinode = -1    # if dup then the original (oldest created) inode ... original == first created .. hence not duplicate
        self.ouid   = -1    # if dup then the original (oldest creater) uid ... original == first created .. hence not duplicate
    
    def filter_flist_by_uid(self,uid):
        to_delete = []
        for i,fl in enumerate(self.flist):
            if fl.uid != uid : to_delete.append(i)
        delete_unwanted_indexes(self.flist,to_delete)
    
    def filter_out_symlinks_from_flist(self):
        to_delete = []
        for i,fl in enumerate(self.flist):
            if fl.issyml : to_delete.append(i)
        delete_unwanted_indexes(self.flist,to_delete)
            
    def compute(self,uid,hashhashsplits): # 1. move oldest to the first position 2. find ndup 3. find size 4. filter by uid 5. get depth folder
        if uid != 0: self.filter_flist_by_uid(uid)
        # self.filter_out_symlinks_from_flist() # already done this before
        nf = len(self.flist)

        if nf > 1:
            # if files have same size but different inode .. they are duplicates
            # if flist has different sizes then they should be split into different hash ... as they are NOT duplicates
            to_delete = list()  # make list of redundant inode files to delete ... these are just hardlinks ... ignore for now.
            sizelist = dict()
            for i,j in enumerate(self.flist):
                # if j.issyml: continue
                if not j.size in sizelist: sizelist[j.size] = dict()
                if j.inode in sizelist[j.size]:
                    to_delete.append(i)
                else:
                    sizelist[j.size][j.inode] = 1
            delete_unwanted_indexes(self.flist,to_delete)
            if len(sizelist) != 1:  # multiple sizes found ... split required
                self.size = 0
                self.ndup = 0                
                for i,s in enumerate(sizelist.keys()):
                    tophash, bottomhash = self.hash.split("#")
                    bottomhash += "_" + str(i)
                    newhash = "#".join([tophash,bottomhash])
                    hashhashsplits[newhash] = dfUnit(newhash)
                    for f in self.flist:
                        if f.inode in sizelist[s]:
                            f.xhash_bottom = bottomhash
                            hashhashsplits[newhash].flist.append(f)
            else: # all files are duplicates and have the same hash, same size but different inodes
                self.size = list(sizelist.keys())[0]
                self.ndup = len(sizelist[self.size])
                # bring the earliest created file to the beginning
                earliest_time = -1
                earliest = -1
                for i,j in enumerate(self.flist):
                    if earliest_time == -1: 
                        earliest_time = j.ctime
                        earliest = i
                    elif earliest_time > j.ctime:
                        earliest_time = j.ctime
                        earliest = i
                if earliest > 0: self.flist = swapPositions(self.flist,0,earliest)
                self.oinode = self.flist[0].inode
                self.ouid   = self.flist[0].uid
        elif nf == 1:
                self.size = self.flist[0].size
                self.ndup = 1
        else: # nf == 0
            self.size = 0
            self.ndup = 0
    
    def __str__(self):
        # print("HERE")
        # print(self.hash)
        # print(self.ndup)
        # print(self.size)
        # print("##".join(map(lambda x:str(x),self.flist)))
        # exit()
        return "{0} : {1} {2} {3}".format(self.hash, self.ndup, self.size,"##".join(map(lambda x:str(x),self.flist)))
        