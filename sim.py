import Pitcher as Pitcher
import Batter as Batter

home_runs_by_inning = []
away_runs_by_inning = []

def main():

    test_pitcher = Pitcher.Pitcher("Nola", 60, 70, 85, 40, 75, 80, ["Knuckle Curve", "Four Seamer", "Sinker", "Changeup", "Cutter"])
    test_batter = Batter.Batter("Harper", 80, 70, 55, 90)
    test_pitcher.print()
    test_batter.print()
    printScoreboard(0,0,0,0)







def printScoreboard(inning, outs, batter, pitcher):
    scoreboard ="""----------------------------------------------------------------------------------------------------------------------
|                                                                                                                    |
|                                                                                                                    |
|                                                                                                                    |
|                                                                                                                    |
|                                                                                                                    |
|                                                                                                                    |
---------------------------------------------------------------------------------------------------------------------- 
                """
    print(scoreboard)
if __name__ == '__main__':
    main()

