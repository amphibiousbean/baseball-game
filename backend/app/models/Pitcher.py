import random
import json
from backend.app.config import PRINT
from backend.app.config import avg_velos
from backend.app.config import velo_low_bound
from backend.app.config import velo_up_bound
import os

class Pitcher:
    QUALITY_BASE=0.5
    pitch_index_dict={
        "Four-seam Fastball" : 0,
        "Sinker" : 1,
        "Cutter" : 2,
        "Slider" : 3,
        "Changeup" : 4,
        "Curveball" : 5,
        "Splitter" : 6,
        "Sweeper" : 7,
        "Slurve" : 8,
        "Knuckle-curve" : 9
    }
    FILENAME="players.json"
    base_dir = os.path.dirname(os.path.dirname(__file__))  # project/
    FILEPATH = os.path.join(base_dir, 'resources', FILENAME)
    pitches_thrown=0
    tot_quality=0
    tot_v_q=0
    tot_loc_q=0
    tot_stuff_q=0
    strikes=0
    def __init__(self, name): #, velo, K_rate, BB_rate, HR_rate, H_rate, control, pitches, stuff
        try:
            with open(self.FILEPATH, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            print("error finding file :" + self.FILEPATH)
        player_dict=None
        for player in data:
            if player["name"] == name:
                if player["type"] == "Pitcher":
                    player_dict=player
                    break
                else:
                    raise ValueError(f"Given player \"{name}\" is not a batter.")
        if player_dict:
            self.type = "Pitcher"
            self.name = name
            self.velo = player["velo"] #dictionary key:pitch type : value : pitch velo
            self.K_rate = player["K/9"]
            self.BB_rate = player["BB/9"]
            self.HR_rate = player["HR/9"]
            self.H_rate = player["H/9"]
            self.control = player["control"]
            self.pitches = list(player["velo"].keys()) #list of pitches
            self.stuff = player["stuff"] #dictionary key:pitch type : value : pitch "stuff"
            self.fatigue = 0
            self.pitch_count=0
            self.confidence=0 #pitching well improves confidence, pitching poorly reduces confidence. max increase/decrease = 0.2
            self.game_log={
                "pitched" : False,
                "outs_made" : 0,
                "H" : 0,
                "ER" : 0,
                "BB" : 0,
                "K" : 0,
                "HR" : 0
            }
        else:
            raise ValueError(f"Given player \"{name}\" does not exist in \"{self.FILEPATH}\"")
        
    def make_pitch(self):
        self.game_log["pitched"] = True
        #type_ind=random.randin(0,len(self.pitches))
        self.pitches_thrown+=1
        type_out=self.pitches[random.randint(0,len(self.pitches)-1)]
        velo_out=self.get_velo(type_out)
        quality=self.get_quality(type_out,velo_out)
        type_out_ind=self.pitch_index_dict[type_out]
        self.tot_quality+=quality
        strike=self.get_strike()
        if strike:
            self.strikes+=1
        if PRINT:
            print(type_out + " | " + str(round(velo_out,1)))
        self.pitch_count+=1
        return (type_out_ind, velo_out, quality, strike)

    def add_fatigue(self, n): #adds fatigue to pitcher based on how many pitches were thrown in their last inning
        pass
        '''
        self.pitch_count+=n
        pitch_count_fatigue=self.pitch_count/2500
        per_inning_fatigue=((n-15)/1000)
        if self.pitch_count<=80:
            self.fatigue+=per_inning_fatigue #gains energy after quick innings (less than 15 pitches), loses for longer innings
        else:
            self.fatigue+=(pitch_count_fatigue+per_inning_fatigue)
        '''
    
    def get_strike(self):
        strike_chance = ((self.control+self.confidence)/(50-(self.confidence/2)))*0.5  #50% chance by default, adjusted based on control attribute and confidence level
        strike_rand = random.random()
        strike=True

        if strike_rand > strike_chance:
            strike=False

        return strike

    def get_velo(self, pitch_type): #gets the velo of the pitch, between 2 under and 2 above the pitcher's average
        k=0.062 #to smooth out the velo scaling
        average_vel=avg_velos[self.pitch_index_dict[pitch_type]] #dict calls : 1
        velo=self.velo[pitch_type]
        velo_out_avg=(average_vel + (((velo/50)*average_vel)-average_vel)/(1+k*((velo/50)*average_vel)-average_vel))*(1-self.fatigue)
        return random.uniform(velo_out_avg-2,velo_out_avg+2)
    
        
    def get_quality(self, pitch_type, pitch_velo): #domain : (0,1)
        stuff=self.__stuff_factor(pitch_type)  #[-0.25, 0.5] can be more simple, literally just based off of the attribute for now
        pitch_ind=self.pitch_index_dict[pitch_type]
        v=self.__scaled_velo(pitch_velo, pitch_ind) # [-0.25, 1]how much the velocity will impact the quality
                                                     # high on upper bound, but only applies to pitches w/ elite velocity
        loc_factor=self.__loc_factor() #[-0.25, 0.25]
        self.tot_loc_q+=loc_factor
        self.tot_v_q+=v
        self.tot_stuff_q+=stuff
        quality=max(0, (min(self.QUALITY_BASE+v+stuff+loc_factor,1))) # keeps it within [0,1]
        return quality
        #NOT FINAL EQUATION #TODO : MAKE THIS ACTUALLY BE SOMETHING. PITCHES NEED STUFF ATT

    def __stuff_factor(self,pitch):
        stuff_x=self.stuff[pitch]/50
        stuff_val=((5/12)*stuff_x)-(5/12) 
        stuff_raw=random.uniform(stuff_val-0.125, stuff_val+0.125)
        if stuff_raw > 0:
            return min(stuff_raw,0.25)
        else:
            return max(stuff_raw, -0.25)

    def __loc_factor(self):
        #value that is based off of pitchers control. a psuedo "painted vs meatball" factor.
        loc_x=((self.control/50)+(self.BB_rate/50))/2
        loc_val=((5/12)*loc_x)-(5/12) 
        loc_raw=random.uniform(loc_val-0.125, loc_val+0.125) #random in [loc-0.2, loc+0.2], restricted to -.25 >= y >= .25
        if loc_raw > 0:
            return min(loc_raw,0.25)
        else:
            return max(loc_raw, -0.25)
        
    def __scaled_velo(self, velo, type): #return scaled value for use in functions
        
        if velo > avg_velos[type]:
            low=avg_velos[type]
            up=velo_up_bound[type]
            num=velo-low
            denom=up-low
            ret_val=(((num/denom)**1.7))
        else:
            low=velo_low_bound[type]
            up=avg_velos[type]
            num=velo-low
            denom=up-low
            ret_val=0.25*(1-(1-(num/denom)**2)-1)
        
        return ret_val
    
    def print(self):
        if PRINT:
            print(self.str())
    
    def str(self):
        r = str(self.name) +"\nK/9 : " + str(self.K_rate) + "\nBB/9 : " + str(self.BB_rate) + "\nHR/9 : " + str(self.HR_rate) + "\nH/9 : " + str(self.H_rate) + "\nControl : " + str(self.control) +"\n"
        txt="\n{:<18} {:<4} {:<5}"
        r += txt.format("Pitch Types", "Velo", "Stuff") + "\n"
        for pitch in self.pitches:
            r += txt.format(pitch, self.velo[pitch], self.stuff[pitch])

        return r

    def update_log(self, stat, num):
        self.game_log[stat] += num

    def log_hr(self):
        self.game_log["H"] += 1
        self.game_log["HR"] += 1
    
    def flush_log(self):
         self.game_log={
                "pitched" : False,
                "outs_made" : 0,
                "H" : 0,
                "ER" : 0,
                "BB" : 0,
                "K" : 0,
                "HR" : 0
            }

    def get_avg_quality(self):
        qual=self.tot_quality/self.pitches_thrown
        return round(qual, 4)
    
    def get_strike_percent(self):
        rate=(self.strikes/self.pitches_thrown)*100

        return round(rate, 5)
    
    def get_stuff_q(self):
        return self.tot_stuff_q/self.pitches_thrown
    
    def get_v_q(self):
        return self.tot_v_q/self.pitches_thrown
    
    def get_loc_q(self):
        return self.tot_loc_q/self.pitches_thrown