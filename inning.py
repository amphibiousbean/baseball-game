class inning:
    def __init__(self):
        self.outs=0
        self.runs_scored=0
        self.hits=0
        self.walks=0
    
    def add_outs(self, num): #param : num is for future integration of double/triple plays
        self.outs+=num

    def add_runs(self, num):
        self.runs_scored+=num

    def add_hit(self):
        self.hits+=1

    def add_walk(self):
        self.walks+=1

    def flush(self): #returns inning results, resets values
        final_state=(self.outs, self.runs_scored, self.hits, self.walks)
        self.outs=0
        self.runs_scored=0
        self.hits=0
        self.walks=0
        return final_state
    
    def print(self):
        print("Outs : " + str(self.outs) + " Hits : " + str(self.hits) + " Walks : " + str(self.walks) + " Runs : " + str(self.runs_scored))