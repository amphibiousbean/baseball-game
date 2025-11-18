using System.Collections.Generic;
using System.Text.Json.Serialization;
using Microsoft.AspNetCore.SignalR;

public class Game
{
    [JsonPropertyName("game_id")]
    public int GameId {get;set;}
    public string? Winner {get;set;}
    public string? Loser {get;set;}
    public string? Home {get;set;}
    public string? Away {get;set;}
    [JsonPropertyName("home_score")]
    public Score? HomeScore{get;set;}
    [JsonPropertyName("away_score")]
    public Score? AwayScore{get;set;}
    [JsonPropertyName("home_box")]
    public BoxScore? HomeBox{get;set;}
    [JsonPropertyName("away_box")]
    public BoxScore? AwayBox{get;set;}
}

public class Score
{
    public int Runs{get;set;}
    public int Hits {get;set;}
    public int Walks{get;set;}
    [JsonPropertyName("by_inning_runs")]
    public List<int>? ByInningRuns{get;set;}
    public int Inning{get;set;}
    [JsonPropertyName("curr_inning_runs")]
    public int CurrInningRuns{get;set;}

}

public class BoxScore
{
    public Dictionary<string, PlayerStats>? Hitters{get;set;}
    public Dictionary<string, PitcherStats>? Pitchers{get;set;}
}

public class PlayerStats
{
    public int AB{get;set;}
    public int H{get;set;}
    public int RBI{get;set;}
    public int BB{get;set;}
    public int K{get;set;}
    [JsonPropertyName("1B")]
    public int Singles{get;set;}
    [JsonPropertyName("2B")]
    public int Doubles{get;set;}
    [JsonPropertyName("3B")]
    public int Triples{get;set;}
    public int HR{get;set;}

}

public class PitcherStats
{
    public bool Pitched{get;set;}
    [JsonPropertyName("outs_made")]
    public int OutsMade{get;set;}
    public int H{get;set;}
    public int ER{get;set;}
    public int BB{get;set;}
    public int K{get;set;}
    public int HR{get;set;}
}