import Pitcher as Pitcher
import Batter as Batter

home_runs_by_inning = []
away_runs_by_inning = []

def main():

    scoreboard = makeScoreboard(0,0,0,0)
    print(scoreboard)
    teamA = makeTeam()
    teamB = makeTeam()
    #displayTeam(teamA)
    #displayTeam(teamB)


def makeTeam():
    team = []
    for x in range(10):
        if x < 9:
            team.append(Batter.Batter("Joe Random", 50, 50, 50, 50))
        else:
            team.append(Pitcher.Pitcher("Mary Jane", 50, 50 ,50 ,50 ,50 ,50, ["Four Seamer", "Slider", "Changeup", "Curveball"]))
    return team

def displayTeam(team):
    r =  ""
    count = 1
    for player in team:
        if(player.type == "Pitcher"):
            r += "\nSP :\n" + player.toString() + "\n"
        else:
            r += str(count) + ".\n" + player.toString() + "\n"
            count += 1
    
    print(r)
         
def makeScoreboard(inning, outs, batter, pitcher):
    scoreboard ="""----------------------------------------------------------------------------------------------------------------------
|                                                                                                                    |
|                                                                                                                    |
|                                                                                                                    |
|                                                                                                                    |
|                                                                                                                    |
|                                                                                                                    |
---------------------------------------------------------------------------------------------------------------------- 
                """
    return scoreboard
if __name__ == '__main__':
    main()

