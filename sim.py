import Pitcher as Pitcher
import Batter as Batter
import Team as Team
import display as display
import time

home_runs_by_inning = [1,0,2,0]
away_runs_by_inning = [1,1,0,0]
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
def main():

    #displayScore()
    home_team = Team.Team("Phillies")
    away_team = Team.Team("Red Sox")
    startGame(home_team, away_team)
    
team_a_runs = 1 #set to 1 for testing
team_b_runs = 0

def startGame(teamA, teamB):
    
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
        

        if inning == 9.5 and team_a_runs > team_b_runs:
            print("FINAL")
            displayScore()
            return

        if inning==0:
            print(teamA.strBasic())
            print(teamB.strBasic())
            print("Play ball! Poggers")
            inning+=1
            time.sleep(1)
        
        if inning % 1 == 0:
            print(f"Top of the {get_ordinal(int(inning))} inning\n----------------------------------------")
            sim_half_inning(teamA, teamB)
            inning+=0.5
        else: 
            print(f"Bottom of the {get_ordinal(int(inning))} inning\n----------------------------------------")
            sim_half_inning(teamB,teamA)
            inning+=0.5
        

#GAME LOOP END------------------------------------------------------------------------------------
        


def sim_half_inning(pitching, batting): 

    inning_state = {
        "outs" : 0,
        "bases" : {
            "first" : 0,
            "second" : 0,
            "third" : 0
        },
        "runs_scored" : 0
    }

    outs=0
    while inning_state["outs"] < 3:
        inning_state["outs"] += outs
        outs+=1
        print("Out " + str(outs))
        time.sleep(0.3)
        
    print("inning over!")


def sim_AB(pitcher, batter):
    return None
def sim_action(batter, pitcher):
    return None


def get_ordinal(n): #getting the "st", "nd", "rd", "th" for the inning
    if 10 <= n % 100 <= 20: 
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

def makeScoreboard(inning, outs, batter, pitcher):
    
    return None


def displayScore():
    
    home = ""
    away = ""

    for x in range(9):
        if x < len(home_runs_by_inning):
            home += "  " + str(home_runs_by_inning[x])
        else:
            home += "   "

    home += "  " + str(sum(home_runs_by_inning))

    for x in range(9):
        if x < len(away_runs_by_inning):
            away += "  " + str(away_runs_by_inning[x])
        else:
            away += "   "
    
    away += "  " + str(sum(away_runs_by_inning))

    dis = "      1  2  3  4  5  6  7  8  9  T\nAway" + away + "\nHome" + home
    
    print(dis)



if __name__ == '__main__':
    main()

