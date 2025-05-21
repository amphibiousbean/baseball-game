import random
class Batter:
    avg_velos = {
        "Fastball" : 92.5,
        "Curveball" : 82,
        "Slider" : 86,
        "Changeup" : 80,
        "Sinker" : 91
    } 

    #name : their name
    #pow : ability to hit for power
    #con : ability to make solid contact
    #vis : ability to foul off pitches and avoid swinging and missing
    #disc : ability to take balls and not swing at bad pitches
    def __init__(self, name, pow, con, vis, disc):
        self.type = "Batter"
        self.name = name
        self.pow = pow
        self.con = con
        self.vis = vis
        self.disc = disc

    def print(self):
        r = str(self.name) +  "\nPower :  " + str(self.pow) + "\nContact : " + str(self.con) + "\nVision : " + str(self.vis) + "\nDiscipline : " + str(self.disc)
        print(r)

    def str(self):
        r = str(self.name) +  "\nPower :  " + str(self.pow) + "\nContact : " + str(self.con) + "\nVision : " + str(self.vis) + "\nDiscipline : " + str(self.disc)
        return r

    #arg: pitch is tuple (str : type_out, float : velo_out, float : quality, bool : strike)
    def get_swing(self, pitch): #return true if batter swings, false if not

        if pitch[3]:
            #prob = 1-(pitch[2]/(self.vis/50))
            prob=0
        else:
            #prob = pitch[2]/(self.disc/50)
            prob=0

        swing_rand=random.random()
        if swing_rand<=prob:
            return self.swing_outcome(pitch)
        else: #no swing
            if pitch[3]:#if strike
                return "strike"
            else:
                return "ball"
    
    def swing_outcome(self, pitch): #returns result of a swing as a string from ["whiff", "foul", "out", "single", "double", "triple", "home run"]
        
        contact=None
        pitch_quality=pitch[2]
        strike=pitch[3]
        #get whiff or no whiff

        if strike:
            vis_factor=self.vis/50
        else:
            vis_factor=(self.vis/50)*0.85

        whiff_rand=random.random()
        whiff=vis_factor*pitch_quality*0.58
        if whiff > whiff_rand:
            return "whiff" #returns no contact made
        
        else: #determine quality of contact, starting with determining foul ball
            contact_rand=random.random() #random from domain (0,1), determines if contact results in a hit
            con_ratio=self.con/50
            contact=con_ratio-(con_ratio*pitch_quality*0.9) #domain [con_ratio/10, con_ratio], typically lower.
            if contact > contact_rand: 
                rand_fact=contact-contact_rand #used in con_factor calculation. always less than 1, typically low
                return self.get_hit(pitch, contact, rand_fact)
            elif contact*1.1 > contact_rand: #if it was within 10% of the rand
                return "foul"
            else:
                return "out"

    def get_hit(self, pitch, contact, rand_fact): #TODO
        velo_factor=(pitch[1]/self.avg_velos[pitch[0]])*1.05 #(pitch velo / avg velo of that pitch type)*1.05
        con_factor=
        pow_factor=velo_factor*(self.pow/50)

        

        
        pass