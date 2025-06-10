import collections
from config import PRINT
class bases:
    
    def __init__(self, runners):
        if runners: #if inputting a runner state for testing
            self.runners=collections.deque(runners)
        else:  
            self.runners=collections.deque([None]*3) #fixed length queue, will contain batters.


    #updates the bases based on an event. returns runs scored on the update.
    def update_hit(self, num_bases, batter):
        #needs to add runners incrementally. 
        # ie: on a bases empty double, the runner will be first added, then a None type will be added.
        # so the bases would look like thi: [None, None, None] -> [batter, None, None] -> [None, batter, None].
        # hits with men on base would look like this : [batter1, None, None] -> [batter2, batter1, None] -> [None, batter2, batter1]
        # when a batter is popped off the queue, add 1 to the runs counter.
        runs=0
        popped=self.enqueue_hit(batter)
        if(popped):
            runs+=1
        while num_bases > 1:
            popped=self.enqueue_hit(None)
            if(popped):
                runs+=1
            num_bases-=1
        return runs
    
    def update_walk(self, batter): #returns runs scored
        runs=0
        if self.enqueue_walk(batter):
            runs+=1
        return runs


    #pops end element off, returns what it was, adds the next element
    def enqueue_hit(self, next):
        popped=self.runners.pop()
        self.runners.appendleft(next.name if next else None)
        if PRINT:
            print(str(self.runners))
        return popped
    
    def enqueue_walk(self, batter): #returns None if no
        if not self.runners[0]: #1st open
            self.runners[0] = batter.name
            return None
        elif not self.runners[1]: #1st+3rd, 1st [x, None, y] -> [z, x, y], [x,None,None] -> [z,x,None]
            self.runners[1]=self.runners[0]
            self.runners[0]=batter.name
            return None
        else: #1st+2nd, bases loaded
            popped=self.runners.pop()
            self.runners.appendleft(batter.name if batter else None)
            return popped

    def print(self):
        if PRINT:
            print(str(self.runners))

    def flush(self): #clears bases for a new inning
        self.runners=collections.deque([None]*3)

        