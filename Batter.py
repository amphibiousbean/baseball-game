import random
class Batter:
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
            outcome=self.swing_outcome(pitch) #tuple (contact, foul, hit)
            
            #TODO : refactor this to be in swing_outcome

            if outcome[0]: #if any contact
                if outcome[1]: #if contact is a foul ball
                    return "foul"
                elif outcome[2]: #if its a hit
                    return self.get_hit(pitch)
                else: #hit into an out
                    return "out"
            
            else: #swing and miss
                return "whiff"  
            
        else: #no swing
            if pitch[3]:#if strike
                return "strike"
            else:
                return "ball"
    
    def swing_outcome(self, pitch): #returns result of a swing as tuple (contact, foul, hit)
        contact=False
        foul=False
        hit=False
        

        return (contact, foul, hit) #TEMP

    def get_hit(self, pitch):
        pass