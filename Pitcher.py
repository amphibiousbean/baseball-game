class Pitcher:

    def __init__(self, name, velo, K_rate, BB_rate, HR_rate, H_rate, control, pitches):
        self.type = "Pitcher"
        self.name = name
        self.velo = velo
        self.K_rate = K_rate
        self.BB_rate = BB_rate
        self.HR_rate = HR_rate
        self.H_rate = H_rate
        self.control = control
        self.pitches = pitches
    
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

    

    