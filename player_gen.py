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
    "chase" : 6.2,
    "sweet_spot" : 4.4,
    "solid_con" : 2.2,
    "barrel_rate" : 4.9,
    "hard_hit" : 8.5,
    "ev50" : 2.6,
    "z_whiff" : 5.3
}

avg_bat = {
    "exit_vel" : 88.5,
    "xba" : .245,
    "xwoba" : .315,
    "bb" : 8.4,
    "k" : 22.2,
    "whiff" : 23.1,
    "chase" : 27.5,
    "sweet_spot" : 35.1,
    "solid_con" : 6.7,
    "barrel_rate" : 9.9,
    "hard_hit" : 43.5,
    "ev50" : 100.9,
    "z_whiff" : 16.1

}


def calc_att(atts):
    att=round(50+(sum(atts)))
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
player_name=tuple(name.lower().split(' '))
#playerid=playerid_lookup(player[1], player[0]).iloc[0]["key_mlbam"]
if mode == "b":
    
    player={
        "type" : "Batter",
        "name" : name
        }
    #setting dataframes
    data=batter.pull_player_data(player_name)
    events=batter.filter_non_events(data)
    xba_filter=batter.filter_for_xba(events)
    at_bats=batter.filter_non_AB(data)
    batted_balls=batter.only_batted_balls(data)

    #setting batter's strike zone
    top_zone=data['sz_top'].agg('mean')
    bot_zone=data['sz_bot'].agg('mean')
    sz=[top_zone, bot_zone]

    #getting stat impact
    exit_vel=calc_stat_impact(batter.get_exit_vel(events), "exit_vel")
    xwoba=calc_stat_impact(batter.get_xwoba(events), "xwoba")
    xba=calc_stat_impact(batter.get_xba(xba_filter), "xba")
    bb=calc_stat_impact(batter.get_bb(events), "bb")
    k=calc_stat_impact(batter.get_k(events),"k", invert=True)
    whiff=calc_stat_impact(batter.get_whiff(data),"whiff", invert=True)
    chase=calc_stat_impact(batter.get_chase(data,sz),"chase",invert=True)
    sweet_spot=calc_stat_impact(batter.get_la_ss_rate(batted_balls), "sweet_spot")
    solid_con=calc_stat_impact(batter.get_solid_con_rate(batted_balls), "solid_con")
    barrel_rate=calc_stat_impact(batter.get_barrel_rate(batted_balls), "barrel_rate")
    hard_hit=calc_stat_impact(batter.get_hard_hit(batted_balls), "hard_hit")
    ev50=calc_stat_impact(batter.get_ev50(batted_balls), "ev50")
    z_whiff=calc_stat_impact(batter.get_zone_whiff(data,sz),"z_whiff", invert=True)
    
    #list to pass to calc_att
    con=[xba*0.3, solid_con*0.3, sweet_spot*0.3,exit_vel*0.1]
    pow=[xwoba*0.2,barrel_rate*0.1, hard_hit*0.4, ev50*0.3]
    vis=[z_whiff*0.25, bb*0.25, whiff*0.5]
    disc=[chase*0.5, k*0.2, bb*0.3]    

    #calculating attributes
    player["con"] = calc_att(con)
    player["pow"] = calc_att(pow)
    player["vis"] = calc_att(vis)
    player["disc"] = calc_att(disc)
    
    #adding to players.json, printing to cmd
    add_player(player)
    print(player)
    
else:
    pass

