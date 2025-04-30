class scoreboard:
    def __init__(self):
        self.runs=0
        self.hits=0
        self.walks=0
        self.by_inning_runs=[] #list for tracking runs per inning
        self.inning=0
        self.curr_inning_runs=0

    def add_runs(self, num):
        self.runs+=num
        self.curr_inning_runs+=num
        self.by_inning_runs[self.inning-1]=self.curr_inning_runs

    def add_hit(self):
        self.hits+=1

    def add_walk(self):
        self.walks+=1

    def new_inning(self):
        self.inning+=1
        self.by_inning_runs.append(0)
        self.curr_inning_runs=0

    def print(self):
        print(self.make_display())

    def make_display(self):

        dis="{:<3}".format("")
        for x in range(9):
            if x < len(self.by_inning_runs):
                dis += "{:<3}".format(str(self.by_inning_runs[x]))
            else:
                dis += "{:<3}".format("")
        dis += "{:<3}".format(str(self.runs))
        dis += "{:<3}".format(str(self.hits))
        dis+="\n"
        return dis
        
