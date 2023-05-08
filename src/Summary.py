wAge = 0.25
wDup = 0.45
wOcc = 0.35

def scored(age,bytes):
    ageScore = 1.0
    s1 = 0.1
    s2 = 0.8
    if age <= 180: # < 6months
        ageScore = (age/180) * s1
    elif age < 720: # < 24 months
        age = age - 180
        ageScore = s1 + ((age/540) * s2)
    elif age <= 1000:
        age = age - 720
        ageScore = s1 + s2 + ((age/280) * (1 - (s1+s2)))
    try:
        score = (bytes * ageScore) / (bytes)
    except ZeroDivisionError:
        score = (ageScore / age)
    return score


class Summary:
    def __init__(self,path):
        self.path = path
        self.non_dup_Bytes = []
        self.dup_Bytes = []
        self.non_dup_ages = []
        self.dup_ages = []
        self.non_dup_age_scores = []
        self.dup_age_scores = []
        self.AgeScore = -1
        self.DupScore = -1
        self.OccScore = -1
        self.OverallScore = -1

    def update_scores(self,quota):
        dup_Bytes = sum(self.dup_Bytes)
        tot_Bytes = sum(self.non_dup_Bytes) + dup_Bytes
        self.non_dup_age_scores = list(map(lambda x,y:scored(x,y),self.non_dup_ages,self.non_dup_Bytes))
        self.dup_age_scores = list(map(lambda x,y:scored(x,y),self.dup_ages,self.dup_Bytes))
        try:
            self.AgeScore = (sum(self.non_dup_age_scores) + sum(self.dup_age_scores)) / (len(self.non_dup_age_scores) + len(self.dup_age_scores)) 
        except ZeroDivisionError:
            self.AgeScore = 0
        try:
            self.DupScore = float(dup_Bytes) / tot_Bytes
        except ZeroDivisionError:
            self.DupScore = 1
        self.OccScore = 1.0
        quota_5perc = float(0.05*quota)
        if tot_Bytes <= quota_5perc:
            self.OccScore = tot_Bytes / quota_5perc
            # print(quota_5perc,tot_Bytes,self.OccScore)
        
        self.AgeScore = wAge * self.AgeScore
        self.DupScore = wDup * self.DupScore
        self.OccScore = wOcc * self.OccScore
        self.OverallScore = int(100 - 100 * (self.AgeScore + self.DupScore + self.OccScore))
    
    def __str__(self):
        dup_Bytes = sum(self.dup_Bytes)
        tot_Bytes = sum(self.non_dup_Bytes) + dup_Bytes
        try:
            dup_mean_age = sum(self.dup_ages)/len(self.dup_ages)
        except ZeroDivisionError:
            dup_mean_age = 0
        try:
            tot_mean_age = (sum(self.dup_ages) + sum(self.non_dup_ages))/(len(self.dup_ages)+len(self.non_dup_ages))
        except ZeroDivisionError:
            tot_mean_age = 0
        dup_files = len(self.dup_Bytes)
        tot_files = dup_files + len(self.non_dup_Bytes)
        return_str = str(self.path)+"\t"
        return_str += "%d\t"%(tot_Bytes)
        return_str += "%d\t"%(dup_Bytes)
        try:
            return_str += "%.2f\t"%(dup_Bytes*100.0/tot_Bytes)
        except ZeroDivisionError:
            return_str += "%.2f\t"%(0)
        return_str += "%d\t"%(tot_files)
        return_str += "%d\t"%(dup_files)
        try:
            return_str += "%.2f\t"%(dup_files*100.0/tot_files)
        except ZeroDivisionError:
            return_str += "%.2f\t"%(0)
        return_str += "%.2f\t"%(tot_mean_age)
        return_str += "%.2f\t"%(dup_mean_age)
        return_str += "%.4f\t"%(self.AgeScore)
        return_str += "%.4f\t"%(self.DupScore)
        return_str += "%.4f\t"%(self.OccScore)
        return_str += "%d"%(self.OverallScore)
        return return_str

