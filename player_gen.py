import savant_batter as batter
import savant_pitcher as pitcher
from pybaseball import statcast_batter
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
from pybaseball import batting_stats_bref
from datetime import date
import json

#TODO: refactor this all into multiple files to separate stat collection from the attribute conversion


ZONE_WIDTH = 0.83
ZONE_TOP = 3.5
ZONE_BOTTOM = 1.5

FILEPATH="players.json"

def add_player(player):
    try:
        with open(FILEPATH, 'r') as file:
            data = json.load(file)
            
    except FileNotFoundError:
        print("error finding file :" + FILEPATH)
    
    data.append(player)
    with open(FILEPATH, 'w') as file:
        
        json.dump(data, file, indent = 4)
    

std_dict={
    "exit_vel" : 2.4,
    "xba" : 0.03,
    "xwoba" : .04,
    "bb" : 3.6,
    "k" : 5.9,
    "whiff" : 6.2,
    "chase" : 6.2
}

avg_bat = {
    "exit_vel" : 88.5,
    "xba" : .245,
    "xwoba" : .315,
    "bb" : 8.4,
    "k" : 22.2,
    "whiff" : 23.1,
    "chase" : 27.5
}


def calc_att(x,y):
    att=round(50+(x+y))
    return max(20, min(80, att))

def calc_stat_impact(x, stat, invert=False):
    mean = avg_bat[stat]
    std = std_dict[stat]

    if std == 0:
        return 0

    z = (x - mean) / std
    scaler=10*z
    if invert:
        scaler*=-1
    return scaler  
    
mode=""
while mode != "b" or "p":
    mode=input("Type \"p\" for a pitcher or \"b\" for a batter : ")
    if mode == "b" or "p":
        break
name=input("Enter player name : ")
player=tuple(name.lower().split(' '))
playerid=playerid_lookup(player[1], player[0]).iloc[0]["key_mlbam"]
if mode == "b":
    
    player={
        "type" : "Batter",
        "name" : name
        }
    #setting dataframes
    data=batter.pull_player_data(player)
    batted_balls=batter.filter_non_events(data)
    at_bats=batter.filter_non_AB(data)

    #getting stat impact
    exit_vel=calc_stat_impact(batter.get_exit_vel(batted_balls), "exit_vel")
    xwoba=calc_stat_impact(batter.get_xwoba(batted_balls), "xwoba")
    xba=calc_stat_impact(batter.get_xba(batted_balls), "xba")
    bb=calc_stat_impact(batter.get_bb(data), "bb")
    k=calc_stat_impact(batter.get_k(data),"k", invert=True)
    whiff=calc_stat_impact(batter.get_whiff(data),"whiff", invert=True)
    chase=calc_stat_impact(batter.get_chase(data),"chase",invert=True)

    player["con"] = calc_att(xba,whiff)
    player["pow"] = calc_att(xwoba, exit_vel)
    player["vis"] = calc_att(k,whiff)
    player["disc"] = calc_att(bb, chase)
    
    add_player(player)
    print(player)
    
else:
    pass

