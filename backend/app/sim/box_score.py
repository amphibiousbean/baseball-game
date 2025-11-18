class box_score:
    HIT_TXT="{:<25}|{:<2}|{:<2}|{:<3}|{:<2}|{:<2}|" #NAME|AB|R|H|RBI|BB|K
    PITCH_TXT="{:<25}|{:<2}|{:<2}|{:<2}|{:<2}|{:<2}|{:<3}" #NAME|IP|ER|BB|K|HR|ERA

    def __init__(self, name, hitters, pitchers):
        self.name = name
        self.hitters=hitters
        self.pitchers=pitchers

    def print(self):

        hit_str=self.HIT_TXT.format("Batters", "AB", "H", "RBI","BB","K")
        pitch_str=self.PITCH_TXT.format("Pitchers", "IP", "ER","BB","K","HR","ERA")

        for hitter in self.hitters:
            log=hitter.game_log
            hit_str += "\n" + self.HIT_TXT.format(hitter.name, log["AB"],log["H"], log["RBI"], log["BB"], log["K"])
        for pitcher in self.pitchers:
            
            log=pitcher.game_log
            if log["pitched"]:
                dis_innings=(log["outs_made"] // 3) + (0.1*(log["outs_made"] % 3))
                calc_innings=(log["outs_made"] // 3) + ((1/3)*(log["outs_made"] % 3))
                era=(log["ER"]*9)/calc_innings
                pitch_str += "\n" + self.PITCH_TXT.format(pitcher.name, dis_innings, log["ER"], log["BB"], log["K"], log["HR"], era)
            else:
                pitch_str += "\n" + self.PITCH_TXT.format(pitcher.name, "0.0", log["ER"], log["BB"], log["K"], log["HR"], "---")

        box=self.name + "\n\n" + hit_str + "\n\n" + pitch_str
        print(box)

    def get_str(self):
        hit_str=self.HIT_TXT.format("Batters", "AB", "H", "RBI","BB","K")
        pitch_str=self.PITCH_TXT.format("Pitchers", "IP", "ER","BB","K","HR","ERA")

        for hitter in self.hitters:
            log=hitter.game_log
            hit_str += "\n" + self.HIT_TXT.format(hitter.name, log["AB"],log["H"], log["RBI"], log["BB"], log["K"])
        for pitcher in self.pitchers:
            
            log=pitcher.game_log
            if log["pitched"]:
                dis_innings=(log["outs_made"] // 3) + (0.1*(log["outs_made"] % 3))
                calc_innings=(log["outs_made"] // 3) + ((1/3)*(log["outs_made"] % 3))
                era=(log["ER"]*9)/calc_innings
                pitch_str += "\n" + self.PITCH_TXT.format(pitcher.name, dis_innings, log["ER"], log["BB"], log["K"], log["HR"], era)
            else:
                pitch_str += "\n" + self.PITCH_TXT.format(pitcher.name, "0.0", log["ER"], log["BB"], log["K"], log["HR"], "---")

        box=self.name + "\n\n" + hit_str + "\n\n" + pitch_str
        return box
    

    def get_dict(self):
        dict={}
        hitters_dict={}
        pitchers_dict={}
        for hitter in self.hitters:
            hitters_dict[hitter.name]=hitter.game_log
        for pitcher in self.pitchers:
            pitchers_dict[pitcher.name]=pitcher.game_log
        dict["hitters"]=hitters_dict
        dict["pitchers"]=pitchers_dict
        return dict