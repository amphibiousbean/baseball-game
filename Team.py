import Pitcher as Pitcher
import Batter as Batter

class Team:

    def __init__(self, name):
        self.name = name
        self.lineup = self.makeLineup()
        self.starter = self.makeStarter()
        self.bench = self.makeBench()
        self.bullpen = self.makeBullpen()


    def makeLineup(self):
        batters = []

        for x in range(9):
            batters.append(Batter.Batter("Joe Random", 50, 50, 50, 50))
       
        return batters


    def makeBench(self):
        bench = []

        for x in range(5):
            bench.append(Batter.Batter("Joe Shmo", 40, 40, 40 ,40))
        
        return bench


    def makeStarter(self):
      
        return Pitcher.Pitcher("Mary Jane", 50, 50 ,50 ,50 ,50 ,50, ["Four Seamer", "Slider", "Changeup", "Curveball"])
    
    def makeBullpen(self):
        bullpen = []
        bullpen.append(Pitcher.Pitcher("Jane Doe", 40, 40, 40, 40, 40, 40, ["Four Seamer", "Slider", "Sinker"]))
        return bullpen
    
    def strDetailed(self):
        s = ""
        

        return s
    
    def strBasic(self):

        s = ""
        s += "Starting Pitcher\n\n" + self.starter.name + "\n\nLineup\n\n"

        lineup = ""
        for batter in self.lineup:
            lineup += batter.name + "\n"
        s += lineup + "\nBench\n\n"

        bench = ""
        for player in  self.bench:
            bench += player.name + "\n"
        s += bench + "\nBullpen\n\n"

        bullpen = ""
        for pitcher in self.bullpen:
            bullpen += pitcher.name + "\n"
        s += bullpen 

        return s