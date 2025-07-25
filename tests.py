import Pitcher as Pitcher
import Batter as Batter
import Team as Team
# import display as display
import bases as bases
import scoreboard as scoreboard
import time
import random
import os
import collections as c
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
outcomes=[1,2,3,4]
runner1="1"
runner2="2"
runner3="3"
test_runner="test"
base_states = [
    [runner1, None, None],
    [None, runner1, None],
    [None, None, runner1],
    [runner1, runner2, None],
    [runner1, None, runner2],
    [None, runner1, runner2],
    [runner1, runner2, runner3]
]
away="{:>3}".format("BOS")
home="{:>3}".format("PHI")
away_score=scoreboard.scoreboard()
home_score=scoreboard.scoreboard()
display = "{:>6}".format("") + "1  2  3  4  5  6  7  8  9  T  H\n"

def test_bases():
    for state in base_states:
        bases_state=bases.bases(state)
        print("\nstate : " + str(state))
        temp_counter=1
        for outcome in outcomes:

            print("outcome : " + str(outcome))
            temp_runner=test_runner + str(temp_counter)
            scored=bases_state.update_hit(outcome, temp_runner)
            print("runs : " + str(scored))
            temp_counter+=1
def test_display():
    for x in range(9):
        away_score.new_inning()
        away_score.add_runs(2)
        away_score.add_hit()
        print_display()
        home_score.new_inning()
        home_score.add_runs(1)
        home_score.add_hit()
        print_display()        

def print_display():
    dis=display + away + away_score.make_display() + home + home_score.make_display()
    print(dis)


def test_teams(details):
    phillies=Team.Team("Phillies",PHI, "Zack Wheeler")
    red_sox=Team.Team("Red Sox", BOS, "Garrett Crochet")
    print(phillies.str(details))
    print("\n\n" + red_sox.str(details))

#wheels=Pitcher.Pitcher("Zack Wheeler")
#wheels.print()
#test_teams(False)
#print("----------------------------------------------------------")
#test_teams(True)
#test_bases() #tested, works!
#test_display() #works

print(os.getcwd()+"\\test_data")





