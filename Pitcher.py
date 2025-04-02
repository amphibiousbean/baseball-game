import random

class Pitcher:
    avg_velos = {
        "Fastball" : 92.5,
        "Curveball" : 82,
        "Slider" : 86,
        "Changeup" : 80,
        "Sinker" : 91
    } 
    def __init__(self, name, velo, K_rate, BB_rate, HR_rate, H_rate, control, pitches):
        self.type = "Pitcher"
        self.name = name
        self.velo = velo
        self.K_rate = K_rate
        self.BB_rate = BB_rate
        self.HR_rate = HR_rate
        self.H_rate = H_rate
        self.control = control
        self.pitches = pitches #dictionary key:pitch type : value : pitch "stuff"
        self.fatigue = 0
        self.pitch_count=0
        self.confidence=0 #pitching well improves confidence, pitching poorly reduces confidence. max of 0.2
    
    def make_pitch(self):
        #type_ind=random.randin(0,len(self.pitches))
        k=0.062 #to smooth out the velo scaling
        type_out="Fastball" #hard coding fastballs... for now
        average_vel=self.avg_velos[type_out]
        velo_out=(average_vel + (((self.velo/50)*average_vel)-average_vel)/(1+k*((self.velo/50)*average_vel)-average_vel))*(1-self.fatigue)
        quality= (self.pitches[type_out]/50)*0.5 #NOT FINAL EQUATION
        strike_chance = ((self.control+self.confidence)/(50-(self.confidence/2)))*0.5  #50% chance by default, adjusted based on control attribute and confidence level
        strike_rand = random.random()
        strike=True

        if strike_rand > strike_chance:
            strike=False
            print(type_out + " | " + str(velo_out))
        else:
            print(type_out + " | " + str(velo_out))

        self.pitch_count+=1
        return (type_out, velo_out, quality, strike)

    def add_fatigue(self, n): #adds fatigue to pitcher based on how many pitches were thrown in their last inning
        pass


    def print(self):
        r = str(self.name) +  "\nVelocity : " + str(self.velo) + "\nK/9 : " + str(self.K_rate) + "\nBB/9 : " + str(self.BB_rate) + "\nHR/9 : " + str(self.HR_rate) + "\nH/9 : " + str(self.H_rate) + "\nControl : " + str(self.control)
        pitches_str = "\n"
        count = 0
        for pitch in self.pitches:
            count += 1
            pitches_str += str(count) + " : " + str(pitch) + "\n"
        r += pitches_str
        print(r)
    
    def str(self):
        r = str(self.name) +  "\nVelocity :  " + str(self.velo) + "\nK/9 : " + str(self.K_rate) + "\nBB/9 : " + str(self.BB_rate) + "\nHR/9 : " + str(self.HR_rate) + "\nH/9 : " + str(self.H_rate) + "\nControl : " + str(self.control)
        pitches_str = "\n"
        count = 0
        for pitch in self.pitches:
            count += 1
            pitches_str += str(count) + " : " + str(pitch) + "\n"
        r += pitches_str

        return r

    

    