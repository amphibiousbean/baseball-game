import json

FILE_IN='stats.json'

try:
    with open(FILE_IN, 'r') as file:
        data = json.load(file)
except FileNotFoundError:
        print("error finding file : " + FILE_IN)
except json.JSONDecodeError:
        print("JSONDecoderError detected : " + FILE_IN)

table_head_bat=f"|{'Name':<20}|{'AVG':<5}|{'HR':<3}|{'RBI':<4}|{'OBP':<5}|{'SLG':<5}|{'OPS':<5}|\n"
table_head_pitch=f"|{'Name':<20}|{'ERA':<4}|{'IP':<7}|{'K':<4}|{'WHIP':<5}|{'K/9':<4}|{'H/9':<5}|{'BB/9':<4}|\n"
bat_table=table_head_bat
pitch_table=table_head_pitch

for player in data:
   
   name=player['name']
   stats=player['stats']

   if 'pitched' in stats:

      dis_innings=(stats["outs_made"] // 3) + (0.1*(stats["outs_made"] % 3))
      calc_innings=(stats["outs_made"] // 3) + ((1/3)*(stats["outs_made"] % 3))
      era=(stats['ER']*9)/calc_innings
      k=stats['K']
      whip=(stats['H']+stats['BB'])/calc_innings
      h_9=(stats['H']*9)/calc_innings
      k_9=(stats['K']*9)/calc_innings
      bb_9=(stats['BB']*9)/calc_innings

      new_row=f"|{name:<20}|{round(era,2):<4}|{dis_innings:<7}|{k:<4}|{round(whip,3):<5}|{round(k_9,2):<4}|{round(h_9,2):<5}|{round(bb_9,2):<4}|\n"
      pitch_table+=new_row

   else:
      
      avg=stats['H']/stats['AB']
      hr=stats['HR']
      rbi=stats['RBI']
      obp=(stats['H']+stats['BB'])/(stats['AB']+stats['BB'])
      slg=(stats['1B'] + (2*stats['2B']) + (3*stats['3B']) + (4*hr))/stats['AB']
      ops=obp+slg

      new_row=f"|{name:<20}|{round(avg,3):<5}|{hr:<3}|{rbi:<4}|{round(obp,3):<5}|{round(slg,3):<5}|{round(ops,3):<5}|\n"
      bat_table+=new_row
      
print(bat_table)
print("\n\n\n")
print(pitch_table)