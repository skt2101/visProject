from lib import utils
import numpy as np
leagues = utils.getAllDatafromTable('league')
countries = utils.getAllDatafromTable('country')
countryNameMap = dict()
for country in countries:
    countryNameMap[country[0]]=country[1]
matches = utils.getAllDatafromTable('match')
leagueScoreMap = dict()
for league in leagues:
    leagueScoreMap[league[0]] = []
for match in matches:
    home_team_goals = int(match[9])
    away_team_goals = int(match[10])
    if home_team_goals == away_team_goals:
        home_team_score = 1
        away_team_score = 1
    elif home_team_goals > away_team_goals:
        home_team_score = 3
        away_team_score = 0
    else:
        away_team_score = 3
        home_team_score = 0
    leagueScoreMap[match[2]].append([home_team_score,away_team_score])
avgLeagueScore = dict()
for league in leagueScoreMap.keys():
    scores = leagueScoreMap.get(league)
    avg_home_score = np.mean([score[0] for score in scores])
    avg_away_score = np.mean([score[1] for score in scores])
    avgLeagueScore[league] = [avg_home_score,avg_away_score]
data = []
for league in avgLeagueScore.keys():
    avg_home_score = avgLeagueScore.get(league)[0]
    avg_away_score = avgLeagueScore.get(league)[1]
    countryName = countryNameMap.get(league)
    data.append([countryName,avg_home_score,avg_away_score])
utils.createFile(data,"homeAdvantage.csv",["country","avg_home_score","avg_away_score"])