import Pitcher as Pitcher
import Batter as Batter
import Team as Team
# import display as display
import stat_logger as logger
import scoreboard as scoreboard
import bases as b
import inning as inning
import time
import random
import box_score as box
import traceback
import config

game_loop = False
EXTRA_INNINGS = False
EXTRAS_COUNTER=0
GAME_SPEED=0
SIM_NUM=0
PRINT=False

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
stats=logger.stat_logger()

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
    global GAME_SPEED, SIM_NUM, PRINT
    home_team = Team.Team("Phillies", PHI, "Zack Wheeler")
    away_team = Team.Team("Red Sox", BOS, "Garrett Crochet")
    home=0
    away=0
    winner=""
    start_time=None
    while SIM_NUM == 0:
        SIM_NUM=int(input("Enter the number of games you wish to simulate : "))
        config.update_sim_num(SIM_NUM)
        if SIM_NUM == 0:
            print("Cannot simulate zero games")
    
    speed=input("""Game speed is the length of the delay between actions\n
                \nSIM : No delay and no stop actions. Use when simulating a larger number of games\n
                \nAny number  : Delay will be the number you input in seconds. Will have stop actions.\n
                \nDesired speed : """)
    print_input=input("Would you like printed results for every action? (Not recommended for large sims)\n\ny/N : ")
    if print_input and print_input == "y" :
        config.update_print(True)
        PRINT=True
       

    if speed == "SIM":
        start_time=time.time()
    else:
        config.update_speed(speed)
        GAME_SPEED=int(speed)

    try:
        print("Simulator running...")
        for i in range(SIM_NUM):
            winner = startGame(home_team, away_team)
            if winner == home_team.name:
                home+=1
            else:
                away+=1

        print("Record : " + str(home) +"-"+str(away))
        
        if start_time:
            elapsed=time.time()-start_time
            print(f"Sim time elapsed : {elapsed}")

        factors_time=time.time()
        with open("test_factors.txt", "a") as file:
            file.write("------------------TEST @ " + str(start_time)+"------------------\n")
            for batter in home_team.lineup:
                file.write("\n"+str(batter.get_avg_factors() + "\n"))
            for batter in away_team.lineup:
                file.write("\n"+str(batter.get_avg_factors() + "\n"))
        print(f"Factors write time : {time.time()-factors_time}")
        
    except Exception as e:
        traceback.print_exc()
        print("Record : " + str(home) +"-"+str(away))
    

def startGame(teamA, teamB):
    global game_loop, EXTRA_INNINGS, EXTRAS_COUNTER, GAME_SPEED
    winner=""
    home_box=box.box_score(teamA.name, teamA.lineup, [teamA.starter])
    away_box=box.box_score(teamB.name, teamB.lineup, [teamB.starter])
    if GAME_SPEED != 0:
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
    else:
        game_loop=True
            
#GAME LOOP START---------------------------------------------------------------------------------------------
    inning=0
    while game_loop:

        if EXTRA_INNINGS:
            EXTRAS_COUNTER+=0.5

        if check_end(inning):
            if home_score.runs>away_score.runs:
                if PRINT:
                    print("FINAL - " + teamA.name + " WINS!")
                winner=teamA.name
            else:
                if PRINT:
                    print("FINAL - " + teamB.name + " WINS!")
                winner=teamB.name
            if PRINT:
                print_display()
            break

        if inning == 9.5:
            #print("#\n#\n#\n START OF EXTRAS \n#\n#\n#")
            EXTRA_INNINGS=True #includes bottom nine for sake of home team walk offs
            EXTRAS_COUNTER+=0.5

        if inning==0:
            if PRINT:
                print(teamA.str())
                print(teamB.str())
                print("Play ball! Poggers")
            inning+=1
            time.sleep(GAME_SPEED) #DELAY
        
        if inning % 1 == 0:
            if PRINT:
                print(f"Top of the {get_suffix(int(inning))} inning\n----------------------------------------")
            sim_half_inning(teamA, teamB, away_score,home_box,away_box)
            if PRINT:
                print_display()
                inning_state.print()
                bases.print()
            inning+=0.5
        else: 
            if PRINT:
                print(f"Bottom of the {get_suffix(int(inning))} inning\n----------------------------------------")
            sim_half_inning(teamB,teamA, home_score, home_box, away_box)
            if PRINT:
                print_display()
                inning_state.print()
                bases.print()
            inning+=0.5

    game_loop=False
    stats_update(teamA)
    stats_update(teamB)
    home_score.flush()
    away_score.flush()
    EXTRA_INNINGS=False
    EXTRAS_COUNTER=0
    return winner

#GAME LOOP END------------------------------------------------------------------------------------
        
################################        CORE GAME METHODS       ###################################

def sim_half_inning(pitching, batting, score, home_box, away_box): #returns outcome of inning as a tuple :
                                        #(runs, hits, walks) gets added to batting team
    
    score.new_inning()
    pitcher=pitching.starter
    inning_pitch_count=0
    walkoff=False

    while inning_state.outs < 3:
        bases.print()
        next_up=batting.next_spot()
        if PRINT:
            print("Now batting : " + batting.lineup[next_up].name)

        if GAME_SPEED != 0:
            input("Press ENTER to continue inning") #stop action if not sim speed

        batter=batting.lineup[next_up]
        outcome = sim_AB(pitcher, batter)
        update_inning_state(pitcher,batter,outcome,score)
        inning_pitch_count+=outcome[2]
        if PRINT:
            inning_state.print()

        if EXTRA_INNINGS and EXTRAS_COUNTER % 1 == 0: #if in extras and bottom of inning
            if home_score.runs>away_score.runs:
                walkoff=True
                break
    if PRINT:
        home_box.print()
        away_box.print()
    pitcher.add_fatigue(inning_pitch_count)
    bases.flush()
    inning_state.flush()
    if walkoff:
        if PRINT:
            print("WALKOFF!!!")
    else:
        if PRINT:
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
        if PRINT:
            print_count(count)

        time.sleep(GAME_SPEED) #DELAY 

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
        if PRINT:
            print_count(count)
            print("Walk")

        batter.update_log("BB", 1)
        
        return ("walk",1,AB_pitch_count)
    elif count[1]==3:
        if PRINT:
            print_count(count)
            print("Strikeout")
        pitcher.update_log("K", 1)
        pitcher.update_log("outs_made", 1)
        batter.update_log("K", 1)
        batter.update_log("AB", 1)
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
            pitcher.update_log("H", 1)
            
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

def stats_update(team):

    for batter in team.lineup:
        stats.update_player(batter)
        batter.flush_log()

    stats.update_player(team.starter)
    team.starter.flush_log()

#checking if the game is over. 
def check_end(inning):
    
    if inning == 9.5 and home_score.runs > away_score.runs: #home team leading going into bot 9
        return True
    
    # when in extras, check if away is leading at start of inning, if so : end
    if EXTRA_INNINGS and EXTRAS_COUNTER % 1 == 0 and away_score.runs > home_score.runs:
        return True
    
    # when in extras, check if home is leading at end of inning, if so : end (walk off ends inning within sim_inning())
    if EXTRA_INNINGS and EXTRAS_COUNTER % 1 != 0 and home_score.runs > away_score.runs: 
        return True
    
    return False
    

    


########################        HELPERS         ##########################



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

