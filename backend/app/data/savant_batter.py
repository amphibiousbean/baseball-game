from pybaseball import statcast_batter
from pybaseball import playerid_lookup
from pybaseball import batting_stats_bref
from datetime import date

ZONE_WIDTH = 0.94
ZONE_TOP = 3.5
ZONE_BOTTOM = 1.5



not_AB=['sac_bunt','sac_fly','hit_by_pitch', 'walk']
swing_events = ['swinging_strike', 'foul', 'foul_tip', 'hit_into_play', 'swinging_strike_blocked']
not_in_xba = ['walk','hit_by_pitch']

today = date.today()
f_date = today.strftime("%Y-%m-%d")
start_date='2025-03-26'

#returns the pybaseball dataframe for a player, removes truncated plate appearances
def pull_player_data(player):
    print(player)
    playerid=playerid_lookup(player[1], player[0], fuzzy=True).iloc[0]["key_mlbam"]
    data=statcast_batter(start_date, f_date, player_id=playerid)
    non_trunc=data[~data['events'].isin(['truncated_pa'])]
    return non_trunc

#returns dataframe with non-event actions filtered out. 
def filter_non_events(data):
    events=data[data['events'].notnull()]
    return events

#returns dataframe with only balls that were in play 
def only_batted_balls(data):
    batted_balls=data[data['description'].isin(['hit_into_play'])]
    return batted_balls

#remove walks and HBP, set strikeouts to 0
def filter_for_xba(data):
    data['estimated_ba_using_speedangle'].fillna(0,inplace=True)
    no_walks=data[~data['events'].isin(not_in_xba)]
    return no_walks

#filters actions that are not counted as an official at bat
def filter_non_AB(data):
    at_bats=data[~data['events'].isin(not_AB)]
    return at_bats

#returns a player's xBA.    
def get_xba(data):
    print("xBA : " + str(data.estimated_ba_using_speedangle.agg("mean")))
    return data.estimated_ba_using_speedangle.agg("mean")

#returns player's xwOBA
def get_xwoba(data):
    xwoba=data.estimated_woba_using_speedangle.agg("mean")
    print("xwOBA : " + str(xwoba))
    return data.estimated_woba_using_speedangle.agg("mean")

#returns player's avg exit velocity
def get_exit_vel(data):
    velo=data.launch_speed.agg("mean")
    print("Exit Velo : " + str(velo))
    return velo

#return player's BB%. 
def get_bb(data):
    walks = data[data['events'] == 'walk'].shape[0]
    bb=((walks/data.shape[0])*100)
    print("BB% : " +str(bb))
    return bb

#returns player's K%. 
def get_k(data):
    strikeouts = data[data['events'].isin(['strikeout'])].shape[0]
    k=((strikeouts/data.shape[0])*100)
    print("K% : " + str(k))
    return k

#returns player's whiff%.
def get_whiff(data):
    
    numerator=data[data['description'].isin(['swinging_strike', 'swinging_strike_blocked'])].shape[0]
    #numerator=data['swinging_strike'] + data['swinging_strike_blocked']
    denom=numerator+data[data['description'].isin(['foul', 'foul_tip','hit_into_play'])].shape[0]
    #denom=numerator+data['foul']+data['foul_tip']+data['hit_into_play']
    whiff_rate=(numerator/denom)*100
    print("Whiff % : " +str(whiff_rate))
    return whiff_rate

#returns player's chase%
def get_chase(data,sz):

    outside_zone = data[
        (data['plate_x'].abs() > ZONE_WIDTH) |
        (data['plate_z'] > sz[0]) |
        (data['plate_z'] < sz[1])
    ]

    outside_swings = outside_zone[outside_zone['description'].isin(swing_events)]
    total_outside = len(outside_zone)
    swings_outside = len(outside_swings)
    if total_outside > 0:
        chase=(swings_outside / total_outside) * 100
        print("Chase% : " + str(chase))
        return chase
    else:
        print("Chase% : never")
        return 0
    
#return player's launch angle sweet spot %. "sweet spot" = 8-32 degrees
def get_la_ss_rate(data):
    sweet_spots=data.loc[lambda x : (x['launch_angle'] >= 8) & (x['launch_angle'] <= 32)].shape[0]
    ss_rate=(sweet_spots/(data.shape[0]))*100
    print("Sweet Spot % : " + str(ss_rate))
    return ss_rate

#return player's rate of solid contact
def get_solid_con_rate(data):
    solid_con=data[data['launch_speed_angle'].isin([5])].shape[0]
    rate=(solid_con/data.shape[0])*100
    print("Solid Con % : " + str(rate))
    return rate

#return player's barrel rate
def get_barrel_rate(data):
    barrel=data[data['launch_speed_angle'].isin([6])].shape[0]
    rate=(barrel/data.shape[0])*100
    print("Barrel % : " + str(rate))
    return rate

#returns player's hard hit %
def get_hard_hit(data):
    hard_hit=data[data['launch_speed'] >= 95].shape[0]
    rate=(hard_hit/data.shape[0])*100
    print("Hard Hit % : " + str(rate))
    return rate

#returns the average exit velocity for the top 50% of batted balls
def get_ev50(data):
    mid=len(data) // 2
    sorted_df=data.sort_values(by='launch_speed',ascending=False)
    top_50_percent=sorted_df.head(int(len(sorted_df) * 0.5))
    velo=top_50_percent['launch_speed'].mean()
    print("EV50 : " +str(velo))
    return velo

#returns the player's in-zone whiff % (Z-whiff rate)
def get_zone_whiff(data,sz):
    inside_zone = data[
        (data['plate_x'].abs() <= ZONE_WIDTH) |
        (data['plate_z'] <= sz[0]) |
        (data['plate_z'] >= sz[1])
    ]
    inside_whiffs = inside_zone[inside_zone['description'].isin(["swinging_strike"])].shape[0]
    total_inside = inside_zone[inside_zone['description'].isin(swing_events)].shape[0]
    z_whiff=(inside_whiffs/total_inside)*100
    print("Z-Whiff % : " +str(z_whiff))
    return z_whiff


    