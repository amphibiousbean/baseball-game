import Team as Team
import Pitcher as Pitcher
import Batter as Batter

home_runs_by_inning = [1,0,2,0]
away_runs_by_inning = [1,1,0,0]

def main():
    displayScore()
    home_team = Team.Team("Phillies")
    away_team = Team.Team("Red Sox")
    print(home_team.strBasic())
    #displayTeamDetails(home_team)
    #displayTeam(away_team)


def displayScore():
    
    home = ""
    away = ""

    for x in range(9):
        if x < len(home_runs_by_inning):
            home += "  " + str(home_runs_by_inning[x])
        else:
            home += "   "

    home += "  " + str(sum(home_runs_by_inning))

    for x in range(9):
        if x < len(away_runs_by_inning):
            away += "  " + str(away_runs_by_inning[x])
        else:
            away += "   "
    
    away += "  " + str(sum(away_runs_by_inning))

    dis = "      1  2  3  4  5  6  7  8  9  T\nAway" + away + "\nHome" + home
    
    print(dis)


    
def makeScoreboard(inning, outs, batter, pitcher):
    
    return None

def displayTeamDetails(team):
    r =  team.name + "\n"
    count = 1
    for player in team.pitchers:
            r += "\nSP: " + player.str() + "\n"
    for player in team.batters:
            r += str(count) + ". " + player.str() + "\n"
            count += 1
    
    print(r)


if __name__ == '__main__':
    main()