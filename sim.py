import Pitcher as Pitcher
import Batter as Batter
import Team as Team
# import display as display
import scoreboard as scoreboard
import bases as b
import inning as inning
import time
import random
import box_score as box

game_loop = False
averages_dict = {
     "k_percent" : 0.2106,
     "bb_percent" : 0.087,
     "whiff_percent" : 0.2405,
     "swing_percent" : 0.4787
}
count_ratios = { #alters probabilities based on current count
        "0-0" : 1.0,
        "1-0" : 1.05,
        "2-0" : 1.15,
        "3-0" : 1.0,
        "3-1" : 1.4,
        "3-2" : .9,
        "2-2" : .7,
        "1-2" : .6,
        "0-2" : .3
    }
outcomes_dict={
    "whiff" : None,
    "strike" : None,
    "ball" : None,
    "foul" : None,
    "out" : None,
    "single" : None,
    "double" : None,
    "triple" : None,
    "home run" : None
}
display = "{:>6}".format("") + "1  2  3  4  5  6  7  8  9  T  H\n"
away="{:>3}".format("BOS")
home="{:>3}".format("PHI")
bases=b.bases(None)
inning_state=inning.inning()
away_score=scoreboard.scoreboard()
home_score=scoreboard.scoreboard()

PHI=[
    "Bryson Stott",
    "Trea Turner",
    "Bryce Harper",
    "Kyle Schwarber",
    "Nick Castellanos",
    "J.T. Realmuto",
    "Max Kepler",
    "Alec Bohm",
    "Johan Rojas"
]
BOS=[
    "Jarren Duran",
    "Rafael Devers",
    "Wilyer Abreu",
    "Romy Gonzalez",
    "Alex Bregman",
    "Trevor Story",
    "Ceddanne Rafaela",
    "Connor Wong",
    "Kristian Campbell"
]


def main():

    #displayScore()
    home_team = Team.Team("Phillies", PHI, "Zack Wheeler")
    away_team = Team.Team("Red Sox", BOS, "Garrett Crochet")
    #sim_half_inning(home_team,away_team,away_score)
    #print_display()
    #inning_state.print()
    #bases.print()
    startGame(home_team, away_team)
    

def startGame(teamA, teamB):
    home_box=box.box_score(teamA.name, teamA.lineup, [teamA.starter])
    away_box=box.box_score(teamB.name, teamB.lineup, [teamB.starter])
    start_str = ""
    while start_str != "start" or "exit":
        start_str = input("Type \"start\" to begin simulation or type \"exit\" to exit : ")
        if start_str == "start":
            game_loop=True
            break
        elif start_str == "exit":
            return
        else:
            print("Try again\n")
            
#GAME LOOP START---------------------------------------------------------------------------------------------
    inning=0
    while game_loop:
        
        if inning == 9.5 and home_score.runs > away_score.runs:
            print("FINAL")
            print_display()
            return

        if inning==0:
            print(teamA.str())
            print(teamB.str())
            print("Play ball! Poggers")
            inning+=1
            #time.sleep(1)
        
        if inning % 1 == 0:
            print(f"Top of the {get_suffix(int(inning))} inning\n----------------------------------------")
            sim_half_inning(teamA, teamB, away_score,home_box,away_box)
            print_display()
            inning_state.print()
            bases.print()
            inning+=0.5
        else: 
            print(f"Bottom of the {get_suffix(int(inning))} inning\n----------------------------------------")
            sim_half_inning(teamB,teamA, home_score, home_box, away_box)
            print_display()
            inning_state.print()
            bases.print()
            inning+=0.5
        

#GAME LOOP END------------------------------------------------------------------------------------
        


def sim_half_inning(pitching, batting, score, home_box, away_box): #returns outcome of inning as a tuple :
                                        #(runs, hits, walks) gets added to batting team
    
    score.new_inning()
    pitcher=pitching.starter
    inning_pitch_count=0
    while inning_state.outs < 3:
        bases.print()
        next_up=batting.next_spot()
        print("Now batting : " + batting.lineup[next_up].name)
        input("Press ENTER to continue inning")
        batter=batting.lineup[next_up]
        outcome = sim_AB(pitcher, batter)
        update_inning_state(pitcher,batter,outcome,score)
        inning_pitch_count+=outcome[2]
        inning_state.print()

    home_box.print()
    away_box.print()
    pitcher.add_fatigue(inning_pitch_count)
    bases.flush()
    inning_state.flush()
    print("inning over!")


#returns outcome of AB as tuple (outcome, advance_fact)
# #advance_fact = advancing factor, how well a runner
#               could take extra bases ie: 1st to 3rd on a single
#advance factor <= 0.4 = no attempt to advance
#0.4 < advance factor <= 0.6 attempt to advance, contested
#advance factor > 0.6 = always advances, no contest
def sim_AB(pitcher, batter):
    count=(0,0)           #(balls, strikes)
    AB_pitch_count=0
    while count[0] < 4 and count[1] < 3:
        print_count(count)
        #time.sleep(1)
        pitch=pitcher.make_pitch()
        action_outcome=batter.get_swing(pitch) #returns a string which is a key in outcomes_dict
        AB_pitch_count+=1
        match action_outcome:
            case "whiff" | "strike":
                count=(count[0],count[1]+1)
            case "foul" if count[1] < 2:
                count=(count[0],count[1]+1)
            case "ball":
                count=(count[0]+1, count[1])
            case "out":
                pitcher.update_log("outs_made", 1)
                return("out",0,AB_pitch_count)
            case "single":
                return("hit", 1,AB_pitch_count)
            case "double":
                return("hit", 2,AB_pitch_count)
            case "triple":
                return ("hit", 3,AB_pitch_count)
            case "home run":
                return("hit", 4,AB_pitch_count)
            
    if count[0]==4:
        print_count(count)
        batter.update_log("BB", 1)
        print("Walk")
        
        return ("walk",1,AB_pitch_count)
    elif count[1]==3:
        print_count(count)
        print("Strikeout")
        pitcher.update_log("K", 1)
        pitcher.update_log("outs_made", 1)
        batter.update_log("K", 1)
        return("strikeout",0,AB_pitch_count)   
    else:    
        return("ERROR",-1)

    

def update_inning_state(pitcher, batter, outcome,score): #takes outcome tuple and updates inning_state
    match outcome[0]:      
        case "out" | "strikeout":
            inning_state.add_outs(1)
        case "hit":
            inning_state.add_hit()
            score.add_hit()
            runs = bases.update_hit(outcome[1], batter)

            batter.update_log("RBI", runs)
            pitcher.update_log("ER", runs)
            
            inning_state.add_runs(runs)
            score.add_runs(runs)
        case "walk":
            inning_state.add_walk()
            score.add_walk()
            runs = bases.update_walk(batter)

            batter.update_log("RBI", runs)
            pitcher.update_log("ER", runs)
            pitcher.update_log("BB", 1)

            inning_state.add_runs(runs)
            score.add_runs(runs)

    
        

def print_count(count):
    print(str(count[0])+"-"+str(count[1]))


def get_suffix(n): #getting the "st", "nd", "rd", "th" for the inning
    if 10 <= n % 100 <= 20: 
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def print_display():
    dis=display + away + away_score.make_display() + home + home_score.make_display()
    print(dis)

if __name__ == '__main__':
    main()

