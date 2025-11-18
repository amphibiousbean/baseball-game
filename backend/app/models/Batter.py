import random
import json
import backend.app.config as config
from backend.app.config import PRINT
import backend.app.config as config
import math
import os
import numpy

class Batter:
    avg_velos=config.avg_velos
    velo_up_bound=config.velo_up_bound
    velo_low_bound=config.velo_low_bound
    count_ratios=config.count_ratios
    hits=["1B", "2B", "3B", "HR"]
    FILENAME="players.json"
    base_dir = os.path.dirname(os.path.dirname(__file__)) 
    FILEPATH = os.path.join(base_dir, 'resources', FILENAME)
    total_hit_factor=0
    total_con_factor=0
    total_pow_factor=0
    total_contact=0
    pitches_seen=0
    swings=0
    true_strikes=0 
    looking_strikes=0
    true_balls=0 #if it was a pitch out of the zone, ie: would be a ball if there is no swing
    chases=0
    whiffs=0
    tot_con_impact=0
    tot_ball_strike_impact=0
    tot_quality_impact=0
    tot_in_play=0
    tot_AB=0
    hit_calcs=0
    tot_swing_prob_strike=0
    tot_swing_prob_ball=0
    tot_foul=0
    k=0
    tot_foul_chance=0
    foul_calcs=0
    ooz_bbe=0 #out of zone batted ball events
    tot_homer_prob=0
    tot_xbh_prob=0
    tot_hits=0
    ZONE_SWING_BASE=0.65
    OUT_ZONE_SWING_BASE=0.25
    CON_BASELINE=0.2
    CON_MAX=0.4
    FOUL_BASE=1.2
    VIS_BASE=0.2
    UPPER_BOUND_CONST=(1/6)
    HOMER_CONST=0.05
    XBH_CONST=0.05
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
                #"R" : 0,
                "1B" : 0,
                "2B" : 0,
                "3B" : 0,
                "HR" : 0,
                }
        else:
            raise ValueError(f"Given player \"{name}\" does not exist in \"{self.FILEPATH}\"")

    def print(self):
        if PRINT:
            print(self.str())

    def str(self,label=True):
        txt="{:<25} {:<3} {:<3} {:<3} {:<3}"
        r=""
        if label:
            r+=txt.format("Name","Pow","Con","Vis","Dis")
        r+=txt.format(self.name,self.pow,self.con,self.vis,self.disc)
        return r

    #arg: pitch is tuple (str : type_out, float : velo_out, float : quality, bool : strike)
    def get_swing(self, pitch,count): #return true if batter swings, false if not
        
        swing_rand=random.random()
        if swing_rand<=self.get_swing_prob(pitch,count):

            self.swings+=1
            if not pitch[3]:
                self.chases+=1

            return self.swing_outcome(pitch,count)
        else: #no swing
            if pitch[3]:#if strike
                self.looking_strikes+=1
                if PRINT:
                    print("\n")
                return "strike"
            else:
                if PRINT:
                    print("\n")
                return "ball"
            

    def get_swing_prob(self, pitch,count):

        self.pitches_seen+=1
        quality=pitch[2]
        #TODO : make this actually good lol. needs sharper curve around the average range. 40-60. sin curves probably not the move
                                            # sharper at the very start, evens out in the 60-80 range. possibly log curve?
        q_fact=-1*(0.125*quality)+0.0625 # scales attribute multiplier up or down based on how good the pitch was
        vis_multiplier=q_fact*((self.vis/50)-1)*100 # for in zone pitches
        disc_multiplier=q_fact*((self.disc/50)-1)*100 # for out of zone pitches
        #if strike
        if pitch[3]: #strikes [~0.4,~0.8] without pitch quality weighed in
            if self.vis/50 > 1:
                vis_fact=(1/5.25)*(math.sin((math.pi/2)*vis_multiplier))
            else:
                vis_fact=(1/3.25)*(math.sin((math.pi/2)*vis_multiplier))
                
            prob = self.ZONE_SWING_BASE + vis_fact
            #print(f"q_fact : {q_fact}\nvis_mult : {vis_multiplier}\nvis_fact : {vis_fact}\nprob : {prob}\n")
            self.tot_swing_prob_strike+=prob
            self.true_strikes+=1
            #TODO : fix this. 
        else: #balls [~0.1, ~0.5]
            if self.disc/50 > 1:

                disc_fact=(-1*(1/3.25)*(math.sin((math.pi/2)*disc_multiplier))**2)
            else:
                disc_fact=((1/2)*(math.sin((math.pi/2)*disc_multiplier))**2)
                

            prob = self.OUT_ZONE_SWING_BASE+disc_fact
            #print(f"disc_att : {self.disc}\nq_fact : {q_fact}\ndisc_mult : {disc_multiplier}\ndisc_fact : {disc_fact}\nprob : {prob}\n")
            self.true_balls+=1
            self.tot_swing_prob_ball+=prob
        
        return prob




    #TODO : tweak this so that slightly below average attribute guys aren't always hitting under the mendoza line
    def swing_outcome(self, pitch,count): #returns result of a swing as a string from ["whiff", "foul", "out", "single", "double", "triple", "home run"]
        
        contact=None
        type=pitch[0]
        raw_v=pitch[1] #velo
        v=self.__scaled_velo(raw_v, type)
        q=pitch[2] #quality
        strike=pitch[3]

        if self.get_whiff(pitch):
            if PRINT:
                print("Whiff")
            self.whiffs+=1
            return "whiff" #returns no contact made
        
        else: #determine quality of contact, starting with determining foul ball
            contact_rand=random.random() #random from domain (0,1), determines if contact results in a hit
            #con_ratio=self.con/50
            #contact=con_ratio-(con_ratio*q*0.9) #domain [con_ratio/10, con_ratio], typically lower. #TODO : make this work right
            contact=self.get_hit_prob(pitch, count) 
            foul_chance=numpy.log10((self.vis/50))
            if self.vis/50 < 1:
                foul_chance*=0.25
            self.foul_calcs+=1
            self.tot_foul_chance+=(self.FOUL_BASE+foul_chance)
            #print(f"BASE : {self.FOUL_BASE}\nfoul_chance : {foul_chance}\nboth : {self.FOUL_BASE+foul_chance}\n")

            if contact > contact_rand: 
                rand_fact=contact-contact_rand #used in con_factor calculation. always less than 1, typically low
                return self.get_hit(pitch, contact, rand_fact, count)
            
            
            
            elif contact*(self.FOUL_BASE+foul_chance) > contact_rand: #if it was within 20% of the rand TODO : make this scale w/ vision attribute
                if PRINT:
                    print("Foul")
                
                self.tot_foul+=1
                self.total_contact+=1
                
                return "foul"
            
            else:
                self.update_log("AB", 1)
                if PRINT:
                    print("Out")
                self.tot_in_play+=1
                self.total_contact+=1
                self.tot_AB+=1
                return "out"
        
    #TODO : this thing sucks. TOO MANY XBH. ESPECIALLY HOME RUNS
    def get_hit(self, pitch, contact, rand_fact, count): 
        quality=pitch[2]
        velo_factor=(pitch[1]/self.avg_velos[pitch[0]])*1.05 #(pitch velo / avg velo of that pitch type)*1.05
        stuff_factor=(0.5-quality)/(2+quality) #same as in get_hit_prob()

        #TODO: tweak these. more homers, less doubles. probably something to do with how pow is weighed.
        homer_prob=1-((self.HOMER_CONST*(self.pow/50)*velo_factor)-(stuff_factor/4)) 
        xbh_prob=0.8-((self.XBH_CONST*(self.pow/50)*velo_factor)-(stuff_factor/4))
        pow_factor=random.random() #(0,1)

        self.tot_homer_prob+=homer_prob
        self.tot_xbh_prob+=xbh_prob
        self.total_pow_factor+=pow_factor
        self.tot_hits+=1
        self.total_contact+=1
        self.tot_in_play+=1
        self.tot_AB+=1

        #if high enough to be a home run
        if pow_factor>=homer_prob:
            self.log_hit("HR")
            if PRINT:
                print("HOME RUN!!!")
            return "home run"
        
        #if xbh TODO: incorporate player speed to get chances of a triple. until then triples are not possible
        elif pow_factor>=xbh_prob:
            self.log_hit("2B")
            if PRINT:
                print("Double!")
            return "double"
        
        #if neither home run or xbh then it is a single
        else:
            self.log_hit("1B")
            if PRINT:
                print("Single")
            return "single"
    
    '''
    returns the "xBA" of the batted ball. 
    This is a random number from range (low_bound, upper_bound). 
    As contact attribute increases so do the bounds. 
    Impacted by ball/strike and pitch quality
    '''
    def get_hit_prob(self, pitch, count): 
        q=pitch[2] #quality
        strike=pitch[3] #strike=True, ball=False
        con_impact_lower=(self.con/50)/25 
        
        quality_impact=(0.5-q)/(2+q)
        ball_strike_impact=0
        if not strike:
            ball_strike_impact=(((self.vis/50))/10)-self.VIS_BASE
            self.tot_ball_strike_impact+=ball_strike_impact
            self.ooz_bbe+=1

        self.tot_quality_impact+=quality_impact
        self.hit_calcs+=1

        
        con_impact_upper=((self.con/50)/3)+self.UPPER_BOUND_CONST+quality_impact+ball_strike_impact

        con_impact=random.uniform(con_impact_lower, con_impact_upper) #essentially the raw "xBA" of the hit.
        self.tot_con_impact+=con_impact
        self.hit_calcs+=1
        return con_impact
          

    def get_whiff(self,pitch):
        type=pitch[0]
        raw_v=pitch[1] #velo
        v=self.__scaled_velo(raw_v, type)
        q=pitch[2] #quality
        strike=pitch[3]
        #get whiff or no whiff

        if strike:
            vis_factor=self.vis/50
            quality_factor=(((q-(1/9))**3)+(1/9))
            velo_factor=((1/8)*(v-0.5))    
        else:
            quality_factor=(((1/8)*((q+0.725)**4))+(1/8))
            velo_factor=((1/8)*(v-0.5))
            vis_factor=(self.vis/50)*0.85

        #TODO : very close... an average player whiffs around 25%, 
        #       need to work out how well it works with different
        #       pitchers. test with some "lower quality" pitchers
        whiff_rand=random.random()
        whiff_factor=quality_factor + velo_factor - (vis_factor*0.1)
        return whiff_factor>whiff_rand

    def __scaled_velo(self, velo, type): #return scaled value for use in functions
        
        if velo > self.avg_velos[type]:
            low=self.avg_velos[type]
            up=self.velo_up_bound[type]
            num=velo-low
            denom=up-low
            ret_val=0.5 * (((num/denom)**3)+1)
        else:
            low=self.velo_low_bound[type]
            up=self.avg_velos[type]
            num=velo-low
            denom=up-low
            ret_val=0.5*(1-(1-(num/denom)**3))
        
        return ret_val

    def update_log(self, stat, num):
        self.game_log[stat] += num

    def log_hit(self, hit):
        self.update_log("H", 1)
        self.update_log(hit, 1)
        self.update_log("AB", 1)

    def flush_log(self):
        self.game_log={
                "AB" : 0,
                "H" : 0,
                "RBI" : 0,
                "BB" : 0,
                "K" : 0,
                #"R" : 0,
                "1B" : 0,
                "2B" : 0,
                "3B" : 0,
                "HR" : 0,
                }
        

    def print_avg_factors(self):
        ret_str=self.name
        if self.total_contact > 100:
            avg_hit=self.total_hit_factor/self.total_contact
            avg_pow=self.total_pow_factor/self.total_contact
            avg_con=self.total_con_factor/self.total_contact
            ret_str += f"\navg_hit : {avg_hit} \navg_pow : {avg_pow} \navg_con : {avg_con}"
            print(ret_str)

    def get_avg_factors_str(self):
        ret_str=self.name
        if self.total_contact > 100:
            avg_hit=self.total_hit_factor/self.total_contact
            avg_pow=self.total_pow_factor/self.total_contact
            avg_con=self.total_con_factor/self.total_contact
            ret_str += f"\navg_hit : {avg_hit} \navg_pow : {avg_pow} \navg_con : {avg_con}"
        return ret_str
            
    def get_avg_factors_tup(self):
        avg_hit=0
        avg_con=0
        avg_pow=0
        if self.total_contact > 1:
            avg_hit=self.total_hit_factor/self.total_contact
            avg_pow=self.total_pow_factor/self.tot_hits
            avg_con=self.total_con_factor/self.total_contact
            
        return (avg_hit, avg_pow, avg_con)
    
    def get_swing_rate(self):
        rate=(self.swings/self.pitches_seen)*100
        return round(rate, 2)
    
    def get_chase_rate(self):
        rate=(self.chases/self.true_balls)*100
        return round(rate,2)
    
    def get_whiff_rate(self):
        rate=(self.whiffs/self.swings)*100
        return round(rate, 2)
    
    def get_strikes_looking(self):
        looking=(self.looking_strikes/self.true_strikes)*100
        return round(looking, 2)

    def get_avg_con_imp(self):
        return self.tot_con_impact/self.hit_calcs
    
    def get_avg_b_s_imp(self):
        return self.tot_ball_strike_impact/self.ooz_bbe
    
    def get_avg_q_imp(self):
        return self.tot_quality_impact/self.hit_calcs
    
    def get_in_play_rate(self):
        return (self.tot_in_play/self.tot_AB)*100
    
    def update_tot_AB(self):

        self.tot_AB+=1

    def get_avg_swing_prob(self):
        return self.tot_swing_prob_strike/self.true_strikes
    
    def get_avg_chase_prob(self):
        return self.tot_swing_prob_ball/self.true_balls
    
    def get_foul_rate(self):
        return self.tot_foul/self.total_contact
    
    def update_k(self):
        self.k+=1

    def get_k_rate(self):
        return (self.k/self.tot_AB)*100
    
    def avg_foul_chance(self):
        return self.tot_foul_chance/self.foul_calcs
    
    def get_avg_hr_prob(self):
        return self.tot_homer_prob/self.tot_hits
    
    def get_avg_xbh_prob(self):
        return self.tot_xbh_prob/self.tot_hits