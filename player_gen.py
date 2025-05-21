from pybaseball import statcast_batter
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
from pybaseball import batting_stats_bref
from datetime import date
import json

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
    
def get_chase(outside_zone):
    outside_swings = outside_zone[outside_zone['description'].isin(swing_events)]

    total_outside = len(outside_zone)
    swings_outside = len(outside_swings)

    return (swings_outside / total_outside) * 100 if total_outside > 0 else 0


today = date.today()
f_date = today.strftime("%Y-%m-%d")
start_date='2024-03-28'
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
    not_AB=['sac_bunt','sac_fly','hit_by_pitch', 'walk']
    swing_events = ['swinging_strike', 'foul', 'foul_tip', 'hit_into_play']

    data=statcast_batter(start_date, f_date, player_id=playerid)

    outside_zone = data[
        (data['plate_x'].abs() > ZONE_WIDTH) |
        (data['plate_z'] > ZONE_TOP) |
        (data['plate_z'] < ZONE_BOTTOM)
    ]

    batted_balls=data[data['events'].notnull()]
    batted_balls['estimated_ba_using_speedangle'].fillna(0, inplace=True)
    at_bats=batted_balls[~batted_balls['events'].isin(not_AB)]

    #walks+k
    walks = batted_balls[batted_balls['events'] == 'walk'].shape[0]
    strikeouts = batted_balls[batted_balls['events'].isin(['strikeout', 'strikeout_swinging', 'strikeout_looking'])].shape[0]
    total_pa=batted_balls.shape[0]
    bb=((walks/total_pa)*100)
    k=((strikeouts/total_pa)*100)

    #whiffs+chase
    desc_group=data.groupby('description').size()
    numerator=desc_group['swinging_strike'] + desc_group['swinging_strike_blocked']
    denom=numerator+desc_group['foul']+desc_group['foul_tip']+desc_group['hit_into_play']
    whiff_rate=(numerator/denom)*100
    chase_rate=get_chase(outside_zone)

    #everything else
    exit_vel=calc_stat_impact(batted_balls.launch_speed.agg("mean"), "exit_vel")
    xwoba=calc_stat_impact(batted_balls.estimated_woba_using_speedangle.agg("mean"), "xwoba") #TODO: take difference of their stats from the average and compare it to the difference of the max/min to the avg
    xba=calc_stat_impact(at_bats.estimated_ba_using_speedangle.agg("mean"), "xba")
    bb=calc_stat_impact(bb, "bb")
    k=calc_stat_impact(k,"k", invert=True)
    whiff=calc_stat_impact(whiff_rate,"whiff", invert=True)
    chase=calc_stat_impact(chase_rate,"chase",invert=True)

    player["con"] = calc_att(xba,whiff)
    player["pow"] = calc_att(xwoba, exit_vel)
    player["vis"] = calc_att(k,whiff)
    player["disc"] = calc_att(bb, chase)
    
    add_player(player)
    print(player)
    
    

else:
    data=statcast_pitcher(start_date, f_date, player_id=playerid)

#print(data)
