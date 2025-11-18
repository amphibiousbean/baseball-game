import json
import os

class stat_logger:

    FILENAME="stats.json"
    base_dir = os.path.dirname(os.path.dirname(__file__)) 
    FILEPATH= os.path.join(base_dir, 'resources', FILENAME)

    def __init__(self):
        try:
            with open(self.FILEPATH, 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
                print("error finding file : " + self.FILEPATH)
        except json.JSONDecodeError:
                print("JSONDecoderError detected : " + self.FILEPATH)
            
    #updates a player's overall stats
    def update_player(self, player):  #player : list of the names of batters or pitcher
        player_data=None
        if len(self.data) > 0:
            for index in self.data:
                if index["name"] == player.name:
                    player_data=index
                    break
            if player_data:
                for stat in player_data["stats"]:
                    player_data["stats"][stat] += player.game_log[stat]
                self.save()
            else: 
                self.create_new_player_stat(player)
        
        else:
            self.create_new_player_stat(player)

    
    #create a new entry to stats.json if needed
    def create_new_player_stat(self, player):
        new_player={
            "name" : player.name,
            "stats" : player.game_log
        }
        self.data.append(new_player)
        self.save()

    #saving data
    def save(self):
        with open(self.FILEPATH, 'w') as file:
            json.dump(self.data, file, indent=4)


    
        

            