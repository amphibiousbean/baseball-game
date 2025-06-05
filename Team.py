import Pitcher as Pitcher
import Batter as Batter


class Team:

    def __init__(self, name, lineup, starter):
        if len(lineup) < 9:
            raise ValueError(f"Passed lineup does not contain enough players. 9 players required, {len(lineup)} given.")
        
        self.name = name
        self.lineup = self.makeLineup(lineup)
        self.starter = self.makeStarter(starter)
        #self.bench = self.makeBench()
        #self.bullpen = self.makeBullpen()
        self.upnext = 0 #current spot in lineup


    def makeLineup(self,lineup):
        batters = []

        for player in lineup:
            batters.append(Batter.Batter(player))
       
        return batters


    def makeBench(self):
        pass
        bench = []

        for x in range(5):
            bench.append(Batter.Batter("Joe Shmo", 40, 40, 40 ,40))
        
        return bench

    def next_spot(self): #next spot in the batting order. returns the current spot and increments lineup position
        r=self.upnext
        if self.upnext < 8: 
            self.upnext+=1
        else:
            self.upnext=0
        return r


    def makeStarter(self,pitcher):

        return Pitcher.Pitcher(pitcher)
    
    def makeBullpen(self):
        pass
        bullpen = []
        bullpen.append(Pitcher.Pitcher("Jane Doe", 40, 40, 40, 40, 40, 40, {"Fastball" : 50, "Slider" : 50, "Sinker" : 50}))
        return bullpen
    
    def str(self, detail=False):
        if detail:
            return self._strDetailed()
        else:
            return self._strBasic()

    def _strDetailed(self):
        s = ""
        s += "Starting Pitcher\n\n" + self.starter.str() + "\n\nLineup\n\n"

        lineup_txt="{:<25} {:<3} {:<3} {:<3} {:<3}"
        s += lineup_txt.format("Name","Pow","Con","Vis","Dis")
        for batter in self.lineup:
            s += "\n"+batter.str(label=False)
        
        '''
        bench = ""
        for player in  self.bench:
            bench += player.name + "\n"
        s += bench + "\nBullpen\n\n"
        
        bullpen = ""
        for pitcher in self.bullpen:
            bullpen += pitcher.name + "\n"
        s += bullpen 
        '''

        return s
    
    def _strBasic(self):

        s = ""
        s += "Starting Pitcher\n\n" + self.starter.name + "\n\nLineup\n\n"

        lineup = ""
        for batter in self.lineup:
            lineup += batter.name + "\n"
        s += lineup + "\n"

        '''
        bench = ""
        for player in  self.bench:
            bench += player.name + "\n"
        s += bench + "\nBullpen\n\n"
        
        bullpen = ""
        for pitcher in self.bullpen:
            bullpen += pitcher.name + "\n"
        s += bullpen 
        '''

        return s