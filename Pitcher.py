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
    
    def make_pitch(self):
        #type_ind=random.randin(0,len(self.pitches))
        k=0.062 #to smooth out the velo scaling
        type_out="Fastball"
        average_vel=self.avg_velos[type_out]
        velo_out=(average_vel + (((self.velo/50)*average_vel)-average_vel)/(1+k*((self.velo/50)*average_vel)-average_vel))*(1-self.fatigue)
        quality= (self.pitches[type_out]/50)
    
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

    

    