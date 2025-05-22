from pybaseball import statcast_batter
from pybaseball import playerid_lookup
from pybaseball import batting_stats_bref
from datetime import date

ZONE_WIDTH = 0.83
ZONE_TOP = 3.5
ZONE_BOTTOM = 1.5

not_AB=['sac_bunt','sac_fly','hit_by_pitch', 'walk']
swing_events = ['swinging_strike', 'foul', 'foul_tip', 'hit_into_play']

today = date.today()
f_date = today.strftime("%Y-%m-%d")
start_date='2024-03-28'

#returns the pybaseball dataframe for a player
def pull_player_data(player):
    playerid=playerid_lookup(player[1], player[0]).iloc[0]["key_mlbam"]
    data=statcast_batter(start_date, f_date, player_id=playerid)
    return data

#returns dataframe with non-event actions filtered out. 
def filter_non_events(data):
    batted_balls=data[data['events'].notnull()]
    batted_balls['estimated_ba_using_speedangle'].fillna(0, inplace=True)
    return batted_balls

#filters actions that are not counted as an official at bat
def filter_non_AB(data):
    at_bats=data[~data['events'].isin(not_AB)]
    return at_bats

#returns a player's xBA.    
def get_xba(data):
    return data.estimated_ba_using_speedangle.agg("mean")

#returns player's xwOBA
def get_xwoba(data):
    return data.estimated_woba_using_speedangle.agg("mean")

#returns player's avg exit velocity
def get_exit_vel(data):
    return data.launch_speed.agg("mean")

#return player's BB%. 
def get_bb(data):
    walks = data[data['events'] == 'walk'].shape[0]
    bb=((walks/data.shape[0])*100)
    return bb

#returns player's K%. 
def get_k(data):
    strikeouts = data[data['events'].isin(['strikeout', 'strikeout_swinging', 'strikeout_looking'])].shape[0]
    k=((strikeouts/data.shape[0])*100)
    return k

#returns player's whiff%.
def get_whiff(data):
    numerator=data['swinging_strike'] + data['swinging_strike_blocked']
    denom=numerator+data['foul']+data['foul_tip']+data['hit_into_play']
    whiff_rate=(numerator/denom)*100
    return whiff_rate

#returns player's chase%
def get_chase(data):

    outside_zone = data[
        (data['plate_x'].abs() > ZONE_WIDTH) |
        (data['plate_z'] > ZONE_TOP) |
        (data['plate_z'] < ZONE_BOTTOM)
    ]

    outside_swings = outside_zone[outside_zone['description'].isin(swing_events)]
    total_outside = len(outside_zone)
    swings_outside = len(outside_swings)

    return (swings_outside / total_outside) * 100 if total_outside > 0 else 0