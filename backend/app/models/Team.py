import backend.app.models.Pitcher as Pitcher
import backend.app.models.Batter as Batter


class Team:

    def __init__(self, name, lineup, rotation):
        if len(lineup) < 9:
            raise ValueError(f"Passed lineup does not contain enough players. 9 players required, {len(lineup)} given.")
        
        self.name = name
        self.lineup = self.makeLineup(lineup)
        self.rotation = self.makeRotation(rotation)
        #self.bench = self.makeBench()
        #self.bullpen = self.makeBullpen()
        self.upnext = 0 #current spot in lineup
        self.rotation_spot = -1


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
    
    def next_pitcher(self):
        if self.rotation_spot < len(self.rotation)-1:
            self.rotation_spot+=1
        else:
            self.rotation_spot=0


    def makeRotation(self,rotation):
        pitchers=[]
        for player in rotation:
            pitchers.append(Pitcher.Pitcher(player))
        return pitchers
    
    
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
        s += "Starting Pitcher\n\n" + self.rotation[self.rotation_spot].str() + "\n\nLineup\n\n"

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
        s += "Starting Pitcher\n\n" + self.rotation[self.rotation_spot].name + "\n\nLineup\n\n"

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