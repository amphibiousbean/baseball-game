import random
import json
class Pitcher:
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
        type_out=self.pitches[random.randint(0,len(self.pitches)-1)]
        velo_out=self.get_velo(type_out)
        quality=self.get_quality(type_out,velo_out)
        strike=self.get_strike()
        print(type_out + " | " + str(round(velo_out,1)))
        self.pitch_count+=1
        return (type_out, velo_out, quality, strike)

    def add_fatigue(self, n): #adds fatigue to pitcher based on how many pitches were thrown in their last inning
        self.pitch_count+=n
        pitch_count_fatigue=self.pitch_count/2500
        per_inning_fatigue=((n-15)/1000)
        if self.pitch_count<=80:
            self.fatigue+=per_inning_fatigue #gains energy after quick innings (less than 15 pitches), loses for longer innings
        else:
            self.fatigue+=(pitch_count_fatigue+per_inning_fatigue)
    
    def get_strike(self):
        strike_chance = ((self.control+self.confidence)/(50-(self.confidence/2)))*0.5  #50% chance by default, adjusted based on control attribute and confidence level
        strike_rand = random.random()
        strike=True

        if strike_rand > strike_chance:
            strike=False

        return strike

    def get_velo(self, pitch_type): #gets the velo of the pitch, between 2 under and 2 above the pitcher's average
        k=0.062 #to smooth out the velo scaling
        average_vel=self.avg_velos[pitch_type]
        velo_out_avg=(average_vel + (((self.velo[pitch_type]/50)*average_vel)-average_vel)/(1+k*((self.velo[pitch_type]/50)*average_vel)-average_vel))*(1-self.fatigue)
        return random.uniform(velo_out_avg-2,velo_out_avg+2)

    def get_quality(self, pitch_type, pitch_velo): #domain : (0,1)
        return (self.stuff[pitch_type]/50)*0.5 #NOT FINAL EQUATION

    def print(self):
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
    

    