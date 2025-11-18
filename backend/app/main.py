from fastapi import FastAPI
import backend.app.sim.sim as sim
import backend.app.config as config
import backend.app.models.Team as Team

PHI=[
    "Trea Turner",
    "Kyle Schwarber",
    "Bryce Harper",
    "Alec Bohm",
    "J.T. Realmuto",
    "Brandon Marsh",
    "Harrison Bader",
    "Max Kepler",
    "Bryson Stott"
]
BOS=[
    "Jarren Duran",
    "Rafael Devers",
    "Wilyer Abreu",
    "Romy Gonzalez",
    "Alex Bregman",
    "Trevor Story",
    "Ceddanne Rafaela",
    "Connor Wong",
    "Kristian Campbell"
]
PHI_ROT=[
    "Zack Wheeler",
    "Cristopher S\u00e1nchez",
    "Ranger Su\u00e1rez",
    "Aaron Nola",
    "Jes\u00fas Luzardo"
    ]
BOS_ROT=[
    "Garrett Crochet",
    "Brayan Bello",
    "Lucas Giolito",
    "Walker Buehler",
    "Hunter Dobbins"
    ]

home_team = Team.Team("Phillies", PHI, PHI_ROT)
away_team = Team.Team("Red Sox", BOS, BOS_ROT)

app=FastAPI()

@app.get("/")
async def root():
    return {"Message" : "Hello World"}

@app.get("/simulate")
async def simulate(count : int):
    home_team = Team.Team("Phillies", PHI, PHI_ROT)
    away_team = Team.Team("Red Sox", BOS, BOS_ROT)
    games=[]
    for i in range(count):
        game_id=str(i)
        winner, loser,home_away, home_box, away_box,home_score,away_score =sim.startGame(home_team,away_team)
        result={"game_id" : i, 
                "winner" : winner,
                "loser" : loser,
                "home" : home_away["home"],
                "away" : home_away["away"],
                "home_score" : home_score,
                "away_score" : away_score,
                "home_box" : home_box.get_dict(),
                "away_box" : away_box.get_dict()}
        games.append(result)
    return games
