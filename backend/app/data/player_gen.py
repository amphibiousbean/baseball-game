import backend.app.data.savant_batter as batter
import backend.app.data.savant_pitcher as pitcher
from pybaseball import statcast_batter
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
from pybaseball import batting_stats_bref
from datetime import date
import json

#TODO: refactor this all into multiple files to separate stat collection from the attribute conversion


ZONE_WIDTH = 0.83

FILEPATH="players.json"
TEAM_FILE="teams.json"

def add_player(player):
    try:
        with open(FILEPATH, 'r') as file:
            data = json.load(file)
            
    except FileNotFoundError:
        print("error finding file :" + FILEPATH)
    
    data.append(player)
    with open(FILEPATH, 'w') as file:
        
        json.dump(data, file, indent = 4)
    

stdev_bat={
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

velo_avg={
    "Four-seam Fastball" : 94.26,
    "Sinker" : 93.58,
    "Cutter" : 89.49,
    "Slider" : 85.8,
    "Changeup" : 86.36,
    "Curveball" : 79.76,
    "Splitter" : 86.73,
    "Sweeper" : 82.17,
    "Slurve" : 81.3,
    "Knuckle-curve" : 80.4
}

velo_stdev={
    "Four-seam Fastball" : 2.38,
    "Sinker" : 2.51,
    "Cutter" : 2.7,
    "Slider" : 2.66,
    "Changeup" : 3.31,
    "Curveball" : 3.51,
    "Splitter" : 3.2,
    "Sweeper" : 2.85,
    "Slurve" : 2.23,
    "Knuckle-curve" : 3.51

}

avg_pitch={
    "k" : 21.8,
    "bb" : 7.9,
    "xwoba" : 0.327,
    "xwobacon" : 0.383,
    "xba" : 0.256,
    "xbacon" : 0.383,
    "sweet_spot" : 33.9,
    "barrel_rate" : 8.7,
    "hard_hit" : 41.5,
    "ev50" : 78.8
}

stdev_pitch={
    "k" : 5.3,
    "bb" : 2.3,
    "xwoba" : 0.039,
    "xwobacon" : 0.031,
    "xba" : 0.028,
    "xbacon" : 0.025,
    "sweet_spot" : 3.9,
    "barrel_rate" : 2.1,
    "hard_hit" : 4.7,
    "ev50" : 4.7
}

def calc_att(atts):
    att=round(50+(sum(atts)))
    return max(20, min(80, att))

def calc_velo(velo):
    velo_atts={}
    for pitch in velo:
        att=round(50+velo[pitch])
        velo_atts[pitch] = max(20, min(80,att))
    return velo_atts

def calc_stat_impact_bat(x, stat, invert=False):
    
    mean = avg_bat[stat]
    std = stdev_bat[stat]
    

    if std == 0:
        return 0

    z = (x - mean) / std
    scaler=10*z
    if invert:
        scaler*=-1
    return scaler  

def calc_stat_impact_pitch(x, stat, invert=False):
    
    mean = avg_pitch[stat]
    std = stdev_pitch[stat]
    

    if std == 0:
        return 0

    z = (x - mean) / std
    scaler=10*z
    if invert:
        scaler*=-1
    return scaler


def calc_velo_impact(velo):
    dict={}
    for pitch in velo:
        x=velo[pitch]
        mean=velo_avg[pitch]
        std=velo_stdev[pitch]
        if std==0:
            return 0
        z = (x-mean) / std
        scaler=10*z
        dict[pitch]=scaler
    return dict
    



###########################    SCRIPT    ######################################
looping=True

while looping:
    mode=""
    team_query=""

    while team_query != "player" or "team":
        team=False
        team_query=input("Type \"player\" for a single player or \"team\" for a team : ")
        if team_query == "player" or "team":
            if team_query == "team":
                team=True
                break
            else:
                break
    
    while mode != "b" or "p":
        mode=input("Type \"p\" for pitcher(s) or \"b\" for batter(s) : ")
        if mode == "b" or "p":
            break

    if mode == "b" or "p":
        loop_count=1
        if team:

            team_loop=True

            while team_loop:
                name=input("Enter team name :")
                try:
                    with open(TEAM_FILE, 'r') as file:
                        data = json.load(file)
                except FileNotFoundError:
                    print("error finding file : " + TEAM_FILE)
                except json.JSONDecodeError:
                    print("JSONDecoderError detected : " + TEAM_FILE)

                try:
                    team_data=data[name]
                    
                except KeyError:
                    print("KeyError : key \'" + name + "\' was not found in " + TEAM_FILE + ", please try again.")
                    continue
                team_loop=False

        else:
            name=input("Enter player name : ")
            player_name=tuple(name.lower().split(' '))
            id_res=playerid_lookup(player_name[1], player_name[0], fuzzy=True)
            if id_res.empty:
                print(print(f"No player found for: {player_name[1]} {player_name[0]}. Please try again"))
                continue
    #playerid=playerid_lookup(player[1], player[0]).iloc[0]["key_mlbam"]


    if mode == "b":
        if team:
            names=team_data["batters"]
            loop_count=len(names)

        while loop_count>0:

            if team:
                json_name=names[loop_count-1]
                player_name=tuple(names[loop_count-1].lower().split(' '))
                
                
            #setting dataframes
            data=batter.pull_player_data(player_name)
            events=batter.filter_non_events(data)
            xba_filter=batter.filter_for_xba(events)
            at_bats=batter.filter_non_AB(data)
            batted_balls=batter.only_batted_balls(data)


            player={
                "type" : "Batter",
                "name" : json_name
                }

            #setting batter's strike zone
            top_zone=data['sz_top'].agg('mean')
            bot_zone=data['sz_bot'].agg('mean')
            sz=[top_zone, bot_zone]

            #getting stat impact
            exit_vel=calc_stat_impact_bat(batter.get_exit_vel(events), "exit_vel")
            xwoba=calc_stat_impact_bat(batter.get_xwoba(events), "xwoba")
            xba=calc_stat_impact_bat(batter.get_xba(xba_filter), "xba")
            bb=calc_stat_impact_bat(batter.get_bb(events), "bb")
            k=calc_stat_impact_bat(batter.get_k(events),"k", invert=True)
            whiff=calc_stat_impact_bat(batter.get_whiff(data),"whiff", invert=True)
            chase=calc_stat_impact_bat(batter.get_chase(data,sz),"chase",invert=True)
            sweet_spot=calc_stat_impact_bat(batter.get_la_ss_rate(batted_balls), "sweet_spot")
            solid_con=calc_stat_impact_bat(batter.get_solid_con_rate(batted_balls), "solid_con")
            barrel_rate=calc_stat_impact_bat(batter.get_barrel_rate(batted_balls), "barrel_rate")
            hard_hit=calc_stat_impact_bat(batter.get_hard_hit(batted_balls), "hard_hit")
            ev50=calc_stat_impact_bat(batter.get_ev50(batted_balls), "ev50")
            z_whiff=calc_stat_impact_bat(batter.get_zone_whiff(data,sz),"z_whiff", invert=True)
            
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
        
            add_player(player)
            print("\n\n" + str(player))
            loop_count-=1

    else:
        if team:
            names=team_data['pitchers']
            loop_count=len(names)

        while loop_count>0:
            
            if team:
                json_name=names[loop_count-1]
                player_name=tuple(names[loop_count-1].lower().split(' '))

            player = {
                "type" : "Pitcher",
                "name" : json_name
            }

            #setting dataframes
            data=pitcher.pull_player_data(player_name)
            events=pitcher.filter_non_events(data)
            xba_filter=pitcher.filter_for_xba(events)
            #at_bats=pitcher.filter_non_AB(data)
            batted_balls=pitcher.only_batted_balls(data)
            """
            pitcher : 
            velo : straightforward
            k : straight forward
            bb : straight forward
            hr rate : ev50, barrel%, xwoba, hardhit %
            hit rate : xba, sweetspot%, xbacon
            control : bb%, 
            """

            k = calc_stat_impact_pitch(pitcher.get_k(events), "k")
            bb = calc_stat_impact_pitch(pitcher.get_bb(events), "bb", invert=True)
            ev50 = calc_stat_impact_pitch(pitcher.get_ev50(batted_balls), "ev50", invert=True)
            barrel = calc_stat_impact_pitch(pitcher.get_barrel_rate(batted_balls), "barrel_rate", invert=True)
            xwoba = calc_stat_impact_pitch(pitcher.get_xwoba(events), "xwoba", invert=True)
            xwobacon = calc_stat_impact_pitch(pitcher.get_xwoba(batted_balls), "xwobacon", invert=True)
            hard_hit = calc_stat_impact_pitch(pitcher.get_hard_hit(batted_balls), "hard_hit", invert=True)
            xba = calc_stat_impact_pitch(pitcher.get_xba(xba_filter), "xba", invert=True)
            xbacon = calc_stat_impact_pitch(pitcher.get_xba(batted_balls), "xbacon", invert=True)
            sweet_spot = calc_stat_impact_pitch(pitcher.get_la_ss_rate(batted_balls), "sweet_spot", invert=True)
            velos = calc_velo_impact(pitcher.get_velo(data))

            hr=[ev50*0.3, barrel*0.2,hard_hit*0.3,xwoba*0.1]
            hit=[xwobacon*0.15,xba*0.3,xbacon*0.3,sweet_spot*0.15]

            player["velo"]=calc_velo(velos)
            player["stuff"]=calc_velo(velos) #PLACEHOLDER FOR NOW JUST TO TEST FUNCTIONALITY OF MOVING PITCHER TO SIM
            player["K/9"] = calc_att([k])
            player["BB/9"] = calc_att([bb])
            player["HR/9"] = calc_att(hr)
            player["H/9"] = calc_att(hit)
            player["control"] = calc_att([bb]) #PLACEHOLDER FOR NOW JUST TO TEST FUNCTIONALITY OF MOVING PITCHER TO SIM


            #adding to players.json, printing to cmd
            add_player(player)
            print("\n\n" + str(player))
            loop_count-=1

    exit_code=input("\n\nType \"exit\" to exit, any other key to add another player/team. ")
    if exit_code=="exit":
        looping=False


