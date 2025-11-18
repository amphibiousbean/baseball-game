from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
from datetime import date


today = date.today()
f_date = today.strftime("%Y-%m-%d")
start_date='2025-03-26'

not_in_xba = ['walk','hit_by_pitch']

PITCH_TYPES = {
    "FF" : "Four-seam Fastball",
    "SI" : "Sinker",
    "ST" : "Sweeper",
    "FS" : "Splitter",
    "FC" : "Cutter",
    "CU" : "Curveball",
    "SL" : "Slider",
    "CH" : "Changeup",
    "KC" : "Knuckle-curve",
    "SV" : "Slurve",
    "KN" : "Knuckleball",
    "SC" : "Screwball",
    "FO" : "Forkball"
}
pitch_out='PO'
#returns the pybaseball dataframe for a player, removes truncated plate appearances
def pull_player_data(player):
    print(player)
    playerid=playerid_lookup(player[1], player[0]).iloc[0]["key_mlbam"]
    data=statcast_pitcher(start_date, f_date, player_id=playerid)
    return data[data['pitch_type'] != pitch_out]

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

#return's a list of the player's pitch arsenal
def get_pitches(data):
    unique_pitches=data['pitch_type'].unique()
    pitches=[]
    for pitch in unique_pitches:
        pitches.append(PITCH_TYPES[pitch])
    print(pitches)
    return pitches

#returns player's xwOBA
def get_xwoba(data):
    xwoba=data.estimated_woba_using_speedangle.agg("mean")
    print("xwOBA : " + str(xwoba))
    return data.estimated_woba_using_speedangle.agg("mean")

#returns a player's xBA.    
def get_xba(data):
    print("xBA : " + str(data.estimated_ba_using_speedangle.agg("mean")))
    return data.estimated_ba_using_speedangle.agg("mean")

#return player's launch angle sweet spot %. "sweet spot" = 8-32 degrees
def get_la_ss_rate(data):
    sweet_spots=data.loc[lambda x : (x['launch_angle'] >= 8) & (x['launch_angle'] <= 32)].shape[0]
    ss_rate=(sweet_spots/(data.shape[0]))*100
    print("Sweet Spot % : " + str(ss_rate))
    return ss_rate

#return's the barrel rate of the balls in play
def get_barrel_rate(data):
    barrel=data[data['launch_speed_angle'].isin([6])].shape[0]
    rate=(barrel/data.shape[0])*100
    print("Barrel % : " + str(rate))
    return rate

#returns the average exit velocity for the bottom 50% of batted balls
def get_ev50(data):
    sorted_df=data.sort_values(by='launch_speed',ascending=True)
    top_50_percent=sorted_df.head(int(len(sorted_df) * 0.5))
    velo=top_50_percent['launch_speed'].mean()
    print("EV50 : " +str(velo))
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

#returns player's hard hit %
def get_hard_hit(data):
    hard_hit=data[data['launch_speed'] >= 95].shape[0]
    rate=(hard_hit/data.shape[0])*100
    print("Hard Hit % : " + str(rate))
    return rate

#returns a dictionary of the average velocity for each of the pitcher's pitches
def get_velo(data):
    full_name_dict={}
    avg_velos=data.groupby('pitch_type')['release_speed'].mean()
    dict=avg_velos.to_dict()
    for pitch in dict:
        full_name_dict[PITCH_TYPES[pitch]] = dict[pitch]
    print(full_name_dict)
    return full_name_dict


