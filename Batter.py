import random
import json
class Batter:
    hits=["1B", "2B", "3B", "HR"]
    avg_velos={
        "Four-seam Fastball" : 94.26,
        "Sinker" : 93.58,
        "Cutter" : 89.49,
        "Slider" : 85.8,
        "Changeup" : 86.36,
        "Curveball" : 79.76,
        "Splitter" : 86.73,
        "Sweeper" : 82.17,
        "Slurve" : 81.3,
        "Knuckle-curve" : 80.4
    }
    FILEPATH="players.json"
    #name : their name
    #pow : ability to hit for power
    #con : ability to make solid contact
    #vis : ability to foul off pitches and avoid swinging and missing
    #disc : ability to take balls and not swing at bad pitches
    def __init__(self, name): #, pow, con, vis, disc
        try:
            with open(self.FILEPATH, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("error finding file :" + self.FILEPATH)
        player_dict=None
        for player in data:
            if player["name"] == name:
                if player["type"] == "Batter":
                    player_dict=player
                    break
                else:
                    raise ValueError(f"Given player \"{name}\" is not a batter.")
        if player_dict:
            self.type = "Batter"
            self.name = player["name"]
            self.pow = player["pow"]
            self.con = player["con"]
            self.vis = player["vis"]
            self.disc = player["disc"]
            self.game_log={
                "AB" : 0,
                "H" : 0,
                "RBI" : 0,
                "BB" : 0,
                "K" : 0,
                "R" : 0,
                "1B" : 0,
                "2B" : 0,
                "3B" : 0,
                "HR" : 0,
                }
        else:
            raise ValueError(f"Given player \"{name}\" does not exist in \"{self.FILEPATH}\"")

    def print(self):
        print(self.str())

    def str(self,label=True):
        txt="{:<25} {:<3} {:<3} {:<3} {:<3}"
        r=""
        if label:
            r+=txt.format("Name","Pow","Con","Vis","Dis")
        r+=txt.format(self.name,self.pow,self.con,self.vis,self.disc)
        return r

    #arg: pitch is tuple (str : type_out, float : velo_out, float : quality, bool : strike)
    def get_swing(self, pitch): #return true if batter swings, false if not

        if pitch[3]:
            prob = 1-(pitch[2]/(self.vis/50))
            #prob=0
        else:
            prob = pitch[2]/(self.disc/50)
            #prob=0

        swing_rand=random.random()
        if swing_rand<=prob:
            return self.swing_outcome(pitch)
        else: #no swing
            if pitch[3]:#if strike
                print("\n")
                return "strike"
            else:
                print("\n")
                return "ball"
    
    def swing_outcome(self, pitch): #returns result of a swing as a string from ["whiff", "foul", "out", "single", "double", "triple", "home run"]
        
        contact=None
        pitch_velo=pitch[1]/self.avg_velos[pitch[0]]
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
            print("Whiff")
            return "whiff" #returns no contact made
        
        else: #determine quality of contact, starting with determining foul ball
            contact_rand=random.random() #random from domain (0,1), determines if contact results in a hit
            con_ratio=self.con/50
            contact=con_ratio-(con_ratio*pitch_quality*0.9) #domain [con_ratio/10, con_ratio], typically lower.
            if contact > contact_rand: 
                rand_fact=contact-contact_rand #used in con_factor calculation. always less than 1, typically low
                return self.get_hit(pitch, contact, rand_fact)
            elif contact*1.1 > contact_rand: #if it was within 10% of the rand
                print("Foul")
                return "foul"
            else:
                self.update_log("AB", 1)
                print("Out")
                return "out"


    def get_hit(self, pitch, contact, rand_fact): #TODO
        velo_factor=(pitch[1]/self.avg_velos[pitch[0]])*1.05 #(pitch velo / avg velo of that pitch type)*1.05
        stuff_factor=(pitch[2])
        pow_rand=random.uniform(0.1,1.5)
        con_factor=(self.con/50)/(velo_factor*stuff_factor) # should hover around 0.9-1.1 ideally
        pow_factor=velo_factor*(self.pow/50)*pow_rand # will need extensive testing. should range from close to 0 to 2.
        hit=con_factor+pow_factor
        print(f"pow_rand : {pow_rand}")
        print(f"pow_factor : {pow_factor}")
        print(f"con_factor : {con_factor}")
        print(f"hit : {hit}")
        if hit < 2:
            self.log_hit("1B")
            print("Single")
            return "single"
        elif hit < 2.9:
            self.log_hit("2B")
            print("Double!")
            return "double"
        elif hit < 3:
            self.log_hit("3B")
            print("Triple!!")
            return "triple"
        else:
            self.log_hit("HR")
            print("HOME RUN!!!")
            return "home run" 
  
    def update_log(self, stat, num):
        self.game_log[stat] += num

    def log_hit(self, hit):
        self.update_log("H", 1)
        self.update_log(hit, 1)
        self.update_log("AB", 1)

        

        
        