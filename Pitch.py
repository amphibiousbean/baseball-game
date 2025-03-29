def __init__(self, strike, quality, type, velo):
    self.quality=quality #0-1 scale, represents quality of pitch. 
                         #ie: high quality ball will be more likely to get a swing 
                         #whereas a low quality ball will almost never get a swing
                         #high quality strikes will be more likely to get a whiff or looking strike(depending on batter attributes)
                         #batters have boosted attributes against low quality strikes

    self.strike=strike #bool, True=strike, False=ball
    self.type=type #just for visual purposes, no functionality yet
    self.velo=velo #double edged sword. batters are much less likely to make "good" contact
                   #but when good contact is made, it is trouble!




def print(self):
    if(self.strike):
        print("Strike | " + str(self.type) + " " + str(self.velo) + "MPH")
    else:
        print("Ball | " + str(self.type) + " " + str(self.velo) + "MPH")
    
