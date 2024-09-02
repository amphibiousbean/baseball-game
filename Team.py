import Pitcher as Pitcher
import Batter as Batter

class Team:

    def __init__(self, name):
        self.name = name
        self.batters = self.makeBatters()
        self.pitchers = self.makePitcher()


    def makeBatters(self):
        batters = []

        for x in range(9):
            batters.append(Batter.Batter("Joe Random", 50, 50, 50, 50))
       
        return batters



    def makePitcher(self):
        pitchers = []
        pitchers.append(Pitcher.Pitcher("Mary Jane", 50, 50 ,50 ,50 ,50 ,50, ["Four Seamer", "Slider", "Changeup", "Curveball"]))
        return pitchers